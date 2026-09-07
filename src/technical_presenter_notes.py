"""Accessible presenter cues for Layer 9 · Technical drill-down."""

TECHNICAL_PRESENTER_NOTES = {
    "appendix_A": (
        "Appendix A · GA mechanics",
        "Technical backup",
        [
            "INDIVIDUAL|w = one estimator recipe.",
            "C MATRIX|Fixed Monte Carlo outputs from the base estimators.",
            "EVALUATE|Every new w → Cw → loss → fitness.",
            "EVOLVE|Selection → crossover → mutation → new w → evaluate again.",
            "SIMPLEX|Weights are non-negative and sum to 1.",
            "WARM START|A previous winner may enter again, but gets no bonus.",
            "CLAIM|Fitness searches. Frozen validation decides.",
        ],
        "Open Metrics & Gate only if the committee asks how acceptance is decided.",
    ),
    "appendix_B": (
        "Appendix B · Metrics & gate",
        "Technical backup",
        [
            "TARGET|θ(F) = E[X].",
            "MSE|Average squared error.",
            "q95|Upper-tail squared error — difficult cases.",
            "GAIN|Positive gain = candidate has lower risk.",
            "GATE|ΔMSE ≥ 0 AND Δq95 ≥ 0.",
            "CI|If the interval crosses zero, replacement is uncertain.",
            "BENCHMARK|Compare against the strongest admissible benchmark.",
        ],
        "Open Technical Results only if exact candidates or numbers are requested.",
    ),
    "appendix_C": (
        "Appendix C · Technical results",
        "Technical backup",
        [
            "FIRST FUNNEL|36 → 16 → 2 confirmed.",
            "EXPANDED|26 learnable → 12 discovery winners.",
            "TAXONOMY|25 → 2 transfer · 10 local · 7 near-gate · 6 controls.",
            "SPECIALISTS|FWVR011 / FWVR012 pass locked-unseen but fail original mode.",
            "REAL DATA|26/43 eligible parents show corrected specialist wins.",
            "DEPTH|255 subgroup wins remain after correcting for many tests.",
            "AUDIT|23/34 no random pass · 8/8 strongest controls pass.",
            "CLAIM|Narrow specialists — not universal winners.",
        ],
        "Answer the exact question and stop; do not replay the full Results section.",
    ),
    "appendix_D": (
        "Appendix D · Committee Q&A",
        "Technical backup",
        [
            "WHY GA?|Search many interpretable recipes across generations.",
            "WHY AI?|Evolution can generate and improve estimator mixtures, not only select one fixed estimator.",
            "WHY q95?|Average risk can hide difficult cases.",
            "WHY FREEZE?|Prevent adaptation to confirmation data.",
            "WHY RETAIN?|The framework is allowed to say: benchmark wins.",
            "REAL DATA?|Transfer evidence — not known population truth.",
            "NOVELTY?|Integrated AI search + interpretable estimator design + frozen claim control.",
            "LIMIT?|Known truth is simulation-based; strongest gains are narrow.",
            "MAIN CONTRIBUTION|A reusable AI search framework with evidence-controlled acceptance.",
        ],
        "Give the short answer first. Add detail only if the committee asks.",
    ),
}
