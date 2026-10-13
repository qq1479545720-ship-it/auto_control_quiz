# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

elem_ids = re.findall(r"document\.getElementById\(['\"](.*?)['\"]\)", html)
print('Referenced element IDs in JS:', set(elem_ids))

html_ids = set(re.findall(r'id=["\'](.*?)["\']', html))
missing_ids = [eid for eid in set(elem_ids) if eid not in html_ids]
print('Missing DOM IDs referenced in JS:', missing_ids)

# Check query selectors
qs = re.findall(r"querySelectorAll\(['\"](.*?)['\"]\)", html)
print('Query selector targets:', set(qs))

# Check functions called in onclick
onclicks = re.findall(r'onclick=["\'](.*?)["\']', html)
print('Onclick calls count:', len(onclicks))
for oc in onclicks:
    print('  onclick:', oc)
