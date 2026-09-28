"""
builder.py – Training dataset construction.

Orchestrates the full pipeline:
  synthetic data → feature extraction → label creation → Parquet samples.

Each row is one (timestamp, grid_cell) sample with:
  - all input features
  - all target labels (12 total: 6 horizons × 2 targets)

⚠ DATA LEAKAGE PREVENTION:
  Input features use only T0 and prior data.
  Labels use only future data (T0 + horizon).
  The check_no_leakage() function is called for every sample.

⚠ DEMO MODE: All data is clearly labelled DEMO/SYNTHETIC.
"""
from __future__ import annotations

import gc
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.config import AppConfig
from src.ingestion.synthetic import SyntheticDataGenerator
from src.ingestion.lightning import grid_lightning_features
from src.preprocessing.grid import CommonGrid
from src.preprocessing.temporal import (
    build_timeline,
    build_input_sequence,
    build_target_times,
    check_no_leakage,
)
from src.features.radar_features import extract_radar_features
from src.features.satellite_features import extract_satellite_features
from src.features.nwp_features import extract_nwp_features
from src.dataset.labels import thunderstorm_labels, lightning_labels, HORIZONS_MINUTES
from src.logger import get_logger, Timer

log = get_logger("dataset.builder")

LOOKBACK_MIN = 60
STEP_MIN = 15
FUTURE_BUFFER_MIN = 400   # must cover max horizon (360) + tolerance (15)


def build_dataset(
    config: AppConfig,
    grid: CommonGrid,
    start: datetime,
    end: datetime,
    output_path: Path,
    t0_interval_min: int = 30,
    max_t0s: int | None = None,
) -> pd.DataFrame:
    """
    Build a training dataset from synthetic (DEMO) or real data.

    For each T0 in [start, end]:
      1. Generate/load observations for [T0-60min, T0+360min]
      2. Extract input features (only ≤ T0 data)
      3. Construct target labels (only > T0 data)
      4. Flatten grid: one row per (T0, grid_cell)
      5. Save to Parquet

    Args:
        config: AppConfig.
        grid: CommonGrid.
        start: Start of T0 range.
        end: End of T0 range.
        output_path: Where to save the Parquet dataset.
        t0_interval_min: Spacing between T0 timestamps.
        max_t0s: Limit number of T0s (for fast testing).

    Returns:
        DataFrame of all samples.
    """
    log.info(
        "Building dataset",
        mode=config.data_mode,
        region=grid.region_name,
        start=start.isoformat(),
        end=end.isoformat(),
    )

    t0_times = build_timeline(start, end, interval_minutes=t0_interval_min)
    if max_t0s:
        t0_times = t0_times[:max_t0s]

    log.info(f"T0 timestamps to process: {len(t0_times)}")

    # In DEMO mode, use synthetic generator
    gen = SyntheticDataGenerator(grid, seed=42, n_storm_cells=3)

    # Generate the full observation sequence covering all T0s
    # with buffer for lookback and future labels
    seq_start = start - timedelta(minutes=LOOKBACK_MIN)
    seq_end = end + timedelta(minutes=FUTURE_BUFFER_MIN)

    with Timer(log, "Generating synthetic sequence"):
        full_sequence = gen.generate_sequence(seq_start, seq_end, interval_minutes=STEP_MIN)

    # Index snapshots by timestamp for fast lookup
    snap_index: dict[datetime, dict] = {}
    lightning_index: dict[datetime, pd.DataFrame] = {}
    for snap in full_sequence:
        ts = snap["timestamp"]
        snap_index[ts] = snap
        lightning_index[ts] = snap["lightning_events"]

    all_rows: list[dict] = []

    with Timer(log, f"Extracting features for {len(t0_times)} T0s"):
        for t0 in t0_times:
            rows = _process_t0(t0, snap_index, lightning_index, grid, config)
            all_rows.extend(rows)

    if not all_rows:
        log.warning("No samples generated!")
        return pd.DataFrame()

    df = pd.DataFrame(all_rows)
    log.info(f"Dataset: {len(df)} rows, {len(df.columns)} columns")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    log.info(f"Dataset saved to {output_path}")

    # Save data quality report
    _save_quality_report(df, output_path.parent / "data_quality_report.json", config)

    return df


