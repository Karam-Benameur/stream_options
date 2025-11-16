import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

from core.pricing import price_european_option_mc
from core.data_io import download_history_yahoo, compute_spot_and_vol_from_history



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

# --- Monte Carlo pricing : déclenché par au moins un des deux boutons ---

if show_price_by_time or run_simulation:
    option_type = "call" if call_or_put.lower() == "call" else "put"

    # 1) Télécharger l'historique de prix depuis Yahoo Finance
    try:
        df_hist = download_history_yahoo(
            ticker=ticker,
            start=start_date,
            end=end_date,
        )
    except Exception as e:
        st.error(f"Erreur lors du téléchargement des données : {e}")
        st.stop()

    # 2) Calculer S0 et la volatilité historique annuelle
    try:
        S0, sigma_est = compute_spot_and_vol_from_history(df_hist)
    except Exception as e:
        st.error(f"Erreur lors du calcul de S0/volatilité : {e}")
        st.stop()

    st.info(
        f"Prix spot S₀ (dernier Adj Close) : {S0:.2f}  •  "
        f"Volatilité historique annuelle estimée : {sigma_est:.2%}"
    )

    # Pour l'instant, on utilise la volatilité historique dans la simulation
    sigma_used = sigma_est

    # 3) Lancer la simulation Monte Carlo
    price, stderr, paths, discounted = price_european_option_mc(
        S0=S0,
        K=strike,
        T=maturity,
        r=discount_rate,
        sigma=sigma_used,
        n_steps=252,
        n_sims=int(n_sims),
        option_type=option_type,
    )

    # ---- Résumé du prix ----
    st.subheader("Estimated option price")

    ci_low = price - 1.96 * stderr
    ci_high = price + 1.96 * stderr

    st.write(
        f"Estimated **{call_or_put}** price: **{price:.2f}** "
        f"(95% CI ≈ [{ci_low:.2f} ; {ci_high:.2f}])"
    )

    # ---- Objets utiles pour les graphes ----
    S_T = paths[-1, :]
    n_show = min(30, paths.shape[1])
    df_paths = pd.DataFrame(paths[:, :n_show])
    df_paths.index.name = "Step"

    # ---- Onglets de visualisation ----
    tab_paths, tab_dist, tab_conv, tab_hist = st.tabs(
        ["Sample paths", "Distribution at maturity", "Convergence", "Historical prices"]
    )

    # 1) Trajectoires simulées
    with tab_paths:
        st.write(f"Affichage de {n_show} trajectoires simulées (sur {paths.shape[1]}).")
        st.line_chart(df_paths)

    # 2) Distribution du prix à l'échéance (courbe lissée)
    with tab_dist:
        counts, bin_edges = np.histogram(S_T, bins=60, density=True)
        centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

        fig, ax = plt.subplots()
        ax.plot(centers, counts)
        ax.set_title("Distribution du prix du sous-jacent à l'échéance")
        ax.set_xlabel("S_T")
        ax.set_ylabel("Densité empirique")
        st.pyplot(fig)

    # 3) Convergence de l'estimation du prix
    with tab_conv:
        n_sims_int = int(n_sims)
        grid = np.linspace(100, n_sims_int, num=min(50, n_sims_int - 99), dtype=int)
        estimates = [discounted[:m].mean() for m in grid]

        df_conv = pd.DataFrame(
            {"n_sims": grid, "Price estimate": estimates}
        ).set_index("n_sims")

        st.write("Convergence de l'estimation du prix en fonction du nombre de trajectoires :")
        st.line_chart(df_conv)

    # 4) Prix historiques du sous-jacent (graphe type image 1)
    with tab_hist:
        st.write("Prix historique (Adj Close) sur la période sélectionnée :")
        # 'Adj Close' si dispo, sinon 'Close'
        col_name = "Adj Close" if "Adj Close" in df_hist.columns else "Close"
        st.line_chart(df_hist[col_name])
