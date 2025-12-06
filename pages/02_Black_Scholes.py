
import sys
=======
>>>>>>> 36cb82cf091508dbb19d3bda466320887201beb9
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

# Configuration de la page
st.set_page_config(page_title="Black-Scholes Method", layout="wide")

# Titre de la page
st.title("Pricing Options using Black-Scholes Method")

# Description de la page
st.markdown("""
This page allows you to calculate the price and Greeks of a European option (Call or Put) using the Black-Scholes method.
""")

# Paramètres directement sur la page principale
col1, col2 = st.columns(2)

with col1:
    ticker = st.text_input("Select a ticker", "AAPL")
    start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End date", pd.to_datetime("2023-12-31"))
    kind = st.selectbox("Call or Put", ["call", "put"])
    K = st.number_input("Strike Price", value=100.0)
    r = st.number_input("Risk-free rate (r)", value=0.02)
    sigma = st.number_input("Volatility (σ, annual)", value=0.2)
    T = st.number_input("Maturity (T, in years)", value=1.0)
    run = st.button("Calculate")

with col2:
    if st.button("Price by time"):
        data = yf.Ticker(ticker).history(start=start_date, end=end_date)
        if not data.empty:
            fig, ax = plt.subplots(figsize=(6, 3))  # Réduction de la taille du graphique
            ax.plot(data.index, data['Close'])
            ax.set_title(f"{ticker} Price by Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            st.pyplot(fig)
        else:
            st.error("Unable to fetch data from Yahoo Finance.")

if run:
    try:
        data = yf.Ticker(ticker).history(period="1d")
        if not data.empty:
            S0 = float(data["Close"].iloc[-1])
        else:
            S0 = 100.0
    except:
        S0 = 100.0

    pricer = OptionPricer(S0=S0, K=K, r=r, sigma=sigma, T=T, kind=kind)
    res = pricer.black_scholes()

    st.subheader("Results")
    st.write(f"Estimated {kind} price: **{res['price']:.2f}**")

    # Affichage des Greeks
    st.write("### Greeks")
    greeks_data = {
        "Delta": [res["delta"]],
        "Gamma": [res["gamma"]],
        "Vega": [res["vega"]],
        "Theta": [res["theta"]],
        "Rho": [res["rho"]]
    }
    st.table(greeks_data)

    # Graphique du Payoff avec taille réduite
    st.subheader("Payoff at Maturity")
    S_values = np.linspace(50, 150, 100)
    if kind == "call":
        payoffs = [max(S - K, 0) for S in S_values]
    else:
        payoffs = [max(K - S, 0) for S in S_values]

    fig, ax = plt.subplots(figsize=(6, 3))  # Réduction de la taille du graphique
    ax.plot(S_values, payoffs, label='Payoff')
    ax.axvline(x=K, color='red', linestyle='--', label='Strike Price')
    ax.set_xlabel('Underlying Price')
    ax.set_ylabel('Payoff')
    ax.set_title(f'Payoff of the {kind} option')
    ax.legend()
    st.pyplot(fig)

    # Graphique des Greeks avec taille réduite
    st.subheader("Greeks Evolution")
    S_grid = np.linspace(50, 150, 100)
    deltas, gammas, vegas, thetas, rhos = [], [], [], [], []
    for S in S_grid:
        p = OptionPricer(S0=S, K=K, r=r, sigma=sigma, T=T, kind=kind).black_scholes()
        deltas.append(p["delta"])
        gammas.append(p["gamma"])
        vegas.append(p["vega"])
        thetas.append(p["theta"])
        rhos.append(p["rho"])

    fig2, ax2 = plt.subplots(figsize=(6, 3))  # Réduction de la taille du graphique
    ax2.plot(S_grid, deltas, label="Delta")
    ax2.plot(S_grid, gammas, label="Gamma")
    ax2.plot(S_grid, vegas, label="Vega")
    ax2.plot(S_grid, thetas, label="Theta")
    ax2.plot(S_grid, rhos, label="Rho")
    ax2.set_xlabel('Underlying Price')
    ax2.set_ylabel('Greek Value')
    ax2.set_title("Evolution of Greeks")
    ax2.legend()
    st.pyplot(fig2)
