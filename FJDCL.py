import json
import glob

import os
from datetime import datetime

your_name = "Shahriar Sohan"
friend_name = "AdrIshA"

os.makedirs("processed_llm_data", exist_ok=True)

for filepath in glob.glob("raw_data/*.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = data["messages"][::-1]  # Oldest to newest

    dataset = []

    context = []
    last_sender = None

    for msg in messages:
        if "content" not in msg:
            continue

        sender = msg["sender_name"]
        content = msg["content"].strip()

        if sender != your_name:
            # Add new message only if it's not a duplicate of the last
            if not context or context[-1] != content:
                context.append(content)
            last_sender = sender
        elif context:
            # Save instruction-response pair
            dataset.append({
                "instruction": f"{friend_name} said:\n" + "\n".join(context),
                "input": "",
                "output": content
            })
            context = []

    filename = os.path.join(
        "processed_llm_data",
        f"train_{os.path.basename(filepath).replace('.json', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(dataset)} cleaned chat pairs to {filename}.")