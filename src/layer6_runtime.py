"""Small compatibility hook for the expanded Layer 6 architecture page."""

from __future__ import annotations

import html
import streamlit as st
import streamlit.components.v1 as components

from src.thesis_ga_presenter_notes import THESIS_GA_PRESENTER_NOTES

_LAYER6 = "06 · Experiment pipeline"
_VERSION = "layer6-didactic-scroll-v1"


def _note_html(key: str) -> str:
    title, _source, bullets, transition = THESIS_GA_PRESENTER_NOTES[key]
    lis = "".join(f"<li>{html.escape(str(item))}</li>" for item in bullets)
    return f"""
    <style>
      [data-testid="stAppViewContainer"]{{background:#071525!important}}
      .block-container{{max-width:1180px!important;padding:2.6rem 3.2rem!important}}
      .layer6-note{{font-family:Arial,sans-serif;color:#f4f8ff}}
      .layer6-note h1{{font-size:2.3rem!important;color:#72cfff!important;margin-bottom:1.7rem!important}}
      .layer6-note .box{{background:#0b2138;border:1px solid #356e99;border-left:5px solid #f3c743;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.25rem}}
      .layer6-note h2{{font-size:1rem!important;letter-spacing:.1em;color:#f3c743!important;margin:0 0 .85rem!important}}
      .layer6-note li{{font-size:1.34rem;line-height:1.5;margin:.68rem 0}}
      .layer6-note .transition{{font-size:1.18rem;line-height:1.48;color:#c7d8e8}}
    </style>
    <div class="layer6-note"><h1>{html.escape(title)}</h1>
      <div class="box"><h2>HELP</h2><ul>{lis}</ul></div>
      <div class="box"><h2>TRANSITION</h2><div class="transition">{html.escape(transition)}</div></div>
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
            return base_markdown(_note_html(key), unsafe_allow_html=True)
        return base_markdown(body, *args, **kwargs)

    def html_component(body, *args, **kwargs):
        active = st.session_state.get("defense_section")
        architecture = st.session_state.get("layer6_view", "architecture") == "architecture"
        if active == _LAYER6 and architecture and "THESIS GA ARCHITECTURE" in str(body):
            kwargs["height"] = 4300
            kwargs["scrolling"] = False
        return base_html(body, *args, **kwargs)

    st.markdown = markdown
    components.html = html_component
