from datetime import datetime, timezone
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from backend.app.engines.market_access_engine import is_founder
from backend.app.engines.market_data_engine import scan_market
from backend.app.engines.market_memory_engine import update_memory
from backend.app.engines.market_paper_engine import run_paper_trades
from backend.app.engines.market_portfolio_engine import load_portfolio, reset_portfolio
from backend.app.engines.market_score_engine import score_trades
from backend.app.engines.market_state_engine import load_market_state, save_market_state
from backend.app.engines.market_strategy_competition import run_strategies
from backend.app.engines.market_strategy_leaderboard import update_strategy_board, load_strategy_board
from backend.app.engines.market_winner_signal_engine import build_signals_for_strategy
from backend.app.engines.market_genetics_engine import load_genetics, evolve_genetics

router = APIRouter()

class PortfolioResetRequest(BaseModel):
    starting_balance: float = 50.0
    risk_per_trade: float = 0.10

def _now_iso():
    return datetime.now(timezone.utc).isoformat()

@router.post("/founder/market/reset-portfolio")
def founder_market_reset_portfolio(payload: PortfolioResetRequest, x_api_key: str = Header(None)):
    if not is_founder(x_api_key):
        raise HTTPException(status_code=401, detail="unauthorized")
    try:
        return reset_portfolio(payload.starting_balance, payload.risk_per_trade)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"reset_portfolio_failed: {e}")

@router.post("/founder/market/strategy-run")
def founder_market_strategy_run(x_api_key: str = Header(None)):
    if not is_founder(x_api_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    data = scan_market()
    results = run_strategies(data)
    board = update_strategy_board(results["strategies"], results["best_strategy"])
    genetics = evolve_genetics(board, load_genetics())

    return {
        "status": "strategy_cycle_complete",
        "scan": data,
        "results": results,
        "strategy_board": board,
        "genetics": genetics,
        "timestamp": _now_iso()
    }

@router.post("/founder/market/run")
def founder_market_run(x_api_key: str = Header(None)):
    if not is_founder(x_api_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    try:
        data = scan_market()

        strategy_results = run_strategies(data)
        best_strategy = strategy_results["best_strategy"]
        strategy_board = update_strategy_board(strategy_results["strategies"], best_strategy)
        genetics = evolve_genetics(strategy_board, load_genetics())

        signals = build_signals_for_strategy(best_strategy, data)
        trades = run_paper_trades(signals, data)
        score = score_trades(trades)
        memory = update_memory(trades)
        portfolio = load_portfolio()

        state = {
            "status": "full_cycle_complete",
            "best_strategy": best_strategy,
            "strategy_results": strategy_results,
            "strategy_board": strategy_board,
            "genetics": genetics,
            "scan": data,
            "signals": signals,
            "trades": trades,
            "score": score,
            "memory": memory,
            "portfolio": portfolio,
            "updated_at": _now_iso(),
        }

        save_market_state(state)
        return state

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"founder_market_run_failed: {e}")

@router.get("/market/portfolio")
def market_portfolio():
    return load_portfolio()

@router.get("/market/performance")
def market_performance():
    state = load_market_state()
    return {
        "score": state.get("score", {}),
        "portfolio": load_portfolio(),
        "best_strategy": state.get("best_strategy"),
        "updated_at": state.get("updated_at")
    }

@router.get("/market/strategy-board")
def market_strategy_board():
    return load_strategy_board()

@router.get("/market/latest")
def market_latest():
    return load_market_state()

@router.get("/market/genetics")
def market_genetics():
    return load_genetics()

@router.post("/market/scan")
def market_scan():
    state = load_market_state()
    data = scan_market()
    state["status"] = "scanned"
    state["scan"] = data
    state["updated_at"] = _now_iso()
    save_market_state(state)
    return {"data": data}

@router.post("/market/signal-run")
def market_signal_run():
    state = load_market_state()
    data = state.get("scan", [])
    if not data:
        data = scan_market()
        state["scan"] = data

    strategy_results = run_strategies(data)
    best_strategy = strategy_results["best_strategy"]
    signals = build_signals_for_strategy(best_strategy, data)

    state["status"] = "signaled"
    state["best_strategy"] = best_strategy
    state["signals"] = signals
    state["updated_at"] = _now_iso()
    save_market_state(state)
    return {
        "best_strategy": best_strategy,
        "signals": signals
    }

@router.post("/market/paper-run")
def market_paper_run():
    state = load_market_state()
    data = state.get("scan", [])
    if not data:
        data = scan_market()
        state["scan"] = data

    strategy_results = run_strategies(data)
    best_strategy = strategy_results["best_strategy"]
    strategy_board = update_strategy_board(strategy_results["strategies"], best_strategy)
    genetics = evolve_genetics(strategy_board, load_genetics())
    signals = build_signals_for_strategy(best_strategy, data)

    trades = run_paper_trades(signals, data)
    score = score_trades(trades)
    memory = update_memory(trades)
    portfolio = load_portfolio()

    state["status"] = "paper_complete"
    state["best_strategy"] = best_strategy
    state["strategy_results"] = strategy_results
    state["strategy_board"] = strategy_board
    state["genetics"] = genetics
    state["signals"] = signals
    state["trades"] = trades
    state["score"] = score
    state["memory"] = memory
    state["portfolio"] = portfolio
    state["updated_at"] = _now_iso()
    save_market_state(state)

    return {
        "best_strategy": best_strategy,
        "trades": trades,
        "score": score,
        "memory": memory,
        "genetics": genetics,
        "portfolio": portfolio
    }
