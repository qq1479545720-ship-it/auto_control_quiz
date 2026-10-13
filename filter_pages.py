import fitz
import glob
import os
import json
import re

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"

pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))
image_list = []

for pdf_path in pdfs:
    filename = os.path.basename(pdf_path)
    
    try:
        doc = fitz.open(pdf_path)
        
        # 核心修复：从 PDF 内部正文的第一页提取年份（因为文件名是一串哈希代码，没有年份）
        year = "历年真题"
        for i in range(min(3, len(doc))):
            text = doc[i].get_text("text")
            # 匹配 2000-2029 的年份
            match = re.search(r'(20[0-2]\d)\s*年?', text)
            if match:
                year = match.group(1) + "年"
                break
                
        for i, page in enumerate(doc):
            text = page.get_text("text")
            
            # Filter 1: Blank pages
            if len(text.strip()) < 50:
                continue
            
            # Filter 2: Cover pages
            if i == 0 and ("注意事项" in text or "得分" in text or "试卷" in text or "答题" in text):
                if not ("已知" in text or "求" in text or "传递函数" in text or "如图" in text):
                    continue
            
            img_name = f"{filename[:-4]}_page_{i+1}.png"
            
            image_list.append({
                "year": year,
                "page": i + 1,
                "url": f"paper_images/{img_name}"
            })
    except Exception as e:
        print(f"Error processing {filename}: {e}")

js_content = "const paperImages = " + json.dumps(image_list, ensure_ascii=False, indent=4) + ";"
with open(os.path.join(base_dir, "image_data.js"), "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Successfully re-processed {len(image_list)} valid pages with actual year from text.")
