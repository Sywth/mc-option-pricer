import streamlit as st
import plotly.express as px
from options_pricer.monte_carlo import generate_3d_data


def main():
    st.title("Monte Carlo Options Pricer (3D Demo)")
    st.write("This is a placeholder 3D visualization using Plotly.")

    data = generate_3d_data(100)
    fig = px.line_3d(data, x="x", y="y", z="z")

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
