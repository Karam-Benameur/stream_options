import os
import sys
import pytest
from pathlib import Path

# Ajoute la racine du projet au PYTHONPATH (tests/.. = racine)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.pricing import OptionPricer

# Add root directory to path so we can import 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_black_scholes_logic():
    """Checks if Black-Scholes returns a float > 0 for valid inputs."""
    price = OptionPricer.black_scholes_price(100, 100, 1, 0.05, 0.2, "call")
    assert isinstance(price, float)
    assert price > 0

def test_bopm_convergence():
    """Checks if Binomial converges to BS within a tolerance."""
    bs_price = OptionPricer.black_scholes_price(100, 100, 1, 0.05, 0.2, "call")
    # Using 50 steps for better precision
    bopm_res = OptionPricer.calculate_bopm(100, 100, 1, 0.05, 0.2, 50, "call")
    bopm_price = bopm_res[3] # Price is the 4th element
    
    # Assert they are close (within 0.5 currency unit)
    assert abs(bopm_price - bs_price) < 0.5
