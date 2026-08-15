"""Interactive opening scene for the thesis research logic.

The visible notation follows the final KBS manuscript: regime ℛ, induced
sampling distribution F_ℛ, fixed target μ_F = E_F[X], simplex-constrained
composites, and finite-sample MSE decomposition.
"""

PANELS = (
    (
        "Problem",
        "The target stays fixed, but estimator performance changes with the regime.",
        "No operationally admissible estimator is uniformly best across all data-generating conditions.",
        "Change the regime, and the risk ranking can change.",
    ),
    (
        "Objective / RQ",
        "When can evolutionary search produce an interpretable mixture that improves on the strongest admissible benchmark?",
        "The question is conditional: discovery proposes candidates, but validation decides whether replacement is justified.",
        "We ask when improvement is supported, not whether GA always wins.",
    ),
    (
        "H1–H4",
        "Four linked hypotheses turn the No-Free-Lunch intuition into testable claims.",
        "They separate regime dependence, selective opportunity, and evidence control.",
        "The hypotheses form the logical spine of the defense.",
    ),
    (
        "Target / Simplex",
        "The estimand is fixed at the population mean; the GA only changes the estimator recipe.",
        "Every candidate is a non-negative convex mixture of named estimators and remains inspectable.",
        "The target is fixed; only the weights evolve.",
    ),
    (
        "Why can win",
        "A composite can win only when variance reduction more than compensates for squared bias.",
        "Clean light-tailed symmetry leaves little room; skewness, heavy tails, or contamination may create conditional opportunity.",
        "A valid mixture is not automatically a better estimator.",
    ),
)


