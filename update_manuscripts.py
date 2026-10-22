#!/usr/bin/env python3
"""
Update personalized metadata across all manuscript files
Author: Vu Minh Anh
Affiliation: Faculty of Information Technology, Ho Chi Minh City University of Industry and Trade
Email: mvu103536@gmail.com
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

output_dir = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------
# 1. Update manuscript.tex
# ------------------------------------------------------------------------------
tex_path = os.path.join(output_dir, "manuscript.tex")
with open(tex_path, "r", encoding="utf-8") as f:
    tex_content = f.read()

# Replace email and affiliation
tex_content = tex_content.replace(
    r"\ead{minhanh.vu@univ-example.edu.vn}",
    r"\ead{mvu103536@gmail.com}"
)
old_affil = (
    r"\affiliation[inst1]{organization={Department of Biomedical Engineering, Faculty of Applied Sciences}," "\n"
    r"            addressline={University Campus}," "\n"
    r"            city={Ho Chi Minh City}," "\n"
    r"            country={Vietnam}}"
)
new_affil = (
    r"\affiliation[inst1]{organization={Faculty of Information Technology, Ho Chi Minh City University of Industry and Trade}," "\n"
    r"            addressline={140 Le Trong Tan Street, Tay Thanh Ward, Tan Phu District}," "\n"
    r"            city={Ho Chi Minh City}," "\n"
    r"            country={Vietnam}}"
)
tex_content = tex_content.replace(old_affil, new_affil)

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(tex_content)
print("[SUCCESS] manuscript.tex updated.")

# ------------------------------------------------------------------------------
# 2. Re-generate manuscript.docx with exact details
# ------------------------------------------------------------------------------
import generate_docx
print("[SUCCESS] manuscript.docx updated.")

# ------------------------------------------------------------------------------
# 3. Re-generate manuscript.pdf with exact details
# ------------------------------------------------------------------------------
pdf_gen_script = os.path.join(output_dir, "build_pdf.py")
with open(pdf_gen_script, "r", encoding="utf-8") as f:
    pdf_code = f.read()

pdf_code = pdf_code.replace(
    "minhanh.vu@univ-example.edu.vn",
    "mvu103536@gmail.com"
)
pdf_code = pdf_code.replace(
    "Department of Biomedical Engineering, Faculty of Applied Sciences",
    "Faculty of Information Technology, Ho Chi Minh City University of Industry and Trade"
)

with open(pdf_gen_script, "w", encoding="utf-8") as f:
    f.write(pdf_code)

import build_pdf
print("[SUCCESS] manuscript.pdf rebuilt.")
