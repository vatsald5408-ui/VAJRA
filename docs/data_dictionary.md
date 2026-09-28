# Data Dictionary: Spatiotemporal Nowcasting Features & Targets

This document defines all input features, derived variables, and target definitions used in the spatiotemporal multimodal nowcasting system for India.

---

## 1. Grid Specifications
- **CRS:** WGS84 (`EPSG:4326`) for API/Dashboard; `EPSG:7755` for metric distance computations.
- **Default Resolution:** Configurable (e.g. 5 km cell spacing for Delhi-NCR prototype).
- **Indexing:** `i` (latitude row from North to South), `j` (longitude column from West to East).

---

## 2. Input Features (Extracted at $T_0$ using history $[T_{-60}, T_0]$)

### Radar Features
| Feature Name | Description | Unit | Range / Values |
|---|---|---|---|
| `refl_max` | Maximum radar reflectivity at $T_0$ | dBZ | 0.0 – 75.0 |
| `refl_mean` | Spatial/cell mean reflectivity at $T_0$ | dBZ | 0.0 – 75.0 |
| `refl_median` | Cell median reflectivity at $T_0$ | dBZ | 0.0 – 75.0 |
| `refl_above_20dbz` | Binary mask for reflectivity $\ge 20$ dBZ | Binary | 0 or 1 |
| `refl_above_35dbz` | Binary mask for reflectivity $\ge 35$ dBZ (convective threshold) | Binary | 0 or 1 |
| `refl_above_40dbz` | Binary mask for reflectivity $\ge 40$ dBZ | Binary | 0 or 1 |
| `refl_above_45dbz` | Binary mask for reflectivity $\ge 45$ dBZ | Binary | 0 or 1 |
| `refl_above_50dbz` | Binary mask for severe reflectivity $\ge 50$ dBZ | Binary | 0 or 1 |
| `storm_cell_area_fraction` | Local cell convective mask (reflectivity $\ge 35$ dBZ) | Fraction | 0.0 – 1.0 |
| `storm_centroid_i` | Latitude index of storm cell centroid | Grid Index | $0 \dots N_{lat}-1$ |
| `storm_centroid_j` | Longitude index of storm cell centroid | Grid Index | $0 \dots N_{lon}-1$ |
| `spectrum_width_mean` | Radar Doppler spectrum width | m/s | 0.0 – 15.0 |
| `refl_change_10min` | Reflectivity difference: $Refl(T_0) - Refl(T_{-10m})$ | dBZ | -50.0 – +50.0 |
| `refl_change_30min` | Reflectivity difference: $Refl(T_0) - Refl(T_{-30m})$ | dBZ | -50.0 – +50.0 |
| `storm_area_change_30min` | Convective mask change over 30 min | Fraction | -1.0 – +1.0 |
| `centroid_displacement_cells_30min` | Distance storm centroid moved in last 30 min | Grid Cells | $\ge 0.0$ |
| `refl_rolling_max` | Maximum reflectivity across full lookback stack $[T_{-60}, T_0]$ | dBZ | 0.0 – 75.0 |
| `refl_rolling_mean` | Mean reflectivity across full lookback stack | dBZ | 0.0 – 75.0 |
| `refl_rolling_std` | Standard deviation of reflectivity across lookback stack | dBZ | $\ge 0.0$ |

