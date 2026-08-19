"""Deterministic defense schematic of the implemented thesis GA.

This module never runs an optimisation.  It visualises the documented search
architecture so the pedagogical Layer 5 demo stays separate from thesis evidence.
"""


def _t(x, y, text, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{text}</text>'


def _rect(x, y, w, h, cls="card", rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>'


def thesis_ga_architecture_svg() -> str:
    """Return one slide-like SVG explaining the real thesis GA architecture."""
    w, h = 1600, 900
    b = [
        f'<rect x="24" y="22" width="1552" height="852" rx="18" class="canvas"/>',
        _t(78, 82, "THESIS GA ARCHITECTURE", "kicker"),
        _t(78, 132, "The animation showed evolution; this is the implemented search-and-claim logic.", "title"),
        _t(78, 164, "Schematic only · no optimization is run in this view", "subtitle"),
    ]

    # --- Left: Monte Carlo outputs and fast scoring ---------------------------------
    b += [_rect(72, 205, 430, 430, "panel"), _t(98, 243, "1 · MONTE CARLO → MATRIX C", "section")]
    b += [_t(98, 275, "Rows = replications · columns = named estimators", "small")]
    cell_x, cell_y = 112, 308
    for r in range(6):
        for c in range(7):
            cls = "cellhi" if (r + 2 * c) % 5 == 0 else "cell"
            b.append(f'<rect x="{cell_x+c*34}" y="{cell_y+r*28}" width="26" height="20" rx="3" class="{cls}"/>')
    b += [
        _t(232, 501, "C", "matrixlabel", "middle"),
        _t(355, 405, "×", "math", "middle"),
        _rect(382, 326, 76, 157, "weightbox"),
    ]
    weights = (21, 56, 34, 72, 43)
    for i, width in enumerate(weights):
        b.append(f'<rect x="394" y="{344+i*26}" width="{width*0.62}" height="13" rx="3" class="weight"/>')
    b += [
        _t(420, 505, "w", "matrixlabel", "middle"),
        '<path d="M255 535 L430 535" class="arrow" marker-end="url(#arr)"/>',
        _t(98, 571, "FAST CANDIDATE SCORING", "label"),
        _t(98, 601, "composite outputs = Cw", "formula"),
        _t(98, 625, "The GA changes weights — not raw observations.", "small"),
    ]

    # --- Centre: evolutionary loop ---------------------------------------------------
    b += [_rect(525, 205, 660, 430, "panel"), _t(551, 243, "2 · SIMPLEX-SAFE EVOLUTION LOOP", "section")]
    steps = (
        ("DIRICHLET INIT", "valid proportions", 590),
        ("SELECTION", "tournament 2 / 3", 720),
        ("CROSSOVER", "convex blend", 850),
        ("MUTATION", "Dirichlet nudge", 980),
        ("DIVERSITY", "elitism + immigration", 1110),
    )
    for i, (head, sub, cx) in enumerate(steps):
        b += [f'<circle cx="{cx}" cy="335" r="48" class="node"/>', _t(cx, 329, str(i+1), "nodeNum", "middle"), _t(cx, 353, head, "nodeHead", "middle"), _t(cx, 411, sub, "small", "middle")]
        if i < len(steps)-1:
            b.append(f'<path d="M{cx+50} 335 L{steps[i+1][2]-52} 335" class="arrow" marker-end="url(#arr)"/>')
    # small illustrative graphics below operators
    # initialization bars
    for i, ww in enumerate((35, 18, 55, 29)):
        b.append(f'<rect x="{558+i*18}" y="452" width="12" height="{ww}" rx="2" class="mini" transform="rotate(180 {564+i*18} 507)"/>')
    # selection population
    for i in range(6):
        cls = "sel" if i in (1, 4) else "ghost"
        b.append(f'<circle cx="{684+(i%3)*28}" cy="{468+(i//3)*30}" r="9" class="{cls}"/>')
    # crossover parents / child
    b += [
        '<path d="M820 461 L850 486" class="thin"/>', '<path d="M880 461 L850 486" class="thin"/>',
        '<rect x="809" y="447" width="42" height="10" rx="3" class="parentA"/>',
        '<rect x="861" y="447" width="42" height="10" rx="3" class="parentB"/>',
        '<rect x="828" y="490" width="44" height="13" rx="3" class="child"/>',
    ]
    # mutation before/after bars
    for i, ww in enumerate((22, 39, 18)):
        b.append(f'<rect x="{944+i*18}" y="{500-ww}" width="12" height="{ww}" rx="2" class="mutA"/>')
    b.append('<path d="M1000 474 L1021 474" class="tinyarrow" marker-end="url(#arr)"/>')
    for i, ww in enumerate((30, 24, 45)):
        b.append(f'<rect x="{1025+i*18}" y="{500-ww}" width="12" height="{ww}" rx="2" class="mutB"/>')
    # elitism + immigration
    b += [
        '<circle cx="1090" cy="468" r="11" class="gold"/>', '<circle cx="1120" cy="468" r="11" class="gold"/>',
        '<circle cx="1150" cy="468" r="11" class="imm"/>', _t(1120, 517, "keep best + add new", "tiny", "middle"),
        '<path d="M1125 550 C1125 585 590 585 590 392" class="loop" marker-end="url(#arr)"/>',
        _t(853, 600, "repeat across generations / folds", "looptext", "middle"),
    ]

    # --- Right: fitness -> freeze -> gate -------------------------------------------
    b += [_rect(1208, 205, 320, 430, "panel"), _t(1234, 243, "3 · SEARCH ≠ CLAIM", "section")]
    b += [
        _rect(1235, 277, 266, 96, "fitness"),
        _t(1368, 306, "FITNESS", "label", "middle"),
        _t(1368, 334, "0.70 q95 + 0.30 max loss", "formulaSmall", "middle"),
        _t(1368, 358, "+ regularisation", "small", "middle"),
        '<path d="M1368 378 L1368 414" class="arrow" marker-end="url(#arr)"/>',
        _rect(1260, 420, 216, 61, "candidate"),
        _t(1368, 446, "candidate w*", "nodeHead", "middle"),
        _t(1368, 468, "promising — not confirmed", "tiny", "middle"),
        '<path d="M1368 484 L1368 519" class="arrow" marker-end="url(#arr)"/>',
        _rect(1260, 524, 216, 44, "freeze"),
        _t(1368, 552, "FREEZE WEIGHTS", "label", "middle"),
        '<path d="M1368 571 L1368 596" class="arrow" marker-end="url(#arr)"/>',
        _t(1368, 616, "held-out dual gate", "gateText", "middle"),
    ]

    # --- Bottom: claim-control and configuration strip -------------------------------
    b += [
        _rect(72, 660, 1456, 90, "claimband"),
        _t(102, 694, "FITNESS GUIDES SEARCH", "claimHead"),
        _t(102, 723, "selection pressure inside the GA", "small"),
        _t(770, 694, "→", "bigarrow", "middle"),
        _t(840, 694, "GATE CONTROLS THE CLAIM", "claimHead"),
        _t(840, 723, "ΔMSE ≥ 0  AND  Δq95 ≥ 0", "formula"),
        _rect(1260, 680, 110, 48, "pass"), _t(1315, 710, "PASS", "passText", "middle"),
        _rect(1384, 680, 110, 48, "retain"), _t(1439, 710, "RETAIN", "retainText", "middle"),
    ]

    config = (
        ("POP", "N = 100"), ("FOLDS", "K = 3"), ("GEN", "G = 20 / fold"), ("SEEDS", "101 · 202"),
        ("MUT", "μ₀ = .12 / .18"), ("MIN MUT", "μmin = .05"), ("IMM", "5–10% / 15 gen"), ("STOP", "5 gen · p=3 · δ=.005"),
    )
    start_x = 72
    for i, (lab, val) in enumerate(config):
        x = start_x + i * 182
        b += [_rect(x, 772, 168, 72, "config"), _t(x+14, 798, lab, "configLab"), _t(x+14, 827, val, "configVal")]

    css = """
    body{margin:0;background:#081525;font-family:Arial,sans-serif}
    svg{width:100%;height:900px}.canvas{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}
    .kicker{font-size:14px;font-weight:800;letter-spacing:1.7px;fill:#72cfff}.title{font-size:30px;font-weight:800;fill:#f5f9ff}.subtitle{font-size:15px;fill:#a9c0d5}
    .panel{fill:#0b2036;stroke:#3d749b;stroke-width:1.4}.section{font-size:15px;font-weight:800;fill:#f5f9ff}.small{font-size:12.5px;fill:#b9ccdf}.tiny{font-size:10.5px;fill:#aac0d4}
    .cell{fill:#214967}.cellhi{fill:#58aee8}.matrixlabel{font-family:Georgia,serif;font-size:27px;font-weight:800;fill:#f3c743}.weightbox{fill:#102c48;stroke:#397daa}.weight{fill:#a777e3}.math{font-family:Georgia,serif;font-size:27px;fill:#dceaff}.formula{font-family:Georgia,serif;font-size:18px;font-weight:700;fill:#f3c743}.formulaSmall{font-family:Georgia,serif;font-size:14px;font-weight:700;fill:#f3c743}.label{font-size:12px;font-weight:800;letter-spacing:.8px;fill:#72cfff}
    .node{fill:#143552;stroke:#58aee8;stroke-width:2}.nodeNum{font-size:21px;font-weight:800;fill:#f3c743}.nodeHead{font-size:10.5px;font-weight:800;fill:#f6fbff}.arrow{stroke:#72cfff;stroke-width:2.5;fill:none}.tinyarrow{stroke:#72cfff;stroke-width:1.7;fill:none}.thin{stroke:#9abbd4;stroke-width:1.6;fill:none}.loop{stroke:#a777e3;stroke-width:2.3;fill:none;stroke-dasharray:7 5}.looptext{font-size:11px;font-weight:700;fill:#c5aaf0}
    .mini{fill:#58aee8}.sel{fill:#54c786;stroke:#b7ffca;stroke-width:1.3}.ghost{fill:#45627a}.parentA{fill:#58aee8}.parentB{fill:#a777e3}.child{fill:#f3c743}.mutA{fill:#5f7892}.mutB{fill:#63dfa2}.gold{fill:#f3c743}.imm{fill:#72cfff;stroke:#e8f8ff;stroke-width:1.2}
    .fitness{fill:#192f4b;stroke:#a777e3;stroke-width:1.8}.candidate{fill:#17354f;stroke:#f3c743;stroke-width:1.7}.freeze{fill:#193d5e;stroke:#f3c743;stroke-width:1.8}.gateText{font-size:13px;font-weight:800;fill:#dceaff}
    .claimband{fill:#0d2842;stroke:#4c86ad;stroke-width:1.6}.claimHead{font-size:15px;font-weight:800;fill:#f5f9ff}.bigarrow{font-size:27px;font-weight:800;fill:#72cfff}.pass{fill:#123d30;stroke:#54c786;stroke-width:1.8}.retain{fill:#382335;stroke:#ff825f;stroke-width:1.8}.passText{font-size:13px;font-weight:800;fill:#c8ffd7}.retainText{font-size:13px;font-weight:800;fill:#ffd6cc}
    .config{fill:#0a1c31;stroke:#2d6d9c;stroke-width:1.2}.configLab{font-size:10px;font-weight:800;letter-spacing:.8px;fill:#72cfff}.configVal{font-size:12px;font-weight:700;fill:#e1edf8}
    """
    return f'''<html><style>{css}</style><svg viewBox="0 0 {w} {h}"><defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4z" fill="#dceaff"/></marker></defs>{''.join(b)}</svg></html>'''
