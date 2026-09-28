# Robust Estimators Lab

Public Streamlit dashboard for the MSc thesis defense.

## Canonical runtime

- Repository: `ALRIER/robust-estimators-lab`
- Canonical branch: `main`
- Canonical Streamlit entrypoint: `streamlit_app.py`
- Compatibility shim: `app.py` imports the canonical entrypoint only
- Public app: `https://robust-estimators-lab.streamlit.app/`

The dashboard uses bundled precomputed research outputs. It does not rerun the thesis GA at runtime.

## Current application structure

`streamlit_app.py` owns navigation and the live defense flow.

Core live modules are under `src/`, including:

- `research_logic.py`
- `data_world.py`
- `defense_mode.py`
- `experiment_pipeline.py`
- `results_journey_polished.py`
- `thesis_ga_architecture.py`
- `data_loader.py`
- pedagogical GA/simplex modules

Scientific result tables live under `data/raw/` and `data/processed/`.

## Deployment

Streamlit Community Cloud must be configured as:

- repo: `ALRIER/robust-estimators-lab`
- branch: `main`
- main file path: `streamlit_app.py`

See `docs/DEPLOYMENT.md` and `docs/REPOSITORY_HEALTH.md`.

## Local launch

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The sidebar displays a build identifier. Use it to verify that the public deployment is running the same revision as the repository.
