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
            "PURPOSE|Validate the simulated world before interpreting estimator performance or any GA evidence.",
            "CERTIFICATION SUMMARY|125 validation conditions · 0 hard failures · 29 explainable warnings · maximum relative mean error 0.976%.",
            "MOMENT FIDELITY|• WHAT WAS DONE: Large generated populations were compared with the analytic population mean for the regime. • WHY IT WAS DONE: Every downstream squared-error calculation depends on the simulator being centred on the correct target; a wrong population mean would shift the entire error surface. • WHAT WE OBTAINED: The maximum relative mean error was 0.976%, below the 1% hard threshold used by the certification layer.",
            "CONTAMINATION FIDELITY|• WHAT WAS DONE: After contamination was injected, the realised contamination rate, contamination direction and MAD-based distance were checked against the regime definition. • WHY IT WAS DONE: A regime labelled as a given contamination rate or stress mechanism must actually contain that stress; otherwise estimator comparisons would be performed under a mislabelled data-generating condition. • WHAT WE OBTAINED: The certification battery reported no hard failures overall. Deviations associated with dilution, masking or scale effects were retained transparently as diagnostic warnings rather than silently discarded.",
            "THEORY RECOVERY|• WHAT WAS DONE: The simulator was challenged with known statistical sanity checks before any new GA conclusion was interpreted; a key example is the expected clean-Normal ordering in which the sample mean should outperform the median in MSE. • WHY IT WAS DONE: A simulation and scoring pipeline that cannot reproduce well-established statistical behaviour should not be trusted to support a new estimator claim. • WHAT WE OBTAINED: The complete certification battery produced 0 hard failures, so the theory-recovery checks did not identify a failure severe enough to invalidate the simulated world.",
            "EMPIRICAL ANCHORING|• WHAT WAS DONE: Public real-data diagnostics were used as structural anchors for the synthetic regimes, comparing relevant empirical shapes and stress patterns with the simulation design. • WHY IT WAS DONE: This checks that the synthetic world remains empirically relevant without treating real data as if the true population mean were known. • WHAT WE OBTAINED: The external datasets served as calibration anchors, not training targets or known-truth validation. Any anchoring mismatch was retained as a diagnostic warning; the overall certification still recorded 0 hard failures.",
            "FAIRNESS & REPRODUCIBILITY|• WHAT WAS DONE: Within each Monte Carlo replicate, estimators see the same sample path; seeds are fixed and regimes are logged. • WHY IT WAS DONE: Comparisons should differ because of estimator behaviour, not because methods saw different random samples or unreproducible conditions. • WHAT WE OBTAINED: The validation conditions can be reproduced and audited from the recorded regime and seed structure.",
            "WARNINGS|29 warnings are not 29 failed validation conditions. They are retained diagnostic cases that can reflect natural 3-MAD flags, dilution, masking, scale effects or empirical-anchoring mismatch.",
            "KEY IDEA|The simulator is certified independently of the GA: first validate the world, then measure estimator risk, and only after that interpret search results.",
        ],
        "Next, I show one generated sample in the Simulation Lab.",
    ),}
