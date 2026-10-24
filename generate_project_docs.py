#!/usr/bin/env python3
"""Regenerate project README.md and local report.html from canonical JSON."""
from pathlib import Path
import json,html

root=Path(__file__).resolve().parent
r=json.loads((root/'simulation_results.json').read_text(encoding='utf-8'))
plan=r['planning_strategies'];m=r['monte_carlo']['irregular_unseen'];setup=r['setup_uncertainty'];sub=r['subvoxel_sensitivity']
strategies=['Isotropic 5mm','Isotropic 12mm','ITV + 2mm setup','ITV + 3mm setup','ITV + 4mm setup','ITV + 5mm setup','Anisotropic (Mid-pos + 2mm setup)','Anisotropic (Mid-pos + 3mm setup)']

def f(x):return f'{x:.1f}'
def br(z):return f"{f(z[0])}–{f(z[1])}"
def mdstr(s):return s.replace('setup','').replace(' (Mid-pos +',' (Mid-pos +')
def fmt(strategy):
 p=plan[strategy];x=m[strategy];s5=setup['sbrt_5fx'][strategy];s30=setup['cfrt_30fx'][strategy]
 return f'| {strategy} | {f(p["ptv_volume_cc"])} | {f(p["min_coverage"])}% | {f(x["pct_pass_95"])}% ({br(x["pct_pass_wilson_ci_95"])}%) | {f(s5["patient_all_fraction_success_pct"])}% ({br(s5["patient_all_pass_wilson_ci_95"])}%) | {f(s30["fraction_pass_rate_pct"])}% ({br(s30["fraction_pass_cluster_boot_ci_95"])}%) |'
rows='\n'.join(fmt(k) for k in strategies)
subrows='\n'.join(f'| {k} | {f(v["discrete_pass_rate_pct"])}% | {f(v["subvoxel_pass_rate_pct"])}% | {v["pass_rate_difference_pct"]:+.1f} pp | {f(v["cr_mean_abs_error_pct"])} pp |'
 for k,v in sub['targets'].items())
