import random
import json
import os

SCORE_FILE = "backend/data/scores.json"

def leaderboard():
    if not os.path.exists(SCORE_FILE):
        return []
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            scores = json.load(f)
    except:
        return []

    if not isinstance(scores, dict):
        return []

    ranked = []
    for topic, values in scores.items():
        if not isinstance(values, list) or not values:
            continue
        clean_values = [float(v) for v in values]
        avg = round(sum(clean_values) / len(clean_values), 2)
        ranked.append({
            "topic": topic,
            "runs": len(clean_values),
            "avg_score": avg,
            "best_score": max(clean_values)
        })

    ranked.sort(key=lambda x: x["avg_score"], reverse=True)
    return ranked

def generate_topic():
    ranked = leaderboard()

    base = [
        "AI productivity system",
        "faceless content engine",
        "automated money system",
        "self-improving workflow",
        "digital product generator"
    ]

    if ranked and random.random() < 0.55:
        pool = ranked[:3] if len(ranked) >= 3 else ranked
        return random.choice(pool)["topic"]

    return random.choice(base)

def simulate(topic: str):
    score = round(random.uniform(6.5, 9.5), 2)
    return {
        "topic": topic,
        "score": score,
        "verdict": "keep" if score > 7.5 else "discard"
    }

