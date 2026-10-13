import fitz, os, re, json
import numpy as np

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"

with open(os.path.join(base_dir, "classified_data.js"), "r", encoding="utf-8") as f:
    c = f.read().replace("const classifiedImages = ", "").rstrip(";")
    data = json.loads(c)

print(f"Total questions in database: {len(data)}")

# Let's inspect each year's questions by checking headings in the questions
# Group by year
by_year = {}
for q in data:
    by_year.setdefault(q['year'], []).append(q)

for yr, qlist in sorted(by_year.items()):
    print(f"{yr}: {len(qlist)} questions -> {[q['q_num'] for q in qlist]}")
