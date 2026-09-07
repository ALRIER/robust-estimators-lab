"""Accessible presenter cues for Layer 2 · Data-generating world.

These notes are deliberately low-density: one visual anchor and one short idea
per line, matching the emergency-cue style used in Layer 1.
"""

DATA_WORLD_PRESENTER_NOTES = {
    "data_world_why_simulation": (
        "Layer 2 · Why simulation?",
        "Known-truth simulation logic",
        [
            "PROBLEM|To measure estimator error, I need to know the truth.",
            "REAL DATA|The true population mean is hidden.",
            "SIMULATION|The target is known before scoring.",
            "TARGET|θ(F) = μF = E[X].",
            "BRIDGE|Known truth → repeated samples → measurable risk.",
            "KEY IDEA|Simulation measures error. It does not replace real data.",
        ],
        "Next, I define one complete statistical regime.",
    ),
    "data_world_regime": (
        "Layer 2 · Build a regime",
        "Regime definition and structural coverage",
        [
            "REGIME|One complete statistical environment.",
            "INGREDIENTS|F₀ family · γ rate · c scale · m mechanism · n sample size.",
            "TARGET|The population mean stays fixed.",
            "DISTRIBUTION|Clean baseline + designed contamination.",
            "FAMILIES|Six families create different shapes and tails.",
            "COVERAGE|6 families · 5 sample sizes · 576 profiles/family · 2,880 regimes/family.",
            "LOGIC|Change regime → change risk → ranking may change.",
            "KEY IDEA|Estimator performance is conditional, not universal.",
        ],
        "Next, I show why this simulated world can be trusted.",
    ),
    "data_world_validity": (
        "Layer 2 · Trust the simulator",
        "Simulator certification summary",
        [
            "PURPOSE|Validate the simulator before interpreting GA evidence.",
            "SUMMARY|125 conditions · 0 failures · 29 warnings · max mean error 0.976%.",
            "CHECK 1|Moment fidelity: recover the intended mean.",
            "CHECK 2|Contamination fidelity: generate the intended stress.",
            "CHECK 3|Theory recovery: known statistical patterns reappear.",
            "CHECK 4|Empirical anchoring: synthetic structure remains realistic.",
            "FAIRNESS|Same sample path · fixed seeds · logged regimes.",
            "WARNINGS|Warnings are diagnostic cases, not failures.",
            "KEY IDEA|Simulator validation is independent of the GA.",
        ],
        "Next, I show one generated sample in the Simulation Lab.",
    ),
}
