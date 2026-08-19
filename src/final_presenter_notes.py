"""Simple presenter-note entries for the current defense views.

Each value is:
(title, source label, simple speaking bullets, transition)

The wording is intentionally easy to say aloud during the defense.
"""

FINAL_PRESENTER_NOTES = {
    # ------------------------------------------------------------------
    # Layer 2 · Data-generating world
    # ------------------------------------------------------------------
    "data_world_why_simulation": (
        "Layer 2 · Why simulation?",
        "Methods · known-truth simulation logic",
        [
            "Main idea: I use simulation because I need to know the true population mean before I measure estimator error.",
            "In real data, I can observe the dataset, but I cannot directly observe the true population mean.",
            "In simulation, the generating distribution defines the target first: theta of F equals mu F equals E of X.",
            "The target is always the population mean. What changes later is the data-generating regime around that target.",
            "Monte Carlo is simple: choose one regime, generate one sample, apply every estimator to the same sample, compare with the known target, and repeat many times.",
            "Using the same sample inside one replicate makes the estimator comparison fair.",
            "Important: simulation is a measurement tool. It does not replace the later real-data stage.",
            "Formula to remember: theta(F) = mu_F = E_F[X]. This means the target is the population mean under distribution F.",
        ],
        "Now I can define exactly what changes from one synthetic condition to another: the regime.",
    ),
    "data_world_regime": (
        "Layer 2 · Build a regime",
        "Methods · regime definition and structural coverage",
        [
            "A regime is one complete statistical environment.",
            "Formula: R = (F0, gamma, c, m, n). F0 is the baseline family, gamma is contamination rate, c is outlier scale, m is the contamination mechanism, and n is sample size.",
            "The induced distribution is F_R = (1 - gamma) F0 + gamma G_m,c(F0). The first part is clean data; the second part is the designed contamination.",
            "The target is still the population mean. The regime changes the sampling environment, not the type of estimand.",
            "The six families are Normal, Lognormal, Weibull, Inverse Gaussian, Ex-Gaussian and Ex-Wald.",
            "They are useful because they create different symmetry, skewness and tail structures.",
            "The controlled grid contains 6 families, 5 sample sizes, 576 profiles per family and 2,880 regimes per family.",
            "The key causal sentence is: change the regime, change finite-sample risk, and the estimator ranking may also change.",
            "Do not say one family is globally harder or that one estimator should always win. The study is conditional by design.",
        ],
        "Before trusting any estimator comparison, I first check that this simulated world behaves as intended.",
    ),
    "data_world_validity": (
        "Layer 2 · Trust the simulator",
        "Methods · simulator certification",
        [
            "Main idea: the simulator is tested before the GA evidence is interpreted.",
            "The validation summary is 125 conditions, 0 hard failures, 29 explainable warnings, and a maximum mean error of 0.976 percent.",
            "Moment fidelity asks: does the generator recover the intended analytic mean? The maximum relative mean error stayed below the 1 percent hard threshold.",
            "Contamination fidelity asks: did we actually generate the stress condition we labelled? We check realised rate, direction and MAD-based distance.",
            "Theory recovery asks: do known robust-statistics patterns appear before we trust new GA findings?",
            "Empirical anchoring uses real datasets as structural anchors. They are not treated as known population truth and they are not GA training targets.",
            "Fair comparison: every estimator sees the same sample inside one Monte Carlo replicate.",
            "Reproducibility: seeds and regime settings are fixed and logged.",
            "Important: 29 warnings are not 29 failures. Warnings are retained diagnostic cases and can reflect natural flags, dilution, masking, scale effects or anchoring mismatch.",
            "The sentence to finish with is: the simulator is validated independently of the GA.",
        ],
        "Now I can show one sample from this validated world in the Simulation Lab.",
    ),

    # ------------------------------------------------------------------
    # Layer 7 · Results journey
    # ------------------------------------------------------------------
    "results_stage_0": (
        "Layer 7 · Discovery + Frozen I",
        "Fixed thesis results",
        [
            "Read the funnel from 36 controlled regimes to 16 discovery wins to 2 frozen confirmations.",
            "Discovery is an opportunity signal, not a final result.",
            "CV-019 and CV-010 are the two Lognormal signals that survive 8 out of 8 validation seeds.",
            "Do not call all 16 discovery wins confirmed results.",
        ],
        "Move to expanded rediscovery: what changes when the search basis gets stronger?",
    ),
    "results_stage_1": (
        "Layer 7 · Expanded rediscovery",
        "Fixed thesis results",
        [
            "Cycle 1 used 10 learnable components. Cycle 2 reopened the search with 26.",
            "HPF2 exposure increased from 80 percent to 90 percent.",
            "Cycle 2 produced 12 discovery winners: Normal 1, Lognormal 2, Weibull 2, Inverse Gaussian 4, Ex-Gaussian 0, and Ex-Wald 3.",
            "CV-019 and CV-010 enter only as warm starts. They do not receive an automatic win.",
        ],
        "Now test whether the new candidates actually transfer under frozen validation.",
    ),
    "results_stage_2": (
        "Layer 7 · Strict validation",
        "Fixed thesis results",
        [
            "FWVR011 and FWVR012 are frozen Weibull candidates.",
            "Both pass mean and q95 gates in related locked-unseen regimes.",
            "Both fail strongly in original-regime validation.",
            "The correct interpretation is narrow transfer specialist, not family-wide winner.",
        ],
        "After synthetic validation, ask whether related signal appears in real data.",
    ),
    "results_stage_3": (
        "Layer 7 · Real-world battery",
        "Fixed thesis results",
        [
            "External funnel: 264 requested, 228 loaded, 120 evaluated, and 43 eligible parent datasets.",
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
            "23 of 34 audited cells have no random pass. 11 show some signal.",
            "All 8 strongest positive controls pass, so the audit can detect strong signal when it is present.",
            "This supports benchmark retention as often meaningful, not simply weak GA search.",
        ],
        "Move to conclusions: harder evidence makes the claim smaller and more credible.",
    ),

    # ------------------------------------------------------------------
    # Layer 8 · Conclusions
    # ------------------------------------------------------------------
    "conclusions_claims": (
        "Layer 8 · Claims H1–H4",
        "Discussion and contributions",
        [
            "H1, H2 and H4 are supported. H3 has conservative support.",
            "H3 is conservative because GA gains survive, but only in narrow validated profiles.",
            "The central conclusion is conditional estimator discovery, not universal GA superiority.",
        ],
        "Open Contributions & Limits to state what the thesis adds and where the claim stops.",
    ),
    "conclusions_contrib": (
        "Layer 8 · Contributions & Limits",
        "Discussion and contributions",
        [
            "Statistical contribution: target-aware robust estimation of the same population mean E of X.",
            "AI contribution: interpretable evolutionary search over simplex-constrained weights.",
            "Methodological contribution: staged validation, benchmark retention and explicit claim control.",
            "Main limits: simulated truth, narrow confirmed effects, profile-dependent transfer, and real-data reference instead of known population truth.",
            "Strongest contribution: a reproducible framework that knows when to claim improvement and when to keep the benchmark.",
        ],
        "This ends the timed defense. Open the technical appendix only when the committee asks.",
    ),

    # ------------------------------------------------------------------
    # Layer 9 · Technical appendix — deliberately narrow after Layer 2 redesign
    # ------------------------------------------------------------------
    "appendix_A": (
        "Appendix A · GA mechanics",
        "Technical backup",
        [
            "Use this page only if the committee asks how the real thesis GA works.",
            "C is the estimator-output matrix. Rows are Monte Carlo replications and columns are named base estimators.",
            "The composite is T_mix = Cw. The GA searches the weight vector w.",
            "The simplex rule is simple: every weight is non-negative and all weights add to 1.",
            "The generation flow is Dirichlet start, selection, convex crossover, mutation, elitism and immigration.",
            "Warm-started does not mean privileged. A warm start must compete again with the new search basis.",
            "Search settings shown here are the thesis settings, not a live GA run.",
            "Most important sentence: fitness guides search; the held-out gate controls acceptance.",
        ],
        "Answer the committee question directly. Open Metrics & Gate only if they ask how acceptance is decided.",
    ),
    "appendix_B": (
        "Appendix B · Metrics & gate",
        "Technical backup",
        [
            "Use this page for MSE, q95, gain, bootstrap confidence intervals, admissibility or the dual gate.",
            "The target is theta(F) = mu_F = E_F[X]. It is the population mean.",
            "MSE measures average squared error across repeated samples.",
            "q95 measures difficult-case squared error. It is not a p-value.",
            "Positive Gain percent means the candidate has lower risk than the benchmark. Negative gain means the benchmark is better.",
            "The gate has two checks: mean MSE gain must be non-negative AND q95 gain must be non-negative.",
            "If one criterion fails, the benchmark stays.",
            "Bootstrap confidence intervals show uncertainty around the gain. An interval crossing zero weakens the replacement claim.",
            "The comparator is the best admissible benchmark, not a deliberately weak baseline.",
        ],
        "If the committee asks for the exact candidates or numbers, move to Results.",
    ),
    "appendix_C": (
        "Appendix C · Technical results",
        "Technical backup",
        [
            "Use this page for exact evidence behind Layer 7.",
            "Cycle I is 36 regimes to 16 discovery wins to 2 frozen confirmations.",
            "CV-019 has about 16.3 percent q95 gain and CV-010 about 2.2 percent; both survive 8 out of 8 validation seeds.",
            "Expanded rediscovery used 26 learnable components and produced 12 discovery winners across five families.",
            "FWVR011 and FWVR012 pass related locked-unseen validation but fail original-regime validation. Call them narrow transfer specialists.",
            "External breadth is 26 of 43 eligible parent datasets. External depth is 255 profile-level confirmations.",
            "Do not call 255 confirmations 255 independent datasets.",
            "Dirichlet audit: 23 of 34 no random pass, 11 of 34 some signal, and 8 of 8 strongest positive controls pass.",
            "The candidate-level explorer is only for an exact candidate, seed, mode, decision or confidence interval.",
        ],
        "Return to the committee question instead of walking through every result again.",
    ),
    "appendix_D": (
        "Appendix D · Committee Q&A",
        "Technical backup",
        [
            "Rule: say the bold short answer first. Add more detail only if the committee asks.",
            "Why GA? Because I search many interpretable weight combinations across generations.",
            "Why q95? Because average performance can hide difficult cases.",
            "What is frozen validation? The weights are locked before new evidence is evaluated.",
            "Why benchmark retention? Because the design allows the GA to lose when replacement is not supported.",
            "What do real-data results prove? External empirical support, not known-truth validation.",
            "What is the strongest contribution? A reproducible framework that knows when to claim improvement and when to keep the benchmark.",
            "Main limitation: known-truth evidence is simulation-based and confirmed gains are narrow.",
        ],
        "Finish the answer and return to the committee. Do not turn the appendix into a second presentation.",
    ),
}
