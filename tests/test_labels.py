"""
test_labels.py – Unit tests for target label construction.
"""
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
import pandas as pd
from src.dataset.labels import thunderstorm_labels, lightning_labels
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


class TestTargetLabels:
    def test_thunderstorm_labels_threshold(self):
        refl = np.zeros(GRID_SHAPE)
        refl[2, 3] = 45.0  # Above 40 dBZ threshold
        future_snaps = {T0 + timedelta(minutes=15): refl}
        labels = thunderstorm_labels(
            future_radar_snapshots=future_snaps,
            t0=T0,
            horizons_minutes=[15],
            grid_shape=GRID_SHAPE,
            reflectivity_threshold_dbz=40.0,
        )
        assert "target_thunderstorm_15m" in labels
        assert labels["target_thunderstorm_15m"][2, 3] == 1.0
        assert labels["target_thunderstorm_15m"][0, 0] == 0.0

    def test_lightning_labels_presence(self):
        events = pd.DataFrame([
            {"timestamp": T0 + timedelta(minutes=15), "latitude": 28.5, "longitude": 77.0},
        ])
        labels = lightning_labels(
            future_lightning_events=events,
            t0=T0,
            grid=GRID,
            horizons_minutes=[15],
            spatial_tolerance_km=10.0,
        )
        assert "target_lightning_15m" in labels
        assert labels["target_lightning_15m"].sum() > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
