"""
test_no_leakage.py – Rigorous temporal data leakage tests.

Critical requirement:
  For any forecast at T0, NO input feature may access observation data timestamped > T0.
"""
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
import pandas as pd
from src.preprocessing.temporal import check_no_leakage, build_input_sequence
from src.preprocessing.grid import CommonGrid


T0 = datetime(2022, 7, 1, 15, 0, 0, tzinfo=timezone.utc)
GRID_SHAPE = (5, 5)
GRID = CommonGrid(
    region_name="TEST",
    lats=np.linspace(29.0, 28.0, 5),
    lons=np.linspace(76.5, 77.5, 5),
    resolution_km=10.0,
    crs="EPSG:4326",
)


class TestLeakageAssertion:
    def test_future_timestamp_detected_and_rejected(self):
        seq_times = build_input_sequence(T0, lookback_minutes=60, step_minutes=15)
        # Verify valid sequence passes
        assert check_no_leakage(T0, seq_times) is True

        # Append future time T+15m
        future_seq = seq_times + [T0 + timedelta(minutes=15)]
        with pytest.raises(ValueError, match="DATA LEAKAGE DETECTED"):
            check_no_leakage(T0, future_seq)

    def test_strict_t0_boundary(self):
        exact_t0_seq = [T0 - timedelta(minutes=60), T0 - timedelta(minutes=30), T0]
        assert check_no_leakage(T0, exact_t0_seq) is True

        # 1 second past T0 is illegal
        illegal_seq = [T0 + timedelta(seconds=1)]
        with pytest.raises(ValueError, match="DATA LEAKAGE DETECTED"):
            check_no_leakage(T0, illegal_seq)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
