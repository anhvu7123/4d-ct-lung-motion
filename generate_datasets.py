#!/usr/bin/env python3
"""Export reproducible analysis CSVs and separate illustrative CT phantom volumes.

The analysis CSVs come ONLY from simulation_results.json; the example NPZ is
created with an independent fixed seed and MUST NOT be treated as the exact
random phantom draw used in all Monte Carlo trials.
"""
from pathlib import Path
import csv
import json
import numpy as np
from main import generate_dynamic_phantom

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
DATA.mkdir(exist_ok=True)
RESULTS=ROOT/'simulation_results.json'
with RESULTS.open(encoding='utf-8') as f:
    results=json.load(f)

# 1. Simulation-result trajectories, consistent with the main JSON.
with (DATA/'tumor_trajectories_10phases.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['Breathing_Pattern','Phase_Index','Phase_Percentage','Z_Superior_Inferior_mm',
                'Y_Anterior_Posterior_mm','X_Left_Right_mm','Displacement_From_T6_mm'])
    for scenario in ('regular','deep','irregular'):
        centroids=np.asarray(results['scenarios'][scenario]['centroids_true'])
        ref=centroids[6]
        for t,c in enumerate(centroids):
            w.writerow([scenario.capitalize(),f'T{t}',f'{t*10}%',*(f'{x:.4f}' for x in c),
                        f'{np.linalg.norm(c-ref):.4f}'])

# 2. Frozen planning PTV, evaluated independently in each deterministic scenario.
with (DATA/'ptv_margin_coverage_analysis.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['Breathing_Pattern','Strategy','PTV_Volume_cc','Min_Geometric_Coverage_Pct',
                'Mean_Geometric_Coverage_Pct','Pass_Study_Threshold_95',*[f'T{t}_CR_Pct' for t in range(10)]])
    for scenario in ('regular','deep','irregular'):
        for strategy,dat in results['scenarios'][scenario]['evaluated_planning_ptvs'].items():
            vol=results['planning_strategies'][strategy]['ptv_volume_cc']
            w.writerow([scenario.capitalize(),strategy,f'{vol:.3f}',f"{dat['min_coverage']:.3f}",
                        f"{dat['mean_coverage']:.3f}", 'YES' if dat['pass_threshold_95'] else 'NO',
                        *(f'{c:.3f}' for c in dat['coverages'])])

# 3. Example CT phantom, same anatomy/grid but generated independently of
# the JSON trials. This is intentionally labeled as an illustrative example.
arrays={}
np.random.seed(20261024)
for scenario in ('regular','deep','irregular'):
    volumes,masks,spacing,gt=generate_dynamic_phantom(scenario=scenario,
                            nz=70,ny=90,nx=90,dz=2.0,dy=1.5,dx=1.5)
    arrays['vols_'+scenario]=volumes
    arrays['masks_'+scenario]=masks
    arrays['centroids_'+scenario+'_mm']=np.asarray(gt)
arrays['voxel_spacing_mm']=np.asarray(spacing)
arrays['reference_phase']=np.asarray(6)
np.savez_compressed(DATA/'4dct_phantom_tensor_10phases.npz',**arrays)

(DATA/'DATA_README.md').write_text('''# 4D-CT synthetic data files

All arrays are **synthetic** and **not patient CT scans**. They are not proof of
clinical efficacy or a substitute for dose calculations.

- `tumor_trajectories_10phases.csv`: Exact analytical centroid trajectories
  in `simulation_results.json`, referenced to **T6** (end expiration).
- `ptv_margin_coverage_analysis.csv`: All nominal frozen-planning PTV
  evaluations under three deterministic breathing scenarios from the same JSON.
  Pass means **study-defined geometric CR >= 95%**, not ICRU dosimetric compliance.
- `4dct_phantom_tensor_10phases.npz`: An **independent illustrative phantom**
  generated with seed 20261024, containing 10 phases with shape
  `(10,70,90,90)` and voxel spacing `(2.0,1.5,1.5)` mm. The NPZ includes its
  own centroid trajectories `centroids_{regular,deep,irregular}_mm`, since the
  irregular example is a distinct random realization from the paper's deterministic
  scenario. The NPZ and Monte Carlo outcomes should not be mistaken as a
  single shared random draw.

Recreate from the project root:
```bash
python3 main.py
python3 generate_datasets.py
```
The `simulation_results.json` is the canonical statistical output; re-running
may change results if the simulation implementation or dependencies change.
''',encoding='utf-8')
print('Wrote synchronized CSV analysis and independently labeled illustrative phantom to',DATA)
