import pymupdf as fitz
import cv2
import numpy as np
import os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638977592_743cdcf4.pdf'))

p2 = doc[2]
pix2 = p2.get_pixmap(dpi=150)
img2 = np.frombuffer(pix2.samples, dtype=np.uint8).reshape(pix2.height, pix2.width, pix2.n)
if pix2.n == 4: img2 = cv2.cvtColor(img2, cv2.COLOR_RGBA2BGR)

p3 = doc[3]
pix3 = p3.get_pixmap(dpi=150)
img3 = np.frombuffer(pix3.samples, dtype=np.uint8).reshape(pix3.height, pix3.width, pix3.n)
if pix3.n == 4: img3 = cv2.cvtColor(img3, cv2.COLOR_RGBA2BGR)

scale = 150.0 / 72.0
# Q7 text on Page 2
# y = 524.62 pt * scale = 1092 px
q7_text = img2[int(524.62 * scale - 15):int(pix2.height * 0.94), :]
# Q7 diag on Page 3
q7_diag = img3[int(50 * scale):int(195 * scale), :]

q7_full = np.vstack([q7_text, q7_diag])
out_p = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_2014_q7.png"
_, buf = cv2.imencode('.png', q7_full)
buf.tofile(out_p)
print("Saved 2014 Q7 stitched!")
