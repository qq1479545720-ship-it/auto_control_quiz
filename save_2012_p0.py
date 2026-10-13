import pymupdf as fitz
import cv2
import numpy as np
import os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638977591_76a523d2.pdf'))
p0 = doc[0]
pix = p0.get_pixmap(dpi=100)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
if pix.n == 4:
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
_, buf = cv2.imencode('.png', img)
out_path = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_2012_p0.png"
buf.tofile(out_path)
print("Saved 2012 p0")
