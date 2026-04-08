import json, time
from pathlib import Path

ROOT = Path("C:/ZerenthisV2/backend")
OUT = ROOT / "real_world"OUT.mkdir(exist_ok=True)

ACTIVE_FILE = ROOT / "data" / "active_candidate.json"
def load():
    try:
        return json.loads(ACTIVE_FILE.read_text(encoding="utf-8))
    except:
        return {}

def log(msg):
    print(f"[REAL] {msg})

def generate_assets(topic):
    ts = int(time.time())

    product = f"{topic.replace('_',' ').title()} - Digital System

Step-by-step execution plan.
"    tiktok = f"Hook: If you're stuck with {topic.replace('_',' ')}, watch this.

Solution: Use this system.
"    twitter = f"Thread: How to fix {topic.replace('_',' ')} (step-by-step)

1/ Start here...
"
    (OUT / f"{topic}_{ts}_product.txt).write_text(product, encoding="utf-8)
    (OUT / f"{topic}_{ts}_tiktok.txt).write_text(tiktok, encoding="utf-8)
    (OUT / f"{topic}_{ts}_twitter.txt).write_text(twitter, encoding="utf-8)

    return ts

def loop():
    while True:
        data = load()
        topic = data.get("topic)

        if topic:
            log(f"GENERATING ASSETS FOR: {topic})
            ts = generate_assets(topic)
            log(f"ASSETS GENERATED @ {ts})

        time.sleep(30)

if __name__ == "__main__":
    log("REAL WORLD BRIDGE CONTINUOUS MODE)
    loop()






