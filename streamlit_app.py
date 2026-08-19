import streamlit as st
import streamlit.components.v1 as components
import time
from base64 import b64encode
from pathlib import Path
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
from src.synthetic_data import DemoScenario, draw_sample
from src.estimators import location_estimates
from src.mini_ga import MiniGAConfig, run_pedagogical_ga
from src import simplex as simplex_renderer
from src.fixed_simplex import fixed_simplex_figure
from src.simplex_svg import simplex_svg
from src.cluster_evolution import cluster_map_svg, contamination_shift_svg
from src.experiment_pipeline import STAGES as PIPELINE_STAGES, experiment_pipeline_svg
from src.thesis_ga_architecture import thesis_ga_architecture_svg
from src.defense_mode import VALIDATION_STAGES, defense_scene_svg, validation_scene_svg
from src.research_logic import PANELS as RESEARCH_PANELS, research_logic_svg
from src.data_world import DATA_WORLD_VIEWS, data_world_detail_svg
from src.data_loader import load_winners, load_final_decisions, load_bootstrap_ci, load_evidence_taxonomy, load_validated_specialists, load_dirichlet_summary, load_dirichlet_signals
from src.constants import ESTIMATOR_NAMES

UNIVERSITY_LOGO_DATA_URI = (
    "data:image/jpeg;base64,"
    + b64encode((Path(__file__).parent / "assets" / "university_of_hull_logo.jpeg").read_bytes()).decode("ascii")
)

