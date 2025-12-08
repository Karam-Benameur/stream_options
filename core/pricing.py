import numpy as np
from dataclasses import dataclass
from math import log, sqrt, exp, erf, pi
from typing import Literal, Dict, Tuple


# =====================================================================
# 1) Monte Carlo : simulation de trajectoires + pricing
# =====================================================================

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
    Simule des trajectoires de prix sous-jacent via un Mouvement Brownien
    Géométrique (modèle de Black-Scholes).

    Parameters
    ----------
    S0 : float
        Prix initial du sous-jacent (doit être > 0).
    r : float
        Taux sans risque (annuel).
    sigma : float
        Volatilité (annuelle, doit être >= 0).
    T : float
        Maturité en années (doit être > 0).
    n_steps : int
        Nombre de pas de temps (doit être > 0).
    n_sims : int
        Nombre de trajectoires simulées (doit être > 0).
    seed : int, optional
        Graine du générateur aléatoire (pour la reproductibilité).

    Returns
    -------
    np.ndarray
        Tableau de taille (n_steps + 1, n_sims) contenant les trajectoires.

    Raises
    ------
    ValueError
        Si S0 <= 0, sigma < 0, T <= 0 ou si n_steps / n_sims ne sont pas positifs.
    """
    if S0 <= 0:
        raise ValueError("S0 must be strictly positive.")
    if sigma < 0:
        raise ValueError("sigma must be non-negative.")
    if T <= 0:
        raise ValueError("T must be strictly positive.")
    if n_steps <= 0 or n_sims <= 0:
        raise ValueError("n_steps and n_sims must be positive integers.")

    dt = T / n_steps
    rng = np.random.default_rng(seed)

    Z = rng.standard_normal((n_steps, n_sims))
    increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z

    log_paths = np.log(S0) + np.cumsum(increments, axis=0)
    paths = np.exp(log_paths)

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

    Retourne : (prix, erreur_std, paths, discounted)
    - prix : estimation Monte Carlo
    - erreur_std : écart-type de l'estimateur
    - paths : trajectoires simulées
    - discounted : payoffs actualisés (pour histogramme / convergence)

    Raises
    ------
    ValueError
        Si ``option_type`` n'est pas 'call' ou 'put', ou si les paramètres
        passés à ``simulate_gbm_paths`` sont invalides.
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

    return price, stderr, paths, discounted


# =====================================================================
# 2) Black-Scholes fermé + classe OptionPricer
# =====================================================================

def _norm_pdf(x: float) -> float:
    """Densité de la loi normale standard φ(x)."""
    return (1.0 / sqrt(2.0 * pi)) * exp(-0.5 * x * x)


def _norm_cdf(x: float) -> float:
    """Fonction de répartition de la loi normale standard Φ(x)."""
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


@dataclass
class OptionPricer:
    """
    Petit pricer Black-Scholes pour une option européenne.
    """

    S0: float
    K: float
    r: float
    sigma: float
    T: float
    kind: Literal["call", "put"] = "call"

    def __post_init__(self) -> None:
        """Validation basique des paramètres (avec ValueError)."""
        self.kind = self.kind.lower()
        if self.kind not in {"call", "put"}:
            raise ValueError("kind must be 'call' or 'put'")
        if self.S0 <= 0:
            raise ValueError("S0 must be > 0")
        if self.K <= 0:
            raise ValueError("K must be > 0")
        if self.T <= 0:
            raise ValueError("T (maturity) must be > 0")
        if self.sigma < 0:
            raise ValueError("sigma must be >= 0")

    def _d1_d2(self) -> Tuple[float, float]:
        """Calcule d1 et d2 de Black-Scholes."""
        vol_sqrt_T = self.sigma * sqrt(self.T)
        if vol_sqrt_T == 0:
            raise ValueError("sigma * sqrt(T) must be > 0 for Black-Scholes.")

        d1 = (log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / vol_sqrt_T
        d2 = d1 - vol_sqrt_T
        return d1, d2

    def black_scholes(self) -> Dict[str, float]:
        """
        Calcule le prix Black-Scholes et les Greeks.

        Returns
        -------
        dict
            Dictionnaire avec les clés :
            "price", "delta", "gamma", "vega", "theta", "rho".
        """
        d1, d2 = self._d1_d2()
        Nd1 = _norm_cdf(d1)
        Nd2 = _norm_cdf(d2)
        pdf_d1 = _norm_pdf(d1)
        df = exp(-self.r * self.T)

        if self.kind == "call":
            price = self.S0 * Nd1 - self.K * df * Nd2
            delta = Nd1
            theta = (
                - (self.S0 * pdf_d1 * self.sigma) / (2.0 * sqrt(self.T))
                - self.r * self.K * df * Nd2
            )
            rho = self.K * self.T * df * Nd2
        else:
            price = self.K * df * (1.0 - Nd2) - self.S0 * (1.0 - Nd1)
            delta = Nd1 - 1.0
            theta = (
                - (self.S0 * pdf_d1 * self.sigma) / (2.0 * sqrt(self.T))
                + self.r * self.K * df * (1.0 - Nd2)
            )
            rho = -self.K * self.T * df * (1.0 - Nd2)

        gamma = pdf_d1 / (self.S0 * self.sigma * sqrt(self.T))
        vega = self.S0 * pdf_d1 * sqrt(self.T)

        return {
            "price": price,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
        }

    @classmethod
    def black_scholes_price(
        cls,
        S0: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        kind: str = "call",
    ) -> float:
        """
        Méthode de classe utilitaire pour obtenir *uniquement* le prix
        Black-Scholes, comme attendu dans les tests unitaires.
        """
        pricer = cls(S0=S0, K=K, r=r, sigma=sigma, T=T, kind=kind)
        res = pricer.black_scholes()
        return res["price"]
