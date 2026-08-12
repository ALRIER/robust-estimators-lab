"""Dedicated opening scenes for the thesis-defense research logic."""

PANELS = (
    ("1 · Problem", "No single admissible estimator remains uniformly reliable across skewed, heavy-tailed, contaminated, and sample-size-varying regimes."),
    ("2 · Objective / RQs", "Determine whether evolutionary search can find interpretable combinations that improve E[X] under defined regimes — and whether those gains remain credible after optimisation ends."),
    ("3 · H1–H4", "The hypotheses form one causal argument, not four disconnected predictions."),
    ("4 · Target / Simplex", "The target never changes: θ = E[X]. The GA changes the estimator by changing interpretable weights."),
    ("5 · Why can win", "A composite wins only when the variance reduction it buys is larger than the squared bias it introduces."),
)

PRESENTER_GUIDES = (
    "The mean is not always bad, and robust estimators are not always good. Ranking changes with the data-generating regime, so this thesis asks when a composite is supported — never whether it wins everywhere.",
    "The objective has two parts: discover opportunity, then establish credibility after search. RQ1 asks where; RQ2 asks if it survives; RQ3 expands the basis; RQ4 examines compatible public data.",
    "No universal winner means regime-dependent performance; that makes GA help selective; the gate prevents unsupported claims.",
    "The GA learns an auditable recipe over named estimators while every candidate aims at the same population mean.",
    "Clean symmetry leaves little room. Difficult regimes can create opportunity, but the GA only searches: Monte Carlo and the gate decide support.",
)


def _t(x, y, value, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{value}</text>'


def _scene_text(x, y, value, cls="body", anchor="start"):
    return _t(x, y, value, cls, anchor)


def _scene_box(parts, x, y, w, h, heading, lines, cls="card"):
    parts += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}"/>', _scene_text(x + 20, y + 32, heading, "head")]
    parts += [_scene_text(x + 20, y + 62 + i * 23, line) for i, line in enumerate(lines)]


def _scene_rail(parts, meaning, why, next_step):
    _scene_box(parts, 1260, 175, 300, 555, "WHAT THIS MEANS", meaning, "rail")
    parts += [_scene_text(1280, 320, "WHY IT MATTERS", "kicker"), _scene_text(1280, 350, why, "railtext"),
              _scene_text(1280, 420, "NEXT", "kicker"), _scene_text(1280, 450, next_step, "railtext")]


