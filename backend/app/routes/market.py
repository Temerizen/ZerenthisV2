from datetime import datetime, timezone
from fastapi import APIRouter, Header
from pydantic import BaseModel

from backend.app.engines.market_access_engine import is_founder
from backend.app.engines.strategy_engine import run_strategies
from backend.app.engines.market_data_engine import scan_market
from backend.app.engines.market_paper_engine import run_paper_trades
from backend.app.engines.market_portfolio_engine import load_portfolio, reset_portfolio
from backend.app.engines.market_score_engine import score_trades
from backend.app.engines.market_state_engine import load_market_state, save_market_state
from backend.app.engines.market_strategy_engine import generate_signals
from backend.app.engines.market_multi_strategy_engine import generate_multi_signals
from backend.app.engines.market_strategy_competition_engine import evaluate_strategies
from backend.app.engines.market_strategy_leaderboard import load_leaderboard, update_competition_results

router = APIRouter()

class PortfolioResetRequest(BaseModel):
    starting_balance: float = 50.0
    risk_per_trade: float = 0.10

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@router.get("/market/latest")
def market_latest():
    state = load_market_state()
    state["portfolio"] = load_portfolio()
    state["leaderboard"] = load_leaderboard()
    return state

@router.get("/market/leaderboard")
def market_leaderboard():
    return load_leaderboard()

@router.get("/market/portfolio")
def market_portfolio():
    return load_portfolio()

@router.post("/founder/market/reset-portfolio")
def founder_market_reset_portfolio(payload: PortfolioResetRequest, x_api_key: str = Header(None)):
    if not is_founder(x_api_key):
            strategy_output = run_strategies(data, LAST_RUN.get("portfolio", {"balance":1000}))
    LAST_RUN["strategy"] = strategy_output

    return {"error": "unauthorized"}
    return reset_portfolio(payload.starting_balance, payload.risk_per_trade)

@router.post("/founder/market/run")
def founder_market_run(x_api_key: str = Header(None)):
    if not is_founder(x_api_key):
            strategy_output = run_strategies(data, LAST_RUN.get("portfolio", {"balance":1000}))
    LAST_RUN["strategy"] = strategy_output

    return {"error": "unauthorized"}

    data = scan_market()
    multi = generate_multi_signals(data)

    competition = evaluate_strategies(multi, data)
    best_strategy = competition["best_strategy"]
    results = competition["results"]

    winning_raw_signals = results[best_strategy]["signals"]
    adapted_signals = generate_signals(data)
    adapted_map = {s["asset"]: s for s in adapted_signals}

    selected_signals = []
    for s in winning_raw_signals:
        asset = s["asset"]
        merged = {
            **s,
            "confidence": adapted_map.get(asset, {}).get("confidence", abs(float(s.get("change", 0)))),
            "bias": adapted_map.get(asset, {}).get("bias", 1.0),
        }
        selected_signals.append(merged)

    trades = run_paper_trades(selected_signals, data, persist=True)
    score = score_trades(trades)
    portfolio = load_portfolio()
    leaderboard = update_competition_results(results, best_strategy)

    state = {
        "status": "full_cycle_complete",
        "active_strategy": best_strategy,
        "scan": data,
        "multi_signals": multi,
        "competition_results": results,
        "signals": selected_signals,
        "trades": trades,
        "score": score,
        "portfolio": portfolio,
        "leaderboard": leaderboard,
        "updated_at": _now_iso(),
    }
    save_market_state(state)
    return state

