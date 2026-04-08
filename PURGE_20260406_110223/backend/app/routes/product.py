from __future__ import annotations

import json
from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.core.control_core import OUTPUT_DIR, append_history, resolve_topic, slugify, read_control_state, write_control_state
from backend.app.engines.product_engine import generate_product

router = APIRouter(prefix="/api/product", tags=["product"])

class ProductRequest(BaseModel):
    topic: str | None = None

@router.post("/generate")
def product_generate(payload: ProductRequest):
    topic = resolve_topic(payload.topic)
    product = generate_product(topic)

    filename = f"{slugify(product['title'])}_product.json"
    path = OUTPUT_DIR / filename
    path.write_text(json.dumps(product, indent=2, ensure_ascii=False), encoding="utf-8")

    state = read_control_state()
    state["active_topic"] = topic
    state["last_product_file"] = str(path)
    write_control_state(state)
    append_history({"event": "product_generated", "topic": topic, "file": str(path)})

    return {
        "status": "product_generated",
        "topic": topic,
        "file": str(path),
        "product": product
    }

