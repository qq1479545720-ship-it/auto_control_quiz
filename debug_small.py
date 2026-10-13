import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

# 1. 2005 Page 2
doc2005 = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_fcd2155a.pdf'))
p2 = doc2005[2]
print("=== 2005 Page 2 text ===")
for b in p2.get_text('blocks'):
    if b[1] > 650:
        print(f"y0={b[1]:.1f}..{b[3]:.1f}: {repr(b[4].strip())}")

# 2. 2009 Page 1
doc2009 = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_bc024558.pdf'))
p1 = doc2009[1]
print("=== 2009 Page 1 text ===")
for b in p1.get_text('blocks'):
    if b[1] > 550:
        print(f"y0={b[1]:.1f}..{b[3]:.1f}: {repr(b[4].strip())}")

# 3. 2011 Page 1 & 2
doc2011 = fitz.open(os.path.join(pdf_dir, 'media_1791638977592_044c77ac.pdf'))
for pno in [1, 2, 3]:
    p = doc2011[pno]
    print(f"=== 2011 Page {pno} blocks ===")
    for b in p.get_text('blocks'):
        if b[0] < 80:
            print(f"  y0={b[1]:.1f}..{b[3]:.1f} (x={b[0]:.1f}): {repr(b[4].strip()[:30])}")
