from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "transactions.csv"

REQUIRED_COLUMNS = {"date", "country", "purchases", "stream_views", "revenue"}

def load_data(path=DATA_PATH):
    df = pd.read_csv(path, parse_dates=["date"])
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Input dataset is empty")
    return df.sort_values("date").reset_index(drop=True)

def aggregate_daily(df):
    out = (
        df.groupby(["date", "country"], as_index=False)
          .agg(
              revenue=("revenue", "sum"),
              purchases=("purchases", "sum"),
              stream_views=("stream_views", "sum"),
          )
    )
    return out.sort_values(["country", "date"]).reset_index(drop=True)

def make_features(df):
    daily = aggregate_daily(df)
    daily["day_of_year"] = daily["date"].dt.dayofyear
    daily["month"] = daily["date"].dt.month
    daily["year"] = daily["date"].dt.year
    daily["revenue_7d"] = (
        daily.groupby("country")["revenue"]
        .transform(lambda s: s.rolling(7, min_periods=1).mean())
    )
    daily["purchases_7d"] = (
        daily.groupby("country")["purchases"]
        .transform(lambda s: s.rolling(7, min_periods=1).mean())
    )
    daily["views_7d"] = (
        daily.groupby("country")["stream_views"]
        .transform(lambda s: s.rolling(7, min_periods=1).mean())
    )
    return daily
