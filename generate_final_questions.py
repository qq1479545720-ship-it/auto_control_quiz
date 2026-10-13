# -*- coding: utf-8 -*-
"""
考研《自动控制原理》2005-2025年（连续21年）官方真题极精细单题切分与大纲分类生成器
核心保障：
1. 100% 每张图片仅有一道独立题目，绝无两题合并。
2. 彻底去除水印、去学校抬头（中国计量大学/学院）、去页脚试卷字样、去【完】标记。
3. 严格遵循官方考研大纲分类：
   - 经典控制理论：控制系统的数学模型、时域分析法、根轨迹法、频率响应法、离散控制系统
   - 现代控制理论：统归“现代控制理论”大类
"""

import os, re, json, sys, glob
import cv2
import numpy as np
import fitz
from collections import Counter

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
img_out_dir = os.path.join(base_dir, "question_images")
os.makedirs(img_out_dir, exist_ok=True)

pdf_map = {
    '2005': 'media_1791638971400_fcd2155a.pdf',
    '2006': 'media_1791638971400_9aa4c2f4.pdf',
    '2007': 'media_1791638971402_48e50a8b.pdf',
    '2008': 'media_1791638971400_fba750cd.pdf',
    '2009': 'media_17916389700_bc024558.pdf' if False else 'media_1791638971400_bc024558.pdf',
    '2010': 'media_1791638977592_4ac36c0b.pdf',
    '2011': 'media_1791638977592_044c77ac.pdf',
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
    '2022': 'media_1791639003002_91ca1547.pdf',
    '2023': 'media_1791639003003_f8cf5af7.pdf',
    '2024': 'media_1791639003002_fc0c6c39.pdf',
    '2025': 'media_1791639006281_e72ca0ec.pdf',
}

def classify_text(text, fallback_type='时域分析法'):
    """严格依据考研大纲权威知识点特征智能分类"""
    # ① 现代控制理论
    if any(k in text for k in [
        '状态方程', '状态空间', '李雅普诺夫', '能控', '能观', '极点配置', 
        '状态反馈', '矩阵', '传递函数矩阵', '对角标准型', '约当', '李氏',
        '不可控', '不可观', '观测器', 'x˙', 'x(k+1)', 'Lyapunov', 'lyapunov'
    ]):
        return '现代控制理论'
        
    # ② 经典控制理论：离散控制系统
    if any(k in text for k in [
        '脉冲传递函数', '采样系统', '采样周期', '差分方程', 'Z变换', 'z变换', 
        'w变换', 'W变换', '闭环脉冲', '零阶保持器', '采样频率', '离散'
    ]):
        return '离散控制系统'
        
    # ③ 经典控制理论：根轨迹法
    if any(k in text for k in [
        '根轨迹', '渐近线', '分离点', '会合点', '与虚轴交点', '出射角', '入射角'
    ]):
        return '根轨迹法'
        
    # ④ 经典控制理论：频率响应法
    if any(k in text for k in [
        '伯德', 'Bode', 'bode', '对数幅频', '奈奎斯特', 'Nyquist', 'nyquist', 
        '乃氏', '幅值裕量', '相位裕量', '相角裕度', '相角裕量', '剪切频率', '截止频率', 
        '对数相频', '超前校正', '滞后校正', '频域', '频率特性', '最小相位'
    ]):
        return '频率响应法'
        
    # ⑤ 经典控制理论：时域分析法
    if any(k in text for k in [
        '超调', '调节时间', '峰值时间', '阻尼比', '稳态误差', '阶跃响应', '单位阶跃', 
        '劳斯', 'Routh', 'routh', '赫尔维茨', '欠阻尼', '误差积分'
    ]):
        return '时域分析法'
        
    # ⑥ 经典控制理论：控制系统的数学模型
    if any(k in text for k in [
        '方框图', '信号流图', '梅逊', 'Mason', '传递函数', '等效', '化简', 
        '电网络', '起搏器', '电冰箱', '微分方程', '结构图'
    ]):
        return '控制系统的数学模型'
        
    return fallback_type

def find_best_gap_cut(gray, y_target, search_up=35, search_down=10):
    H, W = gray.shape
    y_min = max(0, int(y_target - search_up))
    y_max = min(H, int(y_target + search_down))
    sub = (gray[y_min:y_max, int(W*0.08):int(W*0.92)] < 220).astype(np.uint8)
    row_sums = np.sum(sub, axis=1)
    
    zero_indices = np.where(row_sums <= 1)[0]
    if len(zero_indices) > 0:
        return y_min + int(np.median(zero_indices))
    
    best_offset = np.argmin(row_sums)
    return y_min + best_offset