### Satellite Features
| Feature Name | Description | Unit | Range / Values |
|---|---|---|---|
| `ir_bt_mean` | INSAT IR Brightness Temperature | Kelvin (K) | 180.0 – 320.0 |
| `ir_bt_min` | Minimum IR Brightness Temperature at $T_0$ | Kelvin (K) | 180.0 – 320.0 |
| `wv_bt_mean` | INSAT Water Vapour Channel BT | Kelvin (K) | 190.0 – 270.0 |
| `cloud_top_temp` | Inferred Cloud-Top Temperature | Kelvin (K) | 180.0 – 320.0 |
| `vis_mean` | INSAT Visible Channel Reflectance (daytime only) | Normalized | 0.0 – 1.0 / NaN |
| `cloud_top_cooling_rate_30min` | Cooling rate: $IR(T_{-30m}) - IR(T_0)$ (Positive = Convective Growth) | K / 30 min | -50.0 – +50.0 |
| `bt_change_30min` | Brightness temperature change over 30 min | Kelvin (K) | -50.0 – +50.0 |
| `bt_change_60min` | Brightness temperature change over 60 min | Kelvin (K) | -50.0 – +50.0 |
| `cold_cloud_fraction` | Cell mask for IR BT $< 235$ K (Convective Cloud Top) | Binary | 0 or 1 |
| `cloud_area_growth_30min` | Growth of cold cloud top area over 30 min | Fraction | -1.0 – +1.0 |
| `ir_bt_rolling_min` | Minimum IR BT across lookback stack $[T_{-60}, T_0]$ | Kelvin (K) | 180.0 – 320.0 |
| `ir_bt_rolling_mean` | Mean IR BT across lookback stack | Kelvin (K) | 180.0 – 320.0 |
| `ir_bt_rolling_std` | Standard deviation of IR BT across lookback stack | Kelvin (K) | $\ge 0.0$ |

### Lightning Features
| Feature Name | Description | Unit | Range / Values |
|---|---|---|---|
| `strike_count_5min` | Lightning strike count in grid cell in last 5 minutes | Count | $\ge 0$ |
| `strike_count_10min` | Lightning strike count in last 10 minutes | Count | $\ge 0$ |
| `strike_count_15min` | Lightning strike count in last 15 minutes | Count | $\ge 0$ |
| `strike_count_30min` | Lightning strike count in last 30 minutes | Count | $\ge 0$ |
| `strike_count_60min` | Lightning strike count in last 60 minutes | Count | $\ge 0$ |
| `flash_rate_per_min` | Flash rate over last 15 minutes | Strikes / min | $\ge 0.0$ |
| `lightning_density_15min` | Spatial lightning density over last 15 minutes | Strikes / km² | $\ge 0.0$ |
| `lightning_trend_slope` | Slope of 5-min binned strike counts over last 60 min | Linear Slope | $-\infty \dots +\infty$ |
| `dist_nearest_strike_km` | Great-circle distance to nearest strike in last 60 min | km | $\ge 0.0$ / NaN |

### NWP / Reanalysis (ERA5) Features
| Feature Name | Description | Unit | Range / Values |
|---|---|---|---|
| `t2m_K` | 2-meter Air Temperature | Kelvin (K) | 250.0 – 325.0 |
| `td2m_K` | 2-meter Dewpoint Temperature | Kelvin (K) | 240.0 – 315.0 |
| `sp_Pa` | Surface Pressure | Pascals (Pa) | 80000 – 105000 |
| `u10_ms` | 10-meter Zonal (E-W) Wind Velocity | m/s | -50.0 – +50.0 |
| `v10_ms` | 10-meter Meridional (N-S) Wind Velocity | m/s | -50.0 – +50.0 |
| `tcc` | Total Cloud Cover | Fraction | 0.0 – 1.0 |
| `blh_m` | Boundary Layer Height | meters (m) | 50.0 – 4000.0 |
| `tp_m` | Total Accumulating Precipitation | meters (m) | $\ge 0.0$ |
| `wind_speed_10m_ms` | Derived 10m Wind Speed ($\sqrt{u^2 + v^2}$) | m/s | $\ge 0.0$ |
| `wind_dir_10m_deg` | Derived 10m Wind Direction | Degrees (0–360°) | 0.0 – 360.0 |
| `relative_humidity_pct` | Derived 2m Relative Humidity (Magnus formula) | Percentage (%) | 0.0 – 100.0 % |

---

## 3. Target Variable Definitions (Evaluated at $T_0 + H$ min)

Forecast Horizons ($H$): `15`, `30`, `60`, `120`, `180`, `360` minutes.

| Target Name | Type | Definition & Threshold | Source |
|---|---|---|---|
| `target_thunderstorm_{H}m` | Binary (0/1) | $1$ if maximum radar reflectivity within $T_0 + H \pm 15$ min $\ge 40.0$ dBZ; $0$ otherwise. | Radar composite |
| `target_lightning_{H}m` | Binary (0/1) | $1$ if $\ge 1$ lightning strike occurs within 10 km radius during $T_0 + H \pm 15$ min; $0$ otherwise. | Lightning network |
