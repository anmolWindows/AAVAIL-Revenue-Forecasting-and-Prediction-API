from pathlib import Path
import time
from flask import Flask, jsonify, request

from app.ingest import load_data, make_features
from app.model import load_model, make_prediction, FEATURES
from app.logging_utils import get_logger
from app.monitoring import record_request, metrics

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "artifacts" / "model.joblib"

app = Flask(__name__)
logger = get_logger()

def _latest_row(df, country=None):
    data = df if country is None else df[df["country"] == country]
    if data.empty:
        raise ValueError("Country not found")
    return data.sort_values("date").iloc[-1]

@app.get("/health")
def health():
    return jsonify({"status": "ok", "model_loaded": MODEL_PATH.exists()})

@app.get("/metrics")
def get_metrics():
    return jsonify(metrics())

@app.get("/predict")
def predict():
    started = time.perf_counter()
    error = False
    try:
        country = request.args.get("country")
        raw = load_data()
        features = make_features(raw)

        if country:
            row = _latest_row(features, country)
            payload = row[FEATURES].to_dict()
            prediction = make_prediction(load_model(MODEL_PATH), payload)
            result = {"country": country, "predicted_revenue": round(prediction, 2)}
        else:
            model = load_model(MODEL_PATH)
            results = []
            for name in sorted(features["country"].unique()):
                row = _latest_row(features, name)
                results.append({
                    "country": name,
                    "predicted_revenue": round(
                        make_prediction(model, row[FEATURES].to_dict()), 2
                    ),
                })
            result = {"predictions": results}
        logger.info("prediction_success")
        return jsonify(result)
    except Exception as exc:
        error = True
        logger.exception("prediction_error")
        return jsonify({"error": str(exc)}), 400
    finally:
        record_request(time.perf_counter() - started, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
