"""
predict.py – Inference pipeline.

Generates probability maps for all horizons at a given T0.
Supports both DEMO (synthetic) and REAL data modes.

Output format:
  Grid-based: latitude, longitude, horizon, thunderstorm_probability, lightning_probability
  Summary: max probability, region summary
"""
from __future__ import annotations

import pickle
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.config import AppConfig
from src.preprocessing.grid import CommonGrid
from src.ingestion.synthetic import SyntheticDataGenerator
from src.ingestion.lightning import grid_lightning_features
from src.preprocessing.temporal import build_input_sequence, check_no_leakage
from src.features.radar_features import extract_radar_features
from src.features.satellite_features import extract_satellite_features
from src.features.nwp_features import extract_nwp_features
from src.logger import get_logger

log = get_logger("inference.predict")

LOOKBACK_MIN = 60
STEP_MIN = 15


class NowcastPredictor:
    """
    Runs inference for all (target, horizon) combinations
    at a given T0 time, producing probability maps.
    """

    def __init__(
        self,
        config: AppConfig,
        grid: CommonGrid,
        models: dict,                # "thunderstorm_15m" → BaseNowcastModel
        feature_cols: list[str],
        calibrators: dict | None = None,  # same keys → ProbabilityCalibrator
    ):
        self.config = config
        self.grid = grid
        self.models = models
        self.feature_cols = feature_cols
        self.calibrators = calibrators or {}

    def predict_at_t0(
        self,
        t0: datetime,
        synthetic_gen: SyntheticDataGenerator | None = None,
    ) -> dict[str, Any]:
        """
        Generate probability maps for all horizons at T0.

        ⚠ Only data ≤ T0 is used. Future leakage check is applied.

        Args:
            t0: Analysis time.
            synthetic_gen: If DEMO mode, pre-initialized generator.

        Returns:
            Dict with timestamp, region, data_mode, grid_results, summary.
        """
        log.info(f"Inference at T0={t0.isoformat()}", data_mode=self.config.data_mode)

        # Build observation window
        if self.config.data_mode == "DEMO" and synthetic_gen is not None:
            features_df = self._build_features_demo(t0, synthetic_gen)
        else:
            log.warning("REAL mode inference: data loading not yet implemented.")
            features_df = self._empty_features_df()

        if features_df.empty:
            return {"error": "No features available", "t0": t0.isoformat()}

        X = features_df.reindex(columns=self.feature_cols, fill_value=np.nan)

        # Run all models
        horizon_results: dict[str, dict] = {}
        for key, model in self.models.items():
            try:
                raw_proba = model.predict_proba(X)

                # Apply calibration if available
                cal = self.calibrators.get(key)
                if cal and cal.fitted:
                    proba = cal.calibrate(raw_proba)
                    calibration_applied = True
                else:
                    proba = raw_proba
                    calibration_applied = False

                parts = key.split("_")  # e.g. ["thunderstorm", "15m"]
                target = parts[0]
                horizon = parts[1]

                if horizon not in horizon_results:
                    horizon_results[horizon] = {}
                horizon_results[horizon][f"{target}_probability"] = proba.tolist()
                horizon_results[horizon]["calibration_applied"] = calibration_applied

            except Exception as e:
                log.error(f"Inference failed for {key}: {e}")

        # Build grid response
        lat_grid, lon_grid = self.grid.lat_lon_meshgrid()
        grid_rows = []
        for i in range(self.grid.n_lat):
            for j in range(self.grid.n_lon):
                idx = i * self.grid.n_lon + j
                row = {
                    "latitude": float(lat_grid[i, j]),
                    "longitude": float(lon_grid[i, j]),
                    "grid_i": i,
                    "grid_j": j,
                }
                for horizon, hdata in horizon_results.items():
                    for prob_key, prob_arr in hdata.items():
                        if isinstance(prob_arr, list):
                            row[f"{horizon}_{prob_key}"] = round(float(prob_arr[idx]), 4)
                grid_rows.append(row)

        return {
            "timestamp": t0.isoformat(),
            "region": self.config.region.name,
            "data_mode": self.config.data_mode,
            "horizons": horizon_results,
            "grid": grid_rows,
            "summary": self._compute_summary(horizon_results, lat_grid, lon_grid),
        }

    def _build_features_demo(
        self,
        t0: datetime,
        gen: SyntheticDataGenerator,
    ) -> pd.DataFrame:
        """Extract features for DEMO mode inference at T0."""
        seq_start = t0 - timedelta(minutes=LOOKBACK_MIN)
        snapshots = gen.generate_sequence(seq_start, t0, interval_minutes=STEP_MIN)

        snap_index = {s["timestamp"]: s for s in snapshots}
        seq_times = build_input_sequence(t0, LOOKBACK_MIN, STEP_MIN)
        check_no_leakage(t0, seq_times)

        radar_snaps = {t: snap_index[t]["radar"] for t in snap_index if t <= t0}
        sat_snaps = {t: snap_index[t]["satellite"] for t in snap_index if t <= t0}

        all_lightning = pd.concat(
            [snap_index[t]["lightning_events"] for t in snap_index if t <= t0],
            ignore_index=True,
        )

        t0_snap = max((t for t in snap_index if t <= t0), default=None)
        nwp_surface = snap_index[t0_snap]["nwp_surface"] if t0_snap else {}

        radar_feats = extract_radar_features(radar_snaps, t0, self.grid.shape)
        sat_feats = extract_satellite_features(sat_snaps, t0, self.grid.shape)
        light_feats = grid_lightning_features(all_lightning, t0, self.grid)
        nwp_feats = extract_nwp_features(nwp_surface, self.grid.shape)

        rows = []
        for i in range(self.grid.n_lat):
            for j in range(self.grid.n_lon):
                row = {}
                for fd in [radar_feats, sat_feats, light_feats, nwp_feats]:
                    for k, arr in fd.items():
                        if isinstance(arr, np.ndarray) and arr.shape == self.grid.shape:
                            row[k] = float(arr[i, j])
                rows.append(row)

        return pd.DataFrame(rows)

    def _empty_features_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=self.feature_cols)

    def _compute_summary(
        self,
        horizon_results: dict,
        lat_grid: np.ndarray,
        lon_grid: np.ndarray,
    ) -> dict:
        summary = {}
        for horizon, hdata in horizon_results.items():
            h_summary = {}
            for key, arr in hdata.items():
                if isinstance(arr, list):
                    arr_np = np.array(arr)
                    h_summary[key] = {
                        "max": round(float(np.nanmax(arr_np)), 4),
                        "mean": round(float(np.nanmean(arr_np)), 4),
                        "pct_high_risk": round(float((arr_np > 0.6).mean()), 4),
                    }
            summary[horizon] = h_summary
        return summary
