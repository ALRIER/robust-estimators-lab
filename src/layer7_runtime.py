"""Presentation-only wiring for the redesigned Layer 7 results journey.

The thesis evidence remains precomputed.  These hooks replace only the visual
presentation of the existing Layer 7 block and its presenter-help window.  The
module can be removed once the main dashboard file is next consolidated.
"""

from __future__ import annotations

import html
import streamlit as st

from src.results_journey import RESULT_STAGES, EXPLAIN_STEPS, result_figure, message_html

_LAYER7 = "07 · Results journey"

_HELP = (
    {
        "look": [
            "Start with the funnel. We tested 36 controlled regimes, 16 looked promising during discovery, and only 2 survived frozen confirmation.",
            "The two cards on the right are CV-019 and CV-010. Both are Lognormal specialists.",
        ],
        "happened": [
            "The GA first searched for useful mixtures.",
            "Then we froze the weights and tested the same recipes again on fresh validation seeds.",
            "CV-019 kept a 16.3% q95 gain and CV-010 kept a 2.2% q95 gain. Both survived 8 of 8 validation seeds.",
        ],
        "means": [
            "Discovery tells us where to look. Confirmation tells us what we can defend.",
            "The important story is not 16 wins. It is that a strict second test reduced them to 2 credible signals.",
        ],
        "avoid": [
            "Do not call all 16 discovery wins confirmed results.",
            "Do not say the GA was better across all 36 regimes.",
        ],
        "numbers": "36 → 16 → 2 · CV-019: +16.3% q95 · CV-010: +2.2% q95 · both 8/8 seeds",
        "formula": "Gain% = 100 × (benchmark risk − candidate risk) / benchmark risk",
        "questions": [
            ("Why did most discovery wins disappear?", "Because confirmation is deliberately harder. The weights cannot adapt to the new data."),
            ("Why do CV-019 and CV-010 matter later?", "They are the only first-cycle candidates strong enough to enter rediscovery as controlled warm starts."),
        ],
    },
    {
        "look": [
            "This is a family map of the 12 winners found after the search space was expanded.",
            "The bar height is simply the number of discovery winners in each distribution family.",
        ],
        "happened": [
            "The GA moved from 10 learnable estimators to 26, and HPF2 exposure increased from 80% to 90%.",
            "The winners were: Normal 1, Lognormal 2, Weibull 2, Inverse Gaussian 4, Ex-Gaussian 0, and Ex-Wald 3.",
            "CV-019 and CV-010 were allowed to start in the population, but they received no automatic advantage.",
        ],
        "means": [
            "A stronger estimator library changed where opportunity appeared.",
            "That is exactly what a regime-conditional search should reveal: the useful mixture depends on the environment and on the components available to combine.",
        ],
        "avoid": [
            "These 12 bars are discovery results, not final confirmations.",
            "A large discovery gain does not automatically mean a transferable specialist.",
        ],
        "numbers": "10 → 26 components · HPF2 80% → 90% · 12 winners · family counts 1/2/2/4/0/3",
        "formula": "Discovery map = number of gate-passing candidates by family",
        "questions": [
            ("Why does Inverse Gaussian have more winners?", "Four Inverse Gaussian candidates passed this discovery cycle. That is an observed search pattern, not a family-wide superiority claim."),
            ("Why is Ex-Gaussian zero?", "No Ex-Gaussian candidate passed this expanded discovery gate. A zero is also an informative result."),
        ],
    },
    {
        "look": [
            "Green bars are locked-unseen validation. Red bars are original-regime validation. Zero is the benchmark line.",
            "The exact same frozen Weibull weights are being judged in both modes.",
        ],
        "happened": [
            "FWVR011 passed locked-unseen with about +2.79% mean gain and +2.72% q95 gain, but failed the original-regime mode strongly.",
            "FWVR012 passed locked-unseen with about +3.18% mean gain and +1.25% q95 gain, and also failed the original-regime mode.",
            "Across 25 candidates, the taxonomy ended with 2 transfer specialists, 10 local cases, 7 near-gate cases, and 6 controls.",
        ],
        "means": [
            "These two estimators are useful, but only inside a narrow validated profile.",
            "A specialist can genuinely transfer to a related unseen regime and still be unsafe as a general estimator for the whole family.",
        ],
        "avoid": [
            "Do not say the GA found a generally better estimator for Weibull data.",
            "Do not hide the red bars. The failures are what define the boundary of the scientific claim.",
        ],
        "numbers": "FWVR011 locked: +2.79% mean / +2.72% q95 · FWVR012 locked: +3.18% / +1.25%",
        "formula": "Dual gate: ΔMSE ≥ 0 AND Δq95 ≥ 0",
        "questions": [
            ("How can locked-unseen pass while original fails?", "Because performance is regime-conditional. The frozen recipe transfers to one related profile without being uniformly good everywhere nearby."),
            ("Why call them transfer specialists?", "They show fixed-weight improvement in related unseen regimes, but the full evidence also shows that the improvement is narrow."),
        ],
    },
    {
        "look": [
            "The funnel shows how the external battery became smaller as data had to be loaded, prepared, evaluated, and judged eligible.",
            "The two cards separate breadth from depth. That distinction is important.",
        ],
        "happened": [
            "We started with 264 requested targets, loaded 228, evaluated 120, and retained 43 eligible parent datasets.",
            "Twenty-six of the 43 parents had at least one corrected specialist win.",
            "Inside those parents, 255 profile-matched comparisons survived FDR control.",
        ],
        "means": [
            "Breadth is 26 of 43 parent datasets. Depth is 255 repeated profile-level confirmations.",
            "This tells us the specialist idea appears in empirical data, but real data still do not reveal the true population mean.",
        ],
        "avoid": [
            "Do not describe 255 confirmations as 255 independent datasets.",
            "Do not call this known-truth validation. It is external calibration.",
        ],
        "numbers": "264 → 228 → 120 → 43 · breadth 26/43 parents · depth 255 confirmations",
        "formula": "Breadth ≠ depth: parent datasets are the independent top-level units",
        "questions": [
            ("Why are only 43 parents eligible?", "A frozen specialist is applied only when the external data match the structural profile rules needed for a fair comparison."),
            ("What is the difference between 26 and 255?", "Twenty-six describes dataset-level breadth. The 255 results describe repeated profile-level depth inside those datasets."),
        ],
    },
    {
        "look": [
            "Each square is one benchmark-retained cell challenged with random valid simplex mixtures.",
            "Grey means no random pass. Blue means some random signal. The separate green card is the positive-control check.",
        ],
        "happened": [
            "Twenty-three of 34 retained cells had no random pass.",
            "Eleven of 34 showed some random signal.",
            "All 8 of the 8 strongest positive controls passed, so the audit could detect signal when it was clearly present.",
        ],
        "means": [
            "In most audited cells, retaining the benchmark was a meaningful outcome, not simply a weak GA search.",
            "The 11 signal cells are useful too: they identify abstentions that deserve more investigation.",
        ],
        "avoid": [
            "Do not say the audit proves a benchmark is unbeatable.",
            "Do not treat random Dirichlet search as a replacement for the GA or for fixed-weight confirmation.",
        ],
        "numbers": "23/34 no random pass · 11/34 some signal · 8/8 positive controls · 4,000 draws × 8 seeds",
        "formula": "Audit question: can arbitrary valid simplex weights pass the same dual gate?",
        "questions": [
            ("Why use random Dirichlet vectors?", "They provide an independent sanity check. If many arbitrary valid mixtures pass, a benchmark-retention decision deserves another look."),
            ("What do the 11 signal cells mean?", "They show possible composite opportunity that the selected GA path did not capture. The audit flags this; it does not automatically overturn the decision."),
        ],
    },
)


