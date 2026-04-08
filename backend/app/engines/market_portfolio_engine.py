from pathlib import Path
from typing import Dict, Any
from backend.app.engines.state_guard import safe_load_json, safe_save_json, normalize_portfolio

DATA_DIR = Path("backend/data/market")
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"

def load_portfolio() -> Dict[str, Any]:
    return normalize_portfolio(safe_load_json(PORTFOLIO_FILE, {}))

def save_portfolio(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    clean = normalize_portfolio(portfolio)
    return safe_save_json(PORTFOLIO_FILE, clean)

def reset_portfolio(starting_balance: float = 50.0, risk_per_trade: float = 0.10) -> Dict[str, Any]:
    portfolio = normalize_portfolio({
        "starting_balance": starting_balance,
        "balance": starting_balance,
        "risk_per_trade": risk_per_trade,
        "max_open_positions": 3,
        "last_run_trades": [],
        "equity_curve": [starting_balance],
        "peak_balance": starting_balance
    })
    return save_portfolio(portfolio)
