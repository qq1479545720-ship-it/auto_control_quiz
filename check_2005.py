import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_fcd2155a.pdf'))

for pno in range(1, 5):
    p = doc[pno]
    print(f"\n--- 2005 Page {pno} ---")
    txt = p.get_text('text')
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    for l in lines:
        if any(l.startswith(k) for k in ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            print("  ", l[:50])
