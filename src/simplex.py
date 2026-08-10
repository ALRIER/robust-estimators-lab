"""Rich artificial terrains for a transparent, interactive GA teaching lab."""
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import Delaunay


def barycentric_grid(step=.020):
    rows = []
    for a in np.arange(0, 1 + 1e-9, step):
        for b in np.arange(0, 1 + 1e-9, step):
            c = 1 - a - b
            if c >= -1e-9: rows.append((a, b, max(0., c)))
    return np.asarray(rows)


def barycentric_to_xy(weights):
    weights = np.asarray(weights, dtype=float)
    # X left-front, Y right-front, Z rear summit.
    return weights[..., 1] + .5 * weights[..., 2], np.sqrt(3) / 2 * weights[..., 2]


def _simplex(vector):
    vector = np.maximum(np.asarray(vector, dtype=float), .02)
    return vector / vector.sum()


def teaching_terrain(family, contamination, rate, scale, skewness, lens):
    """Translate UI settings into a *declared artificial* terrain variant.

    It is a narrative control, not a scientific thesis objective: the controls
    change where valleys, ridges and plateaus appear so the GA can be explored.
    """
    family_targets = {
        "normal": (.36, .43, .21), "lognormal": (.47, .35, .18),
        "weibull": (.31, .49, .20), "exgaussian": (.41, .38, .21),
    }
    target = np.asarray(family_targets[family], dtype=float)
    shifts = {
        "none": (0, 0, 0), "upper_tail": (.13, -.08, -.05),
        "symmetric": (.07, .03, -.10), "bimodal": (-.07, .14, -.07),
        "point_mass": (.10, -.12, .02),
    }
    target = _simplex(target + np.asarray(shifts[contamination]) * (.35 + 1.5 * rate) + np.asarray((-.10 * skewness, .07 * skewness, .03 * skewness)))
    return {
        "target": target, "contamination": contamination, "rate": rate, "scale": scale,
        "ruggedness": .014 + .004 * scale + .090 * rate + (.018 if lens == "q95(MSE)" else 0),
        "label": f"{family} · {contamination} · {rate:.0%} contamination · skew {skewness:+.1f}",
    }


def demo_objective(a, b, c, terrain=None):
    """Artificial teaching fitness. Lower values produce the displayed valley.

    The broad basin deliberately spans most of the simplex so that the search
    reads as an optimisation process, rather than as points floating on a
    small isolated crater. The tall features are biased toward the rear of
    the displayed triangle; the global optimum remains in the foreground
    basin where the path and the final star are easy to read.
    """
    terrain = terrain or teaching_terrain("normal", "upper_tail", .10, 10., 0., "Tail-risk")
    a, b, c = np.asarray(a), np.asarray(b), np.asarray(c)
    target = terrain["target"]
    distance = 1.9 * (a-target[0])**2 + 2.0 * (b-target[1])**2 + 2.5 * (c-target[2])**2
    global_well = np.exp(-((a-target[0])**2/.025 + (b-target[1])**2/.025 + (c-target[2])**2/.018))
    left_peak = np.exp(-((a-.28)**2/.012 + (b-.07)**2/.014 + (c-.65)**2/.018))
    right_peak = np.exp(-((a-.07)**2/.014 + (b-.28)**2/.012 + (c-.65)**2/.018))
    ridge = np.exp(-((a-.17)**2/.065 + (b-.17)**2/.065 + (c-.57)**2/.030))
    if terrain["contamination"] == "upper_tail": right_peak *= 1.65
    elif terrain["contamination"] == "symmetric": left_peak *= 1.28; right_peak *= 1.28
    elif terrain["contamination"] == "point_mass": left_peak *= 1.8
    boost = .20 + .055 * terrain["scale"] + .90 * terrain["rate"]
    texture = terrain["ruggedness"] * np.sin(15*a + 3*c) * np.cos(13*b - 2*c)
    return .35 + distance - .66*global_well + boost*(left_peak + right_peak + .55*ridge) + texture


