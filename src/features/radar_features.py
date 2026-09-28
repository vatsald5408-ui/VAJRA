"""
radar_features.py – Radar feature extraction.

Computes per-grid-cell radar features from a time sequence
of reflectivity and other radar products.

⚠ All features use ONLY data at or before T0.
"""
from __future__ import annotations

from datetime import datetime

import numpy as np

REFLECTIVITY_THRESHOLDS_DBZ = [20, 35, 40, 45, 50]


def extract_radar_features(
    snapshots: dict[datetime, dict],
    t0: datetime,
    grid_shape: tuple[int, int],
) -> dict[str, np.ndarray]:
    """
    Extract radar features from a time-ordered dict of radar snapshots.

    Args:
        snapshots: Dict mapping timestamp → {"reflectivity": arr, ...}
                   All timestamps must be ≤ T0.
        t0: Analysis time.
        grid_shape: (n_lat, n_lon).

    Returns:
        Dict of feature name → 2D array (grid_shape).
    """
    # ⚠ LEAKAGE GUARD
    valid_snaps = {t: v for t, v in snapshots.items() if t <= t0}
    if not valid_snaps:
        return _zeros(grid_shape)

    times = sorted(valid_snaps.keys())
    refl_stack = [
        valid_snaps[t].get("reflectivity", np.zeros(grid_shape))
        if isinstance(valid_snaps[t], dict) else valid_snaps[t]
        for t in times
    ]
    refl_arr = np.stack(refl_stack, axis=0)  # (T, n_lat, n_lon)

    # Current (T0) snapshot
    t0_snap = valid_snaps[times[-1]]
    if isinstance(t0_snap, dict):
        refl_t0 = t0_snap.get("reflectivity", np.zeros(grid_shape))
        sw_t0 = t0_snap.get("spectrum_width", np.zeros(grid_shape))
        zdr_t0 = t0_snap.get("ZDR", None)
        kdp_t0 = t0_snap.get("KDP", None)
        rhohv_t0 = t0_snap.get("rhoHV", None)
    else:
        refl_t0 = t0_snap
        sw_t0 = np.zeros(grid_shape)
        zdr_t0 = None
        kdp_t0 = None
        rhohv_t0 = None

    features: dict[str, np.ndarray] = {}

    # ---- Current-time statistics ----
    features["refl_max"] = refl_t0.astype(np.float32)
    features["refl_mean"] = refl_t0.astype(np.float32)   # single-scan max ≈ itself
    features["refl_median"] = refl_t0.astype(np.float32)

    # Area fraction above each threshold (per cell: 1 if above, 0 if not)
    for thr in REFLECTIVITY_THRESHOLDS_DBZ:
        features[f"refl_above_{thr}dbz"] = (refl_t0 >= thr).astype(np.float32)

    # Storm area (fraction of grid above 35 dBZ — rolling over full stack)
    storm_mask_t0 = (refl_t0 >= 35).astype(np.float32)
    features["storm_cell_area_fraction"] = storm_mask_t0

    # Storm centroid (broadcast centroid to all cells as distance)
    if storm_mask_t0.sum() > 0:
        lat_grid = np.arange(grid_shape[0], dtype=np.float32).reshape(-1, 1)
        lon_grid = np.arange(grid_shape[1], dtype=np.float32).reshape(1, -1)
        weight = storm_mask_t0 / storm_mask_t0.sum()
        centroid_i = float(np.sum(lat_grid * weight))
        centroid_j = float(np.sum(lon_grid * weight))
        features["storm_centroid_i"] = np.full(grid_shape, centroid_i, np.float32)
        features["storm_centroid_j"] = np.full(grid_shape, centroid_j, np.float32)
    else:
        features["storm_centroid_i"] = np.zeros(grid_shape, np.float32)
        features["storm_centroid_j"] = np.zeros(grid_shape, np.float32)

    features["spectrum_width_mean"] = sw_t0.astype(np.float32)

    if zdr_t0 is not None:
        features["ZDR_mean"] = zdr_t0.astype(np.float32)
    if kdp_t0 is not None:
        features["KDP_mean"] = kdp_t0.astype(np.float32)
    if rhohv_t0 is not None:
        features["rhoHV_mean"] = rhohv_t0.astype(np.float32)

    # ---- Temporal change features ----
    # Find snapshots closest to -10 and -30 min
    t0_sec = t0.timestamp()
    time_secs = np.array([t.timestamp() for t in times])

    def _refl_at_offset(offset_min: int) -> np.ndarray:
        target_sec = t0_sec - offset_min * 60
        diffs = np.abs(time_secs - target_sec)
        idx = int(np.argmin(diffs))
        if diffs[idx] > 20 * 60:  # more than 20 min away — treat as missing
            return np.zeros(grid_shape, np.float32)
        return refl_arr[idx]

    refl_10ago = _refl_at_offset(10)
    refl_30ago = _refl_at_offset(30)

    features["refl_change_10min"] = (refl_t0 - refl_10ago).astype(np.float32)
    features["refl_change_30min"] = (refl_t0 - refl_30ago).astype(np.float32)

    # Storm area change
    storm_30ago = (refl_30ago >= 35).astype(np.float32)
    features["storm_area_change_30min"] = (storm_mask_t0 - storm_30ago).astype(np.float32)

    # Centroid displacement over 30 min (scalar field)
    if storm_30ago.sum() > 0:
        w30 = storm_30ago / storm_30ago.sum()
        ci_30 = float(np.sum(np.arange(grid_shape[0], dtype=float).reshape(-1, 1) * w30))
        cj_30 = float(np.sum(np.arange(grid_shape[1], dtype=float).reshape(1, -1) * w30))
        centroid_displacement = float(np.sqrt(
            (features["storm_centroid_i"][0, 0] - ci_30) ** 2 +
            (features["storm_centroid_j"][0, 0] - cj_30) ** 2
        ))
    else:
        centroid_displacement = 0.0
    features["centroid_displacement_cells_30min"] = np.full(grid_shape, centroid_displacement, np.float32)

    # Rolling statistics over full input stack
    features["refl_rolling_max"] = refl_arr.max(axis=0).astype(np.float32)
    features["refl_rolling_mean"] = refl_arr.mean(axis=0).astype(np.float32)
    features["refl_rolling_std"] = refl_arr.std(axis=0).astype(np.float32)

    return features


def _zeros(grid_shape: tuple[int, int]) -> dict[str, np.ndarray]:
    """Return zero-filled feature dict when no data is available."""
    keys = [
        "refl_max", "refl_mean", "refl_median", "spectrum_width_mean",
        "storm_cell_area_fraction", "storm_centroid_i", "storm_centroid_j",
        "refl_change_10min", "refl_change_30min", "storm_area_change_30min",
        "centroid_displacement_cells_30min",
        "refl_rolling_max", "refl_rolling_mean", "refl_rolling_std",
    ] + [f"refl_above_{t}dbz" for t in REFLECTIVITY_THRESHOLDS_DBZ]
    return {k: np.zeros(grid_shape, np.float32) for k in keys}
