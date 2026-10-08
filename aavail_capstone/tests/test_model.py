import pandas as pd
from app.model import build_pipeline, train, FEATURES

def sample():
    dates = pd.date_range("2025-01-01", periods=20)
    return pd.DataFrame({
        "date": dates,
        "country": ["A"] * 20,
        "purchases": range(1, 21),
        "stream_views": range(10, 30),
        "revenue": [float(x * 2) for x in range(1, 21)],
        "revenue_7d": [5.0 + x for x in range(20)],
        "purchases_7d": [2.0 + x for x in range(20)],
        "views_7d": [11.0 + x for x in range(20)],
        "month": [1] * 20,
        "day_of_year": list(range(1, 21)),
    })

def test_pipeline_has_fit():
    assert hasattr(build_pipeline(), "fit")

def test_training_returns_metrics():
    model, metrics = train(sample())
    assert hasattr(model, "predict")
    assert metrics["model_mae"] >= 0
    assert metrics["baseline_mae"] >= 0
