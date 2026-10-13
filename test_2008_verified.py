# -*- coding: utf-8 -*-
import cv2, numpy as np, os

def trim_whitespace(img, padding=15):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # find where gray < 240
    rows = np.where(np.min(gray, axis=1) < 240)[0]
    cols = np.where(np.min(gray, axis=0) < 240)[0]
    if len(rows) == 0 or len(cols) == 0:
        return img
    r0, r1 = max(0, rows[0] - padding), min(img.shape[0], rows[-1] + padding + 1)
    c0, c1 = max(0, cols[0] - padding), min(img.shape[1], cols[-1] + padding + 1)
    return img[r0:r1, c0:c1]

p1 = cv2.imread('debug_07_11/2008_p1.png')
p2 = cv2.imread('debug_07_11/2008_p2.png')
p3 = cv2.imread('debug_07_11/2008_p3.png')

cuts_2008 = {
    1: p1[140:530, :],
    2: p1[530:900, :],
    3: np.vstack([p1[900:1380, :], p2[135:168, :]]),
    4: p2[168:500, :],
    5: p2[500:780, :],
    6: p2[780:1060, :],
    7: np.vstack([p2[1060:1400, :], p3[135:168, :]]),
    8: p3[168:770, :],
    9: p3[770:1120, :],
}

os.makedirs('test_2008_verified', exist_ok=True)
for q, raw_img in cuts_2008.items():
    trimmed = trim_whitespace(raw_img)
    cv2.imwrite(f'test_2008_verified/q_{q:02d}.png', trimmed)
    print(f"2008 Q{q}: raw shape={raw_img.shape} -> trimmed={trimmed.shape}")