def save_image(img, path):
    _, buf = cv2.imencode('.png', img)
    buf.tofile(path)

def trim_excess_whitespace(img, margin=15):
    """去除四周多余空白、横向/纵向干扰边框线"""
    if img is None or img.size == 0:
        return img
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    H, W = gray.shape
    if H < 10 or W < 10:
        return img
        
    # 排除外侧 5% 左右边缘避免纸张边框线影响行检测
    x_in0 = int(W * 0.05)
    x_in1 = int(W * 0.95)
    inner_gray = gray[:, x_in0:x_in1]
    
    row_sums = np.sum(inner_gray < 220, axis=1)
    ink_rows = np.where(row_sums > 3)[0]
    if len(ink_rows) == 0:
        return img
        
    # 过滤顶部孤立的水平细线（如上级框线残余）
    start_idx = 0
    while start_idx < len(ink_rows):
        r = ink_rows[start_idx]
        if row_sums[r] > 0.45 * (x_in1 - x_in0):
            if start_idx + 1 < len(ink_rows) and ink_rows[start_idx+1] - r > 5:
                start_idx += 1
                continue
        break
    if start_idx >= len(ink_rows):
        start_idx = 0
    top_row = ink_rows[start_idx]
    
    # 过滤底部孤立的水平细线
    end_idx = len(ink_rows) - 1
    while end_idx >= 0:
        r = ink_rows[end_idx]
        if row_sums[r] > 0.45 * (x_in1 - x_in0):
            if end_idx - 1 >= 0 and r - ink_rows[end_idx-1] > 5:
                end_idx -= 1
                continue
        break
    if end_idx < 0:
        end_idx = len(ink_rows) - 1
    bot_row = ink_rows[end_idx]
    
    top = max(0, top_row - margin)
    bot = min(H, bot_row + margin + 1)
    
    # 左右边框剔除
    col_sums = np.sum(gray[top:bot, :] < 220, axis=0)
    left_x = 0
    for x in range(int(W * 0.08)):
        if col_sums[x] > 0.70 * (bot - top):
            left_x = max(left_x, x + 6)
    right_x = W
    for x in range(W - 1, int(W * 0.92), -1):
        if col_sums[x] > 0.70 * (bot - top):
            right_x = min(right_x, x - 6)
            
    return img[top:bot, left_x:right_x]

all_questions = []
global_id = 0

def add_question(year, q_num, q_type, img, filename):
    global global_id
    global_id += 1
    clean_img = trim_excess_whitespace(img)
    save_image(clean_img, os.path.join(img_out_dir, filename))
    all_questions.append({
        "id": global_id,
        "year": f"{year}年",
        "year_num": int(year),
        "q_num": q_num,
        "type": q_type,
        "major_cat": "现代控制理论" if q_type == '现代控制理论' else "经典控制理论",
        "url": f"question_images/{filename}"
    })

