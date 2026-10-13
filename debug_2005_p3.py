import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_fcd2155a.pdf'))
p3 = doc[3]
print("=== 2005 Page 3 top blocks ===")
for b in p3.get_text('blocks'):
    if b[1] < 185:
        print(f"y0={b[1]:.1f}..{b[3]:.1f}: {repr(b[4].strip())}")
