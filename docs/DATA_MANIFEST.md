# Data manifest

All dashboard-ready raw inputs live in `data/raw/`. Their original sources are preserved in `research_reference/source_archives/GA_Results.zip`.

## Layer 1 — live teaching simulation
No CSV required. `src/synthetic_data.py` generates samples. `src/estimators.py` computes teaching estimators.

## Layer 2 — GA search
### DEMO MODE
No research CSV required. `src/mini_ga.py` owns the lightweight pedagogical GA.

### THESIS RESULTS context
`data/processed/winners_all.csv`
- final 26 weights (`w_*`)
- regime metadata
- source seed
- discovery gate pass
- final selected type
- GA and benchmark metrics

Do **not** use this table to fabricate generational histories.

## Layer 3 — thesis results
### Primary
`data/processed/winners_all.csv`
Built from the 12 per-family winner summaries under `data/raw/discovery/winner_summaries/`.

Important fields:
- distribution
- specialist_regime_id
- regime_key / condition_summary
- specialist_seed / source seed context
- gate_pass
- final_selected_type
- final_selected_estimator
- ga_robust_q95_mse / ga_robust_mean_mse
- best_benchmark_q95_estimator / best_benchmark_mean_estimator
- ga_rel_improvement_q95 / ga_rel_improvement_mean
- 26 `w_*` fields

### Cross-family index
`data/raw/discovery/combined_final_regime_results_all_rows.csv`
Use for compact regime/seed filtering and status overview.

### Candidate index
`data/raw/discovery/ga_winner_candidates_for_q1.csv`
Use for discovery-stage GA candidate examples only; do not label all rows as fixed-weight validated.

## Layer 4 — validation pipeline
### Final fixed-weight decisions
`data/raw/validation/final_decision_table.csv`
Use for validation-level final decision cards.

### Seed-level gate
`data/raw/validation/seed_level_expanded_gate.csv`
Use for per-validation-seed GA vs best benchmark metrics and expanded gate pass.

### Bootstrap confidence intervals
`data/raw/validation/bootstrap_ci.csv`
Use for CI whiskers and `ci_confirmed` status.

### Evidence taxonomy
`data/raw/evidence/evidence_taxonomy_all_candidates.csv`
Use for evidence grade, interpretive note and stage-aligned gain summaries.

`data/raw/evidence/validated_specialists.csv`
Use for the concise validated-specialist summary. This file currently contains the strongest fixed-weight-confirmed subset according to the source taxonomy.

### Dirichlet / abstain audit
`data/raw/dirichlet/abstain_audit_results.csv`
Use as optional final sanity/audit panel.

`data/raw/dirichlet/abstain_audit_summary_by_regime.csv`
Use for compact regime-level audit overview.

## Optional / later only
Real-world battery results are preserved in the full GA results archive but are intentionally not part of the one-week MVP unless time remains.

## Processed files
Run:
```bash
python scripts/build_processed_data.py
```
Outputs include:
- `data/processed/winners_all.csv`
- `data/processed/dashboard_cases.csv`
- `data/processed/data_health.json`

Never hand-edit processed files; regenerate them.
