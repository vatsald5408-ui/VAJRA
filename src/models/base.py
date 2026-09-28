"""
base.py – Abstract base class for all ML models.

Provides a pluggable interface so Random Forest can be replaced
by XGBoost, LightGBM, CNN, ConvLSTM, or Transformer
without rewriting the pipeline.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


class BaseNowcastModel(ABC):
    """
    Abstract base for all nowcasting models.

    Every model must implement:
      - fit(X_train, y_train, X_val, y_val)
      - predict_proba(X) → probabilities in [0, 1]
      - save(path)
      - load(path)
      - feature_importance() → dict (if supported)
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable model name."""
        ...

    @property
    @abstractmethod
    def horizon_minutes(self) -> int:
        """Forecast horizon this model predicts."""
        ...

    @property
    @abstractmethod
    def target(self) -> str:
        """Target variable: 'thunderstorm' or 'lightning'."""
        ...

    @abstractmethod
    def fit(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame | None = None,
        y_val: pd.Series | None = None,
    ) -> "BaseNowcastModel":
        """Train the model."""
        ...

    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict probability of positive class.

        Returns:
            1D array of shape (n_samples,) with values in [0, 1].
        """
        ...

    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        """Binary prediction at a given probability threshold."""
        return (self.predict_proba(X) >= threshold).astype(int)

    @abstractmethod
    def save(self, path: Path) -> None:
        """Serialize model to disk."""
        ...

    @classmethod
    @abstractmethod
    def load(cls, path: Path) -> "BaseNowcastModel":
        """Load model from disk."""
        ...

    def feature_importance(self) -> dict[str, float] | None:
        """Return feature importance dict if supported, else None."""
        return None

    def config_dict(self) -> dict[str, Any]:
        """Return model configuration for experiment logging."""
        return {
            "model_name": self.name,
            "target": self.target,
            "horizon_minutes": self.horizon_minutes,
        }