def _stage() -> int:
    try:
        return max(0, min(int(st.session_state.get("results_stage", 0)), 4))
    except Exception:
        return 0


def _active_results() -> bool:
    try:
        return st.session_state.get("defense_section") == _LAYER7
    except Exception:
        return False


def _style_block() -> str:
    return '''<style>
    .result-bubble{background:linear-gradient(150deg,#0e2a47,#08182b);border:1px solid #3b7ba8;border-left:5px solid #f3c743;border-radius:14px;padding:1.12rem 1.12rem 1.18rem;min-height:510px;box-shadow:0 0 24px rgba(33,141,202,.09)}
    .result-kicker{font-size:.72rem;font-weight:800;letter-spacing:.12em;color:#72cfff;margin-bottom:.35rem}
    .result-claim{font-size:1.18rem;font-weight:900;line-height:1.18;margin-bottom:.45rem}
    .result-plain{font-size:1rem;line-height:1.34;color:#f5f8ff;border-bottom:1px solid #285b7f;padding-bottom:.82rem;margin-bottom:.82rem;font-weight:700}
    .result-label{font-size:.69rem;font-weight:900;letter-spacing:.09em;color:#f3c743;margin:.78rem 0 .22rem}
    .result-label.warn{color:#ff8c78}.result-copy{font-size:.86rem;line-height:1.36;color:#dce9f8}
    .result-key-strip{border:1px solid #2f6e98;border-radius:9px;background:#0a1d32;padding:.72rem 1rem;color:#dceaff;font-weight:800;text-align:center;margin:.2rem 0 .75rem}
    </style>'''


