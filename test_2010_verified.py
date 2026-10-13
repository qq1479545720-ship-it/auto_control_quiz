# -*- coding: utf-8 -*-
import cv2, numpy as np, os

def crop_and_clean(img, pad=15):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows = np.where(np.min(gray, axis=1) < 240)[0]
    cols = np.where(np.min(gray, axis=0) < 240)[0]
    if len(rows) == 0 or len(cols) == 0:
        return img
    r0, r1 = rows[0], rows[-1] + 1
    c0, c1 = cols[0], cols[-1] + 1
    cropped = img[r0:r1, c0:c1]
    padded = cv2.copyMakeBorder(cropped, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return padded

p1 = cv2.imread('debug_07_11/2010_p1.png')
p2 = cv2.imread('debug_07_11/2010_p2.png')
p3 = cv2.imread('debug_07_11/2010_p3.png')

cuts_2010 = {
    1: p1[140:590, :],
    2: p1[590:1110, :],
    3: np.vstack([p1[1110:1480, :], p2[118:160, :]]),
    4: p2[158:538, :],
    5: p2[538:800, :],
    6: p2[800:1150, :],
    7: np.vstack([p2[1150:1480, :], p3[130:180, :]]),
    8: p3[180:530, :],
    9: p3[530:1100, :],
}

os.makedirs('test_2010_verified', exist_ok=True)
for q, raw_img in cuts_2010.items():
    cleaned = crop_and_clean(raw_img)
    cv2.imwrite(f'test_2010_verified/q_{q:02d}.png', cleaned)
    print(f"2010 Q{q}: raw shape={raw_img.shape} -> cleaned={cleaned.shape}")
