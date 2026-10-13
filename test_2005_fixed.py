# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2005']))
scale = 150.0 / 72.0

p3 = doc[3].get_pixmap(dpi=150)
img3 = np.frombuffer(p3.samples, dtype=np.uint8).reshape(p3.height, p3.width, p3.n)
if p3.n == 4: img3 = cv2.cvtColor(img3, cv2.COLOR_RGBA2BGR)

p4 = doc[4].get_pixmap(dpi=150)
img4 = np.frombuffer(p4.samples, dtype=np.uint8).reshape(p4.height, p4.width, p4.n)
if p4.n == 4: img4 = cv2.cvtColor(img4, cv2.COLOR_RGBA2BGR)

out_dir = os.path.join(base_dir, "test_2005_fixed")
os.makedirs(out_dir, exist_ok=True)

def save(img, fname):
    _, buf = cv2.imencode('.png', img)
    buf.tofile(os.path.join(out_dir, fname))

q8 = img3[350:520, :]
q9 = img3[575:965, :]
q10 = img3[965:1305, :]
q11 = img3[1305:1480, :]
q12 = np.vstack([img3[1485:1560, :], img4[140:400, :]])

save(q8, "q8.png")
save(q9, "q9.png")
save(q10, "q10.png")
save(q11, "q11.png")
save(q12, "q12.png")
print("Saved 2005 test images successfully with buf.tofile.")
