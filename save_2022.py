import pymupdf as fitz
import cv2
import numpy as np
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791639003002_91ca1547.pdf'))
out_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_2022"
os.makedirs(out_dir, exist_ok=True)

for pno in range(len(doc)):
    page = doc[pno]
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    _, buf = cv2.imencode('.png', img)
    buf.tofile(os.path.join(out_dir, f"p_{pno}.png"))
print("Successfully saved 2022 pages with imencode!")
