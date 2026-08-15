"""Shared package hooks for the Robust Estimators Lab."""

# Presenter-note readability is isolated from the audience-facing dashboard.
# The markdown wrapper is installed as soon as the src package loads, so HELP
# sections are converted reliably even if Streamlit keeps the Python worker
# alive across redeploys. No audience-facing view is modified.
try:
    import re
    import streamlit as st
    from src.presenter_notes_style import PRESENTER_NOTES_CSS

    _HELP_SECTION_RE = re.compile(
        r'(<section class="presenter-section"><h2>HELP</h2>)<p>(.*?)</p>(</section>)',
        re.DOTALL,
    )

    def _presenter_help_to_bullets(html: str) -> str:
        """Convert hidden HELP prose into short sentence-level cue bullets."""
        def _replace(match):
            text = match.group(2).strip()
            bullets = [
                item.strip()
                for item in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])|;\s+', text)
                if item.strip()
            ]
            items = "".join(f'<li>{item}</li>' for item in bullets)
            return (
                f'{match.group(1)}'
                f'<ul class="presenter-help-list">{items}</ul>'
                f'{match.group(3)}'
            )

        return _HELP_SECTION_RE.sub(_replace, html)

    # Install the HELP renderer immediately. Wrapping the function itself does
    # not emit Streamlit elements, so it is safe before st.set_page_config().
    if not getattr(st.markdown, "_presenter_help_wrapper", False):
        _original_markdown = st.markdown

        def _markdown_with_presenter_help(body, *args, **kwargs):
            try:
                if (
                    st.query_params.get("presenter_notes") == "1"
                    and isinstance(body, str)
                    and '<h2>HELP</h2>' in body
                ):
                    body = _presenter_help_to_bullets(body)
            except Exception:
                pass
            return _original_markdown(body, *args, **kwargs)

        _markdown_with_presenter_help._presenter_help_wrapper = True
        st.markdown = _markdown_with_presenter_help

    # Keep the enlarged cue-card typography injection after page configuration.
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
