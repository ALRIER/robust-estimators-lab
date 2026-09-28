# Data manifest — current dashboard evidence

All thesis-result values displayed by the app come from bundled exported files. The dashboard does not infer missing research results.

## Pedagogical simulation
No research CSV is required.

- `src/synthetic_data.py`
- `src/estimators.py`
- `src/mini_ga.py`

These generate teaching output only.

## Discovery / expanded rediscovery
### Processed
`data/processed/winners_all.csv`

Used for candidate/result inspection and the 26-component weight vectors.

### Raw discovery exports
- `data/raw/discovery/combined_final_regime_results_all_rows.csv`
- `data/raw/discovery/ga_winner_candidates_for_q1.csv`
- `data/raw/discovery/winner_summaries/.../`

Do not interpret a discovery pass as fixed-weight confirmation.

## Frozen validation
- `data/raw/validation/final_decision_table.csv`
- `data/raw/validation/seed_level_expanded_gate.csv`
- `data/raw/validation/bootstrap_ci.csv`
- `data/raw/validation/selected_regimes.csv`

These support frozen candidate decisions, seed-level gate behavior and bootstrap evidence.

## Evidence taxonomy
- `data/raw/evidence/evidence_taxonomy_all_candidates.csv`
- `data/raw/evidence/evidence_grade_by_family.csv`
- `data/raw/evidence/validated_specialists.csv`

These define bounded evidence labels and the validated-specialist summaries.

## Dirichlet abstention audit
- `data/raw/dirichlet/abstain_audit_results.csv`
- `data/raw/dirichlet/abstain_audit_summary_by_regime.csv`
- `data/raw/dirichlet/dirichlet_signal_regime_modes.csv`

This audit challenges benchmark-retained synthetic regimes with random valid simplex mixtures. It is not a new GA discovery stage.

## External real-world evidence
The summarized external-evidence facts shown in Stage 5 were validated against the archived external-battery result package used for the thesis. The compact public repository currently carries the presentation summaries rather than the full external-battery tables.

Canonical Stage 5 facts:
- 264 requested public targets
- 228 loaded sources
- 120 evaluated dataset IDs
- 43 eligible parent datasets
- 26 / 43 parents with corrected signal
- 255 corrected confirmations
- abstention audit: 34 regime-mode rows, 23 no-random-pass, 11 signal rows

Breadth and depth must remain distinct:
- parent datasets = breadth
- corrected repeated confirmations = depth

## Processed files
`scripts/build_processed_data.py` rebuilds the processed discovery tables.

Never hand-edit scientific result tables to make the dashboard fit a narrative.
