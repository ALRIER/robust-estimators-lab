"""Shared package hooks for the Robust Estimators Lab."""

# Presenter-note readability is isolated from the audience-facing dashboard.
# We wait until streamlit_app.py calls st.set_page_config(), then inject the
# hidden presenter stylesheet. This preserves Streamlit's page-config ordering
# and leaves every audience-facing view unchanged.
try:
    import streamlit as st
    from src.presenter_notes_style import PRESENTER_NOTES_CSS

    if not getattr(st.set_page_config, "_presenter_typography_wrapper", False):
        _original_set_page_config = st.set_page_config

        def _set_page_config_with_presenter_typography(*args, **kwargs):
            result = _original_set_page_config(*args, **kwargs)
            try:
                if st.query_params.get("presenter_notes") == "1":
                    st.markdown(PRESENTER_NOTES_CSS, unsafe_allow_html=True)
            except Exception:
                pass
            return result

        _set_page_config_with_presenter_typography._presenter_typography_wrapper = True
        st.set_page_config = _set_page_config_with_presenter_typography
except Exception:
    # Presentation-only styling must never interfere with the main app runtime.
    pass
