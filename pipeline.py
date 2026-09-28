"""
pipeline.py – End-to-end Milestone 1 pipeline runner.

Runs the complete pipeline:
1. Load config
2. Build common grid
3. Generate synthetic data (DEMO mode)
4. Build training dataset
5. Train Random Forest models
6. Evaluate metrics
7. Save models + reports

Usage:
    python pipeline.py

Or with options:
    python pipeline.py --max-t0s 20 --output-dir data/samples
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import load_config
from src.preprocessing.grid import build_common_grid
from src.dataset.builder import build_dataset
from src.dataset.splitter import temporal_split
from src.models.random_forest import train_all_models
from src.evaluation.metrics import evaluate_all_horizons
from src.logger import get_logger, Timer

log = get_logger("pipeline")

HORIZONS = [15, 30, 60, 120, 180, 360]
TARGETS = ["thunderstorm", "lightning"]


def get_feature_cols(df) -> list[str]:
    """Return all input feature column names from dataset."""
    exclude = {
        "sample_id", "timestamp", "grid_i", "grid_j",
        "latitude", "longitude", "data_mode",
    }
    label_prefixes = ("target_thunderstorm_", "target_lightning_")
    return [
        c for c in df.columns
        if c not in exclude and not any(c.startswith(p) for p in label_prefixes)
    ]


def run_pipeline(
    max_t0s: int = 30,
    output_dir: Path = PROJECT_ROOT / "data" / "samples",
    model_dir: Path = PROJECT_ROOT / "data" / "models",
    eval_dir: Path = PROJECT_ROOT / "data" / "evaluation",
) -> dict:
    """
    Run Milestone 1 end-to-end pipeline.

    Args:
        max_t0s: Maximum number of T0 timestamps to process.
                 Keep small for fast testing (30 T0s × grid cells).
        output_dir: Where to save dataset Parquet files.
        model_dir: Where to save trained model files.
        eval_dir: Where to save evaluation JSON reports.
    """
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    log.info(f"=== MILESTONE 1 PIPELINE RUN {run_id} ===")

    # ---- 1. Config ----
    with Timer(log, "Loading configuration"):
        config = load_config()
    log.info(f"DATA MODE: {config.data_mode}")
    log.info(f"REGION: {config.region.name}")

    # ---- 2. Common grid ----
    with Timer(log, "Building common grid"):
        grid = build_common_grid(config.region)
    log.info(f"Grid: {grid.shape} cells, {grid.n_lat * grid.n_lon} total")

    # ---- 3. Date ranges (use short demo period for Milestone 1) ----
    # Using just a few days of synthetic data covering train/val
    train_start = datetime(2022, 7, 1, 0, 0, tzinfo=timezone.utc)
    train_end = datetime(2022, 7, 3, 23, 59, tzinfo=timezone.utc)
    val_start = datetime(2023, 7, 1, 0, 0, tzinfo=timezone.utc)
    val_end = datetime(2023, 7, 2, 23, 59, tzinfo=timezone.utc)

    # ---- 4. Build train dataset ----
    train_path = output_dir / "train.parquet"
    with Timer(log, "Building training dataset"):
        train_df = build_dataset(
            config, grid,
            start=train_start, end=train_end,
            output_path=train_path,
            t0_interval_min=30,
            max_t0s=max_t0s,
        )

    # ---- 5. Build val dataset ----
    val_path = output_dir / "val.parquet"
    with Timer(log, "Building validation dataset"):
        val_df = build_dataset(
            config, grid,
            start=val_start, end=val_end,
            output_path=val_path,
            t0_interval_min=30,
            max_t0s=max(5, max_t0s // 4),
        )

    if train_df.empty:
        log.error("Training dataset is empty. Aborting.")
        return {"status": "failed", "reason": "empty_dataset"}

    feature_cols = get_feature_cols(train_df)
    log.info(f"Feature columns: {len(feature_cols)}")

    # ---- 6. Train models ----
    model_dir.mkdir(parents=True, exist_ok=True)
    with Timer(log, "Training Random Forest models"):
        models = train_all_models(
            train_df=train_df,
            val_df=val_df,
            feature_cols=feature_cols,
            horizons=HORIZONS,
            targets=TARGETS,
            model_dir=model_dir,
        )

    # ---- 7. Evaluate on validation set ----
    eval_dir.mkdir(parents=True, exist_ok=True)
    with Timer(log, "Evaluating models on validation set"):
        all_metrics = evaluate_all_horizons(
            df=val_df,
            models=models,
            feature_cols=feature_cols,
            horizons=HORIZONS,
            targets=TARGETS,
            output_dir=eval_dir,
            split_name="validation",
            data_mode=config.data_mode,
        )

    # ---- 8. Save experiment record ----
    exp_dir = PROJECT_ROOT / "experiments" / run_id
    exp_dir.mkdir(parents=True, exist_ok=True)
    exp_record = {
        "run_id": run_id,
        "data_mode": config.data_mode,
        "region": config.region.name,
        "grid_shape": list(grid.shape),
        "train_samples": len(train_df),
        "val_samples": len(val_df),
        "feature_count": len(feature_cols),
        "feature_names": feature_cols,
        "horizons": HORIZONS,
        "targets": TARGETS,
        "models_trained": list(models.keys()),
        "note": (
            "MILESTONE 1 — DEMO/SYNTHETIC DATA. "
            "Metrics are NOT scientifically validated. "
            "Use for pipeline development only."
        ),
    }
    with (exp_dir / "experiment.json").open("w") as f:
        json.dump(exp_record, f, indent=2)

    log.info(f"=== PIPELINE COMPLETE — Run ID: {run_id} ===")
    log.info(f"Models: {list(models.keys())}")
    log.info(f"Experiment record: {exp_dir}/experiment.json")

    return {
        "status": "success",
        "run_id": run_id,
        "train_samples": len(train_df),
        "val_samples": len(val_df),
        "models": list(models.keys()),
        "metrics_dir": str(eval_dir),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Milestone 1 Pipeline")
    parser.add_argument("--max-t0s", type=int, default=30,
                        help="Max T0 timestamps to process (default: 30)")
    parser.add_argument("--output-dir", type=str,
                        default=str(PROJECT_ROOT / "data" / "samples"))
    args = parser.parse_args()

    result = run_pipeline(
        max_t0s=args.max_t0s,
        output_dir=Path(args.output_dir),
    )
    print(json.dumps(result, indent=2))