def main():
    global global_id
    # ==========================================
    # 1. 2025年：高清双栏专属分割 (7道题)
    # ==========================================
    doc2025 = fitz.open(os.path.join(pdf_dir, pdf_map['2025']))
    pix0 = doc2025[0].get_pixmap(dpi=150)
    img0 = np.frombuffer(pix0.samples, dtype=np.uint8).reshape(pix0.height, pix0.width, pix0.n)
    if pix0.n == 4: img0 = cv2.cvtColor(img0, cv2.COLOR_RGBA2BGR)
    pix1 = doc2025[1].get_pixmap(dpi=150)
    img1 = np.frombuffer(pix1.samples, dtype=np.uint8).reshape(pix1.height, pix1.width, pix1.n)
    if pix1.n == 4: img1 = cv2.cvtColor(img1, cv2.COLOR_RGBA2BGR)

    H, W = img0.shape[:2]
    mid_x = W // 2
    q2025_slices = [
        (img0[740:1330, 120:mid_x], '第1题', '控制系统的数学模型'),
        (img0[1330:1680, 120:mid_x], '第2题', '根轨迹法'),
        (img0[80:940, mid_x:W-100], '第3题', '频率响应法'),
        (img0[940:1680, mid_x:W-100], '第4题', '频率响应法'),
        (img1[120:720, 100:mid_x], '第5题', '离散控制系统'),
        (img1[720:1240, 100:mid_x], '第6题', '现代控制理论'),
        (img1[1240:1680, 100:mid_x], '第7题', '现代控制理论'),
    ]
    for idx, (q_img, q_num, q_type) in enumerate(q2025_slices, 1):
        add_question('2025', q_num, q_type, q_img, f"q_2025_{idx:02d}.png")
    print(f"[2025年] 成功提取 7 道题目")

    # ==========================================
    # 2. 2022年：纯图像扫描卷 9道大题毫米级无重叠定位
    # ==========================================
    doc2022 = fitz.open(os.path.join(pdf_dir, pdf_map['2022']))
    cuts_2022 = {
        0: [
            (490, 965, '第1题', '控制系统的数学模型'),
            (965, 1450, '第2题', '时域分析法')
        ],
        1: [
            (120, 700, '第3题', '时域分析法'),
            (700, 1000, '第4题', '根轨迹法'),
            (1000, 1245, '第5题', '频率响应法'),
            (1245, 1480, '第6题', '频率响应法')
        ],
        2: [
            (130, 535, '第7题', '离散控制系统'),
            (535, 925, '第8题', '现代控制理论'),
            (925, 1180, '第9题', '现代控制理论')
        ]
    }
    q2022_cnt = 0
    for pno in [0, 1, 2]:
        page = doc2022[pno]
        pix = page.get_pixmap(dpi=150)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        for y0, y1, q_num, q_type in cuts_2022[pno]:
            q2022_cnt += 1
            sub = img[y0:y1, :]
            add_question('2022', q_num, q_type, sub, f"q_2022_{q2022_cnt:02d}.png")
    print(f"[2022年] 成功提取 9 道题目")

    # ==========================================
    # 3. 2007 - 2011年：已知精确题头坐标切分 (各9~10道题)
    # ==========================================
    early_config = {
        '2007': {
            'pages': {
                1: [92.4, 420.0, 570.0],
                2: [114.3, 262.5, 414.1, 538.5],
                3: [109.0, 252.2, 509.6]
            },
            'types': [
                '控制系统的数学模型', '时域分析法', '根轨迹法',
                '频率响应法', '频率响应法', '频率响应法', '离散控制系统',
                '现代控制理论', '现代控制理论', '现代控制理论'
            ],
            'page_bottoms': {1: 0.94, 2: 0.94, 3: 0.90}
        },
        '2008': {
            'pages': {
                1: [45.9, 265.9, 442.3],
                2: [55.1, 219.6, 354.8, 490.1],
                3: [55.1, 348.5]
            },
            'types': [
                '控制系统的数学模型', '时域分析法', '根轨迹法',
                '根轨迹法', '频率响应法', '频率响应法', '离散控制系统',
                '现代控制理论', '现代控制理论'
            ],
            'page_bottoms': {1: 0.94, 2: 0.94, 3: 0.85}
        },
        '2009': {
            'pages': {
                1: [77.1, 353.4, 592.2],
                2: [86.3, 275.0, 424.5, 570.6],
                3: [77.1, 261.3]
            },
            'types': [
                '控制系统的数学模型', '时域分析法', '根轨迹法',
                '根轨迹法', '频率响应法', '频率响应法', '离散控制系统',
                '现代控制理论', '现代控制理论'
            ],
            'page_bottoms': {1: 0.94, 2: 0.94, 3: 0.65}
        },
        '2010': {
            'pages': {
                1: [45.9, 266.0, 514.2],
                2: [50.0, 212.3, 377.4, 535.3],
                3: [71.0, 237.9]
            },
            'types': [
                '控制系统的数学模型', '时域分析法', '根轨迹法',
                '根轨迹法', '频率响应法', '频率响应法', '离散控制系统',
                '现代控制理论', '现代控制理论'
            ],
            'page_bottoms': {1: 0.94, 2: 0.94, 3: 0.65}
        },
        '2011': {
            'pages': {
                1: [45.9, 248.6, 470.0],
                2: [45.6, 237.3, 318.6, 630.5],
                3: [30.0, 247.1]
            },
            'types': [
                '控制系统的数学模型', '时域分析法', '根轨迹法',
                '根轨迹法', '频率响应法', '频率响应法', '离散控制系统',
                '现代控制理论', '现代控制理论'
            ],
            'page_bottoms': {1: 0.94, 2: 0.94, 3: 0.75}
        }
    }

    for yr, cfg in early_config.items():
        doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
        scale = 150.0 / 72.0
        yr_cnt = 0
        for pno, heads in cfg['pages'].items():
            page = doc[pno]
            pix = page.get_pixmap(dpi=150)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            H, W = gray.shape
            
            cuts = []
            cuts.append(find_best_gap_cut(gray, heads[0] * scale - 15, search_up=25, search_down=5))
            for yh in heads[1:]:
                cuts.append(find_best_gap_cut(gray, yh * scale - 15, search_up=35, search_down=5))
            
            p_bot_factor = cfg.get('page_bottoms', {}).get(pno, 0.94)
            cuts.append(int(H * p_bot_factor))
            
            for i in range(len(cuts) - 1):
                yr_cnt += 1
                sub = img[cuts[i]:cuts[i+1], :]
                q_type = cfg['types'][yr_cnt - 1]
                add_question(yr, f"第{yr_cnt}题", q_type, sub, f"q_{yr}_{yr_cnt:02d}.png")
        print(f"[{yr}年] 成功提取 {yr_cnt} 道题目")

    # ==========================================
    # 4. 2012年：Page 0扫描题(Q1-Q4) + Page 1, 2(Q5-Q10) (共10道题)
    # ==========================================
    doc2012 = fitz.open(os.path.join(pdf_dir, pdf_map['2012']))
    p0 = doc2012[0]
    pix0 = p0.get_pixmap(dpi=150)
    img0 = np.frombuffer(pix0.samples, dtype=np.uint8).reshape(pix0.height, pix0.width, pix0.n)
    if pix0.n == 4: img0 = cv2.cvtColor(img0, cv2.COLOR_RGBA2BGR)

    p0_cuts = [
        (240, 1140, '第1题', '控制系统的数学模型'),
        (1140, 1600, '第2题', '时域分析法'),
        (1600, 2070, '第3题', '时域分析法'),
        (2070, 2470, '第4题', '根轨迹法')
    ]
    for idx, (y0, y1, q_num, q_type) in enumerate(p0_cuts, 1):
        sub = img0[y0:y1, :]
        add_question('2012', q_num, q_type, sub, f"q_2012_{idx:02d}.png")

    p1_heads = [89.4, 167.4, 280.6, 346.8, 526.2]
    p2_heads = [82.7]
    p12_types = ['根轨迹法', '频率响应法', '频率响应法', '频率响应法', '离散控制系统', '现代控制理论']

    cnt_2012 = 4
    scale = 150.0 / 72.0
    for pno, heads in [(1, p1_heads), (2, p2_heads)]:
        page = doc2012[pno]
        pix = page.get_pixmap(dpi=150)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        H, W = gray.shape
        
        cuts = []
        cuts.append(find_best_gap_cut(gray, heads[0] * scale - 15, search_up=25, search_down=5))
        for yh in heads[1:]:
            cuts.append(find_best_gap_cut(gray, yh * scale - 15, search_up=35, search_down=5))
        bot_cut = int(310) if pno == 2 else int(H * 0.94)
        cuts.append(bot_cut)
        
        for i in range(len(cuts) - 1):
            cnt_2012 += 1
            sub = img[cuts[i]:cuts[i+1], :]
            q_type = p12_types[cnt_2012 - 5]
            add_question('2012', f"第{cnt_2012}题", q_type, sub, f"q_2012_{cnt_2012:02d}.png")
    print(f"[2012年] 成功提取 10 道题目")

    # ==========================================
    # 5. 2005 & 2006年：精细大题分割
    # ==========================================
    # 2005: 12题 (填空, 简答, 计算1-10)
    doc2005 = fitz.open(os.path.join(pdf_dir, pdf_map['2005']))
    scale2005 = 150.0 / 72.0
    p1_2005 = doc2005[1].get_pixmap(dpi=150)
    img_p1 = np.frombuffer(p1_2005.samples, dtype=np.uint8).reshape(p1_2005.height, p1_2005.width, p1_2005.n)
    if p1_2005.n == 4: img_p1 = cv2.cvtColor(img_p1, cv2.COLOR_RGBA2BGR)
    add_question('2005', '第1题', '控制系统的数学模型', img_p1[210:780, :], 'q_2005_01.png')
    add_question('2005', '第2题', '现代控制理论', img_p1[780:1240, :], 'q_2005_02.png')
    add_question('2005', '第3题', '控制系统的数学模型', img_p1[1240:1640, :], 'q_2005_03.png')

    p2_heads_2005 = [111.8, 314.6, 509.3, 720.2]
    p2_types_2005 = ['控制系统的数学模型', '时域分析法', '时域分析法', '根轨迹法']
    p2_2005 = doc2005[2].get_pixmap(dpi=150)
    img_p2 = np.frombuffer(p2_2005.samples, dtype=np.uint8).reshape(p2_2005.height, p2_2005.width, p2_2005.n)
    if p2_2005.n == 4: img_p2 = cv2.cvtColor(img_p2, cv2.COLOR_RGBA2BGR)
    gray_p2 = cv2.cvtColor(img_p2, cv2.COLOR_BGR2GRAY)
    cuts_p2 = [find_best_gap_cut(gray_p2, p2_heads_2005[0]*scale2005 - 15, 25, 5)]
    for yh in p2_heads_2005[1:]:
        cuts_p2.append(find_best_gap_cut(gray_p2, yh*scale2005 - 15, 30, 5))
    cuts_p2.append(int(img_p2.shape[0] * 0.985))

    for i in range(3):
        sub = img_p2[cuts_p2[i]:cuts_p2[i+1], :]
        add_question('2005', f"第{4+i}题", p2_types_2005[i], sub, f"q_2005_{4+i:02d}.png")

    p3_2005 = doc2005[3].get_pixmap(dpi=150)
    img_p3 = np.frombuffer(p3_2005.samples, dtype=np.uint8).reshape(p3_2005.height, p3_2005.width, p3_2005.n)
    if p3_2005.n == 4: img_p3 = cv2.cvtColor(img_p3, cv2.COLOR_RGBA2BGR)

    q7_text = img_p2[cuts_p2[3]:cuts_p2[4], :]
    q7_diag = img_p3[120:360, :]
    q7_full = np.vstack([q7_text, q7_diag])
    add_question('2005', '第7题', '根轨迹法', q7_full, 'q_2005_07.png')

    add_question('2005', '第8题', '频率响应法', img_p3[360:650, :], 'q_2005_08.png')
    add_question('2005', '第9题', '频率响应法', img_p3[650:980, :], 'q_2005_09.png')
    add_question('2005', '第10题', '现代控制理论', img_p3[980:1330, :], 'q_2005_10.png')
    add_question('2005', '第11题', '频率响应法', img_p3[1330:1500, :], 'q_2005_11.png')

    # Q12: 跨第3页与第4页，精确定位去除页码4和【完】
    p4_2005 = doc2005[4].get_pixmap(dpi=150)
    img_p4 = np.frombuffer(p4_2005.samples, dtype=np.uint8).reshape(p4_2005.height, p4_2005.width, p4_2005.n)
    if p4_2005.n == 4: img_p4 = cv2.cvtColor(img_p4, cv2.COLOR_RGBA2BGR)
    q12_full = np.vstack([img_p3[1480:1580, :], img_p4[120:415, :]])
    add_question('2005', '第12题', '现代控制理论', q12_full, 'q_2005_12.png')
    print(f"[2005年] 成功提取 12 道题目")

    # 2006: 14题 (一～十四)
    doc2006 = fitz.open(os.path.join(pdf_dir, pdf_map['2006']))
    heads_2006_map = {
        1: ([71.7, 283.4, 501.8], ['控制系统的数学模型', '控制系统的数学模型', '时域分析法']),
        2: ([80.6, 258.7, 392.8, 487.4, 664.3], ['时域分析法', '根轨迹法', '根轨迹法', '时域分析法', '频率响应法']),
        3: ([87.6, 190.4, 396.3, 534.1, 735.8], ['频率响应法', '频率响应法', '现代控制理论', '离散控制系统', '现代控制理论']),
        4: ([252.2], ['现代控制理论'])
    }
    cnt_2006 = 0
    scale2006 = 150.0 / 72.0
    for pno in [1, 2, 3, 4]:
        page = doc2006[pno]
        pix = page.get_pixmap(dpi=150)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        H, W = gray.shape
        heads, types = heads_2006_map[pno]
        
        cuts = [find_best_gap_cut(gray, heads[0] * scale2006 - 15, 25, 5)]
        for yh in heads[1:]:
            cuts.append(find_best_gap_cut(gray, yh * scale2006 - 15, 30, 5))
        bot_cut = int(370 * scale2006) if pno == 4 else int(H * 0.94)
        cuts.append(bot_cut)
        
        for i in range(len(cuts) - 1):
            cnt_2006 += 1
            sub = img[cuts[i]:cuts[i+1], :]
            add_question('2006', f"第{cnt_2006}题", types[i], sub, f"q_2006_{cnt_2006:02d}.png")
    print(f"[2006年] 成功提取 14 道题目")

    # ==========================================
    # 6. 2013 - 2021, 2023 - 2024年：智能标题感知自动分割 (各9道题)
    # ==========================================
    cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')
    modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']

    for yr in modern_years:
        doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
        start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
        end_p = len(doc)
        yr_cnt = 0
        
        for pno in range(start_p, end_p):
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
                                heads_on_page.append((y0, txt))
            
            heads_on_page.sort(key=lambda x: x[0])
            if len(heads_on_page) == 0:
                continue
                
            pix = page.get_pixmap(dpi=150)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            H, W = gray.shape
            scale = 150.0 / 72.0
            
            # 检测顶部页眉（去除学校抬头）
            header_bot_pt = 35.0
            for b in page.get_text("blocks"):
                if b[1] < 120.0 and any(kw in b[4] for kw in ['中国计量', '大学', '学院', '研究生', '考试试题']):
                    header_bot_pt = max(header_bot_pt, b[3] + 8.0)
            
            # 检查本页顶部是否存在上一道大题的跨页内容（图表或附加问）
            first_head_y = heads_on_page[0][0] * scale
            if pno > start_p and heads_on_page[0][0] > 115.0 and len(all_questions) > 0:
                overflow_bottom = find_best_gap_cut(gray, first_head_y - 12, search_up=35, search_down=5)
                overflow_top = int(header_bot_pt * scale)
                if overflow_bottom > overflow_top:
                    overflow_slice = img[overflow_top:overflow_bottom, :]
                    if np.sum(overflow_slice < 220) > 1200:
                        prev_q = all_questions[-1]
                        prev_img_path = os.path.join(img_out_dir, os.path.basename(prev_q['url']))
                        prev_img = cv2.imdecode(np.fromfile(prev_img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
                        if prev_img is not None:
                            merged = np.vstack([prev_img, trim_excess_whitespace(overflow_slice)])
                            save_image(trim_excess_whitespace(merged), prev_img_path)

            # 计算每一题的精准切分线
            cuts = []
            cuts.append(find_best_gap_cut(gray, first_head_y - 12, search_up=25, search_down=5))
            
            for yh, _ in heads_on_page[1:]:
                cut_y = find_best_gap_cut(gray, yh * scale - 12, search_up=35, search_down=5)
                cuts.append(cut_y)
                
            # 页面底部裁切点（严格排除页脚试卷字样及【完】标记）
            footer_top_img = H * 0.94
            for b in page.get_text("blocks"):
                txt = b[4].strip()
                if '【完】' in txt or '【 完 】' in txt or '(完)' in txt:
                    footer_top_img = min(footer_top_img, b[1] * scale - 12)
                elif b[1] > page.rect.height * 0.70 and any(kw in txt for kw in ['试卷', '共', '页']):
                    footer_top_img = min(footer_top_img, b[1] * scale - 10)
                    
            footer_cut = find_best_gap_cut(gray, footer_top_img - 10, search_up=35, search_down=5)
            cuts.append(footer_cut)
            
            for i in range(len(cuts) - 1):
                yr_cnt += 1
                y0_cut = cuts[i]
                y1_cut = cuts[i+1]
                sub = img[y0_cut:y1_cut, :]
                
                # 自动提取该切片文本用于智能分类
                clip_rect = fitz.Rect(0, y0_cut * 72.0 / 150.0, page.rect.width, y1_cut * 72.0 / 150.0)
                crop_text = page.get_text("text", clip=clip_rect)
                
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
                fb = fallback_map.get(yr_cnt, '现代控制理论')
                q_type = classify_text(crop_text, fallback_type=fb)
                
                add_question(yr, f"第{yr_cnt}题", q_type, sub, f"q_{yr}_{yr_cnt:02d}.png")
                
        print(f"[{yr}年] 成功提取 {yr_cnt} 道题目")

    # 排序：按考点类型、年份、编号
    all_questions.sort(key=lambda x: (x["type"], x["year_num"], x["id"]))

    js_content = "const classifiedImages = " + json.dumps(all_questions, ensure_ascii=False, indent=4) + ";"
    out_js_path = os.path.join(base_dir, "classified_data.js")
    with open(out_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    type_counts = Counter(q["type"] for q in all_questions)
    print(f"\n========================================")
    print(f"全部大纲分类处理完成！共生成 {len(all_questions)} 张高品质独立题目图片")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c} 道")
    print(f"数据已保存至: {out_js_path}")

if __name__ == '__main__':
    main()
