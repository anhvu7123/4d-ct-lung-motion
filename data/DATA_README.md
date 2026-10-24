# 4D-CT synthetic data files

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
