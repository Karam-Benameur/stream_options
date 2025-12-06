# test_yfinance.py
import yfinance as yf
import pandas as pd
from datetime import datetime

print("Test de yfinance en action...")
print("-" * 40)

# Test 1: Téléchargement simple
try:
    data = yf.download("AAPL", period="1d", progress=False)
    print(f"✓ Test 1: Download AAPL - {data.shape[0]} lignes, {data.shape[1]} colonnes")
except Exception as e:
    print(f"✗ Test 1 échoué: {e}")

# Test 2: Récupération d'infos
try:
    ticker = yf.Ticker("AAPL")
    info = ticker.info
    print(f"✓ Test 2: Info AAPL - {info.get('longName', 'N/A')}")
except Exception as e:
    print(f"✗ Test 2 échoué: {e}")

# Test 3: Historique
try:
    hist = ticker.history(period="1mo")
    print(f"✓ Test 3: Historique 1 mois - {len(hist)} jours")
except Exception as e:
    print(f"✗ Test 3 échoué: {e}")

print("-" * 40)
print("✅ yfinance est fonctionnel !")
