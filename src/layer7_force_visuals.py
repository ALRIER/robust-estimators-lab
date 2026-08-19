"""Force the polished narrative Layer 7 renderer for every Plotly chart in Results Journey.

This is presentation-only. It never recomputes thesis evidence.
"""

import streamlit as st

from src.results_journey_polished import result_figure

_LAYER7 = "07 · Results journey"
_VERSION = "layer7-force-visuals-v2-polished"


def _stage() -> int:
    try:
        return max(0, min(int(st.session_state.get("results_stage", 0)), 4))
    except Exception:
        return 0


def install_layer7_force_visuals() -> None:
    """Replace any central Plotly figure in Layer 7 with the polished narrative renderer."""
    if getattr(st, "_layer7_force_visuals_version", None) == _VERSION:
        return
    st._layer7_force_visuals_version = _VERSION

    previous_plotly = st.plotly_chart

    def plotly_chart(figure_or_data, *args, **kwargs):
        if st.session_state.get("defense_section") == _LAYER7:
            kwargs.pop("key", None)
            return previous_plotly(result_figure(_stage()), *args, **kwargs)
        return previous_plotly(figure_or_data, *args, **kwargs)

    st.plotly_chart = plotly_chart
