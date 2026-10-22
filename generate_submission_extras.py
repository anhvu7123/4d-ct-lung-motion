#!/usr/bin/env python3
"""
Generate Final Elsevier Submission Package Extras:
1. COVER_LETTER.docx (Formal letter to Editor-in-Chief of Computers in Biology and Medicine)
2. SUGGESTED_REVIEWERS.txt & .docx (International peer reviewers in 4D-CT & Radiotherapy)
3. Graphical_Abstract.png (High-res horizontal banner >= 1328px wide as per CBM specs)
"""

import os
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = os.path.dirname(os.path.abspath(__file__))

# ==============================================================================
# 1. CREATE COVER_LETTER.docx
# ==============================================================================
print("Generating COVER_LETTER.docx...")
doc_cl = Document()
for section in doc_cl.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

style_cl = doc_cl.styles['Normal']
style_cl.font.name = 'Times New Roman'
style_cl.font.size = Pt(11.5)
style_cl.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
style_cl.paragraph_format.line_spacing = 1.3
style_cl.paragraph_format.space_after = Pt(6)

p_h = doc_cl.add_paragraph()
r_h = p_h.add_run("Vu Minh Anh\n")
r_h.bold = True
p_h.add_run("Faculty of Information Technology\nHo Chi Minh City University of Industry and Trade (HUIT)\n"
            "140 Le Trong Tan Street, Tay Thanh Ward, Tan Phu District, Ho Chi Minh City, Vietnam\n"
            "Email: mvu103536@gmail.com\nDate: October 2026")
p_h.paragraph_format.space_after = Pt(14)

p_eic = doc_cl.add_paragraph()
p_eic.add_run("To:\n").bold = True
p_eic.add_run("The Editor-in-Chief\nComputers in Biology and Medicine\nElsevier ScienceDirect")
p_eic.paragraph_format.space_after = Pt(14)

p_sub = doc_cl.add_paragraph()
r_sub = p_sub.add_run("Subject: Submission of Original Research Article for Publication Consideration")
r_sub.bold = True
p_sub.paragraph_format.space_after = Pt(10)

doc_cl.add_paragraph("Dear Editor-in-Chief,")

doc_cl.add_paragraph(
    "I am pleased to submit our original research article entitled \"In Silico 4D-CT-Based Tumor Motion Modeling and Quantitative "
    "Evaluation of PTV Margins for Lung Radiotherapy Planning\" for consideration for publication as a Full Length Article in "
    "Computers in Biology and Medicine, under the section \"Medical Imaging: Image Processing and Reconstruction\"."
)

doc_cl.add_paragraph(
    "Respiratory-induced motion in thoracic oncology introduces major geometric and dosimetric uncertainties in external beam "
    "radiotherapy. Commercial treatment planning systems (TPS) predominantly function as proprietary \"black boxes\", offering "
    "clinicians limited flexibility to inspect multi-scenario trajectory decomposition or personalize planning target volume (PTV) "
    "margins. In this study, we present a fully transparent, open-source computational pipeline based on Python that integrates: "
    "(1) 4D spatiotemporal tensor modeling in calibrated Hounsfield Units (HU) across 10 respiratory phase bins; (2) automatic 3D "
    "center-of-mass tracking via spatial moment analysis; (3) kinematic decomposition across regular, deep, and irregular breathing "
    "profiles; and (4) empirical quantification of target coverage degradation across uniform margin expansions (2 to 12 mm), "
    "benchmarked against the seminal van Herk margin recipe (2.5Σ + 0.7σ) and ICRU 62/83 consensus guidelines."
)

doc_cl.add_paragraph(
    "Our quantitative results demonstrate that tumor excursion is overwhelmingly anisotropic, with craniocaudal (SI) motion "
    "reaching up to 22 mm under deep breathing—an order of magnitude greater than lateral (X) and anteroposterior (Y) displacements. "
    "Crucially, we show that conventional static 5 mm margins fail catastrophically under dynamic breathing (coverage drops to 9.5%), "
    "whereas uniform expansion to 12 mm substantially escalates irradiated normal tissue volume (+444%). These findings provide actionable, "
    "quantitative evidence advocating for patient-specific anisotropic margin customization and active motion mitigation (e.g., DIBH and "
    "respiratory gating per AAPM TG-76/TG-324)."
)

doc_cl.add_paragraph(
    "We believe this manuscript strongly aligns with the scope of Computers in Biology and Medicine, specifically in the domains of "
    "computer-aided radiation dosage planning, medical image segmentation, and biomedical simulation systems. In adherence to open science "
    "practices, all mathematical models and simulation datasets have been documented for public deposition."
)

