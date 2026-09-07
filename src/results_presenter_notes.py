"""Ultra-concise presenter cues for Layer 7 · Results journey."""

RESULTS_PRESENTER_NOTES = {
    "results_stage_0": (
        "Layer 7 · Discovery + Frozen I",
        "Fixed thesis results",
        [
            "FUNNEL|36 regimes → 16 discovery wins → 2 frozen confirmations.",
            "CV-019|Lognormal · +16.3% q95 MSE · 8/8 seeds.",
            "CV-010|Lognormal · +2.2% q95 MSE · 8/8 seeds.",
            "MEANING|Freezing reduced 16 search signals to 2 defensible candidates.",
        ],
        "Next: reopen the search with a stronger 26-estimator basis.",
    ),
    "results_stage_1": (
        "Layer 7 · Expanded rediscovery",
        "Fixed thesis results",
        [
            "REOPEN|10 learnable → 26 learnable · HPF2 80% → 90%.",
            "RESULT|12 discovery winners across 5 families.",
            "COUNTS|Normal 1 · Lognormal 2 · Weibull 2 · Inv. Gaussian 4 · Ex-Gaussian 0 · Ex-Wald 3.",
            "WARM STARTS|CV-019 + CV-010 compete again. No automatic win.",
        ],
        "Next: freeze the expanded candidates and test what evidence survives.",
    ),
    "results_stage_2": (
        "Layer 7 · Strict validation",
        "Fixed thesis results",
        [
            "FREEZE AGAIN|The expanded candidates are locked before strict validation.",
            "TAXONOMY|25 candidates → 2 transfer · 10 local · 7 near-gate · 6 controls.",
            "TRANSFER · 2|Pass in related locked-unseen regimes.",
            "LOCAL · 10|Discovery signal only; frozen validation does not confirm transfer.",
            "NEAR-GATE · 7|Close to the gate, but not enough to replace the benchmark.",
            "CONTROLS · 6|Expected failures; the benchmark was correctly retained.",
            "FWVR011|Locked-unseen: +2.79% mean / +2.72% q95. Original regime: fail.",
            "FWVR012|Locked-unseen: +3.18% mean / +1.25% q95. Original regime: fail.",
            "MEANING|Two narrow Weibull transfer specialists — not family-wide winners.",
        ],
        "Next: test the frozen specialists on external real-world data.",
    ),
    "results_stage_3": (
        "Layer 7 · Real-world battery",
        "Fixed thesis results",
        [
            "FUNNEL|264 requested → 228 loaded → 120 evaluated → 43 eligible parents.",
            "BREADTH|26/43 parents had at least one corrected specialist win.",
            "MATCHED PROFILES|Test the specialist only where the real-data subgroup resembles its validated profile.",
            "DEPTH|255 subgroup wins remained after correcting for many simultaneous tests.",
            "CAUTION|255 subgroup results are not 255 independent datasets.",
            "MEANING|External transfer support — not known-θ population proof.",
        ],
        "Next: audit whether benchmark retention could simply reflect weak GA search.",
    ),
    "results_stage_4": (
        "Layer 7 · Dirichlet audit",
        "Fixed thesis results",
        [
            "QUESTION|Can random valid mixtures beat benchmark-retained cells?",
            "AUDIT|4,000 random simplex vectors × 8 seeds.",
            "RESULT|23/34 no random pass · 11/34 some signal.",
            "CONTROL|8/8 strongest positive controls passed.",
            "MEANING|Abstention was often meaningful, not simply weak GA search.",
        ],
        "Next: conclude with the smaller, evidence-controlled claim.",
    ),
}
