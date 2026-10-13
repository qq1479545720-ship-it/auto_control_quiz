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
    for pno in range(1, 4):
        p = doc[pno]
        found = []
        for b in p.get_text('dict')['blocks']:
            if 'lines' in b:
                for l in b['lines']:
                    txt = ''.join(s['text'] for s in l['spans']).strip()
                    h = l['bbox'][3] - l['bbox'][1]
                    x0 = l['bbox'][0]
                    y0 = l['bbox'][1]
                    # Large line height and left-aligned
                    if h > 20 and x0 < 80:
                        found.append((round(y0, 1), round(h, 1), txt))
        print(f"Page {pno} (found {len(found)}):")
        for y0, h, t in found:
            print(f"   y0={y0}, h={h}: {repr(t)}")
