"""Readability polish for Layer 7 presenter visuals.

Presentation-only CSS. No thesis evidence is changed or recomputed.
"""

import streamlit as st

_LAYER7 = "07 · Results journey"

_READABILITY_CSS = """<style>
.result-bubble{
  padding:1.25rem 1.28rem 1.32rem!important;
  min-height:535px!important;
}
.result-kicker{
  font-size:.80rem!important;
  letter-spacing:.13em!important;
}
.result-claim{
  font-size:1.32rem!important;
  line-height:1.20!important;
}
.result-plain{
  font-size:1.08rem!important;
  line-height:1.42!important;
  padding-bottom:1rem!important;
}
.result-label{
  font-size:.78rem!important;
  line-height:1.25!important;
  margin-top:1rem!important;
}
.result-copy{
  font-size:.96rem!important;
  line-height:1.48!important;
}
.result-key-strip{
  font-size:1.02rem!important;
  line-height:1.35!important;
  padding:.85rem 1.1rem!important;
}
</style>"""


def install_layer7_readability() -> None:
    if getattr(st, "_layer7_readability", False):
        return
    st._layer7_readability = True

    previous_markdown = st.markdown

    def markdown(body, *args, **kwargs):
        text = str(body)
        active = st.session_state.get("defense_section") == _LAYER7
        if active and "RESULTS JOURNEY — precomputed thesis evidence" in text:
            text = _READABILITY_CSS + text
        return previous_markdown(text, *args, **kwargs)

    st.markdown = markdown
