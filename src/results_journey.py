"""Self-explaining visual story for Layer 7 thesis results.

All numbers are fixed thesis outputs already exported with the dashboard bundle.
This module never reruns the GA or recomputes research evidence.
"""

import plotly.graph_objects as go

RESULT_STAGES = (
    {
        "label": "1–2 · Discovery + Frozen I",
        "question": "What survived the first search?",
        "claim": "TWO CONFIRMED SIGNALS",
        "plain": "Many opportunities appeared. Only two survived frozen confirmation.",
        "color": "#e66d4f",
        "what": "The first GA search produced candidate wins, and then the exact same weights were tested again without retraining.",
        "happened": "36 controlled regimes produced 16 discovery wins. Frozen confirmation reduced that set to two Lognormal signals: CV-019 and CV-010.",
        "means": "Discovery tells us where to look. Frozen confirmation tells us what we can defend.",
        "not_claim": "Do not call all 16 discovery wins confirmed results.",
        "key": "36 → 16 → 2",
    },
    {
        "label": "3 · Expanded rediscovery",
        "question": "What changed when the search space became stronger?",
        "claim": "OPPORTUNITY MAP CHANGED",
        "plain": "A stronger 26-component search found a different pattern of opportunity.",
        "color": "#a777e3",
        "what": "The search was reopened with 26 learnable estimators instead of 10, stronger HPF2 exposure, and the modern benchmark gate active from the start.",
        "happened": "Twelve discovery winners appeared across five of the six families. Inverse Gaussian contributed the largest number of winners; Ex-Gaussian contributed none.",
        "means": "Changing the estimator library changes where useful mixtures can be found. The opportunity is structural, not universal.",
        "not_claim": "Do not treat these twelve discovery wins as fixed-weight confirmations.",
        "key": "10 → 26 components · 12 discovery winners",
    },
    {
        "label": "4 · Strict validation",
        "question": "Did the new candidates really transfer?",
        "claim": "TWO WEIBULL TRANSFER SPECIALISTS",
        "plain": "They worked in related unseen regimes, but not everywhere.",
        "color": "#54c786",
        "what": "The exact frozen 26-component candidates were tested in two modes: their original regime and a related locked-unseen regime.",
        "happened": "FWVR011 and FWVR012 passed both mean and q95 gates in locked-unseen validation, but both performed substantially worse in original-regime validation.",
        "means": "These are narrow specialists. Their value is real, but their scope is limited to a validated profile.",
        "not_claim": "Do not say that the GA found a generally better estimator for Weibull data.",
        "key": "2 transfer specialists · original FAIL / locked-unseen PASS",
    },
    {
        "label": "5A · Real-world battery",
        "question": "Does the signal appear in real data?",
        "claim": "EXTERNAL CALIBRATION",
        "plain": "The signal appears in real data, but external evidence is not known-truth validation.",
        "color": "#58aee8",
        "what": "Frozen specialists were applied to external datasets without retraining, after the data passed the loading, preparation, and eligibility filters.",
        "happened": "264 targets were requested, 228 loaded, 120 evaluated, and 43 parent datasets were eligible. Twenty-six of those 43 parents had at least one corrected win, producing 255 profile-matched confirmations.",
        "means": "Breadth is 26 of 43 independent parent datasets. Depth is 255 repeated profile-level confirmations inside that external battery.",
        "not_claim": "Do not describe the 255 confirmations as 255 independent datasets or as population-ground-truth validation.",
        "key": "264 → 228 → 120 → 43 · 26/43 parents · 255 confirmations",
    },
    {
        "label": "5B · Dirichlet audit",
        "question": "Was benchmark retention meaningful?",
        "claim": "ABSTENTION AUDIT",
        "plain": "In most retained cells, even random simplex search could not beat the benchmark.",
        "color": "#4fc3ff",
        "what": "Random Dirichlet weight vectors were tested in benchmark-retained cells using the original dual gate. This is an audit of abstention, not a new GA search.",
        "happened": "Twenty-three of 34 audited cells had no random pass. Eleven showed some random signal. All eight strongest positive controls passed.",
        "means": "Benchmark retention was often a substantive result rather than simply a weak GA search.",
        "not_claim": "Do not assume that every retained benchmark would have been easy to beat with more GA generations.",
        "key": "23/34 no random pass · 11/34 some signal · 8/8 controls pass",
    },
)

