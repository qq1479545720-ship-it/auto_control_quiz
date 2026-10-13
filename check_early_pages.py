import pymupdf as fitz
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

for yr in ['2005', '2006', '2007']:
    doc = fitz.open(os.path.join(pdf_dir, {
        '2005': 'media_1791638971400_fcd2155a.pdf',
        '2006': 'media_1791638971400_9aa4c2f4.pdf',
        '2007': 'media_1791638971402_48e50a8b.pdf'
    }[yr]))
    print(f"=== {yr} ===")
    for pno in range(len(doc)):
        p = doc[pno]
        txt = p.get_text('text').strip()
        print(f"p{pno} text len: {len(txt)}")
        if len(txt) > 0:
            print(f"   First 80 chars: {repr(txt[:80])}")
