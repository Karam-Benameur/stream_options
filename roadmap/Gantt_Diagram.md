```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title  Retro planning compact Option Pricing App 2025 10 21 to 2025 12 12

    section Phase 0 Kickoff
    Project skeleton structure ready                 :k1, 2025-10-21, 1d
    Roadmap README draft                             :k2, 2025-10-22, 3d
    Gantt diagram in README                          :k3, 2025-10-22, 1d
    Repo branches and CI base                        :k4, 2025-10-27, 2d

    section Phase 1 Data and Calibration
    Ingestion and preprocessing S0 calendar rf cache :d1, 2025-10-29, 4d
    Vol calibration hist and EWMA validation         :d2, 2025-10-30, 4d
    Data tests fixtures                              :d3, 2025-11-04, 1d

    section Phase 2 Pricing Engines
    Black Scholes and Binomial price greeks convN    :p1, 2025-11-06, 5d
    Monte Carlo price CI95 timings                   :p2, 2025-11-07, 5d

    section Phase 3 UI and Viz
    Streamlit pages inputs state                     :u1, 2025-11-13, 4d
    Comparisons convergence export                   :u2, 2025-11-14, 4d
    Error and timing table                           :u3, 2025-11-19, 1d

    section Phase 4 QA and Delivery
    Parity and convergence tests refactor            :q1, 2025-11-21, 4d
    CI pytest ruff black packaging wheel             :q2, 2025-11-21, 4d
    Docs screenshots user guide                      :q3, 2025-11-25, 4d
    Dry run and feedback                             :q4, 2025-12-01, 2d
    Bugfix buffer                                    :q5, 2025-12-03, 4d
    Freeze and tag v1 0                              :rel, 2025-12-11, 1d
    Demo and submission                              :fin, 2025-12-12, 1d

```
