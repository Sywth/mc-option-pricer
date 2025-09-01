import numpy as np
from .util import OptionType, std_norm_cdf, std_norm_pdf


def d1_term(S, K, r, T, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def d2_term(S, K, r, T, sigma):
    return d1_term(S, K, r, T, sigma) - sigma * np.sqrt(T)


def black_sholes(
    interest_rate: float,
    strike_price: float,
    underlying_price: np.ndarray,
    time_to_maturity_years: np.ndarray,
    volatility: float,
    option_type: OptionType,
) -> float:
    # Extract the terms
    r = interest_rate
    K = strike_price
    S = underlying_price
    T = time_to_maturity_years  # cast to years
    sigma = volatility

    # Calculate d1 and d2
    d1 = d1_term(S, K, r, T, sigma)
    d2 = d2_term(S, K, r, T, sigma)

    if option_type == "call":
        return S * std_norm_cdf(d1) - K * np.exp(-r * T) * std_norm_cdf(d2)

    if option_type == "put":
        return K * np.exp(-r * T) * std_norm_cdf(-d2) - S * std_norm_cdf(-d1)

    raise ValueError(f"Invalid Option Type `{option_type}`")


def greek_vega(S, K, r, T, sigma):
    d1 = d1_term(S, K, r, T, sigma)
    return S * std_norm_pdf(d1) * np.sqrt(T)


def greek_gamma(S, K, r, T, sigma):
    d1 = d1_term(S, K, r, T, sigma)
    return std_norm_pdf(d1) / (S * sigma * np.sqrt(T))
