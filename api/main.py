"""
main.py – FastAPI service for thunderstorm/lightning nowcasting.

Endpoints:
    GET  /health
    GET  /config
    GET  /data/status
    GET  /latest
    GET  /forecast
    GET  /forecast/{timestamp}
    GET  /forecast/grid
    GET  /forecast/summary
    GET  /metrics
    POST /inference

Runs in DEMO mode by default (no API keys required).
"""
from __future__ import annotations

import json
import pickle
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import load_config
from src.preprocessing.grid import build_common_grid
from src.ingestion.synthetic import SyntheticDataGenerator
from src.inference.predict import NowcastPredictor
from src.logger import get_logger

log = get_logger("api")

app = FastAPI(
    title="Thunderstorm & Lightning Nowcasting API",
    description=(
        "AI/ML Based Nowcasting of Thunderstorm and Lightning — India\n\n"
        "⚠ This is a RESEARCH PROTOTYPE. Not an operational warning system.\n"
        "⚠ DEMO MODE: Synthetic data unless real credentials are configured."
    ),
    version="1.0.0-milestone1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

dashboard_dir = PROJECT_ROOT / "dashboard"
if dashboard_dir.exists():
    app.mount("/dashboard", StaticFiles(directory=str(dashboard_dir), html=True), name="dashboard")

@app.get("/", include_in_schema=False)
async def root_dashboard():
    index_file = dashboard_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Thunderstorm Nowcasting API Running. Navigate to /docs for API documentation."}

# ---- Startup: load config and models ----
_config = None
_grid = None
_predictor = None
_gen = None
_models = {}
_feature_cols = []


@app.on_event("startup")
async def startup():
    global _config, _grid, _predictor, _gen, _models, _feature_cols

    _config = load_config()
    _grid = build_common_grid(_config.region)
    _gen = SyntheticDataGenerator(_grid, seed=42)
    # Generate synthetic storm cells for current session
    now = datetime.now(timezone.utc)
    _gen.generate_sequence(now - timedelta(hours=2), now, interval_minutes=15)

    # Try to load trained models if available
    model_dir = PROJECT_ROOT / "data" / "models"
    if model_dir.exists():
        for pkl_file in model_dir.glob("rf_*.pkl"):
            try:
                from src.models.random_forest import RandomForestNowcaster
                model = RandomForestNowcaster.load(pkl_file)
                key = f"{model.target}_{model.horizon_minutes}m"
                _models[key] = model
                if not _feature_cols:
                    _feature_cols = model._feature_names
            except Exception as e:
                log.warning(f"Could not load model {pkl_file}: {e}")

    if _models:
        _predictor = NowcastPredictor(
            config=_config,
            grid=_grid,
            models=_models,
            feature_cols=_feature_cols,
        )
        log.info(f"API started. Models loaded: {list(_models.keys())}")
    else:
        log.warning("No trained models found. Run pipeline.py first.")

    log.info(f"DATA MODE: {_config.data_mode}")


# ---- Request / Response models ----

class InferenceRequest(BaseModel):
    timestamp: str | None = None   # ISO format; defaults to current time
    region: str | None = None


# ---- Endpoints ----

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "data_mode": _config.data_mode if _config else "DEMO",
        "models_loaded": len(_models),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0-milestone1",
        "disclaimer": "Research prototype. Not an operational warning system.",
    }


@app.get("/config")
async def get_config():
    if not _config:
        raise HTTPException(500, "Config not loaded")
    return {
        "region": {
            "name": _config.region.name,
            "north": _config.region.north,
            "south": _config.region.south,
            "east": _config.region.east,
            "west": _config.region.west,
            "grid_resolution_km": _config.region.grid_resolution_km,
        },
        "data_mode": _config.data_mode,
        "horizons_minutes": _config.horizons_minutes,
        "grid_shape": list(_grid.shape) if _grid else None,
    }


