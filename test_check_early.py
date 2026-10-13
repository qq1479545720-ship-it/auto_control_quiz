# -*- coding: utf-8 -*-
import fitz, cv2, numpy as np, os

base_dir = r"C:\Users\啊哈哈\.gemini\antigravity\scratch\auto_control_quiz"
from generate_final_questions import pdf_map, pdf_dir

# Let's inspect early years: 2007, 2008, 2009, 2010, 2011
# Let's see what questions are in each year and whether any image has 2 headings!
