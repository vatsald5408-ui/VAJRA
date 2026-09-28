"""
labels.py – Target label construction.

Creates binary labels for:
  - thunderstorm occurrence (radar-derived proxy)
  - lightning occurrence (lightning network data)

for each forecast horizon and each grid cell.

⚠ SCIENTIFIC HONESTY:
  All thresholds are documented in configs/target_definition.yaml.
  These are prototype assumptions and should be validated
  against official IMD event reports.

⚠ LEAKAGE PREVENTION:
  Labels use FUTURE data (T0 + horizon). Input features use
  PAST data (≤ T0). These must never be mixed.
"""
from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from src.preprocessing.grid import CommonGrid, latlon_to_grid_indices
from src.logger import get_logger

log = get_logger("dataset.labels")

HORIZONS_MINUTES = [15, 30, 60, 120, 180, 360]
DEFAULT_REFL_THRESHOLD_DBZ = 40.0
DEFAULT_SPATIAL_TOL_KM = 10.0
DEFAULT_TEMPORAL_TOL_MIN = 15


def thunderstorm_labels(
    future_radar_snapshots: dict[datetime, np.ndarray],
    t0: datetime,
    horizons_minutes: list[int],
    grid_shape: tuple[int, int],
    reflectivity_threshold_dbz: float = DEFAULT_REFL_THRESHOLD_DBZ,
    temporal_tolerance_min: int = DEFAULT_TEMPORAL_TOL_MIN,
) -> dict[str, np.ndarray]:
    """
    Create binary thunderstorm labels for each horizon.

    Definition:
      Label = 1 if max composite reflectivity in target window
              ≥ reflectivity_threshold_dbz.
      Label = 0 otherwise.

    ⚠ Uses FUTURE radar data (T+horizon). Never used as input features.

    Args:
        future_radar_snapshots: Dict mapping future timestamp → reflectivity array.
        t0: Analysis time.
        horizons_minutes: Forecast horizons.
        grid_shape: (n_lat, n_lon).
        reflectivity_threshold_dbz: Documented threshold (see target_definition.yaml).
        temporal_tolerance_min: ±minutes around target time to search for event.

    Returns:
        Dict: "target_thunderstorm_{H}m" → binary array (0/1), shape grid_shape.
    """
    labels: dict[str, np.ndarray] = {}

    for h in horizons_minutes:
        target_time = t0 + timedelta(minutes=h)
        t_start = target_time - timedelta(minutes=temporal_tolerance_min)
        t_end = target_time + timedelta(minutes=temporal_tolerance_min)

        max_refl = np.zeros(grid_shape, np.float32)
        found_any = False

        for ts, refl in future_radar_snapshots.items():
            if t_start <= ts <= t_end:
                max_refl = np.maximum(max_refl, refl)
                found_any = True

        if not found_any:
            # No future data available → label as NaN (missing, not 0)
            label = np.full(grid_shape, np.nan, np.float32)
        else:
            label = (max_refl >= reflectivity_threshold_dbz).astype(np.float32)

        labels[f"target_thunderstorm_{h}m"] = label

    return labels


def lightning_labels(
    future_lightning_events: pd.DataFrame,
    t0: datetime,
    grid: CommonGrid,
    horizons_minutes: list[int],
    spatial_tolerance_km: float = DEFAULT_SPATIAL_TOL_KM,
    temporal_tolerance_min: int = DEFAULT_TEMPORAL_TOL_MIN,
) -> dict[str, np.ndarray]:
    """
    Create binary lightning labels for each horizon.

    Definition:
      Label = 1 if ≥1 lightning event occurs within spatial_tolerance_km
              of the grid cell center during [T+horizon ± temporal_tolerance_min].
      Label = 0 otherwise.

    ⚠ Uses FUTURE lightning data. Never used as input features.

    Args:
        future_lightning_events: DataFrame with [timestamp, latitude, longitude].
        t0: Analysis time.
        grid: CommonGrid.
        horizons_minutes: Forecast horizons.
        spatial_tolerance_km: Search radius around grid cell.
        temporal_tolerance_min: Time window around target horizon.

    Returns:
        Dict: "target_lightning_{H}m" → binary array, shape grid.shape.
    """
    labels: dict[str, np.ndarray] = {}

    if future_lightning_events.empty:
        for h in horizons_minutes:
            labels[f"target_lightning_{h}m"] = np.zeros(grid.shape, np.float32)
        return labels

    df = future_lightning_events.copy()
    if hasattr(df["timestamp"].dtype, "tz") and df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")

    t0_utc = pd.Timestamp(t0, tz="UTC") if t0.tzinfo is None else pd.Timestamp(t0)

    # Pre-compute grid cell centres
    lat_grid, lon_grid = grid.lat_lon_meshgrid()

    for h in horizons_minutes:
        target_time = t0_utc + pd.Timedelta(minutes=h)
        t_start = target_time - pd.Timedelta(minutes=temporal_tolerance_min)
        t_end = target_time + pd.Timedelta(minutes=temporal_tolerance_min)

        window_events = df[(df["timestamp"] >= t_start) & (df["timestamp"] <= t_end)]

        label = np.zeros(grid.shape, np.float32)

        if not window_events.empty:
            for _, evt in window_events.iterrows():
                evt_lat = float(evt["latitude"])
                evt_lon = float(evt["longitude"])

                # Distance from event to every grid cell centre
                dlat_km = (lat_grid - evt_lat) * 111.32
                cos_lat = np.cos(np.radians(evt_lat))
                dlon_km = (lon_grid - evt_lon) * 111.32 * cos_lat
                dist_km = np.sqrt(dlat_km ** 2 + dlon_km ** 2)

                label[dist_km <= spatial_tolerance_km] = 1.0

        labels[f"target_lightning_{h}m"] = label

    return labels
