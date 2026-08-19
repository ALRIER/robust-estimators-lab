"""Didactic defense schematic of the implemented thesis GA.

This module never runs an optimisation. It expands the original one-screen
architecture into a scrollable explanation while preserving the documented
search, fitness, freeze, gate, and configuration logic.
"""


def _matrix_cells() -> str:
    cells = []
    for r in range(6):
        for c in range(7):
            cls = "cell hi" if (r + 2 * c) % 5 == 0 else "cell"
            cells.append(f'<span class="{cls}"></span>')
    return "".join(cells)


def _weight_bars() -> str:
    widths = (28, 58, 38, 72, 46)
    return "".join(f'<span class="wbar" style="width:{w}%"></span>' for w in widths)


def _config_cards() -> str:
    config = (
        ("POP", "N = 100", "Population size used by the implemented search."),
        ("FOLDS", "K = 3", "Search is organised across three folds."),
        ("GEN", "G = 20 / fold", "Twenty generations are run inside each fold."),
        ("SEEDS", "101 · 202", "Documented search seeds shown in the thesis architecture."),
        ("MUT", "μ₀ = .12 / .18", "Initial mutation settings used by the search."),
        ("MIN MUT", "μmin = .05", "Lower mutation setting retained during evolution."),
        ("IMM", "5–10% / 15 gen", "Immigration configuration retained from the implemented GA."),
        ("STOP", "5 gen · p=3 · δ=.005", "Stopping rule shown exactly as configured."),
    )
    return "".join(
        f"<div class='config'><div class='configlab'>{lab}</div><div class='configval'>{val}</div><div class='configcopy'>{copy}</div></div>"
        for lab, val, copy in config
    )


