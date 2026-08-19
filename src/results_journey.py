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


BG = "#081525"
PANEL = "#0d2842"
PANEL2 = "#102f4d"
BLUE = "#58aee8"
CYAN = "#72cfff"
GOLD = "#f3c743"
GREEN = "#54c786"
RED = "#e66d4f"
PURPLE = "#a777e3"
MUTED = "#526a85"
TEXT = "#e9f4ff"
SUBTLE = "#aebed3"


def _base_layout(fig, title, subtitle="", height=610):
    fig.update_layout(
        title={
            "text": f"<b>{title}</b><br><span style='font-size:13px;color:{SUBTLE}'>{subtitle}</span>",
            "x": 0.02,
            "xanchor": "left",
        },
        height=height,
        margin=dict(l=24, r=24, t=86, b=28),
        plot_bgcolor=BG,
        paper_bgcolor=BG,
        font=dict(color=TEXT, size=13),
        showlegend=False,
        xaxis=dict(visible=False, range=[0, 1], fixedrange=True),
        yaxis=dict(visible=False, range=[0, 1], fixedrange=True),
    )
    return fig


def _rect(fig, x0, y0, x1, y1, fill=PANEL, border="#326188", width=1.4):
    fig.add_shape(
        type="rect", xref="x", yref="y", x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(color=border, width=width), fillcolor=fill, layer="below",
    )


def _text(fig, x, y, text, size=13, color=TEXT, anchor="center", align="center", bold=False):
    if bold:
        text = f"<b>{text}</b>"
    fig.add_annotation(
        x=x, y=y, xref="x", yref="y", showarrow=False, text=text,
        xanchor=anchor, align=align, font=dict(size=size, color=color),
    )


def _arrow(fig, x0, y0, x1, y1, color=CYAN, width=2):
    fig.add_annotation(
        x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
        text="", showarrow=True, arrowhead=2, arrowsize=1.1, arrowwidth=width, arrowcolor=color,
    )


def _pill(fig, x0, y0, x1, y1, label, value=None, fill=PANEL, border="#326188", value_color=GOLD):
    _rect(fig, x0, y0, x1, y1, fill=fill, border=border, width=1.2)
    if value is None:
        _text(fig, (x0 + x1) / 2, (y0 + y1) / 2, label, size=12, color=TEXT, bold=True)
    else:
        _text(fig, (x0 + x1) / 2, y1 - 0.035, label, size=10, color=CYAN, bold=True)
        _text(fig, (x0 + x1) / 2, y0 + 0.045, value, size=16, color=value_color, bold=True)


def _funnel_band(fig, y0, y1, left0, right0, left1, right1, fill, number, title, detail):
    fig.add_trace(go.Scatter(
        x=[left0, right0, right1, left1, left0],
        y=[y1, y1, y0, y0, y1],
        mode="lines", fill="toself",
        line=dict(color=fill, width=1.5), fillcolor=fill,
        hoverinfo="skip", showlegend=False,
    ))
    cx = (left0 + right0 + left1 + right1) / 4
    _text(fig, cx, (y0+y1)/2 + 0.035, str(number), size=27, color="#ffffff", bold=True)
    _text(fig, cx, (y0+y1)/2 - 0.020, title, size=13, color="#ffffff", bold=True)
    _text(fig, cx, y0 + 0.022, detail, size=9, color="#dce9f8")


def _result_discovery_story():
    fig = go.Figure()
    _funnel_band(fig, .69, .88, .04, .57, .10, .51, MUTED, 36, "CONTROLLED REGIMES", "The first discovery programme starts broad")
    _text(fig, .305, .635, "↓  Benchmark gate keeps only candidates that beat admissible comparators", size=10, color=GOLD)
    _funnel_band(fig, .43, .59, .12, .49, .18, .43, GOLD, 16, "DISCOVERY WINS", "Promising during search — not yet confirmed")
    _text(fig, .305, .365, "↓  Freeze the weights · new seeds · no retraining", size=10, color=CYAN)
    _funnel_band(fig, .17, .31, .21, .40, .245, .365, GREEN, 2, "CONFIRMED SIGNALS", "Only fixed-weight evidence survives")

    _text(fig, .73, .89, "WHO SURVIVED?", size=11, color=CYAN, bold=True)
    _rect(fig, .60, .54, .96, .83, fill="#0d302d", border=GREEN, width=1.6)
    _text(fig, .78, .785, "CV-019 · LOGNORMAL", size=13, color="#dfffea", bold=True)
    _text(fig, .78, .705, "+16.3%", size=28, color=GREEN, bold=True)
    _text(fig, .78, .657, "q95 MSE gain", size=11, color=TEXT, bold=True)
    _text(fig, .78, .595, "8 / 8 validation seeds", size=11, color="#dce9f8")

    _rect(fig, .60, .17, .96, .46, fill="#0d302d", border=GREEN, width=1.6)
    _text(fig, .78, .415, "CV-010 · LOGNORMAL", size=13, color="#dfffea", bold=True)
    _text(fig, .78, .335, "+2.2%", size=28, color=GREEN, bold=True)
    _text(fig, .78, .287, "q95 MSE gain", size=11, color=TEXT, bold=True)
    _text(fig, .78, .225, "8 / 8 validation seeds", size=11, color="#dce9f8")

    _rect(fig, .05, .035, .96, .115, fill="#10253a", border="#3c7198")
    _text(fig, .505, .075, "THE STORY: discovery found 16 possibilities; frozen confirmation left only 2 claims we can defend.", size=12, color=GOLD, bold=True)
    return _base_layout(fig, "What survived the first search?", "The funnel explains why candidates disappear instead of treating every discovery win as a result.")


