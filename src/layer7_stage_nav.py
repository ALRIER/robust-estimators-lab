"""Make Layer 7 result-tab state available before the sidebar is redrawn."""

import streamlit as st
from src.results_journey import RESULT_STAGES


def install_layer7_stage_navigation() -> None:
    if getattr(st, "_layer7_stage_nav", False):
        return
    st._layer7_stage_nav = True

    original_button = st.button
    labels = {item["label"]: i for i, item in enumerate(RESULT_STAGES)}

    def _select(index: int) -> None:
        st.session_state.results_stage = int(index)
        st.session_state.results_explanation = 0

    def button(label, *args, **kwargs):
        try:
            active = st.session_state.get("defense_section") == "07 · Results journey"
        except Exception:
            active = False
        if active and str(label) in labels and "on_click" not in kwargs:
            kwargs["on_click"] = _select
            kwargs["args"] = (labels[str(label)],)
        return original_button(label, *args, **kwargs)

    st.button = button
