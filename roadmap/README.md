# Projet Logiciel Gr.5:" StreamOptions — Tarification d’options européennes (BS / Binomial / Monte-Carlo)"
Auteurs:
  - Ayoub MALOUM
  - Esperance DJOSSOU
  - Karam BENAMEUR


# 1) Nom du projet et idée du concept

**Nom du module** : `stream_options`  
**Idée** : Ce projet consiste à user de Streamlit pour calibrer et comparer le prix d’options européennes (call/put) via 3 différentes méthodes qui sont: Black-Scholes, Binomial et Monte-Carlo.
Suite à cela, sur le site on rendra possible l'analyse des écarts, Greeks, une étude des convergences et d'incertitude.

---

# 2) Minimum Viable Project (MVP)

## 2.1 Objectif utilisateur
- Saisir un **ticker** (ex. `AAPL`), **strike K**, **échéance T**, **r**, **dividendes q** (ou 0).
- Récupérer les **données Yahoo Finance** (spot, historique, dividendes).
- **Calibrer σ** (vol historique simple ou EWMA) ou saisir une **vol implicite** manuelle.
- **Tarifer** l’option européenne **Call/Put** par **3 méthodes** : Black-Scholes (fermé), **Binomial CRR**, **Monte-Carlo**.
- Afficher **prix + Greeks (Δ, Γ, Θ, 𝑽, ρ)**, **écarts entre méthodes**, **temps de calcul**, **IC 95% MC**.
- Visualiser la **convergence** (Binomial: prix vs nombre de pas N; MC: prix & IC vs nombre de 
## 2.2 Hors-scope MVP
- Options américaines / exotiques, modèles de volatilité stochastique, scraping auto des volatilités implicites.

-
# 3) Architecture du projet

## 3.1 Arborescence 


## 3.2. Pile technologique
- **Python 3.11+**
- **Streamlit** (UI), **yfinance** (données Yahoo), **NumPy / SciPy / pandas**
- **plotly** (graphiques interactifs), **joblib** (cache)
- **pytest** (tests), **ruff/black** (lint/format)

``` mermaid
flowchart LR
  %% UI
  subgraph UI ["UI - Streamlit app"]
    NAV["Sidebar router\n(Monte Carlo | Black-Scholes | Binomial)"]
    IN_COMMON["Inputs communs\n(ticker, start/end, call/put, strike K, rate r, vol σ)"]
    IN_SPEC["Inputs spécifiques\n(MC: paths • BS: maturity • Binomial: steps)"]
    ACTIONS["Actions\n(Price by time • Simulation)"]
    PLOTS["Plots panel\n(Time series • Payoff • Paths/Convergence)"]
  end

  %% Data services
  subgraph DATA ["Services - Data"]
    FETCH["fetch_prices(ticker, dates)"]
    VOL["Volatility estimator\n(historique; implied plus tard)"]
    CACHE[("st.cache_data / local cache")]
    API[("Yahoo Finance")]
  end

  %% Core pricing
  subgraph CORE ["Core - Pricing"]
    PRICER["OptionPricer class"]
    BS["Engine: Black-Scholes"]
    BINOM["Engine: Binomial"]
    MC["Engine: Monte Carlo"]
  end

  %% Analytics & viz
  subgraph ANALYTICS ["Analytics"]
    GREEKS["Greeks\n(delta, gamma, vega, theta, rho)"]
    COMP["Compare methods\n(BS vs Binomial vs MC)"]
  end

  subgraph VIZ ["Visualization utils"]
    PLOTUTILS["plotting.py\n(payoff, paths, convergence)"]
  end

  subgraph QA ["Quality"]
    TESTS["pytest"]
    CI["GitHub Actions\n(tests + lint)"]
  end

  %% Flows
  NAV --> IN_COMMON
  IN_COMMON --> IN_SPEC
  IN_COMMON --> FETCH
  IN_SPEC --> PRICER
  ACTIONS --> FETCH
  ACTIONS --> PRICER

  FETCH --> CACHE
  FETCH --> API
  FETCH --> VOL
  VOL --> PRICER

  PRICER --> BS
  PRICER --> BINOM
  PRICER --> MC

  BS --> GREEKS
  BINOM --> COMP
  MC --> COMP

  BS --> PLOTUTILS
  BINOM --> PLOTUTILS
  MC --> PLOTUTILS
  PLOTUTILS --> PLOTS
  GREEKS --> PLOTS
  COMP --> PLOTS

  TESTS --> CORE
  CI --> TESTS


```
UI → Core : les pages appellent les méthodes de pricing.

UI → Data : récupère les prix (avec cache).

Core → Greeks/Plots : calcule greeks, renvoie des objets/figures.

QA : tests locaux (pytest), exécutés automatiquement par GitHub Actions.

# 6) Choix des packages et justifications

Tech stack & pourquoi ces choix

streamlit — UI rapide et reproductible :
Permet de construire l’interface (sidebar, pages “Monte Carlo / Black-Scholes / Binomial”, formulaires d’entrée, affichage des graphiques) en quelques lignes. Cache intégré (st.cache_data) pour éviter de recharger les données à chaque interaction. (Alternatives : Dash, Gradio ; Streamlit est plus simple et suffit pour notre MVP.)

numpy — calcul numérique vectorisé :
Simulation des trajectoires GBM en Monte Carlo, opérations vectorielles dans l’arbre binomial, calculs intermédiaires (log, exp, racines) pour 
𝑑
1
,
𝑑
2
d
1
	​

,d
2
	​

 de Black-Scholes. Réduit le temps de calcul vs. boucles Python pures.

pandas — séries temporelles & préparation des données :
Gestion des prix historiques (index temps), resampling, jointures éventuelles, calcul de rendements et de volatilité historique, traitement des valeurs manquantes avant le pricing.

scipy — fonctions statistiques et outils numériques :
scipy.stats.norm.cdf/pdf pour Black-Scholes (loi normale), éventuellement optimize (recherche de racines / calibration de volatilité implicite) et interp si besoin. Évite de re-coder des briques mathématiques sensibles.

yfinance — téléchargement programmatique des prix :
Récupère les séries OHLCV d’un ticker sur une période donnée. Assure la reproductibilité (scriptable, pas de téléchargement manuel) et alimente les pages “Price by time”. (On pourra cacher les résultats localement.)

matplotlib — graphiques de base & figures statiques :
Payoff call/put, courbes de convergence (prix vs #pas/#trajectoires), exports d’images simples pour le dossier roadmap/pictures.

plotly — graphiques interactifs dans l’UI :
Zoom, hover, tooltips dans Streamlit pour les trajectoires Monte Carlo et les historiques de prix. Améliore l’explicabilité et la démonstration en séance.

pytest — tests unitaires & non-régression :
Vérifie (i) que le prix binomial converge vers Black-Scholes, (ii) que des propriétés de monotonie tiennent (ex. prix ↑ quand σ ↑), (iii) que les fonctions lèvent les bonnes erreurs. Base de la CI.

black / isort / flake8 — qualité & standard PEP8 :
Mise en forme automatique (black), import triés (isort), règles de lint (flake8). Garantit un code lisible, cohérent entre contributeurs et facile à relire par le correcteur.

(optionnel) numba — accélération JIT :
Compile en natif les boucles lourdes (génération de chemins MC, parcours d’un arbre binomial). Gain typique ×5 à ×50 selon la taille (utile pour les démonstrations de performance “Time/Memory efficiency”).



