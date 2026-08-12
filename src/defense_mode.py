"""Manual defense scenes derived from the thesis and defense deck."""

SCENES = (
    "Cover",
    "Research framing",
    "Target & simplex",
    "Why a composite can win",
    "Data-generating world",
    "Monte Carlo engine",
    "What did we learn?",
)


def _t(x, y, text, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{text}</text>'


def defense_scene_svg(scene: int) -> str:
    scene = max(0, min(int(scene), len(SCENES) - 1))
    w, h = 1600, 760
    body = [f'<rect x="28" y="25" width="1544" height="710" rx="18" class="canvas"/>']
    if scene == 0:
        body += [_t(800, 220, "Building Better Estimators", "cover", "middle"), _t(800, 282, "Benchmark-gated, regime-conditional composite mean estimation", "subtitle", "middle"), _t(800, 322, "via genetic search", "subtitle", "middle"), '<path d="M520 410 L1080 410" class="rule"/>', _t(800, 480, "Alvaro Rivera-Eraso · MSc Artificial Intelligence · University of Hull", "body", "middle"), _t(800, 570, "A disciplined way to know when a composite estimator is justified.", "gold", "middle")]
    elif scene == 1:
        body += [_t(90, 105, "RESEARCH FRAMING", "kicker"), _t(90, 160, "Conditional estimator discovery — not universal GA superiority.", "title")]
        cards = ((120, "PROBLEM", "No admissible estimator is", "uniformly reliable."), (575, "OBJECTIVE", "Develop a benchmark-gated", "GA framework for E[X]."), (1030, "QUESTION", "Under which regimes can", "a composite outperform?"))
        for x, head, one, two in cards:
            body += [f'<rect x="{x}" y="250" width="350" height="170" rx="12" class="card"/>', _t(x+28, 292, head, "kicker"), _t(x+28, 340, one, "body"), _t(x+28, 370, two, "body")]
        for i, text in enumerate(("H1 No universal estimator", "H2 Regime matters", "H3 GA helps selectively", "H4 Gate controls claims")):
            body += [f'<rect x="{120+i*365}" y="510" width="320" height="72" rx="8" class="hyp"/>', _t(280+i*365, 553, text, "small", "middle")]
    elif scene == 2:
        body += [_t(90, 105, "WHAT IS BEING LEARNED?", "kicker"), _t(90, 160, "The target is fixed; the estimator is a convex mixture.", "title"), _t(800, 285, "θ̂₍w,n₎ = Σⱼ₌₁ᴸ wⱼ Tⱼ,ₙ", "formula", "middle"), _t(800, 345, "w ∈ Δᴸ = { w ∈ [0,1]ᴸ : Σⱼ₌₁ᴸ wⱼ = 1 }", "formula2", "middle")]
        for x, head, desc in ((170, "POSITIVE WEIGHTS", "No negative contribution."), (620, "SUM TO ONE", "Weights act as proportions."), (1070, "ADMISSIBILITY", "Components must be valid.")):
            body += [f'<circle cx="{x+165}" cy="470" r="48" class="node"/>', _t(x+165, 478, "w", "nodeletter", "middle"), _t(x+165, 550, head, "kicker", "middle"), _t(x+165, 585, desc, "small", "middle")]
    elif scene == 3:
        body += [_t(90, 105, "WHY CAN A COMPOSITE WIN?", "kicker"), _t(90, 160, "A win is possible only where variance reduction beats bias cost.", "title"), _t(800, 285, "B² + V  <  Var(X̄)", "formula", "middle"), _t(800, 335, "bias cost + composite variance  <  variance of the sample mean", "subtitle", "middle"), '<path d="M520 440 L1080 440" class="balance"/>', '<path d="M800 400 L800 525" class="balance"/>']
        body += [_t(510, 500, "Normal", "body", "middle"), _t(510, 535, "little room for improvement", "small", "middle"), _t(1090, 500, "Skew / tails / contamination", "body", "middle"), _t(1090, 535, "opportunity for a specialist", "gold", "middle")]
    elif scene == 4:
        body += [_t(90, 105, "DATA-GENERATING WORLD", "kicker"), _t(90, 160, "Simulation creates controlled regimes where true error is measurable.", "title")]
        items = (("6", "families"), ("5", "sample sizes"), ("8", "rates"), ("9", "scales"), ("8", "mechanisms"))
        for i, (num, label) in enumerate(items):
            x=150+i*270; body += [f'<rect x="{x}" y="260" width="210" height="155" rx="12" class="card"/>', _t(x+105, 325, num, "number", "middle"), _t(x+105, 370, label, "body", "middle")]
        body += [_t(800, 500, "9 scales × 8 rates × 8 mechanisms = 576 contamination profiles per family", "formula2", "middle"), _t(800, 550, "× 5 sample sizes = 2,880 regimes per family", "subtitle", "middle"), _t(800, 610, "The simulator is validated before any GA result is trusted.", "gold", "middle")]
    elif scene == 5:
        body += [_t(90, 105, "MONTE CARLO MEASUREMENT ENGINE", "kicker"), _t(90, 160, "The GA searches on certified error estimates; it does not create the target.", "title")]
        flow = (
            ("1", "Specify regime", "R = {family, n, γ, scale, mechanism}", "One controlled data-generating world.", "family = shape · n = sample size · γ = contamination rate", "scale = severity · mechanism = contamination pattern"),
            ("2", "Compute target", "θ = E[X]", "θ is the known population mean: the fixed truth.", "Every estimator is scored against this same target.", "It is not learned by the GA."),
            ("3", "Generate replicates", "x⁽¹⁾, …, x⁽ᴮ⁾", "B samples are drawn from the same regime R.", "r labels one replication; changing samples reveals", "the estimator's sampling variability."),
            ("4", "Apply estimator bank", "T₁(x), …, Tᴸ(x)", "Each Tⱼ is one admissible location estimator.", "L is the number of estimators in the bank.", "All receive the same simulated sample path."),
            ("5", "Compute squared error", "(Tⱼ(x⁽ʳ⁾) − θ)²", "Subtract the known truth, then square the error.", "This puts every estimator on one comparable", "replicate-level loss scale."),
            ("6", "Aggregate outputs", "MSE and q95 MSE", "MSE is typical squared error across replications.", "q95 MSE is the difficult upper-tail error boundary.", "Both inform the benchmark gate."),
        )
        for i, (n, head, formula, explanation, note1, note2) in enumerate(flow):
            row, col=divmod(i,3); x=150+col*470; y=220+row*230
            body += [f'<rect x="{x}" y="{y}" width="390" height="190" rx="10" class="card"/>', _t(x+28,y+42,n,"number"), _t(x+78,y+40,head,"body"), _t(x+28,y+78,formula,"formula3"), _t(x+28,y+108,explanation,"note"), _t(x+28,y+134,note1,"note"), _t(x+28,y+154,note2,"note")]
        body += [_t(800, 700, "One regime R, one known target θ, many repeated samples: this is how Monte Carlo makes estimator risk measurable.", "gold", "middle")]
    else:
        body += [_t(90, 105, "WHAT DID WE LEARN?", "kicker"), _t(90, 160, "No Free Lunch, made operational.", "title")]
        lessons=(("H1 ✓","No universal estimator"),("H2 ✓","Performance depends on regime"),("H3 ◐","GA helps selectively"),("H4 ✓","Gate prevents false claims"))
        for i,(head,desc) in enumerate(lessons):
            x=120+i*370; body += [f'<rect x="{x}" y="270" width="320" height="180" rx="12" class="card"/>',_t(x+160,335,head,"number","middle"),_t(x+160,395,desc,"body","middle")]
        body += [_t(800, 570, "The contribution is not a universal GA winner.", "subtitle", "middle"), _t(800, 620, "It is a disciplined way to know when a composite estimator is justified.", "gold", "middle")]
    return f'''<html><style>body{{margin:0;background:#081525;font-family:Arial,sans-serif}}svg{{width:100%;height:760px}}.canvas{{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}}.cover{{font-size:48px;font-weight:800;fill:#f5f9ff}}.title{{font-size:29px;font-weight:800;fill:#f5f9ff}}.subtitle{{font-size:19px;fill:#bfd0e4}}.kicker{{font-size:14px;font-weight:800;letter-spacing:2px;fill:#72cfff}}.body{{font-size:18px;fill:#e3edf9}}.small{{font-size:14px;fill:#bfcee0}}.note{{font-size:11px;fill:#bfcee0}}.gold{{font-size:16px;font-weight:800;fill:#f3c743}}.rule{{stroke:#467da5;stroke-width:2}}.card{{fill:#102a45;stroke:#3b78a4;stroke-width:1.5}}.hyp{{fill:#152f50;stroke:#4b7da5;stroke-width:1}}.formula{{font-family:Georgia,serif;font-size:34px;fill:#f3c743}}.formula2{{font-family:Georgia,serif;font-size:22px;fill:#e7f3ff}}.formula3{{font-family:Georgia,serif;font-size:17px;fill:#f3c743}}.node{{fill:#193f61;stroke:#72cfff;stroke-width:2}}.nodeletter{{font-size:36px;font-family:Georgia,serif;fill:#f3c743}}.balance{{stroke:#72cfff;stroke-width:5}}.number{{font-size:32px;font-weight:800;fill:#f3c743}}</style><svg viewBox="0 0 {w} {h}">{''.join(body)}</svg></html>'''


VALIDATION_STAGES = (
    ("1 · Moment fidelity", "Do generated populations recover their analytic moments?", "125 checks · 0 hard failures · warnings retained for review", "Large synthetic draws (n = 50,000) were compared with analytic mean, variance and skewness for representative parameter-grid rows.", "Empirical mean stayed within the hard 1% tolerance; warnings mark closer-to-threshold cases rather than hidden failures.", "If θ is wrong here, every later error calculation is wrong."),
    ("2 · Contamination fidelity", "Does injection produce the designed rate and severity?", "Designed γ and MAD-based scale verified across representative scenarios", "The realised contamination rate γ̂ and robust outlier scale ĉ were measured after injection, using the same MAD-based rule used to describe regimes.", "The check protects regime labels: a declared 10% upper-tail regime must behave like one before it enters Monte Carlo.", "Otherwise profile matching and later conclusions would be attached to the wrong world."),
    ("3 · Statistical sanity", "Does the engine recover known robust-statistics behaviour?", "Textbook normal-case ordering recovered", "Under clean Normal data, the sample mean should dominate the median in MSE; this is the built-in benchmark sanity check.", "The expected ordering reappeared, so the fitness and error calculations pass a theory-based audit.", "The simulator is checked against known theory before it is used to discover anything new."),
    ("4 · Empirical anchoring", "Does the synthetic grid cover relevant real-data shapes?", "5 public datasets · shape diagnostics checked against matched synthetic coverage", "Observed skewness, excess kurtosis and robust CV from public data were compared with the matched synthetic family's diagnostic space.", "Anchoring is calibration, not known-θ validation: it shows the synthetic worlds cover empirical shapes of interest.", "It keeps the simulation study connected to data without claiming real-data ground truth."),
)


def validation_scene_svg(stage: int) -> str:
    """Data-validation evidence scene for the Monte Carlo layer."""
    stage = max(0, min(int(stage), len(VALIDATION_STAGES) - 1))
    title, question, result, method, finding, consequence = VALIDATION_STAGES[stage]
    body = ['<rect x="28" y="25" width="1544" height="710" rx="18" class="canvas"/>', _t(90, 105, "DATA-GENERATING WORLD · VALIDATION", "kicker"), _t(90, 160, title.upper(), "title"), _t(90, 205, question, "subtitle")]
    for i, (label, *_rest) in enumerate(VALIDATION_STAGES):
        x = 110 + i * 365; active = i == stage
        body += [f'<rect x="{x}" y="245" width="320" height="62" rx="9" class="{"active" if active else "tab"}"/>', _t(x+160, 282, label.upper(), "tabtext", "middle")]
    body += [f'<rect x="90" y="350" width="950" height="290" rx="14" class="scene"/>', _t(125, 395, "WHAT WAS CHECKED", "kicker"), _t(125, 432, method, "body2"), _t(125, 485, "RESULT", "kicker"), _t(125, 522, finding, "body2"), _t(125, 582, "WHY THIS MATTERS", "kicker"), _t(125, 618, consequence, "body2"), f'<rect x="1090" y="350" width="385" height="290" rx="14" class="note"/>', _t(1120, 398, "VALIDATION RESULT", "kicker"), _t(1120, 450, result, "result"), _t(1120, 535, "ORDER OF EVIDENCE", "kicker"), _t(1120, 570, "population → contamination", "small"), _t(1120, 596, "→ theory → empirical anchor", "small")]
    return f'''<html><style>body{{margin:0;background:#081525;font-family:Arial,sans-serif}}svg{{width:100%;height:760px}}.canvas{{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}}.title{{font-size:29px;font-weight:800;fill:#f5f9ff}}.subtitle{{font-size:19px;fill:#bfd0e4}}.kicker{{font-size:14px;font-weight:800;letter-spacing:1.6px;fill:#72cfff}}.scene{{fill:#0b2036;stroke:#3d749b;stroke-width:1.4}}.note{{fill:#0d2842;stroke:#4c86ad;stroke-width:1.5}}.tab{{fill:#0c2035;stroke:#38719a;stroke-width:1.2}}.active{{fill:#3a275f;stroke:#f3c743;stroke-width:2.5}}.tabtext{{font-size:12px;font-weight:800;fill:#e3edf9}}.body2{{font-size:16px;fill:#e3edf9}}.small{{font-size:14px;fill:#bfcee0}}.result{{font-size:18px;font-weight:800;fill:#f3c743}}</style><svg viewBox="0 0 1600 760">{''.join(body)}</svg></html>'''
