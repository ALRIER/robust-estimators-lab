# AGENTS.md — non-negotiable project rules

## Mission
Maintain a polished Streamlit dashboard for the thesis defense and teaching/rehearsal workflow. Prefer reliability, scientific traceability, and a single canonical runtime over parallel implementations.

## Canonical application
- Framework: **Streamlit + Plotly**.
- Canonical branch: **main**.
- Canonical deployment entrypoint: **streamlit_app.py**.
- `app.py` is compatibility-only and must not contain independent application logic.
- Do not create a second live dashboard implementation or duplicate a defense layer in another runtime file.
- Audience-facing changes belong in the module actually imported by `streamlit_app.py`.

## Scientific source of truth
- Original research archives and exported result packages are read-only source material.
- Never rerun the full thesis GA unless the user explicitly requests it.
- Dashboard thesis claims must come from exported/curated result files.
- If a quantity is absent, display `Not available in exported results` instead of inferring it.

## Critical scientific invariants
1. The expanded estimator space contains 26 components in the documented order.
2. GA mixture weights are non-negative and sum to 1 up to floating-point tolerance.
3. Any low-dimensional simplex terrain must be labelled as a slice of the full 26-dimensional simplex.
4. Do not claim a real generational trajectory unless an exported history supports it.
5. Pedagogical/demo GA output must remain visibly distinct from thesis results.
6. Fixed-weight validation means weights remain locked.
7. A benchmark remains the winner whenever the exported gate says the GA failed.
8. Preserve distinctions among discovery, fixed-weight validation, evidence taxonomy, external evidence, and Dirichlet abstention audit.
9. External evidence breadth and depth must remain distinct: parent datasets are the independent breadth unit; repeated corrected confirmations are depth.

## Repository discipline
- Keep `main` as the single development/deployment line.
- Temporary branches must never become alternate sources of truth.
- Keep one explicit backup branch when needed; temporary branches should be removed or fast-forwarded once reconciled.
- Before changing a defense view, identify its exact route in `streamlit_app.py` and the renderer it calls.
- Avoid duplicate presenter-note sources. The live Help source must be documented.
- Update `docs/REPOSITORY_HEALTH.md` when architecture or deployment routing changes.
- Keep `PROJECT_INVENTORY.csv` current.

## Deployment discipline
For Streamlit Community Cloud use:
- repository: `ALRIER/robust-estimators-lab`
- branch: `main`
- main file: `streamlit_app.py`

Every deployment-facing change must also update the visible build identifier in `src/app_meta.py`. This makes stale deployments immediately detectable.

## Definition of done
A change is complete only when:
1. the scientific claim is supported by exported evidence;
2. the correct live renderer was changed;
3. the canonical entrypoint imports that renderer;
4. the build identifier was advanced;
5. no duplicate live implementation was introduced.
