import json
import random
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path("backend/data/market")
GENETICS_FILE = DATA_DIR / "strategy_genetics.json"

DEFAULT_GENETICS = {
    "momentum": {"threshold": 2.0, "confidence_mult": 1.5, "max_conf": 10.0},
    "mean_reversion": {"threshold": 3.0, "confidence_mult": 1.2, "max_conf": 10.0},
    "breakout": {"threshold": 5.0, "confidence_mult": 2.0, "max_conf": 10.0},
    "conservative": {"threshold": 4.0, "confidence_mult": 1.0, "max_conf": 6.0}
}

def _clamp(v, lo, hi):
    return max(lo, min(hi, v))

def load_genetics() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if GENETICS_FILE.exists():
        try:
            return json.loads(GENETICS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_GENETICS.copy()
    return DEFAULT_GENETICS.copy()

def save_genetics(genetics: Dict[str, Any]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    GENETICS_FILE.write_text(json.dumps(genetics, indent=2), encoding="utf-8")

def mutate_value(v: float, strength: float = 0.15, lo: float = 0.25, hi: float = 15.0) -> float:
    delta = random.uniform(-strength, strength) * max(abs(v), 1.0)
    return round(_clamp(v + delta, lo, hi), 4)

def evolve_genetics(strategy_board: Dict[str, Any], genetics: Dict[str, Any]):
    strategies = strategy_board.get("strategies", {}) or {}
    if not strategies:
        return genetics

    ranked = sorted(
        strategies.items(),
        key=lambda x: (
            float(x[1].get("avg_profit", 0)),
            float(x[1].get("avg_winrate", 0))
        ),
        reverse=True
    )

    best_name = ranked[0][0]
    worst_name = ranked[-1][0]

    best_gene = genetics.get(best_name, {}).copy()
    if not best_gene:
        return genetics

    # Worst strategy gets pulled toward winner, then mutated
    new_worst = {
        "threshold": mutate_value(float(best_gene.get("threshold", 2.0)), 0.20, 0.5, 8.0),
        "confidence_mult": mutate_value(float(best_gene.get("confidence_mult", 1.5)), 0.20, 0.5, 3.0),
        "max_conf": mutate_value(float(best_gene.get("max_conf", 10.0)), 0.10, 3.0, 10.0),
    }
    genetics[worst_name] = new_worst

    # Small drift on non-winners to keep exploration alive
    for name, gene in list(genetics.items()):
        if name == best_name:
            continue
        genetics[name] = {
            "threshold": mutate_value(float(gene.get("threshold", 2.0)), 0.05, 0.5, 8.0),
            "confidence_mult": mutate_value(float(gene.get("confidence_mult", 1.5)), 0.05, 0.5, 3.0),
            "max_conf": mutate_value(float(gene.get("max_conf", 10.0)), 0.03, 3.0, 10.0),
        }

    save_genetics(genetics)
    return genetics
