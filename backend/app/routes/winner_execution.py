from fastapi import APIRouter, Header, HTTPException
from backend.app.engines.market_access_engine import is_founder
from backend.app.engines.market_winner_execution_engine import run_winner_cycle

router = APIRouter()

@router.post("/founder/market/winner-run")
def winner_run(x_api_key: str = Header(None)):
    if not is_founder(x_api_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    return run_winner_cycle()
