"""Force the polished narrative Layer 7 presentation over the legacy Streamlit block.

This is intentionally presentation-only. It never recomputes thesis evidence.
The legacy Layer 7 code remains in streamlit_app.py for now, but every central
result chart and explanatory rail is replaced at render time.
"""

from __future__ import annotations

import html
import streamlit as st

from src.results_journey import RESULT_STAGES, EXPLAIN_STEPS, message_html
from src.results_journey_polished import result_figure

_LAYER7 = "07 · Results journey"
_VERSION = "layer7-force-v5-polished"


def _stage() -> int:
    try:
        return max(0, min(int(st.session_state.get("results_stage", 0)), 4))
    except Exception:
        return 0


def _active() -> bool:
    try:
        return st.session_state.get("defense_section") == _LAYER7
    except Exception:
        return False


def install_force_layer7_renderer() -> None:
    """Install a versioned, idempotent override for Layer 7 presentation."""
    if getattr(st, "_layer7_force_renderer_version", None) == _VERSION:
        return
    st._layer7_force_renderer_version = _VERSION

    base_plotly = st.plotly_chart
    base_markdown = st.markdown
    base_caption = st.caption
    base_info = st.info
    base_button = st.button

    def plotly_chart(figure_or_data, *args, **kwargs):
        if _active():
            kwargs.pop("key", None)
            return base_plotly(result_figure(_stage()), *args, **kwargs)
        return base_plotly(figure_or_data, *args, **kwargs)

    def markdown(body, *args, **kwargs):
        text = str(body)
        if _active() and "presenter_notes=1" in text and "section=results" in text:
            text = text.replace("section=results", f"section=results_stage_{_stage()}")
        if _active() and '<div class="story-panel"><div class="story-kicker">CLAIM STATUS' in text:
            return base_markdown(message_html(_stage()), *args, **kwargs)
        return base_markdown(text, *args, **kwargs)

    def caption(body, *args, **kwargs):
        text = str(body)
        if _active() and text == "Discovery finds opportunities; fixed-weight evidence decides what survives.":
            item = RESULT_STAGES[_stage()]
            base_caption(
                "Each screen tells one result story: what entered, what disappeared, what survived, and how far the claim can go.",
                *args,
                **kwargs,
            )
            return base_markdown(
                "<div style='border:1px solid #2f6e98;border-radius:9px;background:#0a1d32;"
                "padding:.85rem 1.1rem;color:#dceaff;font-size:1.02rem;font-weight:800;text-align:center;margin:.2rem 0 .75rem'>"
                f"QUESTION: {html.escape(item['question'])} &nbsp;&nbsp;|&nbsp;&nbsp; "
                f"KEY EVIDENCE: {html.escape(item['key'])}</div>",
                unsafe_allow_html=True,
            )
        return base_caption(body, *args, **kwargs)

    def info(body, *args, **kwargs):
        text = str(body)
        if _active() and text.startswith(("Signal —", "Pressure —", "Interpretation —")):
            step = max(0, min(int(st.session_state.get("results_explanation", 0)), 2))
            return base_info(EXPLAIN_STEPS[_stage()][step], *args, **kwargs)
        return base_info(body, *args, **kwargs)

    def button(label, *args, **kwargs):
        if _active() and str(label) == "Advance explanation":
            label = "Explain this result →"
        return base_button(label, *args, **kwargs)

    st.plotly_chart = plotly_chart
    st.markdown = markdown
    st.caption = caption
    st.info = info
    st.button = button
