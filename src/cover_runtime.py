"""Small compatibility hook that renders the modular cover at full width.

The historical Streamlit cover first creates a narrow two-column layout. This
hook intercepts that one legacy column call and renders the current modular
cover before the old layout is created. It does not affect any other layer.
"""

from __future__ import annotations

import importlib
import streamlit as st


_COVER = "00 · Cover"
_VERSION = "cover-full-width-v1"


def _is_legacy_cover_columns(spec) -> bool:
    if not isinstance(spec, (list, tuple)) or len(spec) != 2:
        return False
    try:
        return abs(float(spec[0]) - 1.0) < 1e-9 and abs(float(spec[1]) - 3.4) < 1e-9
    except (TypeError, ValueError):
        return False


def install_cover_runtime() -> None:
    """Intercept only the legacy 1:3.4 cover layout and replace it safely."""
    if getattr(st, "_cover_runtime_version", None) == _VERSION:
        return
    st._cover_runtime_version = _VERSION

    base_columns = st.columns
    rendering = False

    def columns(spec, *args, **kwargs):
        nonlocal rendering
        if rendering:
            return base_columns(spec, *args, **kwargs)

        active = st.session_state.get("defense_section")
        try:
            presenter = str(st.query_params.get("presenter_notes", "")) == "1"
        except Exception:
            presenter = False

        if active == _COVER and not presenter and _is_legacy_cover_columns(spec):
            rendering = True
            try:
                module = importlib.import_module("src.cover_page")
                module = importlib.reload(module)
                module.render_cover_page()
            finally:
                rendering = False
            st.stop()

        return base_columns(spec, *args, **kwargs)

    st.columns = columns
