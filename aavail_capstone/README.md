# AAVAIL Revenue Forecasting Capstone

A small, reproducible machine-learning workflow for forecasting monthly AAVAIL revenue by country.

> **Important:** This repository uses synthetic/sample transaction data so it can run without proprietary course files. Replace `data/transactions.csv` with the official course dataset if your course requires it.

## Project features

- Data ingestion and feature engineering
- Exploratory data analysis with saved visualizations
- Regression model and naive baseline
- Flask REST API for a country or all countries
- Model persistence with joblib
- JSON logging
- Lightweight performance monitoring
- Unit tests for API, model, and logging
- Docker container
- One-command test execution

## Quick start

```bash
pip install -r requirements.txt
python scripts/train.py
python scripts/eda.py
pytest -q
python app/api.py
```

API examples:

```bash
curl "http://127.0.0.1:5000/predict?country=United%20Kingdom"
curl "http://127.0.0.1:5000/predict"
curl "http://127.0.0.1:5000/health"
curl "http://127.0.0.1:5000/metrics"
```

## Docker

```bash
docker build -t aavail-capstone .
docker run --rm -p 5000:5000 aavail-capstone
```

## Project structure

- `app/ingest.py` — data ingestion and feature creation
- `app/model.py` — model training, prediction, and baseline
- `app/api.py` — Flask API
- `app/logging_utils.py` — application logging
- `app/monitoring.py` — request/performance monitoring
- `scripts/train.py` — train and save the model
- `scripts/eda.py` — generate EDA plots
- `tests/` — automated tests
- `data/transactions.csv` — synthetic sample data
- `artifacts/` — generated model and EDA outputs

## Model

The project predicts next-month revenue using recent transaction activity and calendar/country features. A linear regression model is compared with a simple rolling-mean baseline.

## Reproducibility

The sample data generator is deterministic. The project is intended as an educational deployment template; replace the synthetic dataset with the official project data when available.
