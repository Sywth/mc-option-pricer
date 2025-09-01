import streamlit as st
import plotly.express as px
import numpy as np

from plotly.subplots import make_subplots
from options_pricer.analytical import black_sholes, greek_gamma, greek_vega
from plotly import graph_objects as go


def get_fig_call_put_price(XS, YS, ZS_call, ZS_put):
    # Create 1 row × 2 column layout with 3D surface plots
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "surface"}, {"type": "surface"}]],
        subplot_titles=("Call Option Surface", "Put Option Surface"),
        horizontal_spacing=0.05,
        vertical_spacing=0.05,
    )

    trace_args = dict(x=XS, y=YS, opacity=0.8, colorscale="plasma", showscale=False)
    fig.add_trace(
        go.Surface(**trace_args, z=ZS_call, name="Call"),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Surface(**trace_args, z=ZS_put, name="Put"),
        row=1,
        col=2,
    )

    # Update axis labels for both scenes
    plot_formatting = dict(
        xaxis_title="ln(S/K)",
        yaxis_title="Maturity (T)",
        aspectratio=dict(x=1.2, y=1.2, z=0.8),
        xaxis=dict(nticks=5, title_font=dict(size=14), tickfont=dict(size=10)),
        yaxis=dict(nticks=4, title_font=dict(size=14), tickfont=dict(size=10)),
        zaxis=dict(nticks=4, title_font=dict(size=14), tickfont=dict(size=10)),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
    )

    fig.update_layout(
        scene1=dict(**plot_formatting, zaxis_title="Option Price (C)"),
        scene2=dict(**plot_formatting, zaxis_title="Option Price (P)"),
        template="plotly_dark",
    )
    return fig


def get_fig_vega(XS, YS, ZS):
    # Single surface plot of Vega vs Spot Price and Time to Maturity
    fig = go.Figure(
        data=[
            go.Surface(
                x=XS,
                y=YS,
                z=ZS,
                opacity=0.8,
                colorscale="plasma",
                showscale=True,
            )
        ]
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="ln(S/K)",
            yaxis_title="Maturity (T)",
            zaxis_title="Vega",
            aspectratio=dict(x=1.2, y=1.2, z=0.8),
            xaxis=dict(nticks=5, title_font=dict(size=14), tickfont=dict(size=10)),
            yaxis=dict(nticks=4, title_font=dict(size=14), tickfont=dict(size=10)),
            zaxis=dict(nticks=4, title_font=dict(size=14), tickfont=dict(size=10)),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
        ),
        template="plotly_dark",
        margin=dict(l=0, r=0, t=40, b=10),
    )

    return fig


def get_fig_gamma(XS, YS, ZS):
    # Single surface plot of Gamma vs Spot Price and Time to Maturity
    fig = go.Figure(
        data=[
            go.Surface(
                x=XS,
                y=YS,
                z=ZS,
                opacity=0.8,
                colorscale="plasma",
                showscale=True,
            )
        ]
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="ln(S/K)",
            yaxis_title="Maturity (T)",
            zaxis_title="Gamma",
            aspectratio=dict(x=1.2, y=1.2, z=0.8),
            xaxis=dict(nticks=5, title_font=dict(size=14), tickfont=dict(size=10)),
            yaxis=dict(nticks=4, title_font=dict(size=14), tickfont=dict(size=10)),
            zaxis=dict(nticks=4, title_font=dict(size=14), tickfont=dict(size=10)),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
        ),
        template="plotly_dark",
        margin=dict(l=0, r=0, t=40, b=10),
    )

    return fig