def _surface(terrain):
    grid = barycentric_grid(); x, y = barycentric_to_xy(grid)
    fitness = demo_objective(*grid.T, terrain)
    # A restrained vertical compression keeps the valley visible without making
    # the terrain read as a flat plane.  It is visual scaling only.
    elevation = .62 + 8.15 * (fitness - fitness.min()) / (fitness.max() - fitness.min())
    return grid, x, y, elevation, fitness, Delaunay(np.c_[x, y]).simplices


def _contour_trace(x, y, z, triangles, levels):
    """March each terrain triangle to draw genuine topographic lines in 3D."""
    xs, ys, zs = [], [], []
    for level in levels:
        for triangle in triangles:
            ids = list(triangle); hits = []
            for left, right in ((ids[0], ids[1]), (ids[1], ids[2]), (ids[2], ids[0])):
                zl, zr = z[left], z[right]
                if (zl-level) * (zr-level) < 0:
                    fraction = (level-zl) / (zr-zl)
                    hits.append((x[left] + fraction*(x[right]-x[left]), y[left] + fraction*(y[right]-y[left]), level+.018))
            if len(hits) == 2:
                xs.extend([hits[0][0], hits[1][0], None]); ys.extend([hits[0][1], hits[1][1], None]); zs.extend([hits[0][2], hits[1][2], None])
    return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", name="Topographic contours", line=dict(color="rgba(255,255,255,.62)", width=2), hoverinfo="skip")


def _simplex_grid_trace(terrain, elevation):
    xs, ys, zs = [], [], []
    for fixed in (.2, .4, .6, .8):
        for axis in range(3):
            points = []
            for variable in np.linspace(0, 1-fixed, 31):
                weight = np.zeros(3); weight[axis] = fixed; weight[(axis+1)%3] = variable; weight[(axis+2)%3] = 1-fixed-variable; points.append(weight)
            points = np.asarray(points); px, py = barycentric_to_xy(points); pz = elevation(points)+.025
            xs.extend([*px, None]); ys.extend([*py, None]); zs.extend([*pz, None])
    return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", name="Simplex grid", line=dict(color="rgba(255,255,255,.20)", width=1), hoverinfo="skip")


