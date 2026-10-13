# -*- coding: utf-8 -*-
import os, cv2, json, numpy as np

base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
js_path = os.path.join(base_dir, "classified_data.js")

with open(js_path, "r", encoding="utf-8") as f:
    txt = f.read()
data = json.loads(txt.replace("const classifiedImages = ", "").rstrip(";"))

print(f"Total questions in classified_data.js: {len(data)}")
missing = 0
tiny = 0
shapes = []
for q in data:
    fpath = os.path.join(base_dir, q["url"])
    if not os.path.exists(fpath):
        print(f"MISSING: {fpath}")
        missing += 1
    else:
        img = cv2.imdecode(np.fromfile(fpath, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None or img.shape[0] < 50 or img.shape[1] < 200:
            print(f"TINY/CORRUPT: {q['url']}")
            tiny += 1
        else:
            shapes.append(img.shape)

print(f"Audit Result: Missing={missing}, Tiny={tiny}, Valid images={len(shapes)}")
print(f"Min H={min(s[0] for s in shapes)}, Max H={max(s[0] for s in shapes)}, Mean H={sum(s[0] for s in shapes)/len(shapes):.1f}")
