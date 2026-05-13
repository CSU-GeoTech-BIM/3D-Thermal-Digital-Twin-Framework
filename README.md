# 3D Thermal Digital Twin Framework for Permafrost

Code and data for the 3D digital reconstruction framework for seasonally frozen tailings integrating BIM and Bayesian Anisotropic Kriging.

This repository provides a reproducible workflow for permafrost thermal analysis and geometric modeling in a BIM-oriented context.  
It combines:

- Python-based Universal Kriging with Bayesian optimization for borehole temperature interpolation.
- Grasshopper workflows for 3D environment temperature field visualization and frozen-ground region display.
- Grasshopper workflow for permafrost model construction.

The repository is organized for paper submission and Data Availability sharing.

## Repository Structure

```text
3D-Thermal-Digital-Twin-Framework/
├─ Data/
│  ├─ temperature.xlsx
│  └─ kriging_optimization_results_Universal_gaussian_consider_rss.xlsx
├─ Grasshopper/
│  ├─ temperature filed construct.gh
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
```

## Workflow Overview

The full workflow has two connected parts:

1. **Numerical interpolation (Python)**  
   Multi-sheet borehole temperature observations are interpolated at target elevations, then Universal Kriging parameters are optimized with Bayesian search.
2. **Modeling and visualization (Grasshopper)**  
   Results are used for BIM-side thermal field visualization and frozen-ground model generation.

## Part A: Python Code (Interpolation + Optimization)

### 1) Environment setup

Recommended Python version: **3.8+**

```bash
cd Scripts
pip install -r requirements.txt
```

Dependencies are listed in `Scripts/requirements.txt`:

- `numpy`
- `pandas`
- `scipy`
- `scikit-learn`
- `scikit-optimize`
- `PyKrige`
- `openpyxl`

### 2) Input data format

The loader expects one workbook with **one sheet per borehole** (default in script: `Scripts/data/temperature2.xlsx`, or manual input path when missing).

In each sheet:

- Data are read from row index `2` onward (the third row in Excel).
- Column index `2`: temperature values.
- Column index `3`: depth/elevation values used for interpolation.
- Row index `2`, column index `4` and `5`: `x`, `y` coordinates.

Important implementation note:

- `Scripts/data_loader.py` uses positional indexing (`iloc`) instead of column names.
- Therefore, Chinese/English header text does **not** affect reading logic, as long as column order is unchanged.

### 3) Main execution

Run:

```bash
cd Scripts
python main.py
```

The script loops over target elevations and variogram models, then writes one result Excel file per model.

Key parameters in `Scripts/main.py`:

- `path`: input workbook path.
- `heights`: target elevation sequence (for example `np.arange(440.0, 482.2, 0.2)`).
- `models`: variogram model list (`gaussian`, `exponential`, `spherical`, etc.).
- `n_calls`: total Bayesian optimization iterations.
- `n_initial_points`: initial random evaluations.
- `data_percentage`: fraction of data used in optimization.

### 4) Algorithm details

`Scripts/universal_kriging_bayesian_rss.py` implements:

- 2D Universal Kriging (`PyKrige.UniversalKriging`).
- Leave-one-out cross-validation at sample points.
- Bayesian optimization (`gp_minimize`) over:
  - sill
  - range
  - nugget
  - anisotropy scaling
  - anisotropy angle
- Objective: minimize **RSS** (residual sum of squares).

Exported metrics include:

- `RSS`, `TSS`, `R_squared`
- residual mean, residual variance, covariance
- best parameter set
- optimization run metadata

Result files are written to `Scripts/output/` with names like:

`kriging_optimization_Universal_<model>_rss_<data_percentage>.xlsx`

## Part B: Grasshopper Files

The `Grasshopper/` folder contains two workflows with distinct roles:

### 1) `temperature filed construct.gh`

Purpose:

- Construct and visualize the **temperature field in a BIM/environment context**.
- Support **frozen-ground region visualization** from thermal information.

Typical use:

- Import geometry/context and thermal data.
- Map/interpolate temperature values to spatial elements.
- Generate colored thermal distribution and identify frozen zones based on threshold logic.

Expected output:

- Temperature field visualization in 3D environment/BIM scene.
- Frozen vs. non-frozen region display for analysis and presentation.

### 2) `mesh model construct.gh`

Purpose:

- Build the **permafrost geometric/mesh model** used for representation and downstream integration.

Typical use:

- Generate or process mesh geometry for frozen-ground bodies.
- Prepare model geometry for coupling with visualization or BIM workflows.

Expected output:

- Structured frozen-ground mesh model suitable for display, export, or further analysis.

## How to Use the Full Pipeline

1. Prepare/update borehole temperature workbook in `Data/`.
2. Run Python scripts in `Scripts/` to generate interpolation and optimization results.
3. Open `Grasshopper/temperature filed construct.gh` to build environment thermal field and frozen-region visualization.
4. Open `Grasshopper/mesh model construct.gh` to generate frozen-ground mesh model.
5. Combine outputs in your BIM/digital-twin presentation workflow.

## Reproducibility Notes

- Keep raw data workbook unchanged and versioned in `Data/`.
- Store script outputs in `Scripts/output/`.
- Record parameter settings used in each run (`model`, `n_calls`, `n_initial_points`, elevation range).
- If header language is changed (Chinese to English), keep sheet layout and column positions unchanged.

## Citation / Data Availability Suggestion

Suggested statement template:

> The data and scripts required to reproduce the permafrost thermal interpolation and model construction workflow are available in this repository.  
> Python scripts for Universal Kriging with Bayesian optimization are provided under `Scripts/`, and Grasshopper definitions for temperature field visualization and permafrost model construction are provided under `Grasshopper/`.
