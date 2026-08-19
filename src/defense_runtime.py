"""Single presentation router for the final defense pages.

The historical streamlit_app.py still contains legacy Layer 7-9 blocks. Rather than
stacking multiple monkey patches, this module installs exactly one routing layer that
intercepts the first legacy render call and delegates to the current page modules:

- src.results_page.render_results_journey
- src.conclusions.render_conclusions
- src.technical_appendix.render_technical_appendix

No thesis evidence is recomputed. This module exists only until streamlit_app.py is
fully modularised; it is intentionally the only presentation hook in the repository.
"""

from __future__ import annotations

import html
import streamlit as st
import streamlit.components.v1 as components

from src.results_page import render_results_journey
from src.conclusions import render_conclusions
from src.technical_appendix import render_technical_appendix
from src.final_presenter_notes import FINAL_PRESENTER_NOTES

_LAYER7 = "07 · Results journey"
_LAYER8 = "08 · Conclusions"
_LAYER9 = "09 · Technical drill-down"
_VERSION = "single-defense-runtime-v1"


def _current_note_key(active: str) -> str | None:
    if active == _LAYER7:
        stage = max(0, min(int(st.session_state.get("results_stage", 0)), 4))
        return f"results_stage_{stage}"
    if active == _LAYER8:
        return "conclusions_contrib" if st.session_state.get("conclusion_view", "claims") == "contrib" else "conclusions_claims"
    if active == _LAYER9:
        section = max(0, min(int(st.session_state.get("appendix_section", 0)), 5))
        return f"appendix_{'ABCDEF'[section]}"
    return None


def _note_html(key: str) -> str:
    title, _source, bullets, transition = FINAL_PRESENTER_NOTES[key]
    lis = "".join(f"<li>{html.escape(str(item))}</li>" for item in bullets)
    return f"""
    <style>
      [data-testid="stAppViewContainer"]{{background:#071525!important}}
      .block-container{{max-width:1180px!important;padding:2.6rem 3.2rem!important}}
      .final-note{{font-family:Arial,sans-serif;color:#f4f8ff}}
      .final-note h1{{font-size:2.2rem!important;color:#72cfff!important;margin-bottom:1.7rem!important}}
      .final-note .box{{background:#0b2138;border:1px solid #356e99;border-left:5px solid #f3c743;border-radius:12px;padding:1.2rem 1.45rem;margin-bottom:1.2rem}}
      .final-note h2{{font-size:1rem!important;letter-spacing:.1em;color:#f3c743!important;margin:0 0 .8rem!important}}
      .final-note li{{font-size:1.35rem;line-height:1.48;margin:.7rem 0}}
      .final-note .transition{{font-size:1.15rem;line-height:1.45;color:#c7d8e8}}
    </style>
    <div class="final-note"><h1>{html.escape(title)}</h1>
      <div class="box"><h2>HELP</h2><ul>{lis}</ul></div>
      <div class="box"><h2>TRANSITION</h2><div class="transition">{html.escape(transition)}</div></div>
    </div>
    """


def install_defense_runtime() -> None:
    """Install one and only one audience/presenter router for Layers 7-9."""
    if getattr(st, "_single_defense_runtime_version", None) == _VERSION:
        return
    st._single_defense_runtime_version = _VERSION

    base_markdown = st.markdown
    base_warning = st.warning
    base_html = components.html
    rendering = False

    def markdown(body, *args, **kwargs):
        nonlocal rendering
        if rendering:
            return base_markdown(body, *args, **kwargs)

        active = st.session_state.get("defense_section")
        text = str(body)

        # Keep the presenter window synchronized with the exact visible subview.
        if active in (_LAYER7, _LAYER8, _LAYER9) and "presenter_notes=1" in text:
            key = _current_note_key(active)
            if key:
                text = text.replace("section=results", f"section={key}")
                text = text.replace("section=conclusions", f"section={key}")
                text = text.replace("section=technical", f"section={key}")
            return base_markdown(text, *args, **kwargs)

        # First legacy call of Layer 7: replace the entire page and stop the old block.
        if active == _LAYER7 and "RESULTS JOURNEY — precomputed thesis evidence" in text:
            rendering = True
            try:
                render_results_journey()
            finally:
                rendering = False
            st.stop()

        # First legacy call of Layer 9: replace all repeated historical blocks at once.
        if active == _LAYER9 and (
            "THESIS RESULTS — precomputed research output" in text
            or "THESIS RESULTS — external evidence" in text
        ):
            rendering = True
            try:
                render_technical_appendix()
            finally:
                rendering = False
            st.stop()

        return base_markdown(body, *args, **kwargs)

    def html_component(body, *args, **kwargs):
        nonlocal rendering
        if rendering:
            return base_html(body, *args, **kwargs)
        active = st.session_state.get("defense_section")
        text = str(body)
        # Layer 8 legacy entry point is the old defense_scene_svg(6).
        if active == _LAYER8 and "WHAT DID WE LEARN?" in text and "No Free Lunch, made operational." in text:
            rendering = True
            try:
                render_conclusions()
            finally:
                rendering = False
            st.stop()
        return base_html(body, *args, **kwargs)

    def warning(body, *args, **kwargs):
        try:
            presenter = str(st.query_params.get("presenter_notes", "")) == "1"
            key = str(st.query_params.get("section", ""))
        except Exception:
            presenter, key = False, ""
        if presenter and key in FINAL_PRESENTER_NOTES and "No hay notas configuradas" in str(body):
            return base_markdown(_note_html(key), unsafe_allow_html=True)
        return base_warning(body, *args, **kwargs)

    st.markdown = markdown
    st.warning = warning
    components.html = html_component