def _result_cycle_comparison():
    fig = go.Figure()
    # Cycle 1 panel
    _rect(fig, .03, .13, .47, .91, fill="#0c243d", border="#507294", width=1.5)
    _text(fig, .25, .865, "CYCLE 1 · ORIGINAL DISCOVERY", size=14, color="#c8d8ea", bold=True)
    _pill(fig, .07, .74, .22, .82, "LEARNABLE", "10", border="#507294")
    _pill(fig, .28, .74, .43, .82, "HPF2", "80%", border="#507294")
    _text(fig, .25, .675, "36 regimes", size=20, color=TEXT, bold=True)
    _arrow(fig, .25, .64, .25, .585, color="#7693ad")
    _text(fig, .25, .545, "16 discovery wins", size=20, color=GOLD, bold=True)
    _text(fig, .25, .493, "search signals", size=10, color=SUBTLE)
    _arrow(fig, .25, .465, .25, .405, color=CYAN)
    _text(fig, .25, .365, "2 confirmed", size=22, color=GREEN, bold=True)
    _text(fig, .25, .318, "both LOGNORMAL", size=11, color="#dfffea", bold=True)
    _pill(fig, .075, .205, .235, .275, "CV-019", "+16.3% q95", fill="#0d302d", border=GREEN, value_color=GREEN)
    _pill(fig, .265, .205, .425, .275, "CV-010", "+2.2% q95", fill="#0d302d", border=GREEN, value_color=GREEN)
    _text(fig, .25, .165, "These two later enter Cycle 2 only as warm starts.", size=9, color=SUBTLE)

    # Directional bridge
    _arrow(fig, .47, .52, .53, .52, color=PURPLE, width=3)
    _text(fig, .50, .585, "STRONGER BASIS", size=10, color=PURPLE, bold=True)
    _text(fig, .50, .455, "search reopens", size=9, color=SUBTLE)

    # Cycle 2 panel
    _rect(fig, .53, .13, .97, .91, fill="#181d3d", border=PURPLE, width=1.6)
    _text(fig, .75, .865, "CYCLE 2 · EXPANDED REDISCOVERY", size=14, color="#eadcff", bold=True)
    _pill(fig, .57, .74, .72, .82, "LEARNABLE", "26", fill="#201f4a", border=PURPLE, value_color="#d6b4ff")
    _pill(fig, .78, .74, .93, .82, "HPF2", "90%", fill="#201f4a", border=PURPLE, value_color="#d6b4ff")
    _text(fig, .75, .675, "12 discovery winners", size=21, color="#d6b4ff", bold=True)
    _text(fig, .75, .63, "now spread across five families", size=10, color=SUBTLE)

    family_specs = [
        ("NORMAL", "1", .57, .49, MUTED),
        ("LOGNORMAL", "2", .70, .49, PURPLE),
        ("WEIBULL", "2", .83, .49, GREEN),
        ("INV. GAUSS.", "4", .57, .33, GOLD),
        ("EX-GAUSS.", "0", .70, .33, MUTED),
        ("EX-WALD", "3", .83, .33, BLUE),
    ]
    for label, value, x, y, color in family_specs:
        _rect(fig, x, y, x+.10, y+.11, fill="#101d31", border=color, width=1.4)
        _text(fig, x+.05, y+.077, label, size=8, color=SUBTLE, bold=True)
        _text(fig, x+.05, y+.035, value, size=20, color=color, bold=True)

    _rect(fig, .57, .18, .93, .265, fill="#241f3f", border=PURPLE)
    _text(fig, .75, .232, "CV-019 + CV-010 = WARM STARTS", size=10, color="#eadcff", bold=True)
    _text(fig, .75, .195, "allowed to compete · no automatic win", size=9, color=SUBTLE)

    _rect(fig, .05, .035, .95, .105, fill="#10253a", border="#3c7198")
    _text(fig, .50, .070, "THE STORY: when the component library became stronger, the winner pattern changed — exactly what regime-conditional search predicts.", size=11, color=GOLD, bold=True)
    return _base_layout(fig, "What changed when the search space became stronger?", "Cycle 1 and Cycle 2 are shown as two different evidence stories, not as one unexplained bar chart.")


