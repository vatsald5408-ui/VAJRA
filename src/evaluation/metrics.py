"""
metrics.py – Comprehensive evaluation metrics.

Evaluates each model at every forecast horizon separately.
Includes classification, probabilistic, and spatial metrics.

⚠ SCIENTIFIC HONESTY:
  - Do NOT use accuracy alone (severe weather is class-imbalanced).
  - Do NOT report metrics on training data as model performance.
  - Only report test-set metrics after final evaluation.

Produces JSON files:
  thunderstorm_15m_metrics.json
  lightning_360m_metrics.json
  etc.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
    log_loss,
    confusion_matrix,
)
from sklearn.calibration import calibration_curve

from src.logger import get_logger

log = get_logger("evaluation.metrics")


def evaluate_model(
    y_true: np.ndarray,
    y_pred_proba: np.ndarray,
    threshold: float = 0.5,
    label: str = "model",
) -> dict[str, Any]:
    """
    Compute all evaluation metrics for one model.

    Args:
        y_true: Binary labels (0/1). NaN values are dropped.
        y_pred_proba: Predicted probabilities in [0, 1].
        threshold: Decision threshold for binary prediction.
        label: Identifier for this evaluation (e.g. "thunderstorm_15m").

    Returns:
        Dict of metric name → value.
    """
    # Drop NaN labels
    mask = ~np.isnan(y_true) & ~np.isnan(y_pred_proba)
    yt = y_true[mask]
    yp = y_pred_proba[mask]

    if len(yt) == 0:
        log.warning(f"No valid samples to evaluate for {label}")
        return {"label": label, "error": "no_valid_samples"}

    n_pos = int(yt.sum())
    n_neg = int((1 - yt).sum())
    pos_rate = float(yt.mean())

    # Binary predictions
    yb = (yp >= threshold).astype(int)

    metrics: dict[str, Any] = {
        "label": label,
        "n_samples": int(len(yt)),
        "n_positive": n_pos,
        "n_negative": n_neg,
        "positive_rate": round(pos_rate, 4),
        "threshold": threshold,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }

    # ---- Classification metrics ----
    if n_pos > 0 and n_neg > 0:
        metrics["precision"] = round(float(precision_score(yt, yb, zero_division=0)), 4)
        metrics["recall"] = round(float(recall_score(yt, yb, zero_division=0)), 4)
        metrics["f1"] = round(float(f1_score(yt, yb, zero_division=0)), 4)
        metrics["roc_auc"] = round(float(roc_auc_score(yt, yp)), 4)
        metrics["pr_auc"] = round(float(average_precision_score(yt, yp)), 4)

        cm = confusion_matrix(yt, yb)
        tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
        metrics["true_positive"] = int(tp)
        metrics["false_positive"] = int(fp)
        metrics["true_negative"] = int(tn)
        metrics["false_negative"] = int(fn)
        metrics["false_alarm_ratio"] = round(float(fp / (tp + fp + 1e-9)), 4)
        metrics["probability_of_detection"] = round(float(tp / (tp + fn + 1e-9)), 4)
        metrics["critical_success_index"] = round(float(tp / (tp + fp + fn + 1e-9)), 4)
    else:
        log.warning(f"Skipping classification metrics for {label}: only one class present.")

    # ---- Probabilistic metrics ----
    metrics["brier_score"] = round(float(brier_score_loss(yt, yp)), 4)
    if n_pos > 0 and n_neg > 0:
        metrics["log_loss"] = round(float(log_loss(yt, yp)), 4)

    # ---- Calibration ----
    try:
        n_bins = min(10, max(3, n_pos // 10))
        frac_pos, mean_pred = calibration_curve(yt, yp, n_bins=n_bins)
        # Expected calibration error (ECE)
        ece = float(np.mean(np.abs(frac_pos - mean_pred)))
        metrics["expected_calibration_error"] = round(ece, 4)
        metrics["calibration_curve"] = {
            "mean_predicted": [round(float(v), 4) for v in mean_pred],
            "fraction_positive": [round(float(v), 4) for v in frac_pos],
        }
    except Exception as e:
        log.warning(f"Could not compute calibration curve for {label}: {e}")

    return metrics


def persistence_baseline_metrics(
    y_true: np.ndarray,
    y_current: np.ndarray,
    label: str = "persistence",
) -> dict[str, Any]:
    """
    Evaluate the persistence baseline:
    "If storm/lightning exists now, assume it persists."

    Args:
        y_true: Future true labels.
        y_current: Current state (at T0).
        label: Label for this evaluation.

    Returns:
        Dict of metrics.
    """
    return evaluate_model(y_true, y_current, threshold=0.5, label=f"{label}_persistence")


def evaluate_all_horizons(
    df: pd.DataFrame,
    models: dict,
    feature_cols: list[str],
    horizons: list[int],
    targets: list[str],
    output_dir: Path,
    split_name: str = "test",
    data_mode: str = "DEMO",
) -> dict[str, dict]:
    """
    Evaluate all models at all horizons and save JSON reports.

    Args:
        df: DataFrame with features and labels.
        models: Dict of "target_horizon" → trained model.
        feature_cols: Input feature column names.
        horizons: List of forecast horizons (minutes).
        targets: ["thunderstorm", "lightning"].
        output_dir: Where to save JSON reports.
        split_name: "validation" or "test".

    Returns:
        Nested dict of all metrics.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    all_metrics: dict[str, dict] = {}

    X = df[feature_cols]

    for tgt in targets:
        for h in horizons:
            label_col = f"target_{tgt}_{h}m"
            model_key = f"{tgt}_{h}m"

            if label_col not in df.columns:
                log.warning(f"Label column {label_col} not found.")
                continue

            y_true = df[label_col].values.astype(float)

            # ---- Persistence baseline ----
            current_label = f"target_{tgt}_{horizons[0]}m"
            if current_label in df.columns:
                y_current = df[current_label].values.astype(float)
                pers_metrics = persistence_baseline_metrics(
                    y_true, y_current, label=f"{tgt}_{h}m"
                )
                pers_key = f"{tgt}_{h}m_persistence"
                all_metrics[pers_key] = pers_metrics

            # ---- RF model ----
            if model_key in models:
                model = models[model_key]
                try:
                    y_pred = model.predict_proba(X)
                    rf_metrics = evaluate_model(y_true, y_pred, label=f"{tgt}_{h}m")
                    rf_metrics["model"] = model.name
                    rf_metrics["split"] = split_name
                    rf_metrics["data_mode"] = data_mode
                    rf_metrics["note"] = (
                        "DEMO/SYNTHETIC metrics — not scientifically validated"
                        if data_mode == "DEMO" else "REAL DATA metrics"
                    )
                    all_metrics[f"{tgt}_{h}m"] = rf_metrics

                    # Save individual JSON report
                    fname = output_dir / f"{tgt}_{h}m_metrics.json"
                    with fname.open("w") as f:
                        json.dump(rf_metrics, f, indent=2)
                    log.info(f"Metrics saved: {fname}")

                    # Feature importance
                    fi = model.feature_importance()
                    if fi:
                        fi_path = output_dir / f"{tgt}_{h}m_feature_importance.json"
                        top10 = dict(list(fi.items())[:10])
                        with fi_path.open("w") as f:
                            json.dump({
                                "model": model.name,
                                "note": "Feature importances from trained RF. Values are impurity-based importances.",
                                "top_10": top10,
                            }, f, indent=2)

                except Exception as e:
                    log.error(f"Failed to evaluate {model_key}: {e}")

    return all_metrics
