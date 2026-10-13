import pymupdf as fitz
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638997981_93c779ac.pdf')) # 2019
p3 = doc[3]

# check all blocks on p3
for b in p3.get_text('blocks'):
    txt = b[4].strip().replace('\n', ' ')
    print(f"y0={b[1]:.1f}, y1={b[3]:.1f}: {repr(txt[:40])}")