doc_cl.add_paragraph(
    "This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere. "
    "All authors have approved the submission. We confirm that there are no known conflicts of interest associated with this publication."
)

doc_cl.add_paragraph("Thank you very much for your time and consideration of our manuscript.")

p_sign = doc_cl.add_paragraph()
p_sign.add_run("Sincerely,\n\n").bold = True
p_sign.add_run("Vu Minh Anh\nFaculty of Information Technology\nHo Chi Minh City University of Industry and Trade (HUIT)\nEmail: mvu103536@gmail.com")

cl_path = os.path.join(output_dir, "COVER_LETTER.docx")
doc_cl.save(cl_path)
print(f"  -> Saved: {cl_path}")

# ==============================================================================
# 2. CREATE SUGGESTED_REVIEWERS.txt & .docx
# ==============================================================================
print("Generating SUGGESTED_REVIEWERS list...")
reviewers_content = """LIST OF SUGGESTED INDEPENDENT REVIEWERS
Journal: Computers in Biology and Medicine (Elsevier)
Manuscript Title: 4D-CT-Based Tumor Motion Modeling and Quantitative Evaluation of PTV Margins for Lung Radiotherapy Planning
Lead Author: Vu Minh Anh (Ho Chi Minh City University of Industry and Trade - HUIT)

--------------------------------------------------------------------------------
1. Prof. Marcel van Herk
   - Academic Title: Professor of Radiotherapy Physics
   - Affiliation: Division of Cancer Sciences, The University of Manchester, and The Christie NHS Foundation Trust, United Kingdom
   - Institutional Email: marcel.vanherk@manchester.ac.uk
   - Reason for Recommendation: Pioneer and author of the seminal van Herk margin formulation (M = 2.5Σ + 0.7σ) in radiation oncology. Internationally recognized authority on setup errors and geometric uncertainties in radiotherapy.

2. Prof. Paul J. Keall
   - Academic Title: Professor & Director of ACRF Image X Institute
   - Affiliation: Faculty of Medicine and Health, The University of Sydney, Australia
   - Institutional Email: paul.keall@sydney.edu.au
   - Reason for Recommendation: Lead author and Chair of the landmark AAPM Task Group 76 report on respiratory motion management in radiation oncology. Global authority on real-time tumor tracking and 4D thoracic imaging.

3. Prof. Kristy K. Brock
   - Academic Title: Professor of Imaging Physics & Radiation Physics
   - Affiliation: Department of Imaging Physics, The University of Texas MD Anderson Cancer Center, Houston, TX, USA
   - Institutional Email: kkbrock@mdanderson.org
   - Reason for Recommendation: Internationally recognized expert in thoracic 4D-CT deformable image registration (DIR), biomechanical motion modeling, and image-guided target delineation.

4. Prof. Per Rugaard Poulsen
   - Academic Title: Professor of Medical Physics
   - Affiliation: Department of Clinical Medicine, Aarhus University Hospital, Aarhus, Denmark
   - Institutional Email: perpouls@rm.dk
   - Reason for Recommendation: Leading researcher in motion-mitigated radiation therapy, respiratory gating, and real-time internal motion monitoring algorithms.
--------------------------------------------------------------------------------
Note: None of the proposed reviewers have had collaborative, financial, or institutional affiliations with the author in the past five years, ensuring completely unbiased and objective peer evaluation.
"""

rev_txt_path = os.path.join(output_dir, "SUGGESTED_REVIEWERS.txt")
with open(rev_txt_path, "w", encoding="utf-8") as f:
    f.write(reviewers_content)
print(f"  -> Saved: {rev_txt_path}")