# Presenter notes are a rehearsal aid, not a source of new thesis claims.  Each
# entry below is condensed from the defense deck, thesis, and final KBS notation.
PRESENTER_NOTES = {
    "cover": ("Opening", "Defense deck · title slide", [
        "Introduce the problem in one sentence: we want better estimates of a population mean when ordinary conditions fail.",
        "State the bounded contribution: this is benchmark-gated, regime-conditional discovery — not a claim that a GA is universally superior.",
    ], "Move to the research logic: why this experiment is necessary."),
    "research_problem": ("Layer 1 · Problem", "Final KBS manuscript · regime dependence and fixed target", [
        ("HELP", "The problem is not that the target changes. The estimand remains the population mean μ_F = E_F[X]. What changes is the data-generating regime. A regime specifies the baseline family, contamination rate, outlier scale, contamination mechanism, and sample size; together these induce the sampling distribution F_ℛ. Under clean, near-symmetric conditions the sample mean can be highly efficient. Under skewness, heavy tails, or contamination, extreme observations can change the finite-sample risk ranking and robust estimators may move less. So the thesis asks which estimator is justified within a regime, not which estimator wins universally."),
        ("FORMULAS AND NOTATION", ["Regime: ℛ = (F₀, γ, c, m, n).", "F₀ = baseline distribution family; γ = contamination rate; c = outlier scale; m = contamination mechanism; n = sample size.", "Induced distribution: F_ℛ = (1−γ)F₀ + γG_{m,c}(F₀).", "F_ℛ is the distribution from which samples are generated under that regime.", "Fixed target: θ(F) = μ_F = E_F[X].", "The target is always the population mean; it does not move when the regime changes.", "Key interpretation: change the regime → change finite-sample risk → potentially change the estimator ranking."]),
        ("POSSIBLE QUESTIONS", [("Why not use the mean everywhere?", "Clean-data efficiency does not imply uniform finite-sample reliability under skewness, heavy tails, or contamination."), ("Why define F_ℛ explicitly?", "It separates the fixed estimand from the sampling environment and makes clear that performance is regime-conditional."), ("Does contamination change the estimand?", "No. Every estimator is still judged against μ_F = E_F[X] for the distribution being studied.")]),
    ], "Therefore the question is not ‘which estimator always wins?’ but ‘under which regimes can improvement be justified?’"),
    "research_objective": ("Layer 1 · Objective / research questions", "Final KBS manuscript · theoretical background and methods", [
        ("HELP", "The objective is to determine whether evolutionary search can identify interpretable convex mixtures of location estimators that improve estimation of the fixed population mean μ_F under defined regimes, and whether those advantages remain credible after the search is over. The GA is only the proposal mechanism. It searches over simplex-constrained weight vectors. A proposed candidate is then frozen and challenged with held-out evidence, stronger benchmarks, independent seeds, related regimes, and external data. Success therefore includes both supported specialists and justified benchmark retention."),
        ("FORMULAS AND NOTATION", ["Fixed target: θ(F) = μ_F = E_F[X].", "Composite candidate: θ̂_{w,n} = Σⱼ₌₁ᴸ wⱼTⱼ,n.", "Tⱼ,n = jth base location estimator at sample size n; wⱼ = its learned weight; L = number of learnable components.", "Search space: w ∈ Δ_L, where Δ_L = {w ∈ [0,1]^L : Σⱼwⱼ = 1}.", "Discovery proposes w; confirmation freezes w and evaluates fresh evidence without retraining.", "Benchmark gate: improvement must be supported in both mean MSE and q₀.₉₅ MSE; one criterion alone is insufficient."]),
        ("POSSIBLE QUESTIONS", [("Why use a GA rather than select one estimator?", "It searches transparent convex combinations while retaining named, auditable components."), ("Why is the gate necessary?", "Optimisation can exploit a discovery setting; the gate separates a promising candidate from an evidence-supported replacement."), ("What is success?", "Either a supported specialist or a justified decision to retain the strongest admissible benchmark.")]),
    ], "Before looking at results, make the predictions explicit."),
    "research_hypotheses": ("Layer 1 · H1–H4", "Defense deck · 01 Research framing; final KBS framing", [
        ("HELP", "These four hypotheses are one reasoning chain. H1 says there should be no universal winner across incompatible regimes. H2 says estimator performance therefore depends on the regime and its induced distribution F_ℛ. H3 says a GA mixture may help, but only selectively where the bias–variance trade-off creates genuine opportunity. H4 controls the scope of the claim: the benchmark gate must be allowed to reject a discovered mixture and retain the benchmark. The expected pattern is selective improvement, not widespread GA dominance."),
        ("FORMULAS AND NOTATION", ["Hypothesis chain: H1 → H2 → H3 → H4.", "H1: no universal estimator across incompatible regimes.", "H2: finite-sample risk depends on F_ℛ and n.", "H3: a simplex composite may lower risk only in selected regimes.", "H4: benchmark-gated acceptance prevents discovery from automatically becoming a final claim.", "The fixed target throughout is θ(F) = μ_F = E_F[X].", "The evidence layer later evaluates both mean MSE and q₀.₉₅ MSE."]),
        ("POSSIBLE QUESTIONS", [("Is H3 a claim that GA should win often?", "No. It predicts selected, regime-specific opportunity."), ("Does retaining a benchmark reject the whole study?", "No. Benchmark retention is an intended scientific outcome when replacement is unsupported."), ("Why is H4 important?", "It makes abstention part of the design and prevents hindsight interpretation of discovery signals as universal evidence.")]),
    ], "Now define exactly what is fixed and what the GA is allowed to change."),
    "research_target": ("Layer 1 · Target / simplex", "Final KBS manuscript · composite risk and conditional improvement", [
        ("HELP", "Here I separate the estimand from the estimator. The estimand is fixed at θ(F) = μ_F = E_F[X]. The GA never changes that target. Each GA individual is only a weight vector over named location estimators. Because the weights lie on the simplex, they are non-negative and sum to one, so every candidate is an interpretable convex mixture. Importantly, being a valid simplex vector does not make a candidate better; performance must still be established against the same fixed target and strongest admissible benchmark."),
        ("FORMULAS AND NOTATION", ["Target: θ(F) = μ_F = E_F[X], whenever E_F[|X|] < ∞.", "Composite estimator: θ̂_{w,n} = Σⱼ₌₁ᴸ wⱼTⱼ,n.", "Simplex: w ∈ Δ_L = {w ∈ [0,1]^L : Σⱼ₌₁ᴸ wⱼ = 1}.", "wⱼ ≥ 0 means no component has a negative contribution.", "Σwⱼ = 1 means the weights are proportions that sum to 100%.", "Operational admissibility also requires the estimator to be well defined on the support; for example, geometric and harmonic means require positive observations.", "Target compatibility and simplex validity are separate from evidence of lower finite-sample risk."]),
        ("POSSIBLE QUESTIONS", [("Why insist on non-negative weights?", "They keep the candidate inside an interpretable convex mixture rather than allowing arbitrary negative extrapolation."), ("Why not let the GA estimate μ_F directly?", "The contribution is an auditable aggregation of established estimators, not a black-box predictor."), ("Does a valid simplex vector guarantee robustness or better performance?", "No. Convex validity does not guarantee robustness or lower risk; the benchmark gate must establish that empirically.")]),
    ], "A valid mixture can still lose; next is the exact finite-sample condition under which it can improve."),
    "research_why_win": ("Layer 1 · Why a composite can win", "Final KBS manuscript · composite risk and conditional improvement", [
        ("HELP", "A composite can only win through a favourable finite-sample bias–variance trade-off. For fixed weights, its MSE equals squared bias plus variance. Moving weight away from the sample mean may introduce bias relative to μ_F, but it can also reduce sampling variability or sensitivity to extremes. The composite beats the sample mean only when that variance reduction is large enough to compensate for the squared bias cost. This is why clean light-tailed symmetry leaves little room, while skewness, heavy tails, or contamination can create conditional opportunity. The benchmark gate then extends the same logic beyond the sample mean to the strongest admissible comparator and requires support in both mean MSE and q₀.₉₅ MSE."),
        ("FORMULAS AND NOTATION", ["Finite-sample MSE: MSE_{F,n}(θ̂_{w,n}) = B_n(w,F)² + V_n(w,F).", "Bias: B_n(w,F) = Σⱼ₌₁ᴸ wⱼ{E_F[Tⱼ,n] − μ_F}.", "Variance: V_n(w,F) = Var_F(θ̂_{w,n}).", "Dominance over the sample mean: B_n(w,F)² + V_n(w,F) < Var_F(X̄_n).", "Interpretation: the variance reduction must exceed the squared bias cost.", "The final benchmark gate is stricter: the candidate must improve both mean MSE and q₀.₉₅ MSE relative to the criterion-specific strongest admissible benchmark."]),
        ("POSSIBLE QUESTIONS", [("Is bias always bad?", "No. A small bias can be worthwhile if it buys a larger reduction in variance, but the trade-off is always measured against μ_F."), ("Why not minimise mean MSE alone?", "A method can look good on average while producing poor difficult-case errors; q₀.₉₅ MSE adds upper-tail protection."), ("Why is clean Normal data important?", "It is a hard baseline for improvement because the sample mean is already highly efficient there.")]),
    ], "Simulation lets us measure that finite-sample trade-off against known truth."),
    "data_world": ("Layer 2 · Data-generating world", "Defense deck · Monte Carlo evaluation; Appendix A1/A2", [
        "Simulation is deliberate because it makes the true target known; real datasets do not reveal the population mean.",
        "The grid varies family, sample size, contamination rate, outlier scale and contamination mechanism to stress estimator failure modes.",
        "The simulator is validated before any GA conclusion is trusted.",
    ], "First inspect one generated sample in the Simulation Lab before moving to repeated sampling."),
    "data_world_families": ("Layer 2 · Six Families", "Defense deck · Appendix A2; thesis distribution-family table", [
        ("HELP", [
            "The six families create deliberately different statistical environments rather than six arbitrary datasets.",
            "They vary symmetry, positive skew, tail behaviour, duration structure and first-passage behaviour.",
            "The population-mean estimand remains the same type of target across families; what changes is the sampling environment and therefore finite-sample risk.",
            "This structural diversity is what makes H1 and H2 testable rather than assumed.",
        ]),
        ("POSSIBLE QUESTIONS", [
            ("Why exactly these six families?", "They cover the structural shapes emphasized in the thesis: a symmetric baseline, positive right skew, flexible survival-like shapes, asymmetric durations, and reaction-time or first-passage-like tails."),
            ("Are these six real datasets?", "No. They are synthetic distribution families used to create controlled risk environments. Real datasets are used later for external calibration."),
            ("Why not study only Normal and Lognormal?", "Two families would not provide enough structural coverage to test whether estimator rankings change across substantially different skew, tail and hazard shapes."),
            ("Does changing family mean changing the scientific target?", "No. Each estimator is still judged as an estimator of the population mean for the distribution under study."),
        ]),
    ], "After defining structural coverage, show that the generator itself was independently certified."),
    "data_world_certification": ("Layer 2 · Simulator Certification", "Defense deck · Appendix B1", [
        ("HELP", [
            "The simulator is checked before any GA result is trusted.",
            "Certification is independent of the GA and therefore tests the simulated world rather than the algorithm's conclusion.",
            "Four checks cover moment fidelity, contamination fidelity, theory recovery and empirical anchoring.",
            "Across 125 validation conditions there were 0 hard failures and 29 explainable warnings.",
            "Warnings are retained for transparency; they are diagnostic cases, not failed validation conditions.",
        ]),
        ("POSSIBLE QUESTIONS", [
            ("How do you know the simulator is not biased in favour of the GA?", "The validation checks are independent of the GA and run before GA conclusions are interpreted. They certify the simulated world, not the search result."),
            ("What do the 29 warnings mean?", "They are diagnostic, explainable cases associated with expected variance, dilution, masking or empirical anchoring mismatch; they are not hard failures."),
            ("What was checked?", "Moment fidelity, contamination rate/direction/MAD distance, recovery of known robust-statistics behaviour, and empirical structural anchoring."),
            ("Why is empirical anchoring not ground-truth validation?", "A real dataset does not reveal the population mean. It is used to check structural relevance, not to provide known-theta truth."),
        ]),
    ], "With the synthetic world certified, inspect one generated sample before moving to repeated-sampling risk."),
    "simulation_lab": ("Layer 3 · Simulation lab", "Defense script map", [
        "Change contamination and observe estimator movement. Keep the message simple: estimator ranking depends on the regime.",
        "This is a deterministic pedagogical demonstration, not a rerun of the thesis search.",
    ], "Now move from one sample to repeated sampling with the Monte Carlo engine."),
    "monte_carlo_engine": ("Layer 4 · Monte Carlo measurement engine", "Defense deck · 05 Monte Carlo evaluation", [
        "Specify one regime R, compute θ = E[X], generate repeated samples, and apply every estimator to the same sample paths.",
        "For each replication, calculate (Tj(x(r)) − θ)². Aggregate to MSE and q95 MSE.",
        "The GA does not create the target; it searches using certified error estimates from this procedure.",
    ], "With repeated-sampling risk measured, the search procedure can now be interpreted."),
    "monte_carlo_validation_0": ("Layer 4 · Validation: moment fidelity", "Defense deck · Appendix A1", [
        "Check that large generated populations recover their analytic moments before scoring estimators.",
        "If the population target is wrong at this stage, every subsequent error calculation is wrong.",
    ], "Proceed to validate the contamination design."),
    "monte_carlo_validation_1": ("Layer 4 · Validation: contamination fidelity", "Defense deck · Monte Carlo workflow", [
        "Verify that the realised contamination rate and severity match the regime label after injection.",
        "A declared upper-tail or 10% contamination regime must behave as labelled before it enters the experiment.",
    ], "Then check a known statistical benchmark."),
    "monte_carlo_validation_2": ("Layer 4 · Validation: statistical sanity", "Defense deck · Appendix A1", [
        "Under clean Normal data, the sample mean should outperform the median in MSE; this is a theory-based sanity check.",
        "Recovering this ordering supports the fitness and error calculations, but does not yet prove a GA result.",
    ], "Finally, connect the synthetic grid to relevant empirical shapes."),
    "monte_carlo_validation_3": ("Layer 4 · Validation: empirical anchoring", "Thesis abstract; defense deck · Appendix A1", [
        "Public-data diagnostics are used to check that synthetic worlds cover relevant shapes of interest.",
        "This is calibration, not known-θ validation: real data do not provide population ground truth.",
    ], "Only after these checks is the search procedure interpreted."),
    "ga_search": ("Layer 5 · GA search", "Defense deck · 05 Genetic Algorithm Search", [
        "The GA receives certified error information and an admissible estimator bank, then initializes valid simplex weight vectors.",
        "Selection, crossover, mutation and elitism propose a candidate specialist; they do not establish a final claim.",
        "Held-out evidence decides: if the gate is insufficient, the benchmark remains the final answer.",
    ], "The pipeline makes that distinction between proposal and evidence explicit."),
    "pipeline_architecture": ("Layer 6 · Thesis GA Architecture", "Final thesis methods; defense implementation slides", [
        ("HELP", [
            "Layer 5 showed the intuition of evolutionary search; this view shows the actual GA architecture used in the thesis.",
            "Monte Carlo first evaluates every named base estimator across replications and stores those outputs in matrix C.",
            "A candidate is scored by the fast matrix-vector product Cw, so the GA searches only the simplex weight vector w rather than raw observations.",
            "The final multiseed design uses population N=100, 20 generations per fold, three folds, and search seeds 101 and 202.",
            "Dirichlet initialization, convex crossover and Dirichlet-nudge mutation preserve simplex validity; elitism and immigration protect useful solutions and diversity.",
            "Fitness guides where the GA searches, but a candidate becomes evidence only after its weights are frozen and the held-out dual benchmark gate is applied.",
        ]),
        ("POSSIBLE QUESTIONS", [
            ("Why build matrix C?", "It separates estimator evaluation from evolutionary search. Each column is a known estimator across Monte Carlo replications, so each candidate can be evaluated as the auditable product Cw."),
            ("How do you keep every GA individual valid?", "Initialization draws directly from a Dirichlet distribution, crossover is convex, and mutation nudges toward another Dirichlet draw; the operators therefore preserve non-negative weights that sum to one."),
            ("What is the role of warm starts?", "Confirmed prior vectors may enter the expanded search with preserved provenance, but they receive no fitness bonus and no automatic acceptance."),
            ("Why separate fitness from the gate?", "Fitness is an optimization signal. The gate is an evidential decision rule on held-out data. Keeping them separate prevents a discovery optimum from becoming an automatic scientific claim."),
            ("What prevents premature convergence?", "Elitism protects strong candidates while periodic immigration injects fresh Dirichlet draws; mutation also preserves exploration."),
        ]),
    ], "Now place that search engine inside the staged evidentiary programme."),
    "pipeline_stage_0": ("Layer 6 · Stage 1 — Initial Discovery", "Final thesis discovery sequence", [
        ("HELP", [
            "The initial discovery GA learns over 10 estimator components.",
            "HPF1 exposes candidates to 60% of the scenario grid; HPF2 increases exposure to 80%.",
            "Specialist halving concentrates computation on the most promising regimes before the internal held-out discovery gate.",
            "Search seeds are 101 and 202, and the gate evaluates the top five finalists without post-hoc retraining.",
            "A Stage-1 pass is a discovery candidate, not the final evidential claim.",
        ]),
        ("POSSIBLE QUESTIONS", [("Why 60% then 80%?", "Multi-fidelity screening removes weak configurations cheaply before allocating more scenario exposure to promising signals."), ("Why call this discovery rather than validation?", "The weights are still being optimized inside this cycle. Independent fixed-weight confirmation begins only after discovery ends.")]),
    ], "Freeze the discovered vector before stronger confirmation pressure."),
    "pipeline_stage_1": ("Layer 6 · Stage 2 — Frozen Confirmation I", "Final thesis fixed-weight confirmation", [
        ("HELP", [
            "The selected 10-component discovery vector is frozen and the GA is not rerun.",
            "The candidate now faces 26 modern comparators, eight new validation seeds, and both original and locked-unseen related regimes.",
            "Precision rises to R=500 Monte Carlo replicates and B=500 paired bootstrap replicates.",
            "This stage asks whether the discovered estimator itself survives stronger pressure when adaptation is impossible.",
        ]),
        ("POSSIBLE QUESTIONS", [("Why freeze the weights?", "Freezing prevents the candidate from adapting to the confirmation data, separating estimator evidence from search-cell artifacts."), ("Why introduce 26 estimators here if only 10 were learnable?", "At this stage the modern estimators are comparators only. They become learnable later when discovery is deliberately reopened.")]),
    ], "Only confirmed evidence may become a protected prior in rediscovery."),
    "pipeline_stage_2": ("Layer 6 · Stage 3 — Expanded Rediscovery", "Final thesis expanded-basis design", [
        ("HELP", [
            "Discovery is reopened with all 26 estimator components learnable from HPF1 onward.",
            "HPF1 remains at 60% scenario exposure, while HPF2 increases from 80% to 90%.",
            "The expanded modern benchmark gate is active from the start rather than appearing only after discovery.",
            "CV-019 and CV-010 enter as protected warm starts because they passed the earlier fixed-weight confirmation.",
            "Their provenance is preserved, but they receive no fitness bonus and must compete again under the 26-component design.",
        ]),
        ("POSSIBLE QUESTIONS", [("Why reopen the GA?", "This tests whether modern robust pressure changes what can be discovered when those estimators are inside the learnable basis from the beginning."), ("Do CV-019 and CV-010 get an unfair advantage?", "No. They are controlled starting priors only; they must re-survive the same fitness and gate logic as other candidates.")]),
    ], "Freeze the expanded candidates again before testing their evidential scope."),
    "pipeline_stage_3": ("Layer 6 · Stage 4 — Frozen Validation II", "Final thesis post-discovery fixed-weight validation", [
        ("HELP", [
            "The 26-component candidates are frozen after expanded rediscovery; no adaptation is allowed during this stage.",
            "Each candidate is tested on its original regime and on locked-unseen related regimes.",
            "Paired bootstrap evidence and the dual benchmark gate constrain the final interpretation.",
            "The evidence taxonomy distinguishes transfer specialists, local evidence, near-gate candidates, and benchmark-retained cases.",
        ]),
        ("POSSIBLE QUESTIONS", [("What does locked-unseen mean?", "It is a structurally related regime that was unavailable during the discovery cycle, so it tests transfer without allowing retraining."), ("Why use an evidence taxonomy?", "The gate decision is binary, but the taxonomy records how broad or local the supported evidence is without changing the gate itself.")]),
    ], "Move from controlled synthetic evidence to external calibration and abstention audit."),
    "pipeline_stage_4": ("Layer 6 · Stage 5 — External Evidence + Audit", "Final thesis real-world battery and Dirichlet audit", [
        ("HELP", [
            "The real-world battery requested 264 datasets/targets, loaded 228, evaluated 120, and retained 43 as eligible parent datasets.",
            "Frozen specialists are applied without reoptimization; 26 of the 43 eligible parent datasets produced at least one corrected win, with 255 profile-matched confirmations surviving FDR control.",
            "The Dirichlet audit is a separate abstention check, not another discovery stage.",
            "It evaluates 4,000 random simplex vectors across eight audit seeds in benchmark-retained regimes.",
            "The audit found 23 of 34 regimes with no random pass, 11 of 34 with some signal, and all 8 strongest positive controls passing.",
        ]),
        ("POSSIBLE QUESTIONS", [("Why is the real-data layer calibration rather than known-theta validation?", "Real data do not reveal the population mean, so the full-sample mean is an empirical reference rather than population ground truth."), ("What does the Dirichlet audit test?", "It asks whether arbitrary simplex mixtures expose signal in regimes where the selected GA candidate abstained; it does not rerun or replace the GA."), ("Are the 255 confirmations 255 independent datasets?", "No. Breadth is represented by the 43 eligible parent datasets; the 255 results are profile-matched repeated confirmations within that external battery.")]),
    ], "Now inspect the precomputed thesis results that survived this programme."),
    "results": ("Layer 7 · Results journey", "Defense deck · Results: strict validation and transfer/audit", [
        "Use the selected result stage to make a bounded claim. Stronger validation narrows broad discovery signals to local specialists.",
        "The essential conclusion is evidence conditional on profile, not a universal GA winner.",
    ], "Now synthesize what the evidence means before opening the technical backup."),
    "conclusions": ("Layer 8 · Conclusions", "Defense script map · closing message", [
        "The GA proposes candidate mixtures; held-out and fixed-weight evidence decides what survives.",
        "The contribution is an auditable way to identify conditional opportunity and retain the benchmark when support is insufficient.",
    ], "Technical drill-down remains available as backup for committee questions."),
    "technical": ("Layer 9 · Technical drill-down", "Thesis abstract; defense deck · strict validation", [
        "Read the displayed decision as fixed-weight evidence; do not treat a discovery pass as confirmation.",
        "Bootstrap intervals, unseen-similar regimes and evidence taxonomy constrain the interpretation.",
    ], "Use this backup when the committee asks for candidate-level evidence."),
}


