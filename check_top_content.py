import pymupdf as fitz
import re, os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

pdf_map = {
    '2005': ('media_1791638971400_fcd2155a.pdf', range(1, 5)),
    '2006': ('media_1791638971400_9aa4c2f4.pdf', range(1, 5)),
    '2007': ('media_1791638971402_48e50a8b.pdf', range(1, 4)),
    '2008': ('media_1791638971400_fba750cd.pdf', range(1, 4)),
    '2009': ('media_1791638971400_bc024558.pdf', range(1, 4)),
    '2010': ('media_1791638977592_4ac36c0b.pdf', range(1, 4)),
    '2011': ('media_1791638977592_044c77ac.pdf', range(1, 4)),
    '2012': ('media_1791638977591_76a523d2.pdf', range(0, 3)),
    '2013': ('media_1791638977591_d34b8c28.pdf', range(1, 4)),
    '2014': ('media_1791638977592_743cdcf4.pdf', range(1, 4)),
    '2015': ('media_1791638997981_be48dda9.pdf', range(1, 4)),
    '2016': ('media_1791638997993_3807f033.pdf', range(1, 4)),
    '2017': ('media_1791638997993_7f7d8443.pdf', range(1, 4)),
    '2018': ('media_1791638997993_666c4aa3.pdf', range(1, 4)),
    '2019': ('media_1791638997981_93c779ac.pdf', range(0, 4)),
    '2020': ('media_1791639003002_a4998716.pdf', range(0, 4)),
    '2021': ('media_1791639003001_8c86ce8c.pdf', range(0, 3)),
    '2022': ('media_1791639003002_91ca1547.pdf', range(0, 3)),
    '2023': ('media_1791639003003_f8cf5af7.pdf', range(0, 4)),
    '2024': ('media_1791639003002_fc0c6c39.pdf', range(0, 4)),
    '2025': ('media_1791639006281_e72ca0ec.pdf', range(0, 2)),
}

cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')

print("=== Checking Content Above First Heading on Each Page ===")
for yr in ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']:
    fname, prange = pdf_map[yr]
    doc = fitz.open(os.path.join(pdf_dir, fname))
    for pno in prange:
        p = doc[pno]
        blks = p.get_text('blocks')
        first_head_y = 9999
        for b in blks:
            txt = b[4].strip()
            if b[0] < 120 and cn_pat.match(txt):
                first_head_y = min(first_head_y, b[1])
        # check blocks with y < first_head_y
        top_blks = [b for b in blks if b[3] < first_head_y and len(b[4].strip()) > 0 and '试卷' not in b[4] and '中国计量' not in b[4] and '考研' not in b[4] and '考生' not in b[4] and '代码' not in b[4] and '答题纸' not in b[4]]
        if len(top_blks) > 0:
            print(f"{yr} Page {pno}: first_head at y={first_head_y:.1f}, but has {len(top_blks)} content blocks above it:")
            for b in top_blks:
                print(f"   y={b[1]:.1f}..{b[3]:.1f}: {repr(b[4].strip()[:35])}")
