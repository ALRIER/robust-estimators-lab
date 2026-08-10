"""Fixed SVG teaching map for explaining GA generations as population clusters."""
import numpy as np

STAGES = [("1", "Initialize", "#ef4444"), ("2", "Score", "#f97316"), ("3", "Select", "#eab308"),
          ("4", "Recombine", "#65a30d"), ("5", "Mutate", "#14b8a6"), ("6", "Converge", "#6d28d9")]


def _svg_point(x, y, color, r=4, opacity=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" opacity="{opacity}"/>'


def cluster_map_svg(run, frame, contamination, show_inheritance=True, show_eliminated=True, show_grid=True):
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
    return f'''<html><style>body{{margin:0;font-family:Arial,sans-serif;background:#fff}}svg{{width:100%;height:480px}}.grid{{stroke:#e7ebf1;stroke-dasharray:2 6}}.guide{{stroke:#d9dee7;stroke-dasharray:3 4}}.stage{{font-size:14px;font-weight:700;fill:#243047}}.number{{font-size:23px;font-weight:800}}.best{{fill:none;stroke:#6534e8;stroke-width:4}}.inherit{{fill:none;stroke:#cbd2de;stroke-width:2;marker-end:url(#arrow)}}.axis{{font-size:13px;fill:#526075}}</style><svg viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3z" fill="#cbd2de"/></marker></defs>{grid}{guides}{labels}<text x="15" y="250" transform="rotate(-90 15,250)" class="axis">Search-space dimension</text><text x="480" y="435" class="axis">Generation snapshots → selection and recombination progressively concentrate the population</text>{''.join(clouds)}{inherit}<path d="{path_d}" class="best"/>{''.join(_svg_point(x,y,'#6534e8',8,1) for x,y in path)}<circle cx="{target_x}" cy="{target_y}" r="66" fill="#dcfce7" stroke="#16a34a" stroke-width="2" stroke-dasharray="7 5"/><circle cx="{target_x}" cy="{target_y}" r="27" fill="#86efac" opacity=".55"/><circle cx="{target_x}" cy="{target_y}" r="8" fill="#15803d"/><text x="{target_x}" y="112" text-anchor="middle" font-size="15" font-weight="700" fill="#15803d">Target region</text><text x="{target_x}" y="132" text-anchor="middle" font-size="12" fill="#15803d">high robustness</text><text x="70" y="92" font-size="12" fill="#6b7280">Each vertical cloud is one generation snapshot</text></svg></html>'''
