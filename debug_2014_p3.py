import pymupdf as fitz
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638977592_743cdcf4.pdf'))
p3 = doc[3]
print("=== 2014 Page 3 blocks ===")
for b in p3.get_text('blocks'):
    print(f"y0={b[1]:.1f}..{b[3]:.1f}: {repr(b[4].strip()[:40])}")