def _t(x, y, value, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{value}</text>'


def _wrap_text(value: str, max_chars: int = 31):
    """Split SVG copy into short lines so it never escapes its card."""
    words = str(value).split()
    if not words:
        return []
    lines, current = [], words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def research_logic_svg(panel: int) -> str:
    """Render five distinct research-logic scenes in one defense canvas."""
    panel = max(0, min(int(panel), 4))
    headings = (
        "PROBLEM",
        "OBJECTIVE / RESEARCH QUESTIONS",
        "H1–H4: CAUSAL HYPOTHESIS CHAIN",
        "TARGET / SIMPLEX",
        "WHY A COMPOSITE CAN WIN",
    )
    claims = (
        "No single admissible estimator remains uniformly reliable across changing regimes.",
        "Can evolutionary search find credible, interpretable improvement in the fixed target μ_F = E_F[X]?",
        "No universal winner → regime dependence → selective GA opportunity → benchmark-gated claims.",
        "The target stays fixed at θ(F) = μ_F = E_F[X]; the GA learns inspectable simplex weights.",
        "Lower MSE is possible only when variance reduction exceeds the squared bias cost.",
    )
    p = [
        '<rect x="20" y="16" width="1560" height="904" rx="18" class="canvas"/>',
        _t(48, 56, "01 · RESEARCH LOGIC", "kicker"),
        _t(48, 100, headings[panel], "title"),
        _t(48, 137, claims[panel], "claim"),
    ]

    def card(x, y, w, h, title, lines, cls="card"):
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}"/>')
        p.append(_t(x + 20, y + 32, title, "head"))
        p.extend(_t(x + 20, y + 62 + i * 22, line, "body") for i, line in enumerate(lines))

    def rail(lines, why, next_=None):
        """Right-side interpretation rail. NEXT is intentionally omitted."""
        card(1260, 170, 300, 705, "WHAT THIS MEANS", lines, "rail")
        p.append(_t(1280, 310, "WHY IT MATTERS", "kicker"))
        for i, line in enumerate(_wrap_text(why, 31)):
            p.append(_t(1280, 340 + i * 22, line, "railtext"))

    if panel == 0:
        card(48, 185, 520, 350, "CLEAN / NEAR-SYMMETRIC", [
            "Mean is close to the target.",
            "Mean — efficient here.",
        ], "scene")
        p.extend([
            '<path d="M100 435 C180 275 350 275 520 435" class="curve"/>',
            '<path d="M310 268 V465" class="target"/>',
            '<circle cx="310" cy="382" r="10" class="mean"/>',
            _t(310, 495, "target  μ_F", "small", "middle"),
            '<path d="M590 355 L750 355" class="bigarrow" marker-end="url(#arrow)"/>',
        ])
        card(800, 185, 400, 350, "SKEWED / CONTAMINATED", [
            "Extremes can pull the sample mean.",
            "Robust estimators may move less.",
        ], "warn")
        p.extend([
            '<path d="M840 435 C900 285 980 300 1020 415 C1100 440 1140 350 1175 250" class="curvewarn"/>',
            '<path d="M965 268 V465" class="target"/>',
            '<circle cx="1080" cy="382" r="10" class="mean"/>',
            '<circle cx="985" cy="382" r="10" class="robust"/>',
            _t(1080, 415, "Mean", "small", "middle"),
            _t(985, 415, "Robust", "small", "middle"),
            _t(624, 590, "Change regime  →  change risk  →  change ranking", "gold", "middle"),
        ])
        rail(
            ["The target is still μ_F.", "What changes is estimator risk."],
            "The best estimator can depend on F_ℛ.",
        )

    elif panel == 1:
        card(48, 175, 1150, 100, "AIM", [
            "Identify regime-conditional, interpretable improvements in μ_F that remain credible after frozen validation."
        ], "hero")
        for i, (name, desc) in enumerate((
            ("SEARCH", "Propose simplex weight vectors"),
            ("CHALLENGE", "Freeze; test fresh evidence"),
            ("ACCEPT / ABSTAIN", "Gate decides replacement"),
        )):
            x = 65 + i * 380
            card(x, 320, 315, 105, name, [desc], "step")
            if i < 2:
                p.append(f'<path d="M{x+325} 372 L{x+360} 372" class="arrow" marker-end="url(#arrow)"/>')
        rqs = (
            ("RQ1 · Discovery", "Where can a composite improve?", "Discovery + held-out gate."),
            ("RQ2 · Confirmation", "Do gains survive frozen weights?", "Independent confirmation."),
            ("RQ3 · Expanded basis", "What changes from 10 to 26?", "Expanded rediscovery."),
            ("RQ4 · Transfer", "Do specialists transfer?", "External evidence."),
        )
        for i, (label, q, stage) in enumerate(rqs):
            card(48 + i * 290, 480, 270, 165, label, [q, stage], "rqactive" if i == 0 else "card")
        rail(
            ["Search and evidence are separate.", "A candidate is not yet a result."],
            "The framework is allowed to retain the benchmark.",
        )

    elif panel == 2:
        data = (
            ("H1", "No universal estimator.", "Different regimes can have different winners.", "Scope"),
            ("H2", "Performance depends on regime.", "Conditional risk changes with F_ℛ.", "Mechanism"),
            ("H3", "GA helps only selectively.", "Only some regimes should support replacement.", "Opportunity"),
            ("H4", "The gate controls claims.", "Unsupported candidates return to benchmark.", "Claim control"),
        )
        for i, (h, statement, prediction, role) in enumerate(data):
            x = 48 + i * 292
            p.append(f'<rect x="{x}" y="195" width="268" height="355" rx="14" class="hyp"/>')
            p.append(_t(x + 20, 227, h, "head"))
            statement_lines = _wrap_text(statement, 28)
            for line_i, line in enumerate(statement_lines):
                p.append(_t(x + 20, 260 + line_i * 22, line, "hypbody"))
            p.append(_t(x + 20, 320, "PREDICTION", "hypsection"))
            prediction_lines = _wrap_text(prediction, 28)
            for line_i, line in enumerate(prediction_lines):
                p.append(_t(x + 20, 348 + line_i * 22, line, "hypbody"))
            p.append(_t(x + 20, 430, "ROLE IN THE STUDY", "hypsection"))
            p.append(_t(x + 20, 458, role, "hypbody"))
            if i < 3:
                p.append(f'<path d="M{x+272} 375 L{x+286} 375" class="arrow" marker-end="url(#arrow)"/>')
        p.extend([
            _t(620, 635, "H1  →  H2  →  H3  →  H4", "chain", "middle"),
            _t(620, 670, "A reasoning chain: scope → regime dependence → opportunity → evidence control.", "body", "middle"),
        ])
        rail(
            ["These are pre-result predictions.", "They bound what counts as success."],
            "Benchmark retention is a valid scientific outcome.",
        )

    elif panel == 3:
        card(48, 190, 300, 335, "FIXED TARGET", [
            "Population mean.",
            "Every candidate estimates μ_F.",
        ], "scene")
        p.extend([
            '<path d="M100 440 C175 285 270 285 325 440" class="curve"/>',
            '<path d="M210 268 V460" class="target"/>',
            _t(210, 490, "θ(F) = μ_F = E_F[X]", "gold", "middle"),
        ])
        card(400, 190, 410, 335, "CANDIDATE RECIPE", [
            "Each GA individual is a weight vector.",
            "Named components remain inspectable.",
        ], "scene")
        for i, (name, w) in enumerate(zip(("Mean", "Median", "Huber", "Biweight"), (18, 27, 24, 31))):
            y = 325 + i * 44
            p.extend([
                _t(430, y, name, "small"),
                f'<rect x="525" y="{y-17}" width="{w*6}" height="20" rx="4" class="weight"/>',
                _t(735, y, f"{w}%", "small", "end"),
            ])
        p.extend([
            _t(605, 510, "weights sum to 100%", "gold", "middle"),
            '<path d="M835 355 L920 355" class="bigarrow" marker-end="url(#arrow)"/>',
            '<rect x="930" y="255" width="270" height="190" rx="14" class="hero"/>',
            _t(950, 287, "INTERPRETABLE", "head"),
            _t(950, 312, "MIXTURE", "head"),
            _t(950, 345, "θ̂_w,n = Σⱼ₌₁ᴸ wⱼTⱼ,n", "body"),
            _t(950, 367, "w ∈ Δ_L", "body"),
            _t(950, 389, "wⱼ ≥ 0  ·  Σwⱼ = 1", "body"),
        ])
        rail(
            ["The estimand never moves.", "Only the estimator recipe evolves."],
            "Simplex weights are interpretable, not proof of superiority.",
        )

    else:
        card(48, 180, 1150, 100, "FINITE-SAMPLE TRADE-OFF", [
            "A composite is useful only when its lower variance compensates for any bias introduced by robust components."
        ], "hero")
        p.extend([
            _t(90, 345, "Composite MSE", "head"),
            _t(90, 392, "MSE_F,n(θ̂_w,n) = B_n(w,F)² + V_n(w,F)", "formula"),
            _t(90, 495, "Dominance over the sample mean", "head"),
            _t(90, 542, "B_n(w,F)² + V_n(w,F)  <  Var_F(X̄_n)", "formula2"),
        ])
        card(800, 330, 400, 250, "INTERPRETATION", [
            "Clean light-tailed symmetry:",
            "little variance is available to give up.",
            "",
            "Skew / tails / contamination:",
            "robust mixtures may reduce finite-sample risk.",
        ], "scene")
        rail(
            ["MSE = squared bias + variance.", "Improvement is conditional, never guaranteed."],
            "The benchmark gate must confirm both mean MSE and q0.95 MSE.",
        )

    technical = (
        (
            ("REGIME", "ℛ = (F₀, γ, c, m, n)", "Family, rate, scale, mechanism, and sample size."),
            ("INDUCED DISTRIBUTION", "F_ℛ = (1−γ)F₀ + γG_{m,c}(F₀)", "The regime determines the distribution used for sampling."),
            ("FIXED TARGET", "θ(F) = μ_F = E_F[X]", "All estimators are judged against the same population mean."),
        ),
        (
            ("TARGET", "θ(F) = μ_F = E_F[X]", "The estimand is fixed throughout the programme."),
            ("CANDIDATE", "θ̂_w,n = Σⱼ₌₁ᴸ wⱼTⱼ,n", "Evolutionary search proposes an interpretable estimator recipe."),
            ("CLAIM CONTROL", "mean MSE + q₀.₉₅ MSE gate", "Improvement on only one criterion is insufficient."),
        ),
        (
            ("H1", "No universal estimator", "Do not expect one winner across incompatible regimes."),
            ("H2 → H3", "regime dependence → selective opportunity", "Changing F can change the bias–variance trade-off."),
            ("H4", "benchmark-gated acceptance", "Discovery signals must survive independent evidence."),
        ),
        (
            ("COMPOSITE", "θ̂_w,n = Σⱼ₌₁ᴸ wⱼTⱼ,n", "A weighted recipe of named location estimators."),
            ("SIMPLEX", "Δ_L = {w ∈ [0,1]ᴸ : Σwⱼ = 1}", "Non-negative proportions that sum to one."),
            ("TARGET", "θ(F) = μ_F = E_F[X]", "Validity of weights is separate from evidence of lower risk."),
        ),
        (
            ("MSE DECOMPOSITION", "MSE_F,n(θ̂_w,n) = B_n(w,F)² + V_n(w,F)", "Finite-sample risk splits into squared bias and variance."),
            ("BIAS", "B_n(w,F) = Σwⱼ{E_F[Tⱼ,n] − μ_F}", "Robust components can buy stability at a bias cost."),
            ("DOMINANCE", "B_n(w,F)² + V_n(w,F) < Var_F(X̄_n)", "Exact condition for lower MSE than the sample mean."),
        ),
    )[panel]

    p += [
        '<rect x="48" y="720" width="1150" height="140" rx="14" class="technical"/>',
        _t(72, 752, "STATISTICAL SUPPORT — notation for the speaker", "kicker"),
    ]
    for i, (label, formula, note) in enumerate(technical):
        x = 72 + i * 370
        p += [
            _t(x, 783, label, "techlabel"),
            _t(x, 812, formula, "techtext"),
            _t(x, 840, note, "technote"),
        ]

    css = '''body{margin:0;background:#081525;font-family:Arial,sans-serif}svg{width:100%;height:940px}.canvas{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}.kicker{font-size:14px;font-weight:800;letter-spacing:1.5px;fill:#72cfff}.title{font-size:33px;font-weight:800;fill:#f5f9ff}.claim{font-size:20px;font-weight:700;fill:#dceaff}.body{font-size:17px;fill:#dce9f8}.small{font-size:14px;fill:#bdd0e2}.gold{font-size:16px;font-weight:800;fill:#f3c743}.head{font-size:18px;font-weight:800;fill:#f5f9ff}.card,.scene,.step,.hyp{fill:#0d2741;stroke:#397daa;stroke-width:1.4}.warn{fill:#382335;stroke:#ff825f;stroke-width:1.8}.hero,.rqactive{fill:#102d4b;stroke:#f3c743;stroke-width:1.8}.rail{fill:#0b2138;stroke:#4b84ad;stroke-width:1.3}.technical{fill:#0a1c31;stroke:#2d6d9c;stroke-width:1.3}.railtext{font-size:15px;fill:#dce9f8}.hypbody{font-size:15.5px;fill:#dce9f8}.hypsection{font-size:15px;font-weight:800;fill:#f5f9ff}.techlabel{font-size:12px;font-weight:800;letter-spacing:1px;fill:#72cfff}.techtext{font-family:Georgia,serif;font-size:15px;fill:#f3c743}.technote{font-size:12.5px;fill:#bdd0e2}.curve{stroke:#58aee8;stroke-width:4;fill:none}.curvewarn{stroke:#ff825f;stroke-width:4;fill:none}.target{stroke:#f3c743;stroke-width:3;stroke-dasharray:7 5}.mean{fill:#ff825f}.robust{fill:#63dfa2}.arrow,.bigarrow{stroke:#72cfff;stroke-width:3;fill:none}.bigarrow{stroke-width:5}.chain{font-size:27px;font-weight:800;fill:#f3c743}.weight{fill:#58aee8}.formula{font-family:Georgia,serif;font-size:25px;fill:#f3c743}.formula2{font-family:Georgia,serif;font-size:22px;fill:#eaf4ff}'''
    return f'<html><style>{css}</style><svg viewBox="0 0 1600 940"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4z" fill="#dceaff"/></marker></defs>{"".join(p)}</svg></html>'