def _presenter_html(stage: int) -> str:
    stage = max(0, min(int(stage), 4))
    g = _HELP[stage]
    item = RESULT_STAGES[stage]

    def bullets(values):
        return "<ul>" + "".join(f"<li>{html.escape(v)}</li>" for v in values) + "</ul>"

    qs = "".join(
        f'<div class="qa"><div class="q">{html.escape(q)}</div><div class="a">{html.escape(a)}</div></div>'
        for q, a in g["questions"]
    )
    return f'''<style>
    .layer7-help{{max-width:1050px;margin:auto;color:#eef5ff;font-family:Arial,sans-serif}}
    .layer7-help h1{{font-size:2rem;margin:.2rem 0 .4rem;color:#fff}}
    .layer7-help .question{{font-size:1.3rem;color:#72cfff;font-weight:800;margin-bottom:1.1rem}}
    .helpsec{{background:#0b2138;border:1px solid #356e99;border-left:5px solid #f3c743;border-radius:12px;padding:1rem 1.35rem;margin:0 0 1rem}}
    .helpsec h2{{font-size:1.02rem;letter-spacing:.08em;color:#f3c743;margin:.05rem 0 .65rem}}
    .helpsec li{{font-size:1.18rem;line-height:1.45;margin:.4rem 0}}
    .avoid{{border-left-color:#ff7865}}.avoid h2{{color:#ff917f}}
    .numberbox{{background:#102a49;border:1px solid #4fc3ff;border-radius:12px;padding:1rem 1.3rem;margin:1rem 0}}
    .numberbox .big{{font-size:1.42rem;font-weight:900;color:#f7d768;line-height:1.35}}
    .numberbox .formula{{font-size:1.1rem;color:#dce9f8;margin-top:.65rem}}
    .qa{{background:#091a2e;border:1px solid #2f6287;border-radius:10px;padding:.9rem 1.1rem;margin:.75rem 0}}
    .q{{font-size:1.12rem;font-weight:800;color:#72cfff}}.a{{font-size:1.08rem;line-height:1.42;margin-top:.35rem;color:#e4eef8}}
    </style><div class="layer7-help">
      <h1>{html.escape(item['label'])}</h1>
      <div class="question">{html.escape(item['question'])}</div>
      <div class="helpsec"><h2>WHAT AM I LOOKING AT?</h2>{bullets(g['look'])}</div>
      <div class="helpsec"><h2>WHAT HAPPENED?</h2>{bullets(g['happened'])}</div>
      <div class="helpsec"><h2>WHAT DOES IT MEAN?</h2>{bullets(g['means'])}</div>
      <div class="helpsec avoid"><h2>WHAT SHOULD I NOT CLAIM?</h2>{bullets(g['avoid'])}</div>
      <div class="numberbox"><div class="big">{html.escape(g['numbers'])}</div><div class="formula">{html.escape(g['formula'])}</div></div>
      <div class="helpsec"><h2>POSSIBLE QUESTIONS</h2>{qs}</div>
    </div>'''


