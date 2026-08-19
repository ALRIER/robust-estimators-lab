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
    "from src.research_logic import PANELS as RESEARCH_PANELS, research_logic_svg\n",
    "from src.research_logic import PANELS as RESEARCH_PANELS, research_logic_svg\nfrom src.data_world import DATA_WORLD_VIEWS, data_world_detail_svg\n",
    "data-world import",
)

old_note = '''    "data_world": ("Layer 2 · Data-generating world", "Defense deck · Monte Carlo evaluation; Appendix A1/A2", [
        "Simulation is deliberate because it makes the true target known; real datasets do not reveal the population mean.",
        "The grid varies family, sample size, contamination rate, outlier scale and contamination mechanism to stress estimator failure modes.",
        "The simulator is validated before any GA conclusion is trusted.",
    ], "First inspect one generated sample in the Simulation Lab before moving to repeated sampling."),
'''
new_note = old_note + '''    "data_world_families": ("Layer 2 · Six Families", "Defense deck · Appendix A2; thesis distribution-family table", [
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
'''
replace_once(old_note, new_note, "Layer 2 presenter notes")

old_formulas = '''    "data_world": [
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
'''
new_formulas = old_formulas + '''    "data_world_families": [
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
'''
replace_once(old_formulas, new_formulas, "Layer 2 formula cards")

old_resolver = '''    fixed = {
        "00 · Cover": "cover", "02 · Data-generating world": "data_world",
        "03 · Simulation lab": "simulation_lab", "05 · GA search": "ga_search",
        "06 · Experiment pipeline": "pipeline", "07 · Results journey": "results",
        "08 · Conclusions": "conclusions", "09 · Technical drill-down": "technical",
    }
    if active_section == "01 · Research logic":
'''
new_resolver = '''    fixed = {
        "00 · Cover": "cover", "03 · Simulation lab": "simulation_lab", "05 · GA search": "ga_search",
        "06 · Experiment pipeline": "pipeline", "07 · Results journey": "results",
        "08 · Conclusions": "conclusions", "09 · Technical drill-down": "technical",
    }
    if active_section == "01 · Research logic":
'''
replace_once(old_resolver, new_resolver, "presenter fixed map")

old_research_return = '''        return keys[int(st.session_state.get("research_panel", 0))]
    if active_section == "04 · Monte Carlo engine":
'''
new_research_return = '''        return keys[int(st.session_state.get("research_panel", 0))]
    if active_section == "02 · Data-generating world":
        keys = ("data_world", "data_world_families", "data_world_certification")
        return keys[int(st.session_state.get("data_world_view", 0))]
    if active_section == "04 · Monte Carlo engine":
'''
replace_once(old_research_return, new_research_return, "Layer 2 presenter key resolver")

monte_marker = '''if active_section == "04 · Monte Carlo engine":
'''
layer2_block = '''if active_section == "02 · Data-generating world":
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

'''
if text.count(monte_marker) != 1:
    raise RuntimeError(f"Monte Carlo marker count is {text.count(monte_marker)}")
text = text.replace(monte_marker, layer2_block + monte_marker, 1)

old_scene_map = '''DEFENSE_SCENE_SECTION = {
    "02 · Data-generating world": 4,
    "08 · Conclusions": 6,
}
if active_section in DEFENSE_SCENE_SECTION:
    scene_height = 860 if active_section == "02 · Data-generating world" else 770
    components.html(defense_scene_svg(DEFENSE_SCENE_SECTION[active_section]), height=scene_height, scrolling=False)
    if active_section == "08 · Conclusions":
        closing_a, closing_b = st.columns(2)
        closing_a.button("Go to technical appendix", use_container_width=True, on_click=_navigate, args=(9,))
        closing_b.button("Back to results", type="primary", use_container_width=True, on_click=_navigate, args=(7,))
    else:
        st.caption("This methodological scene prepares the live simulations; it does not present a result.")
'''
new_scene_map = '''DEFENSE_SCENE_SECTION = {
    "08 · Conclusions": 6,
}
if active_section in DEFENSE_SCENE_SECTION:
    components.html(defense_scene_svg(DEFENSE_SCENE_SECTION[active_section]), height=770, scrolling=False)
    closing_a, closing_b = st.columns(2)
    closing_a.button("Go to technical appendix", use_container_width=True, on_click=_navigate, args=(9,))
    closing_b.button("Back to results", type="primary", use_container_width=True, on_click=_navigate, args=(7,))
'''
replace_once(old_scene_map, new_scene_map, "remove old Layer 2 static renderer")

path.write_text(text, encoding="utf-8")
print("Layer 2 patch applied successfully")
