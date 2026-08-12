"""Interactive opening scene for the written thesis research logic."""

PANELS = (
    ("Problem", "Estimator performance changes with the regime.", "No admissible estimator is uniformly reliable.", "The regime changes the problem."),
    ("Objective / RQ", "When can a GA mixture beat the strongest admissible benchmark?", "The question is conditional, never universal.", "We ask when, not whether always."),
    ("H1–H4", "Four claims organise the study.", "They separate opportunity, evidence, and scope.", "These hypotheses are the spine of the defense."),
    ("Target / Simplex", "The GA learns an interpretable convex estimator mixture.", "Every individual remains a valid estimator.", "Each candidate is a valid mixture."),
    ("Why can win", "Variance reduction must exceed the bias cost.", "Clean Normal data leave little room; contamination can create opportunity.", "A composite wins only when variance reduction pays for bias."),
)


def _t(x, y, value, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{value}</text>'


def research_logic_svg(panel: int) -> str:
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
