"""Replace the historical per-slide presenter link with one companion launcher."""

from __future__ import annotations

import re
import streamlit as st


_VERSION = "presenter-launcher-v1"


def install_presenter_launcher_runtime() -> None:
    if getattr(st, "_presenter_launcher_runtime_version", None) == _VERSION:
        return
    st._presenter_launcher_runtime_version = _VERSION

    base_markdown = st.markdown

    def markdown(body, *args, **kwargs):
        text = str(body)
        marker = 'title="Open presenter notes in the presenter window"'
        if marker in text and "presenter_notes=1" in text:
            text = re.sub(
                r'href="\?presenter_notes=1&amp;section=[^"]+"',
                'href="?presenter_companion=1"',
                text,
            )
            text = text.replace(
                marker,
                'title="Open Presenter Companion"',
            )
            text = text.replace(
                "robust_estimators_presenter_notes",
                "robust_estimators_presenter_companion",
            )
            return base_markdown(text, *args, **kwargs)
        return base_markdown(body, *args, **kwargs)

    st.markdown = markdown
