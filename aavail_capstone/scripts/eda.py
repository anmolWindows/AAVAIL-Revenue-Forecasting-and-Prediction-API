from pathlib import Path
import matplotlib.pyplot as plt
from app.ingest import load_data

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "artifacts"
out.mkdir(exist_ok=True)

df = load_data()
daily = df.groupby("date", as_index=False)["revenue"].sum()

plt.figure(figsize=(10, 5))
plt.plot(daily["date"], daily["revenue"])
plt.title("Daily Revenue")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(out / "daily_revenue.png")
plt.close()

country = df.groupby("country", as_index=False)["revenue"].sum().sort_values("revenue")
plt.figure(figsize=(8, 5))
plt.barh(country["country"], country["revenue"])
plt.title("Revenue by Country")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig(out / "revenue_by_country.png")
plt.close()

print("EDA plots saved to artifacts/")
