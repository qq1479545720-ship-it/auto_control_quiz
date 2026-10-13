# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

scale = 150.0 / 72.0

for yr in ['2007', '2008', '2009', '2010', '2011']:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    print(f"\n=== {yr} ({len(doc)} pages) ===")
    for pno in range(1, len(doc)):
        page = doc[pno]
        blks = page.get_text('blocks')
        left_blks = [b for b in blks if b[0] < 120 and b[1] > 30 and (b[3]-b[1]) < 50]
        left_blks.sort(key=lambda b: b[1])
        print(f"  Page {pno} (H={page.rect.height:.1f}):")
        for b in left_blks:
            print(f"    y={b[1]:.1f}-{b[3]:.1f}: {b[4].strip()[:30]!r}")
