from pathlib import Path

path = Path("streamlit_app.py")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str):
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Patch target {label!r} count={count}")
    text = text.replace(old, new, 1)


# 1. Import deterministic thesis-GA schematic.
old_import = "from src.experiment_pipeline import STAGES as PIPELINE_STAGES, experiment_pipeline_svg\n"
new_import = old_import + "from src.thesis_ga_architecture import thesis_ga_architecture_svg\n"
replace_once(old_import, new_import, "Layer 6 architecture import")

# 2. Replace the generic Layer-6 cue card with architecture + stage-specific cards.
old_note = '''    "pipeline": ("Layer 6 · Experiment pipeline", "Defense script map; thesis abstract", [
        "Narrate the sequence: discovery proposes candidates; weights are frozen; new seeds and stronger benchmarks test credibility.",
        "Keep discovery, fixed-weight confirmation, profile audit and external calibration distinct.",
    ], "Now inspect the precomputed thesis evidence, not a live optimization."),
'''
new_note = '''    "pipeline_architecture": ("Layer 6 · Thesis GA Architecture", "Final thesis methods; defense implementation slides", [
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
'''
replace_once(old_note, new_note, "Layer 6 presenter notes")

# 3. Replace generic Layer-6 formula cards with architecture + stage-specific cards.
old_formulas = '''    "pipeline": [
        ("FROZEN-WEIGHT PRINCIPLE", "w*_{discovery} → freeze(w*) → validation", [
            "w*_{discovery} = recipe found during search.",
            "freeze(w*) = weights are no longer optimized.",
            "Validation evaluates the exact frozen recipe on fresh evidence.",
        ]),
        ("GAIN AGAINST BENCHMARK", "Δ = MSE_benchmark − MSE_candidate", [
            "Δ > 0 = candidate improves on the benchmark.",
            "Δ = 0 = no advantage.",
            "Δ < 0 = benchmark performs better.",
        ]),
    ],
'''
new_formulas = '''    "pipeline_architecture": [
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
'''
replace_once(old_formulas, new_formulas, "Layer 6 formula cards")

# 4. Presenter-note resolver follows the active Layer-6 subview and stage.
old_fixed = '''    fixed = {
        "00 · Cover": "cover", "03 · Simulation lab": "simulation_lab", "05 · GA search": "ga_search",
        "06 · Experiment pipeline": "pipeline", "07 · Results journey": "results",
        "08 · Conclusions": "conclusions", "09 · Technical drill-down": "technical",
    }
'''
new_fixed = '''    fixed = {
        "00 · Cover": "cover", "03 · Simulation lab": "simulation_lab", "05 · GA search": "ga_search",
        "07 · Results journey": "results", "08 · Conclusions": "conclusions", "09 · Technical drill-down": "technical",
    }
'''
replace_once(old_fixed, new_fixed, "presenter fixed map")

old_resolver_tail = '''    if active_section == "04 · Monte Carlo engine":
        if st.session_state.get("monte_carlo_view", "engine") == "validation":
            return f"monte_carlo_validation_{int(st.session_state.get('validation_stage', 0))}"
        return "monte_carlo_engine"
    return fixed[active_section]
'''
new_resolver_tail = '''    if active_section == "04 · Monte Carlo engine":
        if st.session_state.get("monte_carlo_view", "engine") == "validation":
            return f"monte_carlo_validation_{int(st.session_state.get('validation_stage', 0))}"
        return "monte_carlo_engine"
    if active_section == "06 · Experiment pipeline":
        if st.session_state.get("layer6_view", "architecture") == "architecture":
            return "pipeline_architecture"
        return f"pipeline_stage_{int(st.session_state.get('story_stage', 0))}"
    return fixed[active_section]
'''
replace_once(old_resolver_tail, new_resolver_tail, "Layer 6 presenter resolver")

# 5. Replace the old single-view Layer-6 renderer with Architecture + Evidence Pipeline.
old_layer6 = '''if active_section == "06 · Experiment pipeline":
    if "story_stage" not in st.session_state:
        st.session_state.story_stage = 0
    stage_buttons = st.columns(3)
    for index, (title, _claim, _what, _why) in enumerate(PIPELINE_STAGES):
        with stage_buttons[index % 3]:
            if st.button(f"{index + 1}. {title}", key=f"story_stage_{index}", use_container_width=True, type="primary" if index == st.session_state.story_stage else "secondary"):
                st.session_state.story_stage = index
    components.html(experiment_pipeline_svg(st.session_state.story_stage), height=790, scrolling=False)
    st.caption(f"You are seeing Stage {st.session_state.story_stage + 1} of 5. Select a stage manually; this visual narrative never reruns the thesis GA.")
'''
new_layer6 = '''if active_section == "06 · Experiment pipeline":
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
'''
replace_once(old_layer6, new_layer6, "Layer 6 main renderer")

path.write_text(text, encoding="utf-8")
print("Layer 6 integration patch applied")
