import os
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

# Permet d’accéder au dossier "core/"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.pricing import OptionPricer


# ---------------------------------------------------------
#   TITRE
# ---------------------------------------------------------
st.title("📈 Modèle de Black-Scholes — Prix, Greeks & Yahoo Finance")


# ---------------------------------------------------------
#   RÉCUPÉRATION DU PRIX VIA YAHOO FINANCE
# ---------------------------------------------------------
st.subheader("📥 Charger le prix automatiquement via Yahoo Finance")

ticker = st.text_input("Ticker Yahoo Finance (ex : AAPL, TSLA, MSFT)", "AAPL")

if st.button("Charger le prix Yahoo Finance"):
    data = yf.Ticker(ticker).history(period="1d")
    if not data.empty:
        last_price = float(data["Close"].iloc[-1])
        st.success(f"Prix récupéré depuis Yahoo Finance : **{last_price} USD**")
        S0_from_yahoo = last_price
    else:
        st.error("❌ Impossible de récupérer les données Yahoo Finance.")
        S0_from_yahoo = None
else:
    S0_from_yahoo = None


# ---------------------------------------------------------
#   BARRE LATÉRALE : PARAMÈTRES
# ---------------------------------------------------------
with st.sidebar:
    st.header("Paramètres Black-Scholes")

    kind = st.selectbox("Type d’option", ["call", "put"])

    # Si un prix a été récupéré, on le met automatiquement
    if S0_from_yahoo:
        S0 = st.number_input("Prix spot S0", value=S0_from_yahoo)
    else:
        S0 = st.number_input("Prix spot S0", value=100.0)

    K  = st.number_input("Strike K", value=100.0)
    r  = st.number_input("Taux sans risque r", value=0.02)
    sigma = st.number_input("Volatilité σ", value=0.2)
    T = st.number_input("Maturité (années)", value=1.0)

    run = st.button("Calculer")


# ---------------------------------------------------------
#   CALCUL BLACK-SCHOLES
# ---------------------------------------------------------
if run:

    pricer = OptionPricer(S0=S0, K=K, r=r, sigma=sigma, T=T, kind=kind)
    res = pricer.black_scholes()

    # Résultats
    st.subheader("📊 Résultats Black-Scholes")
    st.metric("Prix théorique", f"{res['price']:.6f}")

    st.write("### Greeks")
    st.table({
        "Delta": [res["delta"]],
        "Gamma": [res["gamma"]],
        "Vega":  [res["vega"]],
        "Theta": [res["theta"]],
        "Rho":   [res["rho"]],
    })

    # Export CSV
    df_result = pd.DataFrame([res])

    st.download_button(
        label="📥 Télécharger les résultats (CSV)",
        data=df_result.to_csv(index=False).encode("utf-8"),
        file_name="black_scholes_results.csv",
        mime="text/csv"
    )

    # -----------------------------------------------------
    #   GRAPHIQUE DU PAYOFF
    # -----------------------------------------------------
    st.subheader("📉 Payoff à maturité")

    S_values = np.linspace(0.5 * S0, 1.5 * S0, 200)

    if kind == "call":
        payoff = np.maximum(S_values - K, 0)
    else:
        payoff = np.maximum(K - S_values, 0)

    fig, ax = plt.subplots()
    ax.plot(S_values, payoff)
    ax.set_xlabel("Prix de l’actif S")
    ax.set_ylabel("Payoff à maturité")
    ax.set_title(f"Payoff de l’option ({kind})")

    st.pyplot(fig)

    # --- Graphique des Greeks ---
st.subheader("Évolution des Greeks selon S")

# Génération d'une grille de prix
S_grid = np.linspace(0.5 * S0, 1.5 * S0, 100)

# Calcul des greeks sur la grille
deltas = []
gammas = []
vegas = []
thetas = []
rhos = []

for S in S_grid:
    p = OptionPricer(S0=S, K=K, r=r, sigma=sigma, T=T, kind=kind).black_scholes()
    deltas.append(p["delta"])
    gammas.append(p["gamma"])
    vegas.append(p["vega"])
    thetas.append(p["theta"])
    rhos.append(p["rho"])

# --- Affichage ---
fig2, ax2 = plt.subplots()
ax2.plot(S_grid, deltas, label="Delta")
ax2.plot(S_grid, gammas, label="Gamma")
ax2.plot(S_grid, vegas, label="Vega")
ax2.plot(S_grid, thetas, label="Theta")
ax2.plot(S_grid, rhos, label="Rho")

ax2.set_xlabel("Prix de l’actif S")
ax2.set_ylabel("Valeur du Greek")
ax2.set_title("Évolution des Greeks en fonction du prix S")
ax2.legend()

st.pyplot(fig2)




