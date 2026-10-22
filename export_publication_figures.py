#!/usr/bin/env python3
"""
Publication Figure Generator for Computers in Biology and Medicine (Elsevier)
Author: Vu Minh Anh
Exports:
  - Figure_1.png (3D Trajectory Decomposition across 10 Phases at 300 DPI)
  - Figure_2.png (PTV Margin Coverage Degradation curves at 300 DPI)
  - Figure_3.png (3D Marching Cubes Anatomical Surface Reconstruction at 300 DPI)
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['lines.linewidth'] = 1.8

output_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Load Simulation Results
with open(os.path.join(output_dir, "simulation_results.json"), "r") as f:
    data = json.load(f)

# FIGURE 1: 3D Trajectory Decomposition across 10 Phases (300 DPI)
print("Generating Figure 1 (3D Kinematic Trajectories @ 300 DPI)...")
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=False)

phases = np.arange(10)
scenarios = [('regular', 'Regular Breathing', '#1f77b4'),
             ('deep', 'Deep Breathing', '#d62728'),
             ('irregular', 'Irregular Breathing', '#2ca02c')]

for idx, (sc_key, sc_name, col) in enumerate(scenarios):
    ax = axes[idx]
    centroids = np.array(data[sc_key]['centroids']) # [Z, Y, X]
    
    disp_z = centroids[:, 0] - centroids[5, 0]
    disp_y = centroids[:, 1] - centroids[5, 1]
    disp_x = centroids[:, 2] - centroids[5, 2]
    
    ax.plot(phases, disp_z, 'o-', color='#1f77b4', label=r'SI ($Z$ - Craniocaudal)', lw=2.2, ms=6)
    ax.plot(phases, disp_y, 's--', color='#ff7f0e', label=r'AP ($Y$ - Anteroposterior)', lw=1.8, ms=5)
    ax.plot(phases, disp_x, '^:', color='#2ca02c', label=r'LR ($X$ - Left-Right)', lw=1.8, ms=5)
    
    ax.set_title(f'({chr(97+idx)}) {sc_name}', fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel(r'Respiratory Phase Bin ($T_0 - T_9$)', fontsize=10)
    ax.set_ylabel(r'Displacement Relative to $T_5$ (mm)', fontsize=10)
    ax.set_xticks(phases)
    ax.set_xticklabels([f'$T_{{{i}}}$' for i in phases])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.axhline(0, color='gray', lw=0.8, linestyle='-')
    if idx == 0:
        ax.legend(frameon=True, fontsize=9, loc='upper left')

plt.tight_layout()
fig_1_path = os.path.join(output_dir, "Figure_1.png")
plt.savefig(fig_1_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  -> Saved: {fig_1_path}")

# FIGURE 2: PTV Coverage Curves vs Margins (300 DPI)
print("Generating Figure 2 (PTV Coverage vs Margin @ 300 DPI)...")
fig, ax = plt.subplots(figsize=(8, 5.5))

margins = [2, 5, 8, 10, 12]
colors = {'regular': '#1f77b4', 'deep': '#d62728', 'irregular': '#2ca02c'}
markers = {'regular': 'o', 'deep': 's', 'irregular': '^'}
labels = {'regular': 'Regular Breathing', 'deep': 'Deep Breathing', 'irregular': 'Irregular Breathing'}

for sc_key in ['regular', 'deep', 'irregular']:
    min_crs = [data[sc_key]['ptv_results'][str(m)]['min_coverage'] for m in margins]
    ax.plot(margins, min_crs, marker=markers[sc_key], color=colors[sc_key],
            label=f"{labels[sc_key]} (Min CR)", lw=2.2, ms=7)

ax.axhline(95.0, color='#d62728', linestyle='--', lw=2.0, label='ICRU 62/83 Threshold (CR >= 95%)')
ax.axvline(5.0, color='gray', linestyle=':', lw=1.5, label='Conventional 5 mm Static Margin')

ax.set_title('Figure 2: Empirical Target Coverage (%) vs. PTV Margin', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Uniform PTV Margin Expansion (mm)', fontsize=11)
ax.set_ylabel('Minimum Target Coverage Rate (%)', fontsize=11)
ax.set_xticks(margins)
ax.set_ylim(-2, 105)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, fontsize=9.5, loc='lower right')

plt.tight_layout()
fig_2_path = os.path.join(output_dir, "Figure_2.png")
plt.savefig(fig_2_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  -> Saved: {fig_2_path}")

# FIGURE 3: 3D Marching Cubes Surface Reconstruction (300 DPI)
print("Generating Figure 3 (3D Marching Cubes Reconstruction @ 300 DPI)...")
from main import generate_dynamic_phantom

vols, masks, spacing, _ = generate_dynamic_phantom(scenario='regular', nz=50, ny=70, nx=70)
ref_vol = vols[5]
tumor_insp = masks[0]
tumor_exp = masks[5]

verts_bone, faces_bone, _, _ = measure.marching_cubes(ref_vol, level=300, spacing=spacing)
verts_t5, faces_t5, _, _ = measure.marching_cubes(tumor_exp.astype(float), level=0.5, spacing=spacing)
verts_t0, faces_t0, _, _ = measure.marching_cubes(tumor_insp.astype(float), level=0.5, spacing=spacing)

fig = plt.figure(figsize=(9, 7.5))
ax = fig.add_subplot(111, projection='3d')

mesh_bone = Poly3DCollection(verts_bone[faces_bone], alpha=0.18, facecolor='#64748b', edgecolor='none')
ax.add_collection3d(mesh_bone)

mesh_t5 = Poly3DCollection(verts_t5[faces_t5], alpha=0.75, facecolor='#0ea5e9', edgecolor='#0284c7')
ax.add_collection3d(mesh_t5)

mesh_t0 = Poly3DCollection(verts_t0[faces_t0], alpha=0.75, facecolor='#ef4444', edgecolor='#b91c1c')
ax.add_collection3d(mesh_t0)

ax.set_xlim(0, 70 * spacing[2])
ax.set_ylim(0, 70 * spacing[1])
ax.set_zlim(0, 50 * spacing[0])

ax.set_xlabel('LR (X) Axis (mm)', fontsize=9, labelpad=8)
ax.set_ylabel('AP (Y) Axis (mm)', fontsize=9, labelpad=8)
ax.set_zlabel('SI (Z) Axis (mm)', fontsize=9, labelpad=8)
ax.set_title('Figure 3: 3D Marching Cubes Surface Rendering of Thoracic Structures and Target Excursion',
             fontsize=11, fontweight='bold', pad=15)
ax.view_init(elev=22, azim=45)

plt.tight_layout()
fig_3_path = os.path.join(output_dir, "Figure_3.png")
plt.savefig(fig_3_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  -> Saved: {fig_3_path}")

print("\n[SUCCESS] All 3 publication figures exported at 300 DPI in compliance with Elsevier standards!")
