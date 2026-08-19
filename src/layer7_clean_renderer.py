"""Final Layer 7 Plotly renderer that bypasses stale presentation wrappers.

Streamlit may hot-reload the app without recreating the module-level `st` object.
Earlier Layer 7 versions wrapped ``st.plotly_chart`` several times, so a stale
closure could keep restoring an older figure even after the source import was
updated.  This module unwraps only our Layer 7 wrappers and then installs one
final polished renderer directly on top of Streamlit's original Plotly method.

Presentation-only: thesis evidence is never recomputed here.
"""

from __future__ import annotations

import inspect
import streamlit as st

from src.results_journey_polished import result_figure

_LAYER7 = "07 · Results journey"
_VERSION = "layer7-clean-renderer-v1"
_LAYER7_MODULE_PREFIX = "src.layer7_"


def _stage() -> int:
    try:
        return max(0, min(int(st.session_state.get("results_stage", 0)), 4))
    except Exception:
        return 0


def _unwrap_layer7_plotly(fn):
    """Walk through Layer 7 wrapper closures until the underlying Streamlit call."""
    seen = set()
    current = fn
    while callable(current) and id(current) not in seen:
        seen.add(id(current))
        module = str(getattr(current, "__module__", ""))
        if not module.startswith(_LAYER7_MODULE_PREFIX):
            break

        next_fn = None
        closure = getattr(current, "__closure__", None) or ()
        freevars = getattr(getattr(current, "__code__", None), "co_freevars", ())
        values = {name: cell.cell_contents for name, cell in zip(freevars, closure)}
        for name in ("previous_plotly", "base_plotly", "original_plotly"):
            candidate = values.get(name)
            if callable(candidate):
                next_fn = candidate
                break
        if next_fn is None:
            # Defensive fallback: use the first callable closure value that is
            # not the wrapper itself.
            for candidate in values.values():
                if callable(candidate) and candidate is not current:
                    next_fn = candidate
                    break
        if next_fn is None:
            break
        current = next_fn
    return current


def install_layer7_clean_renderer() -> None:
    """Install one authoritative polished Plotly renderer for Results Journey."""
    # Always unwrap the current chain first.  The version guard is intentionally
    # secondary because a hot reload may leave a new stale wrapper outside an
    # already-installed clean renderer.
    original_plotly = _unwrap_layer7_plotly(st.plotly_chart)

    if (
        getattr(st, "_layer7_clean_renderer_version", None) == _VERSION
        and getattr(st, "_layer7_clean_renderer_base", None) is original_plotly
        and str(getattr(st.plotly_chart, "__module__", "")) == __name__
    ):
        return

    st._layer7_clean_renderer_version = _VERSION
    st._layer7_clean_renderer_base = original_plotly

    def plotly_chart(figure_or_data, *args, **kwargs):
        if st.session_state.get("defense_section") == _LAYER7:
            kwargs.pop("key", None)
            return original_plotly(result_figure(_stage()), *args, **kwargs)
        return original_plotly(figure_or_data, *args, **kwargs)

    st.plotly_chart = plotly_chart