def _process_t0(
    t0: datetime,
    snap_index: dict[datetime, dict],
    lightning_index: dict[datetime, pd.DataFrame],
    grid: CommonGrid,
    config: AppConfig,
) -> list[dict]:
    """Process one T0 timestamp: extract features + labels, return rows."""

    input_seq = build_input_sequence(t0, LOOKBACK_MIN, STEP_MIN)

    # ---- INPUT FEATURES (only ≤ T0) ----
    radar_snaps: dict[datetime, dict] = {}
    sat_snaps: dict[datetime, dict] = {}
    all_lightning = pd.DataFrame()

    for seq_t in input_seq:
        # Find nearest available snapshot (tolerance 10 min)
        nearest = _find_nearest_snap(seq_t, snap_index, tol_min=10)
        if nearest is None:
            continue

        ts, snap = nearest

        # ⚠ LEAKAGE GUARD
        assert ts <= t0, f"Leakage: {ts} > {t0}"
        check_no_leakage(t0, [ts])

        radar_snaps[ts] = snap["radar"]
        sat_snaps[ts] = snap["satellite"]

        # Accumulate lightning events up to T0
        if ts in lightning_index and not lightning_index[ts].empty:
            all_lightning = pd.concat([all_lightning, lightning_index[ts]], ignore_index=True)

    # Extract per-modality features
    radar_feats = extract_radar_features(radar_snaps, t0, grid.shape)
    sat_feats = extract_satellite_features(sat_snaps, t0, grid.shape)

    # De-duplicate lightning and remove any events after T0
    if not all_lightning.empty:
        all_lightning["timestamp"] = pd.to_datetime(all_lightning["timestamp"], utc=True)
        t0_utc = pd.Timestamp(t0, tz="UTC") if t0.tzinfo is None else pd.Timestamp(t0)
        all_lightning = all_lightning[all_lightning["timestamp"] <= t0_utc]

    light_feats = grid_lightning_features(all_lightning, t0, grid)

    # NWP features from T0 snapshot
    t0_snap = _find_nearest_snap(t0, snap_index, tol_min=20)
    nwp_surface = t0_snap[1]["nwp_surface"] if t0_snap else {}
    nwp_feats = extract_nwp_features(nwp_surface, grid.shape)

    # ---- TARGET LABELS (only > T0) ----
    # Collect future radar and lightning
    future_radar: dict[datetime, np.ndarray] = {}
    future_lightning_dfs: list[pd.DataFrame] = []

    for ts, snap in snap_index.items():
        if ts > t0 and ts <= t0 + timedelta(minutes=HORIZONS_MINUTES[-1] + 20):
            future_radar[ts] = snap["radar"].get("reflectivity", np.zeros(grid.shape))
            if ts in lightning_index and not lightning_index[ts].empty:
                future_lightning_dfs.append(lightning_index[ts])

    future_lightning = pd.concat(future_lightning_dfs, ignore_index=True) if future_lightning_dfs else pd.DataFrame()

    t_storm_labels = thunderstorm_labels(
        future_radar, t0, HORIZONS_MINUTES, grid.shape,
        reflectivity_threshold_dbz=config.target_definition["targets"]["thunderstorm"]["reflectivity_threshold_dbz"],
    )
    t_light_labels = lightning_labels(
        future_lightning, t0, grid, HORIZONS_MINUTES,
        spatial_tolerance_km=config.target_definition["targets"]["lightning"]["spatial_tolerance_km"],
    )

    # ---- FLATTEN GRID → ROWS ----
    lat_grid, lon_grid = grid.lat_lon_meshgrid()
    rows: list[dict] = []

    for i in range(grid.n_lat):
        for j in range(grid.n_lon):
            row: dict = {
                "sample_id": f"{t0.strftime('%Y%m%d%H%M')}_{i:03d}_{j:03d}",
                "timestamp": t0.isoformat(),
                "grid_i": i,
                "grid_j": j,
                "latitude": float(lat_grid[i, j]),
                "longitude": float(lon_grid[i, j]),
                "data_mode": "DEMO/SYNTHETIC" if config.data_mode == "DEMO" else "REAL",
            }

            # Add all feature values at this cell
            for feat_dict in [radar_feats, sat_feats, light_feats, nwp_feats]:
                for k, arr in feat_dict.items():
                    if isinstance(arr, np.ndarray) and arr.shape == grid.shape:
                        row[k] = float(arr[i, j]) if not np.isnan(arr[i, j]) else None
                    # Skip string metadata fields like "data_mode" in nwp dict

            # Add all labels
            for k, arr in t_storm_labels.items():
                row[k] = float(arr[i, j]) if not np.isnan(arr[i, j]) else None
            for k, arr in t_light_labels.items():
                row[k] = float(arr[i, j]) if not np.isnan(arr[i, j]) else None

            rows.append(row)

    return rows


def _find_nearest_snap(
    t: datetime,
    snap_index: dict[datetime, dict],
    tol_min: int = 10,
) -> tuple[datetime, dict] | None:
    """Find the nearest snapshot to time t within tolerance."""
    if not snap_index:
        return None
    times = np.array([ts.timestamp() for ts in snap_index.keys()])
    target = t.timestamp()
    diffs = np.abs(times - target)
    idx = int(np.argmin(diffs))
    if diffs[idx] > tol_min * 60:
        return None
    ts_list = list(snap_index.keys())
    nearest_ts = ts_list[idx]
    return nearest_ts, snap_index[nearest_ts]


def _save_quality_report(df: pd.DataFrame, path: Path, config: AppConfig) -> None:
    """Save a data quality summary report."""
    label_cols = [c for c in df.columns if c.startswith("target_")]
    feat_cols = [c for c in df.columns if c not in label_cols and c not in [
        "sample_id", "timestamp", "grid_i", "grid_j", "latitude", "longitude", "data_mode"
    ]]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_mode": config.data_mode,
        "region": config.region.name,
        "total_samples": len(df),
        "feature_columns": len(feat_cols),
        "label_columns": len(label_cols),
        "missing_features_pct": {
            col: round(float(df[col].isna().mean() * 100), 2)
            for col in feat_cols[:20]  # summarize first 20
        },
        "label_positive_rates": {
            col: round(float(df[col].dropna().mean()), 4)
            for col in label_cols
        },
        "timestamp_range": {
            "min": str(df["timestamp"].min()),
            "max": str(df["timestamp"].max()),
        },
        "note": (
            "DEMO/SYNTHETIC DATA - values are not real observations. "
            "Positive rates are plausibility-checked, not validated."
            if config.data_mode == "DEMO"
            else "REAL DATA"
        ),
    }

    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    log.info(f"Data quality report saved: {path}")
