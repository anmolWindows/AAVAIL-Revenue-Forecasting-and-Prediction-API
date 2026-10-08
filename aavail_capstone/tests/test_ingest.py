import pandas as pd
from app.ingest import aggregate_daily, make_features

def test_aggregate_daily():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-01", "2025-01-01"]),
        "country": ["A", "A"],
        "purchases": [2, 3],
        "stream_views": [10, 20],
        "revenue": [5.0, 7.0],
    })
    out = aggregate_daily(df)
    assert len(out) == 1
    assert out.iloc[0]["revenue"] == 12.0

def test_feature_engineering():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-01", "2025-01-02"]),
        "country": ["A", "A"],
        "purchases": [2, 3],
        "stream_views": [10, 20],
        "revenue": [5.0, 7.0],
    })
    out = make_features(df)
    assert "revenue_7d" in out.columns
