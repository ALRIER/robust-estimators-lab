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
            "MOMENT FIDELITY|• WHAT WAS DONE: For each test condition, we generated a very large sample, calculated its average, and compared that average with the mean we expected from the distribution. • WHY IT WAS DONE: If the simulator does not reproduce the correct mean, every later error calculation would start from the wrong reference point. • WHAT WE OBTAINED: The maximum relative mean error was 0.976%, below the 1% hard threshold used by the certification layer.",
            "CONTAMINATION FIDELITY|• WHAT WAS DONE: We created the contaminated sample exactly as specified, then checked how many observations were affected, where the unusual values appeared, and how far they were from the centre of the data. • WHY IT WAS DONE: If a condition says 10% upper-tail contamination, the generated sample must actually look like a 10% upper-tail contamination case before we compare estimators. • WHAT WE OBTAINED: The certification battery reported no hard failures overall. Deviations associated with dilution, masking or scale effects were retained transparently as diagnostic warnings rather than silently discarded.",
            "THEORY RECOVERY|• WHAT WAS DONE: We ran simple cases where statistics already tells us what should happen. For example, with clean Normal data, we checked that the sample mean performs better than the median in MSE. • WHY IT WAS DONE: Before trusting new findings, the simulator should first reproduce results that are already well understood. • WHAT WE OBTAINED: The complete certification battery produced 0 hard failures, so the theory-recovery checks did not identify a failure severe enough to invalidate the simulated world.",
            "EMPIRICAL ANCHORING|• WHAT WAS DONE: We looked at public real datasets and compared their basic shapes and unusual-value patterns with the kinds of situations created in the simulator. • WHY IT WAS DONE: This helps check that the simulated cases resemble patterns that can actually appear in real data, while still keeping simulation as the place where the true mean is known. • WHAT WE OBTAINED: The external datasets served as calibration anchors, not training targets or known-truth validation. Any anchoring mismatch was retained as a diagnostic warning; the overall certification still recorded 0 hard failures.",
            "FAIRNESS & REPRODUCIBILITY|• WHAT WAS DONE: In each repetition, every estimator was tested on the exact same generated sample. We also fixed the random seeds and saved the settings used for each condition. • WHY IT WAS DONE: A fair comparison requires every estimator to face the same data, and the experiment should be possible to repeat later in the same way. • WHAT WE OBTAINED: The validation conditions can be reproduced and audited from the recorded regime and seed structure.",
            "WARNINGS|29 warnings are not 29 failed validation conditions. They are retained diagnostic cases that can reflect natural 3-MAD flags, dilution, masking, scale effects or empirical-anchoring mismatch.",
            "KEY IDEA|The simulator is certified independently of the GA: first validate the world, then measure estimator risk, and only after that interpret search results.",
        ],
        "Next, I show one generated sample in the Simulation Lab.",
    ),}
