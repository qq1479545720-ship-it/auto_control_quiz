import os, cv2
import numpy as np

# Let's inspect the generated images in test_early to classify 2007-2011
test_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz\test_early"
files = sorted(os.listdir(test_dir))
print(f"Total early images: {len(files)}")
for f in files:
    img = cv2.imread(os.path.join(test_dir, f))
    if img is not None:
        print(f"  {f}: {img.shape[1]}x{img.shape[0]}")
