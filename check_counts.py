import json, re

with open("classified_data.js", "r", encoding="utf-8") as f:
    c = f.read()
# extract JSON
c = c.replace("const classifiedImages = ", "").rstrip(";")
data = json.loads(c)

by_year = {}
for q in data:
    yr = str(q['year_num'])
    by_year.setdefault(yr, []).append(q)

for yr in sorted(by_year.keys()):
    qs = by_year[yr]
    print(f"{yr}: {len(qs)} questions: {[q['q_num'] for q in qs]}")
