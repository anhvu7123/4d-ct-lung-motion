# In Silico Evaluation of 4D-CT Lung Tumor Kinematics, Target Margin Strategies, and Coverage Robustness Under Respiratory Variations and Setup Uncertainties (Revision 3.2)

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
1. **$N = 5,000$ independent unseen breathing cycles** (Monte Carlo with 95% Wilson Score Confidence Intervals for binomial pass rates and empirical $[P_{2.5}, P_{97.5}]$ inter-percentile ranges for Coverage Ratios).
2. **Multi-regimen population setup uncertainties** across $N_{\text{pat}} = 200$ virtual patients ($7,600$ total treatment sessions):
   - **SBRT 3-fraction course** ($3 \times 18$ Gy, 600 sessions)
   - **SBRT 5-fraction course** ($5 \times 10$ Gy, 1,000 sessions)
   - **Conventional 30-fraction course** ($30 \times 2$ Gy, 6,000 sessions)  
   incorporating independent 3D systematic ($\Sigma = 2.0$ mm, constant per patient) and random ($\sigma = 2.0$ mm, daily sampled) setup errors, directly aligned with **AAPM Task Group 324 Report 91.b (2026)** and the **van Herk margin recipe**. Fraction pass rates are evaluated using **95% Patient-Level Cluster Bootstrap** ($B = 2,000$ resamples) to account for intra-patient correlation.
3. **Multi-lesion target coverage robustness** evaluated across small ($r = 8$ mm, 2.1 cc), nominal ($r = 12$ mm, 7.2 cc), and large ($r = 16$ mm, 17.2 cc) lesions ($N = 2,000$ cycles per lesion size; $N_{\text{pat}} = 200$ virtual patients).
4. **Sub-voxel quantization sensitivity analysis** ($N = 1,000$ cycles) verifying that integer voxel rounding ($dz=2.0$ mm, $dy=dx=1.5$ mm; max shift $\approx 1.46$ mm) produces $< 0.5\%$ difference in mean minimum coverage ratio and $\le 3.7\%$ difference in pass rate compared to continuous Monte Carlo sub-voxel point cloud sampling ($N_{\text{sub}} = 2,500$ points), confirming full numerical stability.

---

## 📁 Repository Structure

