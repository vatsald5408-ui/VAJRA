"""
grid.py – Common spatial grid creation and reprojection utilities.

Creates the common latitude/longitude grid to which all data
sources are regridded. Supports configurable regions and resolutions.

⚠ COORDINATE CONVENTION:
    - External: WGS84 lat/lon (EPSG:4326)
    - Internal metric calculations: EPSG:7755 (India NSRS97 LCC)
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pyproj

from src.config import RegionConfig
from src.logger import get_logger

log = get_logger("grid")


@dataclass
class CommonGrid:
    """
    Represents the common spatial grid to which all data sources
    are reprojected.

    All coordinates are in WGS84 (EPSG:4326).
    """
    region_name: str
    lats: np.ndarray      # 1D array of latitude centres (north to south)
    lons: np.ndarray      # 1D array of longitude centres (west to east)
    resolution_km: float
    crs: str = "EPSG:4326"

    @property
    def n_lat(self) -> int:
        return len(self.lats)

    @property
    def n_lon(self) -> int:
        return len(self.lons)

    @property
    def shape(self) -> tuple[int, int]:
        return (self.n_lat, self.n_lon)

    def lat_lon_meshgrid(self) -> tuple[np.ndarray, np.ndarray]:
        """Return 2D meshgrids (lat_grid, lon_grid) of shape (n_lat, n_lon)."""
        return np.meshgrid(self.lats, self.lons, indexing="ij")

    def latlon_to_index(self, lat: float, lon: float) -> tuple[int, int]:
        """
        Convert a lat/lon coordinate to the nearest grid cell index (i, j).
        Returns (-1, -1) if outside the grid.
        """
        if not (self.lats[-1] <= lat <= self.lats[0] and
                self.lons[0] <= lon <= self.lons[-1]):
            return (-1, -1)
        i = int(np.argmin(np.abs(self.lats - lat)))
        j = int(np.argmin(np.abs(self.lons - lon)))
        return (i, j)

    def cell_area_km2(self) -> float:
        """Approximate area of each grid cell in km²."""
        # Approximate using midpoint latitude
        mid_lat = float(np.mean(self.lats))
        lat_km = self.resolution_km
        lon_km = self.resolution_km * np.cos(np.radians(mid_lat))
        return float(lat_km * lon_km)

    def summary(self) -> dict:
        return {
            "region": self.region_name,
            "n_lat": self.n_lat,
            "n_lon": self.n_lon,
            "lat_range": [float(self.lats[-1]), float(self.lats[0])],
            "lon_range": [float(self.lons[0]), float(self.lons[-1])],
            "resolution_km": self.resolution_km,
            "total_cells": self.n_lat * self.n_lon,
            "crs": self.crs,
        }


def build_common_grid(region: RegionConfig, max_cells: int = 500) -> CommonGrid:
    """
    Build the common lat/lon grid from a RegionConfig.

    Grid points are cell centres on a regular lat/lon grid.
    Resolution is converted from km to degrees using the
    equatorial approximation (1 deg ≈ 111.32 km).

    Args:
        region: RegionConfig defining spatial extent and resolution.
        max_cells: Safety guard: maximum cells per dimension.

    Returns:
        CommonGrid instance.

    Raises:
        ValueError: If grid would exceed max_cells per dimension.
    """
    deg_per_km = 1.0 / 111.32
    step = region.grid_resolution_km * deg_per_km

    lats = np.arange(region.north, region.south, -step)
    lons = np.arange(region.west, region.east, step)

    if len(lats) > max_cells or len(lons) > max_cells:
        raise ValueError(
            f"Grid too large: {len(lats)} lat × {len(lons)} lon cells. "
            f"Increase grid_resolution_km or reduce region size. "
            f"Max allowed: {max_cells} per dimension."
        )

    grid = CommonGrid(
        region_name=region.name,
        lats=lats,
        lons=lons,
        resolution_km=region.grid_resolution_km,
        crs=region.crs,
    )
    log.info(
        "Common grid built",
        region=region.name,
        shape=list(grid.shape),
        resolution_km=region.grid_resolution_km,
        total_cells=grid.n_lat * grid.n_lon,
    )
    return grid


def latlon_to_grid_indices(
    lats_pts: np.ndarray,
    lons_pts: np.ndarray,
    grid: CommonGrid,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Map arrays of (lat, lon) points to their nearest grid cell (i, j) indices.
    Points outside the grid get index -1.

    Args:
        lats_pts: 1D array of latitudes.
        lons_pts: 1D array of longitudes.
        grid: CommonGrid.

    Returns:
        (i_indices, j_indices) as integer arrays.
    """
    i_idx = np.searchsorted(-grid.lats, -lats_pts, side="left").clip(0, grid.n_lat - 1)
    j_idx = np.searchsorted(grid.lons, lons_pts, side="left").clip(0, grid.n_lon - 1)

    # Mark out-of-bounds points
    out_of_bounds = (
        (lats_pts < grid.lats[-1]) | (lats_pts > grid.lats[0]) |
        (lons_pts < grid.lons[0]) | (lons_pts > grid.lons[-1])
    )
    i_idx[out_of_bounds] = -1
    j_idx[out_of_bounds] = -1

    return i_idx.astype(np.int32), j_idx.astype(np.int32)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great-circle distance in km between two lat/lon points.
    """
    R = 6371.0
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2) ** 2
    return float(2 * R * np.arcsin(np.sqrt(a)))
