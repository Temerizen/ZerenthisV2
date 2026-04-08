from pathlib import Path
from backend.app.engines.state_guard import safe_load_json, safe_save_json, normalize_performance

BASE = Path("backend/data")
PERF_FILE = BASE / "performance.json"

def update_performance(balance):
    data = normalize_performance(safe_load_json(PERF_FILE, {}))
    equity_curve = data.get("equity_curve", [])
    equity_curve.append(float(balance))
    data["equity_curve"] = equity_curve

    peak = max(equity_curve) if equity_curve else float(balance)
    drawdown = round((peak - float(balance)) / peak, 4) if peak else 0.0
    data["max_drawdown"] = max(float(data.get("max_drawdown", 0.0) or 0.0), drawdown)

    safe_save_json(PERF_FILE, data)
    return data
