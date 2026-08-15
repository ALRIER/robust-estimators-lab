from pathlib import Path
import re

path = Path("streamlit_app.py")
text = path.read_text(encoding="utf-8")

formula_cards = r'''
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
    "pipeline": [
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
'''

marker = "_query = st.query_params"
if "PRESENTER_FORMULA_CARDS =" not in text:
    text = text.replace(marker, formula_cards + "\n" + marker, 1)

new_renderer = r'''# Presenter view: every note is rendered as a large, scan-friendly cue card.
# It accepts both the structured Layer-1 format and the simpler bullet lists
# used by later layers.
if _query.get("presenter_notes") == "1":
    import html as _html

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
            return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text_value) if part.strip()]

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
'''

pattern = re.compile(
    r'# The presenter view deliberately uses.*?if _query\.get\("presenter_notes"\) == "1":.*?\n\s*st\.stop\(\)\n',
    re.S,
)
match = pattern.search(text)
if not match:
    raise SystemExit("Could not find presenter renderer block")
text = text[:match.start()] + new_renderer + "\n" + text[match.end():]

path.write_text(text, encoding="utf-8")
print("Presenter notes renderer and formula cards standardized.")