def demo_surface_with_population(population, path, terrain, highlight_event=None, show_population=True, show_path=True, show_contours=True, show_grid=True, show_contamination=True):
    grid, x, y, z, fitness, triangles = _surface(terrain)
    fig = go.Figure(go.Mesh3d(
        x=x, y=y, z=z, i=triangles[:,0], j=triangles[:,1], k=triangles[:,2], intensity=fitness,
        colorscale=[[0,"#103b66"],[.22,"#176b87"],[.43,"#3c9d7a"],[.62,"#d7bd43"],[.80,"#e67e22"],[1,"#9e281d"]],
        opacity=.99, flatshading=False,
        lighting=dict(ambient=.22, diffuse=.92, specular=.42, roughness=.35, fresnel=.25), lightposition=dict(x=120, y=-80, z=210),
        customdata=np.c_[grid, fitness], hovertemplate="X=%{customdata[0]:.2f}<br>Y=%{customdata[1]:.2f}<br>Z=%{customdata[2]:.2f}<br>Synthetic error=%{customdata[3]:.3f}<extra></extra>", showscale=False,
    ))
    def elevation(weights):
        values = demo_objective(weights[:,0], weights[:,1], weights[:,2], terrain)
        return .62 + 8.15 * (values - fitness.min()) / (fitness.max() - fitness.min())
    if show_contours: fig.add_trace(_contour_trace(x, y, z, triangles, np.linspace(z.min()+.5, z.max()-.4, 14)))
    if show_grid: fig.add_trace(_simplex_grid_trace(terrain, elevation))
    corners = np.array([[1,0,0],[0,1,0],[0,0,1]]); cx, cy = barycentric_to_xy(corners)
    fig.add_trace(go.Scatter3d(x=cx,y=cy,z=elevation(corners)+.15,mode="markers+text",text=["X\n(1, 0, 0)", "Y\n(0, 1, 0)", "Z\n(0, 0, 1)"],textposition="top center",marker=dict(size=7,color="#17232b"),textfont=dict(size=13,color="#17232b"),name="Simplex axes",showlegend=False,hoverinfo="skip"))
    if show_contamination and terrain["contamination"] != "none" and terrain["rate"] > 0:
        centers = {"upper_tail": [[.08,.27,.65]], "symmetric": [[.28,.07,.65],[.07,.28,.65]], "bimodal": [[.28,.07,.65],[.07,.28,.65],[.16,.57,.27]], "point_mass": [[.28,.07,.65]]}[terrain["contamination"]]
        rng = np.random.default_rng(1907); count = max(5, int(terrain["rate"]*70))
        stress = np.asarray([_simplex(np.asarray(centers[i % len(centers)]) + rng.normal(0,.025,3)) for i in range(count)])
        sx, sy = barycentric_to_xy(stress)
        fig.add_trace(go.Scatter3d(x=sx,y=sy,z=elevation(stress)+.12,mode="markers",name="Contamination stress",marker=dict(size=4.5,color="rgba(255,90,35,.70)",symbol="x"),hovertemplate="Contamination stress zone<extra></extra>"))
    if show_population:
        px, py = barycentric_to_xy(population)
        fig.add_trace(go.Scatter3d(x=px,y=py,z=elevation(population)+.07,mode="markers",name="GA candidates",marker=dict(size=6,color="rgba(250,252,255,.95)",line=dict(color="#17232b",width=1)),customdata=demo_objective(*population.T,terrain),hovertemplate="Candidate fitness=%{customdata:.3f}<extra></extra>"))
    if show_path:
        tx, ty = barycentric_to_xy(path)
        fig.add_trace(go.Scatter3d(x=tx,y=ty,z=elevation(path)+.16,mode="lines+markers",name="Best-so-far trace",line=dict(color="rgba(185,22,42,.82)",width=5),marker=dict(size=5.5,color="#ef233c",line=dict(color="#ffffff",width=1.2))))
    target = terrain["target"][None,:]; tx, ty = barycentric_to_xy(target)
    # Scatter3d has no native star marker; overlay a star glyph on a gold
    # diamond so the optimum remains unambiguous in every supported browser.
    fig.add_trace(go.Scatter3d(x=tx,y=ty,z=elevation(target)+.24,mode="markers+text",text=["★"],textposition="middle center",textfont=dict(size=20,color="#5c4200"),name="Perfect convergence",marker=dict(size=15,color="#ffe04b",symbol="diamond",line=dict(color="#684c00",width=2))))
    if highlight_event is not None:
        parents=np.vstack([highlight_event["parent_a"],highlight_event["parent_b"]]); child=np.asarray(highlight_event["child"])[None,:]
        px,py=barycentric_to_xy(parents); cx,cy=barycentric_to_xy(child); pz=elevation(parents)+.21; cz=elevation(child)+.29
        fig.add_trace(go.Scatter3d(x=px,y=py,z=pz,mode="markers",name="Selected parents",marker=dict(size=8,color="#3b82c4",line=dict(color="white",width=1.2))))
        fig.add_trace(go.Scatter3d(x=[px[0],cx[0],None,px[1],cx[0]],y=[py[0],cy[0],None,py[1],cy[0]],z=[pz[0],cz[0],None,pz[1],cz[0]],mode="lines",name="Inheritance links",line=dict(color="rgba(59,130,196,.88)",width=5)))
        fig.add_trace(go.Scatter3d(x=cx,y=cy,z=cz,mode="markers",name="Explained child",marker=dict(size=11,color="#e31a1c" if highlight_event["mutated"] else "#23a36a",symbol="diamond",line=dict(color="white",width=1.5))))
    # High front perspective: the B--C edge stays in front, the mountain
    # plateau rises at the rear, and all three spatial axes are immediately
    # legible on first render.
    fig.update_layout(height=780, margin=dict(l=0,r=0,t=54,b=0), title=f"Simplex convergence landscape — {terrain['label']}", legend=dict(orientation="h",y=1.02,font=dict(size=10)), scene=dict(xaxis=dict(visible=False),yaxis=dict(visible=False),zaxis=dict(visible=False),bgcolor="rgba(0,0,0,0)",aspectratio=dict(x=1.85,y=1,z=.72),camera=dict(eye=dict(x=0,y=-2.25,z=1.45),center=dict(x=0,y=.10,z=.12),up=dict(x=0,y=0,z=1),projection=dict(type="perspective"))))
    return fig
