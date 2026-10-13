import pymupdf as fitz
import cv2
import numpy as np
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

# Let's inspect 2022
doc2022 = fitz.open(os.path.join(pdf_dir, 'media_1791639003002_91ca1547.pdf'))
print("2022 pages:", len(doc2022))
for i, page in enumerate(doc2022):
    pix = page.get_pixmap(dpi=150)
    print(f"Page {i}: width={pix.width}, height={pix.height}")

# Let's inspect 2007-2011 blocks
for yr, fname in [('2007', 'media_1791638971402_48e50a8b.pdf'),
                  ('2008', 'media_1791638971400_fba750cd.pdf'),
                  ('2009', 'media_1791638971400_bc024558.pdf'),
                  ('2010', 'media_1791638977592_4ac36c0b.pdf'),
                  ('2011', 'media_1791638977592_044c77ac.pdf')]:
    doc = fitz.open(os.path.join(pdf_dir, fname))
    print(f"\n--- Year {yr} ---")
    start_p = 1
    for pno in range(start_p, len(doc)):
        p = doc[pno]
        blks = p.get_text('blocks')
        print(f"  Page {pno}: {len(blks)} blocks")
        for b in blks:
            # bbox: (x0, y0, x1, y1)
            # check blocks near left margin (x0 < 80)
            if b[0] < 80 and len(b[4].strip()) > 0:
                repr_txt = b[4].strip().replace('\n', ' ')[:30]
                print(f"    x0={b[0]:.1f}, y0={b[1]:.1f}, y1={b[3]:.1f}: {repr(repr_txt)}")