# Formula cards mirror the notation shown in each defense view.  They are kept
# separate from the speaking bullets so every formula can be decomposed cleanly
# without making HELP difficult to scan during the defense.
PRESENTER_FORMULA_CARDS = {
    "research_problem": [
        ("REGIME", "ℛ = (F₀, γ, c, m, n)", [
            "ℛ = the complete data-generating regime.",
            "F₀ = baseline distribution family.",
            "γ = contamination rate.",
            "c = contamination severity / outlier scale.",
            "m = contamination mechanism.",
            "n = sample size.",
        ]),
        ("INDUCED DISTRIBUTION", "F_ℛ = (1−γ)F₀ + γG_{m,c}(F₀)", [
            "F_ℛ = distribution actually used to generate samples in regime ℛ.",
            "(1−γ)F₀ = uncontaminated share of the observations.",
            "γG_{m,c}(F₀) = contaminated share produced by mechanism m at severity c.",
        ]),
        ("FIXED TARGET", "θ(F) = μ_F = E_F[X]", [
            "θ(F) = target functional.",
            "μ_F = population mean under F.",
            "E_F[X] = expectation of X under F.",
            "The estimand stays fixed even when the regime changes.",
        ]),
    ],
    "research_objective": [
        ("COMPOSITE CANDIDATE", "θ̂_{w,n} = Σⱼ₌₁ᴸ wⱼTⱼ,n", [
            "Tⱼ,n = jth named base estimator at sample size n.",
            "wⱼ = weight assigned to component j.",
            "L = number of learnable estimators.",
            "The GA searches the weights; it does not change the target.",
        ]),
        ("SIMPLEX SEARCH SPACE", "w ∈ Δ_L,  Δ_L = {w ∈ [0,1]ᴸ : Σⱼwⱼ = 1}", [
            "wⱼ ≥ 0 = no negative component contribution.",
            "Σⱼwⱼ = 1 = all weights sum to 100%.",
            "Δ_L = set of all valid convex weight recipes.",
        ]),
        ("DUAL BENCHMARK GATE", "Δ_MSE ≥ 0  AND  Δ_q95 ≥ 0", [
            "Δ_MSE = benchmark MSE minus candidate MSE.",
            "Δ_q95 = benchmark q95(MSE) minus candidate q95(MSE).",
            "Both must support replacement; one metric alone is insufficient.",
        ]),
    ],
    "research_hypotheses": [
        ("HYPOTHESIS CHAIN", "H1 → H2 → H3 → H4", [
            "H1 = no universal estimator.",
            "H2 = finite-sample performance depends on the regime.",
            "H3 = GA opportunity should be selective, not universal.",
            "H4 = the benchmark gate controls the final claim.",
        ]),
        ("CONDITIONAL RISK", "R_{F,n}(T_n) = E_F[(T_n − μ_F)²]", [
            "R_{F,n} = finite-sample squared-error risk under F and n.",
            "T_n = estimator being evaluated.",
            "μ_F = fixed population-mean target.",
            "Changing F or n can change the estimator ranking.",
        ]),
    ],
    "research_target": [
        ("TARGET", "θ(F) = μ_F = E_F[X]", [
            "θ(F) = estimand defined by the distribution F.",
            "μ_F = population mean.",
            "E_F[X] = expected value of X under F.",
        ]),
        ("COMPOSITE ESTIMATOR", "θ̂_{w,n} = Σⱼ₌₁ᴸ wⱼTⱼ,n", [
            "θ̂_{w,n} = composite estimate produced by one weight recipe.",
            "Tⱼ,n = named component estimator.",
            "wⱼ = its non-negative contribution.",
        ]),
        ("SIMPLEX", "w ∈ Δ_L = {w ∈ [0,1]ᴸ : Σⱼwⱼ = 1}", [
            "Every weight is between 0 and 1.",
            "All weights sum to one.",
            "This keeps the recipe interpretable as a convex mixture.",
        ]),
    ],
    "research_why_win": [
        ("MSE DECOMPOSITION", "MSE_{F,n}(θ̂_{w,n}) = B_n(w,F)² + V_n(w,F)", [
            "MSE = total finite-sample squared-error risk.",
            "B_n(w,F)² = squared bias cost.",
            "V_n(w,F) = sampling variance.",
        ]),
        ("BIAS", "B_n(w,F) = Σⱼwⱼ{E_F[Tⱼ,n] − μ_F}", [
            "E_F[Tⱼ,n] − μ_F = bias of component j.",
            "wⱼ = amount of that component entering the mixture.",
            "The composite bias is the weighted combination of component biases.",
        ]),
        ("DOMINANCE OVER THE SAMPLE MEAN", "B_n(w,F)² + V_n(w,F) < Var_F(X̄_n)", [
            "Left side = composite MSE.",
            "Right side = sample-mean variance when the mean is unbiased.",
            "The mixture wins only if variance reduction exceeds the squared-bias cost.",
        ]),
    ],
    "data_world": [
        ("REGIME", "ℛ = (F₀, γ, c, m, n)", [
            "F₀ = baseline family.",
            "γ = contamination rate.",
            "c = contamination severity.",
            "m = contamination mechanism.",
            "n = sample size.",
        ]),
        ("SAMPLING DISTRIBUTION", "F_ℛ = (1−γ)F₀ + γG_{m,c}(F₀)", [
            "F_ℛ is the complete synthetic world for one regime.",
            "The first term represents clean observations.",
            "The second term injects the specified contamination.",
        ]),
        ("KNOWN SYNTHETIC TARGET", "θ(F_ℛ) = E_{F_ℛ}[X]", [
            "Simulation gives access to the population-generating law.",
            "Therefore the true target is known before an estimator is scored.",
        ]),
    ],
    "data_world_families": [
        ("BASELINE FAMILY", "F₀ ∈ {Normal, Lognormal, Weibull, IG, Ex-Gaussian, Ex-Wald}", [
            "F₀ = baseline distribution family for the regime.",
            "Normal = symmetric baseline.",
            "Lognormal = positive right-skew.",
            "Weibull = flexible survival-like positive shape.",
            "IG = Inverse Gaussian, an asymmetric duration family.",
            "Ex-Gaussian = reaction-time-like skew plus exponential tail.",
            "Ex-Wald = first-passage positive process.",
        ]),
        ("POPULATION-MEAN TARGET", "θ(F) = μ_F = E_F[X]", [
            "θ(F) = target functional under distribution F.",
            "μ_F = population mean under that family/regime.",
            "E_F[X] = expectation of X under F.",
            "The family changes the risk environment, not the type of estimand being targeted.",
        ]),
    ],
    "data_world_certification": [
        ("VALIDATION SUMMARY", "125 checks · 0 hard failures · 29 warnings", [
            "125 = validation conditions reviewed before GA evidence is trusted.",
            "0 = no hard validation failure.",
            "29 = explainable diagnostic warnings retained for transparency.",
        ]),
        ("MOMENT FIDELITY", "relative mean error = |μ̂ − μ| / |μ|", [
            "μ̂ = empirical mean from a large generated population.",
            "μ = analytic mean implied by the generating distribution.",
            "The reported maximum mean error was 0.976%, below the 1% hard threshold.",
        ]),
        ("CONTAMINATION FIDELITY", "γ̂ ≈ γ", [
            "γ = designed contamination rate.",
            "γ̂ = realised contamination rate after injection.",
            "Direction and MAD-based distance are checked alongside the rate.",
        ]),
    ],
    "simulation_lab": [
        ("ONE GENERATED SAMPLE", "X₁,…,X_n ∼ F_ℛ", [
            "X₁,…,X_n = observations in the displayed sample.",
            "F_ℛ = selected data-generating regime.",
            "This view illustrates one draw, not repeated-sampling evidence.",
        ]),
        ("ESTIMATION ERROR", "e(T_n) = T_n(X₁:ₙ) − μ_F", [
            "T_n(X₁:ₙ) = estimator computed from the visible sample.",
            "μ_F = known synthetic target.",
            "Changing the regime can change the direction and size of this error.",
        ]),
    ],
    "monte_carlo_engine": [
        ("REPLICATE SQUARED ERROR", "e²_{j,r} = (T_{j,n}(X^{(r)}) − μ_F)²", [
            "r = Monte Carlo replication.",
            "j = estimator index.",
            "T_{j,n}(X^{(r)}) = estimate from replicate r.",
            "μ_F = known population target.",
        ]),
        ("MONTE CARLO MSE", "MSÊ_j = (1/B) Σᵣ₌₁ᴮ e²_{j,r}", [
            "B = number of Monte Carlo replicates.",
            "e²_{j,r} = squared error in replicate r.",
            "The average estimates typical finite-sample risk.",
        ]),
        ("DIFFICULT-CASE METRIC", "q₀.₉₅({e²_{j,r}})", [
            "q₀.₉₅ = 95th percentile of replicate squared errors.",
            "It measures difficult-case behaviour rather than only the average.",
        ]),
    ],
    "monte_carlo_validation_0": [
        ("MOMENT FIDELITY", "X̄_N ≈ E_F[X]  for large N", [
            "X̄_N = empirical mean of a very large generated population.",
            "E_F[X] = analytic population mean.",
            "Agreement checks that the simulator recovers the intended target.",
        ]),
    ],
    "monte_carlo_validation_1": [
        ("REALIZED CONTAMINATION RATE", "γ̂ = N_out / n", [
            "N_out = generated contaminated observations.",
            "n = total observations.",
            "γ̂ should track the declared contamination rate γ.",
        ]),
    ],
    "monte_carlo_validation_2": [
        ("NORMAL-THEORY SANITY CHECK", "MSE_F(X̄_n) < MSE_F(Median_n)", [
            "Under clean Normal data, the sample mean is the efficient reference.",
            "Recovering the expected ordering checks the scoring pipeline.",
            "This validates measurement logic; it is not a GA result.",
        ]),
    ],
    "monte_carlo_validation_3": [
        ("EMPIRICAL REFERENCE MEAN", "μ_ref = (1/N) Σᵢ₌₁ᴺ xᵢ", [
            "N = size of the complete empirical dataset.",
            "μ_ref = full-sample empirical reference mean.",
            "It is useful for calibration but is not known population truth.",
        ]),
    ],
    "ga_search": [
        ("GA INDIVIDUAL", "w = (w₁,…,w_L) ∈ Δ_L", [
            "Each chromosome is a complete estimator-weight recipe.",
            "wⱼ ≥ 0 for every component.",
            "Σⱼwⱼ = 1 keeps the chromosome on the simplex.",
        ]),
        ("COMPOSITE", "θ̂_{w,n} = ΣⱼwⱼTⱼ,n", [
            "The chromosome becomes a statistical estimator through this weighted sum.",
            "Named components remain inspectable after evolution.",
        ]),
        ("GATE", "Δ_MSE ≥ 0  AND  Δ_q95 ≥ 0", [
            "Positive Δ means the candidate has lower error than the benchmark.",
            "Both average and difficult-case criteria must support replacement.",
            "Otherwise the benchmark is retained.",
        ]),
    ],
    "pipeline_architecture": [
        ("ESTIMATOR OUTPUT MATRIX", "C = [T_j(x^(r))]", [
            "r = Monte Carlo replication (row).",
            "j = named base estimator (column).",
            "C stores estimator outputs before the GA changes any weights.",
        ]),
        ("FAST COMPOSITE SCORING", "T_mix = Cw", [
            "w = simplex-constrained candidate weight vector.",
            "Cw = composite estimates across all stored replications.",
            "The GA therefore searches weights, not raw observations.",
        ]),
        ("DIRICHLET INITIALIZATION", "w^(0) ~ Dirichlet(α·1_L)", [
            "α ∈ {0.5, 1.0} in the final search grid.",
            "Dirichlet draws are non-negative and sum to one by construction.",
        ]),
        ("CONVEX CROSSOVER", "child = λ p_A + (1−λ) p_B,  λ ~ U(0,1)", [
            "p_A and p_B = valid parent weight vectors.",
            "0 ≤ λ ≤ 1 keeps the offspring inside the simplex.",
        ]),
        ("DIRICHLET-NUDGE MUTATION", "z ~ Dirichlet(α_mut·1_L);  child' = (1−ρ)child + ρz", [
            "z = fresh simplex-valid direction.",
            "ρ controls the mutation nudge toward z.",
            "The mutation probability follows a log-decay schedule with μ₀ ∈ {0.12,0.18} and μ_min = 0.05.",
        ]),
        ("SEARCH FITNESS", "F(w) = 0.70·q95 + 0.30·max-loss + regularisation", [
            "The displayed weights summarize the principal tail-risk mixture in the final configuration.",
            "Additional penalties control instability, collapse, bias to θ, dominance, and benchmark pressure.",
            "Fitness ranks candidates during optimization; it is not the final acceptance rule.",
        ]),
        ("HELD-OUT DUAL GATE", "Δ_MSE ≥ 0  AND  Δ_q95 ≥ 0", [
            "Both criteria must favour the candidate on held-out evidence.",
            "Failure of either criterion means benchmark retention.",
        ]),
    ],
    "pipeline_stage_0": [
        ("MULTI-FIDELITY EXPOSURE", "HPF1: 60%  →  HPF2: 80%", ["HPF1 is the broad low-cost screen.", "HPF2 gives surviving configuration-regime signals more scenario exposure.", "Specialist halving then concentrates the remaining budget before the held-out discovery gate."]),
    ],
    "pipeline_stage_1": [
        ("FROZEN-WEIGHT PRINCIPLE", "w*_{discovery} → freeze(w*) → confirmation", ["The discovery recipe is fixed before confirmation.", "No further GA optimization is allowed.", "The same fixed vector faces stronger comparators and new seeds."]),
        ("CONFIRMATION PRECISION", "R = 500,  B = 500", ["R = Monte Carlo replicates per validation condition.", "B = paired bootstrap resamples used to quantify gain uncertainty."]),
    ],
    "pipeline_stage_2": [
        ("EXPANDED SEARCH SPACE", "10 learnable → 26 learnable", ["Modern robust estimators become part of the GA basis from HPF1.", "The benchmark gate is also modern from the beginning of rediscovery."]),
        ("EXPANDED EXPOSURE", "HPF1: 60%  →  HPF2: 90%", ["HPF1 keeps the same broad-screen role.", "HPF2 receives greater exposure than in the initial discovery cycle."]),
    ],
    "pipeline_stage_3": [
        ("SECOND FREEZE", "w*_{26} → original + locked-unseen validation", ["w*_{26} = candidate learned in expanded rediscovery.", "Both validation modes use the exact frozen vector.", "No adaptation occurs after the second discovery cycle closes."]),
    ],
    "pipeline_stage_4": [
        ("REAL-WORLD FUNNEL", "264 → 228 → 120 → 43", ["264 = requested targets/datasets in the external battery.", "228 = successfully loaded.", "120 = evaluated after preparation and profile logic.", "43 = eligible parent datasets used for the main parent-level evidence summary."]),
        ("DIRICHLET AUDIT", "4,000 random vectors × 8 seeds", ["Random simplex vectors are tested in benchmark-retained regimes.", "This is an abstention audit rather than a new GA search."]),
    ],
    "results": [
        ("RELATIVE GAIN", "Gain% = 100 × (MSE_b − MSE_c) / MSE_b", [
            "MSE_b = benchmark error.",
            "MSE_c = frozen candidate error.",
            "Positive gain means lower candidate MSE.",
            "The same interpretation is applied separately to q95(MSE).",
        ]),
        ("CONFIRMATION RULE", "CI(Δ) > 0", [
            "Δ = benchmark minus candidate gain measure.",
            "CI(Δ) = bootstrap confidence interval for that gain.",
            "A clearly positive interval supports a bounded confirmation claim.",
        ]),
    ],
    "technical": [
        ("RELATIVE GAIN", "Gain% = 100 × (R_b − R_c) / R_b", [
            "R_b = criterion-specific benchmark risk.",
            "R_c = frozen candidate risk.",
            "Positive values favour the candidate.",
        ]),
        ("BOOTSTRAP EVIDENCE", "CI_boot(Δ)", [
            "Δ = observed benchmark-minus-candidate gain.",
            "CI_boot = bootstrap interval quantifying uncertainty around Δ.",
            "Intervals crossing zero weaken the replacement claim.",
        ]),
        ("DUAL GATE", "Δ_MSE ≥ 0  AND  Δ_q95 ≥ 0", [
            "The mean-risk criterion protects average performance.",
            "The q95 criterion protects difficult-case performance.",
            "Both are required for the intended benchmark-gated claim.",
        ]),
    ],
}

