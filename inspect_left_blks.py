import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

pdf_map = {
    '2007': 'media_1791638971402_48e50a8b.pdf',
    '2008': 'media_1791638971400_fba750cd.pdf',
    '2009': 'media_1791638971400_bc024558.pdf',
    '2010': 'media_1791638977592_4ac36c0b.pdf',
    '2011': 'media_1791638977592_044c77ac.pdf'
}

for yr, fname in pdf_map.items():
    doc = fitz.open(os.path.join(pdf_dir, fname))
    print(f"\n==================== {yr} ====================")
    for pno in range(1, len(doc)):
        p = doc[pno]
        blks = p.get_text('blocks')
        # find blocks where x0 < 80
        left_blks = [b for b in blks if b[0] < 80 and len(b[4].strip()) > 0]
        print(f"Page {pno} (H={p.rect.height:.1f}, left_blks={len(left_blks)}):")
        for b in left_blks:
            t = b[4].strip().replace('\n', ' ')
            print(f"   y={b[1]:.1f}..{b[3]:.1f} (x={b[0]:.1f}): {repr(t[:40])}")
