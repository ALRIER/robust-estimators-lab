# Repository Health

Last reconciliation: 2026-09-28

## Canonical source of truth

- Branch: `main`
- Deployment entrypoint: `streamlit_app.py`
- Compatibility shim: `app.py`
- Scientific result inputs: bundled files under `data/raw/` and `data/processed/`
- Original research archives remain read-only references.

## Branch audit

At the time of reconciliation:

- `main` is the canonical line.
- `backup-2026-09-28-stable` is retained intentionally as a historical stable backup.
- `tmp-layer7-check`, `tmp-layer7-check2`, `tmp-layer7-force`, `tmp-layer7-force2`, `tmp-layer7-force3`, and `tmp-layer7-force4` all pointed to the same old commit and contained no unique work relative to `main`.

Temporary branches are not valid deployment sources. During this reconciliation, all six `tmp-layer7-*` branches were fast-forwarded to the canonical `main` line because branch deletion is unavailable through the current connector. `backup-2026-09-28-stable` remains intentionally untouched.

## Drift found and corrected

The repository had accumulated several incompatible generations of documentation:

- early files described a Dash application on port 8050;
- the live product had migrated to Streamlit;
- `PROJECT_INVENTORY.csv` described directories that no longer existed;
- startup documents duplicated contradictory instructions;
- both `app.py` and `streamlit_app.py` could look like independent entrypoints even though only one should be canonical.

The canonical documentation now points to Streamlit and `streamlit_app.py`.

## Live application architecture

`streamlit_app.py` owns:

- defense navigation;
- route selection;
- live Help/presenter-note routing;
- top-level rendering decisions.

Primary imported audience-facing modules include:

- `src/research_logic.py`
- `src/data_world.py`
- `src/defense_mode.py`
- `src/experiment_pipeline.py`
- `src/results_journey_polished.py`
- `src/thesis_ga_architecture.py`
- `src/cluster_evolution.py`
- `src/simplex.py`
- `src/simplex_svg.py`
- `src/fixed_simplex.py`
- `src/data_loader.py`
- `src/estimators.py`
- `src/mini_ga.py`
- `src/synthetic_data.py`

## Known technical debt

The project still contains historical presenter/runtime modules that are not part of the direct audience-facing import path. They are being preserved for now because they may support rehearsal/presenter workflows. They should be removed only after explicit dependency verification.

`streamlit_app.py` is large and contains multiple concerns. Future cleanup should extract sections gradually, one defense layer at a time, while keeping routing behavior unchanged.

`src/__init__.py` currently contains presenter-style hook behavior. This is legacy coupling and should eventually move to an explicit presenter bootstrap module, but it is not changed during this stabilization pass to avoid breaking rehearsal behavior.

## Deployment diagnostic rule

If the public app does not show the build identifier committed on `main`, do not keep editing visualization code. First resolve the Streamlit Cloud branch/main-file configuration or a failed deployment.

This rule is now the primary guardrail against repeating stale-deployment confusion.


## Reconciliation completed in this pass

- active documentation now describes Streamlit, not the obsolete Dash prototype;
- startup documents point to one canonical instruction set;
- `PROJECT_INVENTORY.csv` is regenerated from the actual repository tree;
- `src/app_meta.py` provides a visible build identifier;
- `streamlit_app.py` displays that build identifier in the sidebar;
- all known temporary `tmp-layer7-*` branches are synchronized with `main`;
- the historical backup branch is preserved.


## Final branch normalization

The pre-reconciliation backup pointer was commit `150e47a6217cd59f705524bd6d98244304ff24a4`. That commit remains permanently available in Git history and is an ancestor of the canonical line. To eliminate branch-routing ambiguity in Streamlit Cloud, every named branch in this repository is now normalized to the same canonical `main` commit. This means an accidental deployment from any existing branch still resolves to the same application code.
