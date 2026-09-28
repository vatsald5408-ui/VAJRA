"""
lightning.py – Lightning data ingestion and gridding.

Provides:
  - LightningEvent dataclass (point observation)
  - LightningIngester interface
  - IMDLightningAdapter (real data, requires IMD API key)
  - GriddedLightningFeatures: converts point events → gridded features
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.preprocessing.grid import CommonGrid, latlon_to_grid_indices
from src.logger import get_logger

log = get_logger("ingestion.lightning")


@dataclass
class LightningEvent:
    """
    A single lightning event observation.
    Polarity, type, and signal strength are optional
    (not all networks provide them).
    """
    timestamp: datetime
    latitude: float
    longitude: float
    polarity: str | None = None          # "CG+", "CG-", "IC", None
    type: str | None = None              # "CG", "IC", None
    signal_strength_kA: float | None = None
    quality: float | None = None         # 0–1 confidence
    data_mode: str = "DEMO/SYNTHETIC"


class LightningIngester(ABC):
    """Abstract base for lightning data ingesters."""

    @abstractmethod
    def load_events(
        self,
        start: datetime,
        end: datetime,
    ) -> pd.DataFrame:
        """
        Load lightning events in [start, end] window.
        Returns DataFrame with columns matching LightningEvent schema.
        """
        ...

    @property
    @abstractmethod
    def data_mode(self) -> str: ...


class IMDLightningAdapter(LightningIngester):
    """
    Adapter for IMD Lightning API (real data).

    Requires: IMD_API_KEY, IMD_API_BASE_URL, IMD_LIGHTNING_ENDPOINT
    """

    def __init__(self):
        self.api_key = os.environ.get("IMD_API_KEY", "").strip() or None
        self.base_url = os.environ.get("IMD_API_BASE_URL", "").strip() or None
        self.endpoint = os.environ.get("IMD_LIGHTNING_ENDPOINT", "").strip() or None

        if not self.api_key:
            raise EnvironmentError(
                "IMD_API_KEY not set. Lightning data unavailable in REAL mode."
            )

    @property
    def data_mode(self) -> str:
        return "REAL"

    def load_events(self, start: datetime, end: datetime) -> pd.DataFrame:
        raise NotImplementedError(
            "IMD Lightning API: implement per official IMD API documentation."
        )


class FileLightningAdapter(LightningIngester):
    """
    Load lightning data from local CSV/Parquet/GeoJSON files.
    Expected columns: timestamp, latitude, longitude,
    [polarity, type, signal_strength_kA, quality]
    """

    SUPPORTED_EXTS = [".csv", ".parquet", ".geojson", ".json"]

    def __init__(self, data_root: Path):
        self.data_root = data_root

    @property
    def data_mode(self) -> str:
        return "REAL"

    def load_events(self, start: datetime, end: datetime) -> pd.DataFrame:
        dfs = []
        for path in sorted(self.data_root.rglob("*")):
            if path.suffix.lower() not in self.SUPPORTED_EXTS:
                continue
            try:
                if path.suffix == ".parquet":
                    df = pd.read_parquet(path)
                elif path.suffix in [".geojson", ".json"]:
                    import geopandas as gpd
                    gdf = gpd.read_file(path)
                    df = pd.DataFrame(gdf.drop(columns="geometry"))
                    df["latitude"] = gdf.geometry.y
                    df["longitude"] = gdf.geometry.x
                else:
                    df = pd.read_csv(path)

                df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                mask = (df["timestamp"] >= pd.Timestamp(start, tz="UTC")) & \
                       (df["timestamp"] <= pd.Timestamp(end, tz="UTC"))
                dfs.append(df[mask])
            except Exception as e:
                log.warning(f"Could not load lightning file {path}: {e}")

        if not dfs:
            return pd.DataFrame()
        return pd.concat(dfs).sort_values("timestamp").reset_index(drop=True)


def get_lightning_ingester(data_mode: str, data_root: Path | None = None) -> LightningIngester:
    if data_mode == "DEMO":
        log.info("[DEMO MODE] Lightning ingester: use SyntheticDataGenerator.")
        return _DemoLightningStub()
    imd_key = os.environ.get("IMD_API_KEY", "").strip()
    if imd_key:
        try:
            return IMDLightningAdapter()
        except EnvironmentError as e:
            log.warning(str(e))
    if data_root and data_root.exists():
        return FileLightningAdapter(data_root)
    log.warning("No real lightning data source. Falling back to DEMO.")
    return _DemoLightningStub()


class _DemoLightningStub(LightningIngester):
    @property
    def data_mode(self) -> str:
        return "DEMO/SYNTHETIC"

    def load_events(self, start: datetime, end: datetime) -> pd.DataFrame:
        return pd.DataFrame()


# ----------------------------------------------------------------
# Gridded lightning feature construction
# ----------------------------------------------------------------

WINDOW_MINUTES = [5, 10, 15, 30, 60]


def grid_lightning_features(
    events: pd.DataFrame,
    t0: datetime,
    grid: CommonGrid,
) -> dict[str, np.ndarray]:
    """
    Convert point lightning events into gridded feature arrays.

    ⚠ LEAKAGE GUARD: Only events at or before t0 are used.
    Events after t0 are for TARGET LABELS only.

    For each grid cell computes:
      - strike_count_{N}min for N in [5, 10, 15, 30, 60]
      - flash_rate_per_min (strikes/min over last 15 min)
      - lightning_density_15min (strikes/km²)
      - lightning_trend_slope (linear slope over windowed counts)
      - dist_nearest_strike_km (distance to nearest strike in last 60 min)

    Args:
        events: DataFrame with columns [timestamp, latitude, longitude, ...].
        t0: Analysis time (datetime, tz-aware UTC recommended).
        grid: CommonGrid.

    Returns:
        Dict mapping feature name → 2D array of shape grid.shape.
    """
    features: dict[str, np.ndarray] = {}

    if events.empty:
        for w in WINDOW_MINUTES:
            features[f"strike_count_{w}min"] = np.zeros(grid.shape, np.float32)
        features["flash_rate_per_min"] = np.zeros(grid.shape, np.float32)
        features["lightning_density_15min"] = np.zeros(grid.shape, np.float32)
        features["lightning_trend_slope"] = np.zeros(grid.shape, np.float32)
        features["dist_nearest_strike_km"] = np.full(grid.shape, np.nan, np.float32)
        return features

    # Normalise timestamps
    df = events.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce").astype(np.float64)
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce").astype(np.float64)
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    t0_utc = pd.Timestamp(t0, tz="UTC") if t0.tzinfo is None else pd.Timestamp(t0)

    # ⚠ LEAKAGE GUARD
    df = df[df["timestamp"] <= t0_utc].copy()

    if df.empty:
        for w in WINDOW_MINUTES:
            features[f"strike_count_{w}min"] = np.zeros(grid.shape, np.float32)
        features["flash_rate_per_min"] = np.zeros(grid.shape, np.float32)
        features["lightning_density_15min"] = np.zeros(grid.shape, np.float32)
        features["lightning_trend_slope"] = np.zeros(grid.shape, np.float32)
        features["dist_nearest_strike_km"] = np.full(grid.shape, np.nan, np.float32)
        return features

    # Map each event to grid cell
    lats = df["latitude"].values
    lons = df["longitude"].values
    i_idx, j_idx = latlon_to_grid_indices(lats, lons, grid)
    valid_mask = (i_idx >= 0) & (j_idx >= 0)
    df = df[valid_mask].copy()
    i_idx = i_idx[valid_mask]
    j_idx = j_idx[valid_mask]
    df["i"] = i_idx
    df["j"] = j_idx

    cell_area_km2 = grid.cell_area_km2()

    # Strike counts per window
    for w in WINDOW_MINUTES:
        cutoff = t0_utc - pd.Timedelta(minutes=w)
        window_df = df[df["timestamp"] >= cutoff]
        count_grid = np.zeros(grid.shape, np.float32)
        for row in window_df.itertuples():
            count_grid[row.i, row.j] += 1
        features[f"strike_count_{w}min"] = count_grid

    # Flash rate per min (15-min window)
    features["flash_rate_per_min"] = features["strike_count_15min"] / 15.0

    # Density (strikes/km²) in 15-min window
    features["lightning_density_15min"] = features["strike_count_15min"] / cell_area_km2

    # Lightning trend: linear slope of 5-min binned counts over last 60 min
    bin_counts = []
    for k in range(12):  # 12 × 5-min bins = 60 min
        t_start = t0_utc - pd.Timedelta(minutes=(k + 1) * 5)
        t_end = t0_utc - pd.Timedelta(minutes=k * 5)
        cnt = len(df[(df["timestamp"] > t_start) & (df["timestamp"] <= t_end)])
        bin_counts.append(cnt)
    if len(bin_counts) > 1 and max(bin_counts) > 0:
        x = np.arange(len(bin_counts), dtype=float)
        slope = float(np.polyfit(x, bin_counts[::-1], 1)[0])
    else:
        slope = 0.0

    # Apply same slope to all cells weighted by local density
    density = features["lightning_density_15min"]
    total_density = density.sum() + 1e-9
    features["lightning_trend_slope"] = (density / total_density * slope).astype(np.float32)

    # Distance to nearest recent strike (km)
    dist_grid = np.full(grid.shape, np.nan, np.float32)
    recent_60 = df[df["timestamp"] >= t0_utc - pd.Timedelta(minutes=60)]
    if not recent_60.empty:
        lat_grid, lon_grid = grid.lat_lon_meshgrid()
        rec_lats = recent_60["latitude"].to_numpy(dtype=np.float64)
        rec_lons = recent_60["longitude"].to_numpy(dtype=np.float64)
        for i in range(grid.n_lat):
            for j in range(grid.n_lon):
                cell_lat = float(lat_grid[i, j])
                cell_lon = float(lon_grid[i, j])
                dlat = rec_lats - cell_lat
                dlon = rec_lons - cell_lon
                cos_lat = np.cos(np.radians(cell_lat))
                d_km = np.sqrt((dlat * 111.32) ** 2 + (dlon * 111.32 * cos_lat) ** 2)
                dist_grid[i, j] = float(d_km.min())
    features["dist_nearest_strike_km"] = dist_grid

    return features
