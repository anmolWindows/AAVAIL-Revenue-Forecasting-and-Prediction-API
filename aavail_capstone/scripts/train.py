from pathlib import Path
import json
from app.ingest import load_data, make_features
from app.model import train, save_model

ROOT = Path(__file__).resolve().parents[1]
df = make_features(load_data())
model, metrics = train(df)
save_model(model, ROOT / "artifacts" / "model.joblib")
(ROOT / "artifacts" / "metrics.json").write_text(json.dumps(metrics, indent=2))
print(json.dumps(metrics, indent=2))
