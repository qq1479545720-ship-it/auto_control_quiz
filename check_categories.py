# -*- coding: utf-8 -*-
import json, os, sys
from collections import Counter

base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"

with open(os.path.join(base_dir, "classified_data.js"), "r", encoding="utf-8") as f:
    c = f.read()
    c = c[c.find('['):c.rfind(']')+1]
    data = json.loads(c)

print(f"Total questions in current JS: {len(data)}")

# Count by category
types = Counter(q['type'] for q in data)
for t, cnt in types.items():
    print(f"  {t}: {cnt}")
