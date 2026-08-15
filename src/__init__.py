"""Shared package hooks for the Robust Estimators Lab."""

# Presenter-note readability is isolated from the audience-facing dashboard.
# The hidden cue-card window is the only view that receives these overrides.
try:
    import streamlit as st
    from src.presenter_notes_style import PRESENTER_NOTES_CSS

    if st.query_params.get("presenter_notes") == "1":
        st.markdown(PRESENTER_NOTES_CSS, unsafe_allow_html=True)
except Exception:
    # Presentation-only styling must never interfere with the main app runtime.
    pass
