"""Small compatibility hook for the expanded Layer 6 architecture page."""

from __future__ import annotations

import html
import streamlit as st
import streamlit.components.v1 as components

from src.thesis_ga_presenter_notes import THESIS_GA_PRESENTER_NOTES

_LAYER6 = "06 · Experiment pipeline"
_VERSION = "layer6-didactic-scroll-v3-accessible-cues"


def _note_html(key: str) -> str:
    title, _source, bullets, transition = THESIS_GA_PRESENTER_NOTES[key]
    rows = []
    emphasis_anchors = {
        "KEY IDEA", "QUESTION", "STATUS", "FREEZE", "FREEZE AGAIN",
        "4 · GATE", "3 · SEARCH ≠ CLAIM", "REAL-WORLD FUNNEL",
    }
    for item in bullets:
        raw = str(item)
        if "|" in raw:
            anchor, copy = raw.split("|", 1)
        else:
            anchor, copy = "", raw
        emphasis = " cue-emphasis" if anchor in emphasis_anchors or anchor.startswith(("1 ·", "2 ·", "3 ·", "4 ·")) else ""
        rows.append(
            f'<div class="cue-row{emphasis}">'
            f'<div class="cue-anchor">{html.escape(anchor)}</div>'
            f'<div class="cue-copy">{html.escape(copy)}</div>'
            '</div>'
        )

    return f"""
    <style>
      [data-testid="stAppViewContainer"]{{background:#071525!important}}
      .block-container{{max-width:1120px!important;padding:2.1rem 3rem 2.8rem!important}}
      .layer6-note{{font-family:Arial,sans-serif;color:#f6f9ff}}
      .layer6-note h1{{font-size:2.65rem!important;line-height:1.12!important;color:#72cfff!important;margin:0 0 1.7rem!important;font-weight:900!important}}
      .cue-label{{font-size:.95rem;font-weight:900;letter-spacing:.16em;color:#91abc3;margin-bottom:.9rem}}
      .cue-row{{display:grid;grid-template-columns:245px 1fr;gap:28px;align-items:center;background:#0b2138;border:1px solid #32688f;border-left:6px solid #4ea9e8;border-radius:13px;padding:1.1rem 1.35rem;margin:0 0 .9rem}}
      .cue-row.cue-emphasis{{border-left-color:#f3c743;background:#102941}}
      .cue-anchor{{font-size:1.07rem;line-height:1.25;font-weight:900;letter-spacing:.075em;color:#f3c743;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:6px}}
      .cue-copy{{font-size:1.78rem;line-height:1.31;font-weight:750;color:#fff;letter-spacing:.005em}}
      .cue-transition{{margin-top:1.5rem;padding-top:1rem;border-top:1px solid #294f6d;color:#bcd0e2;font-size:1.14rem;line-height:1.4}}
      .cue-transition b{{color:#72cfff;letter-spacing:.08em;font-size:.9rem;margin-right:.55rem}}
      @media(max-width:850px){{
        .block-container{{padding:1.5rem 1.2rem 2rem!important}}
        .layer6-note h1{{font-size:2.2rem!important}}
        .cue-row{{grid-template-columns:1fr;gap:.65rem;padding:1rem 1.1rem}}
        .cue-copy{{font-size:1.5rem}}
      }}
    </style>
    <div class="layer6-note">
      <h1>{html.escape(title)}</h1>
      <div class="cue-label">EMERGENCY CUES · FOLLOW THE CHAIN</div>
      {''.join(rows)}
      <div class="cue-transition"><b>NEXT</b>{html.escape(transition)}</div>
    </div>
    """


def install_layer6_runtime() -> None:
    if getattr(st, "_layer6_runtime_version", None) == _VERSION:
        return
    st._layer6_runtime_version = _VERSION

    base_markdown = st.markdown
    base_html = components.html

    def markdown(body, *args, **kwargs):
        try:
            presenter = str(st.query_params.get("presenter_notes", "")) == "1"
            key = str(st.query_params.get("section", ""))
        except Exception:
            presenter, key = False, ""
        if presenter and key == "pipeline_architecture" and "presenter-heading" in str(body):
            base_markdown(_note_html(key), unsafe_allow_html=True)
            st.stop()
        return base_markdown(body, *args, **kwargs)

    def html_component(body, *args, **kwargs):
        active = st.session_state.get("defense_section")
        architecture = st.session_state.get("layer6_view", "architecture") == "architecture"
        if active == _LAYER6 and architecture and "THESIS GA ARCHITECTURE" in str(body):
            kwargs["height"] = 4450
            kwargs["scrolling"] = False
        return base_html(body, *args, **kwargs)

    st.markdown = markdown
    components.html = html_component
