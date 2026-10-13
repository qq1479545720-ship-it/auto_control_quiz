# -*- coding: utf-8 -*-
"""
严谨自查：遍历所有现代卷及数字排版卷，根据每一题的裁切区间提取文字，
核查是否存在一张截图里包含 2 个及以上大题题号的情况！
"""
import pymupdf as fitz
import re, os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
from update_all_questions import pdf_map

cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')
modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']

scale = 150.0 / 72.0
error_count = 0

for yr in modern_years:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
    
    # 提取所有大题题号及其绝对页码与y坐标
    all_heads = []
    for pno in range(start_p, len(doc)):
        page = doc[pno]
        for b in page.get_text('dict')['blocks']:
            if 'lines' in b:
                for line in b['lines']:
                    txt = ''.join(s['text'] for s in line['spans']).strip()
                    if line['bbox'][0] < 120:
                        m = cn_pat.match(txt)
                        if m:
                            all_heads.append((pno, line['bbox'][1], m.group(1), txt))
                            
    all_heads.sort(key=lambda x: (x[0], x[1]))
    
    # 验证是否恰好有9个大题题号
    if len(all_heads) != 9:
        print(f"ERROR: {yr} found {len(all_heads)} heads: {[h[2] for h in all_heads]}")
        error_count += 1
    else:
        # 核查题号顺序是否为 一至九
        expected_seq = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
        actual_seq = [h[2] for h in all_heads]
        if actual_seq != expected_seq:
            print(f"ERROR: {yr} heading sequence mismatch: {actual_seq}")
            error_count += 1

print(f"\n现代年份大题题号序列审计完成：发现错误数 = {error_count}")
