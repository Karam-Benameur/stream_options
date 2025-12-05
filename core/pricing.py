import numpy as np
from dataclasses import dataclass
from typing import Literal, Dict, Tuple


# ============================================================================
#  Outils pour la loi normale
# ============================================================================

def _norm_cdf(x: float) -> float:
    """Fonction de répartition de N(0,1)."""
    return 0.5 * (1.0 + np.erf(x / np.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    """Densité de N(0,1)."""
    return (1.0 / np.sqrt(2.0 * np.pi)) * np.exp(-0.5 * x**2)


# ============================================================================
#  Classe OptionPricer : Black-Scholes + Greeks
# ============================================================================

@dataclass
class OptionPricer:
    """
    Pricer Black-Scholes pour une option européenne.

    Parameters
    ----------
    S0 : float
        Prix spot initial (> 0).
    K : float
        Strike (> 0).
    r : float
        Taux sans risque (annuel).
    sigma : float
        Volatilité annuelle (>= 0).
    T : float
        Maturité (en années, > 0).
    kind : {"call", "put"}
        Type d'option.
    """

    S0: float
    K: float
    r: float
    sigma: float
    T: float
    kind: Literal["call", "put"] = "call"

    def __post_init__(self) -> None:
        """Vérifie la validité des paramètres."""
        if self.S0 <= 0:
            raise ValueError("S0 must be > 0")
        if self.K <= 0:
            raise ValueError("K must be > 0")
        if self.T <= 0:
            raise ValueError("T (maturity) must be > 0")
        if self.sigma < 0:
            raise ValueError("sigma must be >= 0")

        k = self.kind.lower()
        if k not in {"call", "put"}:
            raise ValueError("kind must be 'call' or 'put'")
        self.kind = k

    # --------------------- d1, d2 --------------------- #

    def _d1_d2(self) -> Tuple[float, float]:
        """Calcule d1 et d2 de Black-Scholes."""
        if self.sigma == 0 or self.T == 0:
            raise ValueError("sigma and T must be > 0 to compute d1 and d2")

        d1 = (
            np.log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma**2) * self.T
        ) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return float(d1), float(d2)

    # --------------------- Black-Scholes --------------------- #

    def black_scholes(self) -> Dict[str, float]:
        """
        Calcule le prix Black-Scholes et les Greeks.

        Returns
        -------
        dict
            Dictionnaire avec les clés :
            "price", "delta", "gamma", "vega", "theta", "rho".

        Raises
        ------
        ValueError
            Si les paramètres sont invalides.
        """
        d1, d2 = self._d1_d2()
        phi_d1 = _norm_pdf(d1)
        N_d1 = _norm_cdf(d1)
        N_d2 = _norm_cdf(d2)
        disc = np.exp(-self.r * self.T)

        if self.kind == "call":
            price = self.S0 * N_d1 - self.K * disc * N_d2
            delta = N_d1
            rho = self.K * self.T * disc * N_d2
            theta = (
                -(self.S0 * phi_d1 * self.sigma) / (2 * np.sqrt(self.T))
                - self.r * self.K * disc * N_d2
            )
        else:  # put
            N_minus_d1 = _norm_cdf(-d1)
            N_minus_d2 = _norm_cdf(-d2)
            price = self.K * disc * N_minus_d2 - self.S0 * N_minus_d1
            delta = N_d1 - 1.0
            rho = -self.K * self.T * disc * N_minus_d2
            theta = (
                -(self.S0 * phi_d1 * self.sigma) / (2 * np.sqrt(self.T))
                + self.r * self.K * disc * N_minus_d2
            )

        gamma = phi_d1 / (self.S0 * self.sigma * np.sqrt(self.T))
        vega = self.S0 * phi_d1 * np.sqrt(self.T)

        return {
            "price": float(price),
            "delta": float(delta),
            "gamma": float(gamma),
            "vega": float(vega),
            "theta": float(theta),
            "rho": float(rho),
        }


# ============================================================================
#  Monte Carlo (utilisé par ta page 01_Monte_Carlo.py)
# ============================================================================

def simulate_gbm_paths(
    S0: float,
    r: float,
    sigma: float,
    T: float,
    n_steps: int,
    n_sims: int,
    seed: int | None = None,
) -> np.ndarray:
    """
    Simule des trajectoires via un Mouvement Brownien Géométrique.

    Retourne un array (n_steps + 1, n_sims).

    Raises
    ------
    ValueError
        Si un paramètre est invalide.
    """
    if S0 <= 0:
        raise ValueError("S0 must be > 0")
    if T <= 0:
        raise ValueError("T (maturity) must be > 0")
    if sigma < 0:
        raise ValueError("sigma must be >= 0")
    if n_steps <= 0:
        raise ValueError("n_steps must be > 0")
    if n_sims <= 0:
        raise ValueError("n_sims must be > 0")

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
    option_type: Literal["call", "put"] = "call",
    seed: int | None = None,
):
    """
    Prix d'une option européenne (Call ou Put) par Monte Carlo.

    Returns
    -------
    (price, stderr, paths, discounted)

    Raises
    ------
    ValueError
        Si option_type est invalide ou si les paramètres sont invalides.
    """
    option_type = option_type.lower()
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")

    paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_sims, seed)
    S_T = paths[-1, :]

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0.0)
    else:
        payoffs = np.maximum(K - S_T, 0.0)

    discounted = np.exp(-r * T) * payoffs
    price = discounted.mean()
    stderr = discounted.std(ddof=1) / np.sqrt(n_sims)

    return price, stderr, paths, discounted