_query = st.query_params
_browser_note = PRESENTER_NOTES.get(_query.get("section", "")) if _query.get("presenter_notes") == "1" else None
st.set_page_config(page_title=_browser_note[0] if _browser_note else "Robust Estimators Lab", page_icon="📊", layout="wide")
pio.templates.default = "plotly_dark"
st.markdown("""<style>
.stApp{background:radial-gradient(circle at 48% -12%,#16365c 0,#08172a 35%,#040a14 76%)!important;color:#eef5ff}.block-container{padding:.45rem 2rem 3rem!important;max-width:none!important}.stMetric{background:linear-gradient(135deg,#0d2038,#081525)!important;border:1px solid #218dca!important;border-top:3px solid #9a5cff!important;border-radius:7px;padding:10px;box-shadow:inset 0 0 18px rgba(33,141,202,.08)}.stMetric label,.stMetric [data-testid="stMetricLabel"]{color:#b8c8de!important}.stMetric [data-testid="stMetricValue"]{color:#f5f8ff!important}.badge{padding:6px 10px;border-radius:6px;font-size:.78rem;font-weight:800;display:inline-block;letter-spacing:.03em}.demo{background:#28184c;color:#d7c3ff;border:1px solid #8759de}.thesis{background:#0b372d;color:#9df0b7;border:1px solid #3aaf6f}
h1{color:#f5f8ff!important;margin:0 0 .1rem!important;font-size:2rem!important;text-shadow:0 0 18px rgba(71,169,255,.34)}h2,h3{color:#f2f7ff!important}[data-testid="stCaptionContainer"],.stCaption{color:#aebed3!important}[data-baseweb="tab-list"]{border-bottom:1px solid #2374b4!important;box-shadow:none!important;margin-top:.25rem!important;gap:.4rem}[data-baseweb="tab-border"]{display:none!important}[data-testid="stTabs"]>div:first-child{border-bottom:0!important}[data-baseweb="tab"]{color:#aebed3!important;background:#0a1930!important;border:1px solid #1d5688!important;border-bottom:0!important;border-radius:6px 6px 0 0!important;font-weight:700!important}[aria-selected="true"][data-baseweb="tab"]{color:#f6fbff!important;background:#102a49!important;box-shadow:inset 0 2px #4fc3ff!important}.layer-heading{font-size:1.3rem;font-weight:800;color:#f5f8ff;margin:.3rem 0 .1rem;text-shadow:0 0 14px rgba(79,195,255,.25)}.layer-subheading{color:#aebed3;margin:0 0 .75rem}.scenario-panel{border:1px solid #237fc0;border-left:4px solid #4fc3ff;border-radius:7px;background:linear-gradient(135deg,#0e2743,#081626);padding:.8rem 1rem;margin:.45rem 0 .8rem;color:#e8f3ff}.independent-note{color:#aebed3;font-size:.86rem;border-top:1px solid #20517e;padding-top:.65rem;margin-top:.35rem}.metric-caption{font-size:.78rem;color:#aebed3;margin-top:-.4rem}
div[data-testid="stVerticalBlockBorderWrapper"],div[data-testid="stExpander"]{border-color:#236b9e!important;background:#08182b!important}.stButton>button{background:linear-gradient(135deg,#5931bd,#2575bb)!important;color:#fff!important;border:1px solid #62c7ff!important;border-radius:6px!important;font-weight:700}.stSelectbox label,.stSlider label,.stNumberInput label,.stRadio label{color:#dceaff!important}.stAlert{background:#102a49!important;border:1px solid #287db5!important;color:#e7f4ff!important}.js-plotly-plot .plotly .modebar{background:#102541!important}
.pipeline-stage{min-height:136px;padding:14px 12px;border:1px solid #2b668f;border-radius:9px;background:#0a1b30;color:#b9cae0}.pipeline-stage.active{background:linear-gradient(135deg,#203d67,#152b48);border:2px solid #f3c743;box-shadow:0 0 20px rgba(243,199,67,.22);color:#f6fbff}.pipeline-step{font-size:11px;font-weight:800;letter-spacing:.08em;color:#72cfff}.pipeline-title{font-size:16px;font-weight:800;margin:8px 0}.pipeline-mini{font-size:12px;line-height:1.35}.story-panel{min-height:245px;padding:24px;border:1px solid #367eaf;border-radius:10px;background:linear-gradient(135deg,#0d2642,#08182b)}.story-kicker{font-size:12px;font-weight:800;letter-spacing:.1em;color:#72cfff}.story-title{font-size:28px;font-weight:800;color:#f5f8ff;margin:8px 0 16px}.story-label{font-size:12px;font-weight:800;letter-spacing:.08em;color:#f3c743;margin-bottom:6px}.story-body{font-size:16px;line-height:1.48;color:#dbe9f7}.funnel-step{padding:10px 14px;margin:6px auto;border:1px solid #3c79a5;border-radius:6px;background:#0d2642;color:#dceaff;text-align:center;font-weight:700}.funnel-step.active{border-color:#4de080;color:#c8ffd7;background:#123d30}
[data-testid="stSidebar"]{min-width:215px!important;max-width:215px!important;background:#071525!important;border-right:1px solid #245f8e}[data-testid="stSidebar"] [data-testid="stRadio"] label{font-size:.78rem!important;line-height:1.15!important;padding:.18rem 0!important}
</style>""", unsafe_allow_html=True)

