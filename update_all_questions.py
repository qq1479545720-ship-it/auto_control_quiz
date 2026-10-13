# -*- coding: utf-8 -*-
"""
更新与生成《自动控制原理》2005-2025年（连续21年）全部检查完毕的高品质题目截图及大纲分类
严格遵循硬性准则：
1. 裁切分割只识别大题题号，忽略小题（例如(1)(2)这类子小问）。
2. 每张截图必须且只能有 1 个大题题号，禁止出现 2 个及以上大题题号。
3. 严格排除学校抬头、试卷页眉页脚、排除【完】字样与水印。
4. 自动检测并垂直无缝拼接跨页溢出内容（子小问、图表、附加问）。
5. 现代控制理论题目统归“现代控制理论”大类；经典控制理论按官方考纲分为5类。
"""

import os, re, json, sys
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

pdf_map = {
    '2005': 'media_1791638971400_fcd2155a.pdf',
    '2006': 'media_1791638971400_9aa4c2f4.pdf',
    '2007': 'media_1791638971402_48e50a8b.pdf',
    '2008': 'media_1791638971400_fba750cd.pdf',
    '2009': 'media_1791638971400_bc024558.pdf',
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
    # 1. 现代控制理论
    if any(k in text for k in [
        '状态方程', '状态空间', '李雅普诺夫', '能控', '能观', '极点配置', 
        '状态反馈', '矩阵', '传递函数矩阵', '对角标准型', '约当', '李氏',
        '不可控', '不可观', '观测器', 'x˙', 'x(k+1)', 'Lyapunov', 'lyapunov',
        '可控', '可观', '李雅普诺'
    ]):
        return '现代控制理论'
        
    # 2. 经典控制理论：离散控制系统
    if any(k in text for k in [
        '脉冲传递函数', '采样系统', '采样周期', '差分方程', 'Z变换', 'z变换', 
        'w变换', 'W变换', '闭环脉冲', '零阶保持器', '采样频率', '离散'
    ]):
        return '离散控制系统'

    # 3. 经典控制理论：频率响应法
    if any(k in text for k in [
        '伯德', 'Bode', 'bode', '对数幅频', '幅频', '奈奎斯特', 'Nyquist', 'nyquist', 
        '奈氏', '༜氏', '༜༢斯特', '乃奎斯特', '乃氏', '幅值裕量', '相位裕量', '相角裕度', 
        '相角裕量', '相稳定裕度', '剪切频率', '截止频率', '对数相频', '超前校正', '滞后校正', 
        '频域', '频率特性', '最小相位', '⏤䖥对数', '对数幅频渐近'
    ]):
        return '频率响应法'
        
    # 4. 经典控制理论：根轨迹法
    if any(k in text for k in [
        '根轨迹', '分离点', '会合点', '与虚轴交点', '出射角', '入射角'
    ]):
        return '根轨迹法'
        
    # 5. 经典控制理论：时域分析法
    if any(k in text for k in [
        '超调', '调节时间', '峰值时间', '阻尼比', '阻尼系数', '稳态误差', '阶跃响应', 
        '单位阶跃', '劳斯', 'Routh', 'routh', '赫尔维茨', '欠阻尼', '误差积分',
        '静态加速度', '等幅振荡', '位置随动', '起搏器'
    ]):
        return '时域分析法'
        
    # 6. 经典控制理论：控制系统的数学模型
    if any(k in text for k in [
        '方框图', '信号流图', '梅逊', 'Mason', '传递函数', '等效', '化简', 
        '电网络', '微分方程', '结构图', '无源网络', '电冰箱'
    ]):
        return '控制系统的数学模型'
        
    return fallback_type

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
        
    x_in0 = int(W * 0.05)
    x_in1 = int(W * 0.95)
    inner_gray = gray[:, x_in0:x_in1]
    
    row_sums = np.sum(inner_gray < 220, axis=1)
    ink_rows = np.where(row_sums > 3)[0]
    if len(ink_rows) == 0:
        return img
        
    # 过滤顶部孤立水平细线
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
    
    # 过滤底部孤立水平细线
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

def get_page_image(doc, pno, dpi=150):
    page = doc[pno]
    pix = page.get_pixmap(dpi=dpi)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    return img

def stitch_images_vertically(img_top, img_bottom):
    """确保宽度一致并垂直拼接"""
    if img_top is None or img_top.size == 0:
        return img_bottom
    if img_bottom is None or img_bottom.size == 0:
        return img_top
    W_target = max(img_top.shape[1], img_bottom.shape[1])
    top_pad = np.pad(img_top, ((0,0), (0, W_target - img_top.shape[1]), (0,0)), constant_values=255)
    bot_pad = np.pad(img_bottom, ((0,0), (0, W_target - img_bottom.shape[1]), (0,0)), constant_values=255)
    return np.vstack([top_pad, bot_pad])

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

def process_all():
    global global_id
    scale = 150.0 / 72.0

    # =========================================================================
    # 1. 2025年：高清双栏专属分割 (7道题) - 跨栏/跨页精确定位
    # =========================================================================
    print(">>> 处理 2025年 (7道大题)...")
    doc2025 = fitz.open(os.path.join(pdf_dir, pdf_map['2025']))
    img0 = get_page_image(doc2025, 0)
    img1 = get_page_image(doc2025, 1)

    # Q1: Page 0 left col [775:1342, 60:1180]
    add_question('2025', '第1题', '控制系统的数学模型', img0[775:1342, 60:1180], 'q_2025_01.png')
    # Q2: Page 0 left col [1342:1545, 60:1180]
    add_question('2025', '第2题', '根轨迹法', img0[1342:1545, 60:1180], 'q_2025_02.png')
    # Q3: 跨栏拼接 Page 0 left col 底部 [1545:1625, 60:1180] + Page 0 right col 顶部 [80:965, 1200:2350]
    q3_stitched = stitch_images_vertically(img0[1545:1625, 60:1180], img0[80:965, 1200:2350])
    add_question('2025', '第3题', '频率响应法', q3_stitched, 'q_2025_03.png')
    # Q4: 跨页拼接 Page 0 right col [965:1635, 1200:2350] + Page 1 left col [120:295, 60:1180]
    q4_stitched = stitch_images_vertically(img0[965:1635, 1200:2350], img1[120:295, 60:1180])
    add_question('2025', '第4题', '频率响应法', q4_stitched, 'q_2025_04.png')
    # Q5: Page 1 left col [295:830, 60:1180]
    add_question('2025', '第5题', '离散控制系统', img1[295:830, 60:1180], 'q_2025_05.png')
    # Q6: Page 1 left col [830:1340, 60:1180]
    add_question('2025', '第6题', '现代控制理论', img1[830:1340, 60:1180], 'q_2025_06.png')
    # Q7: Page 1 left col [1340:1640, 60:1180]
    add_question('2025', '第7题', '现代控制理论', img1[1340:1640, 60:1180], 'q_2025_07.png')
    print("  2025年完成：7 道题目")

    # =========================================================================
    # 2. 2022年：纯图像扫描卷 9道大题毫米级无重叠定位
    # =========================================================================
    print(">>> 处理 2022年 (9道大题)...")
    doc2022 = fitz.open(os.path.join(pdf_dir, pdf_map['2022']))
    cuts_2022 = {
        0: [
            (472, 962, '第1题', '控制系统的数学模型'),
            (962, 1440, '第2题', '时域分析法')
        ],
        1: [
            (115, 680, '第3题', '时域分析法'),
            (680, 975, '第4题', '根轨迹法'),
            (975, 1210, '第5题', '频率响应法'),
            (1210, 1470, '第6题', '频率响应法')
        ],
        2: [
            (115, 518, '第7题', '离散控制系统'),
            (518, 905, '第8题', '现代控制理论'),
            (905, 1170, '第9题', '现代控制理论')
        ]
    }
    cnt_2022 = 0
    for pno in [0, 1, 2]:
        img = get_page_image(doc2022, pno)
        for y0, y1, q_num, q_type in cuts_2022[pno]:
            cnt_2022 += 1
            add_question('2022', q_num, q_type, img[y0:y1, :], f"q_2022_{cnt_2022:02d}.png")
    print(f"  2022年完成：{cnt_2022} 道题目")

    # =========================================================================
    # 3. 2005年：12道大题（填空1、简答2、计算1-10）
    # =========================================================================
    print(">>> 处理 2005年 (12道大题)...")
    doc2005 = fitz.open(os.path.join(pdf_dir, pdf_map['2005']))
    img_p1 = get_page_image(doc2005, 1)
    img_p2 = get_page_image(doc2005, 2)
    img_p3 = get_page_image(doc2005, 3)
    img_p4 = get_page_image(doc2005, 4)

    # Q1: 填空题
    add_question('2005', '第1题', '控制系统的数学模型', img_p1[210:780, :], 'q_2005_01.png')
    # Q2: 简答题
    add_question('2005', '第2题', '现代控制理论', img_p1[780:1240, :], 'q_2005_02.png')
    # Q3: 计算题1
    add_question('2005', '第3题', '控制系统的数学模型', img_p1[1240:1640, :], 'q_2005_03.png')

    # Q4: 计算题2 (P2)
    add_question('2005', '第4题', '控制系统的数学模型', img_p2[215:640, :], 'q_2005_04.png')
    # Q5: 计算题3 (P2)
    add_question('2005', '第5题', '时域分析法', img_p2[640:1045, :], 'q_2005_05.png')
    # Q6: 计算题4 (P2)
    add_question('2005', '第6题', '时域分析法', img_p2[1045:1485, :], 'q_2005_06.png')
    # Q7: 计算题5 (P2底部题干 + P3顶部图表垂直拼接)
    q7_full = stitch_images_vertically(img_p2[1485:1680, :], img_p3[120:350, :])
    add_question('2005', '第7题', '根轨迹法', q7_full, 'q_2005_07.png')

    # Q8: 计算题6 (P3)
    add_question('2005', '第8题', '频率响应法', img_p3[350:575, :], 'q_2005_08.png')
    # Q9: 计算题7 (P3)
    add_question('2005', '第9题', '频率响应法', img_p3[575:965, :], 'q_2005_09.png')
    # Q10: 计算题8 (P3)
    add_question('2005', '第10题', '现代控制理论', img_p3[965:1305, :], 'q_2005_10.png')
    # Q11: 计算题9 (P3)
    add_question('2005', '第11题', '频率响应法', img_p3[1305:1485, :], 'q_2005_11.png')
    # Q12: 计算题10 (P3底部题干 + P4顶部图表和矩阵拼接，彻底排除【完】与页码)
    q12_full = stitch_images_vertically(img_p3[1485:1580, :], img_p4[140:400, :])
    add_question('2005', '第12题', '现代控制理论', q12_full, 'q_2005_12.png')
    print("  2005年完成：12 道题目")

    # =========================================================================
    # 4. 2006年：14道大题（一～十四）
    # =========================================================================
    print(">>> 处理 2006年 (14道大题)...")
    doc2006 = fitz.open(os.path.join(pdf_dir, pdf_map['2006']))
    img06_p1 = get_page_image(doc2006, 1)
    img06_p2 = get_page_image(doc2006, 2)
    img06_p3 = get_page_image(doc2006, 3)
    img06_p4 = get_page_image(doc2006, 4)

    # P1: 一、二、三
    add_question('2006', '第1题', '控制系统的数学模型', img06_p1[135:576, :], 'q_2006_01.png')
    add_question('2006', '第2题', '控制系统的数学模型', img06_p1[576:1031, :], 'q_2006_02.png')
    add_question('2006', '第3题', '时域分析法', img06_p1[1031:1470, :], 'q_2006_03.png')

    # P2: 四、五、六、七、八
    add_question('2006', '第4题', '时域分析法', img06_p2[153:525, :], 'q_2006_04.png')
    add_question('2006', '第5题', '根轨迹法', img06_p2[525:804, :], 'q_2006_05.png')
    add_question('2006', '第6题', '根轨迹法', img06_p2[804:1001, :], 'q_2006_06.png')
    add_question('2006', '第7题', '时域分析法', img06_p2[1001:1370, :], 'q_2006_07.png')
    add_question('2006', '第8题', '频率响应法', img06_p2[1370:1680, :], 'q_2006_08.png')

    # P3: 九、十、十一、十二、十三(跨P3/P4)
    add_question('2006', '第9题', '频率响应法', img06_p3[168:382, :], 'q_2006_09.png')
    add_question('2006', '第10题', '频率响应法', img06_p3[382:811, :], 'q_2006_10.png')
    add_question('2006', '第11题', '现代控制理论', img06_p3[811:1098, :], 'q_2006_11.png')
    add_question('2006', '第12题', '离散控制系统', img06_p3[1098:1519, :], 'q_2006_12.png')
    # Q13: P3底部[1519:1720] + P4顶部[120:500] 拼接
    q13_full = stitch_images_vertically(img06_p3[1519:1720, :], img06_p4[120:500, :])
    add_question('2006', '第13题', '现代控制理论', q13_full, 'q_2006_13.png')

    # Q14: P4 [510:885]，严格排除【完】与2007封面试卷
    add_question('2006', '第14题', '现代控制理论', img06_p4[510:885, :], 'q_2006_14.png')
    print("  2006年完成：14 道题目")

    # =========================================================================
    # 5. 2007年：9道大题（共九大题，Q6跨P2/P3拼接）
    # =========================================================================
    print(">>> 处理 2007年 (9道大题)...")
    doc2007 = fitz.open(os.path.join(pdf_dir, pdf_map['2007']))
    p1_07 = get_page_image(doc2007, 1)
    p2_07 = get_page_image(doc2007, 2)
    p3_07 = get_page_image(doc2007, 3)

    add_question('2007', '第1题', '控制系统的数学模型', p1_07[160:860, :], 'q_2007_01.png')
    add_question('2007', '第2题', '时域分析法', p1_07[860:1480, :], 'q_2007_02.png')
    add_question('2007', '第3题', '根轨迹法', p2_07[200:530, :], 'q_2007_03.png')
    add_question('2007', '第4题', '频率响应法', p2_07[530:845, :], 'q_2007_04.png')
    add_question('2007', '第5题', '频率响应法', p2_07[845:1105, :], 'q_2007_05.png')
    # Q6: P2[1105:1480] + P3[70:220] (含(1)(2)(3)子小问)
    q6_07 = stitch_images_vertically(p2_07[1105:1480, :], p3_07[70:220, :])
    add_question('2007', '第6题', '频率响应法', q6_07, 'q_2007_06.png')
    add_question('2007', '第7题', '离散控制系统', p3_07[220:520, :], 'q_2007_07.png')
    add_question('2007', '第8题', '现代控制理论', p3_07[520:1055, :], 'q_2007_08.png')
    add_question('2007', '第9题', '现代控制理论', p3_07[1055:1420, :], 'q_2007_09.png')
    print("  2007年完成：9 道题目")

    # =========================================================================
    # 6. 2008年：9道大题（Q3跨P1/P2拼接，Q7跨P2/P3拼接）
    # =========================================================================
    print(">>> 处理 2008年 (9道大题)...")
    doc2008 = fitz.open(os.path.join(pdf_dir, pdf_map['2008']))
    p1_08 = get_page_image(doc2008, 1)
    p2_08 = get_page_image(doc2008, 2)
    p3_08 = get_page_image(doc2008, 3)

    add_question('2008', '第1题', '控制系统的数学模型', p1_08[90:530, :], 'q_2008_01.png')
    add_question('2008', '第2题', '时域分析法', p1_08[530:1115, :], 'q_2008_02.png')
    # Q3: 跨P1/P2拼接
    q3_08 = stitch_images_vertically(p1_08[1115:1450, :], p2_08[70:180, :])
    add_question('2008', '第3题', '根轨迹法', q3_08, 'q_2008_03.png')
    add_question('2008', '第4题', '根轨迹法', p2_08[180:590, :], 'q_2008_04.png')
    add_question('2008', '第5题', '频率响应法', p2_08[590:895, :], 'q_2008_05.png')
    add_question('2008', '第6题', '频率响应法', p2_08[895:1195, :], 'q_2008_06.png')
    # Q7: 跨P2/P3拼接
    q7_08 = stitch_images_vertically(p2_08[1195:1450, :], p3_08[70:160, :])
    add_question('2008', '第7题', '离散控制系统', q7_08, 'q_2008_07.png')
    add_question('2008', '第8题', '现代控制理论', p3_08[160:720, :], 'q_2008_08.png')
    add_question('2008', '第9题', '现代控制理论', p3_08[720:1360, :], 'q_2008_09.png')
    print("  2008年完成：9 道题目")

    # =========================================================================
    # 7. 2009年：9道大题（各题独立在页内）
    # =========================================================================
    print(">>> 处理 2009年 (9道大题)...")
    doc2009 = fitz.open(os.path.join(pdf_dir, pdf_map['2009']))
    p1_09 = get_page_image(doc2009, 1)
    p2_09 = get_page_image(doc2009, 2)
    p3_09 = get_page_image(doc2009, 3)

    add_question('2009', '第1题', '控制系统的数学模型', p1_09[150:730, :], 'q_2009_01.png')
    add_question('2009', '第2题', '时域分析法', p1_09[730:1225, :], 'q_2009_02.png')
    add_question('2009', '第3题', '根轨迹法', p1_09[1225:1600, :], 'q_2009_03.png')
    add_question('2009', '第4题', '根轨迹法', p2_09[105:500, :], 'q_2009_04.png')
    add_question('2009', '第5题', '频率响应法', p2_09[500:875, :], 'q_2009_05.png')
    add_question('2009', '第6题', '频率响应法', p2_09[875:1180, :], 'q_2009_06.png')
    add_question('2009', '第7题', '离散控制系统', p2_09[1180:1620, :], 'q_2009_07.png')
    add_question('2009', '第8题', '现代控制理论', p3_09[55:540, :], 'q_2009_08.png')
    add_question('2009', '第9题', '现代控制理论', p3_09[540:925, :], 'q_2009_09.png')
    print("  2009年完成：9 道题目")

    # =========================================================================
    # 8. 2010年：9道大题（Q3跨P1/P2拼接，Q7跨P2/P3拼接）
    # =========================================================================
    print(">>> 处理 2010年 (9道大题)...")
    doc2010 = fitz.open(os.path.join(pdf_dir, pdf_map['2010']))
    p1_10 = get_page_image(doc2010, 1)
    p2_10 = get_page_image(doc2010, 2)
    p3_10 = get_page_image(doc2010, 3)

    add_question('2010', '第1题', '控制系统的数学模型', p1_10[85:545, :], 'q_2010_01.png')
    add_question('2010', '第2题', '时域分析法', p1_10[545:1060, :], 'q_2010_02.png')
    q3_10 = stitch_images_vertically(p1_10[1060:1500, :], p2_10[55:100, :])
    add_question('2010', '第3题', '根轨迹法', q3_10, 'q_2010_03.png')
    add_question('2010', '第4题', '根轨迹法', p2_10[100:435, :], 'q_2010_04.png')
    add_question('2010', '第5题', '频率响应法', p2_10[435:775, :], 'q_2010_05.png')
    add_question('2010', '第6题', '频率响应法', p2_10[775:1105, :], 'q_2010_06.png')
    q7_10 = stitch_images_vertically(p2_10[1105:1500, :], p3_10[65:190, :])
    add_question('2010', '第7题', '离散控制系统', q7_10, 'q_2010_07.png')
    add_question('2010', '第8题', '现代控制理论', p3_10[190:490, :], 'q_2010_08.png')
    add_question('2010', '第9题', '现代控制理论', p3_10[490:1020, :], 'q_2010_09.png')
    print("  2010年完成：9 道题目")

    # =========================================================================
    # 9. 2011年：9道大题（各题独立在页内）
    # =========================================================================
    print(">>> 处理 2011年 (9道大题)...")
    doc2011 = fitz.open(os.path.join(pdf_dir, pdf_map['2011']))
    p1_11 = get_page_image(doc2011, 1)
    p2_11 = get_page_image(doc2011, 2)
    p3_11 = get_page_image(doc2011, 3)

    add_question('2011', '第1题', '控制系统的数学模型', p1_11[85:510, :], 'q_2011_01.png')
    add_question('2011', '第2题', '时域分析法', p1_11[510:970, :], 'q_2011_02.png')
    add_question('2011', '第3题', '根轨迹法', p1_11[970:1500, :], 'q_2011_03.png')
    add_question('2011', '第4题', '根轨迹法', p2_11[85:485, :], 'q_2011_04.png')
    add_question('2011', '第5题', '频率响应法', p2_11[485:655, :], 'q_2011_05.png')
    add_question('2011', '第6题', '频率响应法', p2_11[655:1305, :], 'q_2011_06.png')
    add_question('2011', '第7题', '离散控制系统', p2_11[1305:1500, :], 'q_2011_07.png')
    add_question('2011', '第8题', '现代控制理论', p3_11[55:505, :], 'q_2011_08.png')
    add_question('2011', '第9题', '现代控制理论', p3_11[505:925, :], 'q_2011_09.png')
    print("  2011年完成：9 道题目")

    # =========================================================================
    # 10. 2012年：10道大题（Q1-Q4扫描卷P0，Q5-Q8在P1，Q9跨P1/P2拼接，Q10在P2排除【完】）
    # =========================================================================
    print(">>> 处理 2012年 (10道大题)...")
    doc2012 = fitz.open(os.path.join(pdf_dir, pdf_map['2012']))
    img12_p0 = get_page_image(doc2012, 0)
    img12_p1 = get_page_image(doc2012, 1)
    img12_p2 = get_page_image(doc2012, 2)

    add_question('2012', '第1题', '控制系统的数学模型', img12_p0[240:1140, :], 'q_2012_01.png')
    add_question('2012', '第2题', '时域分析法', img12_p0[1140:1600, :], 'q_2012_02.png')
    add_question('2012', '第3题', '时域分析法', img12_p0[1600:2070, :], 'q_2012_03.png')
    add_question('2012', '第4题', '根轨迹法', img12_p0[2070:2470, :], 'q_2012_04.png')

    # P1: 五(172px)、六(334px)、七(570px)、八(708px)、九(1082px)
    add_question('2012', '第5题', '频率响应法', img12_p1[172:334, :], 'q_2012_05.png')
    add_question('2012', '第6题', '频率响应法', img12_p1[334:570, :], 'q_2012_06.png')
    add_question('2012', '第7题', '时域分析法', img12_p1[570:708, :], 'q_2012_07.png')
    add_question('2012', '第8题', '离散控制系统', img12_p1[708:1082, :], 'q_2012_08.png')

    # Q9: P1底部[1082:1750] + P2顶部[60:160] (包含第4小问: 状态转移矩阵e^At)
    q9_12 = stitch_images_vertically(img12_p1[1082:1750, :], img12_p2[60:160, :])
    add_question('2012', '第9题', '现代控制理论', q9_12, 'q_2012_09.png')

    # Q10: P2[160:345]，严格避开【完】
    add_question('2012', '第10题', '现代控制理论', img12_p2[160:345, :], 'q_2012_10.png')
    print("  2012年完成：10 道题目")

    # =========================================================================
    # 11. 2013-2021, 2023-2024年：智能大题题号绝对定位 + 跨页溢出自动拼接 (11个年份, 各9题)
    # =========================================================================
    cn_pat = re.compile(r'^\s*([一二三四五六七八九十]+)\s*[、.．\s\uff0c,（\(]')
    modern_years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2023', '2024']

    for yr in modern_years:
        print(f">>> 处理 {yr}年 (9道大题)...")
        doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
        start_p = 0 if yr in ['2019', '2020', '2021', '2023', '2024'] else 1
        
        yr_questions = []  # list of (q_num, img, text)
        
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
                
            img = get_page_image(doc, pno)
            H, W = img.shape[:2]
            
            # 检测顶部页眉基准线（严格剔除学校抬头）
            header_bot_pt = 35.0
            for b in page.get_text("blocks"):
                if b[1] < 120.0 and any(kw in b[4] for kw in ['中国计量', '大学', '学院', '研究生', '考试试题', '招生考试']):
                    header_bot_pt = max(header_bot_pt, b[3] + 8.0)
            header_bot_px = int(header_bot_pt * scale)
            
            # 检测跨页溢出内容（本页第1个题号之前是否存在上一题的子问或图表）
            first_h_pt = heads_on_page[0][0]
            first_h_px = int(first_h_pt * scale)
            
            if pno > start_p and first_h_pt > (header_bot_pt + 20.0) and len(yr_questions) > 0:
                top_cut_y = first_h_px - 14
                if top_cut_y > header_bot_px:
                    top_slice = img[header_bot_px:top_cut_y, :]
                    top_text = page.get_text("text", clip=fitz.Rect(0, header_bot_pt, page.rect.width, first_h_pt - 8.0)).strip()
                    ink_cnt = np.sum(top_slice < 220)
                    if len(top_text) > 0 or ink_cnt > 1200:
                        prev_num, prev_img, prev_txt = yr_questions[-1]
                        merged_img = stitch_images_vertically(prev_img, top_slice)
                        yr_questions[-1] = (prev_num, merged_img, prev_txt + "\n" + top_text)
                        print(f"    P{pno}: 自动垂直缝合跨页内容 ({top_slice.shape[0]}px) 到上一题 {prev_num}")
            
            # 页脚底部检测（严格剔除试卷共X页及【完】标记）
            footer_top_px = int(H * 0.95)
            for b in page.get_text("blocks"):
                txt = b[4].strip()
                if any(kw in txt for kw in ['【完】', '【 完 】', '(完)', '【完 】']):
                    footer_top_px = min(footer_top_px, int(b[1] * scale - 12))
                elif b[1] > page.rect.height * 0.70 and any(kw in txt for kw in ['试卷', '共', '页']):
                    footer_top_px = min(footer_top_px, int(b[1] * scale - 10))
                    
            for i, (yh_pt, h_cn, h_txt) in enumerate(heads_on_page):
                # 题号上方纯白留白恒定切线，严格保证当前截图从自身题号开始
                y_start = int(yh_pt * scale - 14)
                if i == 0 and pno == start_p:
                    y_start = max(header_bot_px, y_start)
                    
                if i < len(heads_on_page) - 1:
                    # 到下一道大题题号上方为止
                    next_yh_pt = heads_on_page[i+1][0]
                    y_end = int(next_yh_pt * scale - 14)
                else:
                    # 本页最后一题延伸到底部
                    y_end = footer_top_px
                    
                q_slice = img[y_start:y_end, :]
                clip_rect = fitz.Rect(0, y_start / scale, page.rect.width, y_end / scale)
                q_txt = page.get_text("text", clip=clip_rect)
                yr_questions.append((f"第{len(yr_questions)+1}题", q_slice, q_txt))
                
        assert len(yr_questions) == 9, f"{yr} 应为 9 道题，实际得到 {len(yr_questions)} 道"
        
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
        for idx, (q_num, q_img, q_txt) in enumerate(yr_questions, 1):
            fb = fallback_map.get(idx, '现代控制理论')
            q_type = classify_text(q_txt, fallback_type=fb)
            add_question(yr, q_num, q_type, q_img, f"q_{yr}_{idx:02d}.png")
        print(f"  {yr}年完成：9 道题目")

    # =========================================================================
    # 生成分类数据并保存 classified_data.js
    # =========================================================================
    all_questions.sort(key=lambda x: (x["type"], x["year_num"], x["id"]))

    js_content = "const classifiedImages = " + json.dumps(all_questions, ensure_ascii=False, indent=4) + ";"
    out_js_path = os.path.join(base_dir, "classified_data.js")
    with open(out_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("\n" + "=" * 60)
    print(f"全部考研真题更新完毕！总计提取并更新题目：{len(all_questions)} 道")
    type_counts = Counter(q["type"] for q in all_questions)
    for cat, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  【{cat}】: {count} 道")
    print(f"配置文件已生成至: {out_js_path}")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    process_all()
