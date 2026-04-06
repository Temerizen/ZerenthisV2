from __future__ import annotations

from typing import Dict, List

def generate_traffic(topic: str, product_title: str) -> Dict[str, object]:
    topic = (topic or "").strip()
    product_title = (product_title or "Premium Digital System").strip()

    hooks: List[str] = [
        f"If {topic} feels impossible right now, this fixes the chaos.",
        f"Most people fail at {topic} because they never install a system.",
        f"This {topic} framework is built for execution, not motivation.",
    ]

    tiktok_scripts: List[str] = [
        f"Hook: Stop trying to brute-force {topic}. Here's the system.\nBody: Most people stay stuck because they use random advice. {product_title} gives you a repeatable path.\nCTA: Comment SYSTEM if you want the blueprint.",
        f"Hook: This is how to make {topic} finally feel organized.\nBody: Clear goal, simple loop, fewer decisions, more momentum.\nCTA: Grab {product_title} and start today.",
        f"Hook: You're not lazy. Your {topic} process is broken.\nBody: A clean framework beats motivation every time.\nCTA: DM me RESET for the guide.",
    ]

    twitter_threads: List[str] = [
        f"Thread: Why most people fail at {topic} and how a system fixes it.\n\n1. They chase motivation.\n2. They use random advice.\n3. They never install repeatable steps.\n\n{product_title} solves that with a cleaner framework.",
        f"Want to improve {topic} without drowning in complexity?\n\nHere is the simple play:\n1. Define the goal\n2. Remove friction\n3. Use a daily loop\n4. Review weekly\n\nThat's the structure behind {product_title}.",
    ]

    captions: List[str] = [
        f"A cleaner way to win at {topic}.",
        f"Less chaos. More execution. {product_title}",
        f"Built for momentum, not burnout.",
    ]

    return {
        "topic": topic,
        "product_title": product_title,
        "hooks": hooks,
        "tiktok_scripts": tiktok_scripts,
        "twitter_threads": twitter_threads,
        "captions": captions,
    }