# Presenter view: every note is rendered as a large, scan-friendly cue card.
# It accepts both the structured Layer-1 format and the simpler bullet lists
# used by later layers.
if _query.get("presenter_notes") == "1":
    import html as _html
    import re as _re

    note_section = _query.get("section", "")
    note = PRESENTER_NOTES.get(note_section)
    if note:
        _heading, _source, talking_points, _transition = note

        def _sentence_bullets(copy):
            if isinstance(copy, (list, tuple)):
                return [str(item).strip() for item in copy if str(item).strip()]
            text_value = str(copy).strip()
            if not text_value:
                return []
            return [part.strip() for part in _re.split(r"(?<=[.!?])\s+", text_value) if part.strip()]

        def _bullets(items, css_class=""):
            return "<ul class=\"%s\">%s</ul>" % (
                css_class,
                "".join(f"<li>{_html.escape(str(item))}</li>" for item in items),
            )

        def _render_formula_cards(cards):
            output = []
            for title, formula, parts in cards:
                output.append(
                    '<div class="formula-card">'
                    f'<div class="formula-label">{_html.escape(title)}</div>'
                    f'<div class="formula-expression">{_html.escape(formula)}</div>'
                    f'{_bullets(parts, "formula-parts")}'
                    '</div>'
                )
            return (
                '<section class="presenter-section">'
                '<h2>FORMULAS AND NOTATION</h2>'
                + "".join(output)
                + '</section>'
            )

        def _render_presenter_section(label, copy):
            if label == "HELP":
                return (
                    '<section class="presenter-section presenter-help"><h2>HELP</h2>'
                    + _bullets(_sentence_bullets(copy), "help-bullets")
                    + '</section>'
                )
            if label == "FORMULAS AND NOTATION":
                # Formula content is rendered below from PRESENTER_FORMULA_CARDS,
                # where each expression has an explicit symbol-by-symbol breakdown.
                return ""
            if label == "POSSIBLE QUESTIONS":
                content = "".join(
                    '<li><strong>%s</strong><ul><li>%s</li></ul></li>'
                    % (_html.escape(question), _html.escape(answer))
                    for question, answer in copy
                )
                return f'<section class="presenter-section"><h2>{label}</h2><ul>{content}</ul></section>'
            if isinstance(copy, (list, tuple)):
                return f'<section class="presenter-section"><h2>{_html.escape(label)}</h2>{_bullets(copy)}</section>'
            return f'<section class="presenter-section"><h2>{_html.escape(label)}</h2><p>{_html.escape(str(copy))}</p></section>'

        # Structured Layer-1 notes already contain labelled sections.  Later
        # layers are converted automatically into a HELP section.
        if all(isinstance(item, (list, tuple)) and len(item) == 2 for item in talking_points):
            presenter_sections = list(talking_points)
        else:
            presenter_sections = [("HELP", list(talking_points))]

        notes_html = "".join(_render_presenter_section(label, copy) for label, copy in presenter_sections)
        formula_cards_for_view = PRESENTER_FORMULA_CARDS.get(note_section, [])
        if formula_cards_for_view:
            # Put formulas after HELP and before questions whenever possible.
            question_marker = '<section class="presenter-section"><h2>POSSIBLE QUESTIONS</h2>'
            formula_html = _render_formula_cards(formula_cards_for_view)
            if question_marker in notes_html:
                notes_html = notes_html.replace(question_marker, formula_html + question_marker, 1)
            else:
                notes_html += formula_html

        st.markdown(f'''<style>
          [data-testid="stAppViewContainer"]{{background:#071525!important}}
          .block-container{{max-width:1260px!important;padding:2.6rem 3.4rem!important}}
          .presenter-heading{{font-family:Arial,sans-serif;font-size:2.35rem;font-weight:800;line-height:1.18;color:#72cfff;margin:0 0 2.35rem}}
          .presenter-copy{{font-family:Arial,sans-serif;font-size:1.62rem;line-height:1.52;color:#f4f8ff}}
          .presenter-section{{margin:0 0 3rem}}
          .presenter-section h2{{font-size:1.22rem!important;letter-spacing:.12em;color:#72cfff!important;margin:0 0 1rem!important}}
          .presenter-section p{{margin:0}}
          .presenter-section ul{{margin:.15rem 0 0 1.5rem;padding:0}}
          .presenter-section li{{margin:0 0 .9rem;padding-left:.22rem}}
          .presenter-section li::marker{{color:#f3c743}}
          .presenter-section li ul{{margin:.55rem 0 .2rem 1.45rem;color:#c6d8e9;font-size:1.35rem}}
          .help-bullets li{{margin-bottom:1.05rem}}
          .formula-card{{background:#0b2138;border:1px solid #356e99;border-left:5px solid #f3c743;border-radius:12px;padding:1.25rem 1.45rem;margin:0 0 1.35rem}}
          .formula-label{{font-size:1rem;font-weight:800;letter-spacing:.1em;color:#72cfff;margin-bottom:.55rem}}
          .formula-expression{{font-family:Georgia,serif;font-size:1.82rem;font-weight:700;color:#f7d768;line-height:1.35;margin-bottom:.85rem}}
          .formula-parts{{font-size:1.28rem!important;line-height:1.45;color:#dce9f8}}
          .formula-parts li{{margin-bottom:.5rem}}
        </style><div class="presenter-heading">{_html.escape(_heading)}</div><div class="presenter-copy">{notes_html}</div>''', unsafe_allow_html=True)
    else:
        st.warning("No hay notas configuradas para esta vista todavía.")
    st.stop()


st.title("Robust Estimators Lab")
st.caption("Defense Mode · a visual thesis narrative for robust estimator mixtures")

# Deliberate guardrail from the defense redesign: these two live demonstrations
# are approved teaching components. Do not change their visuals, data logic,
# controls, or playback except for navigation and truly global styling.
FROZEN_COMPONENTS = ("Layer 6 · Build the problem", "Layer 7 · GA search")

@st.cache_data(show_spinner="Building the pedagogical GA landscape…")
def build_layer2_demo(family, contamination, contamination_rate, outlier_scale, mutation_rate, population_size, lens, seed, renderer_version):
    """The terrain and GA share one artificial objective, changed by UI controls."""
    terrain = simplex_renderer.teaching_terrain(family, contamination, contamination_rate, outlier_scale, 0., lens)
    objective = lambda weights: simplex_renderer.demo_objective(weights[:, 0], weights[:, 1], weights[:, 2], terrain)
    # Eight real generations keep the defense animation concise while allowing
    # every generation to dwell on its five recorded GA operations.
    run = run_pedagogical_ga(objective, MiniGAConfig(population_size=population_size, generations=8, mutation_rate=mutation_rate, seed=seed))
    return {"run": run, "terrain": terrain}

DEFENSE_INDEX = (
    "00 · Cover", "01 · Research logic", "02 · Data-generating world", "03 · Simulation lab",
    "04 · Monte Carlo engine", "05 · GA search", "06 · Experiment pipeline", "07 · Results journey",
    "08 · Conclusions", "09 · Technical drill-down",
)

def _navigate(index):
    st.session_state.defense_section = DEFENSE_INDEX[max(0, min(index, len(DEFENSE_INDEX) - 1))]


def _set_presenter_state(key, value):
    """Set a view before the sidebar is rendered during Streamlit's rerun."""
    st.session_state[key] = value


def _presenter_note_key(active_section: str) -> str:
    """Resolve the exact speaking note for the currently visible defense view."""
    fixed = {
        "00 · Cover": "cover", "03 · Simulation lab": "simulation_lab", "05 · GA search": "ga_search",
        "07 · Results journey": "results", "08 · Conclusions": "conclusions", "09 · Technical drill-down": "technical",
    }
    if active_section == "01 · Research logic":
        keys = ("research_problem", "research_objective", "research_hypotheses", "research_target", "research_why_win")
        return keys[int(st.session_state.get("research_panel", 0))]
    if active_section == "02 · Data-generating world":
        keys = ("data_world", "data_world_families", "data_world_certification")
        return keys[int(st.session_state.get("data_world_view", 0))]
    if active_section == "04 · Monte Carlo engine":
        if st.session_state.get("monte_carlo_view", "engine") == "validation":
            return f"monte_carlo_validation_{int(st.session_state.get('validation_stage', 0))}"
        return "monte_carlo_engine"
    if active_section == "06 · Experiment pipeline":
        if st.session_state.get("layer6_view", "architecture") == "architecture":
            return "pipeline_architecture"
        return f"pipeline_stage_{int(st.session_state.get('story_stage', 0))}"
    return fixed[active_section]


def _presenter_notes_link(section: str) -> str:
    """Open and then reuse one movable presenter-notes browser window."""
    return f'''<a href="?presenter_notes=1&amp;section={section}"
        title="Open presenter notes in the presenter window" style="display:block;margin-top:1.4rem"
        onclick="const n=window.open(this.href, 'robust_estimators_presenter_notes', 'popup=yes,width=980,height=780,resizable=yes,scrollbars=yes'); if(n){{n.focus();}} return false;">
      <img src="{UNIVERSITY_LOGO_DATA_URI}" alt="University of Hull"
           style="display:block;width:100%;box-sizing:border-box;border-radius:6px;border:1px solid #245f8e;padding:4px;background:#fff" />
    </a>'''

with st.sidebar:
    st.markdown("### DEFENSE MODE")
    st.caption("Manual presentation index · live layers are preserved")
    active_section = st.radio("Defense section", DEFENSE_INDEX, label_visibility="collapsed", key="defense_section")
    position = DEFENSE_INDEX.index(active_section)
    previous, following = st.columns(2)
    previous.button("← Previous", use_container_width=True, disabled=position == 0, on_click=_navigate, args=(position - 1,))
    following.button("Next →", use_container_width=True, disabled=position == len(DEFENSE_INDEX) - 1, on_click=_navigate, args=(position + 1,))
    st.markdown(_presenter_notes_link(_presenter_note_key(active_section)), unsafe_allow_html=True)

