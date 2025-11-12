import streamlit as st

def hero_home():
    st.write(
        """
        Welcome to **Stream Options** — compare European option pricing with
        **Monte Carlo**, **Black–Scholes**, and **Binomial** in one place.
        Use the sidebar to pick a method, set inputs, click **Price by time**,
        then **Simulation** to see results (price, Greeks, paths, convergence).
        """
    )
