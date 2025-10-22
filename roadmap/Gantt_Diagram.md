```mermaid
gantt
    title Rétro-planning compact — Option Pricing App (27/10 → 12/12/2025)
    dateFormat  YYYY-MM-DD

    section Phase 0 – Kickoff
    Snapshot + repo/branches/CI skeleton           :s0, 2025-10-27, 2d

    section Phase 1 – Données & Calibration (parallèle)
    Ingestion + prétraitements (S0, calendrier, r_f, cache) :d1, 2025-10-29, 4d
    Calibration σ (historique & EWMA) + validation          :d2, 2025-10-30, 4d
    Tests data (fixtures rapides)                           :d3, 2025-11-04, 1d
    M1 Données prêtes                                       :milestone, m1, 2025-11-05, 0d

    section Phase 2 – Pricing Engines (parallèle)
    BS + Binomial (prix & Greeks) + conv N                  :p1, 2025-11-06, 5d
    Monte-Carlo (prix, IC95%, timings)                      :p2, 2025-11-07, 5d
    M2 Moteurs OK                                           :milestone, m2, 2025-11-12, 0d

    section Phase 3 – UI & Viz (parallèle)
    Streamlit : pages, inputs, state                        :u1, 2025-11-13, 4d
    Viz comparatives + convergence + export                 :u2, 2025-11-14, 4d
    Tableau erreurs/temps                                   :u3, 2025-11-19, 1d
    M3 UI prête                                             :milestone, m3, 2025-11-20, 0d

    section Phase 4 – QA & Delivery (parallèle)
    Parity/conv tests + refactor                            :q1, 2025-11-21, 4d
    CI complète (pytest, ruff/black) + packaging/wheel      :q2, 2025-11-21, 4d
    Docs + screenshots + guide utilisateur                  :q3, 2025-11-25, 4d
    Dry-run + feedback                                      :q4, 2025-12-01, 2d
    Buffer bugfix                                           :q5, 2025-12-03, 4d
    Freeze & tag v1.0                                       :rel, 2025-12-11, 1d
    Démo & rendu                                            :fin, 2025-12-12, 1d

```
