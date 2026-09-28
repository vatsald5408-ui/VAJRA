"""
test_temporal_alignment.py – Tests for temporal alignment and leakage prevention.

Critical test:
  If T0 = 15:00, no feature may use data after 15:00.
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.preprocessing.temporal import (
    build_input_sequence,
    build_target_times,
    check_no_leakage,
    find_nearest_observation,
    TemporalAligner,
)


T0 = datetime(2022, 7, 1, 15, 0, 0, tzinfo=timezone.utc)


class TestInputSequence:
    def test_all_times_at_or_before_t0(self):
        seq = build_input_sequence(T0, lookback_minutes=60, step_minutes=15)
        for t in seq:
            assert t <= T0, f"Leakage: {t} > T0 {T0}"

    def test_last_element_is_t0(self):
        seq = build_input_sequence(T0, 60, 15)
        assert seq[-1] == T0

    def test_sequence_length(self):
        seq = build_input_sequence(T0, 60, 15)
        # T-60, T-45, T-30, T-15, T0 = 5 steps
        assert len(seq) == 5

    def test_configurable_step(self):
        seq = build_input_sequence(T0, 30, 10)
        # T-30, T-20, T-10, T0 = 4 steps
        assert len(seq) == 4


class TestLeakagePrevention:
    def test_no_leakage_passes(self):
        seq = build_input_sequence(T0, 60, 15)
        assert check_no_leakage(T0, seq) is True

    def test_leakage_raises(self):
        future_t = T0 + timedelta(minutes=15)
        with pytest.raises(ValueError, match="DATA LEAKAGE DETECTED"):
            check_no_leakage(T0, [future_t])

    def test_exact_t0_passes(self):
        assert check_no_leakage(T0, [T0]) is True


class TestTargetTimes:
    def test_all_targets_after_t0(self):
        horizons = [15, 30, 60, 120, 180, 360]
        targets = build_target_times(T0, horizons)
        for h, target_t in targets.items():
            assert target_t > T0, f"Target for {h}m is not in the future"

    def test_correct_offsets(self):
        targets = build_target_times(T0, [15, 60])
        assert targets[15] == T0 + timedelta(minutes=15)
        assert targets[60] == T0 + timedelta(hours=1)


class TestNearestObservation:
    def test_past_obs_selected(self):
        available = [T0 - timedelta(minutes=5), T0 + timedelta(minutes=5)]
        result = find_nearest_observation(T0, available, tolerance_minutes=10, allow_future=False)
        assert result == T0 - timedelta(minutes=5)

    def test_future_excluded_when_no_future(self):
        available = [T0 + timedelta(minutes=5)]
        result = find_nearest_observation(T0, available, tolerance_minutes=10, allow_future=False)
        assert result is None

    def test_exact_match(self):
        available = [T0]
        result = find_nearest_observation(T0, available, tolerance_minutes=0, allow_future=False)
        assert result == T0

    def test_outside_tolerance_returns_none(self):
        available = [T0 - timedelta(minutes=30)]
        result = find_nearest_observation(T0, available, tolerance_minutes=10, allow_future=False)
        assert result is None


class TestTemporalAligner:
    def test_no_future_in_alignment(self):
        aligner = TemporalAligner(T0, lookback_minutes=60, step_minutes=15)
        available = [T0 - timedelta(minutes=i*15) for i in range(5)]
        alignment = aligner.align_source("radar", available)
        for seq_t, matched_t in alignment.items():
            assert seq_t <= T0
            if matched_t is not None:
                assert matched_t <= T0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
