# In Silico Evaluation of 4D-CT Lung Tumor Kinematics, Target Margin Strategies, and Coverage Robustness Under Respiratory Variations and Setup Uncertainties (Revision 3.1)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AAPM TG-324](https://img.shields.io/badge/AAPM-TG--324%20Report%2091.b%20(2026)-green.svg)](https://doi.org/10.1002/mp.70677)

**Author:** Vu Minh Anh, B.S.  
**Affiliation:** Faculty of Information Technology, Ho Chi Minh City University of Industry and Trade (HUIT), Vietnam  
**Correspondence:** `anhvm@huit.edu.vn`  
**Repository:** [https://github.com/anhvu7123/4d-ct-lung-motion](https://github.com/anhvu7123/4d-ct-lung-motion)

---

## 🔬 Overview & Scientific Scope

This open-source in silico simulation framework models the complex interplay between 4D-CT respiratory kinematics, target margin expansion strategies (Isotropic, Internal Target Volume [ITV], and Mid-position Anisotropic), and statistical coverage robustness in lung radiation therapy.

To overcome the **methodological tautology** prevalent in prior literature (evaluating target coverage exclusively on the identical 10 planning phases used to construct the ITV), this platform freezes planning target volumes from the nominal regular 4D-CT and stress-tests them across:
1. **$N = 5,000$ independent unseen breathing cycles** (Monte Carlo with exact 95% Wilson Score Confidence Intervals for binomial pass rates and empirical $[P_{2.5}, P_{97.5}]$ inter-percentile ranges for Coverage Ratios).
2. **Multi-regimen population setup uncertainties** across 50 virtual patients:
   - **SBRT 3-fraction course** ($3 \times 18$ Gy, 150 sessions)
   - **SBRT 5-fraction course** ($5 \times 10$ Gy, 250 sessions)
   - **Conventional 30-fraction course** ($30 \times 2$ Gy, 1,500 sessions)
   incorporating independent 3D systematic ($\Sigma = 2.0$ mm) and random ($\sigma = 2.0$ mm) setup errors, directly aligned with **AAPM Task Group 324 Report 91.b (2026)** and the **van Herk margin recipe**.

---

## 📁 Repository Structure

```
.
├── main.py                     # Core simulation pipeline (Phases 1–6)
├── build_full_manuscript.py    # Synchronized DOCX, TeX, and Cover Letter generator
├── build_publication_pdf.py    # Publication-grade PDF generator (ReportLab)
├── requirements.txt            # Python dependencies (numpy, scipy, matplotlib, python-docx, reportlab)
├── simulation_results.json     # 100% synchronized numerical database
├── manuscript.pdf              # 6-page publication-ready PDF manuscript
├── manuscript.docx             # Microsoft Word manuscript format
├── manuscript.tex              # LaTeX source code
├── COVER_LETTER.docx           # Formal cover letter and response to reviewers
├── report.html                 # Interactive 4D-CT visualization tool
├── fig1_phantom.png            # Figure 1: Anthropomorphic Thorax Phantom
├── fig2_trajectory.png         # Figure 2: 3D Tumor Trajectory & T6 End-Exhalation Reference
├── fig3_coverage.png           # Figure 3: Unclipped (0–105%) Phase Coverage Dynamics
├── fig4_tradeoff.png           # Figure 4: PTV Volume vs Planning Coverage Trade-off
├── fig5_robustness_amplitude.png # Figure 5: Amplitude Sensitivity with 95% Wilson CIs
└── fig6_setup_uncertainty.png  # Figure 6: SBRT 3-fx, 5-fx, and CFRT 30-fx Setup Distributions
```

---

## 🚀 Reproduction Instructions

### 1. Environment Setup
```bash
git clone https://github.com/anhvu7123/4d-ct-lung-motion.git
cd 4d-ct-lung-motion
pip install -r requirements.txt
```

### 2. Run Simulation Pipeline
```bash
python3 main.py
```
This executes the 6-phase pipeline in ~25 seconds, producing `simulation_results.json` and all 6 publication-quality figures (`fig1` through `fig6`).

### 3. Generate Manuscript & Cover Letter
```bash
python3 build_full_manuscript.py
python3 build_publication_pdf.py
```
Generates `manuscript.docx`, `manuscript.tex`, `manuscript.pdf`, and `COVER_LETTER.docx` with zero manual copy-pasting.

---

## 📊 Key Findings

| Strategy | PTV Vol (cc) | Vol vs 5mm | Plan Min CR | Irreg MC Pass (Wilson 95% CI) | SBRT 3-fx All-Pass | SBRT 5-fx All-Pass | CFRT 30-fx Frac-Pass |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Isotropic 5 mm** | 20.6 | Baseline | 64.7% | 0.0% [0.0%, 0.1%] | 0.0% | 0.0% | 1.9% |
| **Isotropic 12 mm** | 58.0 | +182% | 100.0% | 29.9% [28.6%, 31.1%] | 40.0% | 40.0% | 69.6% |
| **ITV + 2 mm setup** | 22.2 | +7.6% | 100.0% | 55.4% [54.0%, 56.8%] | 8.0% | 2.0% | 35.3% |
| **ITV + 3 mm setup** | 23.9 | +16.0% | 100.0% | 87.1% [86.1%, 88.0%] | 42.0% | 12.0% | 59.1% |
| **ITV + 4 mm (TG-324)** | 25.7 | +24.9% | 100.0% | 87.2% [86.3%, 88.1%] | 62.0% | 32.0% | 74.9% |
| **ITV + 5 mm (TG-324)** | 27.7 | +34.3% | 100.0% | **97.9% [97.4%, 98.2%]** | **82.0%** | **62.0%** | **87.4%** |
| **Anisotropic (Mid-pos + 2mm)** | 19.3 | -6.3% | 99.4% | 18.3% [17.3%, 19.4%] | 0.0% | 0.0% | 19.9% |
| **Anisotropic (Mid-pos + 3mm)** | 22.0 | +6.9% | 100.0% | 53.1% [51.7%, 54.5%] | 14.0% | 2.0% | 43.3% |

> **Clinical Takeaway:** While tight ITV margins ($\le 3$ mm) and anisotropic expansions achieve normal tissue sparing on regular planning 4D-CT, they deteriorate sharply under setup uncertainty in hypofractionated SBRT (dropping from 100% to only 12.0% all-fraction success for 5-fraction courses). In concordance with AAPM TG-324, an ITV setup margin of 4–5 mm is required for free-breathing lung SBRT unless daily volumetric image guidance (CBCT) and active motion management are deployed.

---

## 📜 Citation & License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```bibtex
@article{vu2026insilico,
  title={In Silico Evaluation of 4D-CT Lung Tumor Kinematics, Target Margin Strategies, and Coverage Robustness Under Respiratory Variations and Setup Uncertainties},
  author={Vu, Minh Anh},
  journal={Medical Physics / In Silico Radiation Oncology},
  year={2026},
  url={https://github.com/anhvu7123/4d-ct-lung-motion}
}
```
