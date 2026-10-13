import fitz, os, re, sys, json
import numpy as np

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

# Check for each year 2013-2024
cn_heads = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

print("--- Checking 2013-2024 heading distribution across pages ---")
modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']
cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')

for yr in modern_years:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
    found_heads = []
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        blks = page.get_text('dict')['blocks']
        for b in blks:
            if 'lines' in b:
                for line in b['lines']:
                    txt = ''.join(s['text'] for s in line['spans']).strip()
                    x0 = line['bbox'][0]
                    y0 = line['bbox'][1]
                    if x0 < 120:
                        m = cn_pat.match(txt)
                        if m:
                            found_heads.append((pno, round(y0, 1), m.group(1), txt[:25]))
    print(f"[{yr}] Found {len(found_heads)} headings: {[h[2] for h in found_heads]}")
    # Verify no heading was missed
    expected = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
    actual = [h[2] for h in found_heads]
    if actual != expected:
        print(f"  WARNING! Mismatch in {yr}: expected {expected}, got {actual}")
