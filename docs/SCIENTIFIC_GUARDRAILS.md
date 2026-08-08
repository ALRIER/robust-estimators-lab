# Scientific guardrails

## 1. Demo vs evidence
The dashboard is allowed to *teach* using new lightweight simulations, but those simulations must never be described as thesis outcomes.

Use permanent badges:
- `DEMO MODE — pedagogical simulation`
- `THESIS RESULTS — precomputed research output`

## 2. The 26-dimensional simplex
The research GA searches convex weights over 26 estimators. Any triangle or geological 3D view is a low-dimensional slice/projection.

Required text near every simplex visualization:
> Low-dimensional slice of the full 26-dimensional simplex; shown for visualization only.

Recommended slice rule for real winner inspection:
- choose the 3 largest weights
- keep remaining 23 weights fixed or aggregate their total mass explicitly
- vary only the selected coordinates while preserving non-negativity and total mass
- state which rule is used in the UI

## 3. Geological landscape
For a pedagogical mini-GA, terrain height may be computed live from a real objective on the demo sample.

For thesis results, do not synthesize a fake terrain and imply it was evaluated by the original GA. If a local landscape is generated post hoc, label it:
`Post-hoc local sensitivity surface around a fixed thesis solution`.

## 4. Search history
The R core contains convergence/history logic, but the curated current results archive does not export full convergence history files. Therefore:
- never reconstruct a “real” population path from final weights
- use the Python mini-GA for animated evolution
- if authentic convergence files are later exported, add them through a new data contract

## 5. Gate interpretation
A discovery `gate_pass=True` is not identical to later fixed-weight confirmation. Show stages separately.

## 6. Validation
Fixed-weight validation uses locked weights. Dashboard interactions may filter or visualize validation results but must not re-optimize the weights.

## 7. Metrics
Avoid displaying relative gain without its direction and metric. Prefer labels such as:
- `Relative gain in mean MSE`
- `Relative gain in q95(MSE)`

Lower MSE/q95(MSE) is better. Positive gain fields in the research tables should be interpreted according to the originating table definition; do not silently reverse signs.

## 8. Missing information
If a source table lacks a field, display `Not exported` or omit the element. Do not derive scientific claims from UI convenience.
