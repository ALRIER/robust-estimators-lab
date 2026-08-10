"""Art-directed fixed simplex landscape with dynamic GA overlays."""
import html
import numpy as np


def _point(weights):
    x, y, z = weights
    return 100 + 1200*y + 600*z, 550 - 460*z


def _circles(points, color, radius, opacity=1):
    return "".join(f'<circle cx="{_point(p)[0]:.1f}" cy="{_point(p)[1]:.1f}" r="{radius}" fill="{color}" opacity="{opacity}" stroke="#fff" stroke-width="1.3"/>' for p in points)


def simplex_svg(population, history, terrain, event=None, show_population=True, show_path=True,
                show_contours=True, show_grid=True, show_contamination=True):
    """Return a non-interactive SVG where only GA state changes by generation."""
    target = terrain["target"]
    tx, ty = _point(target)
    path = "".join(f'{"M" if i == 0 else "L"}{_point(p)[0]:.1f},{_point(p)[1]:.1f}' for i,p in enumerate(history))
    population_svg = _circles(population, "#ffffff", 5.5, .96) if show_population else ""
    history_svg = _circles(history, "#ef233c", 4.4, .88) if show_path else ""
    line_svg = f'<path d="{path}" class="best-path"/>' if show_path and len(history) else ""
    stress = ""
    if show_contamination and terrain.get("contamination") != "none":
        sites = [[.23,.12,.65],[.10,.26,.64],[.35,.05,.60],[.12,.55,.33]]
        n = max(5, int(terrain.get("rate", .1)*70)); rng=np.random.default_rng(1907)
        dots=[]
        for i in range(n):
            w=np.maximum(np.asarray(sites[i % len(sites)])+rng.normal(0,.022,3),.01); w/=w.sum(); px,py=_point(w)
            dots.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="#ff5a36" opacity=".7"/>')
        stress="".join(dots)
    heredity=""
    if event and event.get("event_type") == "offspring":
        a,b,c=_point(event["parent_a"]),_point(event["parent_b"]),_point(event["child"])
        child_color="#f59e0b" if event["mutated"] else "#16a34a"
        heredity=(f'<path d="M{a[0]:.1f},{a[1]:.1f} L{c[0]:.1f},{c[1]:.1f} M{b[0]:.1f},{b[1]:.1f} L{c[0]:.1f},{c[1]:.1f}" class="inherit"/>'
                  f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="7" fill="#2563eb" stroke="white" stroke-width="2"/>'
                  f'<circle cx="{b[0]:.1f}" cy="{b[1]:.1f}" r="7" fill="#2563eb" stroke="white" stroke-width="2"/>'
                  f'<rect x="{c[0]-6:.1f}" y="{c[1]-6:.1f}" width="12" height="12" rx="2" fill="{child_color}" stroke="white" stroke-width="2" transform="rotate(45 {c[0]:.1f} {c[1]:.1f})"/>')
    contour = "" if not show_contours else """
      <path d="M185 520 Q350 420 505 500 Q700 575 900 485 Q1080 420 1220 520" class="contour"/>
      <path d="M255 478 Q390 360 520 455 Q700 530 870 445 Q1050 350 1160 480" class="contour"/>
      <path d="M330 430 Q430 275 555 400 Q700 500 840 380 Q995 270 1100 435" class="contour"/>
      <ellipse cx="825" cy="495" rx="150" ry="48" class="contour"/><ellipse cx="825" cy="495" rx="105" ry="32" class="contour"/><ellipse cx="825" cy="495" rx="62" ry="18" class="contour"/>
    """
    grid = "" if not show_grid else """<path d="M100 550 L700 90 L1300 550 M250 550 L700 205 L1150 550 M400 550 L700 320 L1000 550 M550 550 L700 435 L850 550" class="grid"/>"""
    return f'''<html><style>
      body{{margin:0;background:#fff;font-family:Arial,sans-serif}} svg{{width:100%;height:650px}} .contour{{fill:none;stroke:#fff;stroke-width:2;opacity:.68}} .grid{{fill:none;stroke:#fff;stroke-width:1;opacity:.22}} .best-path{{fill:none;stroke:#8f1535;stroke-width:3;stroke-dasharray:8 7;opacity:.9}} .inherit{{fill:none;stroke:#2563eb;stroke-width:2.5;stroke-dasharray:6 5;opacity:.86}} .label{{font-size:17px;font-weight:700;fill:#17232b}}
      </style><svg viewBox="0 0 1400 650" preserveAspectRatio="xMidYMid meet">
      <defs><clipPath id="triangle"><path d="M100 550 L700 90 L1300 550 Z"/></clipPath>
        <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#5cbf92"/><stop offset=".55" stop-color="#227f9c"/><stop offset="1" stop-color="#0d4c98"/></linearGradient>
        <linearGradient id="mountain" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#e9c54b" stop-opacity=".15"/><stop offset=".42" stop-color="#f07d24"/><stop offset="1" stop-color="#a41422"/></linearGradient>
        <radialGradient id="valley"><stop stop-color="#082c73"/><stop offset=".45" stop-color="#106caf"/><stop offset="1" stop-color="#2a9d9a" stop-opacity=".05"/></radialGradient>
      </defs><g clip-path="url(#triangle)">
        <path d="M100 550 L700 90 L1300 550 Z" fill="url(#floor)"/>
        <path d="M105 550 Q250 445 345 390 L405 250 L470 365 L535 210 L610 355 L700 145 L785 320 L875 205 L950 370 L1065 285 L1140 420 Q1220 485 1295 550 Z" fill="url(#mountain)"/>
        <path d="M110 550 Q305 490 425 515 Q610 575 825 505 Q1025 440 1290 550 Z" fill="url(#valley)"/>
        {grid}{contour}{stress}{line_svg}{history_svg}{population_svg}{heredity}
      </g>
      <circle cx="{tx:.1f}" cy="{ty:.1f}" r="15" fill="#ffd84d" stroke="#704b00" stroke-width="2"/><text x="{tx:.1f}" y="{ty+7:.1f}" text-anchor="middle" font-size="23">★</text>
      <circle cx="100" cy="550" r="7" fill="#17232b"/><text x="100" y="585" text-anchor="middle" class="label">X<tspan x="100" dy="18" font-size="13">(1, 0, 0)</tspan></text>
      <circle cx="1300" cy="550" r="7" fill="#17232b"/><text x="1300" y="585" text-anchor="middle" class="label">Y<tspan x="1300" dy="18" font-size="13">(0, 1, 0)</tspan></text>
      <circle cx="700" cy="90" r="7" fill="#17232b"/><text x="700" y="58" text-anchor="middle" class="label">Z<tspan x="700" dy="18" font-size="13">(0, 0, 1)</tspan></text>
      <text x="1080" y="80" font-size="15" fill="#8f1535">■ historical best trace</text><text x="1080" y="106" font-size="15" fill="#334155">○ GA candidates</text><text x="1080" y="132" font-size="15" fill="#ff5a36">● contamination stress</text>
      </svg></html>'''
