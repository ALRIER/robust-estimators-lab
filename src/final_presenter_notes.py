"""Presenter-note entries for the final Layers 7–9.

The values follow the same tuple structure used by streamlit_app.PRESENTER_NOTES:
(title, source, talking_points, transition).
"""

FINAL_PRESENTER_NOTES = {
    "results_stage_0": (
        "Layer 7 · Discovery + Frozen I",
        "Fixed thesis results",
        [
            "Read the funnel from 36 controlled regimes to 16 discovery wins to 2 frozen confirmations.",
            "Discovery is an opportunity signal, not a final result.",
            "CV-019 and CV-010 are the two Lognormal signals that survive 8/8 validation seeds.",
            "Do not call all 16 discovery wins confirmed results.",
        ],
        "Move to expanded rediscovery: what changes when the search basis gets stronger?",
    ),
    "results_stage_1": (
        "Layer 7 · Expanded rediscovery",
        "Fixed thesis results",
        [
            "Cycle 1 used 10 learnable components; Cycle 2 reopened the search with 26.",
            "HPF2 exposure increased from 80% to 90%.",
            "Cycle 2 produced 12 discovery winners across five families: Normal 1, Lognormal 2, Weibull 2, Inverse Gaussian 4, Ex-Gaussian 0, Ex-Wald 3.",
            "CV-019 and CV-010 re-enter only as warm starts; they do not receive an automatic win.",
        ],
        "Now test whether the new candidates actually transfer under frozen validation.",
    ),
    "results_stage_2": (
        "Layer 7 · Strict validation",
        "Fixed thesis results",
        [
            "FWVR011 and FWVR012 are frozen Weibull candidates.",
            "Both pass mean and q95 gates in related locked-unseen regimes.",
            "Both fail substantially in original-regime validation.",
            "The correct interpretation is narrow transfer specialist, not family-wide winner.",
        ],
        "After synthetic validation, ask whether related signal appears in real data.",
    ),
    "results_stage_3": (
        "Layer 7 · Real-world battery",
        "Fixed thesis results",
        [
            "External funnel: 264 requested, 228 loaded, 120 evaluated, 43 eligible parent datasets.",
            "Breadth: 26 of 43 parents have at least one corrected specialist win.",
            "Depth: 255 profile-level confirmations inside those eligible parents.",
            "255 confirmations are not 255 independent datasets, and real data do not reveal population theta.",
        ],
        "Finish the evidence journey with the independent Dirichlet abstention audit.",
    ),
    "results_stage_4": (
        "Layer 7 · Dirichlet audit",
        "Fixed thesis results",
        [
            "The audit asks whether arbitrary valid simplex mixtures could easily beat benchmark-retained cells.",
            "23 of 34 audited cells have no random pass; 11 show some signal.",
            "All 8 strongest positive controls pass, showing the audit can detect strong signal when present.",
            "This supports benchmark retention as often meaningful, not merely weak GA search.",
        ],
        "Move to conclusions: harder evidence makes the claim smaller and more credible.",
    ),
    "conclusions_claims": (
        "Layer 8 · Claims H1–H4",
        "Discussion and contributions",
        [
            "H1, H2 and H4 are supported; H3 has conservative support.",
            "H3 is conservative because GA gains survive, but only in narrow validated profiles.",
            "The central conclusion is conditional estimator discovery, not universal GA superiority.",
        ],
        "Open Contributions & Limits to state what the thesis adds and where the claim stops.",
    ),
    "conclusions_contrib": (
        "Layer 8 · Contributions & Limits",
        "Discussion and contributions",
        [
            "Statistical contribution: target-aware robust estimation of the same population mean E[X].",
            "AI contribution: interpretable evolutionary search over simplex-constrained weights.",
            "Methodological contribution: staged validation, benchmark retention and explicit claim control.",
            "Limits: simulated truth, narrow confirmed effects, profile-dependent transfer, and real-data reference rather than known population truth.",
            "Strongest contribution: a reproducible framework that knows when to claim improvement and when to keep the benchmark.",
        ],
        "This ends the timed defense; open the technical appendix only when the committee asks.",
    ),
    "appendix_A": ("Appendix A · Simulation", "Technical backup", ["Use this for why simulation, the six-family regime grid, or the Monte Carlo measurement loop.", "Key sentence: simulation gives known theta and every estimator sees the same replicate."], "Return to the question being answered."),
    "appendix_B": ("Appendix B · Validity", "Technical backup", ["Use this if the simulator or reproducibility is challenged.", "Remember: 125 validation conditions, 0 hard failures, 29 explainable warnings, max mean error 0.976%."], "Return to the question being answered."),
    "appendix_C": ("Appendix C · GA code", "Technical backup", ["Use this for representation, operators, hyperparameters or interpretability.", "Key sentence: fitness guides search; the held-out gate controls acceptance."], "Return to the question being answered."),
    "appendix_D": ("Appendix D · Metrics & gate", "Technical backup", ["Use this for MSE, q95, gain, bootstrap CI, admissibility or the dual gate.", "q95 is difficult-case risk, not a p-value."], "Return to the question being answered."),
    "appendix_E": ("Appendix E · Results", "Technical backup", ["Start with the evidence map; open the candidate-level explorer only if exact CIs or decisions are requested.", "No candidate is retrained in this appendix."], "Return to the question being answered."),
    "appendix_F": ("Appendix F · Q&A", "Technical backup", ["Answer with the first sentence first; expand only when asked.", "Keep returning to conditional improvement, frozen validation and honest benchmark retention."], "Return to the committee question."),
}
