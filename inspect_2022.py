import fitz, os, cv2
import numpy as np

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
fname = "media_1791639003002_91ca1547.pdf"

doc = fitz.open(os.path.join(pdf_dir, fname))
out_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\debug_2022"
os.makedirs(out_dir, exist_ok=True)

for pno in range(len(doc)):
    page = doc[pno]
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    
    # Draw horizontal grid lines every 50 pixels with y-coordinate label
    grid_img = img.copy()
    for y in range(0, img.shape[0], 50):
        color = (0, 0, 255) if y % 100 == 0 else (200, 200, 200)
        cv2.line(grid_img, (0, y), (img.shape[1], y), color, 1)
        if y % 100 == 0:
            cv2.putText(grid_img, str(y), (10, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
    _, buf = cv2.imencode('.png', grid_img)
    buf.tofile(os.path.join(out_dir, f"page_{pno}_grid.png"))
    print(f"Page {pno} shape: {img.shape}")
