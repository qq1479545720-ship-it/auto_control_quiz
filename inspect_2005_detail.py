# -*- coding: utf-8 -*-
import fitz, os, re, cv2
import numpy as np

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2005']))
print(f"2005 has {len(doc)} pages")

for pno in range(len(doc)):
    page = doc[pno]
    txt = page.get_text('text')
    print(f"\n--- Page {pno} (size: {page.rect.width} x {page.rect.height}) text len={len(txt)} ---")
    blks = page.get_text('blocks')
    for b in blks:
        if b[4].strip():
            print(f"  y={b[1]:.1f}-{b[3]:.1f}: {b[4][:50]!r}")
