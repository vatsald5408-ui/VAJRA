"""
synthetic.py – DEMO/SYNTHETIC data generator.

⚠ ALL DATA PRODUCED BY THIS MODULE IS SYNTHETIC.
⚠ It is clearly labelled [DEMO/SYNTHETIC] throughout.
⚠ Do NOT mix with real observations without explicit mode separation.

Generates scientifically PLAUSIBLE (not physically exact) synthetic
atmospheric observations for development and testing purposes.

Physical assumptions (documented):
- Thunderstorm cells are simulated as Gaussian reflectivity blobs
  that move with a background wind field.
- Lightning strikes are clustered near high-reflectivity regions
  (consistent with co-location of lightning and intense convection).
- IR brightness temperature (TIR) is anti-correlated with reflectivity:
  higher reflectivity → colder cloud tops.
- NWP fields are spatially smooth with realistic India monsoon ranges.
- Storm events are more frequent in afternoon (14:00–18:00 IST) and
  monsoon season (June–September), as documented in Indian weather climatology.

References (for plausibility only, not for claimed accuracy):
- Vaidya & Bhardwaj (2012): Indian thunderstorm climatology
- IMD Climatological Atlas of India
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

import numpy as np
import pandas as pd

from src.preprocessing.grid import CommonGrid
from src.logger import get_logger

log = get_logger("synthetic")

DEMO_BANNER = "[DEMO/SYNTHETIC DATA — NOT REAL OBSERVATIONS]"


@dataclass
class SyntheticStormCell:
    """Represents one synthetic convective cell for simulation."""
    center_lat: float
    center_lon: float
    max_reflectivity_dbz: float  # peak dBZ at cell center
    radius_km: float             # approximate e-folding radius
    velocity_ms_lat: float       # northward movement m/s
    velocity_ms_lon: float       # eastward movement m/s
    lifetime_minutes: int        # how long cell exists
    birth_time: datetime

    def is_alive_at(self, t: datetime) -> bool:
        age_min = (t - self.birth_time).total_seconds() / 60
        return 0 <= age_min <= self.lifetime_minutes

    def position_at(self, t: datetime) -> tuple[float, float]:
        """Compute cell position at time t (lat, lon)."""
        dt_sec = (t - self.birth_time).total_seconds()
        lat = self.center_lat + self.velocity_ms_lat * dt_sec / 111320
        lon = self.center_lon + self.velocity_ms_lon * dt_sec / (111320 * np.cos(np.radians(self.center_lat)))
        return lat, lon

    def reflectivity_at(self, t: datetime, grid: CommonGrid) -> np.ndarray:
        """
        Compute synthetic reflectivity field (dBZ) on the common grid.

        Uses a Gaussian bell shape centered on the cell position.
        Reflectivity decays with age (cell growth then dissipation).
        """
        if not self.is_alive_at(t):
            return np.zeros(grid.shape)

        age_min = (t - self.birth_time).total_seconds() / 60
        # Intensity envelope: grow for first third, then decay
        peak_frac = self.lifetime_minutes / 3
        if age_min < peak_frac:
            intensity = age_min / peak_frac
        else:
            intensity = 1.0 - (age_min - peak_frac) / (self.lifetime_minutes - peak_frac)
        intensity = np.clip(intensity, 0.0, 1.0)

        clat, clon = self.position_at(t)
        lat_grid, lon_grid = grid.lat_lon_meshgrid()

        # Approximate km distance from cell center
        dlat_km = (lat_grid - clat) * 111.32
        dlon_km = (lon_grid - clon) * 111.32 * np.cos(np.radians(clat))
        dist_km = np.sqrt(dlat_km ** 2 + dlon_km ** 2)

        # Gaussian reflectivity profile
        refl = self.max_reflectivity_dbz * intensity * np.exp(-0.5 * (dist_km / self.radius_km) ** 2)
        return refl.astype(np.float32)


class SyntheticDataGenerator:
    """
    Generates synthetic atmospheric observations for the common grid
    across a time range.

    ⚠ DATA MODE: DEMO/SYNTHETIC
    ⚠ All values are plausible but NOT real measurements.
    """

    def __init__(
        self,
        grid: CommonGrid,
        seed: int = 42,
        n_storm_cells: int = 3,
    ):
        self.grid = grid
        self.rng = np.random.default_rng(seed)
        self.n_storm_cells = n_storm_cells
        self._storm_cells: list[SyntheticStormCell] = []
        log.info(f"{DEMO_BANNER} SyntheticDataGenerator initialized", region=grid.region_name)

    def _generate_storm_cells(
        self,
        t0: datetime,
        n_hours: int = 6,
    ) -> list[SyntheticStormCell]:
        """
        Generate a set of synthetic storm cells for a given period.
        Cells are distributed randomly across the grid.
        """
        cells = []
        period_minutes = n_hours * 60
        lat_center = (self.grid.lats[0] + self.grid.lats[-1]) / 2
        lon_center = (self.grid.lons[0] + self.grid.lons[-1]) / 2
        lat_range = abs(self.grid.lats[0] - self.grid.lats[-1])
        lon_range = abs(self.grid.lons[-1] - self.grid.lons[0])

        for _ in range(self.n_storm_cells):
            # Random birth time within period
            birth_offset_min = int(self.rng.uniform(0, period_minutes * 0.5))
            birth_t = t0 + timedelta(minutes=birth_offset_min)

            cell = SyntheticStormCell(
                center_lat=lat_center + self.rng.uniform(-lat_range * 0.3, lat_range * 0.3),
                center_lon=lon_center + self.rng.uniform(-lon_range * 0.3, lon_range * 0.3),
                max_reflectivity_dbz=float(self.rng.uniform(35, 65)),  # 35–65 dBZ
                radius_km=float(self.rng.uniform(10, 50)),
                velocity_ms_lat=float(self.rng.uniform(-5, 5)),
                velocity_ms_lon=float(self.rng.uniform(-3, 8)),   # mostly eastward
                lifetime_minutes=int(self.rng.uniform(60, 240)),
                birth_time=birth_t,
            )
            cells.append(cell)
        return cells

    # ----------------------------------------------------------------
    # RADAR
    # ----------------------------------------------------------------
    def radar_reflectivity(self, t: datetime) -> np.ndarray:
        """
        Return synthetic composite reflectivity (dBZ) field.

        ⚠ DEMO/SYNTHETIC — not real radar data.
        Values: 0–70 dBZ (realistic range).
        Background noise: 0–15 dBZ.
        """
        field = np.zeros(self.grid.shape, dtype=np.float32)
        for cell in self._storm_cells:
            field += cell.reflectivity_at(t, self.grid)

        # Background noise (ground clutter / light precipitation)
        noise = self.rng.exponential(scale=3.0, size=self.grid.shape).astype(np.float32)
        field = np.clip(field + noise, 0.0, 75.0)
        return field

    def radar_radial_velocity(self, t: datetime) -> np.ndarray:
        """
        Synthetic radial velocity (m/s). -30 to +30 m/s.
        ⚠ DEMO/SYNTHETIC
        """
        base_u = 5.0  # m/s eastward background
        noise = self.rng.normal(0, 3, self.grid.shape)
        return (base_u + noise).astype(np.float32)

    def radar_spectrum_width(self, t: datetime) -> np.ndarray:
        """
        Synthetic spectrum width (m/s). Higher near storm cores.
        ⚠ DEMO/SYNTHETIC
        """
        refl = self.radar_reflectivity(t)
        sw = 1.0 + (refl / 75.0) * 5.0 + self.rng.uniform(0, 1, self.grid.shape)
        return sw.astype(np.float32)

    # ----------------------------------------------------------------
    # SATELLITE
    # ----------------------------------------------------------------
    def satellite_ir_brightness_temp(self, t: datetime) -> np.ndarray:
        """
        Synthetic TIR1 brightness temperature (K).

        ⚠ DEMO/SYNTHETIC — not real INSAT data.

        Physical assumption: colder cloud tops (lower BT) co-locate
        with higher reflectivity (deep convection).
        Clear sky BT ≈ 295–310 K (surface emission, tropical India).
        Deep convection: BT < 220 K.
        """
        refl = self.radar_reflectivity(t)
        # Map reflectivity [0,70] dBZ → BT [310, 200] K (inverse relationship)
        clear_sky_bt = 305.0
        bt = clear_sky_bt - (refl / 70.0) * 105.0
        noise = self.rng.normal(0, 2, self.grid.shape)
        return np.clip(bt + noise, 180.0, 320.0).astype(np.float32)

    def satellite_wv_brightness_temp(self, t: datetime) -> np.ndarray:
        """
        Synthetic WV channel brightness temperature (K).
        ⚠ DEMO/SYNTHETIC
        """
        ir_bt = self.satellite_ir_brightness_temp(t)
        offset = self.rng.normal(20, 5, self.grid.shape)
        return np.clip(ir_bt + offset, 200.0, 280.0).astype(np.float32)

    def satellite_visible(self, t: datetime) -> np.ndarray | None:
        """
        Synthetic visible channel (0–1 normalized).
        Returns None during nighttime (rough approximation).
        ⚠ DEMO/SYNTHETIC
        """
        # Nighttime: 18:30–06:00 IST (UTC+5:30)
        hour_utc = t.hour
        if hour_utc < 1 or hour_utc > 13:  # approx night IST
            return None

        refl = self.radar_reflectivity(t)
        vis = 0.2 + (refl / 70.0) * 0.8
        noise = self.rng.normal(0, 0.02, self.grid.shape)
        return np.clip(vis + noise, 0.0, 1.0).astype(np.float32)

    # ----------------------------------------------------------------
    # LIGHTNING
    # ----------------------------------------------------------------
    def lightning_events(
        self,
        t: datetime,
        window_minutes: int = 15,
    ) -> pd.DataFrame:
        """
        Generate synthetic lightning event records.

        ⚠ DEMO/SYNTHETIC — not real lightning network data.

        Lightning is clustered near storm cells with high reflectivity.
        Flash rate: approximately 0–50 flashes per minute per cell
        (consistent with published Indian thunderstorm studies).

        Returns:
            DataFrame with columns: timestamp, latitude, longitude,
            polarity, type, signal_strength_kA
        """
        events = []
        for cell in self._storm_cells:
            if not cell.is_alive_at(t):
                continue
            age_min = (t - cell.birth_time).total_seconds() / 60
            # Flash rate peaks at mature stage
            peak_frac = cell.lifetime_minutes / 3
            if age_min < peak_frac:
                intensity = age_min / peak_frac
            else:
                intensity = 1.0 - (age_min - peak_frac) / (cell.lifetime_minutes - peak_frac)
            intensity = max(0.0, intensity)

            # Number of strikes in window
            rate_per_min = intensity * 10.0  # max 10 flashes/min per cell
            n_strikes = int(self.rng.poisson(rate_per_min * window_minutes))

            if n_strikes == 0:
                continue

            clat, clon = cell.position_at(t)
            # Strikes scatter around cell center with std ~ radius/3
            scatter_km = cell.radius_km / 3
            lats_s = self.rng.normal(clat, scatter_km / 111.32, n_strikes)
            lons_s = self.rng.normal(
                clon,
                scatter_km / (111.32 * np.cos(np.radians(clat))),
                n_strikes,
            )
            times_s = [
                t - timedelta(minutes=float(self.rng.uniform(0, window_minutes)))
                for _ in range(n_strikes)
            ]

            for i in range(n_strikes):
                events.append({
                    "timestamp": times_s[i],
                    "latitude": float(np.clip(lats_s[i], self.grid.lats[-1], self.grid.lats[0])),
                    "longitude": float(np.clip(lons_s[i], self.grid.lons[0], self.grid.lons[-1])),
                    "polarity": self.rng.choice(["CG-", "CG+", "IC"], p=[0.7, 0.1, 0.2]),
                    "type": self.rng.choice(["CG", "IC"], p=[0.8, 0.2]),
                    "signal_strength_kA": float(self.rng.uniform(5, 80)),
                    "quality": float(self.rng.uniform(0.7, 1.0)),
                    "data_mode": "DEMO/SYNTHETIC",
                })

        if not events:
            return pd.DataFrame(columns=[
                "timestamp", "latitude", "longitude",
                "polarity", "type", "signal_strength_kA", "quality", "data_mode",
            ])
        df = pd.DataFrame(events)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        return df.sort_values("timestamp").reset_index(drop=True)

    # ----------------------------------------------------------------
    # NWP / ATMOSPHERIC FIELDS
    # ----------------------------------------------------------------
    def nwp_surface(self, t: datetime) -> dict[str, np.ndarray]:
        """
        Generate synthetic NWP surface fields.

        ⚠ DEMO/SYNTHETIC — not ERA5 or any real NWP product.
        ⚠ ERA5 is HISTORICAL REANALYSIS, not a future forecast.

        Ranges based on Indian monsoon climatology (plausible, not exact):
        - T2m: 290–310 K (17–37°C) monsoon season
        - Td2m: 285–300 K
        - Surface pressure: 98000–103000 Pa
        - Wind: 0–15 m/s (monsoon westerlies/easterlies)
        - CAPE: 0–3000 J/kg (documented range for Indian thunderstorms)
        - BLH: 200–2000 m
        """
        lat_grid, lon_grid = self.grid.lat_lon_meshgrid()

        # Temperature decreases northward (gradient ~0.5 K/deg lat)
        t2m_base = 303.0
        lat_center = float(np.mean(self.grid.lats))
        t2m = t2m_base + (lat_center - lat_grid) * 0.5
        t2m += self.rng.normal(0, 0.5, self.grid.shape)

        # Dew point ~2-5 K below T2m during monsoon
        td2m = t2m - self.rng.uniform(2, 5, self.grid.shape)

        sp = 101300 + self.rng.normal(0, 100, self.grid.shape)  # Pa

        # Monsoon westerly winds (south-west India in June-August)
        u10 = 5.0 + self.rng.normal(0, 2, self.grid.shape)
        v10 = 2.0 + self.rng.normal(0, 1, self.grid.shape)

        # CAPE: higher near active storm cells
        refl = self.radar_reflectivity(t)
        cape = np.clip((refl / 45.0) * 1500.0 + self.rng.exponential(200, self.grid.shape), 0, 3000)

        cin = -np.clip(self.rng.exponential(50, self.grid.shape), 0, 500)

        tcc = np.clip((refl / 70.0) * 0.9 + self.rng.uniform(0.0, 0.2, self.grid.shape), 0, 1)

        blh = 500 + self.rng.uniform(0, 1500, self.grid.shape)

        tp = np.clip(self.rng.exponential(1.0, self.grid.shape) * (refl / 50.0), 0, 50) / 1000  # m/hr

        return {
            "t2m": t2m.astype(np.float32),
            "td2m": td2m.astype(np.float32),
            "sp": sp.astype(np.float32),
            "u10": u10.astype(np.float32),
            "v10": v10.astype(np.float32),
            "cape": cape.astype(np.float32),
            "cin": cin.astype(np.float32),
            "tcc": tcc.astype(np.float32),
            "blh": blh.astype(np.float32),
            "tp": tp.astype(np.float32),
            "data_mode": "DEMO/SYNTHETIC",  # type: ignore[dict-item]
        }

    # ----------------------------------------------------------------
    # FULL SNAPSHOT
    # ----------------------------------------------------------------
    def generate_snapshot(self, t: datetime) -> dict[str, Any]:
        """
        Generate all observations for a single timestamp.
        Returns a dict with data_mode clearly set to DEMO/SYNTHETIC.
        """
        return {
            "timestamp": t,
            "data_mode": "DEMO/SYNTHETIC",
            "radar": {
                "reflectivity": self.radar_reflectivity(t),
                "radial_velocity": self.radar_radial_velocity(t),
                "spectrum_width": self.radar_spectrum_width(t),
            },
            "satellite": {
                "ir_brightness_temp": self.satellite_ir_brightness_temp(t),
                "wv_brightness_temp": self.satellite_wv_brightness_temp(t),
                "visible": self.satellite_visible(t),
            },
            "lightning_events": self.lightning_events(t, window_minutes=15),
            "nwp_surface": self.nwp_surface(t),
        }

    def generate_sequence(
        self,
        start: datetime,
        end: datetime,
        interval_minutes: int = 15,
    ) -> list[dict[str, Any]]:
        """
        Generate a time sequence of synthetic observations.
        Storm cells are shared across the sequence for temporal consistency.
        """
        log.info(
            f"{DEMO_BANNER} Generating synthetic sequence",
            start=start.isoformat(),
            end=end.isoformat(),
            interval_min=interval_minutes,
        )

        # Generate storm cells for this period
        n_hours = int((end - start).total_seconds() / 3600) + 1
        self._storm_cells = self._generate_storm_cells(start, n_hours=n_hours)
        log.info(f"  {len(self._storm_cells)} synthetic storm cells generated")

        snapshots = []
        t = start
        while t <= end:
            snapshots.append(self.generate_snapshot(t))
            t += timedelta(minutes=interval_minutes)

        return snapshots
