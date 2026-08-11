"""Narrative SVG for the thesis experiment pipeline; no results are simulated."""
import numpy as np

STAGES = (
    ("SCENARIO UNIVERSE", "576 contamination conditions", "Performance depends on regime."),
    ("HPF1", "Broad low-cost screening", "Do not spend full computation everywhere."),
    ("HPF2", "Deeper screen on survivors", "Concentrate effort where signal persists."),
    ("SPECIALIST HALVING", "Narrow to five gate candidates", "Discovery is still not confirmation."),
    ("HELD-OUT DUAL GATE", "Mean MSE AND q95(MSE)", "Search performance is not validation."),
    ("FREEZE & CONFIRM", "Weights locked; no retraining", "Confirmation must occur without adaptation."),
    ("CYCLE II — NEST26", "Reopen discovery with 26 components", "Modern estimators apply new pressure."),
    ("SECOND FREEZE", "Fixed-weight evaluation again", "The expanded search faces the same separation."),
    ("EXTERNAL EVIDENCE", "Calibration and Dirichlet audit", "Transfer and random-search questions differ."),
)


def _text(x, y, value, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{value}</text>'


def _dot(x, y, color="#5b87b5", radius=8, opacity=1):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" opacity="{opacity}"/>'


def experiment_pipeline_svg(stage: int) -> str:
    """Render a stage of the written-thesis protocol as a visual gauntlet."""
    stage = max(0, min(int(stage), len(STAGES) - 1))
    width, height = 1600, 780
    nav, scene, notes = [], [], []
    for i, (title, _, _) in enumerate(STAGES):
        y = 70 + i * 67; active = i == stage
        nav.append(f'<rect x="28" y="{y-24}" width="255" height="49" rx="7" fill="{"#273f67" if active else "#0b1c31"}" stroke="{"#f3c743" if active else "#2e638b"}" stroke-width="{"2.5" if active else "1"}"/>')
        nav.append(_text(47, y + 5, f"{i + 1}. {title}", "navactive" if active else "nav", "start"))
    title, what, why = STAGES[stage]
    notes += [f'<rect x="1250" y="105" width="310" height="500" rx="12" class="notecard"/>', _text(1280, 155, "WHAT HAPPENS", "kicker"), _text(1280, 197, title, "notetitle"), _text(1280, 270, what, "notebody"), _text(1280, 365, "WHY INCLUDED", "kicker"), _text(1280, 410, why, "notebody"), _text(1280, 545, "THESIS METHOD", "kicker"), _text(1280, 580, "GA proposes; evidence decides.", "notefoot")]
    # Common scene frame and motion corridor.
    scene += [f'<rect x="325" y="105" width="875" height="500" rx="14" class="scenebox"/>', _text(365, 160, f"STAGE {stage + 1} — {title}", "scenehead"), '<path d="M380 545 L1135 545" class="track" marker-end="url(#arrow)"/>']
    rng = np.random.default_rng(320 + stage)
    if stage == 0:
        scene += [_text(760, 220, "576 CONTAMINATION CONDITIONS", "big", "middle"), _text(760, 252, "9 scales × 8 rates × 8 mechanisms", "sub", "middle")]
        for row in range(6):
            for col in range(12):
                colors = ("#3d83c4", "#5cbf74", "#a76de1", "#f3a83b")
                scene.append(f'<rect x="{445+col*43}" y="{300+row*35}" width="27" height="21" rx="3" fill="{colors[(row+col)%4]}" opacity=".9"/>')
        scene += [_text(760, 550, "distribution family · contamination rate · scale · mechanism", "caption", "middle")]
    elif stage in (1, 2):
        label, exposure, generations = ("HPF1", "60% scenario exposure", "8 generations / fold") if stage == 1 else ("HPF2", "80% initial · 90% expanded", "15 generations / fold")
        for i in range(18 if stage == 1 else 8):
            scene.append(_dot(455 + (i % 6)*35, 285 + (i // 6)*45, "#5d86b0", 8))
        scene += [f'<rect x="690" y="250" width="180" height="185" rx="12" class="filter"/>', _text(780, 322, label, "filtertitle", "middle"), _text(780, 360, exposure, "filtersub", "middle"), _text(780, 388, generations, "filtersub", "middle"), '<path d="M650 345 L685 345" class="flow" marker-end="url(#arrow)"/>', '<path d="M875 345 L925 345" class="flow" marker-end="url(#arrow)"/>']
        for i in range(7 if stage == 1 else 4): scene.append(_dot(950 + (i % 3)*44, 290 + (i // 3)*55, "#4de080", 10))
        scene += [_text(530, 475, "many configurations", "caption", "middle"), _text(1025, 475, "survivors", "caption", "middle")]
    elif stage == 3:
        scene += [_text(760, 230, "SPECIALIST HALVING", "big", "middle"), _text(760, 260, "computation concentrates on strongest candidate–regime pairs", "sub", "middle")]
        for i in range(10): scene.append(_dot(470 + i*54, 345, "#5d86b0", 11, .7))
        scene += ['<path d="M450 410 L1070 410" class="flow" marker-end="url(#arrow)"/>', _text(760, 455, "keep fraction = 0.50", "filtersub", "middle")]
        for i in range(5): scene.append(_dot(640 + i*62, 510, "#f3c743", 13))
        scene += [_text(760, 570, "5 candidates evaluated at the held-out gate", "caption", "middle")]
    elif stage == 4:
        scene += [_text(515, 265, "CANDIDATE", "kicker", "middle"), _dot(515, 320, "#f3c743", 17), '<path d="M515 345 L515 390" class="flow" marker-end="url(#arrow)"/>']
        for y, label in ((405, "MEAN MSE GATE"), (500, "q95(MSE) GATE")):
            scene += [f'<rect x="400" y="{y-28}" width="230" height="55" rx="8" class="gate"/>', _text(515, y + 6, label, "gatetext", "middle"), _text(665, y + 6, "✓ must improve", "pass")]
        scene += [f'<rect x="800" y="255" width="300" height="235" rx="10" class="benchmark"/>', _text(950, 300, "BEST ADMISSIBLE", "kicker", "middle"), _text(950, 330, "BENCHMARK", "filtertitle", "middle"), _text(840, 385, "Mean MSE", "filtersub"), f'<rect x="940" y="370" width="105" height="15" fill="#58aee8"/><rect x="940" y="400" width="135" height="15" fill="#64748b"/>', _text(840, 450, "q95(MSE)", "filtersub"), f'<rect x="940" y="435" width="120" height="15" fill="#58aee8"/><rect x="940" y="465" width="150" height="15" fill="#64748b"/>']
        scene += [_text(515, 575, "PASS only if BOTH gates improve", "pass", "middle"), _text(950, 535, "Otherwise: BENCHMARK RETAINED", "fail", "middle")]
    elif stage in (5, 7):
        cycle = "CYCLE I" if stage == 5 else "CYCLE II — NEST26"
        scene += [_text(760, 225, cycle, "big", "middle"), _text(760, 255, "DISCOVERED WEIGHT VECTOR", "kicker", "middle")]
        names = ("Mean", "Median", "Huber", "Biweight")
        vals = (190, 260, 315, 225)
        for i, (name, val) in enumerate(zip(names, vals)):
            y = 305 + i*48; scene += [_text(460, y+15, name, "filtersub"), f'<rect x="560" y="{y}" width="{val}" height="21" rx="4" fill="{"#4de080" if i % 2 else "#58aee8"}"/>']
        scene += [f'<rect x="900" y="315" width="180" height="145" rx="12" class="lockbox"/>', _text(990, 365, "🔒", "lock", "middle"), _text(990, 415, "WEIGHTS LOCKED", "filtertitle", "middle"), _text(760, 535, "new seeds · stronger benchmarks · paired bootstrap · unseen related regimes", "caption", "middle")]
    elif stage == 6:
        scene += [f'<rect x="400" y="245" width="260" height="235" rx="12" class="cyclebox"/>', _text(530, 295, "CYCLE I", "filtertitle", "middle"), _text(530, 335, "10 estimators", "filtersub", "middle"), _text(530, 385, "GA search → freeze", "caption", "middle"), '<path d="M680 360 L850 360" class="flow" marker-end="url(#arrow)"/>', _text(765, 330, "modern estimator pressure", "caption", "middle"), f'<rect x="870" y="245" width="260" height="235" rx="12" class="cyclebox activecycle"/>', _text(1000, 295, "CYCLE II", "filtertitle", "middle"), _text(1000, 335, "26 estimators", "filtersub", "middle"), _text(1000, 385, "GA search → freeze", "caption", "middle"), _text(760, 545, "Only Cycle I and Cycle II reopen evolutionary search.", "pass", "middle")]
    else:
        scene += [_text(760, 225, "FINAL SPECIALIST", "big", "middle"), _dot(760, 285, "#f3c743", 18), '<path d="M760 310 L760 365" class="flow" marker-end="url(#arrow)"/>', '<path d="M760 385 L545 460" class="flow" marker-end="url(#arrow)"/>', '<path d="M760 385 L975 460" class="flow" marker-end="url(#arrow)"/>']
        scene += [f'<rect x="400" y="465" width="290" height="120" rx="10" class="cyclebox"/>', _text(545, 510, "EXTERNAL CALIBRATION", "filtertitle", "middle"), _text(545, 545, "Does the signal transfer?", "filtersub", "middle"), f'<rect x="830" y="465" width="290" height="120" rx="10" class="cyclebox"/>', _text(975, 510, "DIRICHLET AUDIT", "filtertitle", "middle"), _text(975, 545, "Could random weights pass?", "filtersub", "middle")]
    return f'''<html><style>body{{margin:0;background:#081525;font-family:Arial,sans-serif}}svg{{width:100%;height:780px}}.nav{{font-size:12px;font-weight:700;fill:#9fb4cb}}.navactive{{font-size:12px;font-weight:800;fill:#fff}}.notecard{{fill:#0c2036;stroke:#3a78a8;stroke-width:1.5}}.kicker{{font-size:13px;font-weight:800;letter-spacing:1.5px;fill:#72cfff}}.notetitle{{font-size:22px;font-weight:800;fill:#f3c743}}.notebody{{font-size:16px;fill:#dce9f8}}.notefoot{{font-size:13px;fill:#9db2ca}}.scenebox{{fill:#0a1b30;stroke:#2f678f;stroke-width:1.5}}.scenehead{{font-size:19px;font-weight:800;fill:#eef6ff}}.track{{stroke:#285273;stroke-width:2;stroke-dasharray:4 6}}.big{{font-size:27px;font-weight:800;fill:#f4f8ff}}.sub{{font-size:16px;fill:#b4c8dd}}.caption{{font-size:14px;fill:#b4c8dd}}.filter{{fill:#153d60;stroke:#72cfff;stroke-width:2}}.filtertitle{{font-size:19px;font-weight:800;fill:#f4f8ff}}.filtersub{{font-size:14px;fill:#c8daed}}.flow{{fill:none;stroke:#72cfff;stroke-width:4}}.gate{{fill:#173d5c;stroke:#f3c743;stroke-width:2}}.gatetext{{font-size:15px;font-weight:800;fill:#f5f8ff}}.pass{{font-size:15px;font-weight:800;fill:#4de080}}.fail{{font-size:14px;font-weight:800;fill:#ff8b7c}}.benchmark{{fill:#10283f;stroke:#6689a8;stroke-width:1.5}}.lockbox{{fill:#153d60;stroke:#4de080;stroke-width:2}}.lock{{font-size:38px}}.cyclebox{{fill:#10283f;stroke:#3d79a5;stroke-width:1.5}}.activecycle{{stroke:#f3c743;stroke-width:2.5}}</style><svg viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4z" fill="#dceaff"/></marker></defs>{''.join(nav)}{''.join(scene)}{''.join(notes)}</svg></html>'''
