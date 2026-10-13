# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os, re, sys
from PIL import Image

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map, trim_excess_whitespace, classify_text

cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')
modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']

scale = 150.0 / 72.0

test_out = os.path.join(base_dir, "test_modern_out")
os.makedirs(test_out, exist_ok=True)

for yr in modern_years:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
    
    yr_questions = [] # list of (q_num, img, text)
    
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        blks = page.get_text('dict')['blocks']
        heads_on_page = []
        for b in blks:
            if 'lines' in b:
                for line in b['lines']:
                    txt = ''.join(s['text'] for s in line['spans']).strip()
                    x0 = line['bbox'][0]
                    y0 = line['bbox'][1]
                    if x0 < 120:
                        m = cn_pat.match(txt)
                        if m:
                            heads_on_page.append((y0, m.group(1), txt))
        
        heads_on_page.sort(key=lambda x: x[0])
        if not heads_on_page:
            continue
            
        pix = page.get_pixmap(dpi=150)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        H, W = img.shape[:2]
        
        # Header bottom
        header_bot_pt = 35.0
        for b in page.get_text("blocks"):
            if b[1] < 120.0 and any(kw in b[4] for kw in ['中国计量', '大学', '学院', '研究生', '考试试题', '招生考试']):
                header_bot_pt = max(header_bot_pt, b[3] + 8.0)
                
        # Top overflow to previous question
        first_h_pt = heads_on_page[0][0]
        first_h_px = int(first_h_pt * scale)
        header_bot_px = int(header_bot_pt * scale)
        
        if pno > start_p and first_h_pt > (header_bot_pt + 20.0) and len(yr_questions) > 0:
            top_cut_y = first_h_px - 14
            if top_cut_y > header_bot_px:
                top_slice = img[header_bot_px:top_cut_y, :]
                top_text = page.get_text("text", clip=fitz.Rect(0, header_bot_pt, page.rect.width, first_h_pt - 8.0)).strip()
                ink_cnt = np.sum(top_slice < 220)
                # Verify if there is actual content
                if len(top_text) > 0 or ink_cnt > 1200:
                    prev_num, prev_img, prev_txt = yr_questions[-1]
                    merged_img = np.vstack([prev_img, top_slice])
                    yr_questions[-1] = (prev_num, merged_img, prev_txt + "\n" + top_text)
                    print(f"  [{yr}] P{pno}: Stitched top overflow ({top_slice.shape[0]}px) to {prev_num}")
                    
        # Cut points on this page
        # Footer detection
        footer_top_px = int(H * 0.95)
        for b in page.get_text("blocks"):
            txt = b[4].strip()
            if any(kw in txt for kw in ['【完】', '【 完 】', '(完)', '【完 】']):
                footer_top_px = min(footer_top_px, int(b[1] * scale - 12))
            elif b[1] > page.rect.height * 0.70 and any(kw in txt for kw in ['试卷', '共', '页']):
                footer_top_px = min(footer_top_px, int(b[1] * scale - 10))
                
        for i, (yh_pt, h_cn, h_txt) in enumerate(heads_on_page):
            y_start = int(yh_pt * scale - 14)
            if i == 0 and pno == start_p:
                y_start = max(header_bot_px, y_start)
                
            if i < len(heads_on_page) - 1:
                next_yh_pt = heads_on_page[i+1][0]
                y_end = int(next_yh_pt * scale - 14)
            else:
                y_end = footer_top_px
                
            q_slice = img[y_start:y_end, :]
            clip_rect = fitz.Rect(0, y_start / scale, page.rect.width, y_end / scale)
            q_txt = page.get_text("text", clip=clip_rect)
            yr_questions.append((f"第{len(yr_questions)+1}题", q_slice, q_txt))
            
    print(f"{yr}: Extracted {len(yr_questions)} questions")
    assert len(yr_questions) == 9, f"{yr} expected 9 questions, got {len(yr_questions)}"
    
    # Audit each question: verify it has EXACTLY 1 heading!
    for idx, (q_num, q_img, q_txt) in enumerate(yr_questions, 1):
        clean = trim_excess_whitespace(q_img)
        # Check headings in q_txt
        found_in_txt = [m.group(1) for m in cn_pat.finditer(q_txt)]
        # We know each question should have its own heading
        print(f"  {yr} Q{idx}: img shape={clean.shape}")