```
.
├── LICENSE                     # Official MIT Open-Source License
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
├── fig5_robustness_amplitude.png # Figure 5: Dual-panel Amplitude Sensitivity (Pass Rate & Continuous Min CR)
└── fig6_setup_uncertainty.png  # Figure 6: SBRT 3-fx, 5-fx, and CFRT 30-fx Setup Distributions across 200 Patients
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
This executes the 6-phase pipeline in ~39 seconds, producing `simulation_results.json` and all 6 publication-quality figures (`fig1` through `fig6`).

### 3. Generate Manuscript & Cover Letter
```bash
python3 build_full_manuscript.py
python3 build_publication_pdf.py
```
Generates `manuscript.docx`, `manuscript.tex`, `manuscript.pdf`, and `COVER_LETTER.docx` with zero manual copy-pasting.

---

## 📊 Key Findings

### Table 3: Target Strategy Comparison & Setup Uncertainty across 200 Virtual Patients (7,600 Sessions)

| Strategy | PTV Vol (cc) | Vol vs 5mm | Plan Min CR | Irreg MC Pass (95% Wilson CI) | SBRT 3-fx All-Pass (95% Wilson CI) | SBRT 5-fx All-Pass (95% Wilson CI) | CFRT 30-fx Frac-Pass (95% Cluster Boot) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Isotropic 5 mm** | 20.6 | Baseline | 64.7% | 0.0% [0.0%, 0.1%] | 0.0% [0.0%, 1.9%] | 0.0% [0.0%, 1.9%] | 1.5% [1.1%, 1.9%] |
| **Isotropic 12 mm** | 58.0 | +182% | 100.0% | 29.9% [28.6%, 31.1%] | 37.5% [31.1%, 44.4%] | 31.5% [25.4%, 38.3%] | 64.9% [63.2%, 66.7%] |
| **ITV + 2 mm setup** | 22.2 | +7.6% | 100.0% | 55.4% [54.0%, 56.8%] | 1.5% [0.5%, 4.3%] | 0.0% [0.0%, 1.9%] | 27.2% [25.7%, 28.7%] |
| **ITV + 3 mm setup** | 22.3 | +8.3% | 100.0% | 68.3% [67.0%, 69.5%] | 16.5% [12.0%, 22.3%] | 6.0% [3.5%, 10.2%] | 46.4% [43.6%, 49.3%] |
| **ITV + 4 mm (TG-324)** | 26.2 | +27.3% | 100.0% | 87.2% [86.3%, 88.1%] | 42.0% [35.3%, 49.0%] | 27.0% [21.3%, 33.6%] | 67.2% [65.5%, 68.9%] |
| **ITV + 5 mm (TG-324)** | 31.0 | +50.3% | 100.0% | **96.2% [95.7%, 96.7%]** | **66.0% [59.2%, 72.2%]** | **53.0% [46.1%, 59.8%]** | **82.7% [80.5%, 84.9%]** |
| **Anisotropic (Mid-pos + 2mm)** | 19.3 | -6.3% | 99.4% | 18.3% [17.3%, 19.4%] | 0.5% [0.1%, 2.8%] | 0.0% [0.0%, 1.9%] | 20.4% [19.0%, 21.8%] |
| **Anisotropic (Mid-pos + 3mm)** | 22.0 | +6.9% | 100.0% | 53.1% [51.7%, 54.5%] | 12.0% [8.2%, 17.2%] | 4.0% [2.0%, 7.8%] | 37.4% [35.8%, 39.0%] |

### Table 4: Multi-Lesion Target Coverage Robustness ($N=2,000$ MC Cycles, $N_{\text{pat}}=200$ Patients)

| Lesion Radius (mm) | Target Strategy | PTV Vol (cc) | Plan Min CR | Irreg MC Pass (95% Wilson CI) | SBRT 5-fx Frac-Pass (95% Cluster Boot) | SBRT 5-fx All-Pass (95% Wilson CI) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **r = 8 mm (Small, 2.1 cc)** | ITV + 3 mm setup | 9.9 | 100.0% | 54.9% [52.7%, 57.1%] | 33.2% [29.8%, 36.5%] | 0.5% [0.1%, 2.8%] |
| | ITV + 5 mm setup | 15.1 | 100.0% | 86.3% [84.7%, 87.7%] | 73.8% [70.4%, 77.1%] | 29.5% [23.6%, 36.2%] |
| **r = 12 mm (Nominal, 7.2 cc)** | ITV + 3 mm setup | 22.3 | 100.0% | 67.8% [65.7%, 69.8%] | 45.8% [41.8%, 49.7%] | 6.5% [3.8%, 10.8%] |
| | ITV + 5 mm setup | 31.0 | 100.0% | 96.3% [95.4%, 97.0%] | 84.3% [81.5%, 86.9%] | 51.0% [44.1%, 57.8%] |
| **r = 16 mm (Large, 17.2 cc)** | ITV + 3 mm setup | 41.7 | 100.0% | 81.2% [79.5%, 82.9%] | 53.7% [50.0%, 57.3%] | 9.0% [5.8%, 13.8%] |
| | ITV + 5 mm setup | 54.5 | 100.0% | 97.8% [97.1%, 98.4%] | 88.0% [85.7%, 90.3%] | 60.0% [53.1%, 66.5%] |

> **Clinical Takeaway:** While tight ITV margins ($\le 3$ mm) and anisotropic expansions achieve normal tissue sparing on regular planning 4D-CT, they deteriorate sharply under setup uncertainty in hypofractionated SBRT (dropping from 100% to only 6.0% all-fraction success for 5-fraction courses). In concordance with AAPM TG-324 Report 91.b, an ITV setup margin of 4–5 mm is a standard baseline for free-breathing lung SBRT. However, even with ITV + 5 mm, geometric undercoverage persists (17.3% fraction failure in CFRT, 47.0% whole-course failure in SBRT 5-fx), underscoring that margins alone cannot eliminate geometric miss without daily volumetric image guidance (CBCT) and active motion management.

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
