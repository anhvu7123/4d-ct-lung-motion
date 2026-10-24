#!/usr/bin/env python3
"""Read-only sanity-check of CSVs and JSON; never modifies project files."""
from pathlib import Path
import csv,json,math,re,sys
import numpy as np

root=Path(__file__).resolve().parent
err=[]
def ck(cond,msg):
    if not cond:err.append(msg)
with (root/'simulation_results.json').open(encoding='utf-8') as f:r=json.load(f)
main=r['monte_carlo']['irregular_unseen']
sub=r['subvoxel_sensitivity']
setup=r['setup_uncertainty']
for name,z in sub['targets'].items():
    p1,p2=z['discrete_pass_rate_pct'],z['subvoxel_pass_rate_pct']
    ck(abs((p2-p1)-z['pass_rate_difference_pct'])<1e-7,f'subvoxel pass delta: {name}')
    ck(abs((z['subvoxel_mean_min_cr']-z['discrete_mean_min_cr'])-z['mean_cr_difference_pp'])<1e-6,
       f'subvoxel mean CR delta: {name}')
    x,y=z.get('raw_discrete_min_cr_per_cycle'),z.get('raw_subvoxel_min_cr_per_cycle')
    ck(x is not None and y is not None and len(x)==len(y)==sub['n_cycles'],f'missing paired cycles: {name}')
    if x and y:
        a,b=np.asarray(x),np.asarray(y)
        ck(abs(100*np.mean(a>=95)-p1)<1e-8,f'wrong discrete pass numerator: {name}')
        ck(abs(100*np.mean(b>=95)-p2)<1e-8,f'wrong subvoxel pass numerator: {name}')
        ck(abs(np.mean(abs(a-b))-z['cr_mean_abs_error_pct'])<1e-6,f'wrong paired CR MAE: {name}')
for reg,nfr in [('sbrt_3fx',3),('sbrt_5fx',5),('cfrt_30fx',30)]:
 for name,z in setup[reg].items():
    raw=z.get('raw_fraction_cr_by_patient')
    ck(raw is not None and len(raw)==200 and all(len(x)==nfr for x in raw),
        f'patient-by-fraction values unavailable: {reg}/{name}')
    if raw:
        a=np.asarray(raw)
        ck(abs(100*np.mean(a>=95)-z['fraction_pass_rate_pct'])<1e-8,f'fraction pass: {reg}/{name}')
        flattened=np.asarray(z.get('raw_fraction_crs',[]))
        ck(len(flattened)==200*nfr and np.allclose(flattened,a.reshape(-1)),
           f'full fraction trace (no 300-fraction truncation): {reg}/{name}')
        ck(abs(100*np.mean(np.mean(a>=95,axis=1)>=0.90)-z['patient_course_avg_success_pct'])<1e-8,
           f'exploratory >=90%-fraction course pass: {reg}/{name}')
        ck(abs(100*np.mean(np.all(a>=95,axis=1))-z['patient_all_fraction_success_pct'])<1e-8,
           f'all-pass: {reg}/{name}')
        ck(z['fraction_pass_cluster_boot_ci_95'][0]<=z['fraction_pass_rate_pct']<=z['fraction_pass_cluster_boot_ci_95'][1],
           f'bootstrap interval excludes estimate: {reg}/{name}')
ck(r.get('metadata',{}).get('figure_evaluation',{}).get('figure6A_values_per_strategy')==6000,
   'figure 6A metadata must state n=6000')
ck(r.get('metadata',{}).get('figure_evaluation',{}).get('figure5_mc_cycles_per_amplitude_per_strategy')==500,
   'figure 5 metadata must state n=500 per amplitude per strategy')
with (root/'data'/'tumor_trajectories_10phases.csv').open(newline='') as f:
  traj=list(csv.DictReader(f))
ck(len(traj)==30,'trajectory csv requires 3 x 10 phases')
for row in traj:
  if row['Phase_Index']=='T6':ck(abs(float(row['Displacement_From_T6_mm']))<1e-6,'T6 not zero')
with (root/'data'/'ptv_margin_coverage_analysis.csv').open(newline='') as f:
  rows=list(csv.DictReader(f))
ck(len(rows)==3*len(r['planning_strategies']), 'coverage csv missing strategies/scenarios')
for row in rows:
  sc=row['Breathing_Pattern'].lower(); k=row['Strategy']
  truth=r['scenarios'][sc]['evaluated_planning_ptvs'][k]
  ck(abs(float(row['Min_Geometric_Coverage_Pct'])-truth['min_coverage'])<0.001,
      f'coverage csv mismatch: {sc}/{k}')
with np.load(root/'data'/'4dct_phantom_tensor_10phases.npz') as z:
  ck(z['vols_regular'].shape==(10,70,90,90),'example NPZ wrong shape')
  ck(int(z['reference_phase'])==6,'example NPZ wrong reference phase')
# The editable manuscript and README must agree with the regenerated primary results.
from docx import Document
word=Document(root/'manuscript.docx')
word_text=' '.join(p.text for p in word.paragraphs)
readme_text=(root/'README.md').read_text(encoding='utf-8')
for nm in ('ITV + 3mm setup', 'ITV + 5mm setup'):
    reported=f"{r['monte_carlo']['irregular_unseen'][nm]['pct_pass_95']:.1f}%"
    ck(reported in word_text, f'paper missing current irregular pass result: {nm}, {reported}')
    ck(reported in readme_text, f'README missing current irregular pass result: {nm}, {reported}')
for nm in ('ITV + 3mm setup', 'ITV + 5mm setup'):
    reported=f"{r['subvoxel_sensitivity']['targets'][nm]['subvoxel_pass_rate_pct']:.1f}%"
    ck(reported in word_text, f'paper missing current sub-voxel result: {nm}, {reported}')
    ck(reported in readme_text, f'README missing current sub-voxel result: {nm}, {reported}')

for required in ['manuscript.docx','manuscript.pdf','README.md','LICENSE','main.py']:
 ck((root/required).exists(),'missing required '+required)
if err:
 print('FAILED:',*err,sep='\n - ');sys.exit(1)
print('PASS: JSON raw fraction and sub-voxel measurements verified; CSV tables and phantom reference verified.')
print('Main irregular pass ITV+3 / ITV+5:',main['ITV + 3mm setup']['pct_pass_95'],main['ITV + 5mm setup']['pct_pass_95'])
print('CFRT 30fx pass ITV+5:',setup['cfrt_30fx']['ITV + 5mm setup']['fraction_pass_rate_pct'])
