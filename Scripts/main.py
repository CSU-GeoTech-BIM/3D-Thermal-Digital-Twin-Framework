"""
Batch Universal Kriging hyperparameter search with Bayesian optimization (RSS objective)
and export of summary tables to Excel.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from data_loader import DataLoader
from universal_kriging_bayesian_rss import UniversalKriging2D_Optimizer


class MainProgram:
    """Loads data per elevation, runs optimization, aggregates rows for Excel export."""

    def __init__(
        self,
        path,
        hs,
        n_calls=10,
        n_initial_points=10,
        model="gaussian",
        data_percentage=1.0,
        output_dir=None,
    ):
        self.path = path
        self.hs = hs
        self.n_calls = n_calls
        self.model = model
        self.data_percentage = data_percentage
        self.n_initial_points = n_initial_points
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_new(self):
        results = []
        loader = DataLoader(self.path)

        for h in self.hs:
            data = loader.read_h(h)
            print(data)
            print(f"Loaded data with {len(data)} points for height {h}.")

            optimizer = UniversalKriging2D_Optimizer(
                data,
                model=self.model,
                n_calls=self.n_calls,
                n_initial_points=self.n_initial_points,
                data_percentage=self.data_percentage,
            )

            opt_result = optimizer.optimize()

            res = opt_result["result"]
            result_dict = {
                "Optimizer Type": "Universal",
                "Model": self.model,
                "Height": h,
                "Sill": opt_result["sill"],
                "Range": opt_result["range"],
                "Nugget": opt_result["nugget"],
                "Scaling": opt_result["scaling"],
                "Angle": opt_result["angle"],
                "Combined Objective": opt_result["combined_objective"],
                "RSS": opt_result["rss"],
                "TSS": opt_result["tss"],
                "R_squared": opt_result["r_squared"],
                "Mean Residual": opt_result["mean_residual"],
                "Variance Residual": opt_result["var_residual"],
                "Covariance": opt_result["cov"],
                "n_calls": self.n_calls,
                "n_initial_points": self.n_initial_points,
                "n_iterations": len(res.func_vals) if res is not None else None,
                "best_fun": float(res.fun) if res is not None else None,
            }
            results.append(result_dict)

        safe_model = str(self.model).replace(" ", "_")
        filename = (
            self.output_dir
            / f"kriging_optimization_Universal_{safe_model}_rss_{self.data_percentage}.xlsx"
        )
        df = pd.DataFrame(results)
        df.to_excel(filename, index=False)
        print(f"Results saved to '{filename}'")


if __name__ == "__main__":
    # Point to your multi-sheet borehole Excel (same layout as original project).
    path = Path(__file__).resolve().parent / "data" / "temperature2.xlsx"
    if not path.is_file():
        path = Path(input("Enter full path to temperature Excel file: ").strip().strip('"'))

    model = "gaussian"
    n_calls = 350
    n_initial_points = 200
    heights = np.arange(440.0, 482.2, 0.2)
    data_percentage = 1.0
    models = ["exponential"]

    out_dir = Path(__file__).resolve().parent / "output"

    for variogram_model in models:
        main_program = MainProgram(
            path,
            heights,
            n_calls,
            n_initial_points,
            model=variogram_model,
            data_percentage=data_percentage,
            output_dir=out_dir,
        )
        main_program.run_new()
