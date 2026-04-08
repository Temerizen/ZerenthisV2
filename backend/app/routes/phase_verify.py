from fastapi import APIRouter
from backend.app.engines.phase_verify import run

router = APIRouter()

@router.get("/api/phase/verify")
def phase_verify():
    return run()