def _specialist_card(fig, x0, x1, title, locked_mean, locked_q95, original_mean, original_q95):
    _rect(fig, x0, .22, x1, .90, fill="#0c2238", border="#416f92", width=1.4)
    _text(fig, (x0+x1)/2, .855, title, size=14, color=TEXT, bold=True)
    _text(fig, (x0+x1)/2, .817, "WEIBULL · same frozen weights", size=9, color=SUBTLE)

    _rect(fig, x0+.025, .57, x1-.025, .77, fill="#0d302d", border=GREEN, width=1.6)
    _text(fig, (x0+x1)/2, .735, "LOCKED-UNSEEN · PASS", size=11, color="#dfffea", bold=True)
    _text(fig, x0+.12, .655, f"+{locked_mean:.2f}%", size=21, color=GREEN, bold=True)
    _text(fig, x0+.12, .610, "mean MSE", size=9, color=SUBTLE)
    _text(fig, x1-.12, .655, f"+{locked_q95:.2f}%", size=21, color=GREEN, bold=True)
    _text(fig, x1-.12, .610, "q95 MSE", size=9, color=SUBTLE)

    _text(fig, (x0+x1)/2, .515, "same candidate ↓ tested in another mode", size=9, color=CYAN)

    _rect(fig, x0+.025, .30, x1-.025, .49, fill="#321b20", border=RED, width=1.6)
    _text(fig, (x0+x1)/2, .455, "ORIGINAL-REGIME MODE · FAIL", size=11, color="#ffd9d2", bold=True)
    _text(fig, x0+.12, .382, f"{original_mean:.2f}%", size=20, color=RED, bold=True)
    _text(fig, x0+.12, .338, "mean MSE", size=9, color=SUBTLE)
    _text(fig, x1-.12, .382, f"{original_q95:.2f}%", size=20, color=RED, bold=True)
    _text(fig, x1-.12, .338, "q95 MSE", size=9, color=SUBTLE)

    _text(fig, (x0+x1)/2, .255, "NARROW TRANSFER SPECIALIST — not a family-wide winner", size=9, color=GOLD, bold=True)


def _result_strict_validation():
    fig = go.Figure()
    _specialist_card(fig, .03, .48, "FWVR011", 2.785, 2.719, -15.774, -45.062)
    _specialist_card(fig, .52, .97, "FWVR012", 3.175, 1.248, -15.196, -34.563)

    _text(fig, .50, .165, "25-CANDIDATE EVIDENCE TAXONOMY", size=10, color=CYAN, bold=True)
    _pill(fig, .05, .055, .25, .13, "TRANSFER", "2", fill="#0d302d", border=GREEN, value_color=GREEN)
    _pill(fig, .275, .055, .475, .13, "LOCAL", "10", fill="#15283d", border=BLUE, value_color=BLUE)
    _pill(fig, .525, .055, .725, .13, "NEAR-GATE", "7", fill="#2f2b18", border=GOLD, value_color=GOLD)
    _pill(fig, .75, .055, .95, .13, "CONTROLS", "6", fill="#2b1c22", border=RED, value_color=RED)
    return _base_layout(fig, "Did the new candidates really transfer?", "Each card shows the same frozen specialist under two validation modes — the contrast defines the boundary of the claim.", height=640)


