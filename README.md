# AI/ML Based Nowcasting of Thunderstorm and Lightning Using Atmospheric Observations (India)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-green.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/pytest-passing-brightgreen.svg)]()

> ⚠ **IMPORTANT DISCLAIMER:**  
> This is a **RESEARCH PROTOTYPE system**, NOT an operational meteorological warning system.  
> Out-of-the-box it runs in **DEMO / SYNTHETIC MODE** without requiring official API credentials.

---

## 1. Core Problem Statement

Thunderstorm and lightning events across India cause significant damage and loss of life annually. Precise short-term forecasting (nowcasting, **0–6 hour horizon**) requires ingesting high-frequency multimodal observations:
1. **Radar Imagery** (reflectivity, velocity, spectrum width)
2. **Satellite Observations** (INSAT-3D/3DR IR, water vapour, visible channels)
3. **Lightning Detections** (point strike events & flash density)
4. **Atmospheric / NWP Reanalysis** (ERA5 surface & pressure-level fields)

Given atmospheric observations at current time $T_0$ and historical lookback $[T_{-60}, T_0]$, this system predicts for each spatial grid cell:
- **Probability of thunderstorm occurrence**
- **Probability of lightning occurrence**

across multiple future horizons: **+15 min, +30 min, +60 min, +120 min, +180 min, +360 min**.

---

## 2. Architecture Overview

```
DATA SOURCES (Radar, Satellite, Lightning, NWP)
       │
       ▼
DATA INGESTION (Adapters for IMD, INSAT, ERA5 & Demo Generator)
       │
       ▼
SPATIAL & TEMPORAL ALIGNMENT (Common Grid & No-Future-Leakage Guard)
       │
       ▼
FEATURE ENGINEERING (Spatiotemporal Multimodal Features)
       │
       ▼
TARGET LABEL CONSTRUCTION (Radar & Lightning proxies at T0+H)
       │
       ▼
ML MODELING (12 Horizon-Specific Random Forest Classifiers + Baselines)
       │
       ▼
PROBABILITY CALIBRATION (Isotonic / Platt Scaling on Validation Set)
       │
       ▼
EVALUATION & INFERENCE (Brier Score, ROC-AUC, CSI, PR-AUC, Feature Importance)
       │
       ▼
WEB DASHBOARD & REST API (FastAPI + Leaflet Interactive Map)
```

---

## 3. Data Leakage Prevention

Strict temporal enforcement ensures that for any forecast generated at $T_0$:
- Input features use **ONLY** observations timestamped $\le T_0$ ($T_0, T_{-15}, T_{-30}, T_{-45}, T_{-60}$).
- Observations timestamped $> T_0$ ($T_{+15}, T_{+30}, \dots$) are strictly reserved for **target label evaluation**.
- Verified automatically by automated tests in `tests/test_no_leakage.py`.

---

## 4. Installation & Quickstart

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)

### Setup Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

---

## 5. Running the Nowcasting Pipeline

Run the complete Milestone 1 pipeline end-to-end (Demo Mode):

```bash
python pipeline.py --max-t0s 30
```

### What this command executes:
1. Loads configuration (`configs/region.yaml`, `features.yaml`, `horizons.yaml`, `split.yaml`, `target_definition.yaml`).
2. Constructs the common spatial grid (e.g. Delhi-NCR prototype region).
3. Generates synthetic spatiotemporal observation sequences (clearly marked `DEMO/SYNTHETIC`).
4. Extracts 54 multimodal features per grid cell per timestep.
5. Builds training, validation, and test datasets saved as Parquet files.
6. Trains 12 Random Forest baseline models.
7. Evaluates probabilistic metrics (Brier Score, ROC-AUC, PR-AUC, CSI, FAR, Calibration curves) against Persistence baseline.
8. Exports feature importances and JSON evaluation reports.

---

## 6. Running Unit Tests

Run all 31 unit tests covering grid alignment, temporal alignment, feature extraction, label construction, and leakage prevention:

```bash
python -m pytest -v
```

---

## 7. Launching the API & Dashboard

### Start FastAPI Backend
```bash
uvicorn api.main:app --reload --port 8000
```
Interactive API docs available at: `http://localhost:8000/docs`

### API Endpoints:
- `GET /health` — Service status and data mode (`DEMO` or `REAL`).
- `GET /config` — Spatial region, resolution, and horizon configurations.
- `GET /data/status` — Operational status of data sources.
- `GET /latest` — Latest available analysis timestamp.
- `GET /forecast` — Multi-horizon thunderstorm and lightning probability maps.
- `GET /forecast/grid` — Geolocation-indexed grid predictions.
- `GET /metrics` — Model evaluation reports and calibration scores.

### Open Dashboard
Open `dashboard/index.html` in any web browser to view the interactive map, horizon selector, probability legend, and risk timeline.

---

## 8. Real Data Configuration

To enable **REAL DATA MODE**, copy `.env.example` to `.env` and fill in credentials:

```bash
cp .env.example .env
```

```env
DATA_MODE=REAL
IMD_API_KEY=your_official_imd_key
IMD_API_BASE_URL=https://api.imd.gov.in
ERA5_CDS_KEY=your_copernicus_cds_key
DATA_ROOT=./data/raw
```

---

## 9. Documentation Roadmap

Detailed technical documentation is available in `docs/`:
- [`docs/data_dictionary.md`](file:///c:/Users/Vatsal%20Dwivedi/Desktop/sihprob72/docs/data_dictionary.md): Complete data definitions & feature schemas.
- [`docs/model_methodology.md`](file:///c:/Users/Vatsal%20Dwivedi/Desktop/sihprob72/docs/model_methodology.md): Machine learning architecture, calibration, & split protocols.
- [`docs/data_sources.md`](file:///c:/Users/Vatsal%20Dwivedi/Desktop/sihprob72/docs/data_sources.md): Registry of Indian meteorological data providers & adapters.
- [`docs/experiment_protocol.md`](file:///c:/Users/Vatsal%20Dwivedi/Desktop/sihprob72/docs/experiment_protocol.md): Reproducibility guidelines & experiment logging.

---

## 10. License & Scientific Honesty

- **Data Mode Transparency:** The web dashboard and API explicitly show `DATA MODE: DEMO` when running on synthetic/demo data.
- **Baseline Models:** Random Forest is provided as an initial baseline. Future deep learning architectures (ConvLSTM, Transformers) can be integrated by extending `BaseNowcastModel`.
