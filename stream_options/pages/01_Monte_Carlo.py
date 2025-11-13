import streamlit as st
import pandas as pd
from datetime import date

from core.pricing import price_european_option_mc


st.set_page_config(
    page_title="Monte Carlo Method",
    page_icon="🎲",
)

st.title("Pricing Options using Monte Carlo Method")
st.write(
    "Cette page permet de simuler des trajectoires du sous-jacent "
    "et de pricer une option européenne (Call ou Put) par Monte Carlo."
)

col1, col2 = st.columns(2)

with col1:
    ticker = st.selectbox(
        "Select Ticker",
        ["AAPL", "MSFT", "TSLA", "BNP.PA", "AIR.PA"],
        index=0,
    )

    start_date = st.date_input(
        "Start date",
        value=date(2020, 1, 1),
    )

    call_or_put = st.selectbox(
        "Call or Put",
        ["Call", "Put"],
        index=0,
    )

    strike = st.number_input(
        "Strike Price",
        min_value=0.0,
        value=100.0,
        step=1.0,
    )

    discount_rate = st.number_input(
        "Discount Rate (r, en annuel)",
        min_value=0.0,
        value=0.02,
        step=0.005,
        format="%.3f",
    )

with col2:
    end_date = st.date_input(
        "End date",
        value=date(2025, 1, 1),
    )

    n_sims = st.number_input(
        "Number of Simulations",
        min_value=100,
        max_value=100_000,
        value=10_000,
        step=1_000,
    )

    volatility = st.number_input(
        "Volatility (σ, en annuel)",
        min_value=0.01,
        value=0.2,
        step=0.01,
        format="%.2f",
    )

    maturity = st.number_input(
        "Maturity (T, en années)",
        min_value=0.01,
        value=1.0,
        step=0.25,
        format="%.2f",
    )

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    show_price_by_time = st.button("Price by time")
with btn_col2:
    run_simulation = st.button("Simulation")

S0 = 100.0  # provisoire, en attendant le vrai prix via les données

if show_price_by_time or run_simulation:
    option_type = "call" if call_or_put.lower() == "call" else "put"

    price, stderr, paths = price_european_option_mc(
        S0=S0,
        K=strike,
        T=maturity,
        r=discount_rate,
        sigma=volatility,
        n_steps=252,
        n_sims=int(n_sims),
        option_type=option_type,
    )

    if run_simulation:
        st.subheader("Estimated option price")

        ci_low = price - 1.96 * stderr
        ci_high = price + 1.96 * stderr

        st.write(
            f"Estimated **{call_or_put}** price: **{price:.2f}** "
            f"(95% CI ≈ [{ci_low:.2f} ; {ci_high:.2f}])"
        )

        n_show = min(30, paths.shape[1])
        df_paths = pd.DataFrame(paths[:, :n_show])
        df_paths.index.name = "Step"

        st.subheader("Simulated price paths")
        st.line_chart(df_paths)

    if show_price_by_time:
        mean_path = paths.mean(axis=1)
        df_mean = pd.DataFrame({"Mean price": mean_path})

        st.subheader("Average price over time (simulated)")
        st.line_chart(df_mean)
