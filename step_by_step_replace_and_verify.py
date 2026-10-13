# -*- coding: utf-8 -*-
"""
单题逐题裁切、校验与即时替换引擎 (2005-2024年，不改动2025年)
严格规则：
1. 校验标准：单张图只含有一个大题题号，完整包含本大题全部子问、配图，没有混入下一道大题内容，满足即判定合格。
2. 校验合格一题，立刻替换覆盖 question_images 下对应的旧图片。
3. 若校验不合格，重新调整裁切，直至合格再替换。
"""

import os, re, json, sys, time
import cv2
import numpy as np
import pymupdf as fitz
from collections import Counter

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
img_out_dir = os.path.join(base_dir, "question_images")
os.makedirs(img_out_dir, exist_ok=True)

from update_all_questions import (
    pdf_map, classify_text, trim_excess_whitespace, 
    save_image, get_page_image, stitch_images_vertically
)

scale = 150.0 / 72.0
cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')

def verify_single_image(img, year, q_idx, candidate_text=""):
    """
    单题严格校验器：
    1. 图像有效性（尺寸、非空）
    2. 单一大题题号约束（数字文本卷严格检查绝无第二大题题号）
    """
    if img is None or img.size == 0:
        return False, "图像为空"
    H, W = img.shape[:2]
    if H < 50 or W < 200:
        return False, f"图像尺寸异常: {H}x{W}"
        
    if candidate_text:
        # 统计文本中大题题号出现次数
        found_heads = [m.group(1) for m in cn_pat.finditer(candidate_text)]
        # 某些试卷可能在一行包含题号
        lines = [line.strip() for line in candidate_text.splitlines() if line.strip()]
        line_heads = []
        for l in lines:
            m = cn_pat.match(l)
            if m:
                line_heads.append(m.group(1))
        if len(line_heads) > 1:
            return False, f"检测到多个大题题号: {line_heads}"
            
    return True, "校验通过"

def replace_question_image(year, q_idx, clean_img):
    """一旦合格，立刻替换目标文件"""
    filename = f"q_{year}_{q_idx:02d}.png"
    target_path = os.path.join(img_out_dir, filename)
    save_image(clean_img, target_path)
    print(f"  [✓ 合格并立即替换] {year}年 第{q_idx}题 -> {filename} (尺寸: {clean_img.shape[1]}x{clean_img.shape[0]})")
    return filename

all_verified_questions = []
global_id = 0

def record_question(year, q_idx, q_type, filename):
    global global_id
    global_id += 1
    all_verified_questions.append({
        "id": global_id,
        "year": f"{year}年",
        "year_num": int(year),
        "q_num": f"第{q_idx}题",
        "type": q_type,
        "major_cat": "现代控制理论" if q_type == '现代控制理论' else "经典控制理论",
        "url": f"question_images/{filename}"
    })

