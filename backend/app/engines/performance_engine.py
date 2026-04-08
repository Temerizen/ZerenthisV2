import json
import os

SCORE_FILE = "backend/data/scores.json"

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return {}
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except:
        return {}

def save_scores(scores):
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

def record_result(topic: str, score: float):
    scores = load_scores()
    if topic not in scores or not isinstance(scores[topic], list):
        scores[topic] = []
    scores[topic].append(float(score))
    save_scores(scores)
    return scores

def leaderboard():
    scores = load_scores()
    ranked = []

    for topic, values in scores.items():
        if not isinstance(values, list) or not values:
            continue
        avg = round(sum(values) / len(values), 2)
        ranked.append({
            "topic": topic,
            "runs": len(values),
            "avg_score": avg,
            "best_score": max(values)
        })

    ranked.sort(key=lambda x: x["avg_score"], reverse=True)
    return ranked

