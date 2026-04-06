import json
import os

MEMORY_FILE = "backend/data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"seen": []}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "seen" not in data or not isinstance(data["seen"], list):
            return {"seen": []}
        return data
    except:
        return {"seen": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def normalize_topic(topic: str):
    return " ".join(str(topic).lower().split())

def is_duplicate(topic: str):
    memory = load_memory()
    return normalize_topic(topic) in memory["seen"]

def remember(topic: str):
    memory = load_memory()
    norm = normalize_topic(topic)
    if norm not in memory["seen"]:
        memory["seen"].append(norm)
        save_memory(memory)

