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

## 3.3. Pipeline de données (Yahoo → App)

```mermaid
flowchart LR
A[Ticker + dates] --> B[yfinance.download]
B --> C[Prétraitement: ajustements, returns]
C --> D[Calibrage vol: hist/EWMA]
D --> E[Paramètres: S0, r, q, σ, T, K]
E --> F1[Black-Scholes]
E --> F2[Binomial (CRR)]
E --> F3[Monte-Carlo]
F1 & F2 & F3 --> G[Comparaison: prix, Greeks, écarts, IC, temps]
G --> H[Visualisations & export]
```

# 4) Maquettes (wireframes rapides)

## 4.1) Acceuil et calibrage

+-------------------------------------------------------------+
| StreamOptions                                               |
|-------------------------------------------------------------|
| [Ticker] [Start date] [End date] [Download]                 |
| Volatility method: (• Historical) (  EWMA ) (  Manual σ )   |
| If Manual: [σ]                                              |
| Risk-free rate r: [0.02]  Dividend yield q: [0.00]          |
| [Preview data]                                              |
|-------------------------------------------------------------|
| Chart: Price history (line)                                 |
| Box: Calibrated σ, sample size, data freshness              |
+-------------------------------------------------------------+


+-------------------------------------------------------------+
| Option params:  Type: (• Call) (  Put )  K: [strike]  T: [y]|
| Methods: [x] BS  [x] Binomial (Steps: [N])  [x] MC (Paths:M)|
| [Compute]                                                  |
|-------------------------------------------------------------|
| Table: method | price | Δ | Γ | Θ | 𝑽 | ρ | time | IC (MC)  |
|-------------------------------------------------------------|
| Chart 1: Price by method (bar)                             |
| Chart 2: Greeks by method (grouped bars)                   |
+-------------------------------------------------------------+

+-------------------------------------------------------------+
| Convergence controls:  Binomial N: [slider]  MC Paths: [s]  |
|-------------------------------------------------------------|
| Plot A: Price vs N (Binomial) + line → BS price             |
| Plot B: Price vs Paths (MC)  + ribbon = 95% CI              |
| Plot C (optional): Absolute error vs cost (ms)              |
+-------------------------------------------------------------+

