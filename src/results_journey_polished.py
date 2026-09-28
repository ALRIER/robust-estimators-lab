"""Polished narrative renderer for Layer 7.

Presentation-only. All values are fixed thesis outputs already exported with the app.
"""

import plotly.graph_objects as go


BG = "#081525"
PANEL = "#0d2842"
BLUE = "#58aee8"
CYAN = "#72cfff"
GOLD = "#f3c743"
GREEN = "#54c786"
RED = "#e66d4f"
PURPLE = "#a777e3"
MUTED = "#526a85"
TEXT = "#e9f4ff"
SUBTLE = "#b9c8d9"
DARK_TEXT = "#081525"


def _base_layout(fig, title, subtitle="", height=660):
    fig.update_layout(
        title={
            "text": f"<b>{title}</b><br><span style='font-size:15px;color:{SUBTLE}'>{subtitle}</span>",
            "x": 0.02,
            "xanchor": "left",
        },
        height=height,
        margin=dict(l=28, r=28, t=96, b=34),
        plot_bgcolor=BG,
        paper_bgcolor=BG,
        font=dict(color=TEXT, size=15),
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


def _text(fig, x, y, text, size=14, color=TEXT, anchor="center", align="center", bold=False):
    if bold:
        text = f"<b>{text}</b>"
    fig.add_annotation(
        x=x, y=y, xref="x", yref="y", showarrow=False, text=text,
        xanchor=anchor, align=align, font=dict(size=size, color=color),
    )


def _arrow(fig, x0, y0, x1, y1, color=CYAN, width=2):
    fig.add_annotation(
        x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
        text="", showarrow=True, arrowhead=2, arrowsize=1.1,
        arrowwidth=width, arrowcolor=color,
    )


def _stat_card(
    fig, x0, y0, x1, y1, label, value, *,
    fill=PANEL, border="#326188", value_color=GOLD, label_color=CYAN,
    value_size=22, label_size=11
):
    _rect(fig, x0, y0, x1, y1, fill=fill, border=border, width=1.4)
    h = y1 - y0
    _text(fig, (x0+x1)/2, y0 + h*0.70, value, size=value_size, color=value_color, bold=True)
    _text(fig, (x0+x1)/2, y0 + h*0.28, label, size=label_size, color=label_color, bold=True)


def _two_line_card(
    fig, x0, y0, x1, y1, heading, value, subtext="",
    *, fill=PANEL, border="#326188", value_color=GOLD, heading_color=CYAN
):
    _rect(fig, x0, y0, x1, y1, fill=fill, border=border, width=1.5)
    h = y1-y0
    _text(fig, (x0+x1)/2, y0+h*0.80, heading, size=11, color=heading_color, bold=True)
    _text(fig, (x0+x1)/2, y0+h*0.50, value, size=27, color=value_color, bold=True)
    if subtext:
        _text(fig, (x0+x1)/2, y0+h*0.18, subtext, size=10, color=SUBTLE)


def _funnel_band(fig, y0, y1, left0, right0, left1, right1, fill, number, title, detail="", dark_text=False):
    fig.add_trace(go.Scatter(
        x=[left0, right0, right1, left1, left0],
        y=[y1, y1, y0, y0, y1],
        mode="lines", fill="toself",
        line=dict(color=fill, width=1.5), fillcolor=fill,
        hoverinfo="skip", showlegend=False,
    ))
    cx = (left0 + right0 + left1 + right1) / 4
    fg = DARK_TEXT if dark_text else "#ffffff"
    h = y1-y0
    _text(fig, cx, y0+h*0.68, str(number), size=30, color=fg, bold=True)
    _text(fig, cx, y0+h*0.38, title, size=14, color=fg, bold=True)
    if detail:
        detail_color = "#233142" if dark_text else "#edf5ff"
        _text(fig, cx, y0+h*0.13, detail, size=10, color=detail_color)


def _story_strip(fig, text):
    _rect(fig, .05, .025, .95, .105, fill="#10253a", border="#3c7198")
    _text(fig, .50, .065, text, size=13, color=GOLD, bold=True)


def _result_discovery_story():
    fig = go.Figure()
    _funnel_band(
        fig, .69, .89, .04, .57, .10, .51, MUTED, 36,
        "CONTROLLED REGIMES", "The first discovery programme starts broad"
    )
    _text(fig, .305, .635, "↓  Benchmark gate keeps only candidates that beat admissible comparators",
          size=12, color=GOLD, bold=True)
    _funnel_band(
        fig, .43, .60, .12, .49, .18, .43, GOLD, 16,
        "DISCOVERY WINS", "Promising during search — not yet confirmed", dark_text=True
    )
    _text(fig, .305, .365, "↓  Freeze the weights · new seeds · no retraining",
          size=12, color=CYAN, bold=True)
    _funnel_band(
        fig, .17, .32, .21, .40, .245, .365, GREEN, 2,
        "CONFIRMED SIGNALS", "Only fixed-weight evidence survives"
    )

    _text(fig, .78, .895, "WHO SURVIVED?", size=13, color=CYAN, bold=True)
    _two_line_card(
        fig, .60, .54, .96, .83, "CV-019 · LOGNORMAL", "+16.3% q95",
        "8 / 8 validation seeds", fill="#0d302d", border=GREEN,
        value_color=GREEN, heading_color="#dfffea"
    )
    _two_line_card(
        fig, .60, .17, .96, .46, "CV-010 · LOGNORMAL", "+2.2% q95",
        "8 / 8 validation seeds", fill="#0d302d", border=GREEN,
        value_color=GREEN, heading_color="#dfffea"
    )
    _story_strip(fig, "THE STORY: discovery found 16 possibilities; frozen confirmation left only 2 claims we can defend.")
    return _base_layout(
        fig,
        "What survived the first search?",
        "The funnel explains why candidates disappear instead of treating every discovery win as a result.",
        height=680,
    )


def _result_cycle_comparison():
    fig = go.Figure()

    _rect(fig, .025, .13, .475, .92, fill="#0c243d", border="#507294", width=1.6)
    _text(fig, .25, .875, "CYCLE 1 · ORIGINAL DISCOVERY", size=15, color="#d7e4f2", bold=True)
    _stat_card(fig, .065, .745, .225, .845, "LEARNABLE", "10", border="#507294",
               value_color=GOLD, label_color=CYAN)
    _stat_card(fig, .275, .745, .435, .845, "HPF2", "80%", border="#507294",
               value_color=GOLD, label_color=CYAN)

    _text(fig, .25, .675, "36 regimes", size=22, color=TEXT, bold=True)
    _arrow(fig, .25, .642, .25, .585, color="#7693ad")
    _text(fig, .25, .545, "16 discovery wins", size=22, color=GOLD, bold=True)
    _text(fig, .25, .498, "search signals", size=11, color=SUBTLE)
    _arrow(fig, .25, .462, .25, .405, color=CYAN)
    _text(fig, .25, .365, "2 confirmed", size=24, color=GREEN, bold=True)
    _text(fig, .25, .318, "both LOGNORMAL", size=12, color="#dfffea", bold=True)

    _stat_card(fig, .070, .205, .235, .290, "CV-019", "+16.3% q95",
               fill="#0d302d", border=GREEN, value_color=GREEN, label_color="#dfffea",
               value_size=18, label_size=10)
    _stat_card(fig, .265, .205, .430, .290, "CV-010", "+2.2% q95",
               fill="#0d302d", border=GREEN, value_color=GREEN, label_color="#dfffea",
               value_size=18, label_size=10)
    _text(fig, .25, .163, "These two enter Cycle 2 only as warm starts.", size=10, color=SUBTLE)

    _arrow(fig, .478, .52, .525, .52, color=PURPLE, width=3)
    _text(fig, .501, .585, "STRONGER BASIS", size=11, color=PURPLE, bold=True)
    _text(fig, .501, .455, "search reopens", size=10, color=SUBTLE)

    _rect(fig, .525, .13, .975, .92, fill="#181d3d", border=PURPLE, width=1.7)
    _text(fig, .75, .875, "CYCLE 2 · EXPANDED REDISCOVERY", size=15, color="#eadcff", bold=True)
    _stat_card(fig, .565, .745, .725, .845, "LEARNABLE", "26", fill="#201f4a",
               border=PURPLE, value_color="#d6b4ff", label_color="#d9c4f4")
    _stat_card(fig, .775, .745, .935, .845, "HPF2", "90%", fill="#201f4a",
               border=PURPLE, value_color="#d6b4ff", label_color="#d9c4f4")

    _text(fig, .75, .675, "12 discovery winners", size=25, color="#d6b4ff", bold=True)
    _text(fig, .75, .630, "Five families · Ex-Gaussian = 0", size=12, color=SUBTLE)

    # Keep the live slide readable: family, count, and q95 range only.
    # Full IDs, mean-MSE gains, and regime conditions live in Presenter Help.
    family_cards = [
        ("NORMAL", "1 winner", "+7.0% q95", .555, .465, MUTED),
        ("LOGNORMAL", "2 winners", "+3.8–3.9% q95", .755, .465, PURPLE),
        ("WEIBULL", "2 winners", "+7.3–23.6% q95", .555, .315, GREEN),
        ("INV. GAUSS.", "4 winners", "+5.3–38.2% q95", .755, .315, GOLD),
        ("EX-WALD", "3 winners", "+10.4–20.6% q95", .555, .165, BLUE),
    ]
    for label, count, gain, x, y, color in family_cards:
        _rect(fig, x, y, x+.180, y+.115, fill="#101d31", border=color, width=1.6)
        _text(fig, x+.090, y+.086, label, size=11.5, color=color, bold=True)
        _text(fig, x+.090, y+.053, count, size=14, color=TEXT, bold=True)
        _text(fig, x+.090, y+.020, gain, size=11.5, color=SUBTLE, bold=True)

    _rect(fig, .755, .165, .935, .280, fill="#241f3f", border=PURPLE, width=1.6)
    _text(fig, .845, .245, "WARM STARTS", size=11.5, color="#eadcff", bold=True)
    _text(fig, .845, .210, "CV-019 · CV-010", size=13.5, color=TEXT, bold=True)
    _text(fig, .845, .180, "compete again · no bonus", size=9.5, color=SUBTLE)

    _text(fig, .75, .125, "Largest Cycle II cluster: Inverse Gaussian · strongest q95 discovery gain: +38.2%",
          size=10.5, color=GOLD, bold=True)

    _story_strip(fig, "THE STORY: when the component library became stronger, the winner pattern changed — exactly what regime-conditional search predicts.")
    return _base_layout(
        fig,
        "What changed when the search space became stronger?",
        "Cycle 1 and Cycle 2 are shown as two different evidence stories, not as one unexplained bar chart.",
        height=720,
    )


def _specialist_card(fig, x0, x1, title, locked_mean, locked_q95, original_mean, original_q95):
    _rect(fig, x0, .235, x1, .91, fill="#0c2238", border="#416f92", width=1.5)
    cx = (x0+x1)/2
    _text(fig, cx, .865, title, size=16, color=TEXT, bold=True)
    _text(fig, cx, .823, "WEIBULL · same frozen weights", size=10, color=SUBTLE)

    _rect(fig, x0+.025, .585, x1-.025, .785, fill="#0d302d", border=GREEN, width=1.7)
    _text(fig, cx, .747, "LOCKED-UNSEEN · PASS", size=12, color="#dfffea", bold=True)
    _text(fig, x0+.12, .665, f"+{locked_mean:.2f}%", size=23, color=GREEN, bold=True)
    _text(fig, x0+.12, .617, "mean MSE", size=10, color=SUBTLE)
    _text(fig, x1-.12, .665, f"+{locked_q95:.2f}%", size=23, color=GREEN, bold=True)
    _text(fig, x1-.12, .617, "q95 MSE", size=10, color=SUBTLE)

    _text(fig, cx, .535, "same frozen candidate ↓ tested in another mode", size=10, color=CYAN, bold=True)

    _rect(fig, x0+.025, .315, x1-.025, .505, fill="#321b20", border=RED, width=1.7)
    _text(fig, cx, .468, "ORIGINAL-REGIME MODE · FAIL", size=12, color="#ffd9d2", bold=True)
    _text(fig, x0+.12, .392, f"{original_mean:.2f}%", size=22, color=RED, bold=True)
    _text(fig, x0+.12, .345, "mean MSE", size=10, color=SUBTLE)
    _text(fig, x1-.12, .392, f"{original_q95:.2f}%", size=22, color=RED, bold=True)
    _text(fig, x1-.12, .345, "q95 MSE", size=10, color=SUBTLE)

    _text(fig, cx, .270, "NARROW TRANSFER SPECIALIST — not a family-wide winner", size=10, color=GOLD, bold=True)


def _result_strict_validation():
    fig = go.Figure()
    _specialist_card(fig, .03, .48, "FWVR011", 2.785, 2.719, -15.774, -45.062)
    _specialist_card(fig, .52, .97, "FWVR012", 3.175, 1.248, -15.196, -34.563)

    _text(fig, .50, .185, "25-CANDIDATE EVIDENCE TAXONOMY", size=12, color=CYAN, bold=True)
    taxonomy = [
        (.05, .255, "2", "TRANSFER", "#0d302d", GREEN),
        (.285, .49, "10", "LOCAL", "#15283d", BLUE),
        (.52, .725, "7", "NEAR-GATE", "#2f2b18", GOLD),
        (.755, .96, "6", "CONTROLS", "#2b1c22", RED),
    ]
    for x0, x1, value, label, fill, color in taxonomy:
        _stat_card(fig, x0, .045, x1, .145, label, value, fill=fill, border=color,
                   value_color=color, label_color=TEXT, value_size=22, label_size=10)

    return _base_layout(
        fig,
        "Did the new candidates really transfer?",
        "Each card shows the same frozen specialist under two validation modes — the contrast defines the boundary of the claim.",
        height=710,
    )


def _result_external_funnel():
    """One-screen synthesis of the external battery and abstention audit.

    Left = what the evidence produced. Right = what the protocol did.
    Every result is paired to the step that creates its meaning.
    """
    fig = go.Figure()

    _text(fig, .235, .945, "RESULTS · WHAT WE FOUND", size=14, color=GOLD, bold=True)
    _text(fig, .765, .945, "METHODOLOGY · WHAT WE DID", size=14, color=CYAN, bold=True)
    _text(fig, .50, .905, "Each result is tied to the methodological step that produced it.",
          size=11, color=SUBTLE, bold=True)

    rows = [
        (
            "264 REQUESTED PUBLIC TARGETS",
            "Starting universe for external testing",
            "1 · BUILD THE EXTERNAL BATTERY",
            "Assemble 264 public dataset targets so frozen specialists can be tested outside simulation.",
            MUTED,
        ),
        (
            "228 LOADED SOURCES",
            "Successfully retrieved and auditable",
            "2 · LOAD + DOCUMENT SOURCES",
            "Check availability and readability; record URL, access time, file hash, variables, transforms and diagnostics.",
            "#607995",
        ),
        (
            "120 EVALUATED DATASET IDs",
            "Datasets that actually entered external evaluation",
            "3 · EVALUATE USABLE DATASETS",
            "Only loaded dataset IDs that pass preparation and selection enter the compact evaluation output.",
            BLUE,
        ),
        (
            "43 ELIGIBLE PARENT DATASETS",
            "True denominator for the primary external claim",
            "4 · APPLY THE PROFILE GATE",
            "Keep only in-regime, profile-matched comparisons using the pre-registered empirical profile and benchmark policy.",
            GREEN,
        ),
        (
            "26 / 43 PARENTS WITH CORRECTED SIGNAL",
            "Breadth: positive evidence across many parent sources",
            "5 · CONTROL MULTIPLICITY",
            "Compute specialist-vs-benchmark gains and paired bootstrap evidence, then apply dataset-level BH-FDR to the primary claim.",
            BLUE,
        ),
        (
            "255 CORRECTED CONFIRMATIONS",
            "Depth inside those parents · not 255 independent datasets",
            "6 · MEASURE DEPTH",
            "Count surviving profile-matched evidence rows within eligible parents without treating repeated rows as independent sources.",
            PURPLE,
        ),
        (
            "AUDIT · 23 / 34 NO RANDOM PASS",
            "11 / 34 show signal · positive-control sanity check passes all 8 seeds",
            "7 · AUDIT THE ABSTENTIONS",
            "Challenge benchmark-retained synthetic cases with 4,000 random Dirichlet simplex mixtures across 8 audit seeds.",
            GOLD,
        ),
    ]

    centers = [.825, .715, .605, .495, .385, .275, .165]
    for (result_title, result_note, method_title, method_note, color), y in zip(rows, centers):
        # Left: result.
        _rect(fig, .025, y-.043, .425, y+.043, fill="#0c2238", border=color, width=1.55)
        _text(fig, .045, y+.015, result_title, size=13, color=color,
              anchor="left", align="left", bold=True)
        _text(fig, .045, y-.020, result_note, size=9.6, color=SUBTLE,
              anchor="left", align="left")

        # Right: methodology.
        _rect(fig, .575, y-.043, .975, y+.043, fill="#10253a", border="#3c7198", width=1.35)
        _text(fig, .595, y+.017, method_title, size=11.2, color=CYAN,
              anchor="left", align="left", bold=True)
        _text(fig, .595, y-.020, method_note, size=9.2, color=TEXT,
              anchor="left", align="left")

        # Method -> result: the arrow makes the causal/narrative pairing explicit.
        _arrow(fig, .565, y, .440, y, color=color, width=2.2)

    _rect(fig, .06, .025, .94, .090, fill="#10253a", border=GOLD, width=1.6)
    _text(
        fig, .50, .058,
        "TAKE-HOME · conditional real-world transfer has breadth (26/43 parents) and depth (255 corrected confirmations); "
        "the abstention audit shows benchmark retention was often meaningful, but not beyond challenge in every case.",
        size=10.5, color=TEXT, bold=True,
    )

    return _base_layout(
        fig,
        "External evidence + abstention audit",
        "A single story: how public data were filtered into a defensible external claim, then how benchmark retention was independently challenged.",
        height=920,
    )


def _result_dirichlet_audit():
    fig = go.Figure()

    _rect(fig, .04, .82, .59, .94, fill="#10253a", border=CYAN)
    _text(fig, .315, .900, "AUDIT QUESTION", size=11, color=CYAN, bold=True)
    _text(fig, .315, .855, "Could arbitrary valid simplex mixtures beat benchmark-retained cells?",
          size=12, color=TEXT, bold=True)
    _arrow(fig, .315, .81, .315, .75, color=CYAN)

    x0, y0 = .06, .35
    dx, dy = .052, .095
    for i in range(34):
        col = i % 9
        row = i // 9
        xx = x0 + col * dx
        yy = y0 + (3-row) * dy
        fill = MUTED if i < 23 else BLUE
        border = "#8093aa" if i < 23 else CYAN
        _rect(fig, xx, yy, xx+.038, yy+.060, fill=fill, border=border, width=1.0)

    _text(fig, .315, .315, "34 benchmark-retained cells", size=11, color=TEXT, bold=True)
    _text(fig, .315, .278, "each square = one independent audit target", size=10, color=SUBTLE)

    _stat_card(fig, .07, .135, .29, .245, "NO PASS", "23", fill="#17263a",
               border=MUTED, value_color="#c5d0de", label_color="#c5d0de",
               value_size=22, label_size=10)
    _stat_card(fig, .34, .135, .56, .245, "SOME SIGNAL", "11", fill="#102c3f",
               border=BLUE, value_color=BLUE, label_color=BLUE,
               value_size=22, label_size=10)

    _text(fig, .795, .895, "HOW TO READ THE AUDIT", size=12, color=CYAN, bold=True)
    _two_line_card(
        fig, .64, .64, .95, .81, "NO RANDOM PASS", "23 / 34",
        "benchmark retention resisted the challenge",
        fill="#17263a", border=MUTED, value_color="#c5d0de", heading_color=TEXT
    )
    _two_line_card(
        fig, .64, .42, .95, .59, "SOME RANDOM SIGNAL", "11 / 34",
        "these abstentions deserve another look",
        fill="#102c3f", border=BLUE, value_color=BLUE, heading_color=TEXT
    )
    _two_line_card(
        fig, .64, .20, .95, .37, "POSITIVE CONTROLS PASS", "8 / 8",
        "the audit detects strong signal when it exists",
        fill="#0d302d", border=GREEN, value_color=GREEN, heading_color=TEXT
    )

    _story_strip(fig, "THE STORY: most benchmark-retained cells stayed retained even after an independent random-simplex challenge.")
    return _base_layout(
        fig,
        "Was benchmark retention meaningful?",
        "The grid makes every audited cell visible; the three cards explain what the counts mean.",
        height=690,
    )


def result_figure(stage: int):
    stage = max(0, min(int(stage), 4))
    if stage == 0:
        return _result_discovery_story()
    if stage == 1:
        return _result_cycle_comparison()
    if stage == 2:
        return _result_strict_validation()
    if stage in (3, 4):
        return _result_external_funnel()
    return _result_external_funnel()
