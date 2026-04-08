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

def load_portfolio() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if PORTFOLIO_FILE.exists():
        try:
            return json.loads(PORTFOLIO_FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_PORTFOLIO.copy()
    return DEFAULT_PORTFOLIO.copy()

def save_portfolio(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_FILE.write_text(json.dumps(portfolio, indent=2), encoding="utf-8")
    return portfolio

def reset_portfolio(starting_balance: float = 50.0, risk_per_trade: float = 0.10) -> Dict[str, Any]:
    portfolio = {
        "starting_balance": round(float(starting_balance), 2),
        "balance": round(float(starting_balance), 2),
        "risk_per_trade": round(float(risk_per_trade), 4),
        "max_open_positions": 3,
        "last_run_trades": [],
        "equity_curve": [round(float(starting_balance), 2)]
    }
    return save_portfolio(portfolio)
