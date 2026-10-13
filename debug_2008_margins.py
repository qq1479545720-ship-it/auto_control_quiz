# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2008']))

def get_page(pno):
    p = doc[pno]
    pix = p.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    return img

p1 = get_page(1) # H=1519, W=1075
p2 = get_page(2)
p3 = get_page(3)

print("Page shapes:", p1.shape, p2.shape, p3.shape)

# Let's inspect the exact lines / text at specific ranges
# Page 1:
# Top header ends where? Let's check y from 0 to 200 on P1
# Footer starts where? Let's check y from 1400 to 1519 on P1, P2, P3
for pno, pimg in [(1, p1), (2, p2), (3, p3)]:
    # Save top 200 and bottom 150
    cv2.imwrite(f"debug_2008_p{pno}_top.png", pimg[:200, :])
    cv2.imwrite(f"debug_2008_p{pno}_bot.png", pimg[-150:, :])

print("Saved top and bot debug images for 2008.")
