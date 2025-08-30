import numpy as np
import pandas as pd


def generate_3d_data(n_points: int = 50) -> pd.DataFrame:

    t = np.linspace(0, 4 * np.pi, n_points)
    x = np.cos(t)
    y = np.sin(t)
    z = t
    return pd.DataFrame({"x": x, "y": y, "z": z})
