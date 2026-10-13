import os, json, sys
from PIL import Image

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
img_dir = os.path.join(base_dir, "question_images")

with open(os.path.join(base_dir, "classified_data.js"), "r", encoding="utf-8") as f:
    c = f.read().replace("const classifiedImages = ", "").rstrip(";")
    data = json.loads(c)

print(f"Total questions in JS: {len(data)}")

height_issues = []
missing_files = []

for q in data:
    fpath = os.path.join(base_dir, q['url'].replace('/', os.sep))
    if not os.path.exists(fpath):
        missing_files.append(q['url'])
        continue
    with Image.open(fpath) as img:
        w, h = img.size
        if h < 100:
            height_issues.append((q['year'], q['q_num'], f"Too small: {w}x{h}"))
        elif h > 1100:
            height_issues.append((q['year'], q['q_num'], f"Very tall: {w}x{h}"))

print(f"Missing image files: {len(missing_files)}")
print(f"Height warnings (too small < 100px or very tall > 1100px): {len(height_issues)}")
for hw in height_issues:
    print("  ", hw)

print("\nAudit completed!")
