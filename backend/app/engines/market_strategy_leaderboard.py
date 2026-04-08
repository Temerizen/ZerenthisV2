import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path("backend/data/market")
FILE = DATA_DIR / "strategy_leaderboard.json"

DEFAULT = {
    "strategies": {
        "momentum": {"wins": 0, "losses": 0, "pnl": 0.0, "cycles_won": 0},
        "reversal": {"wins": 0, "losses": 0, "pnl": 0.0, "cycles_won": 0},
        "conservative": {"wins": 0, "losses": 0, "pnl": 0.0, "cycles_won": 0}
    },
    "active_strategy": "momentum"
}

def load_leaderboard() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if FILE.exists():
        try:
            return json.loads(FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT.copy()
    return DEFAULT.copy()

def save_leaderboard(data: Dict[str, Any]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def update_competition_results(results: Dict[str, Any], best_strategy: str):
    board = load_leaderboard()

    for strategy_name, payload in results.items():
        if strategy_name not in board["strategies"]:
            board["strategies"][strategy_name] = {"wins": 0, "losses": 0, "pnl": 0.0, "cycles_won": 0}

        score = payload.get("score", {})
        pnl = float(score.get("total_profit", 0))
        wins = int(score.get("wins", 0))
        losses = int(score.get("losses", 0))

        board["strategies"][strategy_name]["wins"] += wins
        board["strategies"][strategy_name]["losses"] += losses
        board["strategies"][strategy_name]["pnl"] = round(board["strategies"][strategy_name]["pnl"] + pnl, 2)

    board["strategies"][best_strategy]["cycles_won"] += 1
    board["active_strategy"] = best_strategy

    save_leaderboard(board)
    return board
