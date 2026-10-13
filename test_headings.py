import pymupdf as fitz
import re, os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

pdf_map = {
    '2005': 'media_1791638971400_fcd2155a.pdf',
    '2006': 'media_1791638971400_9aa4c2f4.pdf',
    '2012': 'media_1791638977591_76a523d2.pdf',
    '2013': 'media_1791638977591_d34b8c28.pdf',
    '2014': 'media_1791638977592_743cdcf4.pdf',
    '2015': 'media_1791638997981_be48dda9.pdf',
    '2016': 'media_1791638997993_3807f033.pdf',
    '2017': 'media_1791638997993_7f7d8443.pdf',
    '2018': 'media_1791638997993_666c4aa3.pdf',
    '2019': 'media_1791638997981_93c779ac.pdf',
    '2020': 'media_1791639003002_a4998716.pdf',
    '2021': 'media_1791639003001_8c86ce8c.pdf',
    '2023': 'media_1791639003003_f8cf5af7.pdf',
    '2024': 'media_1791639003002_fc0c6c39.pdf',
}

# Regex for questions like 一、（15分） or 一、 or 1、 or （一）
# Note that in 2005/2006, they might be 一、 or 1.
pat = re.compile(r'^\s*([一二三四五六七八九十]+|[1-9]|10)\s*([、.．\s\uff0c,]|[\(（])')

for yr in sorted(pdf_map.keys()):
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    start_p = 1 if yr <= '2020' else 0
    all_heads = []
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        blks = page.get_text('dict')['blocks']
        for b in blks:
            if 'lines' in b:
                for line in b['lines']:
                    txt = ''.join(s['text'] for s in line['spans']).strip()
                    m = pat.match(txt)
                    if m:
                        # check if it's near left margin
                        x0 = line['bbox'][0]
                        if x0 < 120: # major headings are on the left
                            all_heads.append((pno, round(x0, 1), round(line['bbox'][1], 1), txt[:30]))
    print(f"=== {yr}: found {len(all_heads)} headings ===")
    for h in all_heads:
        print(f"  P{h[0]} y={h[2]} (x={h[1]}): {h[3]}")
