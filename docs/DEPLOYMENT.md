# Deployment

## Canonical Streamlit Cloud configuration

The public dashboard must be deployed from exactly:

- Repository: `ALRIER/robust-estimators-lab`
- Branch: `main`
- Main file path: `streamlit_app.py`

Public URL:

- `https://robust-estimators-lab.streamlit.app/`

## Important

`app.py` is only a compatibility shim. It contains no independent application logic and should not be selected as the canonical Cloud entrypoint.

## Build verification

The sidebar displays a visible build identifier from `src/app_meta.py`.

When a repository change is deployed successfully:

1. the build identifier in the public app must match the value committed on `main`;
2. the expected visual change must appear;
3. if the build identifier is old, the problem is deployment routing or deployment failure, not the renderer code.

## Stage 5 route

The external evidence view is located at:

`Layer 6 → Experiment pipeline → Evidence Pipeline → 5. External evidence + audit`

Its current live renderer is called from `streamlit_app.py` and uses `result_figure(3)` from `src/results_journey_polished.py`.

## Scientific runtime

The hosted app uses bundled CSV/result files. It does not rerun the full thesis GA.
