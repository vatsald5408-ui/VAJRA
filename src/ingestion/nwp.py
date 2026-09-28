"""
nwp.py – NWP/reanalysis data ingestion.

Provides:
  - NWPSource dataclass (pluggable interface)
  - ERA5Adapter (requires CDS API key and cdsapi package)
  - NWPFileAdapter (for locally downloaded NetCDF/GRIB files)

⚠ ERA5 is HISTORICAL REANALYSIS, not an operational future forecast.
⚠ Never label ERA5 as a forecast or future prediction.
⚠ ACCESS_STATUS = MANUAL (requires CDS API registration)
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

log = get_logger("ingestion.nwp")


@dataclass
class NWPSource:
    """
    Descriptor for an NWP or reanalysis data source.
    Designed to be pluggable — ERA5 can be replaced by GFS, ECMWF-FC, etc.
    """
    name: str                    # e.g. "ERA5", "GFS", "MERRA2"
    provider: str
    temporal_resolution: str     # e.g. "hourly"
    spatial_resolution_deg: float
    data_type: str               # "reanalysis" | "forecast" | "analysis"
    variables: list[str]
    pressure_levels: list[int]   # hPa
    access_status: str           # DEMO / MANUAL / RESTRICTED
    notes: str = ""


@dataclass
class NWPSnapshot:
    """NWP fields at a single timestamp."""
    source_name: str
    timestamp: datetime
    data_type: str            # "reanalysis" | "forecast" | "analysis"
    data_mode: str            # "DEMO/SYNTHETIC" | "REAL"
    surface: dict[str, np.ndarray] = field(default_factory=dict)
    pressure_levels: dict[int, dict[str, np.ndarray]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class NWPIngester(ABC):
    """Abstract base for NWP/reanalysis ingesters."""

    @abstractmethod
    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        ...

    @abstractmethod
    def load(self, timestamp: datetime) -> NWPSnapshot | None:
        ...

    @property
    @abstractmethod
    def data_mode(self) -> str:
        ...

    @property
    @abstractmethod
    def source(self) -> NWPSource:
        ...


class ERA5Adapter(NWPIngester):
    """
    Adapter for ERA5 reanalysis via ECMWF CDS API.

    ⚠ ERA5 is HISTORICAL REANALYSIS.
    ⚠ Must NOT be used or labelled as a future forecast.
    ⚠ Requires: ERA5_CDS_KEY and ERA5_CDS_URL in .env
    ⚠ Requires: pip install cdsapi

    Data is retrieved per-request and cached locally.
    For large-scale use, pre-download files using the CDS API
    and use NWPFileAdapter instead.
    """

    ERA5_SOURCE = NWPSource(
        name="ERA5",
        provider="ECMWF/Copernicus",
        temporal_resolution="hourly",
        spatial_resolution_deg=0.25,
        data_type="reanalysis",
        variables=[
            "2m_temperature", "2m_dewpoint_temperature", "surface_pressure",
            "10m_u_component_of_wind", "10m_v_component_of_wind",
            "total_cloud_cover", "total_precipitation",
            "boundary_layer_height",
            "convective_available_potential_energy",
            "convective_inhibition",
        ],
        pressure_levels=[850, 700, 500, 300],
        access_status="MANUAL",
        notes=(
            "ERA5 is historical reanalysis. Not a future forecast. "
            "Access via https://cds.climate.copernicus.eu/. "
            "Register and obtain CDS API key. "
            "Use cdsapi Python package."
        ),
    )

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cds_key = os.environ.get("ERA5_CDS_KEY", "").strip() or None
        self.cds_url = os.environ.get("ERA5_CDS_URL", "https://cds.climate.copernicus.eu/api").strip()

        if not self.cds_key:
            raise EnvironmentError(
                "ERA5_CDS_KEY not set. "
                "ERA5 reanalysis data unavailable. "
                "Register at https://cds.climate.copernicus.eu/ "
                "and set ERA5_CDS_KEY in .env"
            )

    @property
    def data_mode(self) -> str:
        return "REAL"

    @property
    def source(self) -> NWPSource:
        return self.ERA5_SOURCE

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        raise NotImplementedError("ERA5 available times: scan cache_dir or query CDS API.")

    def load(self, timestamp: datetime) -> NWPSnapshot | None:
        raise NotImplementedError(
            "ERA5 load: implement using cdsapi to download hourly data. "
            "See docs/data_sources.md for detailed instructions."
        )


class NWPFileAdapter(NWPIngester):
    """
    Load NWP/reanalysis data from locally downloaded NetCDF/GRIB files.

    Expected filename convention:
        YYYYMMDD_HH_<source>.nc or YYYYMMDD_HH_<source>.grib2

    Place files in data/raw/nwp/.
    """

    SUPPORTED_EXTS = [".nc", ".nc4", ".grib", ".grib2", ".grb2"]

    def __init__(self, data_root: Path, source_name: str = "ERA5"):
        self.data_root = data_root
        self._source = NWPSource(
            name=source_name,
            provider="Local file",
            temporal_resolution="hourly",
            spatial_resolution_deg=0.25,
            data_type="reanalysis",
            variables=[],
            pressure_levels=[850, 700, 500, 300],
            access_status="MANUAL",
        )

    @property
    def data_mode(self) -> str:
        return "REAL"

    @property
    def source(self) -> NWPSource:
        return self._source

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        times = []
        for path in sorted(self.data_root.rglob("*")):
            if path.suffix.lower() not in self.SUPPORTED_EXTS:
                continue
            try:
                parts = path.stem.split("_")
                ts = datetime.strptime(parts[0] + parts[1], "%Y%m%d%H")
                if start <= ts <= end:
                    times.append(ts)
            except (ValueError, IndexError):
                continue
        return sorted(set(times))

    def load(self, timestamp: datetime) -> NWPSnapshot | None:
        try:
            import xarray as xr
        except ImportError:
            log.error("xarray not installed. Cannot load NWP files.")
            return None

        ts_str = timestamp.strftime("%Y%m%d_%H")
        for ext in self.SUPPORTED_EXTS:
            for candidate in self.data_root.rglob(f"{ts_str}*{ext}"):
                try:
                    ds = xr.open_dataset(candidate, engine="netcdf4")
                    surface = {}
                    for var in ds.data_vars:
                        surface[var] = ds[var].values.astype(np.float32)
                    return NWPSnapshot(
                        source_name=self._source.name,
                        timestamp=timestamp,
                        data_type=self._source.data_type,
                        data_mode="REAL",
                        surface=surface,
                    )
                except Exception as e:
                    log.warning(f"Could not load NWP file {candidate}: {e}")
        return None


def get_nwp_ingester(data_mode: str, data_root: Path | None = None) -> NWPIngester:
    if data_mode == "DEMO":
        log.info("[DEMO MODE] NWP ingester: use SyntheticDataGenerator.")
        return _DemoNWPStub()
    era5_key = os.environ.get("ERA5_CDS_KEY", "").strip()
    if era5_key and data_root:
        try:
            return ERA5Adapter(data_root)
        except EnvironmentError as e:
            log.warning(str(e))
    if data_root and data_root.exists():
        return NWPFileAdapter(data_root)
    log.warning("No real NWP data source configured. Falling back to DEMO.")
    return _DemoNWPStub()


class _DemoNWPStub(NWPIngester):
    _src = NWPSource(
        name="SYNTHETIC_NWP", provider="SYNTHETIC",
        temporal_resolution="15min", spatial_resolution_deg=0.05,
        data_type="reanalysis", variables=[], pressure_levels=[],
        access_status="DEMO",
    )

    @property
    def data_mode(self) -> str:
        return "DEMO/SYNTHETIC"

    @property
    def source(self) -> NWPSource:
        return self._src

    def available_times(self, start: datetime, end: datetime) -> list[datetime]:
        return []

    def load(self, timestamp: datetime) -> NWPSnapshot | None:
        return None
