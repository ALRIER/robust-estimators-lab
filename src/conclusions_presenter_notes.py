"""Accessible presenter cues for Layer 8 · Conclusions."""

CONCLUSIONS_PRESENTER_NOTES = {
    "conclusions_claims": (
        "Layer 8 · Claims H1–H4",
        "Discussion and contributions",
        [
            "H1|No universal estimator — supported.",
            "H2|Performance changes by regime — supported.",
            "H3|GA gains survive, but only in narrow profiles — conservative support.",
            "H4|The gate rejects weak discoveries — supported.",
            "CONCLUSION|Conditional estimator discovery, not universal GA superiority.",
        ],
        "Next: state what the thesis contributes statistically, methodologically, and as an AI search framework.",
    ),
    "conclusions_contrib": (
        "Layer 8 · Contributions & Limits",
        "Discussion and contributions",
        [
            "STATISTICS|Estimate the same target E[X], but search for lower risk in selected regimes.",
            "AI SEARCH MODEL|The GA searches and improves estimator mixtures across generations.",
            "AI USE|Reusable idea: add estimators, define an objective, evolve interpretable recipes.",
            "INTERPRETABLE|The output is weights over named estimators — not a black box.",
            "METHOD|Search → freeze → validate → accept or abstain.",
            "NOVELTY|This thesis proposes an integrated AI search + estimator-design + claim-control framework.",
            "POTENTIAL|The architecture can be extended; this thesis validates the population-mean target E[X].",
            "LIMIT|Known-truth evidence is simulated and the strongest confirmed gains are narrow.",
            "STRONGEST|AI searches for better estimators; independent evidence decides when improvement is real.",
        ],
        "End the timed defense here. Open the technical appendix only for committee questions.",
    ),
}
