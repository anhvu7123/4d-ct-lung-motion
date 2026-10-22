#!/usr/bin/env python3
"""
Generate Complete Research Data Package for Zenodo / Mendeley Data / Elsevier
Author: Vu Minh Anh
Affiliation: Faculty of Information Technology, Ho Chi Minh City University of Industry and Trade (HUIT)

Outputs in ./data/:
  1. tumor_trajectories_10phases.csv (CSV spreadsheet of 3D kinematics)
  2. ptv_margin_coverage_analysis.csv (CSV spreadsheet of PTV coverage % across margins & phases)
  3. 4dct_phantom_tensor_10phases.npz (Raw 4D spatiotemporal matrix (10, Z, Y, X) in Hounsfield Units)
  4. DATA_README.md (Metadata description for open science repositories)
"""

import os
import json
import numpy as np
import csv
from main import generate_dynamic_phantom

output_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(output_dir, "data")
os.makedirs(data_dir, exist_ok=True)

# Load existing simulation results JSON
with open(os.path.join(output_dir, "simulation_results.json"), "r") as f:
    sim_data = json.load(f)

# ------------------------------------------------------------------------------
# 1. Export tumor_trajectories_10phases.csv
# ------------------------------------------------------------------------------
traj_csv_path = os.path.join(data_dir, "tumor_trajectories_10phases.csv")
with open(traj_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Breathing_Pattern", "Phase_Index", "Phase_Percentage", "Z_Superior_Inferior_mm",
        "Y_Anterior_Posterior_mm", "X_Left_Right_mm", "Displacement_From_T5_mm"
    ])
    
    for sc in ['regular', 'deep', 'irregular']:
        centroids = np.array(sim_data[sc]['centroids'])
        ref_t5 = centroids[5]
        for p_idx in range(10):
            cz, cy, cx = centroids[p_idx]
            disp = np.sqrt((cz - ref_t5[0])**2 + (cy - ref_t5[1])**2 + (cx - ref_t5[2])**2)
            writer.writerow([
                sc.capitalize(), f"T{p_idx}", f"{p_idx * 10}%",
                f"{cz:.3f}", f"{cy:.3f}", f"{cx:.3f}", f"{disp:.3f}"
            ])

print(f"[SUCCESS] Exported: {traj_csv_path}")

# ------------------------------------------------------------------------------
# 2. Export ptv_margin_coverage_analysis.csv
# ------------------------------------------------------------------------------
ptv_csv_path = os.path.join(data_dir, "ptv_margin_coverage_analysis.csv")
with open(ptv_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Breathing_Pattern", "PTV_Margin_mm", "PTV_Volume_cc",
        "Min_Coverage_Pct", "Mean_Coverage_Pct", "Pass_ICRU_95",
        "T0_Insp_CR", "T1_CR", "T2_CR", "T3_CR", "T4_CR", "T5_Exp_CR",
        "T6_CR", "T7_CR", "T8_CR", "T9_CR"
    ])
    
    for sc in ['regular', 'deep', 'irregular']:
        for m in [2, 5, 8, 10, 12]:
            m_data = sim_data[sc]['ptv_results'][str(m)]
            cr_phases = [f"{c:.2f}%" for c in m_data['coverages']]
            writer.writerow([
                sc.capitalize(), m, f"{m_data['ptv_volume_cc']:.2f}",
                f"{m_data['min_coverage']:.2f}%", f"{m_data['mean_coverage']:.2f}%",
                "YES" if m_data['pass_icru_95'] else "NO",
                *cr_phases
            ])

print(f"[SUCCESS] Exported: {ptv_csv_path}")

# ------------------------------------------------------------------------------
# 3. Export 4dct_phantom_tensor_10phases.npz (Raw Matrix in HU)
# ------------------------------------------------------------------------------
print("Generating full 4D-CT matrix tensor (T, Z, Y, X)...")
volumes_reg, masks_reg, spacing, _ = generate_dynamic_phantom(scenario='regular', nz=60, ny=80, nx=80)
volumes_deep, masks_deep, _, _ = generate_dynamic_phantom(scenario='deep', nz=60, ny=80, nx=80)
volumes_irreg, masks_irreg, _, _ = generate_dynamic_phantom(scenario='irregular', nz=60, ny=80, nx=80)

npz_path = os.path.join(data_dir, "4dct_phantom_tensor_10phases.npz")
np.savez_compressed(
    npz_path,
    vols_regular=volumes_reg,
    masks_regular=masks_reg,
    vols_deep=volumes_deep,
    masks_deep=masks_deep,
    vols_irregular=volumes_irreg,
    masks_irregular=masks_irreg,
    voxel_spacing_mm=np.array(spacing)
)
print(f"[SUCCESS] Exported raw 4D-CT tensor array: {npz_path}")

# ------------------------------------------------------------------------------
# 4. Export DATA_README.md (Metadata for Zenodo/Mendeley)
# ------------------------------------------------------------------------------
readme_path = os.path.join(data_dir, "DATA_README.md")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(f"""# Research Dataset: 4D-CT Lung Tumor Motion & PTV Margins

**Lead Investigator:** Vũ Minh Anh  
**Affiliation:** Faculty of Information Technology, Ho Chi Minh City University of Industry and Trade (HUIT)  
**Email:** mvu103536@gmail.com  
**Associated Publication:** *4D-CT-Based Tumor Motion Modeling and Quantitative Evaluation of PTV Margins for Lung Radiotherapy Planning* (Computers in Biology and Medicine)

---

## 📁 Dataset Inventory

1. **`tumor_trajectories_10phases.csv`**:
   - Contains 3D center-of-mass coordinates ($Z, Y, X$) in millimeters across 10 respiratory phase bins ($T_0 - T_9$) for Regular, Deep, and Irregular breathing patterns.
   - Includes displacement vector distance from the baseline end-expiration state ($T_5$).

2. **`ptv_margin_coverage_analysis.csv`**:
   - Contains target coverage rates ($CR\%$) for uniform PTV margin expansions ($2, 5, 8, 10, 12\\text{{ mm}}$).
   - Reports Minimum $CR$, Mean $CR$, PTV Volume in cubic centimeters (cc), and binary ICRU 62/83 compliance ($CR \\ge 95\%$).

3. **`4dct_phantom_tensor_10phases.npz`**:
   - Compressed 4-dimensional volumetric image tensors in Hounsfield Units (HU).
   - Array shape: $(T=10, Z=60, Y=80, X=80)$ with calibrated voxel spacing $\\Delta z = 2.0\\text{{ mm}}, \\Delta y = 1.5\\text{{ mm}}, \\Delta x = 1.5\\text{{ mm}}$.
   - Includes true binary segmentation ground-truth masks for each phase.

## 🐍 How to load in Python:
```python
import numpy as np
import pandas as pd

# Load trajectories spreadsheet
df_traj = pd.read_csv('tumor_trajectories_10phases.csv')
print(df_traj.head())

# Load raw 4D-CT tensors in Hounsfield Units
data = np.load('4dct_phantom_tensor_10phases.npz')
vols_reg = data['vols_regular'] # Shape (10, 60, 80, 80)
print("Air HU:", vols_reg[0].min(), "| Bone HU:", vols_reg[0].max())
```
""")

print(f"[SUCCESS] Exported Data Description: {readme_path}")
print("\n[ALL DONE] Full Research Data Package ready in folder: ./data/")
