import pymupdf as fitz
import os, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

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
    p0 = doc[0]
    txt0 = p0.get_text('text').strip()
    is_cover = any(kw in txt0 for kw in ['考生编号', '考生姓名', '报考专业', '考试科目代码']) and ('一、' not in txt0 and '1.' not in txt0 and '一（' not in txt0 and '1、' not in txt0)
    has_q = any(kw in txt0 for kw in ['一、', '一（', '一(', '1.', '1、', '【1】'])
    print(f"{yr}: total_pages={len(doc)}, p0 text_len={len(txt0)}, has_q={has_q}, is_cover={is_cover}")
    if has_q:
        print(f"   p0 sample: {repr(txt0[:120])}")
    elif len(txt0) > 0 and len(txt0) < 300:
        print(f"   p0 sample (short): {repr(txt0[:120])}")
