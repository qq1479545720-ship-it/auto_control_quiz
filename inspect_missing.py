import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

pdf_map = {
    '2012': 'media_1791638977591_76a523d2.pdf',
    '2013': 'media_1791638977591_d34b8c28.pdf',
    '2014': 'media_1791638977592_743cdcf4.pdf',
    '2019': 'media_1791638997981_93c779ac.pdf',
    '2020': 'media_1791639003002_a4998716.pdf'
}

for yr, fname in pdf_map.items():
    doc = fitz.open(os.path.join(pdf_dir, fname))
    print(f"==================== {yr} ====================")
    for pno in range(len(doc)):
        page = doc[pno]
        txt = page.get_text('text')
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        print(f"Page {pno} (total {len(lines)} lines):")
        for l in lines[:10]:
            print(f"   {l[:60]}")
