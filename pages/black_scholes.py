import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Permet d'accéder à core/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.pricing import OptionPricer

st.title("Black-Scholes — Prix et Greeks")

# --- Barre latérale ---
with st.sidebar:
    kind = st.selectbox("Type d’option", ["call", "put"])
    S0 = st.number_input("Prix spot S0", value=100.0)
    K  = st.number_input("Strike K", value=100.0)
    r  = st.number_input("Taux sans risque r", value=0.02)
    sigma = st.number_input("Volatilité σ (annuelle)", value=0.2)
    T = st.number_input("Maturité (années)", value=1.0)
    run = st.button("Calculer")

# --- Calcul ---
if run:
    pricer = OptionPricer(S0=S0, K=K, r=r, sigma=sigma, T=T, kind=kind)
    res = pricer.black_scholes()

    # --- Résultats ---
    st.subheader("Résultats Black-Scholes")

    st.metric("Prix théorique", f"{res['price']:.6f}")

    st.write("### Greeks")
    st.table({
        "Delta": [res["delta"]],
        "Gamma": [res["gamma"]],
        "Vega":  [res["vega"]],
        "Theta": [res["theta"]],
        "Rho":   [res["rho"]],
    })

    # --- Export CSV ---
    df_result = pd.DataFrame([res])

    st.download_button(
        label="📥 Télécharger les résultats en CSV",
        data=df_result.to_csv(index=False).encode("utf-8"),
        file_name="black_scholes_results.csv",
        mime="text/csv"
    )

    # --- Graphique du Payoff ---
    st.subheader("Graphique du Payoff à maturité")

    S_values = np.linspace(0.5 * S0, 1.5 * S0, 200)

    if kind == "call":
        payoff = np.maximum(S_values - K, 0)
    else:
        payoff = np.maximum(K - S_values, 0)

    fig, ax = plt.subplots()
    ax.plot(S_values, payoff)
    ax.set_xlabel("Prix de l’action S")
    ax.set_ylabel("Payoff à maturité")
    ax.set_title(f"Payoff de l’option ({kind})")

    st.pyplot(fig)
