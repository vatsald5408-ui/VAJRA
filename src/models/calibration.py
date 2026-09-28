"""
calibration.py (models) – Probability calibration.

⚠ RandomForest.predict_proba() is NOT automatically calibrated.
   Use Platt scaling or Isotonic regression to post-calibrate.

⚠ Calibration must be fitted on the VALIDATION set only,
   never on the training set (that would overfit).
"""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

from src.logger import get_logger

log = get_logger("models.calibration")


class ProbabilityCalibrator:
    """
    Post-hoc probability calibration for any BaseNowcastModel.

    Methods:
      - platt: Platt scaling (logistic regression on val probabilities)
      - isotonic: Isotonic regression (non-parametric)
    """

    def __init__(self, method: str = "isotonic"):
        assert method in ("platt", "isotonic"), f"Unknown method: {method}"
        self.method = method
        self._calibrator: IsotonicRegression | LogisticRegression | None = None
        self.fitted = False

    def fit(
        self,
        raw_probas: np.ndarray,
        y_true: np.ndarray,
    ) -> "ProbabilityCalibrator":
        """
        Fit calibrator on validation-set raw probabilities and true labels.

        ⚠ Use validation set only, NOT training set.

        Args:
            raw_probas: Shape (n_samples,), uncalibrated probabilities.
            y_true: Shape (n_samples,), binary labels (0/1).
        """
        mask = ~np.isnan(raw_probas) & ~np.isnan(y_true)
        p = raw_probas[mask]
        y = y_true[mask]

        if len(y) < 10 or len(np.unique(y)) < 2:
            log.warning("Too few samples or single class present to calibrate. Calibration skipped.")
            return self

        if self.method == "isotonic":
            self._calibrator = IsotonicRegression(out_of_bounds="clip")
            self._calibrator.fit(p, y)
        else:  # platt
            self._calibrator = LogisticRegression()
            self._calibrator.fit(p.reshape(-1, 1), y)

        self.fitted = True
        log.info(f"Calibration fitted ({self.method}), n={len(y)}")
        return self

    def calibrate(self, raw_probas: np.ndarray) -> np.ndarray:
        """Transform raw probabilities to calibrated probabilities."""
        if not self.fitted or self._calibrator is None:
            log.warning("Calibrator not fitted. Returning raw probabilities.")
            return raw_probas

        if self.method == "isotonic":
            cal = self._calibrator.predict(raw_probas)
        else:
            cal = self._calibrator.predict_proba(raw_probas.reshape(-1, 1))[:, 1]

        return np.clip(cal, 0.0, 1.0).astype(np.float32)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            pickle.dump({"method": self.method, "calibrator": self._calibrator, "fitted": self.fitted}, f)

    @classmethod
    def load(cls, path: Path) -> "ProbabilityCalibrator":
        with path.open("rb") as f:
            data = pickle.load(f)
        obj = cls(method=data["method"])
        obj._calibrator = data["calibrator"]
        obj.fitted = data["fitted"]
        return obj
