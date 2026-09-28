"""
test_grid_alignment.py – Tests for common grid construction and CRS operations.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
from src.config import load_config, RegionConfig
from src.preprocessing.grid import build_common_grid, latlon_to_grid_indices, CommonGrid


class TestCommonGrid:
    def test_grid_shape_reasonable(self):
        region = RegionConfig(
            name="TEST", north=29.0, south=28.0, east=78.0, west=76.5,
            grid_resolution_km=5.0, crs="EPSG:4326",
        )
        grid = build_common_grid(region)
        assert grid.n_lat > 0
        assert grid.n_lon > 0
        assert grid.n_lat < 500
        assert grid.n_lon < 500

    def test_lats_decreasing(self):
        region = RegionConfig(
            name="TEST", north=29.0, south=28.0, east=78.0, west=76.5,
            grid_resolution_km=5.0, crs="EPSG:4326",
        )
        grid = build_common_grid(region)
        assert all(grid.lats[i] >= grid.lats[i+1] for i in range(len(grid.lats)-1))

    def test_lons_increasing(self):
        region = RegionConfig(
            name="TEST", north=29.0, south=28.0, east=78.0, west=76.5,
            grid_resolution_km=5.0, crs="EPSG:4326",
        )
        grid = build_common_grid(region)
        assert all(grid.lons[i] <= grid.lons[i+1] for i in range(len(grid.lons)-1))

    def test_bounds_respected(self):
        region = RegionConfig(
            name="TEST", north=29.0, south=28.0, east=78.0, west=76.5,
            grid_resolution_km=5.0, crs="EPSG:4326",
        )
        grid = build_common_grid(region)
        assert grid.lats[0] <= 29.0
        assert grid.lats[-1] >= 28.0
        assert grid.lons[0] >= 76.5
        assert grid.lons[-1] <= 78.0

    def test_too_large_raises(self):
        region = RegionConfig(
            name="TEST", north=37.0, south=6.5, east=97.5, west=68.0,
            grid_resolution_km=1.0, crs="EPSG:4326",
        )
        with pytest.raises(ValueError, match="Grid too large"):
            build_common_grid(region, max_cells=100)

    def test_meshgrid_shape(self):
        region = RegionConfig(
            name="TEST", north=29.0, south=28.0, east=78.0, west=76.5,
            grid_resolution_km=5.0, crs="EPSG:4326",
        )
        grid = build_common_grid(region)
        lat_g, lon_g = grid.lat_lon_meshgrid()
        assert lat_g.shape == grid.shape
        assert lon_g.shape == grid.shape


class TestLatLonToIndex:
    def setup_method(self):
        region = RegionConfig(
            name="TEST", north=29.0, south=28.0, east=78.0, west=76.5,
            grid_resolution_km=5.0, crs="EPSG:4326",
        )
        self.grid = build_common_grid(region)

    def test_in_bounds_point(self):
        lat = np.array([28.5])
        lon = np.array([77.2])
        i, j = latlon_to_grid_indices(lat, lon, self.grid)
        assert i[0] >= 0
        assert j[0] >= 0

    def test_out_of_bounds_point(self):
        lat = np.array([35.0])  # outside grid
        lon = np.array([90.0])
        i, j = latlon_to_grid_indices(lat, lon, self.grid)
        assert i[0] == -1
        assert j[0] == -1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
