"""Load borehole temperature sheets from Excel for a given elevation."""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


class DataLoader:
    """Reads multi-sheet Excel where each sheet is one borehole log."""

    def __init__(self, path):
        self.excel_file = pd.ExcelFile(path)
        self.names = self.excel_file.sheet_names

    def read_h(self, h):
        """
        Build (x, y, temperature) samples at elevation h by linear interpolation
        along depth for each borehole whose depth range contains h.
        """
        t = []
        x = []
        y = []

        for i in range(len(self.names)):
            df = self.excel_file.parse(self.names[i])
            datat = df.iloc[2:, 2].tolist()
            datah = df.iloc[2:, 3].tolist()
            h_max = max(datah)
            h_min = min(datah)

            if float(h_min) <= h <= float(h_max):
                m = interp1d(datah, datat, bounds_error=False)
                t.append(m(h))
                # Site-specific coordinate offsets (adjust for your project CRS)
                x.append(df.iloc[2, 4] - 466550 - 143.247864)
                y.append(df.iloc[2, 5] - 5246028 + 3.860982)

        data = np.array([[x[i], y[i], t[i]] for i in range(len(x))])
        return data
