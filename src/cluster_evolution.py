"""SVG views for the pedagogical GA; columns are real generations, never stages."""
import numpy as np

PHASES = ("1 Evaluate", "2 Select", "3 Crossover", "4 Mutation", "5 Next generation")


def contamination_shift_svg(rate):
    rng = np.random.default_rng(73); dots = []
    for panel, offset in ((0, 35), (1, 220)):
        for _ in range(45):
            x = offset + 55 + rng.normal(0, 25); y = 75 + rng.normal(0, 18)
            dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.7" fill="#7c8797" opacity=".72"/>')
        target_x = offset + 88 + panel * 22 * rate; target_y = 58 + 18 * panel * rate
        dots.append(f'<circle cx="{target_x:.0f}" cy="{target_y:.0f}" r="25" fill="#bbf7d0" opacity=".35" stroke="#4de080" stroke-width="1.5" stroke-dasharray="4 3"/><circle cx="{target_x:.0f}" cy="{target_y:.0f}" r="5" fill="#4de080"/>')
    for _ in range(max(3, int(rate * 110))):
        dots.append(f'<circle cx="{220+rng.uniform(5,105):.0f}" cy="{75+rng.uniform(-55,55):.0f}" r="3" fill="#ff5b49"/>')
    grid = ''.join(f'<line x1="15" y1="{y}" x2="345" y2="{y}" stroke="#214664" stroke-dasharray="2 5"/>' for y in (30, 75, 120))
    return f'''<html><style>body{{margin:0;background:#081525}}svg{{width:100%;height:190px}}</style><svg viewBox="0 0 360 180">{grid}{''.join(dots)}<path d="M150 75 L205 75" stroke="#6f89a8" stroke-width="2" marker-end="url(#a)"/><defs><marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3z" fill="#6f89a8"/></marker></defs></svg></html>'''


def _point(x, y, color, radius=4, opacity=1, ring=False):
    stroke = ' stroke="#f5fbff" stroke-width="2"' if ring else ''
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}" opacity="{opacity}"{stroke}/>'


