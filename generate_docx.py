#!/usr/bin/env python3
"""
Generate Single-Column Word (.docx) Manuscript for Elsevier Computers in Biology and Medicine
Author: Vu Minh Anh
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

output_dir = os.path.dirname(os.path.abspath(__file__))
doc = Document()

# Set standard margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Style settings
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(12)
normal_style.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
normal_style.paragraph_format.line_spacing = 1.5
normal_style.paragraph_format.space_after = Pt(6)

def add_title(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    p.paragraph_format.space_after = Pt(12)

def add_heading1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)

def add_heading2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12.5)
    run.font.color.rgb = RGBColor(0x25, 0x63, 0xeb)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)

# Title & Metadata
add_title("4D-CT-Based Tumor Motion Modeling and Quantitative Evaluation of PTV Margins for Lung Radiotherapy Planning")

p_auth = doc.add_paragraph()
p_auth.add_run("Vu Minh Anh").bold = True
p_auth.add_run("*\nFaculty of Information Technology, Ho Chi Minh City University of Industry and Trade (HUIT), Ho Chi Minh City, Vietnam\n*Corresponding Author: mvu103536@gmail.com")
p_auth.paragraph_format.space_after = Pt(16)

# Abstract
add_heading1("Abstract")
p_abs = doc.add_paragraph(
    "Respiratory-induced tumor motion remains a formidable challenge in thoracic radiation therapy, causing substantial "
    "anatomical distortions and dosimetric uncertainty. Commercial treatment planning systems frequently employ closed, "
    "proprietary algorithms with static margin recommendations that fail to reflect patient-specific breathing irregularities. "
    "This study presents a transparent, open-source computational pipeline for spatiotemporal (T, Z, Y, X) lung tumor tracking "
    "and planning target volume (PTV) margin assessment using dynamic 4D-CT simulations. A synthetic digital thorax phantom "
    "calibrated in Hounsfield Units (HU) was generated across ten respiratory phases (T0–T9). Three-dimensional center-of-mass "
    "tracking was performed via spatial moment extraction under three distinct breathing scenarios: regular, deep, and irregular. "
    "Target coverage rates (CR) were empirically quantified for uniform margin expansions (2, 5, 8, 10, and 12 mm) relative to the "
    "end-expiration phase (T5) and benchmarked against the analytical van Herk margin recipe (2.5Σ + 0.7σ) in accordance with ICRU "
    "62/83 and AAPM TG-76/TG-324 recommendations (CR ≥ 95%). Kinematic analysis revealed that tumor excursion was overwhelmingly "
    "dominant along the craniocaudal (Superior–Inferior, SI) axis, exhibiting peak-to-peak amplitudes of 12.00 mm (regular), 22.00 mm "
    "(deep), and 14.58 mm (irregular), compared to lateral (X) and anteroposterior (Y) motions (< 6.1 mm). Under regular breathing, "
    "a 12 mm margin satisfied the ICRU threshold (CR = 98.4%), whereas conventional 5 mm margins failed catastrophically under deep "
    "breathing (CR = 9.5%) and irregular patterns (CR = 52.6%). These findings demonstrate the necessity of patient-specific, "
    "anisotropic margin expansion or active respiratory gating, providing an accessible open-source framework for treatment verification."
)

p_kw = doc.add_paragraph()
p_kw.add_run("Keywords: ").bold = True
p_kw.add_run("4D-CT, Lung Radiotherapy, Respiratory Motion, Centroid Tracking, PTV Margins, van Herk Recipe, AAPM TG-324.")

# 1. Introduction
add_heading1("1. Introduction")
doc.add_paragraph(
    "Lung cancer remains the leading cause of oncological mortality worldwide, accounting for over 1.8 million deaths annually. "
    "External beam radiation therapy (EBRT) serves as a principal curative and palliative modality in non-small cell lung cancer (NSCLC). "
    "The primary technical objective of modern radiotherapy is to deliver an ablative dose to the gross tumor volume (GTV) while "
    "minimizing normal tissue complication probability (NTCP) in adjacent organs at risk (OARs), particularly the functional lung parenchyma, "
    "esophagus, spinal cord, and heart."
)
doc.add_paragraph(
    "However, thoracic radiotherapy is complicated by physiological respiratory motion. As the patient breathes, diaphragmatic contraction "
    "and thoracic expansion induce continuous, quasi-periodic displacements of both the tumor and healthy thoracic structures. Conventional "
    "three-dimensional computed tomography (3D-CT) acquires anatomical data asynchronously relative to the respiratory cycle, creating "
    "substantial motion-blurring artifacts, artificial geometric deformation, and inaccurate volumetric delineation of target boundaries."
)
doc.add_paragraph(
    "To address these limitations, four-dimensional computed tomography (4D-CT) sorts volumetric slices into discrete respiratory phase "
    "bins (typically ten phases, T0 to T9, spanning from peak-inspiration to end-expiration). Despite the clinical availability of 4D-CT, "
    "determining the appropriate Planning Target Volume (PTV) margin remains an empirical challenge. According to ICRU Reports 62 and 83 "
    "and consensus recommendations from AAPM Task Group 76 and Task Group 324, the PTV margin must account for both setup uncertainties and "
    "internal organ motion, ensuring that the prescribed dose envelops at least 95% of the target volume throughout the fraction."
)

# 2. Materials and Methods
add_heading1("2. Materials and Methods")
add_heading2("2.1. Spatiotemporal Digital Thorax Phantom")
doc.add_paragraph(
    "An in-silico 4D-CT digital thorax phantom was synthesized as a four-dimensional tensor V(t, z, y, x), where T = 10 represents the "
    "phase bins (T0 = 0% peak-inspiration, T5 = 50% end-expiration). The volume was calibrated in standard Hounsfield Units (HU) using voxel "
    "spacing (dz, dy, dx) = (2.0 mm, 1.5 mm, 1.5 mm). The phantom encompasses realistic radiological HU assignments: surrounding ambient air "
    "(-1000 HU), thoracic soft-tissue envelope (+30 HU), thoracic spine and posterior rib cage (+650 HU), and bilateral lung parenchyma (-750 HU). "
    "A spherical gross tumor volume (GTV) of radius R0 = 12.0 mm (volume 7.24 cc, +45 HU) was embedded in the lower lobe of the right lung."
)

add_heading2("2.2. Kinematic Respiratory Modeling & Centroid Tracking")
doc.add_paragraph(
    "Tumor motion was simulated using the generalized periodic respiratory model described by Lujan et al. Three clinical breathing patterns "
    "were investigated: Regular breathing, Deep breathing (hyperventilation), and Irregular breathing (tachypneic jitter). Delineation was "
    "performed via Hounsfield density thresholding [-300, 150 HU], and 3D centers of mass were tracked using scipy.ndimage.center_of_mass across "
    "all phases."
)

add_heading2("2.3. PTV Margin Expansion and Target Coverage Evaluation")
doc.add_paragraph(
    "The reference GTV was selected at end-expiration (T5). PTV expansions of 2, 5, 8, 10, and 12 mm were generated via 3D Euclidean Distance "
    "Transform. At each phase, the target coverage rate CR(m, t) was quantified as the volumetric overlap of GTV(t) within PTV(m). "
    "Analytical benchmarking was conducted using the van Herk recipe: M = 2.5Σ + 0.7σ."
)

# 3. Results
add_heading1("3. Results")
doc.add_paragraph(
    "Kinematic evaluation revealed that tumor displacement is overwhelmingly dominant along the craniocaudal (SI, Z) axis due to "
    "diaphragmatic excursion. Table 1 summarizes the kinematic trajectory parameters, and Table 2 presents the empirical PTV coverage rates."
)

# Insert Table 1
doc.add_paragraph("Table 1. Kinematic quantification of lung tumor trajectory parameters across breathing profiles.").bold = True
t1 = doc.add_table(rows=4, cols=5)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Breathing Profile", "LR (X) p2p (mm)", "AP (Y) p2p (mm)", "SI (Z) p2p (mm)", "Max 3D Disp. (mm)"]
for i, h in enumerate(headers):
    t1.rows[0].cells[i].text = h
    t1.rows[0].cells[i].paragraphs[0].runs[0].bold = True

t1_data = [
    ["Regular Breathing", "1.18 ± 0.42", "3.50 ± 1.22", "12.00 ± 4.24", "12.56"],
    ["Deep Breathing", "2.00 ± 0.70", "6.07 ± 2.13", "22.00 ± 7.77", "22.91"],
    ["Irregular Breathing", "1.58 ± 0.57", "4.36 ± 1.58", "14.58 ± 5.30", "13.85"]
]
for r_idx, row in enumerate(t1_data):
    for c_idx, val in enumerate(row):
        t1.rows[r_idx+1].cells[c_idx].text = val

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# Insert Table 2
doc.add_paragraph("Table 2. Empirical PTV target coverage rate (CR%) and compliance with ICRU Report 62/83 (CR ≥ 95%).").bold = True
t2 = doc.add_table(rows=6, cols=6)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
t2_headers = ["Margin (mm)", "Volume (cc)", "Regular (Min CR)", "Regular (Mean CR)", "Deep (Min CR)", "Irregular (Min CR)"]
for i, h in enumerate(t2_headers):
    t2.rows[0].cells[i].text = h
    t2.rows[0].cells[i].paragraphs[0].runs[0].bold = True

t2_data = [
    ["2 mm", "10.0", "38.0%", "72.7%", "2.6%", "31.6%"],
    ["5 mm", "19.2", "59.3%", "86.4%", "9.5%", "52.6%"],
    ["8 mm", "31.4", "79.7%", "95.1%", "21.4%", "71.9%"],
    ["10 mm", "42.2", "91.3%", "98.3%", "32.5%", "85.8%"],
    ["12 mm", "54.4", "98.4% (Pass)", "99.8%", "44.6% (Fail)", "95.6% (Pass)"]
]
for r_idx, row in enumerate(t2_data):
    for c_idx, val in enumerate(row):
        t2.rows[r_idx+1].cells[c_idx].text = val

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# 4. Discussion
add_heading1("4. Discussion")
doc.add_paragraph(
    "Our findings demonstrate that conventional 5 mm margins fail catastrophically under dynamic breathing, delivering as low as "
    "9.5% minimum target coverage during deep breathing. Expanding margins to 12 mm restores coverage for regular and irregular breathers "
    "but increases irradiated normal lung volume by +444%, substantially elevating radiation pneumonitis risks. Consequently, for patients "
    "with excursions > 10 mm, active motion mitigation (e.g., Deep Inspiration Breath Hold or Respiratory Gating per AAPM TG-76/TG-324) "
    "is strictly mandated over geometric margin enlargement."
)

# 5. Conclusion
add_heading1("5. Conclusion")
doc.add_paragraph(
    "This study established an open-source 4D-CT spatiotemporal computational pipeline. The findings underscore the clinical necessity "
    "of patient-specific anisotropic margins and motion-adapted protocols in thoracic radiotherapy planning."
)

# Mandatory Declarations
add_heading1("CRediT Authorship Contribution Statement")
doc.add_paragraph("Vu Minh Anh: Conceptualization, Methodology, Software, Data curation, Formal analysis, Visualization, Writing – original draft.")

add_heading1("Declaration of Competing Interests")
doc.add_paragraph("The author declares that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.")

add_heading1("Declaration of Generative AI and AI-Assisted Technologies")
doc.add_paragraph("During the preparation of this work, the author used generative AI tools to assist with English language polishing and code debugging. After using these tools, the author reviewed and edited the content as needed and takes full responsibility for the content of the published article.")

add_heading1("Funding")
doc.add_paragraph("This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.")

# Save docx
doc_path = os.path.join(output_dir, "manuscript.docx")
doc.save(doc_path)
print(f"[SUCCESS] Word manuscript saved: {doc_path}")
