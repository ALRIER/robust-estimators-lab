"""Single presentation router for the modular defense pages.

The historical ``streamlit_app.py`` is still monolithic, so this is the one and only
compatibility router. It keeps Layers 1–2, Layer 4, and Layers 7–9 synchronized with
their current modular pages and presenter notes. Target modules are reloaded from
disk so Streamlit hot-reload cannot serve an old page implementation after a Git
push.

No thesis evidence is recomputed here.
"""

from __future__ import annotations

import html
import importlib
import streamlit as st
import streamlit.components.v1 as components

_LAYER1 = "01 · Research logic"
_LAYER2 = "02 · Data-generating world"
_LAYER4 = "04 · Monte Carlo engine"
_LAYER7 = "07 · Results journey"
_LAYER8 = "08 · Conclusions"
_LAYER9 = "09 · Technical drill-down"
_VERSION = "single-defense-runtime-v5-layer4-validation"


def _load_notes():
    final_module = importlib.import_module("src.final_presenter_notes")
    final_module = importlib.reload(final_module)
    research_module = importlib.import_module("src.research_presenter_notes")
    research_module = importlib.reload(research_module)
    monte_module = importlib.import_module("src.monte_carlo_presenter_notes")
    monte_module = importlib.reload(monte_module)
    notes = dict(final_module.FINAL_PRESENTER_NOTES)
    notes.update(research_module.RESEARCH_PRESENTER_NOTES)
    notes.update(monte_module.MONTE_CARLO_PRESENTER_NOTES)
    return notes


def _load_module(module_name: str):
    module = importlib.import_module(module_name)
    return importlib.reload(module)


def _render_current(module_name: str, function_name: str) -> None:
    module = _load_module(module_name)
    getattr(module, function_name)()


def _current_note_key(active: str) -> str | None:
    if active == _LAYER1:
        panel = max(0, min(int(st.session_state.get("research_panel", 0)), 4))
        return (
            "research_problem",
            "research_objective",
            "research_hypotheses",
            "research_target",
            "research_why_win",
        )[panel]
    if active == _LAYER2:
        view = max(0, min(int(st.session_state.get("data_world_view", 0)), 2))
        return ("data_world_why_simulation", "data_world_regime", "data_world_validity")[view]
    if active == _LAYER4:
        view = max(0, min(int(st.session_state.get("monte_carlo_didactic_view", 0)), 3))
        return (
            "monte_carlo_measurement",
            "monte_carlo_why_validate",
            "monte_carlo_validation_stages",
            "monte_carlo_fairness",
        )[view]
    if active == _LAYER7:
        stage = max(0, min(int(st.session_state.get("results_stage", 0)), 4))
        return f"results_stage_{stage}"
    if active == _LAYER8:
        return "conclusions_contrib" if st.session_state.get("conclusion_view", "claims") == "contrib" else "conclusions_claims"
    if active == _LAYER9:
        section = max(0, min(int(st.session_state.get("appendix_section", 0)), 3))
        return f"appendix_{'ABCD'[section]}"
    return None


def _note_html(key: str) -> str:
    notes = _load_notes()
    title, _source, bullets, transition = notes[key]
    lis = "".join(f"<li>{html.escape(str(item))}</li>" for item in bullets)
    return f"""
    <style>
      [data-testid="stAppViewContainer"]{{background:#071525!important}}
      .block-container{{max-width:1180px!important;padding:2.6rem 3.2rem!important}}
      .final-note{{font-family:Arial,sans-serif;color:#f4f8ff}}
      .final-note h1{{font-size:2.3rem!important;color:#72cfff!important;margin-bottom:1.7rem!important}}
      .final-note .box{{background:#0b2138;border:1px solid #356e99;border-left:5px solid #f3c743;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.25rem}}
      .final-note h2{{font-size:1rem!important;letter-spacing:.1em;color:#f3c743!important;margin:0 0 .85rem!important}}
      .final-note li{{font-size:1.38rem;line-height:1.5;margin:.72rem 0}}
      .final-note .transition{{font-size:1.18rem;line-height:1.48;color:#c7d8e8}}
    </style>
    <div class="final-note"><h1>{html.escape(title)}</h1>
      <div class="box"><h2>HELP</h2><ul>{lis}</ul></div>
      <div class="box"><h2>TRANSITION</h2><div class="transition">{html.escape(transition)}</div></div>
    </div>
    """


