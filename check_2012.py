import pymupdf as fitz
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"
doc = fitz.open(os.path.join(pdf_dir, 'media_1791638977591_76a523d2.pdf'))
print("2012 total pages:", len(doc))
for pno in range(len(doc)):
    page = doc[pno]
    txt = page.get_text('text')
    print(f"Page {pno}: text length {len(txt)}")
    pix = page.get_pixmap(dpi=150)
    print(f"  Pix size: {pix.width}x{pix.height}")
    if len(txt) == 0:
        # maybe it's an image?
        print("  Checking images in page:")
        img_list = page.get_images()
        print(f"  Image count: {len(img_list)}")
