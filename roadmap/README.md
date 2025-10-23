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
  subgraph UI[UI – Streamlit]
    P1[Page 1: Monte Carlo]
    P2[Page 2: Black–Scholes]
    P3[Page 3: Binomial]
  end

  subgraph CORE[Core – Pricing & Greeks]
    PR[OptionPricer<br/>(black_scholes, binomial, monte_carlo)]
    GR[Greeks<br/>(delta, gamma, vega...)]
  end

  subgraph DATA[Data – IO & Cache]
    IO[fetch_prices(ticker, start, end)]
    C[(Local cache)]
    API[(Yahoo Finance)]
  end

  subgraph VIZ[Visualization – Utils]
    PL[plotting.py<br/>(payoff, paths, convergence)]
  end

  subgraph QA[Quality]
    T[pytest]
    CI[GitHub Actions<br/>(tests + lint)]
  end

  %% Flux
  P1 --> PR
  P2 --> PR
  P3 --> PR
  P1 --> IO
  P2 --> IO
  P3 --> IO
  PR --> GR
  PR --> PL
  IO --> C
  IO --> API
  UI --> PL
  T --> PR
  CI --> T
```
