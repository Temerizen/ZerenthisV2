import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path("backend/data/market")
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"

DEFAULT_PORTFOLIO = {
    "starting_balance": 50.0,
    "balance": 50.0,
    "risk_per_trade": 0.10,
    "max_open_positions": 3,
    "last_run_trades": [],
    "equity_curve": [50.0]
}

def _safe_float(value, default):
    try:
        return round(float(value), 4)
    except Exception:
        return default

def load_portfolio() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if PORTFOLIO_FILE.exists():
        try:
            raw = json.loads(PORTFOLIO_FILE.read_text(encoding="utf-8"))
            return {
                "starting_balance": _safe_float(raw.get("starting_balance", 50.0), 50.0),
                "balance": _safe_float(raw.get("balance", 50.0), 50.0),
                "risk_per_trade": _safe_float(raw.get("risk_per_trade", 0.10), 0.10),
                "max_open_positions": int(raw.get("max_open_positions", 3) or 3),
                "last_run_trades": raw.get("last_run_trades", []) or [],
                "equity_curve": raw.get("equity_curve", [50.0]) or [50.0],
            }
        except Exception:
            return DEFAULT_PORTFOLIO.copy()
    return DEFAULT_PORTFOLIO.copy()

def save_portfolio(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    clean = {
        "starting_balance": _safe_float(portfolio.get("starting_balance", 50.0), 50.0),
        "balance": _safe_float(portfolio.get("balance", 50.0), 50.0),
        "risk_per_trade": _safe_float(portfolio.get("risk_per_trade", 0.10), 0.10),
        "max_open_positions": int(portfolio.get("max_open_positions", 3) or 3),
        "last_run_trades": portfolio.get("last_run_trades", []) or [],
        "equity_curve": portfolio.get("equity_curve", [50.0]) or [50.0],
    }
    PORTFOLIO_FILE.write_text(json.dumps(clean, indent=2), encoding="utf-8")
    return clean

def reset_portfolio(starting_balance: float = 50.0, risk_per_trade: float = 0.10) -> Dict[str, Any]:
    starting_balance = round(max(1.0, float(starting_balance)), 2)
    risk_per_trade = round(min(max(float(risk_per_trade), 0.001), 1.0), 4)

    portfolio = {
        "starting_balance": starting_balance,
        "balance": starting_balance,
        "risk_per_trade": risk_per_trade,
        "max_open_positions": 3,
        "last_run_trades": [],
        "equity_curve": [starting_balance]
    }
    return save_portfolio(portfolio)
