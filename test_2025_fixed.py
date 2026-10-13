# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2025']))
pix0 = doc[0].get_pixmap(dpi=150)
img0 = np.frombuffer(pix0.samples, dtype=np.uint8).reshape(pix0.height, pix0.width, pix0.n)
if pix0.n == 4: img0 = cv2.cvtColor(img0, cv2.COLOR_RGBA2BGR)

pix1 = doc[1].get_pixmap(dpi=150)
img1 = np.frombuffer(pix1.samples, dtype=np.uint8).reshape(pix1.height, pix1.width, pix1.n)
if pix1.n == 4: img1 = cv2.cvtColor(img1, cv2.COLOR_RGBA2BGR)

out_dir = os.path.join(base_dir, "test_2025_fixed")
os.makedirs(out_dir, exist_ok=True)

def save(img, fname):
    _, buf = cv2.imencode('.png', img)
    buf.tofile(os.path.join(out_dir, fname))

# Q1: Page 0 left col [775:1342, 60:1180]
save(img0[775:1342, 60:1180], "q01.png")
# Q2: Page 0 left col [1342:1545, 60:1180]
save(img0[1342:1545, 60:1180], "q02.png")
# Q3: 跨栏拼接 Page 0 left col 底部 [1545:1625, 60:1180] + Page 0 right col 顶部 [80:965, 1200:2350]
q3_part1 = img0[1545:1625, 60:1180]
q3_part2 = img0[80:965, 1200:2350]
# Pad width so they match
W_target = max(q3_part1.shape[1], q3_part2.shape[1])
p1_padded = np.pad(q3_part1, ((0,0), (0, W_target - q3_part1.shape[1]), (0,0)), constant_values=255)
p2_padded = np.pad(q3_part2, ((0,0), (0, W_target - q3_part2.shape[1]), (0,0)), constant_values=255)
save(np.vstack([p1_padded, p2_padded]), "q03.png")

# Q4: 跨页拼接 Page 0 right col [965:1635, 1200:2350] + Page 1 left col [120:295, 60:1180]
q4_part1 = img0[965:1635, 1200:2350]
q4_part2 = img1[120:295, 60:1180]
W4_target = max(q4_part1.shape[1], q4_part2.shape[1])
p4_1_pad = np.pad(q4_part1, ((0,0), (0, W4_target - q4_part1.shape[1]), (0,0)), constant_values=255)
p4_2_pad = np.pad(q4_part2, ((0,0), (0, W4_target - q4_part2.shape[1]), (0,0)), constant_values=255)
save(np.vstack([p4_1_pad, p4_2_pad]), "q04.png")

# Q5: Page 1 left col [295:830, 60:1180]
save(img1[295:830, 60:1180], "q05.png")
# Q6: Page 1 left col [830:1340, 60:1180]
save(img1[830:1340, 60:1180], "q06.png")
# Q7: Page 1 left col [1340:1640, 60:1180]
save(img1[1340:1640, 60:1180], "q07.png")

print("2025 slices generated.")
