"""Accessible presenter cues for Layer 4 · Monte Carlo measurement and validation."""

MONTE_CARLO_PRESENTER_NOTES = {
    "monte_carlo_measurement": (
        "Layer 4 · Measure repeated risk",
        "Canonical Monte Carlo measurement engine",
        [
            "5 STEPS|Choose regime → Generate sample → Apply estimators → Compare with θ → Repeat.",
            "SAME SAMPLE|Every estimator sees the same sample inside each replicate.",
            "KNOWN TARGET|Every estimate is compared with the same population mean θ.",
            "LOSS|Squared error = (Tⱼ(xʳ) − θ)².",
            "MSE|Average squared error across repeated samples.",
            "q95|The difficult upper-tail squared error.",
            "KEY IDEA|Repeat the same fair comparison many times to measure risk.",
        ],
        "Next: explain why the simulator must be validated before the GA is trusted.",
    ),
    "monte_carlo_why_validate": (
        "Layer 4 · Why validate first?",
        "Independent simulator validation",
        [
            "RISK|A strong GA can still optimize the wrong simulated world.",
            "INDEPENDENT FIRST|Validate the simulator before interpreting GA evidence.",
            "ORDER|Build world → Validate world → Measure risk → Run search.",
            "AVOID|A GA winner is not proof that the simulator is correct.",
            "KEY IDEA|The GA is not allowed to validate its own environment.",
        ],
        "Next: show the four validation checks and the headline numbers.",
    ),
    "monte_carlo_validation_stages": (
        "Layer 4 · Validation stages",
        "Simulator certification battery",
        [
            "SUMMARY|125 conditions · 0 hard failures · 29 warnings · max mean error 0.976%.",
            "CHECK 1 · MOMENTS|Mean error stayed below the 1% hard threshold; maximum was 0.976%.",
            "CHECK 2 · CONTAMINATION|Check realised contamination rate and MAD-based severity.",
            "CHECK 3 · THEORY|Clean Normal data recover the expected result: mean beats median in MSE.",
            "CHECK 4 · EMPIRICAL|Five public datasets anchor realistic shapes; this is calibration, not known-truth validation.",
            "WARNINGS|29 warnings are diagnostic cases, not failures. Hard failures = 0.",
            "ORDER|Population truth → contamination design → theory sanity → empirical relevance.",
            "KEY IDEA|Trust is built before search begins.",
        ],
        "Next: show the safeguards that keep every comparison fair and auditable.",
    ),
    "monte_carlo_fairness": (
        "Layer 4 · Fairness & order of trust",
        "Reproducibility and anti-leakage safeguards",
        [
            "TARGET FIRST|θ is defined before any estimator or GA candidate is evaluated.",
            "SAME SAMPLE|All estimators receive the same sample inside each replicate.",
            "REPRODUCIBLE|Seeds are fixed and regimes are logged.",
            "TRANSPARENT|Warnings stay visible instead of being silently removed.",
            "6 STAGES|Build → Validate → Measure → Search → Freeze → Gate.",
            "JOBS|Simulator: world credible · Monte Carlo: risk · GA: opportunity · Frozen validation: replacement.",
            "KEY IDEA|No stage is allowed to certify itself.",
        ],
        "Next: move from measured risk to the GA search.",
    ),
}
