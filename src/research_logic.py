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


def research_logic_svg(panel: int) -> str:
    """Render five distinct scenes in the existing single Research Logic canvas."""
    panel = max(0, min(int(panel), 4))
    headings = ("PROBLEM", "OBJECTIVE / RESEARCH QUESTIONS", "H1–H4: CAUSAL HYPOTHESIS CHAIN", "TARGET / SIMPLEX", "WHY A COMPOSITE CAN WIN")
    claims = (
        "No single admissible estimator remains uniformly reliable across changing regimes.",
        "Can evolutionary search find credible, interpretable improvement in E[X]?",
        "No universal winner → regime dependence → selective GA help → benchmark gate.",
        "The target stays fixed: θ = E[X]. The GA learns inspectable estimator weights.",
        "A composite wins only when variance reduction exceeds its squared bias cost.",
    )
    p = ['<rect x="20" y="16" width="1560" height="904" rx="18" class="canvas"/>', _t(48, 56, "01 · RESEARCH LOGIC", "kicker"), _t(48, 100, headings[panel], "title"), _t(48, 137, claims[panel], "claim")]
    def card(x, y, w, h, title, lines, cls="card"):
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}"/>'); p.append(_t(x+20, y+32, title, "head")); p.extend(_t(x+20, y+62+i*22, line, "body") for i,line in enumerate(lines))
    def rail(lines, why, next_):
        card(1260,170,300,705,"WHAT THIS MEANS",lines,"rail"); p.extend([_t(1280,310,"WHY IT MATTERS","kicker"),_t(1280,340,why,"railtext"),_t(1280,410,"NEXT","kicker"),_t(1280,440,next_,"railtext")])
    if panel == 0:
        card(48,185,520,350,"CLEAN / NEAR-SYMMETRIC",["Mean is close to the target.","Mean — efficient here."],"scene")
        p.extend(['<path d="M100 435 C180 275 350 275 520 435" class="curve"/>','<path d="M310 268 V465" class="target"/>','<circle cx="310" cy="382" r="10" class="mean"/>',_t(310,495,"population mean","small","middle"),'<path d="M590 355 L750 355" class="bigarrow" marker-end="url(#arrow)"/>',_t(670,320,"change regime","gold","middle"),_t(670,350,"change risk · change ranking","gold","middle")])
        card(800,185,400,350,"SKEWED / CONTAMINATED",["Outliers pull the mean away.","Robust estimators move less."],"warn")
        p.extend(['<path d="M840 435 C900 285 980 300 1020 415 C1100 440 1140 350 1175 250" class="curvewarn"/>','<path d="M965 268 V465" class="target"/>','<circle cx="1080" cy="382" r="10" class="mean"/>','<circle cx="985" cy="382" r="10" class="robust"/>',_t(1080,415,"Mean","small","middle"),_t(985,415,"Robust","small","middle")])
        rail(["The same estimator can be","excellent here and poor there."],"The regime changes the ranking.","Can a mixture be justified?")
    elif panel == 1:
        card(48,175,1150,95,"AIM",["Determine whether evolutionary search identifies interpretable E[X] improvements that remain credible after optimisation."],"hero")
        for i,(name,desc) in enumerate((("SEARCH","Find candidate recipes"),("CHALLENGE","Freeze; test new seeds"),("ACCEPT / ABSTAIN","Gate decides the claim"))):
            x=65+i*380;card(x,320,315,105,name,[desc],"step")
            if i<2:p.append(f'<path d="M{x+325} 372 L{x+360} 372" class="arrow" marker-end="url(#arrow)"/>')
        rqs=(("RQ1 · Discovery","Where can a GA composite improve?","Discovery + held-out gate."),("RQ2 · Confirmation","Do gains remain after search?","Frozen confirmation."),("RQ3 · Expanded basis","What changes from 10 to 26?","Expanded rediscovery."),("RQ4 · External transfer","Do specialists transfer?","External evidence."))
        for i,(label,q,stage) in enumerate(rqs): card(48+i*290,480,270,165,label,[q,stage],"rqactive" if i==0 else "card")
        rail(["One programme answers four","questions: discovery then credibility."],"Finding is not confirming.","Next: predictions before results.")
    elif panel == 2:
        data=(("H1","No universal estimator.","Changing winners across regimes."),("H2","Performance depends on regime.","Risk maps vary by conditions."),("H3","GA helps only selectively.","Only a subset should pass."),("H4","The gate prevents false claims.","Benchmarks can be retained."))
        for i,(h,claim,evidence) in enumerate(data):
            x=48+i*292;card(x,195,268,355,h,[claim,"","PREDICTION",evidence,"","EVIDENCE USED LATER","Later experiment stage"],"hyp")
            if i<3:p.append(f'<path d="M{x+272} 375 L{x+286} 375" class="arrow" marker-end="url(#arrow)"/>')
        p.extend([_t(620,635,"H1  →  H2  →  H3  →  H4","chain","middle"),_t(620,670,"A causal reasoning chain, not four unrelated statements.","body","middle")])
        rail(["These are predictions before","the final results are shown."],"The gate makes abstention valid.","Next: what does GA change?")
    elif panel == 3:
        card(48,190,300,335,"FIXED TARGET",["Population mean E[X].","Every candidate aims here."],"scene")
        p.extend(['<path d="M100 440 C175 285 270 285 325 440" class="curve"/>','<path d="M210 268 V460" class="target"/>',_t(210,490,"θ","gold","middle")])
        card(400,190,410,335,"CANDIDATE RECIPE",["Each individual is a weight recipe.","Named components remain inspectable."],"scene")
        for i,(name,w) in enumerate(zip(("Mean","Median","Huber","Biweight"),(18,27,24,31))):
            y=325+i*44;p.extend([_t(430,y,name,"small"),f'<rect x="525" y="{y-17}" width="{w*6}" height="20" rx="4" class="weight"/>',_t(735,y,f"{w}%","small","end")])
        p.extend([_t(605,510,"weights sum to 100%","gold","middle"),'<path d="M835 355 L920 355" class="bigarrow" marker-end="url(#arrow)"/>']);card(950,265,250,165,"INTERPRETABLE MIXTURE",["θ̂(w,x) = Σ wⱼTⱼ(x)","wⱼ ≥ 0  ·  Σwⱼ = 1"],"hero")
        rail(["The target is fixed; only the","estimator recipe can change."],"Simplex weights are auditable.","Next: why could it improve?")
    else:
        card(48,180,1150,95,"CLEAN NORMAL",["The sample mean is already efficient: little room for improvement."],"hero")
        for i,(name,w,col) in enumerate((("Sample mean variance",120,"#ff825f"),("Composite variance",105,"#58aee8"),("Composite bias²",85,"#f3c743"))):
            y=350+i*90;p.extend([_t(95,y,name),f'<rect x="360" y="{y-24}" width="{w*2.4}" height="38" rx="6" fill="{col}"/>',_t(380+w*2.4,y+2,str(w),"small")])
        card(850,350,325,165,"LITTLE ROOM",["Bias² + Variance  ≥  Var(X̄)","GA searches; Monte Carlo measures;","the benchmark gate decides."],"scene")
        rail(["MSE = bias² + variance.","A composite is never guaranteed."],"Theory predicts conditional opportunity.","Simulation must measure true error.")
    technical = (
        ("STATISTICAL SUPPORT", "Regime: R = {family, n, ε, mechanism}     ·     sample: x ∼ R     ·     compare risk: R(T̄, R) vs R(Trobust, R)"),
        ("STATISTICAL SUPPORT", "Experiment logic: R → x → {T₁(x), …, Tᴸ(x)} → w → benchmark gate     ·     target: θ = E[X]"),
        ("STATISTICAL SUPPORT", "Risk is conditional: R(T, R) = E[(T(x) − θ)² | R]     ·     evidence uses MSE, q95 and benchmark retention"),
        ("STATISTICAL SUPPORT", "θ̂w,n = Σⱼ₌₁ᴸ wⱼTⱼ,n(x)     ·     wⱼ ≥ 0     ·     Σⱼ wⱼ = 1     ·     interpretable convex mixture"),
        ("STATISTICAL SUPPORT", "MSE(θ̂) = Bias(θ̂)² + Var(θ̂)     ·     improvement only if MSE(θ̂w) < MSE(best admissible benchmark)"),
    )[panel]
    p += ['<rect x="48" y="720" width="1150" height="140" rx="14" class="technical"/>', _t(72, 755, technical[0], "kicker"), _t(72, 795, technical[1], "techtext"), _t(72, 832, "Technical notation supports the speech; the visual argument above remains the main reading path.", "small")]
    css='''body{margin:0;background:#081525;font-family:Arial,sans-serif}svg{width:100%;height:920px}.canvas{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}.kicker{font-size:12px;font-weight:800;letter-spacing:1.5px;fill:#72cfff}.title{font-size:28px;font-weight:800;fill:#f5f9ff}.claim{font-size:17px;font-weight:700;fill:#dceaff}.body{font-size:14px;fill:#dce9f8}.small{font-size:12px;fill:#bdd0e2}.gold{font-size:14px;font-weight:800;fill:#f3c743}.head{font-size:15px;font-weight:800;fill:#f5f9ff}.card,.scene,.step,.hyp{fill:#0d2741;stroke:#397daa;stroke-width:1.4}.warn{fill:#382335;stroke:#ff825f;stroke-width:1.8}.hero,.rqactive{fill:#102d4b;stroke:#f3c743;stroke-width:1.8}.rail{fill:#0b2138;stroke:#4b84ad;stroke-width:1.3}.technical{fill:#0a1c31;stroke:#2d6d9c;stroke-width:1.3}.railtext{font-size:13px;fill:#dce9f8}.techtext{font-family:Georgia,serif;font-size:16px;fill:#f3c743}.curve{stroke:#58aee8;stroke-width:4;fill:none}.curvewarn{stroke:#ff825f;stroke-width:4;fill:none}.target{stroke:#f3c743;stroke-width:3;stroke-dasharray:7 5}.mean{fill:#ff825f}.robust{fill:#63dfa2}.arrow,.bigarrow{stroke:#72cfff;stroke-width:3;fill:none}.bigarrow{stroke-width:5}.chain{font-size:24px;font-weight:800;fill:#f3c743}.weight{fill:#58aee8}'''
    return f'<html><style>{css}</style><svg viewBox="0 0 1600 940"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4z" fill="#dceaff"/></marker></defs>{"".join(p)}</svg></html>'
