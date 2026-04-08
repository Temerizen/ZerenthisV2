from pathlib import Path
import json

FILE = Path("backend/data/market/validation.json")

def load_validation():
    if not FILE.exists():
        return {"runs": []}
    return json.loads(FILE.read_text())

def save_validation(data):
    FILE.write_text(json.dumps(data, indent=2))

def record_run(result):
    data = load_validation()
    data["runs"].append(result)
    save_validation(data)

def reliability_score():
    data = load_validation()
    runs = data["runs"][-10:]

    if not runs:
        return 0

    profits = [r.get("profit", 0) for r in runs]
    wins = sum(1 for p in profits if p > 0)

    avg_profit = sum(profits) / len(profits)

    return round((wins / len(runs)) * 100 + avg_profit, 2)
