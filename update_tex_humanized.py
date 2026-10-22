import os
import re

output_dir = os.path.dirname(os.path.abspath(__file__))
tex_path = os.path.join(output_dir, "manuscript.tex")

with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

new_abs = r"""\begin{abstract}
Target motion during thoracic radiation therapy induces spatial misalignment between planned beam apertures and mobile tumor volumes. Current commercial treatment planning systems (TPS) utilize proprietary margin expansion modules that often treat intrafractional motion as an isotropic uncertainty. In this study, we developed an open-source Python computational pipeline to track 3D tumor centroid trajectories across ten-phase 4D-CT volumes and quantify target coverage under uniform planning target volume (PTV) margin expansions. A calibrated spatiotemporal thorax tensor $(T, Z, Y, X)$ with voxel spacing of $2.0 \times 1.5 \times 1.5\text{ mm}^3$ was synthesized across respiratory phases $T_0$ to $T_9$. Solid tumor volumes were segmented via intensity thresholding ($-300$ to $+150\text{ HU}$) and tracked using spatial moments across regular, deep, and irregular breathing patterns. Empirical target coverage rates ($CR$) for margins of $2$, $5$, $8$, $10$, and $12\text{ mm}$ were benchmarked against the analytical van Herk formula ($2.5\Sigma + 0.7\sigma$) and ICRU 62/83 consensus criteria ($CR \ge 95\%$). Tumor excursion was dominated by craniocaudal displacement, with peak-to-peak amplitudes of $12.00\text{ mm}$ (regular), $22.00\text{ mm}$ (deep), and $14.58\text{ mm}$ (irregular), whereas lateral and anteroposterior excursions remained below $6.07\text{ mm}$. Under regular respiration, a $12\text{ mm}$ margin achieved $98.4\%$ minimum coverage. However, the standard $5\text{ mm}$ clinical margin exhibited severe geometric miss under deep ($CR = 9.5\%$) and irregular breathing ($CR = 52.6\%$). These quantitative findings confirm that uniform 3D margin expansions are suboptimal for tumors with craniocaudal excursions exceeding $10\text{ mm}$, demonstrating the necessity of patient-specific anisotropic margins or active motion mitigation techniques consistent with AAPM Task Group 76 guidelines.
\end{abstract}"""

content = re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}', lambda m: new_abs, content, flags=re.DOTALL)

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(content)
print("[SUCCESS] manuscript.tex updated with humanized abstract.")
