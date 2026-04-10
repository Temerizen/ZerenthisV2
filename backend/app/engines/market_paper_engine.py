from typing import List, Dict

def run_paper_trades(signals: List[Dict], portfolio: Dict) -> Dict:
    """
    Simple deterministic paper trading engine.
    No randomness. No external calls.
    """

    trades = []
    balance = portfolio.get("balance", 0)

    for signal in signals:
        asset = signal.get("asset")
        action = signal.get("action")
        price = signal.get("price", 0)

        if not asset or not action or price <= 0:
            continue

        trade = {
            "asset": asset,
            "action": action,
            "price": price,
            "size": round(balance * 0.1, 2)
        }

        trades.append(trade)

    return {
        "status": "paper_trades_executed",
        "trades": trades,
        "count": len(trades)
    }
