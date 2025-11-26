import numpy as np
from scipy.stats import norm

class OptionPricer:
    """
    Classe pour calculer le prix et les Greeks d'une option européenne.
    """

    def __init__(self, S0, K, r, sigma, T, kind):
        """
        Constructeur de la classe OptionPricer.

        Paramètres :
        - S0 : Prix actuel du sous-jacent.
        - K : Prix d'exercice (strike).
        - r : Taux sans risque.
        - sigma : Volatilité du sous-jacent.
        - T : Temps jusqu'à l'échéance (en années).
        - kind : Type d'option ('call' ou 'put').
        """
        self.S0 = S0
        self.K = K
        self.r = r
        self.sigma = sigma
        self.T = T
        self.kind = kind

    def black_scholes(self):
        """
        Calcule le prix et les Greeks d'une option européenne selon le modèle Black-Scholes.

        Retourne :
        - Un dictionnaire avec le prix et les Greeks (delta, gamma, vega, theta, rho).
        """
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)

        if self.kind == 'call':
            price = self.S0 * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
            delta = norm.cdf(d1)
        else:  # put
            price = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S0 * norm.cdf(-d1)
            delta = norm.cdf(d1) - 1

        # Calcul des Greeks
        gamma = norm.pdf(d1) / (self.S0 * self.sigma * np.sqrt(self.T))
        vega = self.S0 * norm.pdf(d1) * np.sqrt(self.T) * 0.01  # pour 1% de volatilité
        theta_call = (-self.S0 * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T)) -
                      self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)) / 365
        theta_put = (-self.S0 * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T)) +
                     self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)) / 365
        theta = theta_call if self.kind == 'call' else theta_put
        rho = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2 if self.kind == 'put' else d2) * 0.01  # pour 1% de taux

        return {
            'price': price,
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho
        }
