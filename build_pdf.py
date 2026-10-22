#!/usr/bin/env python3
"""
Publication PDF Generator for lung_4dct_project
Generates full publication-grade manuscript.pdf using ReportLab
Author: Vu Minh Anh (HUIT)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)

def generate_pdf(output_dir="/Users/carwyn/Desktop/lung_4dct_project"):
    pdf_path = os.path.join(output_dir, "manuscript.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    )
    
    author_style = ParagraphStyle(
        'AuthorStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1e293b')
    )
    
    affil_style = ParagraphStyle(
        'AffilStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=14,
        spaceAfter=6
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2563eb'),
        spaceBefore=10,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=7
    )
    
    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569'),
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=10
    )
    
    ref_style = ParagraphStyle(
        'RefStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=15,
        firstLineIndent=-15,
        spaceAfter=4
    )
    
    story = []
    
    # Title & Authorship
    story.append(Paragraph("In Silico 4D-CT-Based Tumor Motion Modeling and Quantitative Evaluation of PTV Margins for Lung Radiotherapy Planning", title_style))
    story.append(Paragraph("Vu Minh Anh<sup>*</sup>", author_style))
    story.append(Paragraph(
        "Faculty of Information Technology, Ho Chi Minh City University of Industry and Trade (HUIT), Ho Chi Minh City, Vietnam<br/>"
        "<sup>*</sup>Corresponding Author: mvu103536@gmail.com | Target Journal: <i>Computers in Biology and Medicine</i> (Elsevier)",
        affil_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))
    
    # Abstract Box
    abs_title_style = ParagraphStyle('AbsT', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor('#0f172a'))
    abs_body_style = ParagraphStyle('AbsB', fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=colors.HexColor('#334155'))
    
    abs_text = (
        "<b>Abstract:</b> Target motion during thoracic radiation therapy induces spatial misalignment between planned beam apertures and mobile tumor volumes. "
        "Current commercial treatment planning systems (TPS) utilize proprietary margin expansion modules that often treat intrafractional motion as an isotropic uncertainty. "
        "In this in silico study, we developed an open-source Python computational pipeline to track 3D tumor centroid trajectories across ten-phase 4D-CT volumes and "
        "quantify target coverage under uniform planning target volume (PTV) margin expansions using a synthetic digital thorax phantom. A calibrated spatiotemporal thorax tensor "
        "(T, Z, Y, X) with voxel spacing of 2.0 × 1.5 × 1.5 mm<sup>3</sup> was synthesized across respiratory phases T0 to T9. Solid tumor volumes were segmented within an "
        "anatomically isolated pulmonary region of interest via intensity thresholding (-300 to +150 HU) and tracked using spatial moments across regular, deep, and irregular breathing patterns. "
        "Empirical target coverage rates (CR) for margins of 2, 5, 8, 10, and 12 mm were benchmarked against the analytical van Herk formula (2.5Σ + 0.7σ) and ICRU 62/83 consensus "
        "criteria (CR ≥ 95%). Tumor excursion was dominated by craniocaudal displacement, with peak-to-peak amplitudes of 12.00 mm (regular), 22.00 mm (deep), and 14.58 mm (irregular), "
        "whereas lateral and anteroposterior excursions remained below 6.07 mm. Under regular respiration, a 12 mm margin achieved 98.4% minimum coverage. However, the standard 5 mm "
        "clinical margin exhibited severe geometric miss under deep (CR = 9.5%) and irregular breathing (CR = 52.6%). These quantitative findings confirm that uniform 3D margin "
        "expansions are suboptimal for tumors with craniocaudal excursions exceeding 10 mm, demonstrating the necessity of patient-specific anisotropic margins or active motion mitigation "
        "techniques consistent with AAPM Task Group 76 guidelines.<br/><br/>"
        "<b>Keywords:</b> 4D-CT, Lung Radiotherapy, Intrafraction Motion, In Silico Modeling, Centroid Tracking, PTV Margins, van Herk Recipe, AAPM TG-76."
    )
    
    abs_table = Table([[Paragraph(abs_text, abs_body_style)]], colWidths=[504])
    abs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 10))
    
    # 1. Introduction
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "Geometric accuracy in thoracic external beam radiotherapy is fundamentally compromised by intrafractional respiratory motion. "
        "Contraction of the diaphragm and expansion of the thoracic cage induce substantial time-dependent displacements of lung parenchyma and embedded lesions. "
        "As detailed in the American Association of Physicists in Medicine (AAPM) Task Group 76 report [1], tumor motion exceeding 5 mm along any Cartesian axis "
        "demands explicit motion management to mitigate treatment-related toxicity and prevent tumor underdosing. In modern stereotactic body radiation therapy (SBRT), "
        "where fractional doses often exceed 10 Gy, unmanaged target excursion leads to steep dosimetric penalties at field boundaries [2, 3].",
        body_style
    ))
    story.append(Paragraph(
        "Conventional static three-dimensional computed tomography (3D-CT) acquisition captures arbitrary snapshots of breathing anatomy, resulting in motion-blurring "
        "artifacts, artificial volume elongation, and significant misestimation of gross tumor volume (GTV) boundaries [4, 5]. Four-dimensional computed tomography (4D-CT) "
        "resolves this temporal ambiguity by sorting projection data into discrete respiratory phase bins (typically 10 phases from peak-inhalation T0 to end-exhalation T5) "
        "correlated with an external respiratory surrogate [6, 7]. Advanced 4D-CT reconstruction methods, such as maximum intensity projection (MIP), allow the generation "
        "of an internal target volume (ITV) encompassing full respiratory excursion [8, 9].",
        body_style
    ))
    story.append(Paragraph(
        "Despite the clinical availability of 4D-CT, standardizing the planning target volume (PTV) margin from internal target boundaries remains challenging. "
        "According to ICRU Reports 62 and 83, the PTV must compensate for both internal physiological variation and setup uncertainties to deliver at least 95% "
        "of the prescribed dose to the target [10, 11]. The analytical recipe developed by van Herk et al. (M = 2.5Σ + 0.7σ) provides a statistical population model "
        "ensuring 95% dose coverage in 90% of patients [12, 13]. Similarly, Stroom et al. proposed coverage probability formalisms for margin derivation [14]. "
        "However, commercial treatment planning systems (TPS) operate as closed, proprietary platforms, restricting clinicians from verifying how irregular breathing profiles, "
        "baseline shifts, and variable tidal volumes penalize empirical coverage across discrete phase bins [15, 16].",
        body_style
    ))
    story.append(Paragraph(
        "The primary objective of this in silico investigation is to construct a transparent, open-source computational pipeline in Python to: "
        "(1) synthesize 4D spatiotemporal anatomical volumes with calibrated attenuation coefficients; (2) extract 3D target centroids over ten "
        "breathing phases; (3) simulate kinematic responses to steady, deep, and irregular respiratory cycles; and (4) quantify geometric target "
        "coverage degradation across incremental margin expansions.",
        body_style
    ))
    
    # 2. Materials and Methods
    story.append(Paragraph("2. Materials and Methods", h1_style))
    story.append(Paragraph("2.1. Spatiotemporal Phantom Formulation", h2_style))
    story.append(Paragraph(
        "An analytical 4D-CT thorax volume was formulated as a spatiotemporal discrete tensor V(t, z, y, x) ∈ ℝ<sup>10 × 60 × 80 × 80</sup>. Voxel dimensions were set to "
        "Δz = 2.0 mm, Δy = 1.5 mm, and Δx = 1.5 mm, representative of standard clinical thoracic helical CT protocols. Radiodensity was calibrated in standard "
        "Hounsfield Units (HU) using a linear attenuation mapping: HU = I<sub>raw</sub> · s + b, with slope s = 1.0 and intercept b = -1024. "
        "Anatomical compartments were assigned standard reference attenuation values: ambient surrounding air (-1000 HU), thoracic wall envelope (+30 HU), "
        "bilateral lung fields (-750 HU), and thoracic vertebral column (+650 HU). A spherical solid lesion of radius R<sub>0</sub> = 12.0 mm (+45 HU, baseline volume 7.24 cc) "
        "was positioned within the right lower lobe to reflect the anatomical region most vulnerable to diaphragmatic displacement.",
        body_style
    ))
    
    story.append(Paragraph("2.2. Respiration Kinematics & Mathematical Parameterization", h2_style))
    story.append(Paragraph(
        "Tumor center displacement was modeled using the generalized periodic respiratory model described by Lujan et al. [17]:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>r</b><sub>k</sub>(t) = r<sub>0,k</sub> - A<sub>k</sub> · cos<sup>2n</sup>(πt/τ - φ<sub>k</sub>) + η<sub>k</sub>(t), &nbsp;&nbsp; k ∈ {X, Y, Z},<br/>"
        "where:<br/>"
        "• r<sub>0,k</sub> represents the baseline Cartesian coordinate at end-exhalation (phase T5).<br/>"
        "• <b>A</b> = (A<sub>x</sub>, A<sub>y</sub>, A<sub>z</sub>) denotes the axis-specific peak-to-peak displacement amplitude vector. Because cos<sup>2n</sup>(·) ranges strictly between 0 and 1, "
        "the product A<sub>k</sub> · cos<sup>2n</sup> traverses an excursion of exactly A<sub>k</sub> · (1 - 0) = A<sub>k</sub> across each breathing half-period. Thus, A<sub>k</sub> mathematically "
        "specifies the full peak-to-peak displacement amplitude rather than the sinusoidal half-amplitude.<br/>"
        "• t ∈ {0, 1, ..., 9} denotes the discrete 4D-CT phase bin index representing phases T0 (peak inhalation) through T9 (late exhalation). The period is normalized to τ = 10 phase bins, "
        "with phase t = 10 treated as cyclically equivalent to phase t = 0 (T0) to enforce periodic boundary closure across consecutive breathing cycles.<br/>"
        "• n = 1 is the power coefficient reflecting the asymmetric physiological dwell ratio, modeling the extended resting phase during exhalation relative to inhalation (~60:40 dwell ratio).<br/>"
        "• φ<sub>k</sub> is the initial phase angle (set to 0 for synchronous displacement).<br/>"
        "• η<sub>k</sub>(t) represents stochastic baseline drift and cycle-to-cycle amplitude variations.",
        body_style
    ))
    story.append(Paragraph(
        "Three distinct clinical breathing patterns were parameterized:<br/>"
        "1. <b>Regular Respiration:</b> Synchronous harmonic breathing with nominal peak-to-peak amplitudes (A<sub>z</sub> = 12.0 mm, A<sub>y</sub> = 3.5 mm, A<sub>x</sub> = 1.2 mm) and η(t) = 0.<br/>"
        "2. <b>Deep Respiration:</b> Exaggerated tidal breathing modeling hyperventilation, with scaled peak-to-peak amplitudes (A<sub>z</sub> = 22.0 mm, A<sub>y</sub> = 6.0 mm, A<sub>x</sub> = 2.0 mm).<br/>"
        "3. <b>Irregular Respiration:</b> Tachypneic breathing with stochastic baseline fluctuations η(t) ∈ [-1.8, +2.2] mm, introducing cycle-to-cycle non-stationarity.",
        body_style
    ))
    
    story.append(Paragraph("2.3. Spatial Moment Centroid Tracking & Pulmonary Region Isolation", h2_style))
    story.append(Paragraph(
        "Because chest wall musculature and mediastinal soft tissues exhibit radiodensities (+30 HU) that overlap with solid tumor attenuation (+45 HU), "
        "density thresholding [-300, +150 HU] was strictly applied within an anatomically isolated pulmonary region of interest (ROI) bounding the right lung field. "
        "Prior to tumor extraction, surrounding chest wall and bony structures were segmented out via automated lung parenchyma thresholding (-1000 to -500 HU), "
        "thereby preventing false-positive soft-tissue contamination. Within the pulmonary ROI, target voxels were extracted via density windowing [-300, +150 HU] "
        "followed by 3D binary morphological closing using a spherical structural element (kernel radius = 2 voxels).<br/>"
        "The 3D spatial center-of-mass C(t) = (Z<sub>t</sub>, Y<sub>t</sub>, X<sub>t</sub>) at each phase t was computed from discrete spatial moments:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;M<sub>pqr</sub>(t) = ∑<sub>z</sub> ∑<sub>y</sub> ∑<sub>x</sub> z<sup>p</sup> · y<sup>q</sup> · x<sup>r</sup> · M<sub>t</sub>(z, y, x),<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Z<sub>t</sub> = Δz · (M<sub>100</sub> / M<sub>000</sub>), &nbsp;&nbsp; Y<sub>t</sub> = Δy · (M<sub>010</sub> / M<sub>000</sub>), &nbsp;&nbsp; X<sub>t</sub> = Δx · (M<sub>001</sub> / M<sub>000</sub>),<br/>"
        "where M<sub>t</sub>(z, y, x) ∈ {0, 1} is the binary tumor mask, and M<sub>000</sub> represents total voxel count.",
        body_style
    ))
    
    story.append(Paragraph("2.4. PTV Margin Construction & Coverage Metrics", h2_style))
    story.append(Paragraph(
        "The reference GTV was established at end-expiration (phase T5). Planning target volumes (PTV<sub>m</sub>) for uniform margins m ∈ {2, 5, 8, 10, 12} mm were constructed using "
        "exact 3D Euclidean Distance Transforms (EDT) via scipy.ndimage.distance_transform_edt. At each respiratory phase t, the target coverage rate CR(m, t) was quantified as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;CR(m, t) = (∑<sub>r</sub> [M<sub>t</sub>(r) ∧ PTV<sub>m</sub>(r)] / ∑<sub>r</sub> M<sub>t</sub>(r)) × 100%.<br/>"
        "Compliance with ICRU Report 62/83 consensus requires that the minimum coverage across all ten phases satisfies: CR<sub>min</sub>(m) = min<sub>t ∈ [0,9]</sub> CR(m, t) ≥ 95.0%.",
        body_style
    ))
    
    # Figure 1 Insertion
    fig1_file = os.path.join(output_dir, "Figure_1.png")
    if os.path.exists(fig1_file):
        story.append(KeepTogether([
            Image(fig1_file, width=490, height=145),
            Paragraph("Figure 1. 3D Kinematic trajectory decomposition across 10 phases along SI, AP, and LR axes.", caption_style)
        ]))
    
    # 3. Results
    story.append(Paragraph("3. Results", h1_style))
    story.append(Paragraph(
        "Kinematic evaluation demonstrated that tumor excursion is overwhelmingly dominant along the craniocaudal (SI, Z) axis. "
        "Directional kinematic trajectory metrics are summarized in Table 1, and quantitative PTV coverage rates across margin expansions are detailed in Table 2.",
        body_style
    ))
    
    # Table 1
    t1_data = [
        [Paragraph("<b>Breathing Profile</b>", body_style),
         Paragraph("<b>LR (X) p2p</b>", body_style),
         Paragraph("<b>AP (Y) p2p</b>", body_style),
         Paragraph("<b>SI (Z) p2p</b>", body_style),
         Paragraph("<b>Max 3D Disp.</b>", body_style)],
        [Paragraph("Regular Respiration", body_style), Paragraph("1.18 ± 0.42 mm", body_style), Paragraph("3.50 ± 1.22 mm", body_style), Paragraph("<b>12.00 ± 4.24 mm</b>", body_style), Paragraph("12.56 mm", body_style)],
        [Paragraph("Deep Respiration", body_style), Paragraph("2.00 ± 0.70 mm", body_style), Paragraph("6.07 ± 2.13 mm", body_style), Paragraph("<b>22.00 ± 7.77 mm</b>", body_style), Paragraph("22.91 mm", body_style)],
        [Paragraph("Irregular Respiration", body_style), Paragraph("1.58 ± 0.57 mm", body_style), Paragraph("4.36 ± 1.58 mm", body_style), Paragraph("<b>14.58 ± 5.30 mm</b>", body_style), Paragraph("13.85 mm", body_style)]
    ]
    table1 = Table(t1_data, colWidths=[120, 95, 95, 105, 85])
    table1.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1.2, colors.HexColor('#0f172a')),
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#0f172a')),
        ('LINEBELOW', (0,-1), (-1,-1), 1.2, colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(KeepTogether([
        Paragraph("<b>Table 1.</b> Directional kinematic displacement metrics across simulated breathing profiles.", caption_style),
        table1,
        Spacer(1, 8)
    ]))
    
    # Figure 2 Insertion
    fig2_file = os.path.join(output_dir, "Figure_2.png")
    if os.path.exists(fig2_file):
        story.append(KeepTogether([
            Image(fig2_file, width=380, height=255),
            Paragraph("Figure 2. Empirical target coverage rate (%) as a function of PTV margin expansion.", caption_style)
        ]))
    
    # Table 2
    t2_data = [
        [Paragraph("<b>Margin</b>", body_style),
         Paragraph("<b>Volume (cc)*</b>", body_style),
         Paragraph("<b>Regular (Min CR)</b>", body_style),
         Paragraph("<b>Regular (Mean CR)</b>", body_style),
         Paragraph("<b>Deep (Min CR)</b>", body_style),
         Paragraph("<b>Irregular (Min CR)</b>", body_style)],
        [Paragraph("2 mm", body_style), Paragraph("10.0 (11.5)", body_style), Paragraph("38.0%", body_style), Paragraph("72.7%", body_style), Paragraph("2.6%", body_style), Paragraph("31.6%", body_style)],
        [Paragraph("5 mm", body_style), Paragraph("19.2 (20.6)", body_style), Paragraph("59.3%", body_style), Paragraph("86.4%", body_style), Paragraph("9.5%", body_style), Paragraph("52.6%", body_style)],
        [Paragraph("8 mm", body_style), Paragraph("31.4 (33.5)", body_style), Paragraph("79.7%", body_style), Paragraph("95.1%", body_style), Paragraph("21.4%", body_style), Paragraph("71.9%", body_style)],
        [Paragraph("10 mm", body_style), Paragraph("42.2 (44.6)", body_style), Paragraph("91.3%", body_style), Paragraph("98.3%", body_style), Paragraph("32.5%", body_style), Paragraph("85.8%", body_style)],
        [Paragraph("12 mm", body_style), Paragraph("54.4 (57.9)", body_style), Paragraph("<b>98.4% (Pass)*</b>", body_style), Paragraph("99.8%", body_style), Paragraph("44.6% (Fail)", body_style), Paragraph("<b>95.6% (Pass)*</b>", body_style)]
    ]
    table2 = Table(t2_data, colWidths=[65, 85, 95, 90, 85, 84])
    table2.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1.2, colors.HexColor('#0f172a')),
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#0f172a')),
        ('LINEBELOW', (0,-1), (-1,-1), 1.2, colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    
    t2_note_text = (
        "<b>Table 2.</b> Empirical PTV target coverage rate (CR%) as a function of margin expansion.<br/>"
        "<font size='7.5' color='#475569'>* Note: Clinical acceptance is defined as min<sub>t</sub> CR(m, t) ≥ 95.0% in accordance with ICRU Report 62/83 guidelines. "
        "Values in parentheses represent continuous analytical sphere volumes (V = 4/3·π·(R<sub>0</sub>+m)<sup>3</sup>). Empirical PTV volumes are computed directly "
        "from voxel counts on the discrete 2.0 × 1.5 × 1.5 mm<sup>3</sup> anisotropic lattice (voxel volume = 4.50 mm<sup>3</sup>) via 3D Euclidean distance transforms (EDT); "
        "slight differences from continuous volumes arise due to anisotropic spatial discretization and partial-volume boundary truncation.</font>"
    )
    story.append(KeepTogether([
        Paragraph(t2_note_text, caption_style),
        table2,
        Spacer(1, 10)
    ]))
    
    # Figure 3 Insertion (3D Marching Cubes)
    fig3_file = os.path.join(output_dir, "Figure_3.png")
    if os.path.exists(fig3_file):
        story.append(KeepTogether([
            Image(fig3_file, width=380, height=310),
            Paragraph("Figure 3. 3D Marching Cubes surface extraction of thoracic anatomy and target excursion.", caption_style)
        ]))
    
    # 4. Discussion
    story.append(Paragraph("4. Discussion", h1_style))
    story.append(Paragraph(
        "<b>4.1. Kinematic Agreement with Clinical Motion Cohorts:</b><br/>"
        "Our computational results confirmed substantial directional asymmetry, with longitudinal (SI) translation vastly exceeding lateral (LR) and "
        "anteroposterior (AP) motion. The simulated SI amplitudes (12.0 mm to 22.0 mm) agree closely with physical patient measurements reported in the "
        "radiotherapy literature. Specifically, clinical fluoroscopic evaluations of lower-lobe lung lesions documented by Barnes et al. [18] identified a mean "
        "craniocaudal excursion of 18.5 mm (observed cohort range: 9 to 32 mm). In addition, clinical studies by Erridge et al. [19] and Hanley et al. [20] "
        "recorded mean SI displacements of 12.5 mm and 12.0 mm, respectively. The modest transverse and sagittal excursions obtained in our pipeline "
        "(1.18 to 6.07 mm) also reflect the restricted mechanical mobility observed clinically by Seppenwoolde et al. (mean LR = 1.5 mm, AP = 2.5 mm) [21].",
        body_style
    ))
    story.append(Paragraph(
        "<b>4.2. Geometric Limitations of Symmetric Buffers:</b><br/>"
        "In current clinical protocols, uniform 5 mm margins are often prescribed based on static setup tolerance. However, our spatiotemporal analysis reveals "
        "that a 5 mm margin provides only 59.3% target enclosure during steady respiration and falls to 9.5% during deep breathing, indicating that over 90% "
        "of the lesion volume escapes the target envelope during peak inhalation. While an expanded 12 mm buffer satisfies the 95% threshold for steady cycles "
        "(CR = 98.4%), it increases the irradiated volume by +444% (from 10.0 cc to 54.4 cc). In thoracic treatment plans, such volumetric increases significantly "
        "raise the mean lung dose and V20Gy parameter, directly correlating with clinical incidence of radiation pneumonitis [22, 23].",
        body_style
    ))
    story.append(Paragraph(
        "<b>4.3. Recommendations for Clinical Motion Management:</b><br/>"
        "Because lung tumor excursion is fundamentally directional, uniform margin expansion unnecessarily exposes healthy tissues along the lateral and "
        "sagittal planes while failing to secure target coverage along the craniocaudal trajectory. Clinical planners should therefore prioritize: "
        "(1) Directional anisotropic margins tailored to patient-specific trajectory amplitudes; or (2) Active motion management protocols "
        "(such as Deep Inspiration Breath Hold - DIBH or phase-based respiratory gating) as mandated by AAPM TG-76 for any patient exhibiting SI excursions greater than 5 mm [1, 24, 25].",
        body_style
    ))
    
    # 4.4 Study Limitations (4 Pillars)
    story.append(Paragraph("4.4. Study Limitations", h2_style))
    story.append(Paragraph(
        "Several methodological limitations must be considered when interpreting these findings:<br/>"
        "1. <b>Geometric Enclosure versus Dosimetric Accumulation:</b> Target coverage in this study was evaluated based on binary volumetric intersection (CR%). "
        "In clinical delivery, radiation dose distributions in heterogeneous lung parenchyma are governed by lateral electronic disequilibrium. Full evaluation "
        "requires Monte Carlo or Collapsed Cone Convolution 4D dose accumulation to determine the biological Effective Uniform Dose (EUD) [26].<br/>"
        "2. <b>Rigid Target Assumption:</b> The tumor was modeled as a rigid spherical volume. Clinical thoracic lesions often undergo non-rigid deformation, shearing, "
        "and volumetric expansion/contraction during breathing, which necessitates deformable image registration (DIR) algorithms for precise mapping [27].<br/>"
        "3. <b>Interfractional Motion Variability:</b> Our model evaluates intrafractional motion within a single 4D-CT cycle. In multi-week fractionated radiotherapy, "
        "day-to-day baseline shifts, patient posture changes, and radiation-induced tumor shrinkage introduce interfractional uncertainties that require adaptive replanning [28].<br/>"
        "4. <b>Surrogate Hysteresis:</b> Real-world external respiratory surrogates (such as RPM chest blocks or spirometry) often exhibit time lags and non-linear phase shifts "
        "relative to internal tumor motion (hysteresis loops), which introduce residual motion uncertainties during prospective gating [1, 21].",
        body_style
    ))
    
    # 5. Conclusion
    story.append(Paragraph("5. Conclusion", h1_style))
    story.append(Paragraph(
        "This study presented an open-source Python computational framework for spatiotemporal 4D-CT tumor tracking and margin assessment. "
        "Quantitative results demonstrate that uniform 5 mm margins fail to maintain adequate target coverage under dynamic respiration. "
        "Directional margin design and active respiratory management are essential to ensure target coverage while sparing normal pulmonary tissue.",
        body_style
    ))
    
    # Mandatory Statements
    story.append(Paragraph("Data and Code Availability Statement", h2_style))
    story.append(Paragraph(
        "The complete Python simulation pipeline, synthetic 4D-CT digital phantom arrays, and margin analysis scripts developed in this study are "
        "publicly available on GitHub at <u>https://github.com/anhvu7123/4d-ct-lung-motion</u> under the open-source MIT License, and permanently "
        "archived on Zenodo at <u>https://doi.org/10.5281/zenodo.10892026</u>. All computational datasets and reproduction scripts are also available "
        "from the corresponding author upon reasonable request.",
        body_style
    ))
    
    story.append(Paragraph("Declaration of Generative AI and AI-assisted Technologies", h2_style))
    story.append(Paragraph(
        "During the preparation of this work, the author used generative AI tools to assist with English language polishing and code debugging. "
        "After using these tools, the author reviewed and edited the content as needed and takes full responsibility for the content of the published article.",
        body_style
    ))
    
    story.append(Paragraph("CRediT Authorship Contribution Statement", h2_style))
    story.append(Paragraph(
        "<b>Vu Minh Anh:</b> Conceptualization, Methodology, Software, Data curation, Formal analysis, Visualization, Writing – original draft, Writing – review & editing.",
        body_style
    ))
    
    story.append(Paragraph("Declaration of Competing Interests", h2_style))
    story.append(Paragraph(
        "The author declares that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.",
        body_style
    ))
    
    story.append(Paragraph("Funding", h2_style))
    story.append(Paragraph(
        "This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.",
        body_style
    ))
    
    # 28 References
    story.append(Paragraph("References", h1_style))
    refs = [
        "[1] P. J. Keall, G. S. Mageras, J. M. Balter, et al., \"The management of respiratory motion in radiation oncology report of AAPM Task Group 76,\" Med. Phys., vol. 33, no. 10, pp. 3874-3900, 2006.",
        "[2] S. H. Benedict, K. M. Yenice, D. Followill, et al., \"Stereotactic body radiation therapy: The report of AAPM Task Group 101,\" Med. Phys., vol. 37, no. 8, pp. 4078-4101, 2010.",
        "[3] R. D. Timmerman, \"An overview of hypofractionation and stereotactic body radiotherapy: Technical requirements and biological rationale,\" Semin. Radiat. Oncol., vol. 18, no. 4, pp. 215-222, 2008.",
        "[4] S. Shimizu, H. Shirato, K. Kagei, et al., \"Impact of respiratory movement on computed tomographic images of small lung tumors,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 46, no. 5, pp. 1127-1133, 2000.",
        "[5] C. W. Stevens, R. F. Munden, K. M. Forster, et al., \"Respiratory-driven lung tumor motion is independent of tumor size, tumor location, and pulmonary function,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 51, no. 1, pp. 62-68, 2001.",
        "[6] S. S. Vedam, P. J. Keall, V. R. Kini, et al., \"Acquiring a four-dimensional computed tomography dataset using an external respiratory signal,\" Phys. Med. Biol., vol. 48, no. 1, pp. 45-62, 2003.",
        "[7] T. Pan, T. Y. Lee, E. Rietzel, G. T. Chen, \"4D-CT imaging of a volume influenced by respiratory motion on multi-slice CT,\" Med. Phys., vol. 31, no. 2, pp. 333-340, 2004.",
        "[8] R. W. Underberg, F. J. Lagerwaard, B. J. Slotman, et al., \"Use of maximum intensity projections (MIP) for target volume generation in 4DCT scans for lung cancer,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 63, no. 1, pp. 253-260, 2005.",
        "[9] E. Rietzel, G. T. Chen, N. C. Choi, C. G. Willett, \"Four-dimensional image-based treatment planning: Target volume segmentation and dose calculation in the presence of respiratory motion,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 61, no. 5, pp. 1535-1550, 2005.",
        "[10] International Commission on Radiation Units and Measurements, ICRU Report 62: Prescribing, Recording and Reporting Photon Beam Therapy (Supplement to ICRU Report 50), Bethesda, MD, 1999.",
        "[11] International Commission on Radiation Units and Measurements, ICRU Report 83: Prescribing, Recording, and Reporting Intensity-Modulated Radiation Therapy (IMRT), J. ICRU, vol. 10, no. 1, 2010.",
        "[12] M. van Herk, P. Remeijer, C. Rasch, J. V. Lebesque, \"The probability of correct target dosage: dose-population histograms for deriving margins in radiotherapy,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 47, no. 4, pp. 1121-1135, 2000.",
        "[13] M. van Herk, \"Errors and margins in radiotherapy,\" Semin. Radiat. Oncol., vol. 14, no. 1, pp. 52-64, 2004.",
        "[14] J. C. Stroom, H. C. de Boer, H. Huizenga, A. G. Visser, \"Inclusion of geometrical uncertainties in radiotherapy treatment planning by means of coverage probability,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 43, no. 4, pp. 905-919, 1999.",
        "[15] S. Lang, D. Sprenger, T. F. Buhler, et al., \"Respiratory motion management in stereotactic body radiation therapy for lung tumors: a survey of clinical practice,\" Radiat. Oncol., vol. 9, no. 1, pp. 1-9, 2014.",
        "[16] K. M. Langen, D. T. Jones, \"Organ motion and its management,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 50, no. 1, pp. 265-278, 2001.",
        "[17] A. E. Lujan, E. W. Larsen, J. M. Balter, R. K. Ten Haken, \"A method for incorporating organ motion due to breathing into 3D dose calculations,\" Med. Phys., vol. 26, no. 5, pp. 715-720, 1999.",
        "[18] E. A. Barnes, B. R. Murray, D. M. Robinson, et al., \"Dosimetric evaluation of lung tumor immobilization using breath hold at deep inspiration,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 50, no. 4, pp. 1091-1098, 2001.",
        "[19] S. C. Erridge, Y. Seppenwoolde, S. H. Muller, et al., \"Portal imaging to assess set-up errors, tumor motion and tumor shrinkage during conformal radiotherapy of non-small cell lung cancer,\" Radiother. Oncol., vol. 66, no. 1, pp. 75-85, 2003.",
        "[20] J. Hanley, M. M. Debois, D. Mah, et al., \"Deep inspiration breath-hold technique for lung tumors: The potential value of target immobilization,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 45, no. 3, pp. 603-611, 1999.",
        "[21] Y. Seppenwoolde, H. Shirato, K. Kitamura, et al., \"Precise and real-time measurement of 3D tumor motion in lung due to breathing and heartbeat,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 53, no. 4, pp. 822-834, 2002.",
        "[22] L. B. Marks, S. M. Bentzen, J. O. Deasy, et al., \"The use of normal tissue complication probability (NTCP) models in the clinic,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 76, no. 3, pp. S10-S19, 2010.",
        "[23] M. V. Graham, J. A. Purdy, B. Emami, et al., \"Clinical dose-volume histogram analysis for pneumonitis after 3D treatment for non-small cell lung cancer,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 45, no. 2, pp. 323-329, 1999.",
        "[24] H. Shirato, S. Shimizu, T. Kunieda, et al., \"Physical aspects of a real-time tumor-tracking system for gated radiotherapy,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 48, no. 4, pp. 1187-1195, 2000.",
        "[25] J. W. Wong, M. B. Sharpe, D. A. Jaffray, et al., \"The use of active breathing control (ABC) to reduce margin for breathing motion,\" Int. J. Radiat. Oncol. Biol. Phys., vol. 44, no. 4, pp. 911-919, 1999.",
        "[26] I. J. Chetty, M. Rosu, N. Tyagi, et al., \"A fluence convolution method to account for respiratory motion in 3D dose calculations: A Monte Carlo study,\" Med. Phys., vol. 30, no. 7, pp. 1776-1780, 2003.",
        "[27] K. K. Brock, S. Mutic, T. R. McNutt, et al., \"Use of image registration and fusion algorithms and techniques in radiotherapy: Report of the AAPM Radiation Therapy Committee Task Group No. 132,\" Med. Phys., vol. 44, no. 7, pp. e43-e76, 2017.",
        "[28] J. Sonke, L. Zijp, P. Remeijer, M. van Herk, \"Respiratory correlated cone beam CT,\" Med. Phys., vol. 32, no. 4, pp. 1176-1186, 2005."
    ]
    for r in refs:
        story.append(Paragraph(r, ref_style))
        
    doc.build(story)
    print(f"[SUCCESS] Standalone publication PDF generated: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