EXPLAIN_STEPS = (
    (
        "1 · SIGNAL — The first search produced 16 apparent wins across 36 controlled regimes.",
        "2 · PRESSURE — The weights were frozen and tested again on fresh validation seeds.",
        "3 · MEANING — Only CV-019 and CV-010 remained defensible Lognormal signals.",
    ),
    (
        "1 · CHANGE — The learnable basis expanded from 10 to 26 estimators.",
        "2 · PRESSURE — HPF2 increased to 90% and modern robust competition was active from the beginning.",
        "3 · MEANING — The family map changed, showing that opportunity depends on the search basis and regime.",
    ),
    (
        "1 · SIGNAL — Two Weibull candidates looked strong after expanded rediscovery.",
        "2 · PRESSURE — Their frozen weights were tested in original and locked-unseen regimes.",
        "3 · MEANING — Only narrow transfer survived, so the correct label is specialist, not universal winner.",
    ),
    (
        "1 · FILTER — The external battery narrowed from 264 requested targets to 43 eligible parents.",
        "2 · EVIDENCE — Twenty-six parents produced at least one corrected win, with 255 profile-matched confirmations.",
        "3 · MEANING — This supports empirical transfer, while Monte Carlo remains the known-truth validation layer.",
    ),
    (
        "1 · QUESTION — Could arbitrary simplex weights easily beat cells where the benchmark was retained?",
        "2 · AUDIT — 4,000 random vectors across eight seeds were used as an independent abstention probe.",
        "3 · MEANING — No random pass in 23 of 34 cells supports the interpretation that retention was often meaningful.",
    ),
)


def _base_layout(fig, title, subtitle="", height=520):
    fig.update_layout(
        title={"text": f"<b>{title}</b><br><span style='font-size:13px;color:#aebed3'>{subtitle}</span>", "x": 0.02, "xanchor": "left"},
        height=height,
        margin=dict(l=30, r=28, t=82, b=48),
        plot_bgcolor="#081525",
        paper_bgcolor="#081525",
        font=dict(color="#e9f4ff", size=13),
        showlegend=False,
    )
    return fig


def _card(fig, x0, y0, x1, y1, title, value, detail, border="#4fc3ff", fill="#0d2842"):
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=x0, y0=y0, x1=x1, y1=y1,
                  line=dict(color=border, width=1.5), fillcolor=fill, layer="below")
    fig.add_annotation(xref="paper", yref="paper", x=(x0+x1)/2, y=y1-0.05, showarrow=False,
                       text=f"<b>{title}</b>", font=dict(size=13, color="#72cfff"), xanchor="center", yanchor="top")
    fig.add_annotation(xref="paper", yref="paper", x=(x0+x1)/2, y=(y0+y1)/2+0.03, showarrow=False,
                       text=f"<b>{value}</b>", font=dict(size=24, color="#f7d768"), xanchor="center")
    fig.add_annotation(xref="paper", yref="paper", x=(x0+x1)/2, y=y0+0.05, showarrow=False,
                       text=detail, font=dict(size=11, color="#dce9f8"), xanchor="center", yanchor="bottom", align="center")