@app.get("/data/status")
async def data_status():
    return {
        "data_mode": _config.data_mode if _config else "DEMO",
        "radar": {
            "status": "DEMO/SYNTHETIC" if _config and _config.data_mode == "DEMO" else "RESTRICTED",
            "note": "Real IMD radar data requires IMD_API_KEY",
        },
        "satellite": {
            "status": "DEMO/SYNTHETIC" if _config and _config.data_mode == "DEMO" else "MANUAL",
            "note": "INSAT data from MOSDAC (manual download required)",
        },
        "lightning": {
            "status": "DEMO/SYNTHETIC" if _config and _config.data_mode == "DEMO" else "RESTRICTED",
            "note": "Real IMD lightning data requires IMD_API_KEY",
        },
        "nwp": {
            "status": "DEMO/SYNTHETIC" if _config and _config.data_mode == "DEMO" else "MANUAL",
            "note": "ERA5 reanalysis (historical, not forecast) requires ERA5_CDS_KEY",
        },
    }


@app.get("/latest")
async def get_latest():
    """Return latest available analysis time."""
    now = datetime.now(timezone.utc)
    t0 = now.replace(second=0, microsecond=0)
    t0 = t0 - timedelta(minutes=t0.minute % 15)
    return {
        "latest_t0": t0.isoformat(),
        "data_mode": _config.data_mode if _config else "DEMO",
        "note": "In DEMO mode, synthetic data is generated for this timestamp.",
    }


@app.get("/forecast")
async def get_forecast(
    timestamp: str | None = Query(None, description="ISO timestamp (defaults to current time)"),
):
    return await _run_inference(timestamp)


@app.get("/forecast/{timestamp}")
async def get_forecast_by_ts(timestamp: str):
    return await _run_inference(timestamp)


@app.get("/forecast/grid")
async def get_forecast_grid(
    timestamp: str | None = Query(None),
    horizon: int = Query(15, description="Forecast horizon in minutes"),
):
    result = await _run_inference(timestamp)
    if "error" in result:
        return result
    grid_rows = result.get("grid", [])
    # Filter to requested horizon columns
    horizon_key = f"{horizon}m_"
    filtered = []
    for row in grid_rows:
        filtered_row = {
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "timestamp": result["timestamp"],
            "horizon_minutes": horizon,
        }
        for k, v in row.items():
            if k.startswith(horizon_key):
                clean_key = k.replace(horizon_key, "")
                filtered_row[clean_key] = v
        filtered.append(filtered_row)
    return {
        "timestamp": result["timestamp"],
        "horizon_minutes": horizon,
        "data_mode": result["data_mode"],
        "grid": filtered,
    }


@app.get("/forecast/summary")
async def get_forecast_summary(timestamp: str | None = Query(None)):
    result = await _run_inference(timestamp)
    return {
        "timestamp": result.get("timestamp"),
        "region": result.get("region"),
        "data_mode": result.get("data_mode"),
        "summary": result.get("summary"),
    }


@app.get("/metrics")
async def get_metrics():
    """Return available evaluation metric files."""
    eval_dir = PROJECT_ROOT / "data" / "evaluation"
    if not eval_dir.exists():
        return {"status": "no_metrics", "note": "Run pipeline.py first."}
    metrics = {}
    for f in eval_dir.glob("*_metrics.json"):
        with f.open() as fp:
            metrics[f.stem] = json.load(fp)
    return {"metrics": metrics, "note": "Run on DEMO/SYNTHETIC data — not scientifically validated."}


# ---- OpenStreetMap (OSM) Endpoints ----

