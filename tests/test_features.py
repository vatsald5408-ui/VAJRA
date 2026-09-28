"""
test_features.py – Unit tests for feature extraction modules.
"""
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
import pandas as pd
from src.features.radar_features import extract_radar_features
from src.features.satellite_features import extract_satellite_features
from src.features.nwp_features import extract_nwp_features
from src.ingestion.lightning import grid_lightning_features
from src.preprocessing.grid import CommonGrid


T0 = datetime(2022, 7, 1, 15, 0, 0, tzinfo=timezone.utc)
GRID_SHAPE = (10, 10)
GRID = CommonGrid(
    region_name="TEST",
    lats=np.linspace(29.0, 28.0, 10),
    lons=np.linspace(76.5, 77.5, 10),
    resolution_km=5.0,
    crs="EPSG:4326",
)


class TestRadarFeatures:
    def test_extract_radar_features_shape(self):
        radar_snaps = {
            T0: np.full(GRID_SHAPE, 25.0),
            T0 - pd.Timedelta(minutes=15): np.full(GRID_SHAPE, 20.0),
            T0 - pd.Timedelta(minutes=30): np.full(GRID_SHAPE, 15.0),
        }
        feats = extract_radar_features(radar_snaps, T0, GRID_SHAPE)
        assert isinstance(feats, dict)
        for k, v in feats.items():
            assert v.shape == GRID_SHAPE, f"Shape mismatch for {k}"

    def test_reflectivity_change_calculation(self):
        radar_snaps = {
            T0: np.full(GRID_SHAPE, 30.0),
            T0 - pd.Timedelta(minutes=15): np.full(GRID_SHAPE, 20.0),
            T0 - pd.Timedelta(minutes=30): np.full(GRID_SHAPE, 10.0),
        }
        feats = extract_radar_features(radar_snaps, T0, GRID_SHAPE)
        assert np.allclose(feats["refl_max"], 30.0)
        assert np.allclose(feats["refl_change_30min"], 20.0)


class TestSatelliteFeatures:
    def test_extract_satellite_features(self):
        sat_snaps = {
            T0: {"ir_brightness_temp": np.full(GRID_SHAPE, 240.0), "water_vapour": np.full(GRID_SHAPE, 230.0)},
            T0 - pd.Timedelta(minutes=30): {"ir_brightness_temp": np.full(GRID_SHAPE, 250.0), "water_vapour": np.full(GRID_SHAPE, 235.0)},
        }
        feats = extract_satellite_features(sat_snaps, T0, GRID_SHAPE)
        assert "ir_bt_mean" in feats
        assert np.allclose(feats["cloud_top_cooling_rate_30min"], 10.0)


class TestLightningFeatures:
    def test_grid_lightning_features(self):
        events = pd.DataFrame([
            {"timestamp": T0 - pd.Timedelta(minutes=2), "latitude": 28.5, "longitude": 77.0},
            {"timestamp": T0 - pd.Timedelta(minutes=4), "latitude": 28.5, "longitude": 77.0},
        ])
        feats = grid_lightning_features(events, T0, GRID)
        assert "strike_count_5min" in feats
        assert feats["strike_count_5min"].shape == GRID_SHAPE
        assert feats["strike_count_5min"].sum() == 2


class TestNwpFeatures:
    def test_extract_nwp_features(self):
        nwp_data = {
            "t2m": np.full(GRID_SHAPE, 300.0),
            "td2m": np.full(GRID_SHAPE, 290.0),
            "u10": np.full(GRID_SHAPE, 5.0),
            "v10": np.full(GRID_SHAPE, 5.0),
            "sp": np.full(GRID_SHAPE, 101325.0),
        }
        feats = extract_nwp_features(nwp_data, GRID_SHAPE)
        assert "wind_speed_10m_ms" in feats
        assert np.allclose(feats["wind_speed_10m_ms"], np.sqrt(50.0))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
