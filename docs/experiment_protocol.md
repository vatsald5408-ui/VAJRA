# Experiment Tracking & Reproducibility Protocol

This document defines the protocol for logging, tracking, and reproducing machine learning experiments.

---

## 1. Directory Structure

Every pipeline run creates a timestamped experiment folder under `experiments/`:

```
experiments/
└── 20260926_154409/
    ├── experiment.json        # Full run metadata, parameters, metrics, hashes
    ├── region_snapshot.yaml   # Config snapshot
    ├── features_snapshot.yaml # Config snapshot
    └── metrics_summary.json   # Aggregated evaluation metrics
```

---

## 2. Mandatory Tracking Fields

For every experiment, `experiment.json` must log:

- **Run ID:** Timestamped string (e.g. `20260926_154409`)
- **Data Mode:** `DEMO` or `REAL`
- **Region Name:** `DELHI_NCR`, `INDIA`, etc.
- **Grid Shape & Resolution:** e.g. `(23, 34)` cells, `5.0` km
- **Dataset Hashes:** SHA-256 signatures of training/validation Parquet datasets
- **Feature Columns:** Complete list of input feature names used
- **Model Hyperparameters:** Random seed, `n_estimators`, `max_depth`, `class_weight`
- **Trained Horizons:** List of evaluated forecast horizons ($15 \dots 360$ min)
- **Model Metric Artifact Paths:** Links to horizon-wise evaluation JSON files

---

## 3. Reproducibility Guarantee

To guarantee reproducible model training:
1. Fixed random seed (`random_state=42`) is passed to all numpy, pandas, and scikit-learn models.
2. Complete environment specifications are captured in `requirements.txt`.
3. Train/validation dataset splits are frozen as Parquet artifacts in `data/samples/`.

---

## 4. Scientific Integrity Checklist

Before declaring any benchmark result valid:
- [ ] Verify `check_no_leakage()` passed without warnings.
- [ ] Confirm split separation is event-based / time-based, NOT random row-wise.
- [ ] Verify probability calibration curves and Brier Scores.
- [ ] Ensure `DEMO` metrics are explicitly marked as synthetic and not reported as real operational capability.
