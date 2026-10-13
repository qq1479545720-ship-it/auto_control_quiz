import pymupdf as fitz
import re, os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

pdf_map = {
    '2005': ('media_1791638971400_fcd2155a.pdf', range(1, 5)),
    '2006': ('media_1791638971400_9aa4c2f4.pdf', range(1, 5)),
    '2012': ('media_1791638977591_76a523d2.pdf', range(0, 3)),
    '2013': ('media_1791638977591_d34b8c28.pdf', range(1, 4)),
    '2014': ('media_1791638977592_743cdcf4.pdf', range(1, 4)),
    '2015': ('media_1791638997981_be48dda9.pdf', range(1, 4)),
    '2016': ('media_1791638997993_3807f033.pdf', range(1, 4)),
}

cn_num_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')
num_pat = re.compile(r'^\s*([1-9]|10)\s*[、.．\s]')

for yr in sorted(pdf_map.keys()):
    fname, prange = pdf_map[yr]
    doc = fitz.open(os.path.join(pdf_dir, fname))
    print(f"\n==================== {yr} ====================")
    for pno in prange:
        p = doc[pno]
        blks = p.get_text('dict')['blocks']
        heads_cn = []
        heads_num = []
        for b in blks:
            if 'lines' in b:
                for line in b['lines']:
                    txt = ''.join(s['text'] for s in line['spans']).strip()
                    x0 = line['bbox'][0]
                    y0 = line['bbox'][1]
                    if x0 < 100:
                        if cn_num_pat.match(txt):
                            heads_cn.append((y0, txt[:30]))
                        elif num_pat.match(txt):
                            heads_num.append((y0, txt[:30]))
        print(f"  Page {pno}: {len(heads_cn)} CN headings: {heads_cn}")
        if len(heads_cn) == 0 and len(heads_num) > 0:
            print(f"     -> {len(heads_num)} NUM headings: {heads_num}")
