# Stabilization board

The original seven-day build sprint is complete. This file now tracks repository stabilization priorities.

| Priority | Task | Completion condition |
|---|---|---|
| P0 | Canonicalize deployment | main + streamlit_app.py documented everywhere |
| P0 | Visible build ID | public app shows current `src/app_meta.py` BUILD_ID |
| P0 | Reconcile temporary branches | temporary branches point to canonical main or are deleted |
| P1 | Reconcile documentation | no Dash/4-layer instructions remain in active docs |
| P1 | Keep scientific sources immutable | no result archive modified |
| P1 | Reduce duplicated live logic | each defense view has one canonical renderer |
| P2 | Gradually split `streamlit_app.py` | refactor layer-by-layer without changing behavior |
| P2 | Remove verified dead modules | only after import/dependency audit |
