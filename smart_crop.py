import fitz
import glob
import os
import json
import re

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
img_out_dir = os.path.join(base_dir, "question_images")

# 清空旧图
if os.path.exists(img_out_dir):
    for f in os.listdir(img_out_dir):
        os.remove(os.path.join(img_out_dir, f))
os.makedirs(img_out_dir, exist_ok=True)

pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))

def classify(text):
    if any(k in text for k in ['根轨迹', '分离点', '渐近线', '出射角', '入射角']):
        return '根轨迹'
    if any(k in text for k in ['频率', '伯德图', 'Bode', 'bode', '乃氏', 'Nyquist', 'nyquist', '奈奎斯特', '奈氏', '相位裕度', '幅值裕度', '频域', '增益裕度']):
        return '频率特性'
    if any(k in text for k in ['状态空间', '状态方程', '状态转移', '能控', '能观', '可控', '可观', '状态反馈', '极点配置', '能控性', '能观性']):
        return '状态空间'
    if any(k in text for k in ['离散', 'z变换', 'Z变换', 'z 变换', '差分方程', '采样', '零阶保持']):
        return '离散系统'
    if any(k in text for k in ['超调', '调节时间', '峰值时间', '阻尼比', '稳态误差', '阶跃响应', '单位阶跃', '时域', '上升时间', '劳斯', 'Routh', 'routh', '赫尔维茨', 'Hurwitz']):
        return '时域分析'
    if any(k in text for k in ['传递函数', '方框图', '信号流图', '梅逊', 'Mason', '等效', '化简']):
        return '系统建模'
    if any(k in text for k in ['校正', '补偿', '超前', '滞后', 'PID', 'pid']):
        return '系统校正'
    return '综合题'

all_questions = []
global_index = 0

# 需要跳过的页面关键词
SKIP_KEYWORDS = ['注意事项', '答题须知', '密封线', '装订线', '座位号']

for pdf_path in sorted(pdfs):
    filename = os.path.basename(pdf_path)
    
    try:
        doc = fitz.open(pdf_path)
        
        # 从内容中提取年份
        year = "历年"
        for i in range(min(3, len(doc))):
            t = doc[i].get_text("text")
            match = re.search(r'(20[0-2]\d)\s*[年\-]?', t)
            if match:
                year = match.group(1)
                break
        
        for page_idx, page in enumerate(doc):
            text = page.get_text("text").strip()
            
            # 跳过空白页（文字太少）
            if len(text) < 30:
                continue
            
            # 跳过纯封面/说明页：第一页且只有说明性文字没有题目内容
            is_cover = False
            if page_idx == 0:
                has_question_content = any(k in text for k in ['已知', '求', '传递函数', '如图', '画出', '证明', '设系统', '设单位', '试求', '绘制', '判断', '计算'])
                has_skip_content = any(k in text for k in SKIP_KEYWORDS)
                if has_skip_content and not has_question_content:
                    is_cover = True
            
            if is_cover:
                continue
            
            # 整页高清渲染（200 DPI）
            mat = fitz.Matrix(200/72, 200/72)
            pix = page.get_pixmap(matrix=mat)
            
            q_type = classify(text)
            global_index += 1
            img_name = f"q_{year}_{global_index:04d}.png"
            out_path = os.path.join(img_out_dir, img_name)
            pix.save(out_path)
            
            all_questions.append({
                "id": global_index,
                "year": year + "年",
                "type": q_type,
                "url": f"question_images/{img_name}"
            })
                    
    except Exception as e:
        print(f"Error processing {filename}: {e}")

# 按类型和年份排序
all_questions.sort(key=lambda x: (x["type"], x["year"], x["id"]))

js_content = "const classifiedImages = " + json.dumps(all_questions, ensure_ascii=False, indent=4) + ";"
with open(os.path.join(base_dir, "classified_data.js"), "w", encoding="utf-8") as f:
    f.write(js_content)

from collections import Counter
type_counts = Counter(q["type"] for q in all_questions)
print(f"\n===== 完成 =====")
print(f"共生成 {len(all_questions)} 张完整页面图片")
for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c} 页")
