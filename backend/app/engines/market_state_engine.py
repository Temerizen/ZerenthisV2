import json
from pathlib import Path
from typing import Any, Dict

DATA_DIR = Path("backend/data/market")
STATE_FILE = DATA_DIR / "latest_run.json"

DEFAULT_STATE: Dict[str, Any] = {
    "status": "idle",
    "scan": [],
    "signals": [],
    "trades": [],
    "score": {},
    "updated_at": None,
}

def load_market_state() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8-sig"))
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_market_state(state: Dict[str, Any]) -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8-sig")
    return state

