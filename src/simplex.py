"""Artificial terrain used to make a 3-weight simplex search visible."""
import numpy as np
import plotly.graph_objects as go


def barycentric_grid(step=.025):
    rows = []
    for a in np.arange(0, 1 + 1e-9, step):
        for b in np.arange(0, 1 + 1e-9, step):
            c = 1 - a - b
            if c >= -1e-9: rows.append((a, b, max(0., c)))
    return np.asarray(rows)


def barycentric_to_xy(weights):
    weights = np.asarray(weights, dtype=float)
    return weights[..., 1] + .5 * weights[..., 2], np.sqrt(3) / 2 * weights[..., 2]


def demo_objective(a, b, c):
    """Synthetic pedagogical fitness; lower is better and has no thesis meaning."""
    a, b, c = np.asarray(a), np.asarray(b), np.asarray(c)
    global_distance = 1.55 * (a - .18) ** 2 + 2.10 * (b - .55) ** 2 + 1.30 * (c - .27) ** 2
    local_well = np.exp(-((a - .57) ** 2 / .018 + (b - .18) ** 2 / .020 + (c - .25) ** 2 / .024))
    global_well = np.exp(-((a - .18) ** 2 / .012 + (b - .55) ** 2 / .018 + (c - .27) ** 2 / .014))
    ridge = .11 * np.exp(-((a - .37) ** 2 / .012 + (b - .35) ** 2 / .10))
    texture = .024 * np.sin(15 * a + 3 * b) * np.cos(11 * b - 2 * c)
    return .55 + global_distance - .22 * local_well - .44 * global_well + ridge + texture


def _surface():
    grid = barycentric_grid(); x, y = barycentric_to_xy(grid); fitness = demo_objective(*grid.T)
    return grid, x, y, .35 + 4.8 * (fitness - fitness.min()), fitness


def demo_surface_with_population(population, path, highlight_event=None):
    grid, x, y, z, fitness = _surface()
    fig = go.Figure(go.Mesh3d(x=x, y=y, z=z, intensity=fitness, colorscale="RdYlGn_r", opacity=.98, alphahull=0, flatshading=False, contour=dict(show=True, color="rgba(255,255,255,.55)", width=1), lighting=dict(ambient=.35, diffuse=.85, specular=.30, roughness=.55, fresnel=.15), lightposition=dict(x=150, y=100, z=200), customdata=np.c_[grid, fitness], hovertemplate="A=%{customdata[0]:.2f}<br>B=%{customdata[1]:.2f}<br>C=%{customdata[2]:.2f}<br>Pedagogical fitness=%{customdata[3]:.3f}<extra></extra>", showscale=False))
    elevation = lambda weights: .35 + 4.8 * (demo_objective(weights[:, 0], weights[:, 1], weights[:, 2]) - fitness.min())
    corners = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]); cx, cy = barycentric_to_xy(corners)
    fig.add_trace(go.Scatter3d(x=cx, y=cy, z=elevation(corners)+.1, mode="markers+text", text=["A · Biweight", "B · Median", "C · Trimean"], textposition="top center", marker=dict(size=5, color="#25313a"), textfont=dict(size=11), showlegend=False, hoverinfo="skip"))
    px, py = barycentric_to_xy(population)
    fig.add_trace(go.Scatter3d(x=px, y=py, z=elevation(population)+.035, mode="markers", name="Current population", marker=dict(size=4.8, color="rgba(245,247,250,.95)", line=dict(color="#34424b", width=.8)), customdata=demo_objective(*population.T), hovertemplate="Current candidate<br>Fitness=%{customdata:.3f}<extra></extra>"))
    tx, ty = barycentric_to_xy(path)
    fig.add_trace(go.Scatter3d(x=tx, y=ty, z=elevation(path)+.075, mode="lines+markers", name="Best so far", line=dict(color="#e6533f", width=8), marker=dict(size=4.2, color="#e6533f")))
    target = np.array([[.18, .55, .27]]); tx, ty = barycentric_to_xy(target)
    fig.add_trace(go.Scatter3d(x=tx, y=ty, z=elevation(target)+.15, mode="markers", name="Global optimum", marker=dict(size=10, color="#ffd23f", symbol="diamond", line=dict(color="#8d6700", width=1.5))))
    if highlight_event:
        parents = np.vstack([highlight_event["parent_a"], highlight_event["parent_b"]]); child = np.asarray(highlight_event["child"])[None, :]
        px, py = barycentric_to_xy(parents); cx, cy = barycentric_to_xy(child); parent_z = elevation(parents)+.13; child_z = elevation(child)+.18
        fig.add_trace(go.Scatter3d(x=px, y=py, z=parent_z, mode="markers", name="Selected parents", marker=dict(size=7, color="#246e9e", line=dict(color="white", width=1))))
        fig.add_trace(go.Scatter3d(x=[px[0],cx[0],px[1]], y=[py[0],cy[0],py[1]], z=[parent_z[0],child_z[0],parent_z[1]], mode="lines", name="Inheritance", line=dict(color="rgba(36,110,158,.75)", width=5)))
        fig.add_trace(go.Scatter3d(x=cx, y=cy, z=child_z, mode="markers", name="Explained child", marker=dict(size=9, color="#e6533f" if highlight_event["mutated"] else "#2f8f68", symbol="diamond", line=dict(color="white", width=1.4))))
    fig.update_layout(height=720, margin=dict(l=0,r=0,t=45,b=0), title="Artificial fitness landscape — lower is better", legend=dict(orientation="h", y=1.02, font=dict(size=11)), scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)", aspectratio=dict(x=1.30,y=1,z=.55), camera=dict(eye=dict(x=1.48,y=-1.62,z=1.12))))
    return fig
