from datetime import datetime, timezone
from fastapi import APIRouter, Header, HTTPException

from backend.app.engines.market_access_engine import is_founder
from backend.app.engines.market_data_engine import scan_market
from backend.app.engines.market_strategy_competition import run_strategies

router = APIRouter()

def _now():
    return datetime.now(timezone.utc).isoformat()

@router.post("/founder/market/strategy-run")
def strategy_run(x_api_key: str = Header(None)):
    if not is_founder(x_api_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    data = scan_market()
    results = run_strategies(data)

    return {
        "status": "strategy_cycle_complete",
        "scan": data,
        "results": results,
        "timestamp": _now()
    }
