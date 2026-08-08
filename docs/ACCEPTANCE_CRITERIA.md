# Acceptance criteria

## Global
- App runs locally with no network requirement.
- Four layers/routes load without traceback.
- Visual style is recognizably aligned with `design/mockups/`.
- All thesis-result values come from data files.
- `DEMO MODE` and `THESIS RESULTS` are visually unmistakable.
- `pytest -q` passes.

## Layer 1
- User can choose distribution, contamination, contamination rate, outlier scale, and n.
- Regenerating the sample updates plots and estimator values.
- At minimum Mean, Median, Trimmed Mean, Huber and Biweight are visible.
- Contamination can visibly displace the mean relative to robust estimators in suitable settings.
- UI includes the teaching message that no estimator is uniformly best.

## Layer 2
- Mini-GA completes quickly on a laptop.
- Every individual is a valid convex weight vector.
- Playback exposes generation, best objective, diversity, and mutation rate.
- 3D surface has terrain/contours and a clear low-error basin.
- Figure explicitly says it is a low-dimensional simplex slice.
- Any population path shown as thesis-real must have an authentic history source; otherwise only demo path is shown.

## Layer 3
- Filters by family, regime and seed/context work.
- Top weights sum to approximately 1 when all 26 are included.
- GA win and benchmark-retained examples are both available.
- Gate pass/fail exactly matches source CSV.
- No discovery-stage candidate is mislabeled as fixed-weight validated.

## Layer 4
- Fixed-weight final decision is sourced from `final_decision_table.csv`.
- Bootstrap CI panel is sourced from `bootstrap_ci.csv`.
- Evidence grade is sourced from taxonomy table.
- Clear visual separation between original-regime and locked-unseen-similar validation modes.
- Optional Dirichlet/abstain panel, if included, uses source verdict fields.

## Defense safety
- A `Presentation mode` hides unnecessary controls.
- Key pages can be navigated with a single click.
- Backup screenshots exist under `exports/backup_screens/` before final freeze.
- No long computation occurs during the live defense except mini-GA demo, which must be deterministic and fast.
