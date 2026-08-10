"""Fixed-camera simplex renderer for the Layer 2 GA teaching animation."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation

from src.simplex import _surface, barycentric_to_xy, demo_objective


def fixed_simplex_figure(population, history, terrain, event=None, show_population=True,
                         show_path=True, show_contours=True, show_grid=True,
                         show_contamination=True):
    """Draw one deterministic, non-interactive camera frame of the GA search."""
    grid, x, y, elevation, fitness, triangles = _surface(terrain)
    fig = plt.figure(figsize=(15.5, 6.4), dpi=150, facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    tri = Triangulation(x, y, triangles)
    surface = ax.plot_trisurf(tri, elevation, cmap="turbo", linewidth=.08, antialiased=True,
                              shade=True, vmin=elevation.min(), vmax=np.percentile(elevation, 96))
    if show_contours:
        ax.tricontour(tri, elevation, levels=18, colors="white", linewidths=.55, alpha=.62)

    def z_at(weights):
        values = demo_objective(weights[:, 0], weights[:, 1], weights[:, 2], terrain)
        normalized = np.clip((values-fitness.min())/(fitness.max()-fitness.min()), 0, None)
        return .16 + 7.75 * normalized**1.35

    if show_grid:
        for fixed in (.2, .4, .6, .8):
            for axis in range(3):
                points = []
                for variable in np.linspace(0, 1-fixed, 26):
                    w = np.zeros(3); w[axis] = fixed; w[(axis+1)%3] = variable; w[(axis+2)%3] = 1-fixed-variable; points.append(w)
                points = np.asarray(points); gx, gy = barycentric_to_xy(points)
                ax.plot(gx, gy, z_at(points)+.025, color="white", alpha=.16, linewidth=.45)

    contamination = terrain.get("contamination", "upper_tail"); rate = terrain.get("rate", .10)
    if show_contamination and contamination != "none" and rate:
        centers = {"upper_tail": [[.08,.27,.65]], "symmetric": [[.28,.07,.65],[.07,.28,.65]],
                   "bimodal": [[.28,.07,.65],[.07,.28,.65],[.16,.57,.27]], "point_mass": [[.28,.07,.65]]}[contamination]
        rng = np.random.default_rng(1907); stress = []
        for i in range(max(5, int(rate*70))):
            point = np.maximum(np.asarray(centers[i % len(centers)]) + rng.normal(0,.025,3), .01); stress.append(point/point.sum())
        stress = np.asarray(stress); sx, sy = barycentric_to_xy(stress)
        ax.scatter(sx, sy, z_at(stress)+.12, s=16, c="#ff5722", marker="x", alpha=.78, depthshade=False)

    if show_population:
        px, py = barycentric_to_xy(population)
        ax.scatter(px, py, z_at(population)+.24, s=34, c="white", edgecolors="#334155", linewidths=.55, depthshade=False)
    if show_path and len(history):
        hx, hy = barycentric_to_xy(history); hz = z_at(history)+.38
        ax.plot(hx, hy, hz, color="#9f1239", linewidth=2.1, linestyle="--", alpha=.90)
        ax.scatter(hx, hy, hz, s=28, c="#ef233c", edgecolors="white", linewidths=.45, depthshade=False)

    target = terrain["target"][None, :]; tx, ty = barycentric_to_xy(target); tz = z_at(target)+.32
    ax.scatter(tx, ty, tz, s=210, c="#facc15", marker="*", edgecolors="#713f12", linewidths=.9, depthshade=False, zorder=20)
    if event and event.get("event_type") == "offspring":
        parents = np.vstack([event["parent_a"], event["parent_b"]]); child = np.asarray(event["child"])[None, :]
        px, py = barycentric_to_xy(parents); cx, cy = barycentric_to_xy(child); pz=z_at(parents)+.27; cz=z_at(child)+.34
        ax.scatter(px, py, pz, s=55, c="#2563eb", edgecolors="white", linewidths=.7, depthshade=False)
        ax.plot([px[0],cx[0]], [py[0],cy[0]], [pz[0],cz[0]], color="#2563eb", linewidth=1.5, linestyle="--")
        ax.plot([px[1],cx[0]], [py[1],cy[0]], [pz[1],cz[0]], color="#2563eb", linewidth=1.5, linestyle="--")
        ax.scatter(cx, cy, cz, s=68, c="#f59e0b" if event["mutated"] else "#22c55e", marker="D", edgecolors="white", linewidths=.7, depthshade=False)

    corners = np.array([[1,0,0],[0,1,0],[0,0,1]]); cx, cy = barycentric_to_xy(corners); cz=z_at(corners)+.2
    for xx, yy, zz, label in zip(cx,cy,cz,["X\n(1, 0, 0)", "Y\n(0, 1, 0)", "Z\n(0, 0, 1)"]):
        ax.scatter([xx],[yy],[zz],s=38,c="#17232b",depthshade=False); ax.text(xx,yy,zz+.25,label,fontsize=8,ha="center",va="bottom")
    ax.view_init(elev=26, azim=-90, roll=0); ax.set_proj_type("ortho")
    ax.set_box_aspect((1.8, .92, .72)); ax.set_xlim(-.04,1.04); ax.set_ylim(-.07,.93); ax.set_zlim(0,8.35)
    ax.set_axis_off(); ax.set_facecolor("white")
    fig.subplots_adjust(left=.01, right=.90, bottom=.02, top=.96)
    colorbar = fig.colorbar(surface, ax=ax, fraction=.027, pad=.02, shrink=.63)
    colorbar.set_ticks([fitness.min(), (fitness.min()+fitness.max())/2, fitness.max()])
    colorbar.set_ticklabels(["Low error", "Medium", "High error"]); colorbar.ax.tick_params(labelsize=8)
    return fig
