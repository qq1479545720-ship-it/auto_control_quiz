# -*- coding: utf-8 -*-
import fitz, os, re, cv2
import numpy as np

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2006']))
print(f"2006 has {len(doc)} pages")

cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')

for pno in range(1, len(doc)):
    page = doc[pno]
    print(f"\n--- Page {pno} (size: {page.rect.width} x {page.rect.height}) ---")
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
                        print(f"  Head {m.group(1)} at y={y0:.1f}-{y1:.1f}pt: {txt[:35]}")
