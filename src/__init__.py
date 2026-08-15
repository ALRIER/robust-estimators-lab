"""Shared package hooks for the Robust Estimators Lab."""

# Presenter-note readability is isolated from the audience-facing dashboard.
# The markdown wrapper is installed as soon as the src package loads so the
# hidden cue-card window can render HELP and formula explanations differently
# without touching any audience-facing slide.
try:
    import html
    import re
    import streamlit as st
    from src.presenter_notes_style import PRESENTER_NOTES_CSS
    from src.presenter_formula_guides import FORMULA_GUIDES

    _HELP_SECTION_RE = re.compile(
        r'(<section class="presenter-section"><h2>HELP</h2>)<p>(.*?)</p>(</section>)',
        re.DOTALL,
    )
    _FORMULA_SECTION_RE = re.compile(
        r'<section class="presenter-section"><h2>FORMULAS AND NOTATION</h2>.*?</section>',
        re.DOTALL,
    )

    def _presenter_help_to_bullets(markup: str) -> str:
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

        return _HELP_SECTION_RE.sub(_replace, markup)

    def _formula_guide_html(section_key: str) -> str | None:
        """Build formula → component bullets for one presenter-note panel."""
        guides = FORMULA_GUIDES.get(section_key)
        if not guides:
            return None

        cards = []
        for title, formula, parts in guides:
            bullets = "".join(
                f'<li><strong>{html.escape(symbol)}</strong> — {html.escape(explanation)}</li>'
                for symbol, explanation in parts
            )
            cards.append(
                '<div class="presenter-formula-card">'
                f'<div class="presenter-formula-title">{html.escape(title)}</div>'
                f'<div class="presenter-formula-expression">{html.escape(formula)}</div>'
                f'<ul class="presenter-formula-parts">{bullets}</ul>'
                '</div>'
            )

        return (
            '<section class="presenter-section presenter-formulas">'
            '<h2>FORMULAS AND NOTATION</h2>'
            + "".join(cards)
            + '</section>'
        )

    def _presenter_formulas_to_guides(markup: str, section_key: str) -> str:
        """Replace the flat formula list with structured formula cards."""
        replacement = _formula_guide_html(section_key)
        if not replacement:
            return markup
        return _FORMULA_SECTION_RE.sub(replacement, markup)

    # Install the presenter renderer immediately. Wrapping the function itself
    # emits no Streamlit elements, so it remains safe before set_page_config().
    if not getattr(st.markdown, "_presenter_notes_wrapper", False):
        _original_markdown = st.markdown

        def _markdown_with_presenter_notes(body, *args, **kwargs):
            try:
                if st.query_params.get("presenter_notes") == "1" and isinstance(body, str):
                    if '<h2>HELP</h2>' in body:
                        body = _presenter_help_to_bullets(body)
                    if '<h2>FORMULAS AND NOTATION</h2>' in body:
                        body = _presenter_formulas_to_guides(
                            body,
                            st.query_params.get("section", ""),
                        )
            except Exception:
                # Presenter enhancements must never break the defense app.
                pass
            return _original_markdown(body, *args, **kwargs)

        _markdown_with_presenter_notes._presenter_notes_wrapper = True
        st.markdown = _markdown_with_presenter_notes

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
