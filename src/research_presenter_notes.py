"""Simple presenter notes for the five didactic Layer 1 views."""

RESEARCH_PRESENTER_NOTES = {
    "research_problem": (
        "Layer 1 · Why a problem?",
        "Research framing",
        [
            "FIXED TARGET|The target stays fixed.",
            "CONDITIONS|The data conditions change.",
            "PERFORMANCE|Estimator performance changes with those conditions.",
            "CONCLUSION|The best estimator can be regime-dependent.",
        ],
        "This leads to the research question.",
    ),
    "research_objective": (
        "Layer 1 · What are we asking?",
        "Research objective and questions",
        [
            "MAIN QUESTION|Can the GA find an improvement that survives validation?",
            "DISCOVER · RQ1|Where can a composite improve?",
            "CONFIRM · RQ2|Do the gains survive with frozen weights?",
            "EXPAND · RQ3|Move from 10 to 26 estimators.",
            "TRANSFER · RQ4|Does the validated specialist transfer?",
            "PROCESS|Search → Freeze → Challenge → Accept / Abstain.",
            "KEY IDEA|Search proposes. Validation decides.",
        ],
        "Next, I show what we expect to happen.",
    ),
    "research_hypotheses": (
        "Layer 1 · What should happen?",
        "H1–H4",
        [
            "H1 · SCOPE|No universal estimator.",
            "H2 · REGIME|Performance depends on the regime.",
            "H3 · OPPORTUNITY|The GA should help only selectively.",
            "H4 · CLAIM CONTROL|If evidence is weak, keep the benchmark.",
            "CHAIN|No universal winner → regime dependence → selective opportunity → claim control.",
            "KEY IDEA|Few winners and many retained benchmarks are an expected outcome.",
        ],
        "Next: what is the GA actually allowed to change?",
    ),
    "research_target": (
        "Layer 1 · What can the GA change?",
        "Fixed target and simplex",
        [
            "TARGET|The population mean stays fixed: θ(F) = μF = E[X].",
            "RECIPE|The GA changes only the estimator weights.",
            "COMPOSITE|One candidate is a weighted mix of named estimators.",
            "SIMPLEX|Weights are non-negative and add to 100%.",
            "INTERPRETABLE|The final recipe remains easy to inspect.",
            "EXAMPLE|The bars on screen are only an illustration.",
            "CAUTION|A valid mixture is not automatically better.",
            "KEY IDEA|The target stays fixed. Only the recipe evolves.",
        ],
        "Next: when can that recipe actually win?",
    ),
    "research_why_win": (
        "Layer 1 · When can a mixture win?",
        "Finite-sample bias–variance logic",
        [
            "MSE|MSE = bias² + variance.",
            "BIAS|A robust mixture may add some bias.",
            "VARIANCE|It may reduce instability.",
            "WIN CONDITION|Variance reduction must be larger than the bias cost.",
            "CLEAN DATA|The mean is already strong. Little room to improve.",
            "HARD REGIMES|Skew, tails, or contamination may create opportunity.",
            "FINAL GATE|Beat the strongest benchmark on MSE and q95.",
            "KEY IDEA|A composite can win — but only conditionally.",
        ],
        "Now simulation lets me measure this against known truth.",
    ),
}
