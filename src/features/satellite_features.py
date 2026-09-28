"""
satellite_features.py – Satellite feature extraction.

Computes IR brightness temperature statistics and temporal
change features from satellite imagery sequences.
"""
from __future__ import annotations

from datetime import datetime

import numpy as np


def extract_satellite_features(
    snapshots: dict[datetime, dict],
    t0: datetime,
    grid_shape: tuple[int, int],
) -> dict[str, np.ndarray]:
    """
    Extract satellite features from a time sequence of satellite snapshots.

    ⚠ Only uses data at or before T0 (leakage prevention).

    Args:
        snapshots: Dict mapping timestamp → {"ir_brightness_temp": arr, ...}
        t0: Analysis time.
        grid_shape: (n_lat, n_lon).

    Returns:
        Dict of feature name → 2D array.
    """
    valid = {t: v for t, v in snapshots.items() if t <= t0}
    if not valid:
        return _zeros(grid_shape)

    times = sorted(valid.keys())
    t0_snap = valid[times[-1]]

    ir_t0 = t0_snap.get("ir_brightness_temp", np.full(grid_shape, 300.0, np.float32))
    wv_t0 = t0_snap.get("wv_brightness_temp", np.full(grid_shape, 250.0, np.float32))
    vis_t0 = t0_snap.get("visible", None)

    features: dict[str, np.ndarray] = {}

    # Current-time stats
    features["ir_bt_mean"] = ir_t0.astype(np.float32)
    features["ir_bt_min"] = ir_t0.astype(np.float32)   # per-cell: itself
    features["wv_bt_mean"] = wv_t0.astype(np.float32)
    features["cloud_top_temp"] = ir_t0.astype(np.float32)

    if vis_t0 is not None:
        features["vis_mean"] = vis_t0.astype(np.float32)
    else:
        features["vis_mean"] = np.full(grid_shape, np.nan, np.float32)

    # Temporal change features
    time_secs = np.array([t.timestamp() for t in times])
    t0_sec = t0.timestamp()

    def _ir_at_offset(offset_min: int) -> np.ndarray:
        target = t0_sec - offset_min * 60
        diffs = np.abs(time_secs - target)
        idx = int(np.argmin(diffs))
        if diffs[idx] > 25 * 60:
            return ir_t0.copy()
        return valid[times[idx]].get("ir_brightness_temp", ir_t0.copy())

    ir_30ago = _ir_at_offset(30)
    ir_60ago = _ir_at_offset(60)

    # Cloud-top cooling rate (negative = warming = dissipation)
    # Positive cooling rate = BT decreasing = cloud tops getting colder = convective growth
    features["cloud_top_cooling_rate_30min"] = (ir_30ago - ir_t0).astype(np.float32)
    features["bt_change_30min"] = (ir_t0 - ir_30ago).astype(np.float32)
    features["bt_change_60min"] = (ir_t0 - ir_60ago).astype(np.float32)

    # Cloud area (fraction of cells colder than convection threshold)
    CONV_THRESHOLD_K = 235.0
    cloud_mask_t0 = (ir_t0 < CONV_THRESHOLD_K).astype(np.float32)
    cloud_mask_30 = (ir_30ago < CONV_THRESHOLD_K).astype(np.float32)
    features["cold_cloud_fraction"] = cloud_mask_t0
    features["cloud_area_growth_30min"] = (cloud_mask_t0 - cloud_mask_30).astype(np.float32)

    # Rolling stats across all time steps
    ir_stack = np.stack([
        valid[t].get("ir_brightness_temp", np.full(grid_shape, 300.0, np.float32))
        for t in times
    ], axis=0)
    features["ir_bt_rolling_min"] = ir_stack.min(axis=0).astype(np.float32)
    features["ir_bt_rolling_mean"] = ir_stack.mean(axis=0).astype(np.float32)
    features["ir_bt_rolling_std"] = ir_stack.std(axis=0).astype(np.float32)

    return features


def _zeros(grid_shape: tuple[int, int]) -> dict[str, np.ndarray]:
    keys = [
        "ir_bt_mean", "ir_bt_min", "wv_bt_mean", "cloud_top_temp", "vis_mean",
        "cloud_top_cooling_rate_30min", "bt_change_30min", "bt_change_60min",
        "cold_cloud_fraction", "cloud_area_growth_30min",
        "ir_bt_rolling_min", "ir_bt_rolling_mean", "ir_bt_rolling_std",
    ]
    return {k: np.zeros(grid_shape, np.float32) for k in keys}
