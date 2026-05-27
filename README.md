# A Bayesian-Optimized Scan-to-Simulation Framework for 3D Thermal Digital Twins of Seasonally Frozen Tailings

This repository contains the source code, data, and parametric models for the 3D digital reconstruction framework of seasonally frozen tailings. By integrating Bayesian-optimized anisotropic Kriging with Building Information Modeling (BIM), this repository provides a reproducible, data-driven workflow for spatial thermal analysis and topological geometric reconstruction in a digital twin context.

The workflow seamlessly bridges spatial geostatistics and numerical simulation. It combines:
- **Python-based Universal Kriging** with Bayesian optimization for automated, objective borehole temperature interpolation.
- **Grasshopper/Rhino parametric workflows** for 3D thermal field visualization and automated watertight mesh generation of seasonally frozen zones.

This repository is organized to support the methodology and Data Availability statement of our related manuscript.

---

## Repository Structure

```text
3D-Thermal-Digital-Twin-Framework/
├─ Data/
│  ├─ temperature.xlsx
│  └─ kriging_optimization_results_Universal_gaussian_consider_rss.xlsx
├─ Grasshopper/
│  ├─ temperature field construct.gh
│  └─ mesh model construct.gh
├─ Scripts/
│  ├─ main.py
│  ├─ data_loader.py
│  ├─ universal_kriging_bayesian_rss.py
│  ├─ requirements.txt
│  ├─ README.md
│  ├─ data/
│  └─ output/
└─ README.md