if active_section == "03 · Simulation lab":
    # This is a real, deterministic sample construction, not an analogy.
    # A fixed internal seed makes parameter changes directly comparable without
    # exposing an unnecessary defense-time control.
    L1_SEED = 20260808
    if "l1_next_stage" in st.session_state:
        st.session_state.l1_stage = st.session_state.pop("l1_next_stage")
    controls, visual = st.columns([.72, 5.28])
    with controls:
        st.markdown("**DATA-GENERATING REGIME**")
        l1_family = st.selectbox("Distribution family", ["normal", "lognormal", "weibull", "exgaussian"], key="l1_family")
        l1_contam = st.selectbox("Contamination structure", ["none", "upper_tail", "symmetric", "bimodal", "point_mass"], index=1, key="l1_contam")
        l1_rate = st.slider("Contamination rate", 0.0, .30, .10, .01, key="l1_rate")
        l1_scale = st.slider("Outlier scale", 1.5, 20.0, 10.0, .5, key="l1_scale")
        l1_n = st.select_slider("Population / sample size", [100, 300, 500, 1000, 1500, 2500, 5000], value=1500, key="l1_n")
    l1_key=(l1_family,l1_contam,l1_rate,l1_scale,l1_n)
    if "l1_key" not in st.session_state or st.session_state.l1_key != l1_key:
        st.session_state.l1_key=l1_key; st.session_state.l1_stage=9; st.session_state.l1_playing=False
    with controls:
        st.markdown("**CONSTRUCTION PLAYBACK**")
        play, pause, reset = st.columns(3)
        if play.button("▶", use_container_width=True, key="l1_play"):
            st.session_state.l1_playing=True
        if pause.button("❚❚", use_container_width=True, key="l1_pause"):
            st.session_state.l1_playing=False
        if reset.button("↺", use_container_width=True, key="l1_reset"):
            st.session_state.l1_stage=0; st.session_state.l1_playing=False
        l1_speed=st.select_slider("Animation pace", ["Slow", "Normal", "Fast"], value="Normal", key="l1_speed")
        stage=st.select_slider("Construction stage", options=list(range(10)), value=9, format_func=lambda item: f"Step {item + 1} / 10", key="l1_stage")
    sample=draw_sample(DemoScenario(l1_family,l1_contam,float(l1_rate),float(l1_scale),int(l1_n),L1_SEED))
    construction_order=np.random.default_rng(L1_SEED + 77).permutation(l1_n)
    progress=(stage + 1) / 10
    stage_names=("mixed sample begins", "early mixed draw", "mixed draw grows", "mixed draw grows", "half the sample visible", "mixed draw grows", "contamination becomes clearer", "near-complete mixed sample", "near-complete mixed sample", "full contaminated sample")
    visible_ids=construction_order[:int(round(l1_n * progress))]
    values=sample.values[visible_ids]; visible_outliers=sample.is_outlier[visible_ids]
    full_estimates=location_estimates(sample.values)
    with visual:
        summary, *metric_cards = st.columns([2.1,1,1,1,1,1])
        with summary:
            st.markdown(f'''<div class="scenario-panel"><b>{l1_family.replace('exgaussian', 'Ex-Gaussian').title()}</b> · {l1_contam.replace('_', ' ').title()}<br>ε = {l1_rate:.0%} · scale = {l1_scale:g}× · n = {l1_n:,}<br>Expected outliers: {int(round(l1_rate*l1_n)):,}</div>''', unsafe_allow_html=True)
        for card,(name,value) in zip(metric_cards,full_estimates.items()):
            card.metric(name, f"{value:.3f}")
        st.caption(f"Step {stage + 1} of 10 · {len(values):,} visible observations: {(~visible_outliers).sum():,} inliers and {visible_outliers.sum():,} generated outliers · {stage_names[stage]}")
        fig=go.Figure()
        peak=1.0
        if len(values)>8:
            density,edges=np.histogram(values,bins=48,density=True); centers=(edges[:-1]+edges[1:])/2; peak=max(float(density.max()),.01)
            fig.add_trace(go.Scatter(x=centers,y=density,mode='lines',fill='tozeroy',name='Density',line=dict(color='#79b9e6',width=2.5),fillcolor='rgba(121,185,230,.24)'))
        if (~visible_outliers).any():
            fig.add_trace(go.Scatter(x=values[~visible_outliers],y=np.full((~visible_outliers).sum(),-.055*peak),mode='markers',name='Inliers',marker=dict(size=6,color='#6398d0',opacity=.78)))
        if visible_outliers.any():
            fig.add_trace(go.Scatter(x=values[visible_outliers],y=np.full(visible_outliers.sum(),-.055*peak),mode='markers',name='Outliers',marker=dict(size=10,color='#ff5b49',symbol='x',line=dict(width=1,color='#ffb0a7'))))
        if len(values)>8:
            current=location_estimates(values)
            for name,value in current.items(): fig.add_vline(x=value,line_width=1.5,line_dash='dot',annotation_text=name,annotation_position='top')
        fig.add_vline(x=sample.true_location,line_dash='dash',line_width=2,annotation_text='Synthetic target')
        fig.add_annotation(xref='paper',yref='paper',x=.01,y=.98,xanchor='left',yanchor='top',align='left',showarrow=False,bgcolor='rgba(8,21,37,.82)',bordercolor='#326188',borderwidth=1,text=f"<b>Mixed generated draw</b><br>Blue = inlier · Red × = generated outlier<br>{visible_outliers.sum():,} of {len(values):,} visible observations are contamination")
        fig.update_layout(height=500,xaxis_title='Observed value',yaxis_title='Density',margin=dict(l=10,r=10,t=35,b=20),legend=dict(orientation='h',y=1.02),plot_bgcolor='#081525',paper_bgcolor='#081525',yaxis=dict(range=[-.14*peak,1.15*peak]))
        st.plotly_chart(fig,use_container_width=True)
        strip=go.Figure()
        strip.add_trace(go.Scatter(x=np.arange(len(values))[~visible_outliers],y=values[~visible_outliers],mode='markers',name='Inliers',marker=dict(size=5,color='#3576a8',opacity=.55)))
        if visible_outliers.any(): strip.add_trace(go.Scatter(x=np.arange(len(values))[visible_outliers],y=values[visible_outliers],mode='markers',name='Outliers',marker=dict(size=9,color='#ff5b49',symbol='x',opacity=.9)))
        strip.add_annotation(xref='paper',yref='paper',x=.01,y=.98,xanchor='left',yanchor='top',showarrow=False,bgcolor='rgba(8,21,37,.82)',bordercolor='#326188',borderwidth=1,text='Random observation order: contamination is interleaved with inliers.')
        strip.update_layout(title='Actual generated observation order',height=390,xaxis_title='Random draw order',yaxis_title='Observed value',margin=dict(l=10,r=10,t=40,b=20),legend=dict(orientation='h',y=1.04),plot_bgcolor='#081525',paper_bgcolor='#081525')
        st.plotly_chart(strip,use_container_width=True)
    if st.session_state.l1_playing:
        if stage < 9:
            time.sleep({"Slow":3.5,"Normal":1.8,"Fast":.8}[l1_speed])
            st.session_state.l1_next_stage=stage+1
            st.rerun()
        else:
            st.session_state.l1_playing=False

if active_section == "05 · GA search":
    if "l2_from_layer1" in st.session_state:
        scenario_from_l1=st.session_state.pop("l2_from_layer1")
        st.session_state.l2_family=scenario_from_l1["family"]
        st.session_state.l2_contam=scenario_from_l1["contamination"]
        st.session_state.l2_rate=scenario_from_l1["rate"]
        st.session_state.l2_scale=scenario_from_l1["scale"]
        st.session_state.l2_sample_n=scenario_from_l1["n"]
        st.success("Simulation Lab regime loaded. This mini-GA now optimizes the same pedagogical scenario.")
    controls, visual = st.columns([.72, 5.28])
    with controls:
        st.markdown("**SEARCH CONTEXT**")
        l2_family = st.selectbox("Distribution family", ["normal", "lognormal", "weibull", "exgaussian"], key="l2_family")
        l2_contam = st.selectbox("Contamination structure", ["none", "upper_tail", "symmetric", "bimodal", "point_mass"], index=1, key="l2_contam")
        l2_rate = st.slider("Contamination rate", 0.0, .30, .10, .01, key="l2_rate")
        l2_scale = st.slider("Outlier scale", 1.5, 20.0, 10.0, .5, key="l2_scale")
        l2_sample_n = st.select_slider("Teaching sample size", [100, 300, 500, 1000, 1500, 2500, 5000], value=500, key="l2_sample_n")
        l2_mutation = st.select_slider("Mutation level", options=[.05, .10, .18, .28], value=.18, format_func=lambda value: f"{value:.0%}", key="l2_mutation")
        l2_lens = st.radio("Target metric", ["MSE", "q95(MSE)"], index=1, horizontal=True, key="l2_lens", help="A pedagogical lens that changes only the synthetic terrain's shape.")
        l2_pop = st.select_slider("GA population", [36, 48, 60, 72], value=48, key="l2_pop")
        l2_seed = 20260810
        load = st.button("Generate landscape", type="primary", use_container_width=True)
        st.markdown("**GA PLAYBACK**")
        play_side, pause_side, reset_side = st.columns(3)
        if play_side.button("▶", use_container_width=True, key="l2_play"):
            st.session_state.l2_playing = True
        if pause_side.button("❚❚", use_container_width=True, key="l2_pause"):
            st.session_state.l2_playing = False
        if reset_side.button("↺", use_container_width=True, key="l2_reset"):
            st.session_state.l2_scrubber = 0; st.session_state.l2_playing = False
        speed = st.select_slider("Animation pace", ["Slow", "Normal", "Fast"], value="Normal", key="l2_speed")
    if "l2_next_frame" in st.session_state:
        st.session_state.l2_scrubber = st.session_state.pop("l2_next_frame")
    if "l2_next_phase" in st.session_state:
        st.session_state.l2_phase = st.session_state.pop("l2_next_phase")
    key = (l2_family, l2_contam, l2_rate, l2_scale, l2_mutation, l2_pop, l2_lens, l2_seed)
    if "l2_key" not in st.session_state or st.session_state.l2_key != key or load:
        st.session_state.l2_key = key
        st.session_state.l2_scrubber = 0
        st.session_state.l2_phase = 0
        st.session_state.l2_playing = False
    demo = build_layer2_demo(*key, "generation-steps-v1")
    run, terrain = demo["run"], demo["terrain"]
    max_generation = int(run["generations"][-1])
    frame = int(st.session_state.get("l2_scrubber", 0))
    with controls:
        frame = st.slider("Generation", 0, max_generation, key="l2_scrubber")
        phase = st.select_slider("Operation inside this generation", options=list(range(5)), value=0, format_func=lambda item: ("Evaluate", "Select", "Crossover", "Mutation", "Next generation")[item], key="l2_phase")
        st.markdown("**MAP VIEW**")
        show_population = st.toggle("Population", value=True, key="l2_show_population")
        show_path = st.toggle("Best path", value=True, key="l2_show_path")
        show_contours = st.toggle("Inheritance", value=True, key="l2_show_contours")
        show_grid = st.toggle("Grid", value=True, key="l2_show_grid")
        show_contamination = st.toggle("Eliminated", value=True, key="l2_show_contamination")
    active_rate = float(l2_rate)
    with visual:
        components.html(cluster_map_svg(run, frame, phase, show_inheritance=show_contours, show_eliminated=show_contamination, show_grid=show_grid, show_path=show_path), height=940, scrolling=False)
        observations, target_shift = st.columns(2)
        with observations:
            sample = draw_sample(DemoScenario(l2_family, l2_contam, active_rate, l2_scale, int(l2_sample_n), l2_seed))
            obs = go.Figure()
            inliers = sample.values[~sample.is_outlier]
            outliers = sample.values[sample.is_outlier]
            density, edges = np.histogram(inliers, bins=42, density=True)
            density = np.convolve(density, np.array([1, 2, 3, 2, 1]) / 9, mode="same")
            centers = (edges[:-1] + edges[1:]) / 2
            jitter = np.random.default_rng(l2_seed + 31 * frame)
            obs.add_trace(go.Scatter(x=centers, y=density, mode="lines", line=dict(color="#8b5cf6", width=2.5, shape="spline"), fill="tozeroy", fillcolor="rgba(139,92,246,.20)", hoverinfo="skip"))
            obs.add_trace(go.Scatter(x=inliers, y=jitter.uniform(-density.max()*.075, -density.max()*.015, len(inliers)), mode="markers", marker=dict(size=4, color="#8b5cf6", opacity=.42), hoverinfo="skip"))
            if len(outliers):
                obs.add_trace(go.Scatter(x=outliers, y=jitter.uniform(-density.max()*.20, -density.max()*.09, len(outliers)), mode="markers", marker=dict(size=7, color="#ef4444", opacity=.90), hovertemplate="Outlier<extra></extra>"))
            obs.update_layout(height=190, margin=dict(l=18,r=8,t=8,b=18), showlegend=False, xaxis=dict(showgrid=True, gridcolor="#214664", griddash="dot", zeroline=False), yaxis=dict(showgrid=True, gridcolor="#214664", griddash="dot", zeroline=False, showticklabels=False), plot_bgcolor="#081525", paper_bgcolor="#081525")
            st.plotly_chart(obs, use_container_width=True)
        with target_shift:
            components.html(contamination_shift_svg(active_rate), height=190, scrolling=False)
        score_history, survivor_history = st.columns(2)
        visible_generations = run["generations"][:frame + 1]
        all_scores = run["best_scores"]
        score_span = max(float(all_scores[0] - all_scores[-1]), 1e-9)
        visible_scores = 100 * (all_scores[0] - all_scores[:frame + 1]) / score_span
        visible_scores = np.maximum.accumulate(visible_scores)
        lineage_counts=[]
        for gen in visible_generations:
            if gen >= max_generation:
                lineage_counts.append(0); continue
            event_set=run["events"][int(gen)+1]
            parents={event.get("parent_a_index") for event in event_set if event.get("event_type")=="offspring"}
            parents|={event.get("parent_b_index") for event in event_set if event.get("event_type")=="offspring"}
            lineage_counts.append(len(parents))
        soft_grid = dict(showgrid=True, gridcolor="#214664", griddash="dot", zeroline=False)
        with score_history:
            best_score = go.Figure(go.Scatter(x=visible_generations, y=visible_scores, mode="lines", line=dict(color="#6534e8", width=3, shape="spline"), hovertemplate="Generation %{x}<br>Score %{y:.1f}<extra></extra>"))
            best_score.update_layout(title="Best demo score by generation", height=210, margin=dict(l=24,r=10,t=35,b=22), showlegend=False, xaxis=soft_grid, yaxis=soft_grid, plot_bgcolor="#081525", paper_bgcolor="#081525")
            st.plotly_chart(best_score, use_container_width=True)
        with survivor_history:
            survivors = go.Figure(go.Bar(x=visible_generations, y=lineage_counts, marker_color="#59c977", hovertemplate="Generation %{x}<br>Parents contributing %{y}<extra></extra>"))
            survivors.update_layout(title="Selected lineages by generation", height=210, margin=dict(l=24,r=10,t=35,b=22), showlegend=False, xaxis=soft_grid, yaxis=soft_grid, plot_bgcolor="#081525", paper_bgcolor="#081525", yaxis_title="Parents")
            st.plotly_chart(survivors, use_container_width=True)
        st.caption("Low-dimensional slice of the full 26-dimensional simplex; shown for visualization only.")
    st.markdown('<div class="independent-note">This layer runs its own seeded mini-GA. It does not reuse the Simulation Lab sample as evidence and never represents this animated path as a thesis trajectory.</div>', unsafe_allow_html=True)
    if st.session_state.l2_playing:
        if frame < max_generation or phase < 4:
            time.sleep({"Slow": 4.5, "Normal": 2.0, "Fast": .75}[speed])
            if phase < 4:
                st.session_state.l2_next_phase = phase + 1
            else:
                st.session_state.l2_next_phase = 0
                st.session_state.l2_next_frame = frame + 1
            st.rerun()
        else:
            st.session_state.l2_playing = False
            st.success("Demo run complete. Scrub the timeline or change the regime to compare a new search landscape.")

