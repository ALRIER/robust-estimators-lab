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

    "appendix_A": (
        "Appendix A · Simulation",
        "Technical backup",
        [
            "The main reason for simulation is simple: in real data, the true population mean is unknown.",
            "In simulation, I know theta before I score any estimator.",
            "The target stays the population mean: theta equals E of X.",
            "A regime is defined by family, contamination rate, outlier scale, contamination mechanism, and sample size.",
            "The study uses six distribution families and five sample sizes.",
            "For each regime, I generate a sample, apply every estimator to the same sample, compare each estimate with theta, and repeat this many times.",
            "The repeated errors give mean MSE and q95 difficult-case risk.",
        ],
        "My key point is: simulation gives controlled truth, and Monte Carlo gives a fair repeated comparison.",
    ),
    "appendix_B": (
        "Appendix B · Validity",
        "Technical backup",
        [
            "I did not assume the simulator was correct. I tested it before using GA results.",
            "There were 125 validation conditions, zero hard failures, and 29 explainable warnings.",
            "The maximum relative mean error was 0.976 percent, below the 1 percent hard threshold.",
            "Moment fidelity checks that the generator recovers the intended mean.",
            "Contamination fidelity checks that the realised contamination matches the regime label.",
            "Theory recovery checks that known statistical patterns appear before I trust new GA findings.",
            "Empirical anchoring uses real datasets as structural references, not as known population truth.",
            "Every estimator sees the same sample inside one Monte Carlo replicate, and fixed seeds support reproducibility.",
            "The 29 warnings are diagnostics, not 29 failures.",
        ],
        "The key point is: the simulator was validated independently of the GA.",
    ),
    "appendix_C": (
        "Appendix C · GA mechanics",
        "Technical backup",
        [
            "The GA searches weights over named estimators. It does not learn a black-box prediction model.",
            "C is the matrix of estimator outputs. w is one simplex weight vector. C times w gives one composite candidate.",
            "The weights are non-negative and sum to one, so every candidate is an interpretable convex mixture.",
            "The population starts with Dirichlet weight vectors.",
            "Selection keeps pressure toward better candidates. Convex crossover mixes parents. Mutation changes the weights while staying valid.",
            "Elitism keeps strong candidates and immigration adds fresh diversity.",
            "Warm starts are allowed to enter a later search, but they do not receive an automatic win.",
            "Fitness only tells the GA where to search. The held-out gate decides whether the scientific claim is allowed.",
        ],
        "The shortest summary is: search proposes; validation decides.",
    ),
    "appendix_D": (
        "Appendix D · Metrics & gate",
        "Technical backup",
        [
            "The target is always the population mean, theta equals E of X.",
            "Mean MSE measures typical squared error across replications.",
            "q95 measures difficult-case squared error in the upper tail. It is not a p-value.",
            "A positive gain means the candidate has lower risk than the benchmark. A negative gain means the benchmark is better.",
            "The final gate needs both mean MSE gain and q95 gain to support replacement.",
            "If one side fails, the benchmark stays.",
            "Paired bootstrap confidence intervals show uncertainty around the gain.",
            "The comparison is against the strongest admissible benchmark, not an intentionally weak baseline.",
        ],
        "The key point is: a high GA fitness is not enough; both risk criteria must support replacement.",
    ),
    "appendix_E": (
        "Appendix E · Results",
        "Technical backup",
        [
            "This page is a technical map of evidence already shown in Layer 7. It does not rerun the GA.",
            "Cycle I went from 36 controlled regimes to 16 discovery wins to 2 frozen Lognormal confirmations.",
            "CV-019 has a q95 gain of 16.3 percent and CV-010 has 2.2 percent; both survive 8 of 8 validation seeds.",
            "Cycle II expanded the learnable basis from 10 to 26 components and produced 12 discovery winners across five families.",
            "FWVR011 and FWVR012 are Weibull transfer specialists: both pass in related locked-unseen regimes but fail in original-regime mode.",
            "The external battery narrowed from 264 requested targets to 43 eligible parent datasets. Twenty-six parents had at least one corrected win, with 255 profile-level confirmations.",
            "The 255 confirmations are not 255 independent datasets.",
            "In the Dirichlet audit, 23 of 34 retained cells had no random pass, 11 showed some signal, and all 8 strongest positive controls passed.",
            "If the committee asks for one exact candidate, I can open the candidate-level explorer below this page.",
        ],
        "The key point is: the claim becomes narrower as validation becomes harder, and that is intentional.",
    ),
    "appendix_F": (
        "Appendix F · Q&A",
        "Technical backup",
        [
            "Give the first sentence first. Do not start with a long answer.",
            "Why simulation? Because it gives known truth.",
            "Why GA? Because it searches many interpretable weight combinations across generations.",
            "Why q95? Because average MSE can hide difficult-case error.",
            "What is frozen validation? The weights are locked before new evidence is tested.",
            "Why can a candidate pass locked-unseen and fail original-regime validation? Because it can be a narrow transfer specialist, not a general winner.",
            "What do real-data results prove? External empirical support, not known-truth validation.",
            "Why is benchmark retention a result? Because the design allows the GA to lose when replacement is not supported.",
            "What is the strongest contribution? A reproducible framework for knowing when to claim improvement and when to keep the benchmark.",
            "What is the main limitation? The strongest known-truth validation is simulation-based and the confirmed gains are narrow.",
        ],
        "Answer the question, then return to the main conclusion: conditional improvement with honest benchmark retention.",
    ),
}
