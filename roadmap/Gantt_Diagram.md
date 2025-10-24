
```mermaid
gantt
    title Rétro-planning - Option Pricing App (22/10 → 12/12/2025)
    dateFormat  YYYY-MM-DD

    section Phase 0 – Structure 
    GitHub creation                     :s1, 2025-09-18, 1d
    Brainstroming (ideas of the subject):s2, 2025-09-20, 25d
    Skeleton of the project             :s3, 2025-10-15, 6d
    Snapshot (README+images+Gantt)      :s4, 2025-10-21, 4d
    Repo & branches                     :s5, 2025-10-24, 1d
    Gantt_Diagram                       :s6, 2025-10-21, 1d

    section Phase 1 - Données & Calib
    yfinance + cache                      :p1a, 2025-10-24, 2d
    Pré-traitement (S0, calendrier, rf)   :p1b, 2025-10-26, 3d
    Sigma hist & EWMA (comparatif)        :p1c, 2025-10-28, 3d
    Tests data (fixtures)                 :p1d, 2025-10-30, 2d
    M1 Données prêtes                     :milestone, m1, after p1d, 0d

    section Phase 2 - Pricing Engines
    Black-Scholes + Greeks + tests        :p2a, 2025-10-31, 4d
    Binomial CRR + Greeks + convergence   :p2b, 2025-11-03, 3d
    Monte-Carlo + IC95% + timings         :p2c, 2025-11-05, 6d
    M2 Moteurs OK                         :milestone, m2, after p2c, 0d

    section Phase 3 - UI & Viz
    Streamlit (pages/inputs/state)        :p3a, 2025-11-08, 7d
    Comparatifs prix/greeks + export      :p3b, 2025-11-12, 5d
    Convergences (N / traj. MC)           :p3c, 2025-11-14, 5d
    Tableau erreurs/temps                 :p3d, 2025-11-16, 7d
    M3 UI prête                           :milestone, m3, after p3d, 0d

    section Phase 4 - QA & Delivery
    Parity & conv tests croisés           :p4a, 2025-11-22, 3d
    CI (pytest, ruff/black, wheel)        :p4b, 2025-11-24, 6d
    Docs + screenshots + guide            :p4c, 2025-11-25, 6d
    Packaging (licence, versioning)       :p4d, 2025-11-29, 4d
    Dry-run & feedback                    :p4e, 2025-12-02, 5d
    Buffer bugfix                         :p4f, 2025-12-06, 4d
    Freeze & tag v1.0                     :rel, 2025-12-11, 1d
    Démo & rendu                          :fin, 2025-12-12, 1d


```




















```mermaid
gantt
    title Pipeline de Développement - StreamOptions
    dateFormat  YYYY-MM-DD
    axisFormat %d/%m
    
    section Phase 1: Setup & Architecture
    Initialisation projet      :done, setup1, 2024-01-01, 5d
    Structure fichiers         :done, setup2, after setup1, 3d
    Configuration Git          :done, setup3, after setup2, 2d
    
    section Phase 2: Data Layer & Cache
    Module core/io.py          :active, data1, 2024-01-10, 5d
    fetch_prices() Yahoo Finance :data2, after data1, 4d
    risk_free_rate()           :data3, after data2, 2d
    Normalisation données      :data4, after data3, 3d
    Cache .parquet + st.cache_data :data5, after data4, 3d
    
    section Phase 3: Core Pricing
    pricing.py - OptionPricer  :core1, 2024-01-20, 4d
    black_scholes() méthode    :core2, after core1, 4d
    binomial(steps) arbre      :core3, after core2, 5d
    monte_carlo(paths) simulation :core4, after core3, 5d
    
    section Phase 4: Visualisation
    utils/plotting.py          :viz1, 2024-02-05, 4d
    price_history graphs       :viz2, after viz1, 3d
    payoff diagrams            :viz3, after viz2, 2d
    mc_paths visualisation     :viz4, after viz3, 3d
    convergence analysis       :viz5, after viz4, 3d
    
    section Phase 5: Intégration UI
    Colonne gauche - Price by time :ui1, 2024-02-15, 3d
    Colonne droite - Résultats     :ui2, after ui1, 4d
    IC/Greeks/Graphiques          :ui3, after ui2, 4d
    
    section Phase 6: Documentation
    README.md principal        :doc1, 2024-03-01, 3d
    theoretical_images.md      :doc2, after doc1, 2d
    Gantt_Diagram.md           :doc3, after doc2, 2d
    Bases de données docs      :doc4, after doc3, 2d
    
    section Phase 7: Finalisation
    Tests intégration          :final1, 2024-03-10, 4d
    Optimisation performance   :final2, after final1, 3d
    Revue code                 :final3, after final2, 2d
    Déploiement                :final4, after final3, 2d
```











```




