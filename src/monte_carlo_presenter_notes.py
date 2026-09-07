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
        "Next: show the four validation checks and their main results.",
    ),
    "monte_carlo_validation_stages": (
        "Layer 4 · Validation stages",
        "Simulator certification battery",
        [
            "1 · MOMENTS|Generate very large synthetic populations for representative grid conditions. Compute the empirical mean and compare it with the analytic population mean using relative mean error.",
            "↳ RESULT|Maximum mean error = 0.976%, below the 1% hard threshold.",
            "2 · CONTAMINATION|After contamination is injected, compute the realised contamination rate, verify its direction, and check severity using MAD-based distance against the regime label.",
            "↳ RESULT|The realised rate, direction and MAD-based severity were explicitly checked after injection before those regimes entered Monte Carlo evaluation.",
            "3 · THEORY|Run clean Normal scenarios through the same scoring engine and compare Monte Carlo MSE for the sample mean and the median as a known-theory sanity check.",
            "↳ RESULT|The expected ordering was recovered: under clean Normal data, the sample mean beats the median in MSE.",
            "4 · EMPIRICAL|Compute shape diagnostics on five public datasets and compare them with matched areas of the synthetic grid. Real data are used as structural references, not as known population truth.",
            "↳ RESULT|The five datasets provide empirical anchoring for relevant shapes; this stage is calibration, not known-θ validation.",
            "29 WARNINGS|These were diagnostic flags retained in the validation tables/dataframes, not code errors and not failed validation conditions. They marked explainable cases such as expected sampling variation, contamination dilution or masking, and empirical-anchoring mismatch. They were kept visible for transparency instead of being silently removed.",
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
