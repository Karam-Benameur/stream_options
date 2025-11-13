# core/pricing.py

import numpy as np


def simulate_gbm_paths(
    S0: float,
    r: float,
    sigma: float,
    T: float,
    n_steps: int,
    n_sims: int,
    seed: int | None = None,
):
    """
    Simule des trajectoires de prix sous-jacent via un
    Mouvement Brownien Géométrique (modèle de Black-Scholes).

    Retourne un array de taille (n_steps + 1, n_sims)
    contenant les trajectoires (ligne 0 = temps 0).
    """
    dt = T / n_steps
    rng = np.random.default_rng(seed)

    # Incréments gaussiens
    Z = rng.standard_normal((n_steps, n_sims))
    increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z

    # On travaille en log pour la stabilité numérique
    log_paths = np.log(S0) + np.cumsum(increments, axis=0)
    paths = np.exp(log_paths)

    # On ajoute la valeur initiale S0 en première ligne
    paths = np.vstack([np.full((1, n_sims), S0), paths])

    return paths


def price_european_option_mc(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    n_steps: int = 252,
    n_sims: int = 10_000,
    option_type: str = "call",
    seed: int | None = None,
):
    """
    Prix d'une option européenne (Call ou Put) par Monte Carlo
    sous le modèle de Black-Scholes.

    Retourne : (prix, erreur_std, paths)
    - prix : estimation Monte Carlo
    - erreur_std : écart-type de l'estimateur
    - paths : trajectoires simulées (pour les graphiques)
    """
    paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_sims, seed)
    S_T = paths[-1, :]  # prix à l'échéance

    option_type = option_type.lower()
    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0.0)
    elif option_type == "put":
        payoffs = np.maximum(K - S_T, 0.0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    discounted = np.exp(-r * T) * payoffs
    price = discounted.mean()
    stderr = discounted.std(ddof=1) / np.sqrt(n_sims)

    return price, stderr, paths