def research_logic_scene(panel: int, detail: int = 0) -> str:
    """Five different explanatory scenes, all displayed in the same Layer 1 canvas."""
    panel = max(0, min(int(panel), 4)); detail = max(0, int(detail))
    title, statement = PANELS[panel][:2]
    parts = ['<rect x="20" y="16" width="1560" height="764" rx="18" class="canvas"/>', _scene_text(45, 58, "01 · RESEARCH LOGIC", "kicker"), _scene_text(45, 105, title, "title"), _scene_text(45, 147, statement, "statement")]
    if panel == 0:
        _scene_box(parts, 45, 190, 530, 360, "CLEAN / NEAR-SYMMETRIC", ["Mean is close to the target", "Mean — efficient here"], "scene")
        parts += ['<path d="M95 445 C170 280 340 280 520 445" class="curve"/>', '<path d="M310 275 V470" class="target"/>', '<circle cx="310" cy="390" r="10" class="mean"/>', _scene_text(310, 510, "population mean", "small", "middle"), _scene_text(332, 396, "Mean", "small"), '<path d="M600 365 L755 365" class="bigarrow" marker-end="url(#arrow)"/>', _scene_text(678, 322, "change the regime", "gold", "middle"), _scene_text(678, 354, "→ change risk → change ranking", "gold", "middle")]
        _scene_box(parts, 800, 190, 400, 360, "SKEWED / CONTAMINATED", ["Outliers pull the mean away", "Robust estimators move less"], "warn")
        parts += ['<path d="M840 445 C900 285 985 305 1025 425 C1100 440 1140 360 1175 255" class="curvewarn"/>', '<path d="M965 275 V470" class="target"/>', '<circle cx="1085" cy="390" r="10" class="mean"/>', '<circle cx="985" cy="390" r="10" class="robust"/>', _scene_text(1085, 420, "Mean", "small", "middle"), _scene_text(985, 420, "Robust", "small", "middle")]
        _scene_rail(parts, ["The same estimator can be", "excellent here and poor there."], "The regime changes the ranking.", "Can a mixture be justified?")
    elif panel == 1:
        _scene_box(parts, 45, 180, 1155, 105, "AIM", ["Can evolutionary search identify interpretable combinations that improve E[X] — and remain credible after optimisation ends?"], "hero")
        for i, (name, desc) in enumerate((("SEARCH", "Find candidate recipes"), ("CHALLENGE", "Freeze; test new seeds"), ("ACCEPT / ABSTAIN", "Gate decides the claim"))):
            x = 65 + i * 380; _scene_box(parts, x, 330, 315, 105, name, [desc], "step")
            if i < 2: parts.append(f'<path d="M{x+325} 382 L{x+360} 382" class="arrow" marker-end="url(#arrow)"/>')
        rqs = (("RQ1 · Discovery", "Where can a GA composite improve?", "Discovery + held-out gate."), ("RQ2 · Confirmation", "Do gains remain after search?", "Frozen confirmation."), ("RQ3 · Expanded basis", "What changes from 10 to 26?", "Expanded rediscovery."), ("RQ4 · External transfer", "Do specialists transfer?", "External evidence."))
        for i, (label, question, stage) in enumerate(rqs): _scene_box(parts, 45 + i * 290, 490, 270, 165, label, [question, stage], "active" if i == detail % 4 else "rq")
        _scene_rail(parts, ["One programme answers four", "questions: discovery then credibility."], "Finding is not confirming.", "Next: predictions before results.")
    elif panel == 2:
        data = (("H1", "No universal estimator.", "Prediction: winners change.", "Evidence: regime maps."), ("H2", "Performance depends on regime.", "Prediction: risk shifts.", "Evidence: performance maps."), ("H3", "GA helps only selectively.", "Prediction: subset passes.", "Evidence: confirmation."), ("H4", "The gate prevents false claims.", "Prediction: retain benchmarks.", "Evidence: pass/fail gate."))
        for i, (h, claim, prediction, evidence) in enumerate(data):
            x = 45 + i * 292; _scene_box(parts, x, 205, 268, 360, h, [claim, "", "PREDICTION", prediction, "", "EVIDENCE USED LATER", evidence], "hyp")
            if i < 3: parts.append(f'<path d="M{x+272} 385 L{x+286} 385" class="arrow" marker-end="url(#arrow)"/>')
        parts += [_scene_text(620, 640, "H1  →  H2  →  H3  →  H4", "chain", "middle"), _scene_text(620, 677, "A causal chain — not four isolated facts.", "body", "middle")]
        _scene_rail(parts, ["These are pre-result predictions,", "not final support statuses."], "The gate makes abstention valid.", "Next: what does GA change?")
    elif panel == 3:
        _scene_box(parts, 45, 195, 310, 340, "FIXED TARGET", ["Population mean E[X]", "Every candidate aims here"], "scene")
        parts += ['<path d="M100 450 C175 285 270 285 330 450" class="curve"/>', '<path d="M210 270 V470" class="target"/>', _scene_text(210, 500, "θ", "gold", "middle")]
        _scene_box(parts, 400, 195, 410, 340, "CANDIDATE RECIPE", ["Each individual is a weight recipe", "Named components remain inspectable"], "scene")
        for i, (name, weight) in enumerate(zip(("Mean", "Median", "Huber", "Biweight"), (18, 27, 24, 31))):
            y = 330 + i * 45; parts += [_scene_text(430, y, name, "small"), f'<rect x="525" y="{y-17}" width="{weight*6}" height="20" rx="4" class="weight"/>', _scene_text(735, y, f"{weight}%", "small", "end")]
        parts += [_scene_text(605, 520, "weights sum to 100%", "gold", "middle"), '<path d="M835 365 L920 365" class="bigarrow" marker-end="url(#arrow)"/>']
        _scene_box(parts, 950, 270, 250, 165, "INTERPRETABLE MIXTURE", [("θ̂(w,x) = Σ wⱼTⱼ(x)" if detail else "Composite estimate follows the recipe"), "Not a black-box predictor"], "hero")
        if detail: parts.append(_scene_text(1075, 402, "wⱼ ≥ 0   ·   Σwⱼ = 1", "formula", "middle"))
        _scene_rail(parts, ["Target fixed; estimator recipe", "changes with inspectable weights."], "Simplex weights are auditable.", "Next: why could it improve?")
    else:
        difficult = bool(detail); label = "SKEW / TAILS / CONTAMINATION" if difficult else "CLEAN NORMAL"; copy = "Risk rises: a robust mixture may create opportunity." if difficult else "The sample mean is already efficient: little room."
        _scene_box(parts, 45, 180, 1155, 105, label, [copy], "hero"); values = (270, 120, 70) if difficult else (120, 105, 85)
        for i, (name, value, color) in enumerate(zip(("Sample mean variance", "Composite variance", "Composite bias²"), values, ("#ff825f", "#58aee8", "#f3c743"))):
            y = 350 + i * 94; parts += [_scene_text(95, y, name), f'<rect x="360" y="{y-24}" width="{value*2.4}" height="38" rx="6" fill="{color}"/>', _scene_text(380 + value*2.4, y+2, str(value), "small")]
        _scene_box(parts, 850, 350, 325, 170, "SPECIALIST OPPORTUNITY" if difficult else "LITTLE ROOM", [("Bias² + Variance  <  Var(X̄)" if difficult else "Bias² + Variance  ≥  Var(X̄)"), "GA searches; Monte Carlo measures;", "the benchmark gate decides."], "scene")
        _scene_rail(parts, ["MSE = bias² + variance.", "A composite is never guaranteed."], "Theory predicts conditional opportunity.", "Simulation must measure true error.")
    css = '''body{margin:0;background:#081525;font-family:Arial,sans-serif}svg{width:100%;height:780px}.canvas{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}.kicker{font-size:12px;font-weight:800;letter-spacing:1.5px;fill:#72cfff}.title{font-size:29px;font-weight:800;fill:#f5f9ff}.statement{font-size:17px;font-weight:700;fill:#dceaff}.body{font-size:14px;fill:#dce9f8}.small{font-size:12px;fill:#bdd0e2}.gold{font-size:14px;font-weight:800;fill:#f3c743}.head{font-size:15px;font-weight:800;fill:#f5f9ff}.card,.scene,.step,.rq,.hyp{fill:#0d2741;stroke:#397daa;stroke-width:1.4}.warn{fill:#382335;stroke:#ff825f;stroke-width:1.8}.hero,.active{fill:#102d4b;stroke:#f3c743;stroke-width:1.8}.rail{fill:#0b2138;stroke:#4b84ad;stroke-width:1.3}.railtext{font-size:13px;fill:#dce9f8}.curve{stroke:#58aee8;stroke-width:4;fill:none}.curvewarn{stroke:#ff825f;stroke-width:4;fill:none}.target{stroke:#f3c743;stroke-width:3;stroke-dasharray:7 5}.mean{fill:#ff825f}.robust{fill:#63dfa2}.arrow,.bigarrow{stroke:#72cfff;stroke-width:3;fill:none}.bigarrow{stroke-width:5}.chain{font-size:24px;font-weight:800;fill:#f3c743}.weight{fill:#58aee8}.formula{font-family:Georgia,serif;font-size:17px;fill:#f3c743}'''
    return f'<html><style>{css}</style><svg viewBox="0 0 1600 800"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4z" fill="#dceaff"/></marker></defs>{"".join(parts)}</svg></html>'


