import pymupdf as fitz
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_fba750cd.pdf'))
p1 = doc[1]
for b in p1.get_text('dict')['blocks']:
    if 'lines' in b:
        for l in b['lines']:
            txt = ''.join(s['text'] for s in l['spans']).strip()
            # print line if near left margin
            if l['bbox'][0] < 100:
                print(f"y0={l['bbox'][1]:.1f}, y1={l['bbox'][3]:.1f}, x0={l['bbox'][0]:.1f}: {repr(txt[:40])}")
