from typing import List, Dict
from copy import deepcopy
from backend.app.engines.market_portfolio_engine import load_portfolio, save_portfolio
from backend.app.engines.market_adaptation_engine import update_stats
from backend.app.engines.market_risk_engine import apply_risk_controls, simulate_stop_loss

def run_paper_trades(signals: List[Dict], market_data: List[Dict], persist: bool = True):
    portfolio = deepcopy(load_portfolio())
    balance = float(portfolio.get("balance", 50.0))
    risk_per_trade = float(portfolio.get("risk_per_trade", 0.10))

    price_map = {item.get("asset"): item for item in market_data}
    trades = []

    tradable = [s for s in signals if s.get("action") in ("BUY", "SELL")]
    tradable = tradable[: int(portfolio.get("max_open_positions", 3))]

    for signal in tradable:
        asset = signal.get("asset")
        action = signal.get("action")
        confidence = apply_risk_controls(signal, portfolio)

        market_item = price_map.get(asset, {})
        price = float(market_item.get("price", 0))
        change = float(market_item.get("change", 0))

        position_size = round(balance * risk_per_trade * (confidence / 10), 2)
        if position_size <= 0:
            continue

        edge = abs(change) / 100.0

        if action == "BUY":
            pnl = position_size * edge if change > 0 else -position_size * edge
        else:
            pnl = position_size * edge if change < 0 else -position_size * edge

        stop_loss = simulate_stop_loss(position_size, change, action)
        if stop_loss is not None:
            pnl = round(stop_loss, 2)

        pnl = round(pnl, 2)
        balance = round(balance + pnl, 2)

        trades.append({
            "asset": asset,
            "action": action,
            "price": price,
            "change": change,
            "confidence": confidence,
            "position_size": position_size,
            "profit": pnl,
            "account_balance": balance,
            "timestamp": int(market_item.get("timestamp", 0))
        })

    if persist:
        stats = update_stats(trades)
        portfolio["balance"] = balance
        portfolio["last_run_trades"] = trades
        portfolio["stats"] = stats
        eq = portfolio.get("equity_curve", [])
        eq.append(balance)
        portfolio["equity_curve"] = eq[-50:]
        save_portfolio(portfolio)

    return trades
