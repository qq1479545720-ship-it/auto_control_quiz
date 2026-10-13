import pymupdf as fitz
import cv2
import numpy as np
import os

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638977591_76a523d2.pdf'))
p0 = doc[0]
pix = p0.get_pixmap(dpi=150)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
if pix.n == 4:
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
H, W = gray.shape

# Let's inspect rows
bin_img = (gray < 220).astype(np.uint8)
row_sums = np.sum(bin_img[:, int(W*0.1):int(W*0.9)], axis=1)

# Find blank regions
zero_runs = []
in_z = False
sz = 0
for r in range(H):
    if row_sums[r] < 2:
        if not in_z:
            in_z = True
            sz = r
    else:
        if in_z:
            in_z = False
            if r - sz >= 10:
                zero_runs.append((sz, r, r - sz))
print("2012 P0 blank runs >= 10px (at 150 DPI, H=%d):" % H)
for sz, ez, l in zero_runs:
    print(f"  y={sz}..{ez} (h={l}px)")
