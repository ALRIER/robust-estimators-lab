"""Shared package hooks for the Robust Estimators Lab."""

# Presenter-note readability is isolated from the audience-facing dashboard.
# We wait until streamlit_app.py calls st.set_page_config(), then inject the
# hidden presenter stylesheet and convert only HELP paragraphs into short,
# scannable cue-card bullets. Audience-facing views remain unchanged.
try:
    import re
    import streamlit as st
    from src.presenter_notes_style import PRESENTER_NOTES_CSS

    _HELP_SECTION_RE = re.compile(
        r'(<section class="presenter-section"><h2>HELP</h2>)<p>(.*?)</p>(</section>)',
        re.DOTALL,
    )

    def _presenter_help_to_bullets(html: str) -> str:
        """Turn the hidden HELP paragraph into sentence-level speaking cues."""
        def _replace(match):
            text = match.group(2).strip()
            # Split at sentence boundaries and semicolons. This preserves the
            # original meaning while making the cue card easier to scan at a
            # distance during the defense.
            bullets = [
                item.strip()
                for item in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])|;\s+', text)
                if item.strip()
            ]
            items = "".join(f'<li>{item}</li>' for item in bullets)
            return f'{match.group(1)}<ul class="presenter-help-list">{items}</ul>{match.group(3)}'

        return _HELP_SECTION_RE.sub(_replace, html)

    if not getattr(st.set_page_config, "_presenter_typography_wrapper", False):
        _original_set_page_config = st.set_page_config

        def _set_page_config_with_presenter_typography(*args, **kwargs):
            result = _original_set_page_config(*args, **kwargs)
            try:
                if st.query_params.get("presenter_notes") == "1":
                    _original_markdown = st.markdown
                    _original_markdown(PRESENTER_NOTES_CSS, unsafe_allow_html=True)

                    if not getattr(st.markdown, "_presenter_help_wrapper", False):
                        def _markdown_with_presenter_help(body, *md_args, **md_kwargs):
                            if isinstance(body, str) and '<h2>HELP</h2>' in body:
                                body = _presenter_help_to_bullets(body)
                            return _original_markdown(body, *md_args, **md_kwargs)

                        _markdown_with_presenter_help._presenter_help_wrapper = True
                        st.markdown = _markdown_with_presenter_help
            except Exception:
                pass
            return result

        _set_page_config_with_presenter_typography._presenter_typography_wrapper = True
        st.set_page_config = _set_page_config_with_presenter_typography
except Exception:
    # Presentation-only styling must never interfere with the main app runtime.
    pass
