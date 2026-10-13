# -*- coding: utf-8 -*-
import fitz, os, re, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

print("=== Checking 2013-2024 (except 2022) ===")
cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')

for yr in ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
    heads_by_page = {}
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        blks = page.get_text('dict')['blocks']
        heads_by_page[pno] = []
        for b in blks:
            if 'lines' in b:
                for line in b['lines']:
                    txt = ''.join(s['text'] for s in line['spans']).strip()
                    x0 = line['bbox'][0]
                    y0 = line['bbox'][1]
                    y1 = line['bbox'][3]
                    if x0 < 120:
                        m = cn_pat.match(txt)
                        if m:
                            heads_by_page[pno].append((round(y0,1), round(y1,1), m.group(1), txt[:25]))
    
    print(f"\n--- {yr} ---")
    for pno, heads in heads_by_page.items():
        if heads:
            print(f"  Page {pno}: {[f'{h[2]}({h[0]}-{h[1]})' for h in heads]}")