def main():
    # Page
    st.sidebar.title("Graphing Arguments")
    epsilon = 1e-3

    # Plot parameters
    resolution = st.sidebar.slider(
        "Resolution", min_value=2, max_value=32, value=16, step=1
    )

    st.sidebar.subheader("Black Scholes Parameters")

    # Black Scholes parameters
    interest_rate = st.sidebar.slider(
        "Interest Rate", min_value=0.0, max_value=0.2, value=0.03, step=0.01
    )

    strike_price = st.sidebar.slider(
        "Strike Price", min_value=5.0, max_value=1000.0, value=100.0, step=5.0
    )

    volatility = st.sidebar.slider(
        "Volatility",
        min_value=epsilon,
        max_value=1.0,
        value=0.3,
        step=0.01,
        format="%.3f",
    )

    st.sidebar.subheader("Graph Range")

    # Graph Range
    spot_price_min = st.sidebar.slider(
        "Min Underlying Price", min_value=5.0, max_value=1000.0, value=20.0, step=5.0
    )

    spot_price_max = st.sidebar.slider(
        "Max Underlying Price", min_value=5.0, max_value=1000.0, value=200.0, step=5.0
    )

    time_min = st.sidebar.slider(
        "Min Time to Maturity (Years)",
        min_value=epsilon,
        max_value=10.0,
        value=0.2,
        step=0.01,
        format="%.3f",
    )

    time_max = st.sidebar.slider(
        "Max Time to Maturity (Years)",
        min_value=epsilon,
        max_value=10.0,
        value=5.0,
        step=0.01,
        format="%.3f",
    )

    if spot_price_min > spot_price_max:
        st.error(
            "Invalid Underlying Price range. The minimum price on the slider must be less than the maximum price."
        )
        return

    if time_min > time_max:
        st.error(
            "Invalid Time to Maturity range. The minimum time on the slider must be less than the maximum time."
        )
        return

    # i.e. moneyness scaled by strike price
    spot_prices = np.linspace(spot_price_min, spot_price_max, resolution)
    time_to_maturity_years = np.linspace(time_min, time_max, resolution)

    # Meshgrid for spot price and time
    XS, YS = np.meshgrid(spot_prices, time_to_maturity_years)

    # Compute both surfaces
    ZS_call = black_sholes(
        interest_rate=interest_rate,
        strike_price=strike_price,
        underlying_price=XS,
        time_to_maturity_years=YS,
        volatility=volatility,
        option_type="call",
    )

    ZS_put = black_sholes(
        interest_rate=interest_rate,
        strike_price=strike_price,
        underlying_price=XS,
        time_to_maturity_years=YS,
        volatility=volatility,
        option_type="put",
    )

    ZS_vega = greek_vega(XS, strike_price, interest_rate, YS, volatility)
    ZS_gamma = greek_gamma(XS, strike_price, interest_rate, YS, volatility)

    XS_log_moneyness = np.log(XS / strike_price)
    fig_opt = get_fig_call_put_price(
        XS=XS_log_moneyness,
        YS=YS,
        ZS_call=ZS_call,
        ZS_put=ZS_put,
    )
    fig_vega = get_fig_vega(
        XS=XS_log_moneyness,
        YS=YS,
        ZS=ZS_vega,
    )
    fig_gamma = get_fig_gamma(
        XS=XS_log_moneyness,
        YS=YS,
        ZS=ZS_gamma,
    )

    st.title("Options Pricing & Greeks")
    st.write(
        """
        You can press the fullscreen button (top right) on each plot to view it more clearly. 
        Adjust the parameters on the sidebar to see how they affect the option price surfaces.
        """
    )
    st.subheader("Option Price vs Time To Maturity and Log Moneyness Surface")
    st.plotly_chart(fig_opt, use_container_width=True)
    st.caption(
        "European option surface generated via the analytical Black Scholes formulae."
    )

    st.write(
        """
        Log Moneyness refers to the quantity $m \coloneqq \ln(S/K)$. 
        When $m \gt 0$ we are in the money for calls (expecting a payoff) 
        and when $m \lt 0$ we are out the money for calls (payoff of 0). 
        The opposite is true for put options.

        Plotting option price against log moneyness $m=\ln(S/K)$ and maturity $T$
        reproduces the option price against $S$ & $T$ surface while normalizing 
        with respect to the strike price, $K$, 
        allowing for a relative comparison.
        """
    )

    # Gamma
    st.subheader(
        "[Gamma](https://en.wikipedia.org/wiki/Greeks_(finance)#Gamma) vs Time To Maturity and Log Moneyness Surface"
    )
    st.plotly_chart(fig_gamma, use_container_width=True)
    st.caption(
        "Surface plot of the rate of change of $\Delta$ (i.e. $\Gamma$) "
        + "with respect to the underlying price against time to maturity "
        + "and log moneyness."
    )

    st.write(
        "This is the rate of change of $\Delta$. "
        "That is where $Z$ is $C$ or $P$ (the option price) we have :"
    )
    st.latex(
        r"\Gamma \coloneqq \dfrac{\partial \Delta}{\partial S} "
        + r"= \dfrac{\partial^2 Z}{\partial S^2} "
        + r"= \dfrac{\phi(d_1)}{S \sigma \sqrt{T}}"
    )
    st.write(
        "Where $\phi$ is the [normal pdf](https://en.wikipedia.org/wiki/Normal_distribution). It intuitively measures the convexity of the "
        + "option's price with respect to change in the underlying price."
    )

    # Vega
    st.subheader(
        "[Vega](https://en.wikipedia.org/wiki/Greeks_(finance)#Vega) vs Time To Maturity and Log Moneyness Surface"
    )
    st.plotly_chart(fig_vega, use_container_width=True)
    st.caption(
        "Surface plot of sensitivity to change in volatility (i.e. Vega ($\\nu$)) "
        + "against time to maturity, $T$, and log moneyness, $m$."
    )

    st.write(
        "This is the sensitivity to change in volatility. "
        + "That is where $Z$ is $C$ or $P$ (the option price) we have :"
    )
    st.latex(
        r"\nu \coloneqq \dfrac{\partial Z}{\partial \sigma} "
        + r"= S \phi(d_1) \sqrt{T}"
    )
    st.write(
        "Where $\phi$ is the [normal pdf](https://en.wikipedia.org/wiki/Normal_distribution)."
    )

    # sidebar footer
    st.sidebar.link_button("🔗 LinkedIn", "https://www.linkedin.com/in/sp-ucl")


# TODO :
#   - Make this multipage; extra page using yahoo finance to make P&L plots for any ticker and make this the first page
#       - https://www.youtube.com/watch?v=9n4Ch2Dgex0
#   - Add a graph with the greek Delta on the main page
#   - Use monte carlo for asian options
#       - https://www.youtube.com/watch?v=A663NOHPRHE

if __name__ == "__main__":
    main()
