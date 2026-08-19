from pathlib import Path

path = Path("streamlit_app.py")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str):
    global text
    if old not in text:
        raise RuntimeError(f"Could not find patch target: {label}")
    if text.count(old) != 1:
        raise RuntimeError(f"Patch target is not unique ({text.count(old)}): {label}")
    text = text.replace(old, new, 1)


replace_once(
    "from src.thesis_ga_architecture import thesis_ga_architecture_svg\n",
    "from src.thesis_ga_architecture import thesis_ga_architecture_svg\nfrom src.results_journey import RESULT_STAGES, EXPLAIN_STEPS as RESULT_EXPLAIN_STEPS, result_figure, message_html as result_message_html\n",
    "Layer 7 renderer import",
)

notes_start = text.index('    "results": ("Layer 7 · Results journey"')
notes_end = text.index('    "conclusions":', notes_start)
new_notes = '''    "results_stage_0": ("Layer 7 · Results 1–2 — Discovery + Frozen I", "Thesis discovery and frozen confirmation results", [
        ("WHAT AM I LOOKING AT?", [
            "A funnel from 36 controlled regimes to 16 discovery wins and then to 2 frozen confirmations.",
            "The two green cards are the only signals that survived the first independent confirmation stage: CV-019 and CV-010, both Lognormal.",
        ]),
        ("WHAT HAPPENED?", [
            "The GA found several promising candidates during discovery.",
            "Then the weights were frozen. The GA was not allowed to adapt to the confirmation data.",
            "Only CV-019 and CV-010 survived all eight validation seeds.",
        ]),
        ("WHAT DOES IT MEAN?", [
            "Discovery tells me where there may be an opportunity.",
            "Frozen confirmation tells me which opportunities are strong enough to defend.",
            "The main message is simple: 16 interesting signals became only 2 confirmed signals.",
        ]),
        ("WHAT SHOULD I NOT CLAIM?", [
            "I should not call all 16 discovery wins final results.",
            "I should not say the GA was generally better across the 36 regimes.",
        ]),
        ("POSSIBLE QUESTIONS", [
            ("Why did so many discovery wins disappear?", "Because confirmation is deliberately harder: the weights are frozen and tested on fresh evidence instead of being optimized again."),
            ("Why are CV-019 and CV-010 important?", "They are the two first-cycle signals that survived fixed-weight confirmation and therefore became controlled warm starts later."),
        ]),
    ], "Next, show what changed when the estimator basis itself became stronger."),
    "results_stage_1": ("Layer 7 · Result 3 — Expanded Rediscovery", "Expanded 26-component discovery results", [
        ("WHAT AM I LOOKING AT?", [
            "A family map of the 12 winners found after reopening discovery with 26 learnable estimators.",
            "The height of each bar is the number of discovery winners in that family.",
        ]),
        ("WHAT HAPPENED?", [
            "The learnable basis expanded from 10 to 26 components and HPF2 exposure increased from 80% to 90%.",
            "The 12 winners were distributed as: Normal 1, Lognormal 2, Weibull 2, Inverse Gaussian 4, Ex-Gaussian 0, and Ex-Wald 3.",
            "CV-019 and CV-010 were allowed to enter as warm starts, but they received no automatic win.",
        ]),
        ("WHAT DOES IT MEAN?", [
            "A stronger estimator library changed the map of opportunity.",
            "This supports the idea that useful mixtures depend on the regime and on which estimators are available to combine.",
        ]),
        ("WHAT SHOULD I NOT CLAIM?", [
            "These 12 bars are discovery results, not final fixed-weight confirmations.",
            "A large discovery gain does not automatically mean a transferable specialist.",
        ]),
        ("POSSIBLE QUESTIONS", [
            ("Why did Inverse Gaussian produce more discovery winners?", "Under the expanded search, four Inverse Gaussian regime-seed combinations passed discovery. That is an observed opportunity pattern, not a family-wide superiority claim."),
            ("Why is Ex-Gaussian zero?", "No Ex-Gaussian candidate passed this expanded discovery gate. That is also an informative outcome of the search."),
        ]),
    ], "Now freeze the expanded candidates and test whether any of them really transfer."),
    "results_stage_2": ("Layer 7 · Result 4 — Strict Validation", "Final fixed-weight validation and evidence taxonomy", [
        ("WHAT AM I LOOKING AT?", [
            "The same two frozen Weibull specialists are shown in two validation modes.",
            "Green bars are locked-unseen related regimes. Red bars are the original-regime mode. Zero is the benchmark line.",
        ]),
        ("WHAT HAPPENED?", [
            "FWVR011 passed locked-unseen validation with about +2.79% mean gain and +2.72% q95 gain, but lost strongly in the original-regime mode.",
            "FWVR012 also passed locked-unseen validation with about +3.18% mean gain and +1.25% q95 gain, but lost in the original-regime mode.",
            "Across all 25 candidates, the taxonomy ended with 2 transfer specialists, 10 local candidates, 7 near-gate cases, and 6 negative controls.",
        ]),
        ("WHAT DOES IT MEAN?", [
            "These two estimators are useful specialists for a narrow validated profile.",
            "They are not general Weibull winners. The same fixed weights can help in one related regime and fail badly in another mode.",
        ]),
        ("WHAT SHOULD I NOT CLAIM?", [
            "I should not say the GA found a better estimator for Weibull data in general.",
            "I should not hide the original-regime failures; they define the boundary of the claim.",
        ]),
        ("POSSIBLE QUESTIONS", [
            ("How can a candidate pass locked-unseen but fail the original regime?", "Because the estimator is regime-conditional. A frozen recipe can transfer to one related profile without being uniformly good across every nearby profile."),
            ("Why call this a transfer specialist?", "Because the fixed weights show supported improvement in a locked-unseen related regime, while the evidence also shows that the improvement is narrow rather than universal."),
        ]),
    ], "After controlled validation, ask whether the same type of signal appears in real data."),
    "results_stage_3": ("Layer 7 · Result 5A — Real-World Battery", "External empirical calibration battery", [
        ("WHAT AM I LOOKING AT?", [
            "A filtering funnel from all requested external targets to the parent datasets that were actually eligible for specialist matching.",
            "The two cards separate breadth from depth: independent parent datasets versus repeated profile-level confirmations.",
        ]),
        ("WHAT HAPPENED?", [
            "The battery moved from 264 requested targets to 228 loaded, 120 evaluated, and 43 eligible parent datasets.",
            "Twenty-six of those 43 parents had at least one corrected win.",
            "Inside those eligible parents, 255 profile-matched comparisons survived FDR control.",
        ]),
        ("WHAT DOES IT MEAN?", [
            "Breadth is 26 of 43 parent datasets. Depth is 255 repeated profile-level confirmations.",
            "This is useful external evidence that the specialist idea can transfer to empirical data.",
            "It is still calibration, because real data do not reveal the true population mean.",
        ]),
        ("WHAT SHOULD I NOT CLAIM?", [
            "The 255 confirmations are not 255 independent datasets.",
            "This external battery does not replace the known-truth Monte Carlo validation.",
        ]),
        ("POSSIBLE QUESTIONS", [
            ("Why were only 43 parents eligible?", "Eligibility requires the external dataset to match the structural profile rules needed to apply a frozen specialist fairly."),
            ("What is the difference between 26 and 255?", "Twenty-six measures dataset-level breadth. The 255 results measure repeated profile-matched depth inside those parent datasets."),
        ]),
    ], "Finally, audit whether benchmark retention could simply be a weak search artifact."),
    "results_stage_4": ("Layer 7 · Result 5B — Dirichlet Audit", "Random-simplex abstention audit", [
        ("WHAT AM I LOOKING AT?", [
            "Thirty-four squares represent benchmark-retained cells that were challenged with random simplex mixtures.",
            "Grey means no random pass. Blue means some random signal. The green control card checks that the audit can detect strong positive cases.",
        ]),
        ("WHAT HAPPENED?", [
            "Twenty-three of 34 retained cells had no random pass.",
            "Eleven of 34 showed some random simplex signal.",
            "All eight strongest positive controls passed, so the audit was capable of detecting signal when it was clearly present.",
        ]),
        ("WHAT DOES IT MEAN?", [
            "In most audited retained cells, keeping the benchmark was a meaningful result rather than simply a failed GA search.",
            "The 11 signal cells are also useful because they identify abstentions that deserve further investigation.",
        ]),
        ("WHAT SHOULD I NOT CLAIM?", [
            "I should not say the audit proves the benchmark is unbeatable.",
            "I should not treat random Dirichlet search as a replacement for fixed-weight confirmation or for the GA itself.",
        ]),
        ("POSSIBLE QUESTIONS", [
            ("Why use random Dirichlet vectors?", "They provide an independent sanity check: if many arbitrary valid mixtures can pass, a benchmark-retention decision deserves closer inspection."),
            ("What do the 11 signal cells mean?", "They show that some retained cells contain composite opportunity that the selected GA path did not capture. The audit flags them; it does not automatically overturn the original decision."),
        ]),
    ], "The full results story is selective improvement, narrow transfer, external support, and justified abstention."),
'''
text = text[:notes_start] + new_notes + text[notes_end:]

