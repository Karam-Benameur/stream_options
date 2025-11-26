import numpy as np
from core.pricing import OptionPricer

def test_black_scholes_call_price_positive():
    op = OptionPricer(S0=100, K=100, r=0.01, sigma=0.2, T=1, kind="call")
    res = op.black_scholes()
    assert "price" in res
    assert res["price"] > 0

def test_greeks_signs():
    op = OptionPricer(S0=100, K=100, r=0.01, sigma=0.2, T=1, kind="call")
    res = op.black_scholes()
    assert res["vega"] > 0    # vega doit être positif
    assert res["gamma"] > 0   # gamma positif
