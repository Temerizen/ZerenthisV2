from __future__ import annotations

from typing import Dict, List

def _title_from_topic(topic: str) -> str:
    topic = (topic or "").strip()
    words = [w for w in topic.replace("_", " ").split() if w]
    headline = " ".join(w.capitalize() for w in words[:8]).strip()
    if not headline:
        headline = "Premium Digital System"
    return headline

def generate_product(topic: str) -> Dict[str, object]:
    topic = (topic or "").strip()
    title = _title_from_topic(topic)
    description = (
        f"{title} is a premium digital system built around the idea of {topic}. "
        f"It gives the buyer a clearer path, faster execution, and a practical framework "
        f"they can apply immediately without drowning in complexity."
    )

    steps: List[str] = [
        f"Clarify the goal and remove friction around {topic}",
        "Install a repeatable daily execution loop",
        "Use templates and decision rules to reduce overthinking",
        "Track momentum weekly and refine what actually works",
    ]

    value_bullets: List[str] = [
        "Turns a vague problem into a structured action plan",
        "Saves time by reducing trial-and-error and scattered effort",
        "Creates a reusable framework instead of one-off advice",
        "Easy to package as a PDF, mini-course, or creator product",
    ]

    bonus = (
        "Bonus: plug-and-play templates, quick-start checklist, and a momentum tracker "
        "to help the buyer implement the system fast."
    )

    full_content = f"""# {title}

## Core Promise
Master {topic} with a cleaner, simpler system that is designed for real execution.

## What This Product Helps With
This product helps the buyer move from confusion to focused action. It removes clutter,
builds clarity, and gives them a repeatable process they can use right away.

## System Steps
1. {steps[0]}
2. {steps[1]}
3. {steps[2]}
4. {steps[3]}

## Value
- {value_bullets[0]}
- {value_bullets[1]}
- {value_bullets[2]}
- {value_bullets[3]}

## Bonus
{bonus}

## Suggested Positioning
Sell this as a premium starter system, practical blueprint, or implementation pack.

## Delivery Formats
- PDF guide
- checklist
- swipe file
- creator toolkit
"""

    return {
        "topic": topic,
        "title": title,
        "description": description,
        "steps": steps,
        "value_bullets": value_bullets,
        "bonus": bonus,
        "full_content": full_content,
    }