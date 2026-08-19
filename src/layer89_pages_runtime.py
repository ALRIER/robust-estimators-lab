"""Safe runtime loader for Layer 8/9 while the source module is being consolidated.

It reads the presentation module as text, escapes the one literal-brace q95 formula
inside an f-string, compiles it, and exposes the Layer 8/9 render functions. No thesis
data or results are modified.

Layer 8's Contributions & Limits view is intentionally overridden here because this
is the authoritative runtime module used by the deployed app. The Claims view remains
unchanged.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

_SOURCE = Path(__file__).with_name("layer89_pages.py")
_text = _SOURCE.read_text(encoding="utf-8")
_text = _text.replace(
    "q<sub>.95</sub>({(θ̂−θ)²})",
    "q<sub>.95</sub>({{(θ̂−θ)²}})",
)

_namespace = {
    "__name__": "src.layer89_pages_runtime_impl",
    "__file__": str(_SOURCE),
    "__package__": "src",
}
exec(compile(_text, str(_SOURCE), "exec"), _namespace)


def _conclusion_contrib_html_v2() -> str:
    """Vertical, projection-friendly Contributions & Limits story."""
    base_css = _namespace["_css"]()
    return base_css + """
    <style>
      .vertical-stack{display:flex;flex-direction:column;gap:15px;margin-top:12px}
      .contribution-card{display:grid;grid-template-columns:94px 1fr;gap:18px;align-items:center;
        background:linear-gradient(145deg,#102b48,#0a1d32);border:1px solid #356e99;
        border-radius:15px;padding:18px 22px;min-height:150px}
      .contribution-card.stat{border-left:6px solid #58aee8}
      .contribution-card.ai{border-left:6px solid #a777e3}
      .contribution-card.method{border-left:6px solid #54c786}
      .contribution-icon{width:76px;height:76px;border-radius:18px;display:flex;align-items:center;
        justify-content:center;font-size:43px;background:#08192b;border:1px solid #3c7198}
      .contribution-label{font-size:12px;font-weight:900;letter-spacing:.12em;color:#72cfff;margin-bottom:5px}
      .contribution-title{font-size:25px;font-weight:900;line-height:1.18;color:#fff;margin-bottom:7px}
      .contribution-copy{font-size:16px;line-height:1.48;color:#dce9f8}
      .why{margin-top:8px;font-size:14px;line-height:1.4;color:#b9c8d9}
      .why b{color:#f3c743}
      .limits-heading{margin:26px 0 10px;padding:13px 16px;border-radius:11px;
        background:#241d16;border:1px solid #806622;border-left:5px solid #f3c743}
      .limits-title{font-size:18px;font-weight:900;color:#ffe28b;margin-bottom:3px}
      .limits-sub{font-size:14px;line-height:1.4;color:#d8ccb1}
      .limit-stack{display:flex;flex-direction:column;gap:11px}
      .limit-row{display:grid;grid-template-columns:52px 235px 1fr;gap:14px;align-items:center;
        background:#121b27;border:1px solid #4e4b44;border-radius:12px;padding:14px 16px}
      .limit-icon{font-size:26px;text-align:center}
      .limit-name{font-size:16px;font-weight:900;color:#f5ead1}
      .limit-copy{font-size:15px;line-height:1.42;color:#d9d2c5}
      .strongest{margin-top:24px;border-radius:14px;padding:18px 22px;text-align:center;
        background:linear-gradient(90deg,#0d3047,#123a50);border:1px solid #72cfff;
        border-left:7px solid #f3c743}
      .strongest-label{font-size:12px;font-weight:900;letter-spacing:.13em;color:#f3c743;margin-bottom:6px}
      .strongest-text{font-size:21px;font-weight:900;line-height:1.35;color:#fff}
      @media(max-width:900px){
        .contribution-card{grid-template-columns:72px 1fr}.contribution-icon{width:62px;height:62px;font-size:34px}
        .limit-row{grid-template-columns:42px 1fr}.limit-copy{grid-column:2}
      }
    </style>
    <div class='page' style='min-height:1180px'>
      <div class='kicker'>08 · CONTRIBUTIONS AND LIMITS</div>
      <div class='title'>What the thesis contributes — and where the claim stops.</div>
      <div class='subtitle'>The three contributions are distinct but connected. The limits define the boundary of what the evidence can support.</div>

      <div class='sectionbar'>THREE CONTRIBUTIONS</div>
      <div class='vertical-stack'>
        <div class='contribution-card stat'>
          <div class='contribution-icon'>📊</div>
          <div>
            <div class='contribution-label'>STATISTICAL CONTRIBUTION</div>
            <div class='contribution-title'>Target-aware robust estimation of E[X]</div>
            <div class='contribution-copy'>A regime-conditional framework for combining established location estimators while keeping the population mean fixed as the target under skew, tails and contamination.</div>
            <div class='why'><b>Why it matters:</b> the target does not move when the regime changes; only the estimator strategy is allowed to adapt.</div>
          </div>
        </div>

        <div class='contribution-card ai'>
          <div class='contribution-icon'>🤖</div>
          <div>
            <div class='contribution-label'>AI CONTRIBUTION</div>
            <div class='contribution-title'>Interpretable evolutionary search over simplex weights</div>
            <div class='contribution-copy'>The GA searches convex weights over named estimators rather than learning an opaque prediction function. Every final recipe remains inspectable as a valid estimator mixture.</div>
            <div class='why'><b>Why it matters:</b> evolutionary search supplies flexible exploration without giving up statistical interpretability.</div>
          </div>
        </div>

        <div class='contribution-card method'>
          <div class='contribution-icon'>📘</div>
          <div>
            <div class='contribution-label'>METHODOLOGICAL CONTRIBUTION</div>
            <div class='contribution-title'>Benchmark-gated staged validation and claim control</div>
            <div class='contribution-copy'>Simulation certification, discovery, frozen-weight confirmation, expanded rediscovery, strict validation, external calibration and an independent random-simplex abstention audit are separated into distinct evidentiary stages.</div>
            <div class='why'><b>Why it matters:</b> search can suggest an opportunity, but only held-out evidence is allowed to justify a replacement claim.</div>
          </div>
        </div>
      </div>

      <div class='limits-heading'>
        <div class='limits-title'>LIMITS — where the claim must stop</div>
        <div class='limits-sub'>These are not hidden weaknesses. They are explicit boundaries on interpretation and transfer.</div>
      </div>
      <div class='limit-stack'>
        <div class='limit-row'><div class='limit-icon'>⚠️</div><div class='limit-name'>Simulated truth</div><div class='limit-copy'>The main known-truth validation relies on controlled data-generating distributions because real datasets do not reveal the population mean θ.</div></div>
        <div class='limit-row'><div class='limit-icon'>⚠️</div><div class='limit-name'>Narrow confirmed effects</div><div class='limit-copy'>The strongest supported improvements are specialists. They do not justify claiming a broadly superior estimator across an entire distribution family.</div></div>
        <div class='limit-row'><div class='limit-icon'>⚠️</div><div class='limit-name'>Profile-dependent transfer</div><div class='limit-copy'>A frozen specialist may transfer to a related unseen regime without being reliable far outside the profile under which that transfer was validated.</div></div>
        <div class='limit-row'><div class='limit-icon'>⚠️</div><div class='limit-name'>Real-data reference</div><div class='limit-copy'>External data use the full-sample empirical mean as a reference. That layer supports robustness and transfer, not population-ground-truth error recovery.</div></div>
      </div>

      <div class='strongest'>
        <div class='strongest-label'>SINGLE STRONGEST CONTRIBUTION</div>
        <div class='strongest-text'>A reproducible framework that knows when to claim an improvement — and when to keep the benchmark.</div>
      </div>
    </div>
    """


# Replace only the contribution page in the executed module's namespace. The
# existing Claims H1-H4 renderer and all Layer 9 appendix pages remain unchanged.
_namespace["_conclusion_contrib_html"] = _conclusion_contrib_html_v2


def _render_layer8_v2() -> None:
    """Render Layer 8 with an expanded vertical Contributions & Limits canvas."""
    st.markdown("""<style>
    .layer8-nav .stButton>button{min-height:3.6rem!important;font-size:1.05rem!important;font-weight:800!important}
    </style>""", unsafe_allow_html=True)
    if "conclusion_view" not in st.session_state:
        st.session_state.conclusion_view = "claims"

    st.markdown('<span class="badge thesis">DISCUSSION — close the timed defense</span>', unsafe_allow_html=True)
    st.markdown('<div class="layer8-nav">', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        if st.button(
            "Claims · H1–H4",
            key="conclusion_claims",
            use_container_width=True,
            type="primary" if st.session_state.conclusion_view == "claims" else "secondary",
        ):
            st.session_state.conclusion_view = "claims"
            st.rerun()
    with b:
        if st.button(
            "Contributions & Limits",
            key="conclusion_contrib",
            use_container_width=True,
            type="primary" if st.session_state.conclusion_view == "contrib" else "secondary",
        ):
            st.session_state.conclusion_view = "contrib"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.conclusion_view == "claims":
        html_doc = _namespace["_conclusion_claims_html"]()
        components.html(html_doc, height=735, scrolling=False)
    else:
        html_doc = _conclusion_contrib_html_v2()
        # Use a tall canvas so the browser page provides the scroll. This avoids
        # compressing seven stacked cards into a small embedded frame.
        components.html(html_doc, height=1260, scrolling=False)

    st.markdown("---")
    left, right = st.columns([3, 1])
    with left:
        st.info("End of timed defense. Stop here, thank the committee, and open the technical appendix only if a question requires it.")
    with right:
        if st.button("Technical Appendix →", type="primary", use_container_width=True, key="open_appendix"):
            st.session_state.defense_section = _namespace["_LAYER9"]
            st.rerun()


# Public runtime exports used by the authoritative Layer 8/9 hook.
install_layer89_pages = _namespace["install_layer89_pages"]
render_layer8 = _render_layer8_v2
render_layer9 = _namespace["_render_layer9"]
presenter_notes = _namespace["_presenter_notes"]
