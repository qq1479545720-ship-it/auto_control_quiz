import pymupdf as fitz
import os, sys

pdf_dir = r"C:\Users\啊哈哈\.gemini\antigravity\brain\46c50098-51f1-4527-a086-ce4379ea345a\.user_uploaded"

pdf_map = {
    '2005': 'media_1791638971400_fcd2155a.pdf',
    '2006': 'media_1791638971400_9aa4c2f4.pdf',
    '2007': 'media_1791638971402_48e50a8b.pdf',
    '2008': 'media_1791638971400_fba750cd.pdf',
    '2009': 'media_1791638971400_bc024558.pdf',
    '2010': 'media_1791638977592_4ac36c0b.pdf',
    '2011': 'media_1791638977592_044c77ac.pdf',
    '2012': 'media_1791638977591_76a523d2.pdf',
    '2013': 'media_1791638977591_d34b8c28.pdf',
    '2014': 'media_1791638977592_743cdcf4.pdf',
    '2015': 'media_1791638997981_be48dda9.pdf',
    '2016': 'media_1791638997993_3807f033.pdf',
    '2017': 'media_1791638997993_7f7d8443.pdf',
    '2018': 'media_1791638997993_666c4aa3.pdf',
    '2019': 'media_1791638997981_93c779ac.pdf',
    '2020': 'media_1791639003002_a4998716.pdf',
    '2021': 'media_1791639003001_8c86ce8c.pdf',
    '2022': 'media_1791639003002_91ca1547.pdf',
    '2023': 'media_1791639003003_f8cf5af7.pdf',
    '2024': 'media_1791639003002_fc0c6c39.pdf',
    '2025': 'media_1791639006281_e72ca0ec.pdf'
}

for yr in sorted(pdf_map.keys()):
    doc = fitz.open(os.path.join(pdf_dir, pdf_map[yr]))
    # Check what each page footer says, e.g. "第1页 共X页"
    page_info = []
    for pno in range(len(doc)):
        p = doc[pno]
        txt = p.get_text('text')
        # find "第x页" or "共x页"
        import re
        m = re.search(r'第\s*(\d+)\s*页', txt)
        p_label = f"PageLabel={m.group(1)}" if m else "NoLabel"
        page_info.append(f"p{pno}({p_label})")
    print(f"{yr} (len={len(doc)}): {', '.join(page_info)}")
