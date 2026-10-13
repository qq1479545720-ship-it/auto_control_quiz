# -*- coding: utf-8 -*-
import fitz, os, re, sys
from PIL import Image

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')
modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']

print("=== Checking headings and top overflows for 2013-2024 ===")

for yr in modern_years:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
    
    # Track headings across all pages
    all_heads = [] # (pno, y0, y1, head_cn, text)
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        blks = page.get_text('dict')['blocks']
        for b in blks:
            if 'lines' in b:
                for line in b['lines']:
                    txt = ''.join(s['text'] for s in line['spans']).strip()
                    x0 = line['bbox'][0]
                    y0 = line['bbox'][1]
                    y1 = line['bbox'][3]
                    if x0 < 120:
                        m = cn_pat.match(txt)
                        if m:
                            all_heads.append((pno, y0, y1, m.group(1), txt[:20]))
    
    print(f"\n{yr}: Total {len(all_heads)} headings found: {[h[3] for h in all_heads]}")
    # Check each page: does it have content before the first heading on that page?
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        page_heads = [h for h in all_heads if h[0] == pno]
        if not page_heads:
            print(f"  Page {pno}: NO HEADINGS on this page!")
            continue
        first_h = page_heads[0]
        # Check text or drawings before first_h[1]
        top_text = page.get_text("text", clip=fitz.Rect(0, 40, page.rect.width, first_h[1] - 5)).strip()
        top_drawings = [d for d in page.get_drawings() if d['rect'].y1 < first_h[1] and d['rect'].y0 > 40]
        if top_text or top_drawings:
            print(f"  Page {pno}: First head is {first_h[3]} at y={first_h[1]:.1f}pt. BEFORE IT: text len={len(top_text)}, drawings={len(top_drawings)}")
            if top_text:
                print(f"    Top text preview: {top_text[:60]!r}")
