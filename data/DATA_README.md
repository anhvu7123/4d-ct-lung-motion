# Research Dataset: 4D-CT Lung Tumor Motion & PTV Margins

**Lead Investigator:** Vũ Minh Anh  
**Affiliation:** Faculty of Information Technology, Ho Chi Minh City University of Industry and Trade (HUIT)  
**Email:** mvu103536@gmail.com  
**Associated Publication:** *In Silico 4D-CT-Based Tumor Motion Modeling and Quantitative Evaluation of PTV Margins for Lung Radiotherapy Planning* (Computers in Biology and Medicine)  
**Code Repository:** https://github.com/anhvu7123/4d-ct-lung-motion  

---

## 📁 Dataset Inventory

1. **`tumor_trajectories_10phases.csv`**:
   - Contains 3D center-of-mass coordinates ($Z, Y, X$) in millimeters across 10 respiratory phase bins ($T_0 - T_9$) for Regular, Deep, and Irregular breathing patterns.
   - Includes displacement vector distance from the baseline end-expiration state ($T_5$).

2. **`ptv_margin_coverage_analysis.csv`**:
   - Contains target coverage rates ($CR\%$) for uniform PTV margin expansions ($2, 5, 8, 10, 12\text{ mm}$).
   - Reports Minimum $CR$, Mean $CR$, PTV Volume in cubic centimeters (cc), and binary ICRU 62/83 compliance ($CR \ge 95\%$).

3. **`4dct_phantom_tensor_10phases.npz`**:
   - Compressed 4-dimensional volumetric image tensors in Hounsfield Units (HU).
   - Array shape: $(T=10, Z=60, Y=80, X=80)$ with calibrated voxel spacing $\Delta z = 2.0\text{ mm}, \Delta y = 1.5\text{ mm}, \Delta x = 1.5\text{ mm}$.
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
