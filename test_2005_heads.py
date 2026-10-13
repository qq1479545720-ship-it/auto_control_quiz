import pymupdf as fitz
import re, os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_fcd2155a.pdf'))

for pno in range(1, 5):
    p = doc[pno]
    blks = p.get_text('dict')['blocks']
    print(f"\n--- 2005 Page {pno} ---")
    for b in blks:
        if 'lines' in b:
            for line in b['lines']:
                txt = ''.join(s['text'] for s in line['spans']).strip()
                if any(txt.startswith(k) for k in ['一', '二', '三', '四', '五', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '填空', '简答', '计算']):
                    print(f"  y={line['bbox'][1]:.1f} (x={line['bbox'][0]:.1f}): {txt[:40]}")