if active_section == "06 · Experiment pipeline":
    st.markdown("""<style>
    .layer6-view-nav .stButton>button{min-height:3.6rem!important;padding:.65rem 1rem!important;font-size:1.04rem!important;white-space:normal!important}
    .layer6-stage-nav .stButton>button{min-height:4.3rem!important;padding:.55rem .55rem!important;font-size:.9rem!important;line-height:1.18!important;white-space:normal!important}
    </style>""", unsafe_allow_html=True)
    st.markdown("<div class='layer-heading'>Thesis GA & evidence pipeline</div>", unsafe_allow_html=True)
    if "layer6_view" not in st.session_state:
        st.session_state.layer6_view = "architecture"
    st.markdown('<div class="layer6-view-nav">', unsafe_allow_html=True)
    architecture_tab, evidence_tab = st.columns(2)
    with architecture_tab:
        st.button("Thesis GA Architecture", key="layer6_architecture", use_container_width=True,
                  type="primary" if st.session_state.layer6_view == "architecture" else "secondary",
                  on_click=_set_presenter_state, args=("layer6_view", "architecture"))
    with evidence_tab:
        st.button("Evidence Pipeline", key="layer6_evidence", use_container_width=True,
                  type="primary" if st.session_state.layer6_view == "evidence" else "secondary",
                  on_click=_set_presenter_state, args=("layer6_view", "evidence"))
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.layer6_view == "architecture":
        st.markdown('<span class="badge thesis">THESIS METHOD — schematic of the implemented GA</span>', unsafe_allow_html=True)
        components.html(thesis_ga_architecture_svg(), height=920, scrolling=False)
        st.caption("Layer 5 was a pedagogical live GA. This view documents the actual thesis architecture and configuration; it does not run optimization or recompute evidence.")
    else:
        if "story_stage" not in st.session_state:
            st.session_state.story_stage = 0
        st.markdown('<div class="layer6-stage-nav">', unsafe_allow_html=True)
        stage_buttons = st.columns(5, gap="small")
        for index, (title, _claim, _what, _why) in enumerate(PIPELINE_STAGES):
            with stage_buttons[index]:
                st.button(f"{index + 1}. {title}", key=f"story_stage_{index}", use_container_width=True,
                          type="primary" if index == st.session_state.story_stage else "secondary",
                          on_click=_set_presenter_state, args=("story_stage", index))
        st.markdown('</div>', unsafe_allow_html=True)
        components.html(experiment_pipeline_svg(st.session_state.story_stage), height=790, scrolling=False)
        st.caption(f"You are seeing Stage {st.session_state.story_stage + 1} of 5. The numerical facts are fixed thesis settings/results; this visual narrative never reruns the thesis GA.")

