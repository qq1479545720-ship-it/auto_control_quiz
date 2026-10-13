# -*- coding: utf-8 -*-
import fitz, os, cv2, numpy as np

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2012']))
print(f"2012 has {len(doc)} pages")
scale = 150.0 / 72.0

out_dir = os.path.join(base_dir, "test_2012_fixed")
os.makedirs(out_dir, exist_ok=True)

def save(img, fname):
    _, buf = cv2.imencode('.png', img)
    buf.tofile(os.path.join(out_dir, fname))

# Page 0 (Q1-Q4)
p0 = doc[0]
pix0 = p0.get_pixmap(dpi=150)
img0 = np.frombuffer(pix0.samples, dtype=np.uint8).reshape(pix0.height, pix0.width, pix0.n)
if pix0.n == 4: img0 = cv2.cvtColor(img0, cv2.COLOR_RGBA2BGR)

save(img0[240:1140, :], "q01.png")
save(img0[1140:1600, :], "q02.png")
save(img0[1600:2070, :], "q03.png")
save(img0[2070:2470, :], "q04.png")

# Page 1 (Q5-Q9)
p1 = doc[1]
for b in p1.get_text('blocks'):
    if b[4].strip() and b[0] < 120:
        print(f"P1: y={b[1]:.1f}-{b[3]:.1f}: {b[4][:30]!r}")

# Page 2 (Q10)
p2 = doc[2]
for b in p2.get_text('blocks'):
    if b[4].strip() and b[0] < 120:
        print(f"P2: y={b[1]:.1f}-{b[3]:.1f}: {b[4][:30]!r}")
