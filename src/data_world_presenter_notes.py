"""Simple HELP notes for Layer 2 after the Monte Carlo sequence moved to Layer 4."""

DATA_WORLD_PRESENTER_NOTES = {
    "data_world_why_simulation": (
        "Layer 2 · Why simulation?",
        "Known-truth simulation logic",
        [
            "Main idea: I use simulation because I need to know the true population mean before I can measure estimator error.",
            "In real data, I observe the sample but I do not directly know the true population mean.",
            "In simulation, theta is defined before any estimator is scored.",
            "The target is theta(F) = mu_F = E_F[X]. It is always the population mean.",
            "This layer explains why known truth is needed. It does not explain the full Monte Carlo engine anymore.",
            "The short bridge is: known truth, repeated samples, measurable risk.",
            "Layer 4 contains the complete repeated-sampling sequence and the MSE and q95 calculations.",
            "Important: simulation is a measurement tool. It does not replace the later real-data stage.",
        ],
        "Now I can define exactly what changes from one synthetic condition to another: the regime.",
    ),
    "data_world_regime": (
        "Layer 2 · Build a regime",
        "Regime definition and structural coverage",
        [
            "A regime is one complete statistical environment.",
            "R = (F0, gamma, c, m, n): baseline family, contamination rate, outlier scale, contamination mechanism and sample size.",
            "F_R = (1 - gamma)F0 + gamma G_m,c(F0). The first part is clean data and the second part is the designed contamination.",
            "The target is still the population mean. The regime changes the sampling environment, not the type of estimand.",
            "The six families are Normal, Lognormal, Weibull, Inverse Gaussian, Ex-Gaussian and Ex-Wald.",
            "The controlled grid contains 6 families, 5 sample sizes, 576 profiles per family and 2,880 regimes per family.",
            "The key sentence is: change the regime, change finite-sample risk, and the estimator ranking may also change.",
        ],
        "The next view shows that this simulated world was checked before any GA evidence was trusted.",
    ),
    "data_world_validity": (
        "Layer 2 · Trust the simulator",
        "Simulator certification summary",
        [
            "This is the high-level certification summary for the simulated world.",
            "The headline numbers are 125 validation conditions, 0 hard failures, 29 retained warnings and 0.976 percent maximum mean error.",
            "The four checks are moment fidelity, contamination fidelity, theory recovery and empirical anchoring.",
            "Every estimator sees the same sample inside one Monte Carlo replicate, and seeds and regimes are logged for reproducibility.",
            "The detailed validation sequence is shown later in Layer 4, where validation is connected to the full Monte Carlo pipeline.",
            "Important: 29 warnings are not 29 failures. Warnings remain visible as diagnostic cases.",
            "The key sentence is: the simulator is validated independently of the GA.",
        ],
        "Now I can show one generated sample in the Simulation Lab before moving to repeated sampling in Layer 4.",
    ),
}
