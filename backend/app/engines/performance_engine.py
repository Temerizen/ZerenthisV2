import json, os

BASE = os.path.join(os.getcwd(), "backend", "data")
PERF_FILE = os.path.join(BASE, "performance.json")

def update_performance(balance):
    if os.path.exists(PERF_FILE):
        data = json.load(open(PERF_FILE,"r",encoding="utf-8"))
    else:
        data = {"equity_curve":[]}

    data["equity_curve"].append(balance)

    peak = max(data["equity_curve"])
    drawdown = round((peak - balance)/peak,4) if peak else 0

    data["max_drawdown"] = max(data.get("max_drawdown",0), drawdown)

    json.dump(data, open(PERF_FILE,"w",encoding="utf-8"), indent=2)
    return data
