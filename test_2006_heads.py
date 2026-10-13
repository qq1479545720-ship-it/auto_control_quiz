import pymupdf as fitz
import re, os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_9aa4c2f4.pdf'))

heads_2006 = []
for pno in range(1, 5):
    p = doc[pno]
    blks = p.get_text('dict')['blocks']
    for b in blks:
        if 'lines' in b:
            for line in b['lines']:
                txt = ''.join(s['text'] for s in line['spans']).strip()
                if any(txt.startswith(k) for k in ['一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、', '十一、', '十二、', '十三、', '十四、']):
                    heads_2006.append((pno, line['bbox'][1], txt[:30]))

print(f"Found {len(heads_2006)} headings in 2006:")
for h in heads_2006:
    print(f"  P{h[0]} y={h[1]:.1f}: {h[2]}")
