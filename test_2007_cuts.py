# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2007']))
out_dir = os.path.join(base_dir, "test_2007_cuts")
os.makedirs(out_dir, exist_ok=True)

def get_page(pno):
    p = doc[pno]
    pix = p.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    return img

def save(img, fname):
    _, buf = cv2.imencode('.png', img)
    buf.tofile(os.path.join(out_dir, fname))

p1 = get_page(1)
p2 = get_page(2)
p3 = get_page(3)

# Q1: Page 1 [160:860]
save(p1[160:860, :], "q01.png")
# Q2: Page 1 [860:1480]
save(p1[860:1480, :], "q02.png")

# Q3: Page 2 [200:530]
save(p2[200:530, :], "q03.png")
# Q4: Page 2 [530:845]
save(p2[530:845, :], "q04.png")
# Q5: Page 2 [845:1105]
save(p2[845:1105, :], "q05.png")
# Q6: Page 2 [1105:1480] + Page 3 [70:220]
save(np.vstack([p2[1105:1480, :], p3[70:220, :]]), "q06.png")

# Q7: Page 3 [220:520]
save(p3[220:520, :], "q07.png")
# Q8: Page 3 [520:1055]
save(p3[520:1055, :], "q08.png")
# Q9: Page 3 [1055:1420]
save(p3[1055:1420, :], "q09.png")

print("2007 test cuts complete.")
