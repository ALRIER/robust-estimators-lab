import numpy as np
import plotly.graph_objects as go


def barycentric_grid(step=0.04):
    rows = []
    vals = np.arange(0, 1 + 1e-9, step)
    for a in vals:
        for b in vals:
            c = 1 - a - b
            if c >= -1e-9:
                rows.append((a, b, max(0.0, c)))
    return np.asarray(rows)


def demo_objective(a, b, c):
    """Pedagogical terrain only — NOT a thesis objective/output."""
    basin = (a - 0.42) ** 2 + 1.25 * (b - 0.33) ** 2 + 0.8 * (c - 0.25) ** 2
    ridge = 0.10 * np.sin(8 * a) * np.cos(7 * b)
    return 0.04 + basin + ridge


def demo_surface_figure():
    grid = barycentric_grid(0.035)
    a, b, c = grid.T
    # Map barycentric triangle into Cartesian plane.
    x = b + 0.5 * c
    y = np.sqrt(3) / 2 * c
    z = demo_objective(a, b, c)
    fig = go.Figure(
        go.Mesh3d(
            x=x, y=y, z=z,
            intensity=z,
            colorscale="RdYlGn_r",
            opacity=0.92,
            alphahull=0,
            hovertemplate="A=%{customdata[0]:.2f}<br>B=%{customdata[1]:.2f}<br>C=%{customdata[2]:.2f}<br>Error=%{z:.3f}<extra></extra>",
            customdata=np.c_[a,b,c],
        )
    )
    fig.update_layout(
        height=650,
        margin=dict(l=0,r=0,t=20,b=0),
        scene=dict(
            xaxis_title="Simplex slice coordinate",
            yaxis_title="Simplex slice coordinate",
            zaxis_title="Demo error",
            aspectratio=dict(x=1.2,y=1,z=0.65),
        ),
    )
    return fig


def barycentric_to_xy(weights):
    weights = np.asarray(weights, dtype=float)
    return weights[..., 1] + .5 * weights[..., 2], np.sqrt(3) / 2 * weights[..., 2]


def demo_surface_with_population(population=None, path=None):
    fig = demo_surface_figure()
    if population is not None:
        x, y = barycentric_to_xy(population); z = demo_objective(population[:, 0], population[:, 1], population[:, 2])
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="markers", name="Population", marker=dict(size=3.5, color="#25313a", opacity=.65)))
    if path is not None:
        x, y = barycentric_to_xy(path); z = demo_objective(path[:, 0], path[:, 1], path[:, 2])
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines+markers", name="Best path", line=dict(color="#e6533f", width=6), marker=dict(size=4, color="#e6533f")))
    fig.update_layout(legend=dict(orientation="h", y=1.03), title="DEMO MODE — pedagogical mini-GA")
    return fig
