import fitz
import glob
import os
import json

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
img_out_dir = os.path.join(base_dir, "paper_images")
os.makedirs(img_out_dir, exist_ok=True)

pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))

image_list = []

for pdf_path in pdfs:
    filename = os.path.basename(pdf_path)
    try:
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            # Render page to image at 150 DPI for good readability
            pix = page.get_pixmap(dpi=150)
            img_name = f"{filename[:-4]}_page_{i+1}.png"
            out_path = os.path.join(img_out_dir, img_name)
            pix.save(out_path)
            
            # Simple heuristic for year
            import re
            year_match = re.search(r'(20\d{2})', filename)
            year = year_match.group(1) + "年" if year_match else "真题"
            
            image_list.append({
                "year": year,
                "page": i + 1,
                "url": f"paper_images/{img_name}"
            })
    except Exception as e:
        print(f"Error rendering {filename}: {e}")

js_content = "const paperImages = " + json.dumps(image_list, ensure_ascii=False, indent=4) + ";"
with open(os.path.join(base_dir, "image_data.js"), "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Generated {len(image_list)} page images.")