formula_start = text.index('    "results": [', text.index('PRESENTER_FORMULA_CARDS = {'))
formula_end = text.index('    "technical": [', formula_start)
new_formulas = '''    "results_stage_0": [
        ("RELATIVE q95 GAIN", "Gain% = 100 × (q95_b − q95_c) / q95_b", ["q95_b = benchmark q95 squared-error risk.", "q95_c = frozen candidate q95 squared-error risk.", "Positive gain means the frozen candidate has lower difficult-case error."]),
        ("FROZEN CONFIRMATION", "discovery w* → freeze(w*) → fresh validation", ["The candidate recipe is fixed before confirmation.", "No retraining is allowed on confirmation data.", "Only two first-cycle candidates survived this step."]),
    ],
    "results_stage_1": [
        ("EXPANDED BASIS", "10 learnable → 26 learnable", ["The second discovery cycle gives the GA access to the full modern estimator library.", "This changes the search geometry and the available mixtures."]),
        ("DISCOVERY EXPOSURE", "HPF2: 80% → 90%", ["The expanded cycle uses stronger scenario exposure before its discovery gate.", "The 12 winners are still discovery signals, not final confirmations."]),
    ],
    "results_stage_2": [
        ("GAIN SIGN", "Gain% > 0 ⇒ candidate better; Gain% < 0 ⇒ benchmark better", ["The chart uses benchmark-minus-candidate relative gain.", "Green positive bars favour the frozen candidate.", "Red negative bars favour the benchmark."]),
        ("DUAL GATE", "Δ_MSE ≥ 0  AND  Δ_q95 ≥ 0", ["Both average-risk and difficult-case criteria must support the candidate.", "Failure of either criterion blocks a replacement claim."]),
    ],
    "results_stage_3": [
        ("EXTERNAL BREADTH", "26 / 43 eligible parent datasets", ["43 = eligible independent parent datasets.", "26 = parents with at least one corrected specialist win."]),
        ("EXTERNAL DEPTH", "255 profile-matched confirmations", ["These are repeated profile-level confirmations inside the eligible parent datasets.", "They must not be counted as 255 independent datasets."]),
    ],
    "results_stage_4": [
        ("AUDIT SUMMARY", "23/34 no pass · 11/34 signal · 8/8 controls pass", ["23 = retained cells with no random simplex pass.", "11 = retained cells with some random signal.", "8/8 = strongest positive controls detected by the audit."]),
        ("AUDIT BUDGET", "4,000 random vectors × 8 seeds", ["The random-search budget is an independent abstention probe.", "It does not rerun or replace the thesis GA."]),
    ],
'''
text = text[:formula_start] + new_formulas + text[formula_end:]