def _result_external_funnel():
    fig = go.Figure()
    _funnel_band(fig, .70, .87, .04, .57, .08, .53, MUTED, 264, "REQUESTED TARGETS", "everything we tried to source")
    _text(fig, .305, .655, "↓  availability + loading", size=9, color=SUBTLE)
    _funnel_band(fig, .53, .64, .10, .51, .14, .47, "#607995", 228, "LOADED", "data could be retrieved")
    _text(fig, .305, .485, "↓  preparation + evaluation", size=9, color=SUBTLE)
    _funnel_band(fig, .36, .46, .16, .45, .20, .41, BLUE, 120, "EVALUATED", "usable after preparation")
    _text(fig, .305, .315, "↓  structural profile eligibility", size=9, color=SUBTLE)
    _funnel_band(fig, .18, .29, .22, .39, .245, .365, GREEN, 43, "ELIGIBLE PARENTS", "fair matches for frozen specialists")

    _text(fig, .77, .88, "WHAT DID THOSE 43 PARENTS SHOW?", size=10, color=CYAN, bold=True)
    _rect(fig, .61, .55, .96, .80, fill="#102c3f", border=BLUE, width=1.6)
    _text(fig, .785, .755, "BREADTH", size=11, color=CYAN, bold=True)
    _text(fig, .785, .675, "26 / 43", size=30, color=BLUE, bold=True)
    _text(fig, .785, .625, "parent datasets", size=11, color=TEXT, bold=True)
    _text(fig, .785, .575, "at least one corrected specialist win", size=9, color=SUBTLE)

    _rect(fig, .61, .24, .96, .49, fill="#221e3e", border=PURPLE, width=1.6)
    _text(fig, .785, .445, "DEPTH", size=11, color="#d9bfff", bold=True)
    _text(fig, .785, .365, "255", size=30, color=PURPLE, bold=True)
    _text(fig, .785, .315, "profile confirmations", size=11, color=TEXT, bold=True)
    _text(fig, .785, .265, "repeated evidence inside eligible parents", size=9, color=SUBTLE)

    _rect(fig, .58, .07, .98, .17, fill="#322b18", border=GOLD)
    _text(fig, .78, .122, "IMPORTANT: 255 confirmations ≠ 255 independent datasets", size=10, color=GOLD, bold=True)
    _text(fig, .78, .088, "Breadth = parents · Depth = repeated profile evidence", size=9, color="#efe5bd")
    return _base_layout(fig, "Does the signal appear in real data?", "The funnel explains why the external battery narrows, while the right side separates breadth from depth.")


def _result_dirichlet_audit():
    fig = go.Figure()
    _rect(fig, .04, .82, .59, .93, fill="#10253a", border=CYAN)
    _text(fig, .315, .885, "AUDIT QUESTION", size=9, color=CYAN, bold=True)
    _text(fig, .315, .845, "Could arbitrary valid simplex mixtures beat benchmark-retained cells?", size=11, color=TEXT, bold=True)
    _arrow(fig, .315, .81, .315, .75, color=CYAN)

    # literal 34-cell audit map
    x0, y0 = .06, .34
    dx, dy = .052, .095
    for i in range(34):
        col = i % 9
        row = i // 9
        xx = x0 + col * dx
        yy = y0 + (3-row) * dy
        fill = MUTED if i < 23 else BLUE
        border = "#8093aa" if i < 23 else CYAN
        _rect(fig, xx, yy, xx+.038, yy+.060, fill=fill, border=border, width=1.0)

    _text(fig, .315, .305, "34 benchmark-retained cells", size=10, color=TEXT, bold=True)
    _text(fig, .315, .270, "each square = one independent audit target", size=9, color=SUBTLE)
    _pill(fig, .07, .16, .29, .235, "GREY", "23 no pass", fill="#17263a", border=MUTED, value_color="#b8c6d6")
    _pill(fig, .34, .16, .56, .235, "BLUE", "11 signal", fill="#102c3f", border=BLUE, value_color=BLUE)

    _text(fig, .77, .88, "HOW TO READ THE AUDIT", size=10, color=CYAN, bold=True)
    _rect(fig, .64, .63, .95, .80, fill="#17263a", border=MUTED)
    _text(fig, .795, .755, "23 / 34", size=27, color="#c5d0de", bold=True)
    _text(fig, .795, .705, "NO RANDOM PASS", size=11, color=TEXT, bold=True)
    _text(fig, .795, .657, "retaining the benchmark resisted the challenge", size=9, color=SUBTLE)

    _rect(fig, .64, .41, .95, .58, fill="#102c3f", border=BLUE)
    _text(fig, .795, .535, "11 / 34", size=27, color=BLUE, bold=True)
    _text(fig, .795, .485, "SOME RANDOM SIGNAL", size=11, color=TEXT, bold=True)
    _text(fig, .795, .437, "these abstentions deserve another look", size=9, color=SUBTLE)

    _rect(fig, .64, .19, .95, .36, fill="#0d302d", border=GREEN)
    _text(fig, .795, .315, "8 / 8", size=27, color=GREEN, bold=True)
    _text(fig, .795, .265, "POSITIVE CONTROLS PASS", size=11, color=TEXT, bold=True)
    _text(fig, .795, .217, "the audit detects strong signal when it exists", size=9, color=SUBTLE)

    _rect(fig, .05, .055, .95, .125, fill="#10253a", border="#3c7198")
    _text(fig, .50, .090, "THE STORY: most benchmark-retained cells stayed retained even after an independent random-simplex challenge.", size=11, color=GOLD, bold=True)
    return _base_layout(fig, "Was benchmark retention meaningful?", "The grid makes every audited cell visible; the three cards explain what the counts mean.")


def result_figure(stage: int):
    stage = max(0, min(int(stage), 4))
    if stage == 0:
        return _result_discovery_story()
    if stage == 1:
        return _result_cycle_comparison()
    if stage == 2:
        return _result_strict_validation()
    if stage == 3:
        return _result_external_funnel()
    return _result_dirichlet_audit()


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
