"""
nwp_features.py – NWP/atmospheric feature extraction.

Computes derived atmospheric features from NWP surface fields.
CAPE and CIN are used only if present in the NWP source.
"""
from __future__ import annotations

import numpy as np


def extract_nwp_features(
    nwp_surface: dict[str, np.ndarray],
    grid_shape: tuple[int, int],
) -> dict[str, np.ndarray]:
    """
    Extract NWP features from a surface fields dictionary.

    Args:
        nwp_surface: Dict from SyntheticDataGenerator.nwp_surface()
                     or real NWP adapter.
        grid_shape: (n_lat, n_lon).

    Returns:
        Dict of feature name → 2D array.
    """
    features: dict[str, np.ndarray] = {}

    def _get(key: str, default_val: float = 0.0) -> np.ndarray:
        arr = nwp_surface.get(key, np.full(grid_shape, default_val, np.float32))
        if isinstance(arr, np.ndarray):
            return arr.astype(np.float32)
        return np.full(grid_shape, float(arr), np.float32)

    features["t2m_K"] = _get("t2m", 300.0)
    features["td2m_K"] = _get("td2m", 295.0)
    features["sp_Pa"] = _get("sp", 101300.0)
    features["u10_ms"] = _get("u10", 0.0)
    features["v10_ms"] = _get("v10", 0.0)
    features["tcc"] = _get("tcc", 0.0)
    features["blh_m"] = _get("blh", 500.0)
    features["tp_m"] = _get("tp", 0.0)

    # Derived: wind speed and direction
    u = features["u10_ms"]
    v = features["v10_ms"]
    features["wind_speed_10m_ms"] = np.sqrt(u ** 2 + v ** 2).astype(np.float32)
    features["wind_dir_10m_deg"] = (np.degrees(np.arctan2(u, v)) % 360).astype(np.float32)

    # Derived: relative humidity from T and Td (Magnus approximation)
    # RH = 100 * exp(17.67 * Td / (Td + 243.5)) / exp(17.67 * T / (T + 243.5))
    # Where T and Td are in Celsius
    t_c = features["t2m_K"] - 273.15
    td_c = features["td2m_K"] - 273.15
    e_s = np.exp(17.67 * t_c / (t_c + 243.5))
    e_d = np.exp(17.67 * td_c / (td_c + 243.5))
    rh = np.clip(100.0 * e_d / (e_s + 1e-9), 0.0, 100.0)
    features["relative_humidity_pct"] = rh.astype(np.float32)

    # CAPE and CIN — only include if actually available in source
    if "cape" in nwp_surface:
        features["CAPE_Jkg"] = _get("cape", 0.0)
    if "cin" in nwp_surface:
        features["CIN_Jkg"] = _get("cin", 0.0)

    # Vertical wind shear (850–500 hPa): only if pressure-level data available
    # Placeholder: if pressure-level u/v available, compute shear
    # Not computed here without verified pressure-level data

    return features
