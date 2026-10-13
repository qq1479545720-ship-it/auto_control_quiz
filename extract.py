import fitz
import glob
import json
import os
import re

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))

questions = []

for pdf_path in pdfs:
    filename = os.path.basename(pdf_path)
    
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        
        year = "历年真题"
        for i in range(min(3, len(doc))):
            t = doc[i].get_text("text")
            match = re.search(r'(20[0-2]\d)\s*年?', t)
            if match:
                year = match.group(1) + "年"
                break
                
        for page in doc:
            full_text += page.get_text("text") + "\n"
            
        blocks = re.split(r'\n(?=[一二三四五六七八九十]+、|\d+[\.．、])', full_text)
        
        for block in blocks:
            block = block.strip()
            if len(block) > 60: 
                block = block.replace('\n', '<br>')
                questions.append({
                    "year": year,
                    "type": "未分类(自动提取)",
                    "content": block
                })
    except Exception as e:
        print(f"Error processing {filename}: {e}")

js_content = "const autoQuestionBank = " + json.dumps(questions, ensure_ascii=False, indent=4) + ";"
out_path = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\auto_data.js"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Extracted {len(questions)} questions. Saved to {out_path}")