replace_once(
    '        "07 · Results journey": "results", "08 · Conclusions": "conclusions", "09 · Technical drill-down": "technical",\n',
    '        "08 · Conclusions": "conclusions", "09 · Technical drill-down": "technical",\n',
    "remove generic results presenter key",
)

resolver_marker = '''    if active_section == "06 · Experiment pipeline":
        if st.session_state.get("layer6_view", "architecture") == "architecture":
            return "pipeline_architecture"
        return f"pipeline_stage_{int(st.session_state.get('story_stage', 0))}"
    return fixed[active_section]
'''
resolver_replacement = '''    if active_section == "06 · Experiment pipeline":
        if st.session_state.get("layer6_view", "architecture") == "architecture":
            return "pipeline_architecture"
        return f"pipeline_stage_{int(st.session_state.get('story_stage', 0))}"
    if active_section == "07 · Results journey":
        return f"results_stage_{int(st.session_state.get('results_stage', 0))}"
    return fixed[active_section]
'''
replace_once(resolver_marker, resolver_replacement, "Layer 7 presenter resolver")

results_start = text.index('if active_section == "07 · Results journey":\n')
results_end = text.index('\nif active_section == "09 · Technical drill-down":\n', results_start)
new_results = '''if active_section == "07 · Results journey":
    st.markdown("""<style>
    .results-stage-nav .stButton>button{min-height:4.4rem!important;padding:.58rem .55rem!important;font-size:.88rem!important;line-height:1.16!important;white-space:normal!important}
    .result-bubble{background:linear-gradient(150deg,#0e2a47,#08182b);border:1px solid #3b7ba8;border-left:5px solid #f3c743;border-radius:14px;padding:1.15rem 1.15rem 1.2rem;min-height:520px;box-shadow:0 0 24px rgba(33,141,202,.09)}
    .result-kicker{font-size:.72rem;font-weight:800;letter-spacing:.12em;color:#72cfff;margin-bottom:.35rem}
    .result-claim{font-size:1.20rem;font-weight:900;line-height:1.18;margin-bottom:.45rem}
    .result-plain{font-size:1.02rem;line-height:1.36;color:#f5f8ff;border-bottom:1px solid #285b7f;padding-bottom:.9rem;margin-bottom:.9rem;font-weight:700}
    .result-label{font-size:.70rem;font-weight:900;letter-spacing:.09em;color:#f3c743;margin:.88rem 0 .25rem}
    .result-label.warn{color:#ff8c78}
    .result-copy{font-size:.88rem;line-height:1.38;color:#dce9f8}
    .result-key-strip{border:1px solid #2f6e98;border-radius:9px;background:#0a1d32;padding:.72rem 1rem;color:#dceaff;font-weight:800;text-align:center;margin:.2rem 0 .75rem}
    </style>""", unsafe_allow_html=True)
    st.markdown('<span class="badge thesis">RESULTS JOURNEY — precomputed thesis evidence</span>', unsafe_allow_html=True)
    st.caption("Each view answers one question: what happened, what survived, and how far the claim is allowed to go.")
    if "results_stage" not in st.session_state:
        st.session_state.results_stage = 0
    st.markdown('<div class="results-stage-nav">', unsafe_allow_html=True)
    buttons = st.columns(5, gap="small")
    for i, item in enumerate(RESULT_STAGES):
        with buttons[i]:
            st.button(item["label"], key=f"results_stage_{i}", use_container_width=True,
                      type="primary" if i == st.session_state.results_stage else "secondary",
                      on_click=_set_presenter_state, args=("results_stage", i))
    st.markdown('</div>', unsafe_allow_html=True)

    stage = int(st.session_state.results_stage)
    if st.session_state.get("_results_stage_seen") != stage:
        st.session_state._results_stage_seen = stage
        st.session_state.results_explanation = 0
    item = RESULT_STAGES[stage]
    st.markdown(f'<div class="result-key-strip">QUESTION: {item["question"]} &nbsp;&nbsp;|&nbsp;&nbsp; KEY EVIDENCE: {item["key"]}</div>', unsafe_allow_html=True)

    hero, rail = st.columns([3.25, 1.25], gap="large")
    with hero:
        st.plotly_chart(result_figure(stage), use_container_width=True, key=f"results_story_fig_{stage}")
    with rail:
        st.markdown(result_message_html(stage), unsafe_allow_html=True)

    if "results_explanation" not in st.session_state:
        st.session_state.results_explanation = 0
    explain_left, explain_right = st.columns([1.15, 4.4])
    with explain_left:
        if st.button("Explain this result →", key=f"advance_results_{stage}", use_container_width=True):
            st.session_state.results_explanation = (int(st.session_state.results_explanation) + 1) % 3
    with explain_right:
        st.info(RESULT_EXPLAIN_STEPS[stage][int(st.session_state.results_explanation)])

    show_detail = st.toggle("Show technical detail", value=False, key="results_technical_detail")
    if show_detail:
        st.caption("Technical backup: candidate-level tables remain available here; nothing is recomputed.")
        if stage == 2:
            decisions = load_final_decisions()
            if not decisions.empty:
                st.dataframe(decisions[decisions["validation_id"].isin(["FWVR011", "FWVR012"])], use_container_width=True, hide_index=True)
        else:
            winners = load_winners()
            if not winners.empty:
                top = winners.copy()
                top["gain"] = top["ga_rel_improvement_q95"].astype(float)
                st.dataframe(top[["distribution", "specialist_regime_id", "gate_pass", "final_selected_type", "gain"]].head(12), use_container_width=True, hide_index=True)
'''
text = text[:results_start] + new_results + text[results_end:]

path.write_text(text, encoding="utf-8")
print("Layer 7 results journey patch applied successfully")
