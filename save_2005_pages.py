import pymupdf as fitz
import cv2, os
import numpy as np

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638971400_fcd2155a.pdf'))
for pno in [2, 3]:
    pix = doc[pno].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    cv2.imencode('.png', img)[1].tofile(rf"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_2005_p{pno}.png")
print("Saved 2005 pages 2 & 3")
