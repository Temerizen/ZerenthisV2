import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path("backend/data/market")
LEADERBOARD_FILE = DATA_DIR / "strategy_leaderboard.json"

DEFAULT_BOARD = {
    "strategies": {},
    "last_best_strategy": None
}

def _clean_row(row: Dict[str, Any]) -> Dict[str, Any]:
    row = row or {}
    return {
        "runs": int(row.get("runs", 0) or 0),
        "total_profit": float(row.get("total_profit", 0.0) or 0.0),
        "total_trades": int(row.get("total_trades", 0) or 0),
        "wins": int(row.get("wins", 0) or 0),
        "losses": int(row.get("losses", 0) or 0),
        "last_profit": float(row.get("last_profit", 0.0) or 0.0),
        "avg_profit": float(row.get("avg_profit", 0.0) or 0.0),
        "avg_winrate": float(row.get("avg_winrate", 0.0) or 0.0),
    }

def load_strategy_board() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if LEADERBOARD_FILE.exists():
        try:
            raw = json.loads(LEADERBOARD_FILE.read_text(encoding="utf-8"))
            board = {
                "strategies": {},
                "last_best_strategy": raw.get("last_best_strategy")
            }
            for name, row in (raw.get("strategies", {}) or {}).items():
                board["strategies"][name] = _clean_row(row)
            return board
        except Exception:
            return DEFAULT_BOARD.copy()
    return DEFAULT_BOARD.copy()

def save_strategy_board(board: Dict[str, Any]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LEADERBOARD_FILE.write_text(json.dumps(board, indent=2), encoding="utf-8")

def update_strategy_board(results: Dict[str, Any], best_strategy: str):
    board = load_strategy_board()

    for name, stats in (results or {}).items():
        row = _clean_row(board["strategies"].get(name, {}))

        row["runs"] += 1
        row["total_profit"] += float(stats.get("profit", 0) or 0)
        row["total_trades"] += int(stats.get("trades", 0) or 0)
        row["wins"] += int(stats.get("wins", 0) or 0)
        row["losses"] += int(stats.get("losses", 0) or 0)
        row["last_profit"] = float(stats.get("profit", 0) or 0)
        row["avg_profit"] = round(row["total_profit"] / max(row["runs"], 1), 4)
        row["avg_winrate"] = round((row["wins"] / max(row["total_trades"], 1)) * 100, 2)

        board["strategies"][name] = row

    board["last_best_strategy"] = best_strategy
    save_strategy_board(board)
    return board