if active_section == "07 · Results journey":
    st.markdown('<span class="badge thesis">RESULTS JOURNEY — precomputed thesis evidence</span>', unsafe_allow_html=True)
    st.caption("Discovery finds opportunities; fixed-weight evidence decides what survives.")
    result_stages = (
        ("1–2 · Discovery + Frozen I", "OPPORTUNITY", "36 → 16 → 2", "Discovery creates opportunities; frozen confirmation narrows the claim."),
        ("3 · Expanded rediscovery", "REDISCOVERY", "10 → 26", "Reopening the basis changes what the GA can discover."),
        ("4 · Strict validation", "TRANSFER SPECIALIST", "2 Weibull specialists", "Harder pressure makes the evidence local, not universal."),
        ("5A · Real-world battery", "EXTERNAL CALIBRATION", "26 / 43 parents", "Empirical transfer is calibration, not known-θ truth validation."),
        ("5B · Dirichlet audit", "AUDIT", "23 / 34 no random pass", "Benchmark retention is often meaningful, not merely GA failure."),
    )
    if "results_stage" not in st.session_state:
        st.session_state.results_stage = 0
    buttons = st.columns(5)
    for i, (label, _claim, _metric, _line) in enumerate(result_stages):
        with buttons[i]:
            if st.button(label, key=f"results_stage_{i}", use_container_width=True, type="primary" if i == st.session_state.results_stage else "secondary"):
                st.session_state.results_stage = i
                st.session_state.results_explanation = 0
    stage = st.session_state.results_stage
    label, claim, metric, interpretation = result_stages[stage]
    colors = ("#e66d4f", "#a777e3", "#54c786", "#58aee8", "#4fc3ff")
    hero, rail = st.columns([3.1, 1.05])
    with hero:
        fig = go.Figure()
        if stage == 0:
            fig.add_trace(go.Funnel(y=["Discovery regimes", "Discovery wins", "Locked confirmations"], x=[36,16,2], marker=dict(color=[colors[0],"#f3c743","#54c786"])))
            fig.update_layout(title="Opportunity → fixed-weight confirmation", height=390)
        elif stage == 1:
            fig.add_trace(go.Bar(x=["Cycle I", "Cycle II"], y=[10,26], marker_color=["#7187a4",colors[1]], text=["10 components", "26 components"], textposition="outside"))
            fig.add_annotation(x="Cycle II", y=26, text="HPF: 60% → 90%<br>CV-019 / CV-010 warm starts", showarrow=False, yshift=55)
            fig.update_layout(title="Expanded component library", height=390, yaxis_title="Learnable components")
        elif stage == 2:
            evidence = load_evidence_taxonomy()
            grades = evidence.evidence_grade.value_counts() if not evidence.empty else {}
            fig.add_trace(go.Bar(x=list(grades.index), y=list(grades.values), marker_color=colors[2]))
            fig.update_layout(title="Fixed-weight evidence taxonomy", height=390, xaxis_title="Evidence class", yaxis_title="Candidates")
        elif stage == 3:
            fig.add_trace(go.Bar(x=["Eligible parent datasets", "Parents with ≥1 corrected win"], y=[43,26], marker_color=["#7187a4",colors[3]], text=["43", "26"], textposition="outside"))
            fig.add_annotation(x="Parents with ≥1 corrected win", y=26, text="255 profile-matched FDR 5% confirmations", showarrow=False, yshift=55)
            fig.update_layout(title="Real-world external battery", height=390, yaxis_title="Parent datasets")
        else:
            audit = load_dirichlet_summary()
            total = len(audit) if not audit.empty else 34
            signals = int(audit["dirichlet_signal"].astype(str).str.lower().eq("true").sum()) if not audit.empty else 11
            fig.add_trace(go.Bar(x=["No random pass", "Some random signal", "Strongest controls pass"], y=[23, signals, 8], marker_color=["#7187a4",colors[4],"#54c786"], text=["23 / 34", f"{signals} / {total}", "8 / 8"], textposition="outside"))
            fig.update_layout(title="Dirichlet random-simplex abstain audit", height=390, yaxis_title="Regimes / controls")
        fig.update_layout(plot_bgcolor="#081525", paper_bgcolor="#081525", font_color="#e9f4ff", margin=dict(l=25,r=25,t=52,b=40), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with rail:
        st.markdown(f'''<div class="story-panel"><div class="story-kicker">CLAIM STATUS</div><div class="story-title" style="font-size:21px;color:{colors[stage]}">{claim}</div><div class="story-label">KEY EVIDENCE</div><div class="story-body">{metric}</div><div class="story-label" style="margin-top:18px">INTERPRETATION</div><div class="story-body">{interpretation}</div></div>''', unsafe_allow_html=True)
    if "results_explanation" not in st.session_state:
        st.session_state.results_explanation = 0
    explain_steps = ("Signal — what first appeared in this stage.", "Pressure — what stronger comparison or validation tested.", "Interpretation — the precise, bounded claim allowed by the evidence.")
    left, right = st.columns([1,4])
    with left:
        if st.button("Advance explanation", key="advance_results"):
            st.session_state.results_explanation = min(2, st.session_state.results_explanation + 1)
    with right:
        st.info(explain_steps[st.session_state.results_explanation])
    show_detail = st.toggle("Show technical detail", value=False, key="results_technical_detail")
    if show_detail:
        st.caption("Technical backup: precomputed candidate-level tables remain available below; no result is recomputed here.")
        winners = load_winners()
        if not winners.empty:
            top = winners.copy()
            top["gain"] = top["ga_rel_improvement_q95"].astype(float)
            st.dataframe(top[["distribution", "specialist_regime_id", "gate_pass", "final_selected_type", "gain"]].head(12), use_container_width=True, hide_index=True)

if active_section == "09 · Technical drill-down":
    st.markdown('<span class="badge thesis">THESIS RESULTS — precomputed research output</span>', unsafe_allow_html=True)
    winners=load_winners()
    if winners.empty: st.error('Not exported'); st.stop()
    family=st.selectbox('Distribution',sorted(winners.distribution.dropna().unique()),key='l3fam')
    subset=winners[winners.distribution==family]
    regime=st.selectbox('Regime',list(subset.specialist_regime_id.dropna().unique()))
    row=subset[subset.specialist_regime_id==regime].iloc[0]
    st.subheader(f"{family} — {regime}");st.caption(str(row.get('condition_summary',row.get('regime_key',''))))
    c1,c2,c3=st.columns(3);c1.metric('Discovery gate pass',str(row.get('gate_pass')));c2.metric('Final selected type',str(row.get('final_selected_type')));c3.metric('Best q95 benchmark',str(row.get('best_benchmark_q95_estimator')))
    weights=sorted([(name,float(row.get(f'w_{name}',0) or 0)) for name in ESTIMATOR_NAMES],key=lambda x:x[1],reverse=True)
    wf=go.Figure(go.Bar(x=[x[1] for x in weights],y=[x[0] for x in weights],orientation='h',marker_color='#e6533f'));wf.update_layout(title='26-component final weight vector',height=680,yaxis=dict(autorange='reversed'),xaxis_title='Weight')
    st.plotly_chart(wf,use_container_width=True)
    st.info(f"Relative gain in q95(MSE): {row.get('ga_rel_improvement_q95','Not exported')} · Relative gain in mean MSE: {row.get('ga_rel_improvement_mean','Not exported')}. Discovery does not equal fixed-weight confirmation.")

if active_section == "09 · Technical drill-down":
    st.markdown('<span class="badge thesis">THESIS RESULTS — precomputed research output</span>', unsafe_allow_html=True)
    st.caption('Discovery → locked / fixed weights → bootstrap CI → evidence taxonomy')
    decisions,ci,evidence,validated=load_final_decisions(),load_bootstrap_ci(),load_evidence_taxonomy(),load_validated_specialists()
    ids=list(decisions.validation_id.dropna().unique()) if not decisions.empty else []
    if not ids: st.error('Not exported'); st.stop()
    vid=st.selectbox('Candidate',ids)
    dr=decisions[decisions.validation_id==vid].iloc[0];er=evidence[evidence.validation_id==vid]
    a,b=st.columns(2)
    with a: st.subheader('Fixed-weight decision');st.write(dr.get('final_fixed_weight_validation_decision','Not exported'));st.write('Original-regime gate:',dr.get('expanded_gate_pass_mean.original_regime','Not exported'));st.write('Locked-unseen gate:',dr.get('expanded_gate_pass_mean.locked_unseen_similar','Not exported'))
    with b: st.subheader('Evidence taxonomy');st.write(er.iloc[0].get('evidence_grade','Not exported') if not er.empty else 'Not exported');st.caption(er.iloc[0].get('interpretive_note','Not exported') if not er.empty else 'Not exported')
    sub=ci[ci.validation_id==vid];fig=go.Figure()
    for mode,color in [('original_regime','#e6533f'),('locked_unseen_similar','#3576a8')]:
        x=sub[sub.validation_mode==mode]
        fig.add_trace(go.Scatter(x=x.mean_gain,y=x.validation_seed,error_x=dict(type='data',symmetric=False,array=x.mean_gain_ci_high-x.mean_gain,arrayminus=x.mean_gain-x.mean_gain_ci_low),mode='markers',name=mode,marker=dict(color=color)))
    fig.add_vline(x=0,line_dash='dash');fig.update_layout(title='Mean gain with bootstrap CI',height=400,xaxis_title='Mean gain',yaxis_title='Validation seed')
    st.plotly_chart(fig,use_container_width=True);st.caption(f'Validated specialists in curated taxonomy: {len(validated)}')

if active_section == "09 · Technical drill-down":
    st.markdown('<span class="badge thesis">THESIS RESULTS — external evidence</span>', unsafe_allow_html=True)
    st.caption("These two audits answer different questions and neither retrains a discovered estimator.")
    real, audit = st.columns(2)
    with real:
        st.markdown('''<div class="story-panel"><div class="story-kicker">REAL-WORLD EXTERNAL BATTERY</div><div class="story-title">Empirical calibration</div><div class="story-label">WHAT IT TESTS</div><div class="story-body">Frozen specialists are applied to public datasets without retraining. Repeated subsamples are assessed against the empirical full-sample mean.</div><div class="story-label" style="margin-top:20px">THESIS RESULT</div><div class="story-body">At least one corrected win occurred in 26 of 43 eligible parent datasets; 255 profile-matched comparisons survived false-discovery-rate control.</div><div class="story-label" style="margin-top:20px">QUESTION</div><div class="story-body">Does the supported signal transfer to empirical data?</div></div>''', unsafe_allow_html=True)
    with audit:
        st.markdown('''<div class="story-panel"><div class="story-kicker">RANDOM DIRICHLET ABSTAIN AUDIT</div><div class="story-title">Simplex sanity check</div><div class="story-label">WHAT IT TESTS</div><div class="story-body">Random Dirichlet composites are evaluated in benchmark-retained regimes under the original dual gate. This audit does not rerun the GA.</div><div class="story-label" style="margin-top:20px">QUESTION</div><div class="story-body">Could arbitrary weight vectors reveal composite signal where the selected GA candidate was retained by the benchmark?</div></div>''', unsafe_allow_html=True)
    dirichlet_summary, dirichlet_signals = load_dirichlet_summary(), load_dirichlet_signals()
    if not dirichlet_summary.empty:
        signal_count=int(dirichlet_summary["dirichlet_signal"].astype(str).str.lower().eq("true").sum())
        total=len(dirichlet_summary)
        metric_a, metric_b, metric_c = st.columns(3)
        metric_a.metric("Audited regimes", total)
        metric_b.metric("Regimes with Dirichlet signal", signal_count)
        metric_c.metric("Audit rule", "4,000 draws · 8 seeds")
        plot_data=dirichlet_summary.sort_values("total_seed_stable_passes", ascending=False).head(12)
        audit_fig=go.Figure(go.Bar(x=plot_data["validation_id"], y=plot_data["total_seed_stable_passes"], marker_color=["#f3c743" if str(v).lower()=="true" else "#526a85" for v in plot_data["dirichlet_signal"]], hovertemplate="%{x}<br>Seed-stable passes: %{y}<extra></extra>"))
        audit_fig.update_layout(title="Dirichlet audit: seed-stable random-search passes by regime", height=350, yaxis_title="Passes across audit seeds", plot_bgcolor="#081525", paper_bgcolor="#081525")
        st.plotly_chart(audit_fig, use_container_width=True)
        st.caption("Gold bars indicate a reported Dirichlet signal. A signal calls for the abstention to be revisited; it is not a replacement for fixed-weight confirmation.")
    else:
        st.info("Dirichlet audit results were not exported to this dashboard bundle.")

if active_section == "00 · Cover":
    logo, opening = st.columns([1, 3.4])
    with logo:
        st.image("assets/university_of_hull_logo.jpeg", use_container_width=True)
    with opening:
        st.markdown("## Building Better Estimators")
        st.markdown("### Benchmark-gated, regime-conditional composite mean estimation via genetic search")
        st.caption("MSc Artificial Intelligence · Thesis Defense · Alvaro Rivera-Eraso · Supervisor · University of Hull")
        st.markdown("<br>", unsafe_allow_html=True)
        start, results, appendix = st.columns([1.45, 1, 1])
        start.button("Start Defense →", type="primary", use_container_width=True, on_click=_navigate, args=(1,))
        results.button("Jump to Results", use_container_width=True, on_click=_navigate, args=(7,))
        appendix.button("Technical Appendix", use_container_width=True, on_click=_navigate, args=(9,))
    st.info("Conditional estimator discovery — not universal GA superiority.")

if active_section == "01 · Research logic":
    st.markdown("""<style>
    .research-logic-nav .stButton>button{min-height:3.6rem!important;padding:.65rem .75rem!important;font-size:1.03rem!important;line-height:1.18!important;white-space:normal!important}
    .research-logic-nav .stButton>button[kind="primary"]{box-shadow:0 0 18px rgba(93,62,221,.38)!important}
    .research-logic-next .stButton>button{min-height:3.25rem!important;padding:.65rem 1.25rem!important;font-size:1.05rem!important}
    </style>""", unsafe_allow_html=True)
    st.markdown("<div class='layer-heading'>Research logic: why the experiment exists</div>", unsafe_allow_html=True)
    if "research_panel" not in st.session_state:
        st.session_state.research_panel = 0
    st.markdown('<div class="research-logic-nav">', unsafe_allow_html=True)
    panel_buttons = st.columns(5, gap="medium")
    for i, (label, _what, _why, _say) in enumerate(RESEARCH_PANELS):
        with panel_buttons[i]:
            st.button(label, key=f"research_panel_{i}", use_container_width=True, type="primary" if i == st.session_state.research_panel else "secondary", on_click=_set_presenter_state, args=("research_panel", i))
    st.markdown('</div>', unsafe_allow_html=True)
    components.html(research_logic_svg(st.session_state.research_panel), height=1000, scrolling=False)
    st.markdown('<div class="research-logic-next">', unsafe_allow_html=True)
    st.button("Continue to simulated world →", type="primary", on_click=_navigate, args=(2,))
    st.markdown('</div>', unsafe_allow_html=True)

if active_section == "02 · Data-generating world":
    st.markdown("""<style>
    .data-world-nav .stButton>button{min-height:3.6rem!important;padding:.65rem 1rem!important;font-size:1.03rem!important;line-height:1.18!important;white-space:normal!important}
    .data-world-nav .stButton>button[kind="primary"]{box-shadow:0 0 18px rgba(93,62,221,.38)!important}
    </style>""", unsafe_allow_html=True)
    st.markdown("<div class='layer-heading'>Data-generating world: controlled structural coverage</div>", unsafe_allow_html=True)
    if "data_world_view" not in st.session_state:
        st.session_state.data_world_view = 0
    st.markdown('<div class="data-world-nav">', unsafe_allow_html=True)
    view_buttons = st.columns(3, gap="medium")
    for index, label in enumerate(DATA_WORLD_VIEWS):
        with view_buttons[index]:
            st.button(label, key=f"data_world_view_{index}", use_container_width=True,
                      type="primary" if index == st.session_state.data_world_view else "secondary",
                      on_click=_set_presenter_state, args=("data_world_view", index))
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.data_world_view == 0:
        # Preserve the original Experimental Grid view exactly as it was.
        components.html(defense_scene_svg(4), height=860, scrolling=False)
        st.caption("This methodological scene prepares the live simulations; it does not present a result.")
    else:
        components.html(data_world_detail_svg(st.session_state.data_world_view), height=860, scrolling=False)
        if st.session_state.data_world_view == 1:
            st.caption("Structural coverage: six families expose the same population-mean target to qualitatively different sampling environments.")
        else:
            st.caption("Certification is independent of the GA: 125 validation conditions, 0 hard failures, 29 explainable warnings.")

if active_section == "04 · Monte Carlo engine":
    st.markdown("""<style>
    .monte-carlo-tabs .stButton>button{min-height:3.5rem!important;padding:.65rem 1rem!important;font-size:1.04rem!important;white-space:normal!important}
    .validation-stage-tabs .stButton>button{min-height:3.8rem!important;padding:.55rem .7rem!important;font-size:.96rem!important;line-height:1.2!important;white-space:normal!important}
    </style>""", unsafe_allow_html=True)
    if "monte_carlo_view" not in st.session_state:
        st.session_state.monte_carlo_view = "engine"
    st.markdown('<div class="monte-carlo-tabs">', unsafe_allow_html=True)
    engine_tab, validation_tab = st.columns(2)
    with engine_tab:
        st.button("Monte Carlo measurement engine", key="monte_carlo_engine", use_container_width=True, type="primary" if st.session_state.monte_carlo_view == "engine" else "secondary", on_click=_set_presenter_state, args=("monte_carlo_view", "engine"))
    with validation_tab:
        st.button("Data-generating world validation", key="monte_carlo_validation", use_container_width=True, type="primary" if st.session_state.monte_carlo_view == "validation" else "secondary", on_click=_set_presenter_state, args=("monte_carlo_view", "validation"))
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.monte_carlo_view == "engine":
        components.html(defense_scene_svg(5), height=910, scrolling=False)
    else:
        if "validation_stage" not in st.session_state:
            st.session_state.validation_stage = 0
        st.markdown('<div class="validation-stage-tabs">', unsafe_allow_html=True)
        validation_buttons = st.columns(4, gap="medium")
        for index, (title, *_detail) in enumerate(VALIDATION_STAGES):
            with validation_buttons[index]:
                st.button(title, key=f"validation_stage_{index}", use_container_width=True, type="primary" if index == st.session_state.validation_stage else "secondary", on_click=_set_presenter_state, args=("validation_stage", index))
        st.markdown('</div>', unsafe_allow_html=True)
        components.html(validation_scene_svg(st.session_state.validation_stage), height=860, scrolling=False)

DEFENSE_SCENE_SECTION = {
    "08 · Conclusions": 6,
}
if active_section in DEFENSE_SCENE_SECTION:
    components.html(defense_scene_svg(DEFENSE_SCENE_SECTION[active_section]), height=770, scrolling=False)
    closing_a, closing_b = st.columns(2)
    closing_a.button("Go to technical appendix", use_container_width=True, on_click=_navigate, args=(9,))
    closing_b.button("Back to results", type="primary", use_container_width=True, on_click=_navigate, args=(7,))
