# Projet Logiciel Gr.5:" StreamOptions — Tarification d’options européennes (BS / Binomial / Monte-Carlo)"
Auteurs:
  - Ayoub MALOUM
  - Esperance DJOSSOU
  - Karam BENAMEUR
    
format:
  html:
    toc: true
    number-sections: true
    theme: cosmo
---

# 1) Nom du projet

**Nom du module** : `stream_options`  
**Titre** : *Application Streamlit pour calibrer et comparer le prix d’options européennes (call/put) via Black-Scholes, Binomial et Monte-Carlo, avec analyse des écarts, Greeks, convergence et incertitude.*

---

# 2) Minimum Viable Project (MVP)

## 2.1 Objectif utilisateur
- Saisir un **ticker** (ex. `AAPL`), **strike K**, **échéance T**, **r**, **dividendes q** (ou 0).
- Récupérer les **données Yahoo Finance** (spot, historique, dividendes).
- **Calibrer σ** (vol historique simple ou EWMA) ou saisir une **vol implicite** manuelle.
- **Tarifer** l’option européenne **Call/Put** par **3 méthodes** : Black-Scholes (fermé), **Binomial CRR**, **Monte-Carlo**.
- Afficher **prix + Greeks (Δ, Γ, Θ, 𝑽, ρ)**, **écarts entre méthodes**, **temps de calcul**, **IC 95% MC**.
- Visualiser la **convergence** (Binomial: prix vs nombre de pas N; MC: prix & IC vs nombre de trajectoires M).

## 2.2 Hors-scope MVP
- Options américaines / exotiques, modèles de volatilité stochastique, scraping auto des volatilités implicites.

---

# 3) Architecture du projet

## 3.1 Arborescence prévue

gantt
  title StreamOptions — Rétroplanning (Semaines 1 → 5)
  dateFormat  YYYY-MM-DD
  excludes    weekends

  %% === Phase 0 : Initialisation ===
  section Setup
  Création repo + branches (master/dev)   :done,    s1, 2025-10-21, 1d
  Squelette projet (app/core/tests)       :active,  s2, after s1, 2d
  Requirements + README                   :         s3, after s2, 1d

  %% === Phase 1 : Données & Calibrage ===
  section Données & Calibrage
  Intégration Yahoo (yfinance)            :        d1, 2025-10-24, 2d
  Prétraitement & S0                      :        d2, after d1, 1d
  Calibrage σ (historique / EWMA)         :        d3, after d2, 2d

  %% === Phase 2 : Moteurs de pricing ===
  section Tarification
  Black-Scholes + Greeks                  :        p1, 2025-10-28, 1d
  Binomial (CRR) + Greeks (FD)            :        p2, after p1, 2d
  Monte-Carlo (+ IC 95% + timings)        :        p3, after p2, 2d

  %% === Phase 3 : UI & Visualisations ===
  section UI & Visualisation
  Pages Streamlit (params, résultats)     :        u1, 2025-11-03, 2d
  Graphiques comparatifs (prix/greeks)    :        u2, after u1, 1d
  Convergence (Binomial N / MC M)         :        u3, after u2, 2d

  %% === Phase 4 : Qualité & Livraison ===
  section QA & Livraison
  Tests unitaires (parité, conv.)         :        q1, 2025-11-06, 2d
  Polissage + doc + capture               :        q2, after q1, 1d
  Démo & feedback                         :        dl, 2025-11-10, 1d


