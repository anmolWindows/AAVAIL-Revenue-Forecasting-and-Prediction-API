from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

FEATURES = [
    "country", "purchases", "stream_views", "revenue_7d",
    "purchases_7d", "views_7d", "month", "day_of_year"
]
TARGET = "revenue"

def build_pipeline():
    categorical = ["country"]
    numeric = [x for x in FEATURES if x not in categorical]
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric),
    ])
    return Pipeline([("preprocess", pre), ("model", LinearRegression())])

def add_target(df):
    out = df.copy()
    # Next-day revenue is the forecasting target.
    out["target"] = out.groupby("country")["revenue"].shift(-1)
    return out.dropna(subset=["target"])

def train(df):
    supervised = add_target(df)
    split = int(len(supervised) * 0.8)
    train_df = supervised.iloc[:split]
    test_df = supervised.iloc[split:]
    model = build_pipeline()
    model.fit(train_df[FEATURES], train_df["target"])
    pred = model.predict(test_df[FEATURES])
    mae = float(mean_absolute_error(test_df["target"], pred))
    baseline = float(mean_absolute_error(
        test_df["revenue"], test_df["target"]
    ))
    return model, {"model_mae": mae, "baseline_mae": baseline}

def save_model(model, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)

def load_model(path):
    return joblib.load(path)

def make_prediction(model, row):
    frame = pd.DataFrame([row])
    return float(model.predict(frame[FEATURES])[0])
