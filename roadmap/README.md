# Projet Logiciel Gr.5:" StreamOptions — Tarification d’options européennes (BS / Binomial / Monte-Carlo)"
Auteurs:
  - Ayoub MALOUM
  - Esperance DJOSSOU
  - Karam BENAMEUR 22201020


# 1) Nom du projet et idée du concept

**Nom du module** : `stream_options`  
**Idée** : Ce projet consiste à user de Streamlit pour calibrer et comparer le prix d’options européennes (call/put) via 3 différentes méthodes qui sont: Black-Scholes, Binomial et Monte-Carlo.
Suite à cela, sur le site on rendra possible l'analyse des écarts, Greeks, une étude des convergences et d'incertitude.

---

# 2) Objectifs et utilité

L’application, structurée comme dans nos maquettes (sidebar **Monte Carlo Method**, **Black and Scholes Method**, **Binomial Method**), a un double but **pédagogique** et **pratique**. Depuis les mêmes **inputs** (ticker, période, call/put, **Strike Price**, **Discount Rate**, **Volatility**) et des champs **spécifiques** à chaque page (**Number of Simulation** pour Monte Carlo, **Maturity** pour Black-Scholes, **Steps** pour Binomial), l’utilisateur lance deux parcours : **Price by time** (graphique d’historique à gauche) pour visualiser et contextualiser le sous-jacent, puis **Simulation** (panneau de droite) pour calculer et afficher **prix** et **graphiques clés** (payoff, trajectoires MC, convergence avec #paths/#steps, puis Greeks sur BS). Cette mise en parallèle rend visibles les **hypothèses** (GBM, volatilité), les **compromis précision/temps de calcul** et la **cohérence entre méthodes**. Elle sert à **comparer** rapidement les approches, **explorer des scénarios** (variations de \(K, T, \sigma, r\)) et **choisir la méthode** adaptée au contexte. Les données sont **téléchargées de façon programmatique** (reproductibilité) et mises en cache pour une UX fluide. *Mid-term : le flux « Price by time » et le squelette des pages sont démontrés ; les calculs complets (prix/Greeks) sont finalisés pour le livrable final.*

## 2.1) Comment ça se passe ?

### a) Étapes communes (toutes les pages)
1. **Select Ticker** : entre le symbole (ex. `AAPL`, `BNP.PA`, `^GSPC`).
2. **Start date / End date** : choisis la période d’historique.
3. **Call or Put** : sélectionne le type d’option.
4. **Strike Price (K)** : saisis le strike.
5. **Discount Rate (r)** : taux sans risque (ex. `0.02` = 2%).
6. **Volatility (σ)** : valeur choisie ou issue d’une estimation (historique).
7. Cliquer sur **Price by time** pour afficher l’historique du sous-jacent (graphe de gauche).

**Recommandations**
- σ typique entre **0.10** et **0.60** ; r entre **0.00** et **0.05**.  
- Si pas sûr de σ, commencer par **Price by time**, observe la variabilité, puis ajuster.

---

### b) Particularités par méthode (champs spécifiques)

- **Monte Carlo Method**
  - **Number of Simulation** : nombre de trajectoires (ex. 10 000 → 50 000).
  - *(optionnel)* **Seed** : pour reproduire exactement le résultat.(A voir si on l'ajoute)
- **Black and Scholes Method**
  - **Maturity (T)** : maturité **en années** (ex. `0.5` = 6 mois).
  - (Greeks calculés à partir des mêmes entrées communes.)
- **Binomial Method**
  - **Steps** : nombre d’étapes de l’arbre (ex. 100 → 500).  
    Plus c’est grand, plus le prix **converge** vers Black-Scholes.

---

### c) Ce que tu obtiens selon la méthode

- **Monte Carlo**
  - **Option price (MC)** + **IC 95%** (intervalle de confiance).
  - **Simulated paths** (trajectoires) et/ou **Convergence** (prix vs #paths).
  - **Payoff** à l’échéance.
- **Black-Scholes**
  - **Option price (BS)** (référence fermée).
  - **Greeks** : Delta, Gamma, Vega, Theta, Rho.
  - **Payoff** avec repère du strike.
- **Binomial**
  - **Option price (Binomial)**.
  - **Convergence** du prix quand **Steps** augmente (doit tendre vers BS).

> Dans tous les cas, le graphe **Price by time** (gauche) montre l’historique du sous-jacent pour contextualiser la période choisie.

---

### d) Comment prendre une décision (playbook rapide)

1. **Valide les données** : via **Price by time**, vérifie que la période est cohérente (pas d’anomalies évidentes).
2. **Choisis/ajuste σ** :
   - Démarre avec une **vol historique** raisonnable (ex. 20%).
   - Ajuste σ jusqu’à obtenir une **cohérence** MC / Binomial / BS (écarts faibles).
3. **Compare les méthodes** :
   - **BS** = référence rapide pour une européenne sans dividendes.
   - **Binomial** = contrôle de **convergence** (augmente Steps si besoin).
   - **MC** = donne un **prix avec marge d’erreur** (IC 95%).
4. **Si tu as un prix de marché** (option chain) :
   - Si **Prix_modèle < Prix_marché** → option possiblement **surévaluée**.
   - Si **Prix_modèle > Prix_marché** → option possiblement **sous-évaluée**.
5. **Regarde les Greeks (BS)** :
   - **Delta** (exposition directionnelle), **Vega** (sensibilité à σ), **Theta** (érosion temps).
   - Choisis **K** et **T** selon ton risque/timing.
6. **Robustesse** :
   - **MC** : IC trop large → **augmente** le nombre de simulations.
   - **Binomial** : prix instable → **augmente** Steps jusqu’à stabilisation.

**Valeurs guidées**
- **Volatility (σ)** : 0.20 pour démarrer, puis ajuste.
- **Discount Rate (r)** : 0.02 (USD) / 0.01 (EUR) par défaut.
- **Maturity (T)** : 0.25 / 0.5 / 1.0 (trimestre / semestre / 1 an).
- **Number of Simulation (MC)** : 10 000 → 50 000.
- **Steps (Binomial)** : 100 → 500 (voire 1000 si besoin de stabilité).


# 3) Pipeline 

``` mermaid

flowchart TB
  %% --- Entrée utilisateur ---
  U["Utilisateur"]

  %% --- UI ---
  subgraph UI ["UI - Streamlit"]
    IN["Inputs communs + spécifiques<br/>(ticker, dates, call/put, K, r, σ, T / Steps / #paths)"]
    NAV["Sidebar (Monte Carlo | Black-Scholes | Binomial)"]
  end

  %% --- Data IO & Cache ---
  subgraph DATA ["Data IO & Cache"]
    IO["core/io.py<br/>fetch_prices() • risk_free_rate()"]
    NORM["Normalisation<br/>(UTC, colonnes OHLCV, ret/logret)"]
    CACHE[("Cache local .parquet<br/>+ st.cache_data")]
    API[("Yahoo Finance")]
  end

  %% --- Core & Viz ---
  subgraph CORE ["Core - Pricing"]
    PR["pricing.py<br/>class OptionPricer(...)"]
    BS["black_scholes()"]
    BIN["binomial(steps)"]
    MC["monte_carlo(paths)"]
  end

  subgraph VIZ ["Visualization utils"]
    PLOT["utils/plotting.py<br/>price_history • payoff • mc_paths • convergence"]
  end

  OUTL["Colonne gauche<br/>Price by time"]
  OUTR["Colonne droite<br/>Prix + IC/Greeks + Graphiques"]

  %% --- Flows ---
  U --> IN
  NAV --> IN
  IN <--> |"requête d'historique / DataFrame prêt à tracer"| IO
  IO --> |"download"| API
  IO --> NORM --> CACHE
  IO --> NORM

  IN --> PR
  PR --> BS --> PLOT
  PR --> BIN --> PLOT
  PR --> MC  --> PLOT

  NORM --> PLOT
  PLOT --> OUTL
  PLOT --> OUTR


```

## 3.1) Explication

### a) Parcours complet — étape par étape (selon le schéma)

1) **Saisie utilisateur**
   - L’utilisateur tape : **Ticker** (`AAPL`, `BNP.PA`…), **Dates** (Start/End), **Call/Put**, **Strike K**, **Discount rate r**, **Volatility σ**.
   - Il choisit la page dans la **Sidebar** : **Monte Carlo**, **Black-Scholes** ou **Binomial**.

2) **Envoi vers l’UI (Streamlit)**
   - Le formulaire **Inputs communs + spécifiques** reçoit ces valeurs.
   - Si la page sélectionnée exige un champ en plus, il apparaît :
     - Monte Carlo → **#paths** (Number of Simulation)
     - Black-Scholes → **T** (Maturity, en années)
     - Binomial → **Steps** (nombre d’étapes de l’arbre)

3) **Demande de données (aller)**
   - L’UI appelle **`core/io.py::fetch_prices(ticker, start, end)`** pour récupérer l’historique des prix.

