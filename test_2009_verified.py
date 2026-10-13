# -*- coding: utf-8 -*-
import cv2, numpy as np, os

def trim_whitespace(img, padding=15):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows = np.where(np.min(gray, axis=1) < 240)[0]
    cols = np.where(np.min(gray, axis=0) < 240)[0]
    if len(rows) == 0 or len(cols) == 0:
        return img
    r0, r1 = max(0, rows[0] - padding), min(img.shape[0], rows[-1] + padding + 1)
    c0, c1 = max(0, cols[0] - padding), min(img.shape[1], cols[-1] + padding + 1)
    return img[r0:r1, c0:c1]

p1 = cv2.imread('debug_07_11/2009_p1.png')
p2 = cv2.imread('debug_07_11/2009_p2.png')
p3 = cv2.imread('debug_07_11/2009_p3.png')

cuts_2009 = {
    1: p1[180:680, :],
    2: p1[680:1250, :],
    3: p1[1250:1620, :],
    4: p2[180:600, :],
    5: p2[600:910, :],
    6: p2[910:1210, :],
    7: p2[1210:1630, :],
    8: p3[180:570, :],
    9: p3[570:1000, :],
}

os.makedirs('test_2009_verified', exist_ok=True)
for q, raw_img in cuts_2009.items():
    trimmed = trim_whitespace(raw_img)
    cv2.imwrite(f'test_2009_verified/q_{q:02d}.png', trimmed)
    print(f"2009 Q{q}: raw shape={raw_img.shape} -> trimmed={trimmed.shape}")
