# Acceptance criteria — canonical Streamlit app

## Global
- App runs from `streamlit run streamlit_app.py`.
- All nine defense sections load without traceback.
- Sidebar shows the current build identifier.
- Thesis-result values come only from bundled research outputs.
- Demo output and thesis evidence are visibly distinct.
- No full thesis GA is executed at runtime.
- Main defense content is readable on a presentation screen.

## 01 · Research logic
- Fixed target `E[X]` is clear.
- Regime dependence is explained without implying a universal winner.
- Composite estimator and simplex constraints are interpretable.

## 02 · Data-generating world
- Distribution families and contamination structures are visible.
- Validation coverage is clearly separated from research-result claims.

## 03 · Simulation lab
- Controls update a deterministic pedagogical sample.
- Mean and robust estimators visibly respond to contamination.
- UI states that the simulation is pedagogical.

## 04 · Monte Carlo engine
- Monte Carlo measurement logic is explained.
- Data-generating-world validation can be inspected independently.

## 05 · GA search
- Mini-GA runs quickly and deterministically.
- Every candidate is a valid convex weight vector.
- Any simplex slice is explicitly labelled as low-dimensional.
- No fabricated thesis trajectory is shown.

## 06 · Experiment pipeline
- Five stages are navigable.
- Discovery, frozen confirmation, rediscovery, frozen validation and external evidence remain distinct.
- Stage 3 includes expanded rediscovery results.
- Stage 4 includes strict frozen-validation results.
- Stage 5 contains one coherent external-evidence + abstention-audit story.
- External breadth and depth are not conflated.

## 07 · Conclusions
- Claims remain conditional and benchmark-gated.
- Limits are visible.

## 08 · Technical drill-down
- Candidate-level result inspection works.
- Fixed-weight decisions match exported files.
- Bootstrap evidence and evidence taxonomy are source-derived.
- External evidence detail is available as backup.

## Defense safety
- No long runtime computation except the small pedagogical GA.
- Navigation requires at most one click per main section.
- Build ID in the sidebar makes stale deployment immediately detectable.
