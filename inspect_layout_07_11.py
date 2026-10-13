# -*- coding: utf-8 -*-
import pymupdf as fitz
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
from generate_final_questions import pdf_map

for yr in ['2007', '2008', '2009', '2010', '2011']:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    print(f"\n==================== {yr} (Total pages: {len(doc)}) ====================")
    for pno in range(1, len(doc)):
        page = doc[pno]
        blks = page.get_text('blocks')
        print(f"--- Page {pno} (W={page.rect.width}, H={page.rect.height}) ---")
        for b in blks:
            # print blocks near left margin or significant blocks
            text = b[4].strip().replace('\n', ' ')
            if b[0] < 150 or '试卷' in text or '中国计量' in text or '共' in text:
                print(f"  [x={b[0]:.1f}, y={b[1]:.1f}-{b[3]:.1f}]: {text[:50]}")