def research_logic_svg(panel: int, detail: int = 0) -> str:
    return research_logic_scene(panel, detail)
    # Legacy renderer retained below only for source-history context.
    """A persistent causal flow; the selected panel only changes emphasis."""
    panel = max(0, min(int(panel), len(PANELS) - 1))
    title, what, why, say = PANELS[panel]
    width, height = 1600, 620
    nodes = ((145, "REGIME R", "family · n · contamination"), (410, "SAMPLE x", "known target θ"),
             (675, "ESTIMATOR BANK", "T₁(x) … Tᴸ(x)"), (940, "GA MIXTURE", "Σ wⱼTⱼ(x)"),
             (1205, "BENCHMARK GATE", "MSE AND q95"), (1470, "SELECTED", "only if supported"))
    highlight_ranges = ((0, 1), (0, 5), (0, 5), (2, 3), (0, 3))
    lo, hi = highlight_ranges[panel]
    body = ['<rect x="24" y="20" width="1552" height="575" rx="16" class="canvas"/>']
    body += [_t(72, 78, "RESEARCH LOGIC: WHY THE EXPERIMENT EXISTS", "kicker"),
             _t(72, 122, title, "title")]
    for i, (x, label, desc) in enumerate(nodes):
        active = lo <= i <= hi
        fill = "#22466e" if active else "#0d2137"
        stroke = "#f3c743" if active else "#386b91"
        body.append(f'<rect x="{x-105}" y="215" width="210" height="122" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{"2.5" if active else "1.2"}"/>')
        body += [_t(x, 260, label, "nodeactive" if active else "node", "middle"), _t(x, 298, desc, "small", "middle")]
        if i < len(nodes)-1:
            body.append(f'<path d="M{x+108} 276 L{x+155} 276" class="arrow" marker-end="url(#arrow)"/>')
    if panel == 0:
        body += [_t(270, 425, "clean sample", "small", "middle"), _t(530, 425, "contaminated sample", "small", "middle"),
                 '<path d="M150 470 C250 390 350 390 450 470" class="curve"/>', '<path d="M430 470 C520 340 650 400 710 470" class="curvewarn"/>']
    elif panel == 2:
        for i, h in enumerate((42, 56, 70, 84)):
            x=300+i*180; body += [f'<rect x="{x}" y="{520-h}" width="125" height="{h}" rx="5" class="hyp"/>', _t(x+62, 550, f"H{i+1}", "hyptext", "middle")]
    elif panel == 3:
        weights=(.10,.24,.31,.35); names=("Mean","Median","Huber","Biweight")
        for i,(name,weight) in enumerate(zip(names,weights)):
            x=190+i*220; body += [_t(x,420,name,"small","middle"),f'<rect x="{x-65}" y="440" width="130" height="{weight*230:.0f}" rx="5" class="weight"/>',_t(x,470,f"{weight:.0%}","weighttext","middle")]
        body += [_t(1090,445,"θ̂₍w,n₎ = Σⱼ₌₁ᴸ wⱼTⱼ,ₙ", "formula", "middle"), _t(1090,495,"wⱼ ≥ 0     Σ wⱼ = 1", "formula2", "middle")]
    elif panel == 4:
        body += [_t(670,440,"B² + V", "formula", "middle"), '<path d="M500 472 L845 510" class="balance"/>', '<path d="M675 420 L675 545" class="balance"/>', _t(970,490,"Var(X̄)","formula","middle"), _t(670,570,"B² + V  <  Var(X̄)","formula2","middle")]
    else:
        body += [_t(800,480,"θ = E[X]", "formula", "middle"), _t(800,530,"Discovery proposes; the benchmark gate decides.", "gold", "middle")]
    body += [f'<rect x="1080" y="375" width="420" height="175" rx="12" class="notecard"/>', _t(1110,415,"WHAT IT SHOWS", "kicker"), _t(1110,448,what,"note"), _t(1110,485,"WHY IT MATTERS", "kicker"), _t(1110,518,why,"note"), _t(1110,552,say,"say")]
    return f'''<html><style>body{{margin:0;background:#081525;font-family:Arial,sans-serif}}svg{{width:100%;height:620px}}.canvas{{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}}.kicker{{font-size:13px;font-weight:800;letter-spacing:1.5px;fill:#72cfff}}.title{{font-size:28px;font-weight:800;fill:#f5f9ff}}.node{{font-size:15px;font-weight:800;fill:#c6d8e9}}.nodeactive{{font-size:15px;font-weight:800;fill:#fff}}.small{{font-size:12px;fill:#b7cadc}}.arrow{{stroke:#639aca;stroke-width:3;fill:none}}.curve{{stroke:#58aee8;stroke-width:4;fill:none}}.curvewarn{{stroke:#ff825f;stroke-width:4;fill:none}}.hyp{{fill:#183b5c;stroke:#72cfff}}.hyptext{{font-size:18px;font-weight:800;fill:#f3c743}}.weight{{fill:#58aee8}}.weighttext{{font-size:16px;font-weight:800;fill:#fff}}.formula{{font-family:Georgia,serif;font-size:27px;fill:#f3c743}}.formula2{{font-family:Georgia,serif;font-size:20px;fill:#eaf4ff}}.balance{{stroke:#72cfff;stroke-width:5}}.notecard{{fill:#0d2741;stroke:#4a83ae;stroke-width:1.5}}.note{{font-size:14px;fill:#dce9f8}}.say{{font-size:14px;font-style:italic;fill:#f3c743}}.gold{{font-size:19px;font-weight:800;fill:#f3c743}}</style><svg viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4z" fill="#dceaff"/></marker></defs>{''.join(body)}</svg></html>'''
