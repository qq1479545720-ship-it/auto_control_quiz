# -*- coding: utf-8 -*-
import fitz, os, cv2
import numpy as np

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map

doc = fitz.open(os.path.join(pdf_dir, pdf_map['2022']))
cuts_2022 = {
    0: [
        (472, 962, '第1题', '控制系统的数学模型'),
        (962, 1440, '第2题', '时域分析法')
    ],
    1: [
        (115, 680, '第3题', '时域分析法'),
        (680, 975, '第4题', '根轨迹法'),
        (975, 1210, '第5题', '频率响应法'),
        (1210, 1470, '第6题', '频率响应法')
    ],
    2: [
        (115, 518, '第7题', '离散控制系统'),
        (518, 905, '第8题', '现代控制理论'),
        (905, 1170, '第9题', '现代控制理论')
    ]
}

test_out = os.path.join(base_dir, "test_2022_cuts")
os.makedirs(test_out, exist_ok=True)

cnt = 0
for pno in [0, 1, 2]:
    page = doc[pno]
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    for y0, y1, q_num, q_type in cuts_2022[pno]:
        cnt += 1
        sub = img[y0:y1, :]
        _, buf = cv2.imencode('.png', sub)
        buf.tofile(os.path.join(test_out, f"q_{cnt:02d}.png"))
        print(f"2022 Q{cnt}: pno={pno}, [{y0}:{y1}], size={sub.shape}")

print("2022 slices generated successfully.")
