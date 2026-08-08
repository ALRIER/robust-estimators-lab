# Master plan — 7-day build

## Product concept
`Robust Estimators Lab` is a visual teaching and evidence interface around the thesis. It is not a replacement for the R pipeline and it does not retrain the full GA.

## Layer 1 — Build the problem
**Purpose:** teach why estimator ranking changes with the data-generating regime.

Controls:
- distribution family
- skewness / family parameters when relevant
- contamination direction / structure
- contamination rate
- outlier scale
- sample size
- regenerate sample

Outputs:
- clean vs contaminated sample/density
- Mean, Median, Trimmed Mean, Huber, Biweight markers
- compact estimator cards
- comparison panel
- `No single estimator is uniformly best` teaching note

Data source: generated live in Python. No thesis claim is made from this synthetic demonstration.

## Layer 2 — GA search
**Purpose:** make simplex search and evolution intuitive.

Two modes:
### A. DEMO MODE
- lightweight live GA
- 3–5 estimators
- ~30–60 individuals
- ~20–40 generations
- deterministic seed
- selection, crossover, mutation, diversity and convergence
- should complete in seconds

### B. THESIS RESULTS MODE
- final real weights and outcomes from R CSVs
- no invented generational playback

Key visualization:
- triangular simplex slice with three named estimators
- 3D geological error landscape (height = error)
- population dots and path only for DEMO MODE or genuine exported history
- toggle MSE / q95(MSE) where computationally supported
- mandatory caption: `Low-dimensional slice of the full 26-dimensional simplex.`

## Layer 3 — Thesis results explorer
**Purpose:** show what the actual research found.

Filters:
- family
- regime
- source seed
- gate pass/fail
- final selected type
- evidence grade when available

Outputs:
- winner card
- top-26 weight vector / top weights
- GA vs best benchmark mean MSE
- GA vs best benchmark q95(MSE)
- relative gains
- regime description
- explicit pass/fail decision

Teaching examples to preserve:
- a clear discovery-stage GA pass, e.g. Ex-Wald REG03 seed101, for explaining specialist discovery
- a benchmark-retained case, e.g. Ex-Gaussian REG01 seed101, to show the system does not force GA wins
- do not equate discovery pass with fixed-weight confirmation; Layer 4 handles that distinction

## Layer 4 — Validation pipeline
**Purpose:** demonstrate that optimization is not the final evidence.

Visual pipeline:
`Discovery → held-out / fixed-weight validation → bootstrap CI → evidence taxonomy → optional Dirichlet/abstain audit`

Outputs:
- final fixed-weight validation decision
- seed-level expanded gate
- bootstrap confidence intervals
- evidence grade and interpretive note
- validated specialists table
- optional Dirichlet/abstain sanity panel

## Architecture
```text
R research pipeline (read-only archives)
            │
            ▼
curated raw CSVs ──► preprocessing ──► data/processed/*.csv
                                           │
                                           ▼
                                   Python Dash app
                      ┌──────────┬──────────┬──────────┬──────────┐
                      │ Layer 1  │ Layer 2  │ Layer 3  │ Layer 4  │
                      └──────────┴──────────┴──────────┴──────────┘
```

## Seven-day sprint
**Day 1:** repo boot, data contracts, navigation, visual system, Layer 1 skeleton.  
**Day 2:** finish Layer 1; presentation mode; tests.  
**Day 3:** mini-GA + 2D/3D simplex landscape; clear DEMO badge.  
**Day 4:** Layer 3 real-results explorer and winner weights.  
**Day 5:** Layer 4 fixed-weight validation + evidence taxonomy.  
**Day 6:** visual polish, responsiveness, performance, offline packaging.  
**Day 7:** rehearsal mode, backup screenshots/video, bug fixes, freeze.

## Remaining eight days before defense
Do not add major features. Use them for video recording, defense integration, supervisor feedback, typography fixes, and contingency.
