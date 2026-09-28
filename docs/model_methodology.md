# Model Methodology & Machine Learning Architecture

This document describes the Machine Learning methodology, training strategy, probability calibration, evaluation metrics, and model extension interfaces.

---

## 1. Problem Formulation

The nowcasting task is framed as a **spatiotemporal multimodal probabilistic binary classification problem**.

Given multimodal observation features $X(T_0)$ gathered across historical lookback time steps $[T_{-60}, T_{-45}, T_{-30}, T_{-15}, T_0]$, predict for each grid cell $c = (i, j)$:

$$\hat{P}_{thunderstorm}(c, T_0 + H) = P(Y_{thunderstorm}(c, T_0 + H) = 1 \mid X(T_0))$$

$$\hat{P}_{lightning}(c, T_0 + H) = P(Y_{lightning}(c, T_0 + H) = 1 \mid X(T_0))$$

for horizons $H \in \{15, 30, 60, 120, 180, 360\}$ minutes.

---

## 2. Baseline Model Architecture

### Random Forest Classifier (`RandomForestNowcaster`)
- **Architecture:** 12 independent binary classifiers (6 horizons $\times$ 2 target variables).
- **Class Imbalance Strategy:** `class_weight="balanced"` to dynamically adjust sample weights for rare storm events without synthetic oversampling of spatially correlated samples.
- **Preprocessing Pipeline:**
  1. `SimpleImputer(strategy="median")`
  2. `StandardScaler()`
  3. `RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_leaf=10, oob_score=True)`

---

## 3. Probability Calibration

Tree-based classifier raw probabilities (`predict_proba`) are not well-calibrated (they tend to push probabilities away from 0 and 1).

### Calibration Methods
1. **Isotonic Regression (`IsotonicRegression(out_of_bounds='clip')`):** Non-parametric monotonic transformation.
2. **Platt Scaling (`LogisticRegression()`):** Parametric logistic transformation.

> ⚠ **Rule:** Calibration is fitted exclusively on the **Validation split** ($Y_{val}$) and never on the training split to prevent data leakage/overfitting.

---

## 4. Train / Validation / Test Splitting Strategy

Individual grid cell samples from the same storm event are highly correlated in space and time. **Random row-wise splitting is strictly prohibited** because it causes massive data leakage.

### Temporal & Event-Based Splitting
- **Training Set:** Historical periods (e.g. 2020–2022).
- **Validation Set:** Intermediate held-out period (e.g. 2023). Used for hyperparameter tuning and probability calibration.
- **Test Set:** Strictly held-out future period (e.g. 2024). Untouched until final benchmark evaluation.

---

## 5. Evaluation Metrics

Evaluated independently per target and per horizon.

### Classification Metrics (Imbalanced Context)
- **Precision:** $TP / (TP + FP)$
- **Recall / POD:** $TP / (TP + FN)$
- **F1 Score:** $2 \cdot (Precision \cdot Recall) / (Precision + Recall)$
- **Critical Success Index (CSI / Threat Score):** $TP / (TP + FP + FN)$
- **False Alarm Ratio (FAR):** $FP / (TP + FP)$
- **ROC-AUC & PR-AUC:** Area under Receiver Operating Characteristic and Precision-Recall curves.

### Probabilistic Metrics
- **Brier Score:** Mean Squared Error of probability predictions relative to binary targets:
  $$BS = \frac{1}{N} \sum_{i=1}^{N} (\hat{p}_i - y_i)^2$$
- **Expected Calibration Error (ECE):** Weighted absolute difference between empirical accuracy and mean predicted probability across probability bins.

---

## 6. Baseline Comparisons

To verify whether the ML model adds predictive value:
1. **Persistence Baseline:** Assumes storm state at $T_0$ persists unchanged into horizon $T_0 + H$.
2. **Random Forest Baseline:** Evaluated against Persistence across all horizons.

---

## 7. Model Extension Interface

The repository defines an extensible abstract base class `BaseNowcastModel` (`src/models/base.py`).

Future deep learning models (XGBoost, LightGBM, ConvLSTM, Temporal CNN, Vision Transformers) can replace the Random Forest baseline by implementing `fit()`, `predict_proba()`, `save()`, and `load()` without modifying the feature extraction, dataset builder, API, or dashboard layers.