4) **Téléchargement & normalisation**
   - `fetch_prices` récupère les données (Yahoo Finance si cache manquant), puis **normalise** :
     - index en **UTC**, colonnes **OHLCV** (Open, High, Low, Close, Volume),
     - calcul des **retours** : `ret = Close.pct_change()`, `logret = log(C_t/C_{t-1})`,
     - tri et déduplication.

5) **Cache (retour)**
   - Les données normalisées sont renvoyées à l’UI **et** stockées :
     - en **fichier** (`.parquet` dans *Bases de données/*),
     - en **mémoire** via `st.cache_data` (réutilisation rapide).

6) **Contexte marché (gauche)**
   - L’UI trace **Price by time** (courbe de Close) dans la **colonne gauche** pour contextualiser la période.

7) **Paramétrage du cœur de calcul**
   - L’UI construit **`OptionPricer(S0, K, r, σ, T, kind)`** à partir de l’historique (S0 = dernier Close) et des entrées.

8) **Calcul selon la page**
   - **Monte Carlo** → `monte_carlo(paths)` : simule des trajectoires et renvoie **prix** + **IC95%** (intervalle de confiance).
   - **Black-Scholes** → `black_scholes()` : renvoie **prix** (formule fermée) + **Greeks** (Delta, Gamma, Vega, Theta, Rho).
   - **Binomial** → `binomial(steps)` : renvoie **prix** + info de **convergence** (vers BS quand Steps ↑).

9) **Visualisation des résultats (droite)**
   - `utils/plotting.py` génère les figures :
     - **payoff** (diagramme de gain/perte),
     - **mc_paths** (trajectoires simulées) et/ou **convergence** (prix vs #paths/#steps),
     - éventuellement courbe(s) de **Greeks** (page BS).
   - L’UI affiche ces résultats dans la **colonne droite** : *Prix + IC/Greeks + Graphiques*.

10) **Décision utilisateur**
    - **Vérifie** la cohérence : BS (référence) ≈ Binomial (si Steps suffisant), MC dans un **IC** raisonnable.
    - **Ajuste σ** si besoin (jusqu’à cohérence), puis décide (ex. comparer au **prix de marché** au final).

---

### b) Glossaire des blocs & termes du schéma

#### UI – Streamlit
- **Sidebar** : menu qui choisit la page **Monte Carlo / Black-Scholes / Binomial**.
- **Inputs communs** : `ticker`, `start/end`, `call/put`, **K**, **r**, **σ**.  
- **Inputs spécifiques** :
  - **T (Maturity)** : temps jusqu’à l’échéance en **années** (ex. 0.5 = 6 mois) — page BS.
  - **Steps** : granularité de l’arbre binomial — page Binomial.
  - **#paths** : nombre de trajectoires Monte Carlo — page MC.

#### Data IO & Cache
- **`core/io.py::fetch_prices()`** : télécharge l’historique (Yahoo Finance), gère erreurs/paramètres, renvoie un **DataFrame prêt à tracer**.
- **Normalisation** :
  - **UTC** : dates/horaires standardisés en fuseau **UTC**.
  - **OHLCV** : colonnes **O**pen, **H**igh, **L**ow, **C**lose, **V**olume.
  - **ret / logret** : retours simples et logarithmiques pour estimer la volatilité.
- **Yahoo Finance** : source **gratuite** d’historiques (via package `yfinance`).
- **Cache local `.parquet`** : fichier compact lisible/écrivible rapidement.
- **`st.cache_data`** : mémorise en RAM le résultat d’une fonction pour éviter de re-télécharger.

#### Core – Pricing
- **`pricing.py::OptionPricer`** : classe qui regroupe les paramètres `(S0, K, r, σ, T, kind)` et expose 3 méthodes :
  - **`black_scholes()`** : **formule fermée** pour option européenne ; rapide ; fournit **Greeks**.
  - **`binomial(steps)`** : **arbre CRR** ; le prix **converge** vers BS quand *Steps ↑*.
  - **`monte_carlo(paths)`** : **simulation** de scénarios ; renvoie **prix** + **IC95%** (marge d’erreur).

#### Visualization utils
- **`utils/plotting.py`** : helpers de graphiques
  - **`price_history(df)`** : courbe d’historique (gauche).
  - **`payoff(K, kind)`** : diagramme payoff call/put.
  - **`mc_paths(array)`** : trajectoires simulées.
  - **`convergence(x,y)`** : prix vs #paths/#steps.
- **Colonne gauche** : **Price by time** (historique du sous-jacent).
- **Colonne droite** : **Prix + IC/Greeks + Graphiques** (résultats de la page).

#### Paramètres financiers (rappel)
- **S0** : prix actuel du sous-jacent (dernier **Close**).
- **K (Strike)** : prix d’exercice de l’option.
- **r (Discount rate)** : taux sans risque (ex. 0.02 = 2 %).
- **σ (Volatility)** : volatilité annuelle (ex. 0.20 = 20 %).
- **T (Maturity)** : temps jusqu’à échéance, en années.
- **Call/Put** : droit d’**acheter** / **vendre** au strike K.
- **Steps** : nombre d’étapes du modèle binomial.
- **#paths** : nombre de trajectoires simulées en Monte Carlo.

#### Sorties & interprétation
- **BS (référence)** : prix “théorique” rapide pour européenne, + **Greeks** :
  - **Delta** (sensibilité au sous-jacent), **Vega** (à σ), **Theta** (au temps), **Gamma** (courbure), **Rho** (au taux).
- **Binomial** : vérifie la **convergence** vers BS en augmentant *Steps*.
- **Monte Carlo** : fournit un **prix** avec **IC95%** (estimateur ± marge) ;
  - IC trop large → **augmenter `#paths`**.

---

## Conseils rapides (valeurs par défaut)
- **σ** : 0.20 pour démarrer, puis ajuster.
- **r** : 0.02 (USD) / 0.01 (EUR) par défaut (placeholder mid-term).
- **T** : 0.25 / 0.5 / 1.0 (trimestre / semestre / 1 an).
- **#paths (MC)** : 10 000 → 50 000.
- **Steps (Binomial)** : 100 → 500 (voire 1000 si besoin).

> Les méthodes peuvent rester **stubs** (squelettes) tant que l’architecture, le pipeline et l’affichage “Price by time” fonctionnent. Le **final** apportera implémentations complètes, tests/CI, et étude temps/mémoire.



# 4) Tech stack et justifications

- **streamlit** — UI rapide et reproductible : construit la barre latérale et les 3 pages (Monte Carlo / Black-Scholes / Binomial) avec peu de code ; cache intégré (`st.cache_data`) pour éviter les rechargements.

- **numpy** — calcul numérique vectorisé : simulation des trajectoires GBM (Monte Carlo), opérations du modèle binomial, calcul efficace des intermédiaires de Black-Scholes (`d1`, `d2`).

- **pandas** — séries temporelles & préparation des données : gestion des prix historiques (index temps), resampling, rendements, estimation de volatilité glissante, traitement des manquants.

- **scipy** — statistiques & numérique fiables : `scipy.stats.norm.cdf/pdf` pour Black-Scholes ; `optimize` possible pour calibrer la volatilité implicite.

- **yfinance** — téléchargement programmatique des prix (reproductible) : récupère les données OHLCV par ticker/période, sans téléchargement manuel ; compatible avec le cache local.

- **matplotlib** — figures statiques pour le rapport : payoff call/put et courbes de convergence (prix vs. #pas/#trajectoires), export d’images vers `roadmap/pictures`.

- **plotly** — graphiques interactifs dans Streamlit : zoom, survol/infobulles pour l’historique des prix et les trajectoires Monte Carlo ; améliore l’explicabilité en démo.

- **pytest** — tests unitaires & non-régression : vérifie la convergence binomiale vers Black-Scholes, la monotonie en σ, et la gestion des erreurs ; base de la CI.

- **black / isort / flake8** — qualité & PEP8 : formatage auto (black), imports triés (isort) et linting (flake8) pour un code lisible et cohérent entre contributeurs.

- **numba** *(optionnel)* — accélération JIT : compile les boucles lourdes (MC / binomial) et peut apporter des gains ×5 à ×50 ; utile pour le critère “Time/Memory efficiency”.


# 5) Bases de données (choix & pourquoi)

| Source / Base             | À quoi ça sert dans l’app (référence aux écrans)                                                | Pourquoi ce choix (mid-term)                          | Implémentation prévue |
|---|---|---|---|
| **Yahoo Finance** (via `yfinance`) | **Price by time** (graphe de gauche) ; donne le **prix spot S₀** et l’historique pour estimer une **volatilité historique** | Gratuit, simple, scriptable → reproductible           | `core/io.py::fetch_prices()` + cache `.parquet` |
| **Taux sans risque** (placeholder) | Champ **Discount Rate (r)** des 3 pages (valeur fixe mid-term)                         | Suffisant au mid-term ; API au **final**              | `core/io.py::risk_free_rate()` (USD→2%, EUR→1%) |
| *(Optionnel final)* **FRED/ECB**   | Remplacer **r** par un **taux de marché** (USD/EUR)                                     | Source officielle, API stable                         | `core/io.py::fetch_risk_free_*()` (final) |
| *(Optionnel final)* **Option chain** (yfinance) | Comparer **prix modèle** vs **prix marché** (sanity check)                         | Utile pour l’évaluation, pas requis mid-term          | `core/io.py::fetch_option_chain()` (final) |
| *(Optionnel)* **Calendrier boursier** (`pandas-market-calendars`) | Nettoyer les jours non-trading si besoin                                          | Pour éviter les trous de calendrier                    | `utils/dates.py` (final/si nécessaire) |

**Schéma des champs (Yahoo Finance)** : `Date (index UTC)`, `Open`, `High`, `Low`, `Close` (ou `Adj Close` → **Close**), `Volume`, `ret`, `logret`.  
**Suffixes utiles** : Euronext Paris = `.PA` (`BNP.PA`), indices parfois `^GSPC`, `^FCHI`, etc.  
**Reproductibilité** : pas de données brutes dans Git → **cache local** (`data/*.parquet`) + `st.cache_data` côté UI.

---

# 6) Member taks

| Membre  | Rôle principal         | Branches                     |
| ------- | ---------------------- | ---------------------------- |
| <Nom 1> | Data IO & cache        | `feature/data-io`            |
| <Nom 2> | Black-Scholes + Greeks | `feature/black-scholes`      |
| <Nom 3> | Binomial (convergence) | `feature/binomial`           |
| <Nom 4> | Monte Carlo (paths/IC) | `feature/monte-carlo`        |
| <Nom 5> | UI Streamlit & docs    | `feature/ui`, `docs/roadmap` |