def cluster_map_svg(run, generation, phase, show_inheritance=True, show_eliminated=True, show_grid=True, show_path=True):
    """Explain one genuine GA generation through five visually distinct states."""
    generation, phase = int(generation), int(phase)
    max_generation = len(run["populations"]) - 1
    previous = max(0, generation - 1)
    generations = [previous, generation] if previous != generation else [generation]
    if generation < max_generation and phase >= 2:
        generations.append(generation + 1)
    width, height, top, bottom = 1120, 920, 165, 790
    xs = np.linspace(190, 900, len(generations)); positions = {}
    clouds, labels, frames, links = [], [], [], []
    scores = run["scores"][generation]; order = np.argsort(scores)
    event_set = run["events"][generation + 1] if generation < max_generation else []
    parents = {event.get("parent_a_index") for event in event_set if event.get("event_type") == "offspring"}
    parents |= {event.get("parent_b_index") for event in event_set if event.get("event_type") == "offspring"}
    explained = event_set[run["explained_event_indices"][generation + 1]] if generation < max_generation else None
    rank = np.empty(len(order), dtype=int); rank[order] = np.arange(len(order))
    palette = ("#35c76c", "#68d678", "#f3c743", "#ff9538", "#ff5b49")
    for gen, cx in zip(generations, xs):
        active = gen == generation; is_next = gen == generation + 1
        frames.append(f'<rect x="{cx-145:.0f}" y="{top-20}" width="290" height="{bottom-top+35}" rx="10" fill="{"#153c5f" if active else "#091a2e"}" stroke="{"#f3c743" if active else "#326188"}" stroke-width="{"3" if active else "1.2"}"/>')
        labels.append(f'<text x="{cx:.0f}" y="135" text-anchor="middle" class="gen">GEN {gen}{" — ACTIVE" if active else ""}</text>')
        pop = run["populations"][gen]; local_scores = run["scores"][gen]
        local_order = np.argsort(local_scores); local_rank = np.empty(len(pop), dtype=int); local_rank[local_order] = np.arange(len(pop))
        rng = np.random.default_rng(20260810 + gen)
        for index, weight in enumerate(pop):
            px = cx + rng.normal(0, 64); py = (top + bottom) / 2 - 440 * (weight[2] - weight[0]) + rng.normal(0, 42)
            positions[(gen, index)] = (px, py)
            if is_next and phase < 4:
                continue  # crossover/mutation show the single explained child first
            colour, opacity, ring, radius = "#64748b", .38, False, 4
            if active:
                colour = palette[min(4, int(5 * local_rank[index] / max(1, len(pop))))]
                opacity, radius = .9, 5
                if phase == 1:  # selection: genuine contributing parents survive
                    if index in parents: colour, opacity, ring, radius = "#4de080", 1, True, 7
                    else: opacity = .09 if show_eliminated else 0
                elif phase >= 2:
                    if explained and index == explained["parent_a_index"]: colour, opacity, ring, radius = "#f3c743", 1, True, 8
                    elif explained and index == explained["parent_b_index"]: colour, opacity, ring, radius = "#b879ff", 1, True, 8
                    else: opacity = .11 if show_eliminated else 0
                elif index == order[0]: ring = True
            clouds.append(_point(px, py, colour, radius, opacity, ring))
    if explained and phase >= 2:
        child = positions[(generation + 1, explained["child_index"])]
        pa, pb = positions[(generation, explained["parent_a_index"])], positions[(generation, explained["parent_b_index"])]
        if show_inheritance:
            links += [f'<path d="M{pa[0]:.1f},{pa[1]:.1f} L{child[0]:.1f},{child[1]:.1f}" stroke="#f3c743" class="inherit" marker-end="url(#arrow)"/>', f'<path d="M{pb[0]:.1f},{pb[1]:.1f} L{child[0]:.1f},{child[1]:.1f}" stroke="#b879ff" class="inherit" marker-end="url(#arrow)"/>']
        clouds.append(_point(*child, "#dceaff", 11, 1, True))
        if phase == 3:
            delta = explained.get("mutation_vector", np.zeros(3))
            before = (child[0] - 36, child[1] + 440 * (delta[2] - delta[0]))
            links.append(f'<path d="M{before[0]:.1f},{before[1]:.1f} L{child[0]:.1f},{child[1]:.1f}" stroke="#4de080" class="mutation" marker-end="url(#arrow)"/>')
            clouds.append(_point(*before, "#4de080", 7, .7, True))
    path_svg = ""
    if show_path and len(generations) > 1:
        path = [positions[(gen, int(np.argmin(run["scores"][gen])))] for gen in generations]
        path_svg = '<path d="' + ' '.join(f'{"M" if i == 0 else "L"}{x:.1f},{y:.1f}' for i, (x, y) in enumerate(path)) + '" class="best"/>'
    grid = ''.join(f'<line x1="45" y1="{y}" x2="1075" y2="{y}" class="grid"/>' for y in range(210, bottom, 115)) if show_grid else ""
    step_cards = []
    for index, label in enumerate(PHASES):
        x = 52 + index * 205; active = index == phase
        step_cards.append(f'<rect x="{x}" y="28" width="185" height="65" rx="7" fill="{"#432f76" if active else "#0d223a"}" stroke="{"#b879ff" if active else "#326188"}" stroke-width="{"2.5" if active else "1"}"/><text x="{x+92}" y="67" text-anchor="middle" class="step">{label}</text>')
    instruction = ("Fitness colours reveal error: green is lower." if phase == 0 else "Only recorded parents remain highlighted." if phase == 1 else "Two recorded parents blend into this real child." if phase == 2 else "The child moves from pre-mutation to final weights." if phase == 3 else "The complete child population becomes the next generation.")
    return f'''<html><style>body{{margin:0;background:#081525;font-family:Arial,sans-serif}}svg{{width:100%;height:920px}}.grid{{stroke:#214664;stroke-dasharray:2 6}}.gen{{font-size:17px;font-weight:800;fill:#edf6ff}}.step{{font-size:13px;font-weight:800;fill:#edf6ff}}.best{{fill:none;stroke:#b879ff;stroke-width:3;stroke-dasharray:5 4}}.inherit{{fill:none;stroke-width:3}}.mutation{{fill:none;stroke-width:4;stroke-dasharray:5 3}}.phase{{font-size:17px;font-weight:800;fill:#f3c743}}.hint{{font-size:14px;fill:#c4d5e9}}</style><svg viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3z" fill="#dceaff"/></marker></defs>{''.join(step_cards)}{grid}{''.join(frames)}{path_svg}{''.join(links)}{''.join(clouds)}{''.join(labels)}<text x="52" y="875" class="phase">GEN {generation}: {PHASES[phase]}</text><text x="345" y="875" class="hint">{instruction}</text></svg></html>'''