def install_layer7_runtime_hooks() -> None:
    """Install idempotent presentation hooks on Streamlit's public helpers."""
    if getattr(st, "_layer7_results_hooks", False):
        return
    st._layer7_results_hooks = True

    original_markdown = st.markdown
    original_caption = st.caption
    original_plotly = st.plotly_chart
    original_info = st.info
    original_button = st.button
    original_warning = st.warning

    def markdown(body, *args, **kwargs):
        text = str(body)
        # The sidebar still asks for the legacy generic key.  Rewrite only its
        # presenter link so the private window receives the active result stage.
        if _active_results() and "presenter_notes=1" in text and "section=results" in text:
            text = text.replace("section=results", f"section=results_stage_{_stage()}")
        if _active_results() and "RESULTS JOURNEY — precomputed thesis evidence" in text:
            text = _style_block() + text
        if _active_results() and '<div class="story-panel"><div class="story-kicker">CLAIM STATUS' in text:
            return original_markdown(message_html(_stage()), *args, **kwargs)
        return original_markdown(text, *args, **kwargs)

    def caption(body, *args, **kwargs):
        text = str(body)
        if _active_results() and text == "Discovery finds opportunities; fixed-weight evidence decides what survives.":
            item = RESULT_STAGES[_stage()]
            original_caption("Each view answers one simple question: what happened, what survived, and how far the claim can go.", *args, **kwargs)
            return original_markdown(
                f'<div class="result-key-strip">QUESTION: {html.escape(item["question"])} &nbsp;&nbsp;|&nbsp;&nbsp; KEY EVIDENCE: {html.escape(item["key"])}</div>',
                unsafe_allow_html=True,
            )
        return original_caption(body, *args, **kwargs)

    def plotly_chart(figure_or_data, *args, **kwargs):
        if _active_results():
            title = ""
            try:
                title = str(figure_or_data.layout.title.text or "")
            except Exception:
                pass
            old_titles = (
                "Opportunity → fixed-weight confirmation",
                "Expanded component library",
                "Fixed-weight evidence taxonomy",
                "Real-world external battery",
                "Dirichlet random-simplex abstain audit",
            )
            if any(t in title for t in old_titles):
                return original_plotly(result_figure(_stage()), *args, **kwargs)
        return original_plotly(figure_or_data, *args, **kwargs)

    def info(body, *args, **kwargs):
        text = str(body)
        if _active_results() and text.startswith(("Signal —", "Pressure —", "Interpretation —")):
            step = max(0, min(int(st.session_state.get("results_explanation", 0)), 2))
            return original_info(EXPLAIN_STEPS[_stage()][step], *args, **kwargs)
        return original_info(body, *args, **kwargs)

    def button(label, *args, **kwargs):
        if _active_results() and str(label) == "Advance explanation":
            label = "Explain this result →"
        return original_button(label, *args, **kwargs)

    def warning(body, *args, **kwargs):
        # A stage-specific presenter URL is intentionally not in the legacy
        # PRESENTER_NOTES dictionary.  When that window reaches its fallback,
        # render the simpler stage guide instead of the warning.
        try:
            qp = st.query_params
            section = str(qp.get("section", ""))
            presenter = str(qp.get("presenter_notes", "")) == "1"
        except Exception:
            section, presenter = "", False
        if presenter and section.startswith("results_stage_") and "No hay notas configuradas" in str(body):
            try:
                stage = int(section.rsplit("_", 1)[1])
            except Exception:
                stage = 0
            return original_markdown(_presenter_html(stage), unsafe_allow_html=True)
        return original_warning(body, *args, **kwargs)

    st.markdown = markdown
    st.caption = caption
    st.plotly_chart = plotly_chart
    st.info = info
    st.button = button
    st.warning = warning
