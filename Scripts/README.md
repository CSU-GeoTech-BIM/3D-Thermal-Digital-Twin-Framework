# Universal Kriging with Bayesian optimization (RSS objective)

**Leave-one-out Universal Kriging** with **Bayesian optimization** (`scikit-optimize` `gp_minimize`) over variogram and anisotropy parameters. The minimized objective is **RSS** (residual sum of squares from cross-validation). Summary tables are written to **Excel** under `output/`.

## Method

1. For each target elevation, borehole logs are read from a multi-sheet Excel file and linearly interpolated to that elevation (`data_loader.py`).
2. `UniversalKriging2D_Optimizer` (`universal_kriging_bayesian_rss.py`) evaluates leave-one-out predictions at sample locations for each candidate parameter set, computes RSS, and runs `gp_minimize` on RSS.
3. `main.py` loops over elevations (and optionally variogram models), collects metrics, and exports one spreadsheet per model run.

## Requirements

- Python 3.8+

```bash
pip install -r requirements.txt
```

## Input data

- One Excel workbook, **one sheet per borehole**.
- Per sheet: from row index 2 onward, column 2 = temperature, column 3 = depth/height; row 2, columns 4–5 = borehole x, y (with optional CRS offsets in `data_loader.py`—adjust if your coordinates differ).

Default input path: `data/temperature2.xlsx`. If missing, `main.py` prompts for a path.

## Usage

```bash
python main.py
```

Configure in the `if __name__ == "__main__"` block of `main.py`:

- `path`: workbook path
- `heights`: elevations (e.g. `np.arange(440.0, 482.2, 0.2)`)
- `models`: PyKrige variogram names (`"gaussian"`, `"spherical"`, `"exponential"`, …)
- `n_calls`, `n_initial_points`: optimization budget

Output file pattern:

`output/kriging_optimization_Universal_<model>_rss_<data_fraction>.xlsx`

Exported columns include sill, range, nugget, scaling, angle, RSS, TSS, R², residual mean/variance, covariance, and run metadata (`n_calls`, `best_fun`, iteration count).

## Files

| File | Role |
|------|------|
| `main.py` | Batch over heights, write Excel |
| `universal_kriging_bayesian_rss.py` | UK, LOO CV, `gp_minimize`, RSS objective |
| `data_loader.py` | Excel → `(x, y, T)` at height `h` |
| `requirements.txt` | Dependencies |
| `output/` | Excel exports (created if needed) |
