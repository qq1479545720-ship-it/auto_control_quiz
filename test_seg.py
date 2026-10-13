import pymupdf as fitz
import cv2
import numpy as np
import os, re, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
test_out = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_seg"
os.makedirs(test_out, exist_ok=True)

def find_best_cut(gray, y_target, search_up=35, search_down=5):
    # Find the row with minimum ink density in [y_target - search_up, y_target + search_down]
    H, W = gray.shape
    y_min = max(0, int(y_target - search_up))
    y_max = min(H, int(y_target + search_down))
    sub = (gray[y_min:y_max, int(W*0.08):int(W*0.92)] < 220).astype(np.uint8)
    row_sums = np.sum(sub, axis=1)
    # find min
    best_offset = np.argmin(row_sums)
    return y_min + best_offset

# Let's test on 2015 Page 1 (which had 4 questions merged into 1 previously!)
doc2015 = fitz.open(os.path.join(pdf_dir, 'media_1791638997981_be48dda9.pdf'))
p1 = doc2015[1]
pix = p1.get_pixmap(dpi=150)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
if pix.n == 4:
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Headings in 2015 P1:
# y = 58.07, 291.29, 413.57, 575.27 (pt)
scale = 150.0 / 72.0
pt_heads = [58.07, 291.29, 413.57, 575.27]
y_img_heads = [h * scale for h in pt_heads]

# Find cuts
cuts = []
# top cut for Q1
cuts.append(find_best_cut(gray, y_img_heads[0] - 5, search_up=25, search_down=5))
for yh in y_img_heads[1:]:
    cuts.append(find_best_cut(gray, yh - 10, search_up=25, search_down=5))
# bottom cut for Q4: find content end or footer
cuts.append(int(pix.height * 0.94))

print("2015 P1 Cuts:", cuts)
for i in range(len(cuts) - 1):
    sub = img[cuts[i]:cuts[i+1], :]
    _, buf = cv2.imencode('.png', sub)
    buf.tofile(os.path.join(test_out, f"2015_p1_q{i+1}.png"))
    print(f"  Q{i+1}: height = {cuts[i+1] - cuts[i]}px")
