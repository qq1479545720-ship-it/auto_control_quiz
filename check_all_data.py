# -*- coding: utf-8 -*-
import json, re

with open('classified_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'const classifiedImages = '
idx = text.find(prefix)
if idx != -1:
    raw_json = text[idx + len(prefix):].rstrip(';\n ')
    data = json.loads(raw_json)
    print(f"Total items in classified_data.js: {len(data)}")
    for yr in [2007, 2008, 2009, 2010, 2011]:
        items = [d for d in data if d.get('year_num') == yr]
        print(f"Year {yr}: {len(items)} items")
        for it in sorted(items, key=lambda x: x.get('q_num', '')):
            print(f"  {it.get('q_num')}: type={it.get('type')}, url={it.get('url')}")