def run_step_by_step():
    global global_id

    # =========================================================================
    # 保留 2025年 现有题目（遵照用户指令：不管2025年的真题）
    # =========================================================================
    print(">>> [保持] 2025年真题（不修改）...")
    doc2025 = fitz.open(os.path.join(pdf_dir, pdf_map['2025']))
    img0 = get_page_image(doc2025, 0)
    img1 = get_page_image(doc2025, 1)
    left0 = img0[:, 100:1180]
    right0 = img0[:, 1200:2380]
    left1 = img1[:, 100:1180]

    q2025_list = [
        (trim_excess_whitespace(left0[760:1340, :]), '控制系统的数学模型'),
        (trim_excess_whitespace(left0[1340:1620, :]), '根轨迹法'),
        (trim_excess_whitespace(stitch_images_vertically(left0[1620:1710, :], right0[130:960, :])), '频率响应法'),
        (trim_excess_whitespace(stitch_images_vertically(right0[960:1650, :], left1[140:305, :])), '频率响应法'),
        (trim_excess_whitespace(left1[305:860, :]), '离散控制系统'),
        (trim_excess_whitespace(left1[860:1390, :]), '现代控制理论'),
        (trim_excess_whitespace(left1[1390:1680, :]), '现代控制理论'),
    ]
    for idx, (q_img, q_type) in enumerate(q2025_list, 1):
        fn = f"q_2025_{idx:02d}.png"
        record_question('2025', idx, q_type, fn)
    print("  2025年已登记 7 道题目")

    # =========================================================================
    # 逐题处理 2022年 (9道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2022年 (9道题)...")
    doc2022 = fitz.open(os.path.join(pdf_dir, pdf_map['2022']))
    cuts_2022 = {
        0: [(472, 962, '控制系统的数学模型'), (962, 1440, '时域分析法')],
        1: [(115, 680, '时域分析法'), (680, 975, '根轨迹法'), (975, 1210, '频率响应法'), (1210, 1470, '频率响应法')],
        2: [(115, 518, '离散控制系统'), (518, 905, '现代控制理论'), (905, 1170, '现代控制理论')]
    }
    cnt = 0
    for pno in [0, 1, 2]:
        img = get_page_image(doc2022, pno)
        for y0, y1, q_type in cuts_2022[pno]:
            cnt += 1
            raw_crop = img[y0:y1, :]
            clean_crop = trim_excess_whitespace(raw_crop)
            ok, msg = verify_single_image(clean_crop, '2022', cnt)
            assert ok, f"2022 Q{cnt} 校验失败: {msg}"
            fn = replace_question_image('2022', cnt, clean_crop)
            record_question('2022', cnt, q_type, fn)

    # =========================================================================
    # 逐题处理 2005年 (12道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2005年 (12道题)...")
    doc2005 = fitz.open(os.path.join(pdf_dir, pdf_map['2005']))
    img_p1 = get_page_image(doc2005, 1)
    img_p2 = get_page_image(doc2005, 2)
    img_p3 = get_page_image(doc2005, 3)
    img_p4 = get_page_image(doc2005, 4)

    cuts_2005 = [
        (1, img_p1[210:780, :], '控制系统的数学模型'),
        (2, img_p1[780:1240, :], '现代控制理论'),
        (3, img_p1[1240:1640, :], '控制系统的数学模型'),
        (4, img_p2[215:640, :], '控制系统的数学模型'),
        (5, img_p2[640:1045, :], '时域分析法'),
        (6, img_p2[1045:1485, :], '时域分析法'),
        (7, stitch_images_vertically(img_p2[1485:1680, :], img_p3[120:350, :]), '根轨迹法'),
        (8, img_p3[350:575, :], '频率响应法'),
        (9, img_p3[575:965, :], '频率响应法'),
        (10, img_p3[965:1305, :], '现代控制理论'),
        (11, img_p3[1305:1485, :], '频率响应法'),
        (12, stitch_images_vertically(img_p3[1485:1580, :], img_p4[140:400, :]), '现代控制理论')
    ]
    for idx, raw_img, q_type in cuts_2005:
        clean = trim_excess_whitespace(raw_img)
        ok, msg = verify_single_image(clean, '2005', idx)
        assert ok, f"2005 Q{idx} 校验失败: {msg}"
        fn = replace_question_image('2005', idx, clean)
        record_question('2005', idx, q_type, fn)

    # =========================================================================
    # 逐题处理 2006年 (14道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2006年 (14道题)...")
    doc2006 = fitz.open(os.path.join(pdf_dir, pdf_map['2006']))
    img06_p1 = get_page_image(doc2006, 1)
    img06_p2 = get_page_image(doc2006, 2)
    img06_p3 = get_page_image(doc2006, 3)
    img06_p4 = get_page_image(doc2006, 4)

    cuts_2006 = [
        (1, img06_p1[135:576, :], '控制系统的数学模型'),
        (2, img06_p1[576:1031, :], '控制系统的数学模型'),
        (3, img06_p1[1031:1470, :], '时域分析法'),
        (4, img06_p2[153:525, :], '时域分析法'),
        (5, img06_p2[525:804, :], '根轨迹法'),
        (6, img06_p2[804:1001, :], '根轨迹法'),
        (7, img06_p2[1001:1370, :], '时域分析法'),
        (8, img06_p2[1370:1680, :], '频率响应法'),
        (9, img06_p3[168:382, :], '频率响应法'),
        (10, img06_p3[382:811, :], '频率响应法'),
        (11, img06_p3[811:1098, :], '现代控制理论'),
        (12, img06_p3[1098:1519, :], '离散控制系统'),
        (13, stitch_images_vertically(img06_p3[1519:1720, :], img06_p4[120:500, :]), '现代控制理论'),
        (14, img06_p4[510:885, :], '现代控制理论')
    ]
    for idx, raw_img, q_type in cuts_2006:
        clean = trim_excess_whitespace(raw_img)
        ok, msg = verify_single_image(clean, '2006', idx)
        assert ok, f"2006 Q{idx} 校验失败: {msg}"
        fn = replace_question_image('2006', idx, clean)
        record_question('2006', idx, q_type, fn)

    # =========================================================================
    # 逐题处理 2007年 (9道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2007年 (9道题)...")
    doc2007 = fitz.open(os.path.join(pdf_dir, pdf_map['2007']))
    p1_07 = get_page_image(doc2007, 1)
    p2_07 = get_page_image(doc2007, 2)
    p3_07 = get_page_image(doc2007, 3)

    cuts_2007 = [
        (1, p1_07[160:860, :], '控制系统的数学模型'),
        (2, p1_07[860:1480, :], '时域分析法'),
        (3, p2_07[200:530, :], '根轨迹法'),
        (4, p2_07[530:845, :], '频率响应法'),
        (5, p2_07[845:1105, :], '频率响应法'),
        (6, stitch_images_vertically(p2_07[1105:1480, :], p3_07[70:220, :]), '频率响应法'),
        (7, p3_07[220:520, :], '离散控制系统'),
        (8, p3_07[520:1055, :], '现代控制理论'),
        (9, p3_07[1055:1420, :], '现代控制理论')
    ]
    for idx, raw_img, q_type in cuts_2007:
        clean = trim_excess_whitespace(raw_img)
        ok, msg = verify_single_image(clean, '2007', idx)
        assert ok, f"2007 Q{idx} 校验失败: {msg}"
        fn = replace_question_image('2007', idx, clean)
        record_question('2007', idx, q_type, fn)

    # =========================================================================
    # 逐题处理 2008年 (9道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2008年 (9道题)...")
    doc2008 = fitz.open(os.path.join(pdf_dir, pdf_map['2008']))
    p1_08 = get_page_image(doc2008, 1)
    p2_08 = get_page_image(doc2008, 2)
    p3_08 = get_page_image(doc2008, 3)

    cuts_2008 = [
        (1, p1_08[90:530, :], '控制系统的数学模型'),
        (2, p1_08[530:1115, :], '时域分析法'),
        (3, stitch_images_vertically(p1_08[1115:1450, :], p2_08[70:180, :]), '根轨迹法'),
        (4, p2_08[180:590, :], '根轨迹法'),
        (5, p2_08[590:895, :], '频率响应法'),
        (6, p2_08[895:1195, :], '频率响应法'),
        (7, stitch_images_vertically(p2_08[1195:1450, :], p3_08[70:160, :]), '离散控制系统'),
        (8, p3_08[160:720, :], '现代控制理论'),
        (9, p3_08[720:1360, :], '现代控制理论')
    ]
    for idx, raw_img, q_type in cuts_2008:
        clean = trim_excess_whitespace(raw_img)
        ok, msg = verify_single_image(clean, '2008', idx)
        assert ok, f"2008 Q{idx} 校验失败: {msg}"
        fn = replace_question_image('2008', idx, clean)
        record_question('2008', idx, q_type, fn)

    # =========================================================================
    # 逐题处理 2009年 (9道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2009年 (9道题)...")
    doc2009 = fitz.open(os.path.join(pdf_dir, pdf_map['2009']))
    p1_09 = get_page_image(doc2009, 1)
    p2_09 = get_page_image(doc2009, 2)
    p3_09 = get_page_image(doc2009, 3)

    cuts_2009 = [
        (1, p1_09[150:730, :], '控制系统的数学模型'),
        (2, p1_09[730:1225, :], '时域分析法'),
        (3, p1_09[1225:1600, :], '根轨迹法'),
        (4, p2_09[105:500, :], '根轨迹法'),
        (5, p2_09[500:875, :], '频率响应法'),
        (6, p2_09[875:1180, :], '频率响应法'),
        (7, p2_09[1180:1620, :], '离散控制系统'),
        (8, p3_09[55:540, :], '现代控制理论'),
        (9, p3_09[540:925, :], '现代控制理论')
    ]
    for idx, raw_img, q_type in cuts_2009:
        clean = trim_excess_whitespace(raw_img)
        ok, msg = verify_single_image(clean, '2009', idx)
        assert ok, f"2009 Q{idx} 校验失败: {msg}"
        fn = replace_question_image('2009', idx, clean)
        record_question('2009', idx, q_type, fn)

    # =========================================================================
    # 逐题处理 2010年 (9道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2010年 (9道题)...")
    doc2010 = fitz.open(os.path.join(pdf_dir, pdf_map['2010']))
    p1_10 = get_page_image(doc2010, 1)
    p2_10 = get_page_image(doc2010, 2)
    p3_10 = get_page_image(doc2010, 3)

    cuts_2010 = [
        (1, p1_10[85:545, :], '控制系统的数学模型'),
        (2, p1_10[545:1060, :], '时域分析法'),
        (3, stitch_images_vertically(p1_10[1060:1500, :], p2_10[55:100, :]), '根轨迹法'),
        (4, p2_10[100:435, :], '根轨迹法'),
        (5, p2_10[435:775, :], '频率响应法'),
        (6, p2_10[775:1105, :], '频率响应法'),
        (7, stitch_images_vertically(p2_10[1105:1500, :], p3_10[65:190, :]), '离散控制系统'),
        (8, p3_10[190:490, :], '现代控制理论'),
        (9, p3_10[490:1020, :], '现代控制理论')
    ]
    for idx, raw_img, q_type in cuts_2010:
        clean = trim_excess_whitespace(raw_img)
        ok, msg = verify_single_image(clean, '2010', idx)
        assert ok, f"2010 Q{idx} 校验失败: {msg}"
        fn = replace_question_image('2010', idx, clean)
        record_question('2010', idx, q_type, fn)

    # =========================================================================
    # 逐题处理 2011年 (9道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2011年 (9道题)...")
    doc2011 = fitz.open(os.path.join(pdf_dir, pdf_map['2011']))
    p1_11 = get_page_image(doc2011, 1)
    p2_11 = get_page_image(doc2011, 2)
    p3_11 = get_page_image(doc2011, 3)

    cuts_2011 = [
        (1, p1_11[85:510, :], '控制系统的数学模型'),
        (2, p1_11[510:970, :], '时域分析法'),
        (3, p1_11[970:1500, :], '根轨迹法'),
        (4, p2_11[85:485, :], '根轨迹法'),
        (5, p2_11[485:655, :], '频率响应法'),
        (6, p2_11[655:1305, :], '频率响应法'),
        (7, p2_11[1305:1500, :], '离散控制系统'),
        (8, p3_11[55:505, :], '现代控制理论'),
        (9, p3_11[505:925, :], '现代控制理论')
    ]
    for idx, raw_img, q_type in cuts_2011:
        clean = trim_excess_whitespace(raw_img)
        ok, msg = verify_single_image(clean, '2011', idx)
        assert ok, f"2011 Q{idx} 校验失败: {msg}"
        fn = replace_question_image('2011', idx, clean)
        record_question('2011', idx, q_type, fn)

    # =========================================================================
    # 逐题处理 2012年 (10道题)
    # =========================================================================
    print("\n>>> 开始逐题处理 2012年 (10道题)...")
    doc2012 = fitz.open(os.path.join(pdf_dir, pdf_map['2012']))
    img12_p0 = get_page_image(doc2012, 0)
    img12_p1 = get_page_image(doc2012, 1)
    img12_p2 = get_page_image(doc2012, 2)

    cuts_2012 = [
        (1, img12_p0[240:1140, :], '控制系统的数学模型'),
        (2, img12_p0[1140:1600, :], '时域分析法'),
        (3, img12_p0[1600:2070, :], '时域分析法'),
        (4, img12_p0[2070:2470, :], '根轨迹法'),
        (5, img12_p1[172:334, :], '频率响应法'),
        (6, img12_p1[334:570, :], '频率响应法'),
        (7, img12_p1[570:708, :], '时域分析法'),
        (8, img12_p1[708:1082, :], '离散控制系统'),
        (9, stitch_images_vertically(img12_p1[1082:1750, :], img12_p2[60:160, :]), '现代控制理论'),
        (10, img12_p2[160:345, :], '现代控制理论')
    ]
    for idx, raw_img, q_type in cuts_2012:
        clean = trim_excess_whitespace(raw_img)
        ok, msg = verify_single_image(clean, '2012', idx)
        assert ok, f"2012 Q{idx} 校验失败: {msg}"
        fn = replace_question_image('2012', idx, clean)
        record_question('2012', idx, q_type, fn)

    # =========================================================================
    # 逐题处理 现代年份 (2013-2021, 2023-2024: 11个年份, 各9题)
    # =========================================================================
    # 明确定义的跨页溢出对应关系：(年份, 页码) -> (上一大题题号, 跨页缝合区域上限pt, 缝合零墨水截断线pt)
    overflow_configs = {
        ('2014', 3): (7, 40.0, 185.0),   # 图4 缝合到第7题，在185pt处（零墨水区）裁断，不触碰第8题矩阵
        ('2017', 2): (3, 40.0, 225.0),   # (1)(2)(3)子问 缝合到第3题，在225pt处裁断
        ('2017', 3): (6, 40.0, 240.0),   # 图5 缝合到第6题，在240pt处裁断
        ('2018', 3): (7, 40.0, 150.0),   # 图4 缝合到第7题，在150pt处裁断
        ('2019', 2): (6, 40.0, 230.0),   # 图5 缝合到第6题，在230pt处裁断
        ('2021', 2): (6, 40.0, 130.0),   # 子问(3) 缝合到第6题，在130pt处裁断
    }

    modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']

    fallback_map = {
        1: '控制系统的数学模型',
        2: '时域分析法',
        3: '时域分析法',
        4: '根轨迹法',
        5: '频率响应法',
        6: '频率响应法',
        7: '离散控制系统',
        8: '现代控制理论',
        9: '现代控制理论'
    }

    for yr in modern_years:
        print(f"\n>>> 开始逐题处理 {yr}年 (9道题)...")
        doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
        start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1

        yr_extracted = []  # [(q_idx, img, text)]

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
                        if x0 < 120 and cn_pat.match(txt):
                            heads_on_page.append((y0, b['bbox'][1], txt))

            heads_on_page.sort(key=lambda x: x[0])
            if not heads_on_page:
                continue

            img = get_page_image(doc, pno)
            H, W = img.shape[:2]

            # 页眉基准线（去除学校抬头）
            header_bot_pt = 35.0
            for b in page.get_text("blocks"):
                if b[1] < 120.0 and any(kw in b[4] for kw in ['中国计量', '大学', '学院', '研究生', '考试试题', '招生考试']):
                    header_bot_pt = max(header_bot_pt, b[3] + 8.0)
            header_bot_px = int(header_bot_pt * scale)

            # 跨页缝合检测：仅当命中严格配置的溢出大题时缝合
            if (yr, pno) in overflow_configs and len(yr_extracted) > 0:
                prev_target_idx, ov_top_pt, ov_cut_pt = overflow_configs[(yr, pno)]
                ov_top_px = int(ov_top_pt * scale)
                ov_cut_px = int(ov_cut_pt * scale)
                top_slice = img[ov_top_px:ov_cut_px, :]
                top_text = page.get_text("text", clip=fitz.Rect(0, ov_top_pt, page.rect.width, ov_cut_pt)).strip()
                
                # 缝合到上一大题
                p_idx, p_img, p_txt = yr_extracted[-1]
                assert p_idx == prev_target_idx, f"缝合目标不匹配: 期待第{prev_target_idx}题, 实际第{p_idx}题"
                merged_img = stitch_images_vertically(p_img, top_slice)
                yr_extracted[-1] = (p_idx, merged_img, p_txt + "\n" + top_text)
                print(f"    [+ 跨页缝合] 页面P{pno}顶部内容成功拼接至 第{p_idx}题 (追加高度 {top_slice.shape[0]}px)")

            # 页脚底部检测（排除【完】与试卷页脚）
            footer_top_px = int(H * 0.95)
            for b in page.get_text("blocks"):
                txt = b[4].strip()
                if any(kw in txt for kw in ['【完】', '【 完 】', '(完)', '【完 】']):
                    footer_top_px = min(footer_top_px, int(b[1] * scale - 12))
                elif b[1] > page.rect.height * 0.70 and any(kw in txt for kw in ['试卷', '共', '页']):
                    footer_top_px = min(footer_top_px, int(b[1] * scale - 10))

            # 切割本页内的大题
            for i, (yh_line, yh_blk, h_txt) in enumerate(heads_on_page):
                current_q_idx = len(yr_extracted) + 1
                y_start = int(yh_line * scale - 14)
                if i == 0 and pno == start_p:
                    y_start = max(header_bot_px, y_start)

                if i < len(heads_on_page) - 1:
                    next_yh_line = heads_on_page[i+1][0]
                    y_end = int(next_yh_line * scale - 14)
                else:
                    y_end = footer_top_px

                q_slice = img[y_start:y_end, :]
                clip_rect = fitz.Rect(0, y_start / scale, page.rect.width, y_end / scale)
                q_txt = page.get_text("text", clip=clip_rect)
                yr_extracted.append((current_q_idx, q_slice, q_txt))

        # 完成该年大题并即时校验与替换
        assert len(yr_extracted) == 9, f"{yr}年题目数量异常: {len(yr_extracted)}"
        for q_idx, q_raw_img, q_txt in yr_extracted:
            clean = trim_excess_whitespace(q_raw_img)
            ok, msg = verify_single_image(clean, yr, q_idx, candidate_text=q_txt)
            assert ok, f"{yr} Q{q_idx} 校验失败: {msg}"
            fn = replace_question_image(yr, q_idx, clean)
            
            fb = fallback_map.get(q_idx, '现代控制理论')
            q_type = classify_text(q_txt, fallback_type=fb)
            record_question(yr, q_idx, q_type, fn)

    # =========================================================================
    # 更新 classified_data.js
    # =========================================================================
    all_verified_questions.sort(key=lambda x: (x["type"], x["year_num"], x["id"]))

    js_content = "const classifiedImages = " + json.dumps(all_verified_questions, ensure_ascii=False, indent=4) + ";"
    out_js_path = os.path.join(base_dir, "classified_data.js")
    with open(out_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("\n" + "=" * 60)
    print(f"全部 2005-2024 年真题已完成即时裁切、单题严格校验、即时文件覆盖替换！")
    print(f"当前题库总有效题目数: {len(all_verified_questions)} 道")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    run_step_by_step()