readme=f'''# 4D-CT lung tumor motion: reproducible synthetic simulation

**Author:** Vu Minh Anh, Faculty of Information Technology, HUIT, Vietnam  
**Code:** https://github.com/anhvu7123/4d-ct-lung-motion  
**License:** MIT (see `LICENSE`)  
**Scope:** *In silico* geometry and setup uncertainty. **Not patient imaging, treatment advice, or 4D absorbed-dose validation.**

## What's in this project

- `main.py`: entire synthetic phantom, 10-phase respiratory trajectories (T6 end-exhalation), PTV construction, Monte Carlo robustness, 200 simulated patients per regimen, full patient x fraction CR outcomes, cluster-bootstrap CI, and paired sub-voxel sensitivity evaluation.
- `simulation_results.json`: **canonical computed result**. Contains raw 1,000-cycle discrete / point-cloud comparisons and 200 x 3/5/30 fraction CR arrays for reproducible auditing.
- `manuscript.docx`, `manuscript.pdf`: corrected research manuscript reporting model limitations.
- `fig1_phantom.png` … `fig6_setup_uncertainty.png`: six regenerated analysis figures.
- `generate_datasets.py`: creates `data/` CSV analysis exports and an independently seeded illustrative 4D phantom NPZ.
- `generate_project_docs.py`: refreshes this README and `report.html` from the **current** JSON.
- `validate_project.py`: checks sub-voxel paired cycles, fraction denominators, bootstrap intervals, trajectory T6 and consistency of exported data.
- `submission/`: graphical abstract, cover letter, highlights, suggested reviewers. Keep these separate from analysis code.
- `RUN_ON_MAC.command`: installs dependencies inside a local virtual environment, reruns the pipeline and validation.
- `.git/`: original Git history preserved; removed historical generation scripts remain recoverable from Git or the separately provided backup archive.

## Run locally on macOS

```bash
cd /path/to/lung_4dct_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
python generate_datasets.py
python generate_project_docs.py
python validate_project.py
```

Or run `bash RUN_ON_MAC.command` from this folder in Terminal. No admin privileges required. No folders elsewhere on the Mac are modified. It overwrites **generated outputs in this project only**. Keep a ZIP backup before rerunning a changed model.

**Exact models:** ten 4D-CT phases, 60% model expiration T0→T6 and 40% inspiration T6→T0; normalized power-law motion with a 36° phase shift. Physical voxel spacing 2.0 x 1.5 x 1.5 mm. Lesion radii 8, 12 and 16 mm. Target envelope on planning 4D-CT then held fixed in unseen test cycles. Threshold `min_t CR_t >= 95%` is **study-defined geometric overlap only**, not ICRU dosimetry.

**Sample sizes and uncertainty:** 5,000 main Monte Carlo cycles; multi-lesion sensitivity 2,000 each; 1,000 paired sub-voxel cycles with 2,500 lesion points each. Three separately seeded setup cohorts each have 200 virtual patients: SBRT 3 fractions (600 simulated sessions, seed 42), SBRT 5 fractions (1,000, seed 43), CFRT 30 fractions (6,000, seed 44): total 7,600 sessions. Systematic and random setup uncertainties modeled with 2.0 mm per-axis SD, with patient-specific systematic shift fixed across fractions. No CBCT correction simulated.

## Key simulation outputs (regenerated from current JSON)

| Strategy | Volume (cc) | Planning min CR | Irregular cycle pass (95% Wilson CI) | SBRT 5-fx patient all-pass (95% Wilson CI) | CFRT 30-fx fraction pass (95% patient cluster bootstrap) |
|---|---:|---:|---:|---:|---:|
{rows}

**Different denominators matter:** "fraction pass" counts simulated fractions; "all-pass" counts complete simulated patient courses. Neither is a dose-to-target endpoint.

**Figure 5:** Seven SI amplitude settings (10, 12, 14, 16, 18, 20 and 22 mm) were evaluated with **500 newly simulated cycles per amplitude per strategy**. Different strategies did not share identical amplitude-trial trajectories in that stress test, so error bars are not paired comparisons.

**Figure 6A:** Each box uses the **entire** 200-patient × 30-fraction CFRT minimum-CR matrix = **6,000 observations per strategy**. No first-300-fractions truncation. Within-patient dependence means the boxplot describes simulated fractions and is not an independent-patient confidence interval.

**Figure 6B:** The plotted patient-level endpoint is identical in definition for all three distinct cohorts: **every fraction passes CR ≥95%** (3/3 SBRT, 5/5 SBRT, or 30/30 CFRT). Its interpretation depends on course length; cohorts are not paired. An alternative exploratory CFRT course-level threshold of **at least 27/30 passing fractions (90%)** is also stored in JSON under `patient_course_avg_success_pct` but is **not plotted** alongside the all-pass bars because it is a different endpoint. For ITV + 5 mm, CFRT all-pass is **6.5%**, while exploratory ≥27/30 course-pass is **46.5%**. This threshold is a simulation design choice, not a validated clinical/dosimetric criterion.

### Quantization sensitivity: two *different* evaluators

The discrete approach rounds the centroid to a grid voxel; the point-cloud approach samples lesion points at continuous offsets but still queries a voxelized PTV mask. The latter **is not a truly continuous ground truth**. The two approaches were compared on the same 1,000 cycles; one percentage point (pp) is the difference between two pass percentages.

| Strategy | Discrete pass | Point-cloud pass | Pass-rate difference | Mean paired min-CR absolute error |
|---|---:|---:|---:|---:|
{subrows}

Main caution: ITV + 5 mm changes from **{f(sub['targets']['ITV + 5mm setup']['discrete_pass_rate_pct'])}%** discrete to **{f(sub['targets']['ITV + 5mm setup']['subvoxel_pass_rate_pct'])}%** sampled point-cloud pass. Therefore, quantization *can* change a 95%-pass interpretation. Paired bootstrap intervals and full per-cycle data are provided, but point-count convergence and true continuous-domain validation remain outstanding.

## Data files

`data/tumor_trajectories_10phases.csv` and `data/ptv_margin_coverage_analysis.csv` are exported from **this JSON** and use reference phase **T6**; older T5-based exports should not be mixed in. `data/4dct_phantom_tensor_10phases.npz` is a separately seeded, representative phantom example; its `centroids_*` correspond to **its own** generated tensor, not the irregular JSON scenario.

## Important limitations

Rigid spherical tumor model, synthetic and assumption-dependent distributions, no patient CT validation, no deformable registration, no 4D absorbed dose accumulation, no lung V20 / MLD, no CBCT corrections, and no demonstration that 2,500 points converge for near-boundary coverage. The observed pass proportions must **not** be interpreted as clinical tumor-control rates. The van Herk formula is only a theoretical comparator, not a direct criterion for pass/fail of geometric CR.

**Publication integrity:** All shown results are computed on synthetic inputs. No patient data. Do not claim this code has established clinical necessity of any universal PTV margin, or that an article is published before confirmation from its publisher. For submission, archive a versioned code commit and matched JSON/PDF/Word together.
'''
(root/'README.md').write_text(readme,encoding='utf-8')
# Offline portable HTML summary; all values come from the same JSON.
tds='\n'.join('<tr>'+''.join(f'<td>{html.escape(x)}</td>' for x in [k,f(plan[k]['ptv_volume_cc']),f(plan[k]['min_coverage']),f(m[k]['pct_pass_95']),f(setup['sbrt_5fx'][k]['patient_all_fraction_success_pct']),f(setup['cfrt_30fx'][k]['fraction_pass_rate_pct'])])+'</tr>' for k in strategies)
page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>4D-CT synthetic simulation report</title><style>
body{{font:16px system-ui,-apple-system,Arial,sans-serif;color:#233047;background:#f5f7fb;margin:auto;max-width:1100px;padding:32px}}
article{{background:#fff;border-radius:14px;padding:24px;box-shadow:0 6px 22px #0012}}h1{{color:#123c67}}table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{border:1px solid #d9e2ef;padding:9px;text-align:left}}th{{background:#edf3fd}}.note{{background:#fff5dc;padding:12px;border-left:4px solid #d18b1b}}img{{max-width:100%;margin:14px 0}}</style></head><body><article>
<h1>4D-CT lung simulation — local report</h1><p>Vu Minh Anh · HUIT · synthetic 10-phase phantom · 200 patients/regimen · 7,600 simulated sessions</p>
<p class="note"><b>Research prototype, not medical guidance.</b> The threshold is geometric CR≥95%, not dose. Neither CBCT correction nor tumor control is calculated.</p>
<h2>Numerical summary — current simulation_results.json</h2><table><thead><tr><th>Strategy</th><th>Volume cc</th><th>Planning min CR %</th><th>Irregular cycle pass %</th><th>SBRT 5-fx all-pass %</th><th>CFRT fraction pass %</th></tr></thead><tbody>{tds}</tbody></table>
<h2>Sub-voxel sensitivity</h2><p>ITV + 3 mm: discrete {f(sub['targets']['ITV + 3mm setup']['discrete_pass_rate_pct'])}% vs point-cloud {f(sub['targets']['ITV + 3mm setup']['subvoxel_pass_rate_pct'])}%. ITV + 5 mm: discrete {f(sub['targets']['ITV + 5mm setup']['discrete_pass_rate_pct'])}% vs point-cloud {f(sub['targets']['ITV + 5mm setup']['subvoxel_pass_rate_pct'])}%. The point-cloud estimator queries a voxelized mask; it is not an exact continuous truth.</p>
<h2>Figures</h2>'''+''.join(f'<img loading="lazy" src="fig{i}_{name}.png" alt="Figure {i}">' for i,name in [(1,'phantom'),(2,'trajectory'),(3,'coverage'),(4,'tradeoff'),(5,'robustness_amplitude'),(6,'setup_uncertainty')])+'''<p><small>Rebuild by running main.py, generate_datasets.py, generate_project_docs.py and validate_project.py.</small></p></article></body></html>'''
(root/'report.html').write_text(page,encoding='utf-8')
print('Updated README.md and report.html from',root/'simulation_results.json')
