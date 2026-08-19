"""Simple HELP notes for Layer 6 · Thesis GA Architecture."""

THESIS_GA_PRESENTER_NOTES = {
    "pipeline_architecture": (
        "Layer 6 · Thesis GA Architecture",
        "Implemented GA search-and-claim architecture",
        [
            "Use this page from top to bottom. Each block has one job.",
            "Section 1: Monte Carlo outputs are stored in matrix C. Rows are replications and columns are named estimators.",
            "The GA changes only the weight vector w. It does not change the raw observations and it does not change the target theta.",
            "Multiplying C by w gives the composite outputs across all replications. This makes candidate scoring fast.",
            "Notation: C is the estimator-output matrix, w is a simplex weight vector, and Cw is the composite output vector.",
            "Section 2: the evolution loop is Dirichlet initialization, selection, crossover, mutation, and diversity control.",
            "Dirichlet initialization starts with valid proportions. Selection uses tournament 2 or 3. Crossover is a convex blend. Mutation is a Dirichlet nudge. Diversity uses elitism and immigration.",
            "The loop repeats across generations and folds. Evolution changes the recipe, not the scientific target.",
            "Section 3: fitness is not the final claim. Fitness only guides the search.",
            "The search objective shown here is 0.70 q95 plus 0.30 max loss, plus regularisation.",
            "A good fitness value produces a promising candidate w star. It does not confirm the candidate.",
            "After search, the weights are frozen. The candidate cannot adapt to the held-out evidence.",
            "Then the held-out dual gate controls the claim.",
            "Section 4: the final gate requires Delta MSE greater than or equal to zero AND Delta q95 greater than or equal to zero.",
            "If both criteria support replacement, the candidate can pass. If one fails, the benchmark is retained.",
            "The configuration is visible for audit: population N=100, K=3 folds, G=20 generations per fold, seeds 101 and 202, mutation settings, immigration settings, and the documented stopping rule.",
            "Most important sentence: fitness guides search; the gate controls the claim.",
            "Do not say the GA proves superiority by itself. The GA proposes candidates inside a larger validation system.",
        ],
        "Now move to the Evidence Pipeline to show how discovery, freezing, confirmation, rediscovery, transfer, and external evidence are separated.",
    ),
}