def result_figure(stage: int):
    stage = max(0, min(int(stage), 4))
    if stage == 0:
        fig = go.Figure(go.Funnel(
            y=["Controlled regimes", "Discovery wins", "Frozen confirmations"],
            x=[36, 16, 2],
            domain=dict(x=[0.02, 0.56], y=[0.05, 0.95]),
            marker=dict(color=["#526a85", "#f3c743", "#54c786"]),
            textinfo="value+percent initial",
            textfont=dict(size=15),
            connector=dict(line=dict(color="#4d7898", width=1.5)),
        ))
        _card(fig, .62, .54, .96, .91, "CV-019 · LOGNORMAL", "+16.3% q95 MSE", "8/8 validation seeds<br>95% CI: 7.6% to 23.2%", border="#54c786")
        _card(fig, .62, .08, .96, .45, "CV-010 · LOGNORMAL", "+2.2% q95 MSE", "8/8 validation seeds<br>95% CI: 1.9% to 2.8%", border="#54c786")
        return _base_layout(fig, "What survived the first search?", "Discovery created possibilities; freezing removed most of them.")

    if stage == 1:
        families = ["Normal", "Lognormal", "Weibull", "Inverse Gaussian", "Ex-Gaussian", "Ex-Wald"]
        counts = [1, 2, 2, 4, 0, 3]
        fig = go.Figure(go.Bar(
            x=families, y=counts,
            marker_color=["#6d7f96", "#a777e3", "#54c786", "#f3c743", "#526a85", "#58aee8"],
            text=["1", "2", "2", "4", "0", "3"], textposition="outside",
            hovertemplate="%{x}<br>Discovery winners: %{y}<extra></extra>",
        ))
        fig.update_yaxes(range=[0, 5.2], title="Expanded discovery winners", dtick=1, gridcolor="#214664")
        fig.add_annotation(xref="paper", yref="paper", x=.5, y=1.13, showarrow=False,
                           text="<b>10 → 26 learnable components</b>   ·   HPF2 80% → 90%   ·   warm starts CV-019 / CV-010",
                           font=dict(size=13, color="#dce9f8"))
        fig.add_annotation(x="Inverse Gaussian", y=4.55, showarrow=False, text="best q95 discovery gain: <b>38.2%</b>", font=dict(size=11, color="#f7d768"))
        fig.add_annotation(x="Weibull", y=2.55, showarrow=False, text="best: <b>23.6%</b>", font=dict(size=11, color="#c8ffd7"))
        fig.add_annotation(x="Ex-Wald", y=3.55, showarrow=False, text="best: <b>20.6%</b>", font=dict(size=11, color="#bfe7ff"))
        return _base_layout(fig, "What changed when the search space became stronger?", "Twelve discovery winners appeared, but their family pattern changed.")

    if stage == 2:
        cats = ["FWVR011<br>Mean", "FWVR011<br>q95", "FWVR012<br>Mean", "FWVR012<br>q95"]
        locked = [2.785, 2.719, 3.175, 1.248]
        original = [-15.774, -45.062, -15.196, -34.563]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Locked-unseen", x=cats, y=locked, marker_color="#54c786",
                             text=[f"+{v:.2f}% PASS" for v in locked], textposition="outside"))
        fig.add_trace(go.Bar(name="Original regime", x=cats, y=original, marker_color="#e66d4f",
                             text=[f"{v:.2f}% FAIL" for v in original], textposition="outside"))
        fig.update_layout(barmode="group", showlegend=True, legend=dict(orientation="h", y=1.02, x=.02))
        fig.update_yaxes(title="Gain vs strongest admissible benchmark (%)", gridcolor="#214664", zeroline=True, zerolinecolor="#f3c743", zerolinewidth=2)
        fig.add_annotation(xref="paper", yref="paper", x=.5, y=-.17, showarrow=False,
                           text="<b>25-candidate taxonomy:</b> 2 transfer specialists · 10 local · 7 near-gate · 6 controls",
                           font=dict(size=12, color="#dce9f8"))
        return _base_layout(fig, "Did the new candidates really transfer?", "Positive values favour the frozen GA candidate; negative values favour the benchmark.", height=560)

    if stage == 3:
        fig = go.Figure(go.Funnel(
            y=["Requested targets", "Loaded", "Evaluated", "Eligible parents"],
            x=[264, 228, 120, 43],
            domain=dict(x=[0.02, 0.57], y=[0.05, 0.95]),
            marker=dict(color=["#526a85", "#5f7896", "#58aee8", "#54c786"]),
            textinfo="value+percent initial",
            textfont=dict(size=14),
        ))
        _card(fig, .63, .54, .96, .91, "BREADTH", "26 / 43 parents", "At least one corrected win<br>across eligible parent datasets", border="#58aee8")
        _card(fig, .63, .08, .96, .45, "DEPTH", "255 confirmations", "Profile-matched FDR 5% results<br>inside the external battery", border="#a777e3")
        fig.add_annotation(xref="paper", yref="paper", x=.80, y=.01, showarrow=False,
                           text="255 confirmations ≠ 255 independent datasets", font=dict(size=11, color="#f7d768"))
        return _base_layout(fig, "Does the signal appear in real data?", "External calibration is evidence of transfer, not known-population truth.")

    # Stage 5B: 34 audited cells as a literal cell map.
    xs, ys, colors, hover = [], [], [], []
    for i in range(34):
        xs.append(i % 9)
        ys.append(3 - (i // 9))
        if i < 23:
            colors.append("#526a85")
            hover.append("No random pass")
        else:
            colors.append("#4fc3ff")
            hover.append("Some random signal")
    fig = go.Figure(go.Scatter(
        x=xs, y=ys, mode="markers",
        marker=dict(symbol="square", size=34, color=colors, line=dict(color="#0c2035", width=1.5)),
        text=hover, hovertemplate="Audited cell %{text}<extra></extra>",
    ))
    fig.update_xaxes(visible=False, range=[-.7, 8.7])
    fig.update_yaxes(visible=False, range=[-.7, 3.7])
    fig.add_annotation(xref="paper", yref="paper", x=.02, y=.06, showarrow=False, xanchor="left",
                       text="■ <span style='color:#9eb1c7'>23 / 34 no random pass</span>     ■ <span style='color:#72cfff'>11 / 34 some signal</span>",
                       font=dict(size=13, color="#dce9f8"))
    _card(fig, .70, .63, .97, .92, "POSITIVE CONTROL", "8 / 8 PASS", "Strongest controls behaved as expected", border="#54c786")
    fig.add_annotation(xref="paper", yref="paper", x=.73, y=.34, showarrow=False, xanchor="left", align="left",
                       text="<b>Question answered:</b><br>Could random simplex weights<br>easily beat a retained benchmark?", font=dict(size=12, color="#dce9f8"))
    return _base_layout(fig, "Was benchmark retention meaningful?", "Each square is one audited benchmark-retained cell.")


def message_html(stage: int) -> str:
    item = RESULT_STAGES[max(0, min(int(stage), 4))]
    return f'''<div class="result-bubble">
      <div class="result-kicker">CLAIM STATUS</div>
      <div class="result-claim" style="color:{item['color']}">{item['claim']}</div>
      <div class="result-plain">{item['plain']}</div>
      <div class="result-label">WHAT YOU ARE SEEING</div><div class="result-copy">{item['what']}</div>
      <div class="result-label">WHAT HAPPENED</div><div class="result-copy">{item['happened']}</div>
      <div class="result-label">WHAT IT MEANS</div><div class="result-copy">{item['means']}</div>
      <div class="result-label warn">DO NOT OVERCLAIM</div><div class="result-copy">{item['not_claim']}</div>
    </div>'''
