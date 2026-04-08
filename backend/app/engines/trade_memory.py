import json, os, time

BASE = os.path.join(os.getcwd(), "backend", "data")
HISTORY_FILE = os.path.join(BASE, "trades_history.json")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    return json.load(open(HISTORY_FILE, "r", encoding="utf-8-sig"))

def save_trade(trade):
    history = load_history()
    trade["logged_at"] = int(time.time())
    history.append(trade)
    json.dump(history, open(HISTORY_FILE, "w", encoding="utf-8-sig"), indent=2)

def get_stats():
    history = load_history()
    if not history:
        return {"trades":0}

    total = sum(t.get("profit",0) for t in history)
    wins = sum(1 for t in history if t.get("profit",0) > 0)
    losses = sum(1 for t in history if t.get("profit",0) <= 0)

    return {
        "trades": len(history),
        "total_profit": round(total, 4),
        "wins": wins,
        "losses": losses,
        "winrate": round((wins/max(1,len(history)))*100,2)
    }

