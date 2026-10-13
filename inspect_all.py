import json
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with open('classified_data.js', encoding='utf-8') as f:
    data = json.loads(f.read().replace('const classifiedImages = ', '').rstrip(';'))

print(f"Total questions: {len(data)}")

# Group by year and show types
years = {}
for q in data:
    years.setdefault(q['year'], []).append(q)

for y, qlist in sorted(years.items()):
    print(f"\n=== {y} ({len(qlist)} questions) ===")
    for q in qlist:
        print(f"  {q['q_num']}: [{q['type']}] (file: {q['url']})")
