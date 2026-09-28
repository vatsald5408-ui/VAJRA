"""
future_models.py – Stub interfaces for future deep-learning models.

These stubs implement BaseNowcastModel so the pipeline remains
compatible when replacing Random Forest with CNN/ConvLSTM/Transformer.

None of these models are implemented yet — they raise NotImplementedError
to signal they need real implementation before use.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.models.base import BaseNowcastModel


class XGBoostNowcaster(BaseNowcastModel):
    """Future: XGBoost gradient boosting model."""

    def __init__(self, horizon_minutes: int, target: str):
        self._horizon = horizon_minutes
        self._target = target

    @property
    def name(self) -> str:
        return f"XGBoost_{self._target}_{self._horizon}m"

    @property
    def horizon_minutes(self) -> int:
        return self._horizon

    @property
    def target(self) -> str:
        return self._target

    def fit(self, X_train, y_train, X_val=None, y_val=None):
        raise NotImplementedError("XGBoostNowcaster: not yet implemented.")

    def predict_proba(self, X):
        raise NotImplementedError("XGBoostNowcaster: not yet implemented.")

    def save(self, path): raise NotImplementedError()

    @classmethod
    def load(cls, path): raise NotImplementedError()


class ConvLSTMNowcaster(BaseNowcastModel):
    """Future: ConvLSTM spatiotemporal model."""

    def __init__(self, horizon_minutes: int, target: str):
        self._horizon = horizon_minutes
        self._target = target

    @property
    def name(self) -> str:
        return f"ConvLSTM_{self._target}_{self._horizon}m"

    @property
    def horizon_minutes(self) -> int:
        return self._horizon

    @property
    def target(self) -> str:
        return self._target

    def fit(self, X_train, y_train, X_val=None, y_val=None):
        raise NotImplementedError(
            "ConvLSTMNowcaster: Requires PyTorch/TensorFlow implementation. "
            "Will use full spatial grid arrays, not tabular features."
        )

    def predict_proba(self, X):
        raise NotImplementedError()

    def save(self, path): raise NotImplementedError()

    @classmethod
    def load(cls, path): raise NotImplementedError()
