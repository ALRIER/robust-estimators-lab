"""Query-param runtime for the parallel Presenter Companion.

Installed before the main app calls ``st.set_page_config``.  When the companion
query parameter is present, the same Streamlit deployment renders only the cue
interface and stops before the audience presentation is built.
"""

from __future__ import annotations

import importlib
import streamlit as st


_VERSION = "presenter-companion-runtime-v1"


def install_presenter_companion_runtime() -> None:
    if getattr(st, "_presenter_companion_runtime_version", None) == _VERSION:
        return
    st._presenter_companion_runtime_version = _VERSION

    base_set_page_config = st.set_page_config

    def set_page_config(*args, **kwargs):
        try:
            companion = str(st.query_params.get("presenter_companion", "")) == "1"
        except Exception:
            companion = False

        if not companion:
            return base_set_page_config(*args, **kwargs)

        base_set_page_config(
            page_title="Presenter Companion · Robust Estimators Lab",
            page_icon="🗂️",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        module = importlib.import_module("src.presenter_companion")
        module = importlib.reload(module)
        module.render_presenter_companion()
        st.stop()

    st.set_page_config = set_page_config