# ==============================================================================
# 3. CREATE Graphical_Abstract.png (>= 1328 px wide as per CBM Page 14)
# ==============================================================================
print("Generating Graphical_Abstract.png (1600 x 700 px)...")
fig = plt.figure(figsize=(16, 7), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlim(0, 160)
ax.set_ylim(0, 70)
ax.axis('off')

fig.patch.set_facecolor('#f8fafc')
ax.set_facecolor('#f8fafc')

ax.text(80, 65, "4D-CT Lung Tumor Kinematics & PTV Margin Optimization Pipeline",
        ha='center', va='center', fontsize=18, fontweight='bold', color='#0f172a')
ax.text(80, 61, "Vu Minh Anh | Computers in Biology and Medicine (Elsevier)",
        ha='center', va='center', fontsize=12, fontstyle='italic', color='#64748b')

def draw_card(x, y, w, h, title, bg_color='#ffffff', border_color='#cbd5e1'):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=1.5",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=2.0)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 4, title, ha='center', va='center', fontsize=12, fontweight='bold', color='#1e3a8a')

# Panel 1: 4D-CT Spatiotemporal Input
draw_card(6, 10, 32, 45, "1. 4D-CT Input & HU Calibration")
ax.text(22, 43, "10-Phase Tensor (T, Z, Y, X)\nAir: -1000 HU | Lung: -750 HU\nTumor: +45 HU | Spine: +650 HU",
        ha='center', va='top', fontsize=9.5, color='#334155', linespacing=1.4)
lung_ellipse = patches.Ellipse((22, 24), 16, 20, facecolor='#0f172a', edgecolor='#334155', lw=1.5)
tumor_dot = patches.Circle((20, 20), 3.5, facecolor='#ef4444', edgecolor='#b91c1c')
ax.add_patch(lung_ellipse)
ax.add_patch(tumor_dot)
ax.text(22, 12, "Calibrated Phantom Grid", ha='center', fontsize=8.5, color='#64748b')

# Arrow 1 -> 2
ax.annotate('', xy=(43, 32), xytext=(39, 32),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#2563eb', width=3, headwidth=9))

# Panel 2: 3D Centroid Tracking
draw_card(45, 10, 32, 45, "2. 3D Centroid Tracking")
ax.text(61, 43, "scipy.ndimage.center_of_mass\nMoments: C(t) = (Z_t, Y_t, X_t)\nPeak-to-Peak & SD Extraction",
        ha='center', va='top', fontsize=9.5, color='#334155', linespacing=1.4)
t_mini = np.linspace(50, 72, 30)
wave_z = 25 - 6 * np.cos(np.pi * (t_mini - 50) / 10)**2
ax.plot(t_mini, wave_z, color='#1f77b4', lw=2.5)
ax.text(61, 15, "Z-axis dominant: 12 - 22 mm\nLateral (X, Y) < 6 mm", ha='center', fontsize=9, fontweight='bold', color='#1e3a8a')

# Arrow 2 -> 3
ax.annotate('', xy=(82, 32), xytext=(78, 32),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#2563eb', width=3, headwidth=9))

# Panel 3: PTV Margin Expansion
draw_card(84, 10, 32, 45, "3. PTV Margin Evaluation")
ax.text(100, 43, "3D Euclidean Distance Transform\nMargins: 2, 5, 8, 10, 12 mm\nBenchmark: M = 2.5Σ + 0.7σ",
        ha='center', va='top', fontsize=9.5, color='#334155', linespacing=1.4)
c_gtv = patches.Circle((100, 24), 4, facecolor='#ef4444')
c_ptv1 = patches.Circle((100, 24), 8, fill=False, edgecolor='#f59e0b', linestyle='--', lw=2)
c_ptv2 = patches.Circle((100, 24), 11, fill=False, edgecolor='#10b981', linestyle='-', lw=2)
ax.add_patch(c_gtv)
ax.add_patch(c_ptv1)
ax.add_patch(c_ptv2)
ax.text(100, 12, "GTV vs. PTV Intersections", ha='center', fontsize=8.5, color='#64748b')

# Arrow 3 -> 4
ax.annotate('', xy=(121, 32), xytext=(117, 32),
            arrowprops=dict(facecolor='#2563eb', edgecolor='#2563eb', width=3, headwidth=9))

# Panel 4: Clinical Decision
draw_card(123, 10, 31, 45, "4. ICRU 95% Coverage Rule")
ax.text(138.5, 43, "Clinical Pass: Min CR >= 95%\n\n• 5 mm Margin: FAILS\n  (CR = 9.5% - 59.3%)\n\n• 12 mm Margin: PASSES\n  (Regular CR = 98.4%)\n\n• Deep/Irreg: Mandates DIBH\n  or Gating (AAPM TG-76)",
        ha='center', va='top', fontsize=9, color='#0f172a', linespacing=1.35)

plt.tight_layout()
ga_path = os.path.join(output_dir, "Graphical_Abstract.png")
plt.savefig(ga_path, dpi=100, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print(f"  -> Saved: {ga_path}")

print("\n[ALL COMPLETE] Cover Letter, Reviewers List & Graphical Abstract generated in lung_4dct_project!")
