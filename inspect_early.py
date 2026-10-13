import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_map = {
    '2005': 'media_1791638971400_fcd2155a.pdf',
    '2006': 'media_1791638971400_9aa4c2f4.pdf',
    '2007': 'media_1791638971402_48e50a8b.pdf',
    '2008': 'media_1791638971400_fba750cd.pdf',
    '2009': 'media_1791638971400_bc024558.pdf',
    '2010': 'media_1791638977592_4ac36c0b.pdf',
    '2011': 'media_1791638977592_044c77ac.pdf',
    '2012': 'media_1791638977591_76a523d2.pdf',
    '2013': 'media_1791638977591_d34b8c28.pdf',
    '2022': 'media_1791639003002_91ca1547.pdf'
}
pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

for yr in ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2022']:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    print(f"=== {yr} (pages: {len(doc)}) ===")
    start_p = 1 if yr <= '2020' else 0
    for pno in range(start_p, len(doc)):
        p = doc[pno]
        txt = p.get_text("text")
        lines = [line.strip() for line in txt.split("\n") if line.strip()]
        print(f"  Page {pno}: {len(lines)} lines")
        for line in lines[:15]:
            print(f"    {line[:50]}")
