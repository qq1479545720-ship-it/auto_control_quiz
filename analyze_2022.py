import pymupdf as fitz
import cv2
import numpy as np
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791639003002_91ca1547.pdf'))

print("=== 2022 Analysis ===")
for pno in range(len(doc)):
    page = doc[pno]
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape
    print(f"Page {pno}: shape {H}x{W}")
    
    # Save preview image for inspection if needed
    # Let's inspect horizontal line sums
    bin_img = (gray < 220).astype(np.uint8)
    # Check left margin 10% to 90%
    sub = bin_img[:, int(W*0.08):int(W*0.92)]
    row_sums = np.sum(sub, axis=1)
    
    # Find zero blocks
    zero_runs = []
    in_zero = False
    start_z = 0
    for r in range(H):
        if row_sums[r] < 3: # nearly blank
            if not in_zero:
                in_zero = True
                start_z = r
        else:
            if in_zero:
                in_zero = False
                zero_runs.append((start_z, r, r - start_z))
    if in_zero:
        zero_runs.append((start_z, H, H - start_z))
        
    print(f"  Zero gaps >= 15px:")
    for sz, ez, length in zero_runs:
        if length >= 15:
            print(f"    Gap: y={sz}..{ez} (h={length}px)")