def install_defense_runtime() -> None:
    """Install the single audience/presenter router for the modular defense pages."""
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

        # In the separate presenter window, replace historical monolithic cue
        # cards with the current simplified notes before they are displayed.
        try:
            presenter = str(st.query_params.get("presenter_notes", "")) == "1"
            presenter_key = str(st.query_params.get("section", ""))
        except Exception:
            presenter, presenter_key = False, ""
        direct_note_keys = {
            "research_problem", "research_objective", "research_hypotheses",
            "research_target", "research_why_win",
            "monte_carlo_measurement", "monte_carlo_why_validate",
            "monte_carlo_validation_stages", "monte_carlo_fairness",
        }
        if presenter and presenter_key in direct_note_keys and "presenter-heading" in text:
            return base_markdown(_note_html(presenter_key), unsafe_allow_html=True)

        # Keep the presenter window synchronized with the exact visible subview.
        if active in (_LAYER1, _LAYER2, _LAYER4, _LAYER7, _LAYER8, _LAYER9) and "presenter_notes=1" in text:
            key = _current_note_key(active)
            if key:
                old_keys = (
                    "data_world", "data_world_families", "data_world_certification",
                    "monte_carlo_engine", "monte_carlo_validation_0",
                    "monte_carlo_validation_1", "monte_carlo_validation_2",
                    "monte_carlo_validation_3", "results", "conclusions", "technical",
                )
                for old in old_keys:
                    text = text.replace(f"section={old}", f"section={key}")
            return base_markdown(text, *args, **kwargs)

        # First legacy call of Layer 4: replace the old engine/validation tabs
        # with the current didactic measurement-and-trust page.
        if active == _LAYER4 and "monte-carlo-tabs" in text:
            rendering = True
            try:
                _render_current("src.monte_carlo_layer", "render_monte_carlo_layer")
            finally:
                rendering = False
            st.stop()

        # First legacy call of Layer 7: replace the old page and stop the old block.
        if active == _LAYER7 and "RESULTS JOURNEY — precomputed thesis evidence" in text:
            rendering = True
            try:
                _render_current("src.results_page", "render_results_journey")
            finally:
                rendering = False
            st.stop()

        # First legacy call of Layer 9: replace all historical technical blocks at once.
        if active == _LAYER9 and (
            "THESIS RESULTS — precomputed research output" in text
            or "THESIS RESULTS — external evidence" in text
        ):
            rendering = True
            try:
                _render_current("src.technical_appendix", "render_technical_appendix")
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

        # Layer 1: replace the historical SVG with the current question-led view.
        if active == _LAYER1:
            module = _load_module("src.research_logic")
            panel = max(0, min(int(st.session_state.get("research_panel", 0)), 4))
            heights = (1550, 1850, 1450, 1700, 1650)
            current_html = module.research_logic_svg(panel)
            kwargs["height"] = heights[panel]
            kwargs["scrolling"] = False
            return base_html(current_html, *args, **kwargs)

        # Layer 2: always replace the historical view with the current didactic view.
        if active == _LAYER2:
            module = _load_module("src.data_world")
            view = max(0, min(int(st.session_state.get("data_world_view", 0)), 2))
            heights = (1780, 2150, 1900)
            current_html = module.data_world_detail_svg(view)
            kwargs["height"] = heights[view]
            kwargs["scrolling"] = False
            return base_html(current_html, *args, **kwargs)

        # Layer 8 legacy entry point is the old defense_scene_svg(6).
        if active == _LAYER8 and "WHAT DID WE LEARN?" in text and "No Free Lunch, made operational." in text:
            rendering = True
            try:
                _render_current("src.conclusions", "render_conclusions")
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
        notes = _load_notes() if presenter else {}
        if presenter and key in notes and "No hay notas configuradas" in str(body):
            return base_markdown(_note_html(key), unsafe_allow_html=True)
        return base_warning(body, *args, **kwargs)

    st.markdown = markdown
    st.warning = warning
    components.html = html_component
