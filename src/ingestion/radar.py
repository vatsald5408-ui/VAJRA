"""
radar.py – Radar ingestion module.

Provides:
  - RadarSource dataclass (abstraction for a radar station)
  - RadarIngester interface
  - IMDRadarAdapter (real data, requires IMD API key)
  - SyntheticRadarAdapter (DEMO mode fallback)

⚠ RadarSource abstracts per-station differences.
   Not all Indian radars have identical products.
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from src.logger import get_logger

log = get_logger("ingestion.radar")


@dataclass
class RadarSource:
    """
    Metadata for a single radar station.
    Products vary per station — do NOT assume uniform availability.
    """
    id: str
    name: str
    latitude: float
    longitude: float
    elevation_m: float
    coverage_km: float
    available_products: list[str]       # e.g. ["reflectivity", "radial_velocity"]
    temporal_resolution_min: int
    data_format: list[str]              # e.g. ["GeoTIFF", "NetCDF"]
    provider: str = "IMD"
    access_status: str = "RESTRICTED"  # DEMO / MANUAL / RESTRICTED / UNKNOWN


@dataclass
class RadarObservation:
    """One radar observation snapshot on the common grid."""
    radar_id: str
    timestamp: datetime
    data_mode: str                      # "DEMO/SYNTHETIC" or "REAL"
    reflectivity: np.ndarray | None = None      # dBZ, shape (n_lat, n_lon)
    radial_velocity: np.ndarray | None = None   # m/s
    spectrum_width: np.ndarray | None = None    # m/s
    ZDR: np.ndarray | None = None              # dB
    KDP: np.ndarray | None = None              # deg/km
    rhoHV: np.ndarray | None = None            # dimensionless 0–1
    metadata: dict[str, Any] = field(default_factory=dict)

    def available_products(self) -> list[str]:
        prods = []
        for name in ["reflectivity", "radial_velocity", "spectrum_width", "ZDR", "KDP", "rhoHV"]:
            if getattr(self, name) is not None:
                prods.append(name)
        return prods


class RadarIngester(ABC):
    """Abstract base class for radar data ingesters."""

    @abstractmethod
    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        """Return list of available observation timestamps in range."""
        ...

    @abstractmethod
    def load(self, timestamp: datetime, source: RadarSource) -> RadarObservation | None:
        """Load radar observation for a given timestamp and source."""
        ...

    @property
    @abstractmethod
    def data_mode(self) -> str:
        """Return "DEMO/SYNTHETIC" or "REAL"."""
        ...


class IMDRadarAdapter(RadarIngester):
    """
    Adapter for IMD Radar API (real data).

    Requires environment variables:
        IMD_API_KEY
        IMD_API_BASE_URL
        IMD_RADAR_ENDPOINT

    ⚠ If credentials are missing, raises ConfigurationError.
    ⚠ Do NOT hardcode undocumented IMD endpoints.
    """

    def __init__(self):
        self.api_key = os.environ.get("IMD_API_KEY", "").strip() or None
        self.base_url = os.environ.get("IMD_API_BASE_URL", "").strip() or None
        self.radar_endpoint = os.environ.get("IMD_RADAR_ENDPOINT", "").strip() or None

        if not self.api_key:
            raise EnvironmentError(
                "IMD_API_KEY not set. "
                "Real radar data unavailable. "
                "Run in DEMO mode or set IMD_API_KEY in .env"
            )

    @property
    def data_mode(self) -> str:
        return "REAL"

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        raise NotImplementedError(
            "IMD Radar API: available_times not yet implemented. "
            "Implement per official IMD API documentation."
        )

    def load(self, timestamp: datetime, source: RadarSource) -> RadarObservation | None:
        raise NotImplementedError(
            "IMD Radar API: load not yet implemented. "
            "Implement per official IMD API documentation."
        )


class FileRadarAdapter(RadarIngester):
    """
    Adapter for loading radar data from local files (GeoTIFF / NetCDF / GRIB2).

    Use when data has been manually downloaded and placed in data/raw/radar/.
    """

    SUPPORTED_FORMATS = [".tif", ".tiff", ".nc", ".nc4", ".grib", ".grib2", ".grb2"]

    def __init__(self, data_root: Path):
        self.data_root = data_root
        log.info("FileRadarAdapter initialized", data_root=str(data_root))

    @property
    def data_mode(self) -> str:
        return "REAL"

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        """
        Scan data_root for radar files and extract timestamps from filenames.
        Filename convention: YYYYMMDD_HHMM_<radar_id>.<ext>
        """
        times = []
        for path in sorted(self.data_root.rglob("*")):
            if path.suffix.lower() not in self.SUPPORTED_FORMATS:
                continue
            try:
                parts = path.stem.split("_")
                if len(parts) >= 2:
                    ts = datetime.strptime(parts[0] + parts[1], "%Y%m%d%H%M")
                    if start <= ts <= end:
                        times.append(ts)
            except ValueError:
                continue
        return sorted(set(times))

    def load(self, timestamp: datetime, source: RadarSource) -> RadarObservation | None:
        """
        Load a radar file for the given timestamp and source.
        Supports NetCDF and GeoTIFF.
        """
        try:
            import xarray as xr
            import rasterio
        except ImportError:
            log.error("xarray or rasterio not installed. Cannot load real radar files.")
            return None

        ts_str = timestamp.strftime("%Y%m%d_%H%M")
        for ext in self.SUPPORTED_FORMATS:
            candidate = self.data_root / f"{ts_str}_{source.id}{ext}"
            if candidate.exists():
                log.info(f"Loading radar file: {candidate}")
                # Placeholder: actual parsing depends on file format
                # Return structure for downstream processing
                return RadarObservation(
                    radar_id=source.id,
                    timestamp=timestamp,
                    data_mode="REAL",
                    metadata={"file": str(candidate)},
                )
        log.warning(f"No radar file found for {ts_str} {source.id}")
        return None


def get_radar_ingester(data_mode: str, data_root: Path | None = None) -> RadarIngester:
    """
    Factory: returns the appropriate radar ingester based on data mode.

    In DEMO mode: returns a stub that signals synthetic data will be used.
    In REAL mode with API key: returns IMDRadarAdapter.
    In REAL mode with files: returns FileRadarAdapter.
    """
    if data_mode == "DEMO":
        log.info("[DEMO MODE] Radar ingester will use synthetic data.")
        return _DemoRadarStub()

    imd_key = os.environ.get("IMD_API_KEY", "").strip()
    if imd_key:
        try:
            return IMDRadarAdapter()
        except EnvironmentError as e:
            log.warning(f"Could not create IMDRadarAdapter: {e}")

    if data_root and data_root.exists():
        return FileRadarAdapter(data_root)

    log.warning("No real radar data source configured. Falling back to DEMO mode.")
    return _DemoRadarStub()


class _DemoRadarStub(RadarIngester):
    """Stub used in DEMO mode — signals that synthetic generator should be used."""

    @property
    def data_mode(self) -> str:
        return "DEMO/SYNTHETIC"

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        return []

    def load(self, timestamp: datetime, source: RadarSource) -> RadarObservation | None:
        return None  # Caller should use SyntheticDataGenerator instead
