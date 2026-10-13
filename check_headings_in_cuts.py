# -*- coding: utf-8 -*-
import fitz, os, re, sys, glob
import cv2
import numpy as np

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')

def audit_year_headings(yr):
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
    
    # Collect all headings across all pages
    all_heads = [] # (pno, y0, y1, text)
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        blks = page.get_text('dict')['blocks']
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
                            all_heads.append((pno, y0, y1, m.group(1), txt[:20]))
    return all_heads

modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']
for yr in modern_years:
    h = audit_year_headings(yr)
    print(f"{yr}: {len(h)} headings -> {[x[3] for x in h]}")
