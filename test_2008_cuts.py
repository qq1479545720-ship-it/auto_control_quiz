# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2008']))
out_dir = os.path.join(base_dir, "test_2008_cuts")
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

# Q1: Page 1 一、
save(p1[90:530, :], "q01.png")
# Q2: Page 1 二、
save(p1[530:1115, :], "q02.png")
# Q3: Page 1 三、 + Page 2 top
save(np.vstack([p1[1115:1450, :], p2[70:180, :]]), "q03.png")

# Q4: Page 2 四、
save(p2[180:590, :], "q04.png")
# Q5: Page 2 五、
save(p2[590:895, :], "q05.png")
# Q6: Page 2 六、
save(p2[895:1195, :], "q06.png")
# Q7: Page 2 七、 + Page 3 top
save(np.vstack([p2[1195:1450, :], p3[70:160, :]]), "q07.png")

# Q8: Page 3 八、
save(p3[160:720, :], "q08.png")
# Q9: Page 3 九、
save(p3[720:1360, :], "q09.png")

print("2008 test cuts complete.")
