import pymupdf as fitz
import cv2
import numpy as np
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

# Let's test 2017 Question 3
doc2017 = fitz.open(os.path.join(pdf_dir, 'media_1791638997993_7f7d8443.pdf'))
scale = 150.0 / 72.0

p1 = doc2017[1]
pix1 = p1.get_pixmap(dpi=150)
img1 = np.frombuffer(pix1.samples, dtype=np.uint8).reshape(pix1.height, pix1.width, pix1.n)
if pix1.n == 4: img1 = cv2.cvtColor(img1, cv2.COLOR_RGBA2BGR)

p2 = doc2017[2]
pix2 = p2.get_pixmap(dpi=150)
img2 = np.frombuffer(pix2.samples, dtype=np.uint8).reshape(pix2.height, pix2.width, pix2.n)
if pix2.n == 4: img2 = cv2.cvtColor(img2, cv2.COLOR_RGBA2BGR)

# Q3 starts on P1 at y = 572.9 pt (scale: 1193 px)
q3_part1 = img1[int(572.9 * scale - 15):int(pix1.height * 0.94), :]
# Q3 overflow on P2: y = 50 pt to y = 244.5 pt (scale: 104 px to 509 px)
q3_part2 = img2[int(50 * scale):int(244.5 * scale - 15), :]

q3_full = np.vstack([q3_part1, q3_part2])
out_p = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_2017_q3_stitched.png"
cv2.imencode('.png', q3_full)[1].tofile(out_p)
print("Saved 2017 Q3 stitched!")
