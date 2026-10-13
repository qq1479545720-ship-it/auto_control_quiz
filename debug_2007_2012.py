import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

# 2007 Page 3
doc2007 = fitz.open(os.path.join(pdf_dir, 'media_1791638971402_48e50a8b.pdf'))
p3 = doc2007[3]
print("=== 2007 Page 3 blocks ===")
for b in p3.get_text('blocks'):
    print(f"y0={b[1]:.1f}..{b[3]:.1f} (x0={b[0]:.1f}): {repr(b[4].strip()[:40])}")

# 2012 Page 2
doc2012 = fitz.open(os.path.join(pdf_dir, 'media_1791638977591_76a523d2.pdf'))
p2 = doc2012[2]
print("\n=== 2012 Page 2 blocks ===")
for b in p2.get_text('blocks'):
    print(f"y0={b[1]:.1f}..{b[3]:.1f} (x0={b[0]:.1f}): {repr(b[4].strip()[:40])}")
