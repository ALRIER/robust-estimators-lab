"""Authoritative Layer 8/9 presentation override.

The main app still contains legacy Layer 8/9 blocks. This hook intercepts the exact
legacy render entry points and replaces them with the final defense pages. It is
presentation-only and never recomputes research evidence.
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from src import layer89_pages_runtime as pages_runtime

_LAYER8 = "08 · Conclusions"
_LAYER9 = "09 · Technical drill-down"
_VERSION = "layer89-authoritative-v2-vertical-contrib"


def install_layer89_authoritative() -> None:
    if getattr(st, "_layer89_authoritative_version", None) == _VERSION:
        return
    st._layer89_authoritative_version = _VERSION

    base_html = components.html
    base_markdown = st.markdown
    rendering = False

    def html_component(body, *args, **kwargs):
        nonlocal rendering
        if rendering:
            return base_html(body, *args, **kwargs)
        active = st.session_state.get("defense_section")
        text = str(body)
        if active == _LAYER8 and "WHAT DID WE LEARN?" in text and "No Free Lunch, made operational." in text:
            rendering = True
            try:
                pages_runtime.render_layer8()
            finally:
                rendering = False
            st.stop()
        return base_html(body, *args, **kwargs)

    def markdown(body, *args, **kwargs):
        nonlocal rendering
        if rendering:
            return base_markdown(body, *args, **kwargs)
        active = st.session_state.get("defense_section")
        text = str(body)
        if active == _LAYER9 and (
            "THESIS RESULTS — precomputed research output" in text
            or "THESIS RESULTS — external evidence" in text
        ):
            rendering = True
            try:
                pages_runtime.render_layer9()
            finally:
                rendering = False
            st.stop()
        return base_markdown(body, *args, **kwargs)

    components.html = html_component
    st.markdown = markdown
