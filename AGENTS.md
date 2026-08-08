# AGENTS.md — non-negotiable project rules

## Mission
Build a polished local Dash/Plotly dashboard for a thesis defense and 10–15 minute teaching video. Target completion: **7 calendar days**. Prioritize a reliable MVP over feature creep.

## Scientific source of truth
- The original R code and result archives under `research_reference/source_archives/` are **read-only source material**.
- Never edit, overwrite, reformat, or silently “correct” those archives.
- Never rerun the full thesis GA unless the user explicitly requests it. It takes days and is outside the dashboard scope.
- Dashboard thesis claims must come from curated CSVs under `data/raw/` or files extracted from the source archives.
- If a needed quantity is absent, display `Not available in exported results` rather than infer or fabricate it.

## Critical scientific invariants
1. The expanded estimator space contains **26 components**, in this order:
   `mean, median, trimmed20, harmonic, geometric, mode_hsm, mode_parzen, trimean, huber, biweight, winsorized_0.05, winsorized_0.1, winsorized_0.2, mom_k5, mom_k10, mom_k20, catoni_a0.05, catoni_a0.1, catoni_a0.2, catoni_a0.35, catoni_a0.5, huber_k0.75, huber_k1, huber_k1.345, huber_k1.75, huber_k2`.
2. GA mixture weights must be non-negative and sum to 1, up to floating-point tolerance.
3. A 3D terrain is **not the full simplex**. Always label it: `Low-dimensional slice of the full 26-dimensional simplex`.
4. Do not claim a real generational trajectory unless an exported convergence/history file supports it. Current curated thesis results contain final weights/results, not full population histories.
5. Layer 2 has two visually distinct modes:
   - `DEMO MODE`: live lightweight Python mini-GA, pedagogical only.
   - `THESIS RESULTS`: precomputed R outputs only.
6. Fixed-weight validation means weights remain locked; no retraining in validation views.
7. A benchmark must remain the winner whenever the source CSV says the GA gate failed.
8. Preserve distinctions among discovery result, profile/global audit, fixed-weight validation, evidence grade, and Dirichlet/abstain audit.

## UX / presentation rules
- English UI, because the thesis defense/video is in English.
- Match `design/mockups/` closely: light canvas, charcoal text, thin borders, restrained orange-red accent, compact academic cards.
- The app must work fully **offline/local** for defense reliability.
- Main defense views must load in <2 seconds after preprocessing on a normal laptop.
- Do not use external web fonts, API keys, paid services, remote databases, telemetry, or runtime internet calls.
- Each layer must have a `Presentation mode` with reduced controls and larger text.
- Include a small persistent badge identifying `DEMO MODE` versus `THESIS RESULTS`.
- Every 3D simplex plot must include the low-dimensional-slice disclaimer in the figure or directly beneath it.

## Technical stack
- Python
- Dash
- Plotly
- pandas / NumPy / SciPy
- dash-bootstrap-components only for layout primitives if useful
- plain CSS under `assets/`
- pytest for tests

## Coding rules
- Keep callbacks small; business logic belongs in `src/`.
- No duplicated data-loading logic across pages.
- Use `pathlib.Path`, never hard-coded absolute paths.
- Seed all pedagogical simulations explicitly.
- Add tests for weight validity, data contracts, and evidence mapping before visual polish.
- Prefer cached/preprocessed tables under `data/processed/` over repeated expensive CSV parsing.
- Keep page modules under ~500 lines; split components when they grow.

## Git / change discipline
- Work in small milestones corresponding to `prompts/`.
- Before finishing a milestone run:
  `python scripts/build_processed_data.py`
  `pytest -q`
- Do not delete TODOs tied to later milestones merely to make checks pass.

## Definition of done
See `docs/ACCEPTANCE_CRITERIA.md`. A visually impressive feature is not done if it violates the scientific guardrails.
