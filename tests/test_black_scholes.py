import sys
import os

# Ajoutez le chemin du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pricing import OptionPricer

def test_black_scholes_call():
    pricer = OptionPricer(S0=100, K=100, r=0.05, sigma=0.2, T=1, kind='call')
    result = pricer.black_scholes()
    assert abs(result['price'] - 10.45) < 0.01, "Le prix calculé ne correspond pas au prix attendu pour un call."

def test_black_scholes_put():
    pricer = OptionPricer(S0=100, K=100, r=0.05, sigma=0.2, T=1, kind='put')
    result = pricer.black_scholes()
    assert abs(result['price'] - 5.57) < 0.01, "Le prix calculé ne correspond pas au prix attendu pour un put."
