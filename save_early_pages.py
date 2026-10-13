# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

for yr in ['2008', '2009', '2010', '2011']:
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    out_yr_dir = os.path.join(base_dir, f"pages_{yr}")
    os.makedirs(out_yr_dir, exist_ok=True)
    for pno in range(1, len(doc)):
        page = doc[pno]
        pix = page.get_pixmap(dpi=150)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        _, buf = cv2.imencode('.png', img)
        buf.tofile(os.path.join(out_yr_dir, f"page_{pno}.png"))
    print(f"{yr}: saved {len(doc)-1} pages to pages_{yr}")
