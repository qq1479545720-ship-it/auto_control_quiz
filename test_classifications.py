# -*- coding: utf-8 -*-
import fitz, os, re, sys
from generate_final_questions import pdf_map, classify_text

cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')
modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']

scale = 150.0 / 72.0
pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

for yr in modern_years:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
    
    yr_q = 0
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        blks = page.get_text('dict')['blocks']
        heads_on_page = []
        for b in blks:
            if 'lines' in b:
                for line in b['lines']:
                    txt = ''.join(s['text'] for s in line['spans']).strip()
                    if line['bbox'][0] < 120:
                        m = cn_pat.match(txt)
                        if m:
                            heads_on_page.append((line['bbox'][1], m.group(1), txt))
        heads_on_page.sort(key=lambda x: x[0])
        for i, (yh, h_cn, h_txt) in enumerate(heads_on_page):
            yr_q += 1
            y_start = yh - 5.0
            if i < len(heads_on_page) - 1:
                y_end = heads_on_page[i+1][0] - 5.0
            else:
                y_end = page.rect.height - 35.0
            clip = fitz.Rect(0, y_start, page.rect.width, y_end)
            q_txt = page.get_text('text', clip=clip)
            cat = classify_text(q_txt)
            print(f"{yr} Q{yr_q} ({h_cn}): {cat} | {h_txt[:25]}")
