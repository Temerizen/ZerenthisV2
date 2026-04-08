import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path("backend/data/market")
MEMORY_FILE = DATA_DIR / "strategy_memory.json"

DEFAULT_MEMORY = {
    "assets": {},
    "total_runs": 0
}

def load_memory() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8-sig"))
        except Exception:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(memory: Dict[str, Any]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memory, indent=2), encoding="utf-8-sig")

def update_memory(trades):
    memory = load_memory()
    memory["total_runs"] += 1

    for t in trades:
        asset = t.get("asset")
        profit = float(t.get("profit", 0))

        if asset not in memory["assets"]:
            memory["assets"][asset] = {
                "wins": 0,
                "losses": 0,
                "total_profit": 0.0
            }

        if profit > 0:
            memory["assets"][asset]["wins"] += 1
        elif profit < 0:
            memory["assets"][asset]["losses"] += 1

        memory["assets"][asset]["total_profit"] += profit

    save_memory(memory)
    return memory

