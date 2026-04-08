from fastapi import APIRouter
from backend.app.engines.intelligence_engine import generate_topic, simulate
from backend.app.engines.memory_engine import is_duplicate, remember
from backend.app.engines.evolution_engine import evolve_topic

router = APIRouter()

@router.post("/intelligence/run")
def run_intelligence():
    topic = generate_topic()

    if is_duplicate(topic):
        topic = evolve_topic(topic)

    result = simulate(topic)
    remember(topic)
    return result

