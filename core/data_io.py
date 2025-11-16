from __future__ import annotations

from pathlib import Path
from datetime import date

import numpy as np
import pandas as pd
import yfinance as yf


# Dossier où on va stocker les CSV
DATA_DIR = Path(__file__).resolve().parents[1] / "Bases de données"
DATA_DIR.mkdir(exist_ok=True)


def download_history_yahoo(
    ticker: str,
    start: date,
    end: date,
    save_csv: bool = True,
) -> pd.DataFrame:
    """
    Télécharge les données quotidiennes depuis Yahoo Finance
    pour le ticker entre start et end.

    Renvoie un DataFrame indexé par la date avec au moins 'Adj Close'.
    Sauvegarde un CSV dans 'Bases de données' si save_csv=True.
    """
    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        raise ValueError(f"Aucune donnée reçue pour {ticker} entre {start} et {end}.")

    # On s'assure que l'index est bien une colonne Date
    df = df.rename_axis("Date")

    if save_csv:
        csv_name = f"{ticker}_{start}_{end}.csv"
        csv_path = DATA_DIR / csv_name
        df.to_csv(csv_path)

    return df


def compute_spot_and_vol_from_history(df: pd.DataFrame) -> tuple[float, float]:
    """
    Calcule le prix spot S0 et la volatilité annuelle historique à partir
    d'un DataFrame de prix (colonnes Yahoo Finance).

    Retourne (S0, sigma_annuelle).
    """
    # On privilégie 'Adj Close', sinon 'Close'
    if "Adj Close" in df.columns:
        close = df["Adj Close"].dropna()
    else:
        close = df["Close"].dropna()

    if len(close) < 2:
        raise ValueError("Pas assez de données pour calculer la volatilité.")

    # Spot = dernier prix
    S0 = float(close.iloc[-1])

    # Rendements log
    log_returns = np.log(close / close.shift(1)).dropna()

    # Volatilité annuelle (252 jours de bourse)
    sigma_daily = log_returns.std(ddof=1)
    sigma_ann = float(sigma_daily * np.sqrt(252))

    return S0, sigma_ann
