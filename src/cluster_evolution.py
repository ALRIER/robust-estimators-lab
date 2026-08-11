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
    """Show up to four *real* GA generations and an operation within the current one."""
    generation = int(generation); phase = int(phase)
    max_generation = len(run["populations"]) - 1
    first = max(0, generation - 3)
    generations = list(range(first, generation + 1))
    if phase == 4 and generation < max_generation:
        generations.append(generation + 1)
    # The map is intentionally the dominant defense view.  Its expanded canvas
    # leaves supporting charts below the fold rather than squeezing generations.
    width, height, top, bottom = 1120, 920, 135, 790
    xs = np.linspace(145, 920, len(generations)); positions = {}
    clouds, labels, frames = [], [], []
    palette = ("#386ee8", "#36b6bd", "#72ce67", "#f7b733", "#ff634f")
    for column, (gen, cx) in enumerate(zip(generations, xs)):
        pop, scores = run["populations"][gen], run["scores"][gen]
        order = np.argsort(scores); rank = np.empty(len(pop), dtype=int); rank[order] = np.arange(len(pop))
        frames.append(f'<rect x="{cx-97:.0f}" y="{top-25}" width="194" height="{bottom-top+45}" rx="8" fill="{"#12375a" if gen == generation else "#091a2e"}" stroke="{"#f3c743" if gen == generation else "#326188"}" stroke-width="{"2.5" if gen == generation else "1"}"/>')
        labels.append(f'<text x="{cx:.0f}" y="42" text-anchor="middle" class="gen">GEN {gen}{" (current)" if gen == generation else ""}</text>')
        rng = np.random.default_rng(20260810 + gen)
        for index, weight in enumerate(pop):
            px = cx + rng.normal(0, 47); py = bottom - 330 * (weight[2] - weight[0]) + rng.normal(0, 52)
            positions[(gen, index)] = (px, py)
            active = gen == generation
            color = "#64748b"; opacity = .65
            if active and phase >= 0:
                color = palette[min(4, int(5 * rank[index] / max(1, len(pop))))]
            if active and phase >= 1:
                event_set = run["events"][gen + 1] if gen < max_generation else []
                parents = {event.get("parent_a_index") for event in event_set if event.get("event_type") == "offspring"} | {event.get("parent_b_index") for event in event_set if event.get("event_type") == "offspring"}
                if index not in parents: opacity = .13 if show_eliminated else 0
            clouds.append(_point(px, py, color, 4.5 if active else 3.5, opacity, active and index == order[0]))
    links = []
    if generation < max_generation and phase >= 2 and show_inheritance:
        event = run["events"][generation + 1][run["explained_event_indices"][generation + 1]]
        child = positions.get((generation + 1, event["child_index"]))
        for parent_key, colour in (("parent_a_index", "#f7b733"), ("parent_b_index", "#b879ff")):
            parent = positions.get((generation, event[parent_key]))
            if parent and child:
                links.append(f'<path d="M{parent[0]:.1f},{parent[1]:.1f} L{child[0]:.1f},{child[1]:.1f}" stroke="{colour}" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>')
        if phase >= 3 and event.get("mutated") and child:
            links.append(f'<circle cx="{child[0]:.1f}" cy="{child[1]:.1f}" r="11" fill="none" stroke="#4de080" stroke-width="2" stroke-dasharray="3 2"/>')
    path = []
    if show_path:
        for gen in generations:
            best = int(np.argmin(run["scores"][gen])); path.append(positions[(gen, best)])
    path_svg = "" if len(path) < 2 else '<path d="' + ' '.join(f'{"M" if i == 0 else "L"}{x:.1f},{y:.1f}' for i, (x, y) in enumerate(path)) + '" class="best"/>'
    grid = ''.join(f'<line x1="45" y1="{y}" x2="1040" y2="{y}" class="grid"/>' for y in range(170, bottom, 135)) if show_grid else ""
    phase_label = PHASES[phase]
    return f'''<html><style>body{{margin:0;background:#081525;font-family:Arial,sans-serif}}svg{{width:100%;height:920px}}.grid{{stroke:#214664;stroke-dasharray:2 6}}.gen{{font-size:16px;font-weight:800;fill:#edf6ff}}.best{{fill:none;stroke:#b879ff;stroke-width:3;stroke-dasharray:5 4}}.phase{{font-size:15px;font-weight:700;fill:#f3c743}}.hint{{font-size:12px;fill:#aebed3}}</style><svg viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3z" fill="#dceaff"/></marker></defs>{grid}{''.join(frames)}{path_svg}{''.join(links)}{''.join(clouds)}{''.join(labels)}<text x="50" y="885" class="phase">GEN {generation}: {phase_label}</text><text x="330" y="885" class="hint">columns are real populations; colours encode fitness</text></svg></html>'''
