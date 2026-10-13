import pymupdf as fitz
import cv2
import numpy as np
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
test_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_early"
os.makedirs(test_dir, exist_ok=True)

years_early = {
    '2007': {
        1: [92.4, 420.0, 570.0],
        2: [114.3, 228.0, 414.1, 504.9],
        3: [109.0, 252.2, 509.6]
    },
    '2008': {
        1: [45.9, 233.0, 409.6],
        2: [38.2, 187.2, 354.8, 490.1],
        3: [38.2, 316.0]
    },
    '2009': {
        1: [77.1, 304.9, 543.7],
        2: [55.1, 242.7, 424.5, 570.6],
        3: [30.3, 228.6]
    },
    '2010': {
        1: [45.9, 233.0, 481.3],
        2: [50.0, 165.6, 374.9, 535.3],
        3: [38.2, 205.2]
    },
    '2011': {
        1: [45.9, 248.6, 470.0],
        2: [45.6, 237.3, 318.6, 630.5],
        3: [30.0, 247.1]
    }
}

pdf_map = {
    '2007': 'media_1791638971402_48e50a8b.pdf',
    '2008': 'media_1791638971400_fba750cd.pdf',
    '2009': 'media_1791638971400_bc024558.pdf',
    '2010': 'media_1791638977592_4ac36c0b.pdf',
    '2011': 'media_1791638977592_044c77ac.pdf'
}

def get_cuts_for_page(gray, pt_heads, H):
    scale = 150.0 / 72.0
    cuts = []
    # first cut
    y0_target = max(0, int(pt_heads[0] * scale - 15))
    cuts.append(y0_target)
    for yh in pt_heads[1:]:
        yt = int(yh * scale)
        sub = (gray[max(0, yt-30):min(H, yt+5), :] < 220).astype(np.uint8)
        row_sums = np.sum(sub, axis=1)
        best = np.argmin(row_sums)
        cuts.append(max(0, yt-30) + best)
    # bottom cut
    cuts.append(int(H * 0.96))
    return cuts

for yr, pages in years_early.items():
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    total_q = 0
    for pno, heads in pages.items():
        page = doc[pno]
        pix = page.get_pixmap(dpi=150)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cuts = get_cuts_for_page(gray, heads, pix.height)
        for i in range(len(cuts)-1):
            total_q += 1
            sub = img[cuts[i]:cuts[i+1], :]
            _, buf = cv2.imencode('.png', sub)
            buf.tofile(os.path.join(test_dir, f"{yr}_q{total_q:02d}.png"))
    print(f"{yr}: generated {total_q} questions")
