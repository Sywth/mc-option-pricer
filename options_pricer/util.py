import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from plotly.subplots import make_subplots

from typing import NewType
from typing import Literal

# Define sentinels and consts
NpFloatType = np.float64
OptionType = Literal["call", "put"]
TRADING_DAYS_TO_YEARS = 1 / 252
TRADING_YEARS_TO_DAYS = 252
SEED = 2025


# Auxiliary Functions
def erf(x: np.ndarray) -> np.ndarray:
    # from https://www.johndcook.com/blog/python_erf/

    # constants
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    # Abramowitz Stegun formula formula for approxiating erf(x)
    abs_x = np.abs(x)
    t = 1.0 / (1.0 + p * abs_x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * np.exp(
        -abs_x * abs_x
    )

    return np.sign(x) * y


def std_norm_cdf(x: np.ndarray) -> np.ndarray:
    """
    Returns the cumulative distribution function (CDF) of the standard normal distribution.
    """
    return 0.5 * (1 + erf(x / np.sqrt(2)))


def std_norm_pdf(x: np.ndarray) -> np.ndarray:
    """
    Returns the probability density function (PDF) of the standard normal distribution.
    """
    return np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)
