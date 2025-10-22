```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title  Retro plan Option Pricing App 2025 10 21 to 2025 12 12

    section P0 Kickoff
    Skeleton                                   :k1, 2025-10-21, 1d
    README draft                               :k2, 2025-10-22, 3d
    Gantt in README                            :k3, 2025-10-22, 1d
    Branches and CI base                       :k4, 2025-10-27, 2d

    section P1 Data
    Ingest and prep S0 rf                      :d1, 2025-10-29, 4d
    Sigma hist and EWMA                        :d2, 2025-10-30, 4d
    Data tests                                 :d3, 2025-11-04, 1d

    section P2 Engines
    BS and Binomial greeks convN               :p1, 2025-11-06, 5d
    Monte Carlo CI95 timings                   :p2, 2025-11-07, 5d

    section P3 UI
    Streamlit base                             :u1, 2025-11-13, 4d
    Comparisons and conv export                :u2, 2025-11-14, 4d
    Error time table                           :u3, 2025-11-19, 1d

    section P4 QA
    Parity tests and refactor                  :q1, 2025-11-21, 4d
    CI and wheel                               :q2, 2025-11-21, 4d
    Docs and screenshots                       :q3, 2025-11-25, 4d
    Dry run and feedback                       :q4, 2025-12-01, 2d
    Bugfix buffer                              :q5, 2025-12-03, 4d
    Tag v1 0                                   :rel, 2025-12-11, 1d
    Demo and submission                        :fin, 2025-12-12, 1d

```
