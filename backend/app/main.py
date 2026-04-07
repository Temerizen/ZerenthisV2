from fastapi import FastAPI
from backend.app.routes.intelligence_priority import router as intelligence_priority_router
from backend.app.routes.product import router as product_router
from backend.app.routes.full_cycle import router as full_cycle_router
from backend.app.routes.revenue import router as revenue_router

app = FastAPI()

app.include_router(intelligence_priority_router)
app.include_router(product_router)
app.include_router(full_cycle_router)
app.include_router(revenue_router)

@app.get("/health")
def health():
    return {"status": "ok"}