@app.get("/osm/search")
async def osm_search(q: str = Query(..., description="Location query for OSM Nominatim search")):
    """Search for location coordinates using OpenStreetMap Nominatim API."""
    import urllib.parse
    import urllib.request
    encoded_q = urllib.parse.quote(q)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_q}&format=json&limit=5&countrycodes=in"
    req = urllib.request.Request(url, headers={"User-Agent": "ThunderstormNowcastingApp/1.0 (Research Prototype)"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                results = [
                    {
                        "display_name": item.get("display_name"),
                        "lat": float(item.get("lat")),
                        "lon": float(item.get("lon")),
                        "boundingbox": item.get("boundingbox"),
                        "type": item.get("type"),
                        "class": item.get("class"),
                    }
                    for item in data
                ]
                return {"query": q, "count": len(results), "results": results}
    except Exception as e:
        log.warning(f"OSM Nominatim search failed: {e}")
        return {"query": q, "count": 0, "results": [], "error": str(e)}


@app.get("/osm/reverse")
async def osm_reverse(lat: float = Query(...), lon: float = Query(...)):
    """Reverse geocode coordinates using OpenStreetMap Nominatim API."""
    import urllib.request
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=10"
    req = urllib.request.Request(url, headers={"User-Agent": "ThunderstormNowcastingApp/1.0 (Research Prototype)"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                return {
                    "lat": lat,
                    "lon": lon,
                    "display_name": data.get("display_name", "Unknown Location"),
                    "address": data.get("address", {}),
                }
    except Exception as e:
        log.warning(f"OSM Nominatim reverse failed: {e}")
        return {"lat": lat, "lon": lon, "display_name": f"Location ({lat:.3f}, {lon:.3f})", "error": str(e)}



@app.post("/inference")
async def run_inference(req: InferenceRequest):
    return await _run_inference(req.timestamp)


async def _run_inference(timestamp: str | None) -> dict[str, Any]:
    """Internal: run inference at given timestamp."""
    if not _config or not _grid or not _gen:
        raise HTTPException(500, "System not initialized")

    if timestamp:
        try:
            t0 = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(400, f"Invalid timestamp format: {timestamp}")
    else:
        now = datetime.now(timezone.utc)
        t0 = now.replace(second=0, microsecond=0)
        t0 = t0 - timedelta(minutes=t0.minute % 15)

    if not _predictor:
        # No models: return synthetic structure with placeholder probabilities
        return _demo_forecast_structure(t0, _config, _grid, _gen)

    result = _predictor.predict_at_t0(t0=t0, synthetic_gen=_gen)
    return result


def _demo_forecast_structure(t0, config, grid, gen) -> dict:
    """Generate a demo forecast response when no trained models are available."""
    import numpy as np
    from src.ingestion.synthetic import SyntheticDataGenerator

    # Generate synthetic probabilities (NOT from a trained model)
    gen2 = SyntheticDataGenerator(grid, seed=int(t0.timestamp()) % 1000)
    gen2.generate_sequence(t0 - timedelta(hours=1), t0, interval_minutes=15)
    refl = gen2.radar_reflectivity(t0)

    lat_grid, lon_grid = grid.lat_lon_meshgrid()
    HORIZONS = [15, 30, 60, 120, 180, 360]
    horizons_out = {}
    grid_rows = []

    for h in HORIZONS:
        decay = np.exp(-h / 120.0)
        ts_prob = np.clip(refl / 75.0 * decay + np.random.default_rng(h).normal(0, 0.05, grid.shape), 0, 1)
        lt_prob = np.clip(ts_prob * 0.8, 0, 1)
        horizons_out[f"{h}m"] = {
            "thunderstorm_probability": round(float(ts_prob.max()), 4),
            "lightning_probability": round(float(lt_prob.max()), 4),
            "calibration_applied": False,
            "note": "DEMO — not from a trained model. Run pipeline.py to train models.",
        }

    for i in range(grid.n_lat):
        for j in range(grid.n_lon):
            row = {
                "latitude": float(lat_grid[i, j]),
                "longitude": float(lon_grid[i, j]),
            }
            for h in HORIZONS:
                decay = np.exp(-h / 120.0)
                ts_p = float(np.clip(refl[i, j] / 75.0 * decay, 0, 1))
                row[f"{h}m_thunderstorm_probability"] = round(ts_p, 4)
                row[f"{h}m_lightning_probability"] = round(ts_p * 0.8, 4)
            grid_rows.append(row)

    return {
        "timestamp": t0.isoformat(),
        "region": config.region.name,
        "data_mode": "DEMO/SYNTHETIC",
        "horizons": horizons_out,
        "grid": grid_rows,
        "warning": (
            "No trained models loaded. "
            "Run pipeline.py to train models. "
            "Current probabilities are synthetic placeholders."
        ),
    }
