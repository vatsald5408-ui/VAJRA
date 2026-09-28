# Data Sources Registry & Integration Guidelines

This registry documents atmospheric observation data sources for India, access statuses, parameters, and adapter interfaces.

---

## Data Source Summary Table

| Source Name | Provider | Data Type | Key Variables | Spatial Res. | Temporal Res. | Access Status | Authentication |
|---|---|---|---|---|---|---|---|
| **IMD Doppler Weather Radar** | India Meteorological Dept. (IMD) | Grid / Raster | Reflectivity (dBZ), Radial Velocity, Spectrum Width | 1 km | 10 minutes | RESTRICTED | API Key (`IMD_API_KEY`) |
| **INSAT-3D / 3DR Satellite** | ISRO / MOSDAC | Satellite Raster | IR BT (10.8 µm), Water Vapour (6.8 µm), Cloud Top Temp | 4 km (IR), 1 km (VIS) | 15 minutes | MANUAL / RESTRICTED | MOSDAC Credentials |
| **IMD Lightning Network** | IMD | Point Events | Timestamp, Lat, Lon, Polarity, Signal Strength | Point | Seconds / Continuous | RESTRICTED | API Key (`IMD_API_KEY`) |
| **ERA5 Reanalysis** | ECMWF / Copernicus CDS | Grid (GRIB / NetCDF) | 2m Temp, Dewpoint, Surface Pressure, 10m Wind, CAPE | 0.25° (~28 km) | 1 hour | RESTRICTED / MANUAL | CDS API Key (`ERA5_CDS_KEY`) |
| **Synthetic Demo Generator** | Internal Prototype | Simulated Arrays | Synthetic radar cells, satellite IR cooling, lightning clusters | Configurable (5 km) | 15 minutes | AVAILABLE | None (`DEMO` mode) |

---

## 1. IMD Doppler Weather Radar (DWR)
- **Official Documentation:** IMD Weather API Platform
- **Variables:** Reflectivity ($Z$), Radial Velocity ($V$), Spectrum Width ($SW$), dual-polarization variables ($Z_{DR}, K_{DP}, \rho_{HV}$) where available.
- **Config Variables:**
  - `IMD_API_BASE_URL`
  - `IMD_API_KEY`
  - `IMD_RADAR_ENDPOINT`
- **Adapter Interface:** `IMDRadarAdapter` in `src/ingestion/radar.py`
- **Fallback / Off-line Mode:** Accepts raster files (GeoTIFF, NetCDF, GRIB) via `FileRadarAdapter`.

---

## 2. INSAT-3D / 3DR Satellite
- **Provider:** ISRO MOSDAC (Meteorological and Oceanographic Satellite Data Archival Centre)
- **Channels:**
  - TIR-1 (Thermal Infrared, 10.3 – 11.3 µm): Cloud top temperature
  - MIR (Mid-Infrared, 3.8 – 4.0 µm): Nighttime convective detection
  - WV (Water Vapour, 6.5 – 7.1 µm): Upper tropospheric moisture
  - VIS (Visible, 0.55 – 0.75 µm): Daytime cloud structure
- **Adapter Interface:** `INSATSatelliteAdapter` in `src/ingestion/satellite.py`
- **Manual Data Procedure:** Download HDF5/NetCDF granules from MOSDAC portal into `data/raw/satellite/` for offline processing.

---

## 3. IMD Lightning Location Network
- **Observations:** Point strike/flash detections with latitude, longitude, UTC timestamp, and optional signal strength.
- **Config Variables:**
  - `IMD_LIGHTNING_ENDPOINT`
- **Adapter Interface:** `IMDLightningAdapter` and `FileLightningAdapter` in `src/ingestion/lightning.py`
- **Gridding:** Converted to gridded features (`strike_count_15min`, `lightning_density_15min`, etc.) via `grid_lightning_features()`.

---

## 4. ERA5 Atmospheric Reanalysis
- **Provider:** ECMWF Copernicus Climate Change Service (C3S)
- **Variables:**
  - Surface: 2m temperature (`t2m`), 2m dewpoint (`td2m`), surface pressure (`sp`), 10m u/v wind (`u10`, `v10`), total cloud cover (`tcc`), boundary layer height (`blh`).
  - Pressure levels: Geopotential, temperature, relative humidity, u/v wind at 850, 700, 500 hPa.
- **Adapter Interface:** `ERA5NWPAdapter` in `src/ingestion/nwp.py`
- **Scientific Usage Note:** ERA5 is historical reanalysis reconstruction. It is used for historical training/experiments only and **must never be labelled as an operational future NWP forecast**.
