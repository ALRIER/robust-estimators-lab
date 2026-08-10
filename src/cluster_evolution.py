"""Fixed SVG teaching map for explaining GA generations as population clusters."""
import numpy as np

STAGES = [("1", "Initialize", "#ef4444"), ("2", "Score", "#f97316"), ("3", "Select", "#eab308"),
          ("4", "Recombine", "#65a30d"), ("5", "Mutate", "#14b8a6"), ("6", "Converge", "#6d28d9")]


def contamination_shift_svg(rate):
    """Compact, label-free visual of randomized contamination changing a target."""
    rng=np.random.default_rng(73); dots=[]
    for panel,offset in ((0,35),(1,220)):
        for _ in range(45):
            x=offset+55+rng.normal(0,25); y=75+rng.normal(0,18); dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.7" fill="#7c8797" opacity=".72"/>')
        target_x=offset+88+panel*22*rate; target_y=58+18*panel*rate; radius=25-10*panel*rate
        dots.append(f'<circle cx="{target_x:.0f}" cy="{target_y:.0f}" r="{radius:.0f}" fill="#bbf7d0" opacity=".55" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="4 3"/>')
        dots.append(f'<circle cx="{target_x:.0f}" cy="{target_y:.0f}" r="5" fill="#16a34a"/>')
    for _ in range(max(3, int(rate * 110))):
        dots.append(f'<circle cx="{220+rng.uniform(5,105):.0f}" cy="{75+rng.uniform(-55,55):.0f}" r="3" fill="#ef4444"/>')
    grid = ''.join(f'<line x1="15" y1="{y}" x2="345" y2="{y}" stroke="#edf0f5" stroke-dasharray="2 5"/>' for y in (30, 75, 120))
    return f'''<html><style>body{{margin:0}}svg{{width:100%;height:190px}}</style><svg viewBox="0 0 360 180">{grid}{''.join(dots)}<path d="M150 75 L205 75" stroke="#aab3c2" stroke-width="2" marker-end="url(#a)"/><defs><marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3z" fill="#aab3c2"/></marker></defs></svg></html>'''


def _svg_point(x, y, color, r=4, opacity=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" opacity="{opacity}"/>'


def cluster_map_svg(run, frame, contamination, show_inheritance=True, show_eliminated=True, show_grid=True, show_path=True):
    """Sequential fixed map; values are pedagogical projections of mini-GA states."""
    width, height, left, bottom = 1120, 480, 70, 390
    stage_gens = np.linspace(0, max(1, frame), 6, dtype=int)
    stage_x = np.linspace(130, 920, 6)
    rng = np.random.default_rng(20260810)
    clouds=[]; path=[]
    for i,(generation,cx) in enumerate(zip(stage_gens,stage_x)):
        pop=run["populations"][generation]; scores=run["scores"][generation]
        order=np.argsort(scores); keep=max(6, int(len(pop)*(1-.10*i)))
        best=pop[order[0]]; by=bottom-28*(best[2]-best[0])
        path.append((cx,by))
        spread=32-3.8*i
        for j,w in enumerate(pop):
            py=bottom-28*(w[2]-w[0])+rng.normal(0,spread)
            px=cx+rng.normal(0,24-2*i)
            opacity=.86 if j in order[:keep] else (.19 if show_eliminated else 0)
            clouds.append(_svg_point(px,py,STAGES[i][2],4.2 if j in order[:keep] else 3.2,opacity))
    path_d=" ".join(f'{"M" if i==0 else "L"}{x:.1f},{y:.1f}' for i,(x,y) in enumerate(path))
    grid="".join(f'<line x1="{left}" y1="{y}" x2="1010" y2="{y}" class="grid"/>' for y in range(110,bottom+1,70)) if show_grid else ""
    guides="".join(f'<line x1="{x}" y1="105" x2="{x}" y2="{bottom}" class="guide"/>' for x in stage_x)
    labels="".join(f'<text x="{x}" y="34" text-anchor="middle" class="number" fill="{c}">{n}</text><text x="{x}" y="58" text-anchor="middle" class="stage">{label}</text>' for x,(n,label,c) in zip(stage_x,STAGES))
    inherit="" if not show_inheritance else "".join(f'<path d="M{stage_x[i]+22},{path[i][1]-15} L{stage_x[i+1]-22},{path[i+1][1]-15}" class="inherit"/>' for i in range(5))
    target_x,target_y=1035,205
    best_path = f'<path d="{path_d}" class="best"/>{"".join(_svg_point(x, y, "#6534e8", 8, 1) for x, y in path)}' if show_path else ""
    return f'''<html><style>body{{margin:0;font-family:Arial,sans-serif;background:#fff}}svg{{width:100%;height:480px}}.grid{{stroke:#e7ebf1;stroke-dasharray:2 6}}.guide{{stroke:#d9dee7;stroke-dasharray:3 4}}.stage{{font-size:14px;font-weight:700;fill:#243047}}.number{{font-size:23px;font-weight:800}}.best{{fill:none;stroke:#6534e8;stroke-width:4}}.inherit{{fill:none;stroke:#cbd2de;stroke-width:2;marker-end:url(#arrow)}}</style><svg viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3z" fill="#cbd2de"/></marker></defs>{grid}{guides}{labels}{''.join(clouds)}{inherit}{best_path}<circle cx="{target_x}" cy="{target_y}" r="66" fill="#dcfce7" stroke="#16a34a" stroke-width="2" stroke-dasharray="7 5"/><circle cx="{target_x}" cy="{target_y}" r="27" fill="#86efac" opacity=".55"/><circle cx="{target_x}" cy="{target_y}" r="8" fill="#15803d"/></svg></html>'''
