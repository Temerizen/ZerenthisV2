import json, os

BASE = os.path.join(os.getcwd(), "backend", "data")
PERF_FILE = os.path.join(BASE, "performance.json")

def update_performance(balance):
    os.makedirs(BASE, exist_ok=True)

    data = {}
    if os.path.exists(PERF_FILE):
        try:
            with open(PERF_FILE, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        except Exception:
            data = {}

    equity_curve = data.get("equity_curve", [])
    if not isinstance(equity_curve, list):
        equity_curve = []

    equity_curve.append(float(balance))
    data["equity_curve"] = equity_curve

    peak = max(equity_curve) if equity_curve else float(balance)
    drawdown = round((peak - float(balance)) / peak, 4) if peak else 0.0
    data["max_drawdown"] = max(float(data.get("max_drawdown", 0.0) or 0.0), drawdown)

    with open(PERF_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return data
