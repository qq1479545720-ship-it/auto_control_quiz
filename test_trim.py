import pymupdf as fitz
import cv2
import numpy as np
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

def find_content_bottom(gray, y_start, max_y):
    # Scan downwards from y_start
    # Find the last row with ink before a huge blank gap or footer
    sub = (gray[y_start:max_y, :] < 220).astype(np.uint8)
    row_sums = np.sum(sub, axis=1)
    
    # scan for large blank runs >= 60px
    blank_cnt = 0
    last_ink = 0
    for r in range(len(row_sums)):
        if row_sums[r] > 3:
            last_ink = r
            blank_cnt = 0
        else:
            blank_cnt += 1
            if blank_cnt >= 60:
                # content ended at last_ink!
                return y_start + last_ink + 25
    return min(gray.shape[0], y_start + last_ink + 25)

# Test on 2019 Page 3 (Q9)
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638997981_93c779ac.pdf'))
p3 = doc[3]
pix = p3.get_pixmap(dpi=150)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bot = find_content_bottom(gray, 90, int(pix.height * 0.94))
print(f"2019 Q9 start=90, bot={bot}, height={bot - 90}px")

sub = img[90:bot, :]
_, buf = cv2.imencode('.png', sub)
out_p = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_q9_trimmed.png"
buf.tofile(out_p)
print("Saved trimmed Q9!")
