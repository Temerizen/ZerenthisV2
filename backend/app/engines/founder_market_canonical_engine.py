from datetime import datetime, timezone
from typing import Dict, Any

from backend.app.engines.market_data_engine import scan_market
from backend.app.engines.market_paper_engine import run_paper_trades
from backend.app.engines.market_portfolio_engine import load_portfolio, reset_portfolio
from backend.app.engines.market_score_engine import score_trades
from backend.app.engines.market_state_engine import load_market_state, save_market_state
from backend.app.engines.market_memory_engine import update_memory
from backend.app.engines.market_strategy_competition import run_strategies
from backend.app.engines.market_strategy_leaderboard import update_strategy_board, load_strategy_board
from backend.app.engines.market_winner_signal_engine import build_signals_for_strategy
from backend.app.engines.market_genetics_engine import load_genetics, evolve_genetics
from backend.app.engines.trade_memory import save_trade, get_stats
from backend.app.engines.performance_engine import update_performance
from backend.app.engines.strategy_lock import should_lock

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _safe_best_strategy(strategy_results: Dict[str, Any], strategy_board: Dict[str, Any]) -> str:
    board = strategy_board.get("strategies", {}) or {}
    locked = []
    for name, row in board.items():
        if should_lock(row):
            locked.append((name, float(row.get("avg_profit", 0.0))))
    if locked:
        locked.sort(key=lambda x: x[1], reverse=True)
        return locked[0][0]
    return strategy_results.get("best_strategy", "conservative")

def run_strategy_cycle() -> Dict[str, Any]:
    data = scan_market()
    strategy_results = run_strategies(data)
    strategy_board = update_strategy_board(strategy_results.get("strategies", {}), strategy_results.get("best_strategy", "conservative"))
    genetics = evolve_genetics(strategy_board, load_genetics())

    state = load_market_state()
    state.update({
        "status": "strategy_cycle_complete",
        "strategy_results": strategy_results,
        "strategy_board": strategy_board,
        "genetics": genetics,
        "scan": data,
        "updated_at": _now_iso(),
    })
    save_market_state(state)

    return {
        "status": "strategy_cycle_complete",
        "scan": data,
        "results": strategy_results,
        "strategy_board": strategy_board,
        "genetics": genetics,
        "timestamp": state["updated_at"],
    }

def run_winner_cycle() -> Dict[str, Any]:
    data = scan_market()
    strategy_results = run_strategies(data)
    strategy_board = update_strategy_board(strategy_results.get("strategies", {}), strategy_results.get("best_strategy", "conservative"))
    genetics = evolve_genetics(strategy_board, load_genetics())
    best_strategy = _safe_best_strategy(strategy_results, strategy_board)

    signals = build_signals_for_strategy(best_strategy, data)
    trades = run_paper_trades(signals, data)
    for trade in trades:
        save_trade(trade)

    score = score_trades(trades)
    memory = update_memory(trades)
    portfolio = load_portfolio()
    performance = update_performance(float(portfolio.get("balance", 0.0)))

    state = load_market_state()
    state.update({
        "status": "winner_cycle_complete",
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
        "performance": performance,
        "stats": get_stats(),
        "updated_at": _now_iso(),
    })
    save_market_state(state)
    return state

def run_full_cycle() -> Dict[str, Any]:
    result = run_winner_cycle()
    result["status"] = "full_cycle_complete"
    save_market_state(result)
    return result

def reset_founder_portfolio(starting_balance: float = 50.0, risk_per_trade: float = 0.10) -> Dict[str, Any]:
    return reset_portfolio(starting_balance, risk_per_trade)
