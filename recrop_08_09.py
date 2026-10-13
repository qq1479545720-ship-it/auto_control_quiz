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

# 1. 2008
p1_08 = cv2.imread('debug_07_11/2008_p1.png')
p2_08 = cv2.imread('debug_07_11/2008_p2.png')
p3_08 = cv2.imread('debug_07_11/2008_p3.png')

cuts_2008 = {
    1: p1_08[140:590, :],
    2: p1_08[590:955, :],
    3: np.vstack([p1_08[955:1380, :], p2_08[135:168, :]]),
    4: p2_08[168:500, :],
    5: p2_08[500:780, :],
    6: p2_08[780:1060, :],
    7: np.vstack([p2_08[1060:1400, :], p3_08[135:168, :]]),
    8: p3_08[168:770, :],
    9: p3_08[770:1050, :],
}

os.makedirs('fixed_2008_2009', exist_ok=True)
for q, raw_img in cuts_2008.items():
    cleaned = crop_and_clean(raw_img)
    dst = f'fixed_2008_2009/q_2008_{q:02d}.png'
    cv2.imwrite(dst, cleaned)
    print(f"2008 Q{q}: {cleaned.shape}")

# 2. 2009
p1_09 = cv2.imread('debug_07_11/2009_p1.png')
p2_09 = cv2.imread('debug_07_11/2009_p2.png')
p3_09 = cv2.imread('debug_07_11/2009_p3.png')

cuts_2009 = {
    1: p1_09[180:750, :],
    2: p1_09[750:1250, :],
    3: p1_09[1250:1620, :],
    4: p2_09[180:600, :],
    5: p2_09[600:910, :],
    6: p2_09[910:1225, :],
    7: p2_09[1225:1630, :],
    8: p3_09[180:570, :],
    9: p3_09[570:930, :],
}

for q, raw_img in cuts_2009.items():
    cleaned = crop_and_clean(raw_img)
    dst = f'fixed_2008_2009/q_2009_{q:02d}.png'
    cv2.imwrite(dst, cleaned)
    print(f"2009 Q{q}: {cleaned.shape}")