def thesis_ga_architecture_svg() -> str:
    """Return the current full-scroll Layer 6 thesis GA architecture."""
    matrix = _matrix_cells()
    weights = _weight_bars()
    configs = _config_cards()
    return f"""
    <html>
    <style>
      *{{box-sizing:border-box}}
      body{{margin:0;background:#081525;color:#e9f4ff;font-family:Arial,sans-serif}}
      .page{{padding:30px 34px 44px;background:#081525}}
      .kicker{{font-size:14px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin-bottom:9px}}
      .title{{font-size:39px;line-height:1.15;font-weight:900;color:#fff;margin-bottom:10px}}
      .subtitle{{font-size:19px;line-height:1.5;color:#bfd0e2;max-width:1280px;margin-bottom:22px}}
      .badge{{display:inline-block;padding:8px 12px;border:1px solid #3c7198;border-radius:18px;color:#72cfff;background:#0e2945;font-size:13px;font-weight:900;letter-spacing:.08em;margin-bottom:26px}}
      .section{{background:#091a2e;border:1px solid #2d6d9c;border-radius:18px;padding:28px 30px;margin:0 0 30px}}
      .section-title{{font-size:31px;line-height:1.2;font-weight:900;color:#fff;margin-bottom:8px}}
      .section-sub{{font-size:18px;line-height:1.5;color:#bfd0e2;margin-bottom:22px;max-width:1250px}}
      .visual{{background:#0b2036;border:1px solid #3d749b;border-radius:16px;padding:26px;margin:16px 0 22px}}
      .three{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}}
      .two{{display:grid;grid-template-columns:1fr 1fr;gap:17px}}
      .support{{background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:14px;padding:18px 19px;min-height:155px}}
      .support .lab{{font-size:13px;font-weight:900;letter-spacing:.09em;color:#72cfff;margin-bottom:7px}}
      .support .head{{font-size:20px;font-weight:900;color:#fff;margin-bottom:7px}}
      .support .copy{{font-size:16px;line-height:1.47;color:#dce9f8}}
      .take{{background:#12354a;border:1px solid #58aee8;border-left:7px solid #f3c743;border-radius:14px;padding:20px 22px;margin-top:22px;font-size:19px;line-height:1.46;font-weight:850;color:#fff}}
      .formula{{font-family:Georgia,serif;color:#f3c743;font-size:27px;font-weight:800;line-height:1.4}}
      .formula-small{{font-family:Georgia,serif;color:#f3c743;font-size:21px;font-weight:800}}
      .tiny-note{{font-size:14px;line-height:1.45;color:#a9c0d5;margin-top:9px}}

      /* Section 1 */
      .matrix-wrap{{display:grid;grid-template-columns:minmax(420px,1.35fr) 90px minmax(170px,.55fr) 80px minmax(260px,.85fr);align-items:center;gap:20px}}
      .matrix-card,.weight-card,.output-card{{background:#102a45;border:1px solid #3b78a4;border-radius:15px;padding:20px;min-height:335px}}
      .matrix-card{{display:flex;flex-direction:column;justify-content:center}}
      .matrix-grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;margin:18px 8px}}
      .cell{{height:27px;border-radius:4px;background:#214967}} .cell.hi{{background:#58aee8}}
      .matrix-label{{font-family:Georgia,serif;font-size:40px;font-weight:900;color:#f3c743;text-align:center}}
      .times,.big-arrow{{font-size:42px;font-weight:900;color:#dceaff;text-align:center}}
      .weight-card{{display:flex;flex-direction:column;justify-content:center;align-items:stretch}}
      .wbar{{height:17px;border-radius:4px;background:#a777e3;margin:9px 0}}
      .output-card{{display:flex;flex-direction:column;justify-content:center;text-align:center}}
      .output-card .formula{{font-size:34px}}

      /* Section 2 */
      .evo-track{{display:grid;grid-template-columns:1fr 52px 1fr 52px 1fr 52px 1fr 52px 1fr;align-items:start;gap:4px;margin:18px 0}}
      .node-wrap{{text-align:center}}
      .node{{width:140px;height:140px;border-radius:50%;margin:0 auto;background:#143552;border:3px solid #58aee8;display:flex;flex-direction:column;align-items:center;justify-content:center}}
      .node .num{{font-size:31px;font-weight:900;color:#f3c743;line-height:1}}
      .node .name{{font-size:14px;font-weight:900;color:#fff;margin-top:8px}}
      .node-copy{{font-size:15px;line-height:1.42;color:#dce9f8;margin-top:12px;min-height:65px}}
      .arrow{{font-size:40px;color:#dceaff;text-align:center;padding-top:45px}}
      .mini-viz{{height:95px;margin-top:10px;display:flex;align-items:flex-end;justify-content:center;gap:8px}}
      .bar{{width:16px;border-radius:3px;background:#58aee8}} .ghost{{width:22px;height:22px;border-radius:50%;background:#45627a}} .sel{{width:22px;height:22px;border-radius:50%;background:#54c786;border:2px solid #b7ffca}}
      .parentA,.parentB,.child{{height:14px;border-radius:4px}} .parentA{{width:52px;background:#58aee8}} .parentB{{width:52px;background:#a777e3}} .child{{width:65px;background:#f3c743}}
      .mutA{{width:16px;background:#5f7892;border-radius:3px}} .mutB{{width:16px;background:#63dfa2;border-radius:3px}}
      .dotgold{{width:28px;height:28px;border-radius:50%;background:#f3c743}} .dotimm{{width:28px;height:28px;border-radius:50%;background:#72cfff;border:2px solid #e8f8ff}}
      .loopline{{margin:24px auto 0;border-top:3px dashed #a777e3;max-width:930px;text-align:center;color:#c5aaf0;padding-top:13px;font-size:15px;font-weight:800}}

      /* Section 3 */
      .claim-flow{{max-width:690px;margin:0 auto;display:flex;flex-direction:column;align-items:center}}
      .flowbox{{width:100%;border-radius:16px;padding:20px 24px;text-align:center;background:#192f4b;border:2px solid #a777e3}}
      .flowbox.candidate{{max-width:560px;border-color:#f3c743;background:#17354f}} .flowbox.freeze{{max-width:560px;border-color:#f3c743;background:#193d5e}}
      .down{{font-size:38px;color:#dceaff;line-height:1.1;margin:5px 0}}
      .flowhead{{font-size:19px;font-weight:900;letter-spacing:.08em;color:#72cfff;margin-bottom:8px}}
      .flowcopy{{font-size:16px;line-height:1.45;color:#dce9f8}}
      .gatebox{{max-width:560px;width:100%;background:#0d2842;border:2px solid #58aee8;border-radius:16px;padding:19px;text-align:center}}

      /* Section 4 */
      .claim-band{{display:grid;grid-template-columns:1fr 90px 1fr 260px;gap:17px;align-items:center;background:#0d2842;border:1px solid #4c86ad;border-radius:16px;padding:22px}}
      .claim-head{{font-size:21px;font-weight:900;color:#fff;margin-bottom:7px}}
      .decision{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
      .pass,.retain{{padding:18px 10px;border-radius:12px;text-align:center;font-size:16px;font-weight:900}}
      .pass{{background:#123d30;border:2px solid #54c786;color:#c8ffd7}} .retain{{background:#382335;border:2px solid #ff825f;color:#ffd6cc}}
      .config-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:19px}}
      .config{{background:#0a1c31;border:1px solid #2d6d9c;border-radius:13px;padding:17px;min-height:145px}}
      .configlab{{font-size:12px;font-weight:900;letter-spacing:.09em;color:#72cfff}}
      .configval{{font-size:21px;font-weight:900;color:#fff;margin:7px 0}}
      .configcopy{{font-size:14px;line-height:1.42;color:#b9ccdf}}
      @media(max-width:1050px){{.three,.two,.config-grid{{grid-template-columns:1fr 1fr}}.matrix-wrap{{grid-template-columns:1fr}}.times,.big-arrow{{transform:rotate(90deg)}}.evo-track{{grid-template-columns:1fr}}.arrow{{padding:0;transform:rotate(90deg)}}.claim-band{{grid-template-columns:1fr}}}}
    </style>
    <div class='page'>
      <div class='kicker'>06 · THESIS GA ARCHITECTURE</div>
      <div class='title'>The real thesis GA, explained one stage at a time.</div>
      <div class='subtitle'>Layer 5 showed evolution pedagogically. This page documents the implemented search-and-claim architecture without running optimization or recomputing thesis evidence.</div>
      <div class='badge'>THESIS METHOD · SCHEMATIC ONLY · SCROLL DOWN</div>

      <div class='section'>
        <div class='kicker'>1 · MONTE CARLO → MATRIX C</div>
        <div class='section-title'>First, repeated estimator outputs become a scoring matrix.</div>
        <div class='section-sub'>This is the object the GA searches over. The algorithm changes the weight vector, not the raw observations and not the scientific target.</div>
        <div class='visual'>
          <div class='matrix-wrap'>
            <div class='matrix-card'><div class='tiny-note'>Rows = Monte Carlo replications · columns = named estimators</div><div class='matrix-grid'>{matrix}</div><div class='matrix-label'>C</div></div>
            <div class='times'>×</div>
            <div class='weight-card'><div class='tiny-note'>candidate simplex weights</div>{weights}<div class='matrix-label'>w</div></div>
            <div class='big-arrow'>→</div>
            <div class='output-card'><div class='kicker'>FAST CANDIDATE SCORING</div><div class='formula'>Cw</div><div class='tiny-note'>one composite output for every replication</div></div>
          </div>
        </div>
        <div class='three'>
          <div class='support'><div class='lab'>WHAT IS C?</div><div class='head'>A reusable Monte Carlo output matrix</div><div class='copy'>Each row is one replication. Each column is one named base estimator. Once C is built, the same repeated-sampling evidence can score many candidate mixtures.</div></div>
          <div class='support'><div class='lab'>WHAT DOES THE GA CHANGE?</div><div class='head'>Only the weights w</div><div class='copy'>The candidate is an interpretable recipe over existing estimators. The GA does not rewrite observations, change θ, or invent a new black-box predictor.</div></div>
          <div class='support'><div class='lab'>WHY Cw?</div><div class='head'>Fast candidate evaluation</div><div class='copy'>Multiplying C by w gives the composite output across all replications. That makes repeated candidate scoring practical during evolution.</div></div>
        </div>
        <div class='take'>READ IT THIS WAY: Monte Carlo creates C → the GA proposes w → Cw gives the composite outputs that can be scored.</div>
      </div>

      <div class='section'>
        <div class='kicker'>2 · SIMPLEX-SAFE EVOLUTION LOOP</div>
        <div class='section-title'>Then the GA evolves valid weight vectors across generations and folds.</div>
        <div class='section-sub'>The original loop is preserved, but each operator now has one simple job: create valid candidates, prefer promising ones, combine them, explore nearby recipes, and protect diversity.</div>
        <div class='visual'>
          <div class='evo-track'>
            <div class='node-wrap'><div class='node'><div class='num'>1</div><div class='name'>DIRICHLET INIT</div></div><div class='node-copy'>Start with valid simplex proportions.</div><div class='mini-viz'><span class='bar' style='height:45px'></span><span class='bar' style='height:24px'></span><span class='bar' style='height:70px'></span><span class='bar' style='height:37px'></span></div></div>
            <div class='arrow'>→</div>
            <div class='node-wrap'><div class='node'><div class='num'>2</div><div class='name'>SELECTION</div></div><div class='node-copy'>Tournament 2 / 3 gives better candidates more chances to reproduce.</div><div class='mini-viz'><span class='ghost'></span><span class='sel'></span><span class='ghost'></span><span class='sel'></span></div></div>
            <div class='arrow'>→</div>
            <div class='node-wrap'><div class='node'><div class='num'>3</div><div class='name'>CROSSOVER</div></div><div class='node-copy'>Convex blending combines promising parent recipes.</div><div class='mini-viz' style='flex-wrap:wrap'><span class='parentA'></span><span class='parentB'></span><span class='child'></span></div></div>
            <div class='arrow'>→</div>
            <div class='node-wrap'><div class='node'><div class='num'>4</div><div class='name'>MUTATION</div></div><div class='node-copy'>A Dirichlet nudge explores a nearby simplex direction.</div><div class='mini-viz'><span class='mutA' style='height:35px'></span><span class='mutA' style='height:58px'></span><span class='mutA' style='height:29px'></span><span style='font-size:26px;color:#dceaff'>→</span><span class='mutB' style='height:49px'></span><span class='mutB' style='height:37px'></span><span class='mutB' style='height:65px'></span></div></div>
            <div class='arrow'>→</div>
            <div class='node-wrap'><div class='node'><div class='num'>5</div><div class='name'>DIVERSITY</div></div><div class='node-copy'>Elitism keeps strong candidates; immigration adds fresh ones.</div><div class='mini-viz'><span class='dotgold'></span><span class='dotgold'></span><span class='dotimm'></span></div></div>
          </div>
          <div class='loopline'>repeat across generations / folds ↺</div>
        </div>
        <div class='three'>
          <div class='support'><div class='lab'>WHY DIRICHLET?</div><div class='head'>Valid mixtures from the start</div><div class='copy'>Candidates begin inside the simplex, so weights remain interpretable proportions rather than unconstrained coefficients.</div></div>
          <div class='support'><div class='lab'>WHY MUTATION + IMMIGRATION?</div><div class='head'>Search without collapsing too early</div><div class='copy'>Mutation explores nearby recipes while immigration injects fresh candidates. The purpose is diversity, not evidence generation.</div></div>
          <div class='support'><div class='lab'>WHAT DOES NOT CHANGE?</div><div class='head'>The target and the evidence matrix</div><div class='copy'>Evolution changes w. It does not change the known target θ or the Monte Carlo outputs already stored in C.</div></div>
        </div>
        <div class='take'>READ IT THIS WAY: valid candidates → selective reproduction → controlled variation → preserved diversity → repeat.</div>
      </div>

      <div class='section'>
        <div class='kicker'>3 · SEARCH ≠ CLAIM</div>
        <div class='section-title'>A strong fitness value creates a candidate — not a defended result.</div>
        <div class='section-sub'>This separation is central to the thesis architecture. Fitness guides the evolutionary search; fresh held-out evidence controls whether replacement is supported.</div>
        <div class='visual'>
          <div class='claim-flow'>
            <div class='flowbox'><div class='flowhead'>FITNESS</div><div class='formula-small'>0.70 q95 + 0.30 max loss</div><div class='flowcopy'>+ regularisation · used as selection pressure inside the GA</div></div>
            <div class='down'>↓</div>
            <div class='flowbox candidate'><div class='flowhead'>CANDIDATE w*</div><div class='flowcopy'>Promising — not confirmed.</div></div>
            <div class='down'>↓</div>
            <div class='flowbox freeze'><div class='flowhead'>FREEZE WEIGHTS</div><div class='flowcopy'>The recipe is locked before confirmation evidence is evaluated.</div></div>
            <div class='down'>↓</div>
            <div class='gatebox'><div class='flowhead'>HELD-OUT DUAL GATE</div><div class='flowcopy'>Independent evidence determines whether the candidate can replace the strongest admissible benchmark.</div></div>
          </div>
        </div>
        <div class='three'>
          <div class='support'><div class='lab'>FITNESS</div><div class='head'>Where should the GA look?</div><div class='copy'>Fitness ranks candidates during search. It is an optimization signal, not the final evidentiary statement.</div></div>
          <div class='support'><div class='lab'>FREEZE</div><div class='head'>Stop adapting before confirmation</div><div class='copy'>Once w* is selected, its weights are locked. The candidate cannot retrain itself on the evidence used to confirm it.</div></div>
          <div class='support'><div class='lab'>GATE</div><div class='head'>Is replacement supported?</div><div class='copy'>The final claim depends on held-out risk evidence. If the dual gate is not supported, the benchmark stays.</div></div>
        </div>
        <div class='take'>KEY SENTENCE: fitness guides search; the gate controls the claim.</div>
      </div>

      <div class='section'>
        <div class='kicker'>4 · CLAIM CONTROL + IMPLEMENTED CONFIGURATION</div>
        <div class='section-title'>The final architecture makes abstention explicit and keeps the search settings auditable.</div>
        <div class='section-sub'>These are the elements that sat at the bottom of the original graphic. They are now expanded so the committee can read what they mean without decoding a compressed strip.</div>
        <div class='visual'>
          <div class='claim-band'>
            <div><div class='claim-head'>FITNESS GUIDES SEARCH</div><div class='tiny-note'>selection pressure inside the GA</div></div>
            <div class='big-arrow'>→</div>
            <div><div class='claim-head'>GATE CONTROLS THE CLAIM</div><div class='formula-small'>ΔMSE ≥ 0 &nbsp; AND &nbsp; Δq95 ≥ 0</div><div class='tiny-note'>both criteria must support replacement</div></div>
            <div class='decision'><div class='pass'>PASS</div><div class='retain'>RETAIN</div></div>
          </div>
          <div class='config-grid'>{configs}</div>
        </div>
        <div class='three'>
          <div class='support'><div class='lab'>PASS</div><div class='head'>Replacement is supported</div><div class='copy'>A candidate can move forward only when both mean MSE and q95 evidence support improvement relative to the admissible benchmark.</div></div>
          <div class='support'><div class='lab'>RETAIN</div><div class='head'>Keeping the benchmark is valid</div><div class='copy'>If one criterion does not support replacement, the architecture retains the benchmark rather than forcing a GA win.</div></div>
          <div class='support'><div class='lab'>CONFIGURATION</div><div class='head'>Search settings are visible</div><div class='copy'>Population, folds, generations, seeds, mutation, immigration and stopping settings remain explicit so the implemented GA can be audited.</div></div>
        </div>
        <div class='take'>TAKE-HOME: the GA is an interpretable search mechanism inside a larger evidence-control system. Search proposes; frozen validation decides.</div>
      </div>
    </div>
    </html>
    """
