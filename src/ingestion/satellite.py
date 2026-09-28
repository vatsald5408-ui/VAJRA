"""
satellite.py – Satellite data ingestion.

Provides:
  - SatelliteSource dataclass
  - SatelliteIngester interface
  - MOSDACAdapter (INSAT-3DR/3DS via MOSDAC, requires registration)
  - FileSatelliteAdapter (for manually downloaded files)

⚠ INSAT satellite data from MOSDAC requires account registration
   at https://mosdac.gov.in/. It is not freely accessible via API.
   ACCESS_STATUS = MANUAL
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

log = get_logger("ingestion.satellite")


@dataclass
class SatelliteSource:
    """Metadata for a satellite data product."""
    satellite_name: str
    channel: str
    timestamp: datetime | None
    spatial_resolution_km: float
    projection: str
    file_path: str | None = None
    url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    data_mode: str = "DEMO/SYNTHETIC"


@dataclass
class SatelliteObservation:
    """One satellite observation on the common (or native) grid."""
    source: SatelliteSource
    data: np.ndarray          # 2D array, units depend on channel
    units: str                # "K" for TIR, "normalized" for VIS
    valid: bool = True
    data_mode: str = "DEMO/SYNTHETIC"


class SatelliteIngester(ABC):
    """Abstract base for satellite data ingesters."""

    @abstractmethod
    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        ...

    @abstractmethod
    def load(
        self,
        timestamp: datetime,
        channel: str,
    ) -> SatelliteObservation | None:
        ...

    @property
    @abstractmethod
    def data_mode(self) -> str:
        ...


class MOSDACAdapter(SatelliteIngester):
    """
    Adapter for INSAT-3DR/3DS data from MOSDAC.

    ⚠ ACCESS_STATUS = MANUAL
    Users must register at https://mosdac.gov.in/ and download
    HDF5/NetCDF files manually into data/raw/satellite/.

    This adapter reads those downloaded files.
    Authentication: MOSDAC_USERNAME / MOSDAC_PASSWORD env vars.
    """

    def __init__(self, data_root: Path):
        self.data_root = data_root
        self.username = os.environ.get("MOSDAC_USERNAME", "").strip() or None
        self.password = os.environ.get("MOSDAC_PASSWORD", "").strip() or None
        log.info(
            "MOSDACAdapter initialized",
            data_root=str(data_root),
            authenticated=bool(self.username),
        )

    @property
    def data_mode(self) -> str:
        return "REAL"

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        times = []
        for path in sorted(self.data_root.rglob("*.nc")) + \
                     sorted(self.data_root.rglob("*.h5")) + \
                     sorted(self.data_root.rglob("*.hdf5")):
            try:
                # MOSDAC INSAT filename convention:
                # 3RIMG_YYYYMMDD_HHMM_L1C_ASIA_MER.h5
                parts = path.stem.split("_")
                if len(parts) >= 3:
                    ts = datetime.strptime(parts[1] + parts[2], "%Y%m%d%H%M")
                    if start <= ts <= end:
                        times.append(ts)
            except (ValueError, IndexError):
                continue
        return sorted(set(times))

    def load(self, timestamp: datetime, channel: str) -> SatelliteObservation | None:
        ts_str = timestamp.strftime("%Y%m%d_%H%M")
        for path in self.data_root.rglob(f"*{ts_str}*"):
            try:
                import xarray as xr
                ds = xr.open_dataset(path)
                if channel in ds:
                    data = ds[channel].values
                    return SatelliteObservation(
                        source=SatelliteSource(
                            satellite_name="INSAT-3DR",
                            channel=channel,
                            timestamp=timestamp,
                            spatial_resolution_km=1.0,
                            projection="geostationary",
                            file_path=str(path),
                        ),
                        data=data.astype(np.float32),
                        units="K" if "TIR" in channel or "WV" in channel else "normalized",
                        data_mode="REAL",
                    )
            except Exception as e:
                log.warning(f"Could not load satellite file {path}: {e}")
        return None


class FileSatelliteAdapter(SatelliteIngester):
    """
    Load satellite data from pre-processed local GeoTIFF or NetCDF files.
    """

    SUPPORTED_EXTS = [".tif", ".tiff", ".nc", ".nc4", ".h5", ".hdf5"]

    def __init__(self, data_root: Path):
        self.data_root = data_root

    @property
    def data_mode(self) -> str:
        return "REAL"

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        return []  # Implement per local file naming convention

    def load(self, timestamp: datetime, channel: str) -> SatelliteObservation | None:
        return None  # Implement per local file format


def get_satellite_ingester(data_mode: str, data_root: Path | None = None) -> SatelliteIngester:
    if data_mode == "DEMO":
        log.info("[DEMO MODE] Satellite ingester: use SyntheticDataGenerator.")
        return _DemoSatelliteStub()
    if data_root and data_root.exists():
        return MOSDACAdapter(data_root)
    log.warning("No real satellite data source configured. Falling back to DEMO.")
    return _DemoSatelliteStub()


class _DemoSatelliteStub(SatelliteIngester):
    @property
    def data_mode(self) -> str:
        return "DEMO/SYNTHETIC"

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        return []

    def load(self, timestamp: datetime, channel: str) -> SatelliteObservation | None:
        return None
