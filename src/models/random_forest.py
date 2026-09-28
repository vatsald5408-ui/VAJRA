"""
random_forest.py – Random Forest baseline nowcasting model.

Baseline probabilistic classifier.
One model per (horizon, target) combination.
Total: 6 horizons × 2 targets = 12 models.

⚠ predict_proba() output is NOT automatically calibrated.
   Use src/models/calibration.py for probability calibration.

⚠ Do not report accuracy as the only metric.
   Use Brier Score, ROC-AUC, PR-AUC (see src/evaluation/metrics.py).

Class imbalance strategy:
  - class_weight="balanced" to handle rare positive events.
  - Do not blindly oversample correlated weather samples.
"""
from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from src.models.base import BaseNowcastModel
from src.logger import get_logger

log = get_logger("models.random_forest")


class RandomForestNowcaster(BaseNowcastModel):
    """
    Random Forest classifier for thunderstorm/lightning nowcasting.

    Hyperparameters are configurable; defaults chosen for interpretability.
    """

    def __init__(
        self,
        horizon_minutes: int,
        target: str,
        n_estimators: int = 200,
        max_depth: int | None = 15,
        min_samples_leaf: int = 10,
        class_weight: str = "balanced",
        random_state: int = 42,
        n_jobs: int = -1,
    ):
        self._horizon_minutes = horizon_minutes
        self._target = target
        self.random_state = random_state
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.class_weight = class_weight
        self.n_jobs = n_jobs

        self._pipeline: Pipeline | None = None
        self._feature_names: list[str] = []

    @property
    def name(self) -> str:
        return f"RandomForest_{self._target}_{self._horizon_minutes}m"

    @property
    def horizon_minutes(self) -> int:
        return self._horizon_minutes

    @property
    def target(self) -> str:
        return self._target

    def _build_pipeline(self) -> Pipeline:
        return Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
                class_weight=self.class_weight,
                random_state=self.random_state,
                n_jobs=self.n_jobs,
                oob_score=True,
            )),
        ])

    def fit(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame | None = None,
        y_val: pd.Series | None = None,
    ) -> "RandomForestNowcaster":
        self._feature_names = list(X_train.columns)

        # Drop samples with missing labels
        mask = y_train.notna()
        X_tr = X_train[mask]
        y_tr = y_train[mask]

        if len(y_tr) == 0:
            raise ValueError(f"No valid training samples for {self.name}")

        pos_rate = float(y_tr.mean())
        log.info(
            f"Training {self.name}",
            n_samples=len(y_tr),
            positive_rate=round(pos_rate, 4),
            n_features=len(self._feature_names),
        )

        self._pipeline = self._build_pipeline()
        self._pipeline.fit(X_tr, y_tr)

        # OOB score
        oob = self._pipeline.named_steps["clf"].oob_score_
        log.info(f"  OOB score: {oob:.4f}")

        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if self._pipeline is None:
            raise RuntimeError(f"Model {self.name} has not been fitted.")
        # Align feature order
        X = X.reindex(columns=self._feature_names, fill_value=np.nan)
        proba = self._pipeline.predict_proba(X)
        
        clf = self._pipeline.named_steps["clf"]
        classes = list(clf.classes_)
        if 1 in classes:
            idx = classes.index(1)
            return proba[:, idx].astype(np.float32)
        elif 1.0 in classes:
            idx = classes.index(1.0)
            return proba[:, idx].astype(np.float32)
        else:
            return np.zeros(len(X), dtype=np.float32)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            pickle.dump({
                "pipeline": self._pipeline,
                "feature_names": self._feature_names,
                "config": self.config_dict(),
            }, f)
        log.info(f"Model saved: {path}")

    @classmethod
    def load(cls, path: Path) -> "RandomForestNowcaster":
        with path.open("rb") as f:
            data = pickle.load(f)
        cfg = data["config"]
        obj = cls(
            horizon_minutes=cfg["horizon_minutes"],
            target=cfg["target"],
        )
        obj._pipeline = data["pipeline"]
        obj._feature_names = data["feature_names"]
        log.info(f"Model loaded: {path}")
        return obj

    def feature_importance(self) -> dict[str, float] | None:
        if self._pipeline is None:
            return None
        rf = self._pipeline.named_steps["clf"]
        importances = rf.feature_importances_
        return dict(sorted(
            zip(self._feature_names, importances.tolist()),
            key=lambda x: x[1],
            reverse=True,
        ))

    def config_dict(self) -> dict[str, Any]:
        base = super().config_dict()
        base.update({
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "min_samples_leaf": self.min_samples_leaf,
            "class_weight": self.class_weight,
            "random_state": self.random_state,
        })
        return base


def train_all_models(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    feature_cols: list[str],
    horizons: list[int],
    targets: list[str],
    model_dir: Path,
) -> dict[str, RandomForestNowcaster]:
    """
    Train one RandomForest per (target, horizon) combination.

    Returns:
        Dict mapping "thunderstorm_15m" → trained model, etc.
    """
    models: dict[str, RandomForestNowcaster] = {}

    for tgt in targets:
        for h in horizons:
            label_col = f"target_{tgt}_{h}m"
            if label_col not in train_df.columns:
                log.warning(f"Label column {label_col} not found. Skipping.")
                continue

            y_train = train_df[label_col]
            y_val = val_df[label_col] if val_df is not None else None
            X_train = train_df[feature_cols]
            X_val = val_df[feature_cols] if val_df is not None else None

            model = RandomForestNowcaster(horizon_minutes=h, target=tgt)
            model.fit(X_train, y_train, X_val, y_val)

            key = f"{tgt}_{h}m"
            models[key] = model

            save_path = model_dir / f"rf_{tgt}_{h}m.pkl"
            model.save(save_path)

    log.info(f"Trained {len(models)} models")
    return models
