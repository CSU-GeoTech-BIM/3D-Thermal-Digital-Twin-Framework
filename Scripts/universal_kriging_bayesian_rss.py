"""
Universal Kriging with leave-one-out cross-validation and Bayesian optimization
(scikit-optimize gp_minimize). The objective minimized is RSS (residual sum of squares).
"""

import numpy as np
from skopt import gp_minimize
from pykrige.uk import UniversalKriging


class UniversalKriging2D_Optimizer:
    """2D Universal Kriging; optimizes variogram and anisotropy parameters."""

    def __init__(
        self,
        data,
        model="gaussian",
        n_calls=10,
        n_initial_points=20,
        alpha=0.2,
        data_percentage=1.0,
    ):
        self.full_data = data
        n_samples = int(len(data) * data_percentage)
        self.data = data[:n_samples]
        self.mo = model
        self.n_calls = n_calls
        self.n_initial_points = n_initial_points
        self.result = None
        self.alpha = alpha

    def KR(self, sill, range_, nugget, scaling, angle, enable_plotting=False):
        """Leave-one-out predictions at observation locations."""
        z_pred = []

        for i in range(len(self.data)):
            data_s = np.delete(self.data, i, axis=0)

            uk = UniversalKriging(
                data_s[:, 0],
                data_s[:, 1],
                data_s[:, 2],
                variogram_model=self.mo,
                variogram_parameters={
                    "sill": sill,
                    "range": range_,
                    "nugget": nugget,
                },
                anisotropy_scaling=scaling,
                anisotropy_angle=angle,
                verbose=False,
                enable_plotting=enable_plotting,
            )

            z, ss = uk.execute("points", self.data[i, 0], self.data[i, 1])

            if ss <= 0 or np.isnan(ss):
                return np.array(np.nan), np.inf

            z_pred.append(z[0])

        return np.array(z_pred)

    def cross_validation(self, z_pred):
        """RSS, TSS, R^2, residual moments, and covariance between observed and predicted."""
        if np.any(np.isnan(z_pred)) or np.any(np.isinf(z_pred)):
            return np.inf, np.inf, np.inf, np.inf, np.inf, np.inf

        t_actu = self.data[:, 2]
        t_pre = z_pred

        rss = np.sum((t_actu - t_pre) ** 2)
        tss = np.sum((t_actu - np.mean(t_actu)) ** 2)
        r_squared = 1 - (rss / tss)

        residuals = t_actu - t_pre
        mean_residual = np.mean(residuals)
        var_residual = np.var(residuals)
        cov = np.cov(t_actu, t_pre)[0, 1]

        return rss, tss, r_squared, mean_residual, var_residual, cov

    def optimize(self):
        """Bayesian optimization over sill, range, nugget, scaling, angle; objective = RSS."""
        space = [
            (1.0, 300.0),
            (100, 3000),
            (0.1, 1.0),
            (1.0, 5.0),
            (0.0, 180.0),
        ]

        def objective_function(params):
            a_big_num = 500
            sill, range_, nugget, scaling, angle = params
            z_pred = self.KR(sill, range_, nugget, scaling, angle)

            if z_pred is None or np.any(np.isnan(z_pred)) or np.any(np.isinf(z_pred)):
                return a_big_num

            rss, _tss, _r2, _mean, _var, _cov = self.cross_validation(z_pred)

            if np.isinf(rss) or np.isnan(rss):
                return a_big_num

            combined_objective = rss
            return combined_objective

        self.result = gp_minimize(
            objective_function,
            space,
            n_calls=self.n_calls,
            random_state=0,
            verbose=True,
            n_initial_points=self.n_initial_points,
        )

        sill, range_, nugget, scaling, angle = self.result.x
        z_pred = self.KR(sill, range_, nugget, scaling, angle)
        rss, tss, r_squared, mean_residual, var_residual, cov = self.cross_validation(
            z_pred
        )

        return {
            "result": self.result,
            "sill": sill,
            "range": range_,
            "nugget": nugget,
            "scaling": scaling,
            "angle": angle,
            "combined_objective": self.result.fun,
            "rss": rss,
            "r_squared": r_squared,
            "mean_residual": mean_residual,
            "var_residual": var_residual,
            "cov": cov,
            "tss": tss,
        }

    def kriging_grid(
        self,
        sill,
        range_,
        nugget,
        scaling,
        angle,
        x_steps=100,
        y_steps=100,
        enable_plotting=False,
    ):
        """Regular grid prediction over the data bounding box."""
        x_min, x_max = np.min(self.data[:, 0]), np.max(self.data[:, 0])
        y_min, y_max = np.min(self.data[:, 1]), np.max(self.data[:, 1])

        x_grid = np.linspace(x_min, x_max, x_steps)
        y_grid = np.linspace(y_min, y_max, y_steps)

        uk = UniversalKriging(
            self.data[:, 0],
            self.data[:, 1],
            self.data[:, 2],
            variogram_model=self.mo,
            variogram_parameters={
                "sill": sill,
                "range": range_,
                "nugget": nugget,
            },
            anisotropy_scaling=scaling,
            anisotropy_angle=angle,
            verbose=False,
            enable_plotting=enable_plotting,
        )

        grid_z, _ = uk.execute("grid", x_grid, y_grid)
        return grid_z, x_grid, y_grid
