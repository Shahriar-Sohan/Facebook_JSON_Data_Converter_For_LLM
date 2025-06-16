import json
import glob

import os
from datetime import datetime

your_name = "Shahriar Sohan"
friend_name = None

os.makedirs("processed_llm_data", exist_ok=True)

for filepath in glob.glob("raw_data/**/*.json", recursive=True):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        participants = [p["name"] for p in data.get("participants", [])]
        friend_candidates = [name for name in participants if name != your_name]
        if not friend_candidates:
            print(f"⚠️ No other participants found in {filepath}")
            continue

        messages = data["messages"][::-1]  # Oldest to newest
        dataset = []
        context = []

        for msg in messages:
            if "content" not in msg:
                continue

            sender = msg["sender_name"]
            content = msg["content"].strip()

            if sender != your_name:
                message_pair = f"{sender}: {content}"
                if not context or context[-1] != message_pair:
                    context.append(message_pair)
            elif context:
                dataset.append({
                    "instruction": "\n".join(context),
                    "input": "",
                    "output": content
                })
                context = []

        if not dataset:
            print(f"⚠️ No usable message pairs found in {filepath}")
            continue

        filename = os.path.join(
            "processed_llm_data",
            f"train_{os.path.basename(filepath).replace('.json', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(dataset)} cleaned chat pairs to {filename}.")
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")