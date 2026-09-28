# Master plan — canonical Streamlit defense app

## Product concept
`Robust Estimators Lab` is the live visual interface for the thesis defense. It teaches the statistical problem, explains the GA search, and presents precomputed thesis evidence without rerunning the full research pipeline.

## Canonical runtime
- Framework: Streamlit + Plotly
- Branch: `main`
- Entrypoint: `streamlit_app.py`
- Runtime data: bundled CSVs under `data/raw/` and `data/processed/`

## Defense structure

### 00 · Cover
Opening title, thesis framing, and navigation.

### 01 · Research logic
Explains:
- fixed estimand `E[X]`
- regime dependence
- simplex-constrained composite estimators
- H1–H4 reasoning chain

### 02 · Data-generating world
Shows the controlled simulation world, distribution families, contamination structures, and validation coverage.

### 03 · Simulation lab
Live deterministic pedagogical sample construction. This is teaching output, not thesis evidence.

### 04 · Monte Carlo engine
Explains how risk is measured and how the data-generating world was validated.

### 05 · GA search
Pedagogical mini-GA and simplex visualization. Demo trajectories are clearly separated from precomputed thesis results.

### 06 · Experiment pipeline
Contains two views:

1. **Thesis GA Architecture**
   - implemented search architecture
   - fitness, freeze, gate and configuration

2. **Evidence Pipeline**
   - Stage 1: Initial discovery
   - Stage 2: Frozen confirmation I
   - Stage 3: Expanded rediscovery
   - Stage 4: Frozen validation II
   - Stage 5: External evidence + abstention audit

Stage 5 is the canonical location for the external evidence story.

### 07 · Conclusions
Synthesizes bounded claims, contributions and limitations.

### 08 · Technical drill-down
Backup evidence for committee questions:
- candidate-level results
- fixed-weight validation
- bootstrap intervals
- evidence taxonomy
- external evidence details

## Scientific architecture

```text
read-only research archives / exported results
                │
                ▼
        curated CSV evidence
                │
                ▼
       data/raw + data/processed
                │
                ▼
        Streamlit defense app
                │
     ┌──────────┴──────────┐
     │                     │
 pedagogical demo      thesis evidence
     │                     │
 live Python           precomputed only
```

## Change discipline
Audience-facing changes must be made in the renderer actually called by `streamlit_app.py`. Do not create alternate implementations of the same defense layer.

Deployment-facing changes must advance the build identifier in `src/app_meta.py`.
