import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_9aa4c2f4.pdf'))

for pno in range(1, 5):
    p = doc[pno]
    blks = p.get_text('blocks')
    print(f"2006 Page {pno} (total blocks {len(blks)}):")
    for b in blks[:8]:
        t = b[4].strip().replace('\n', ' ')
        print(f"   x0={b[0]:.1f}, y0={b[1]:.1f}..{b[3]:.1f}: {repr(t[:40])}")
