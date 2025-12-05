Introduction
============

Objectif du projet
------------------

Le projet **StreamOptions** vise à proposer une petite application web
pédagogique pour illustrer le pricing d'options européennes.  
L'utilisateur peut :

- choisir un **ticker** coté (via Yahoo Finance),
- récupérer l'historique des prix,
- estimer la **volatilité** historique,
- pricer l'option avec 3 méthodes complémentaires :

  * Monte Carlo sous Black–Scholes,
  * formule fermée de **Black–Scholes**,
  * **modèle binomial**.


Organisation du code
--------------------

Le code est structuré autour de plusieurs sous-modules :

- ``core.pricing``  

  Contient :

  * :func:`core.pricing.simulate_gbm_paths` – simulation de trajectoires
    de Mouvement Brownien Géométrique.
  * :func:`core.pricing.price_european_option_mc` – pricing Monte Carlo
    d'une option européenne (Call/Put).
  * :class:`core.pricing.OptionPricer` – implémentation de la formule
    fermée de Black–Scholes et des Greeks (delta, gamma, vega, theta, rho).

- ``core.data_io``  

  * :func:`core.data_io.download_history_yahoo` – téléchargement de
    séries de prix quotidiennes via **yfinance**.
  * :func:`core.data_io.compute_spot_and_vol_from_history` – calcul du
    prix spot et de la volatilité annuelle historique.

- ``pages``  

  Regroupe les scripts **Streamlit** :

  * ``Home.py`` – page d'accueil et description du projet,
  * ``01_Monte_Carlo.py`` – pricing et visualisations Monte Carlo,
  * ``02_Black_Scholes.py`` – formule fermée et Greeks,
  * ``03_Binomial.py`` – modèle binomial.


Utilisation rapide
------------------

1. Cloner le dépôt et installer les dépendances (dans un environnement virtuel) ::

     pip install -r requirements.txt

2. Lancer l'application Streamlit depuis la racine du projet ::

     streamlit run Home.py

3. Naviguer entre les pages Monte Carlo, Black–Scholes et Binomial
   via le menu Streamlit.
