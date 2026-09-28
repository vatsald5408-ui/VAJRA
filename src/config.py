"""
config.py – Central configuration loader.

Reads YAML config files and environment variables.
Credentials are NEVER hard-coded here.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

# Load .env from project root if present
_PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(_PROJECT_ROOT / ".env", override=False)

CONFIG_DIR = _PROJECT_ROOT / "configs"


def _load_yaml(name: str) -> dict:
    path = CONFIG_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@dataclass
class RegionConfig:
    name: str
    north: float
    south: float
    east: float
    west: float
    grid_resolution_km: float
    crs: str
    metric_crs: str = "EPSG:7755"


@dataclass
class AppConfig:
    region: RegionConfig
    data_sources: dict[str, Any]
    features: dict[str, Any]
    horizons_minutes: list[int]
    split: dict[str, Any]
    target_definition: dict[str, Any]

    # Runtime flags
    data_mode: str = "DEMO"   # "DEMO" or "REAL"
    imd_api_key: str | None = None
    era5_cds_key: str | None = None


def load_config() -> AppConfig:
    region_cfg = _load_yaml("region.yaml")
    ds_cfg = _load_yaml("data_sources.yaml")
    feat_cfg = _load_yaml("features.yaml")
    horiz_cfg = _load_yaml("horizons.yaml")
    split_cfg = _load_yaml("split.yaml")
    target_cfg = _load_yaml("target_definition.yaml")

    active = region_cfg["active_region"]
    r = region_cfg["regions"][active]

    region = RegionConfig(
        name=active,
        north=r["north"],
        south=r["south"],
        east=r["east"],
        west=r["west"],
        grid_resolution_km=r["grid_resolution_km"],
        crs=r["crs"],
        metric_crs=region_cfg.get("metric_crs", "EPSG:7755"),
    )

    # Check credentials
    imd_key = os.environ.get("IMD_API_KEY", "").strip() or None
    era5_key = os.environ.get("ERA5_CDS_KEY", "").strip() or None
    data_mode = "REAL" if (imd_key or era5_key) else "DEMO"

    return AppConfig(
        region=region,
        data_sources=ds_cfg,
        features=feat_cfg,
        horizons_minutes=horiz_cfg["horizons_minutes"],
        split=split_cfg,
        target_definition=target_cfg,
        data_mode=data_mode,
        imd_api_key=imd_key,
        era5_cds_key=era5_key,
    )
