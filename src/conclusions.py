"""Direct renderer for Layer 8 · Conclusions.

No hooks or compatibility wrappers live here. This is the only audience-facing
Layer 8 implementation used by streamlit_app.py after repository consolidation.
"""

import streamlit as st
import streamlit.components.v1 as components


def _base_css() -> str:
    return """
    <style>
      *{box-sizing:border-box}
      body{margin:0;background:#081525;color:#e9f4ff;font-family:Arial,sans-serif}
      .page{padding:22px 24px 28px;background:#081525}
      .kicker{font-size:13px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin-bottom:8px}
      .title{font-size:32px;line-height:1.15;font-weight:900;color:#fff;margin-bottom:8px}
      .subtitle{font-size:16px;line-height:1.45;color:#b9c8d9;margin-bottom:20px}
      .takehome{margin-top:18px;background:#0e3047;border:1px solid #72cfff;border-left:6px solid #f3c743;border-radius:12px;padding:16px 19px;font-size:17px;line-height:1.45;font-weight:800;color:#f4f8ff}
    </style>
    """


def _claims_html() -> str:
    return _base_css() + """
    <style>
      .chain{display:flex;align-items:center;gap:8px;margin:16px 0 20px}
      .node{flex:1;background:#10253a;border:1px solid #3c7198;border-radius:11px;padding:12px;text-align:center;font-weight:800;font-size:14px}
      .arrow{font-size:25px;color:#72cfff;font-weight:900}
      .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
      .card{background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:13px;padding:17px 18px;min-height:175px}
      .green{border-top:4px solid #54c786}.gold{border-top:4px solid #f3c743}
      .small{font-size:12px;font-weight:900;letter-spacing:.10em;color:#72cfff;margin-bottom:8px}
      .big{font-size:24px;font-weight:900;line-height:1.16;margin-bottom:8px}
      .copy{font-size:15px;line-height:1.45;color:#dce9f8}
      .status{display:inline-block;margin-top:11px;padding:5px 9px;border-radius:16px;font-size:12px;font-weight:900;letter-spacing:.04em}
      .pass{background:#103b31;color:#a9f3c2;border:1px solid #54c786}
      .caution{background:#3a3214;color:#ffe387;border:1px solid #f3c743}
    </style>
    <div class='page'>
      <div class='kicker'>08 · DISCUSSION AND CONTRIBUTIONS</div>
      <div class='title'>No Free Lunch, made operational.</div>
      <div class='subtitle'>The thesis turns one theoretical idea into four testable claims and a disciplined evidence pipeline.</div>
      <div class='chain'>
        <div class='node'>H1 · no universal winner</div><div class='arrow'>→</div>
        <div class='node'>H2 · performance depends on regime</div><div class='arrow'>→</div>
        <div class='node'>H3 · GA helps selectively</div><div class='arrow'>→</div>
        <div class='node'>H4 · gate controls the claim</div>
      </div>
      <div class='grid'>
        <div class='card green'><div class='small'>H1</div><div class='big'>No universal estimator</div><div class='copy'>Estimator rankings change across incompatible distributional and contamination regimes.</div><div class='status pass'>SUPPORTED</div></div>
        <div class='card green'><div class='small'>H2</div><div class='big'>Performance depends on regime</div><div class='copy'>The useful estimator changes with family, contamination, scale, mechanism and sample size.</div><div class='status pass'>SUPPORTED</div></div>
        <div class='card gold'><div class='small'>H3</div><div class='big'>GA helps selected regimes</div><div class='copy'>Real gains exist, but they are narrow and profile-bound rather than general.</div><div class='status caution'>CONSERVATIVE SUPPORT</div></div>
        <div class='card green'><div class='small'>H4</div><div class='big'>The gate prevents false claims</div><div class='copy'>Discovery can be rejected. Benchmark retention is an intended scientific outcome.</div><div class='status pass'>SUPPORTED</div></div>
      </div>
      <div class='takehome'><b>TAKE-HOME:</b> the contribution is not a universal GA winner. It is a disciplined way to know when a composite estimator is justified — and when the benchmark should remain the answer.</div>
    </div>
    """


def _contributions_html() -> str:
    return _base_css() + """
    <style>
      .section-title{font-size:18px;font-weight:900;color:#f3c743;letter-spacing:.05em;margin:24px 0 12px}
      .contrib{display:grid;grid-template-columns:110px 1fr;gap:20px;align-items:center;background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:15px;padding:20px 22px;margin-bottom:16px;min-height:178px}
      .contrib.stat{border-left:6px solid #58aee8}.contrib.ai{border-left:6px solid #a777e3}.contrib.method{border-left:6px solid #54c786}
      .icon{width:82px;height:82px;border-radius:20px;background:#10253a;border:1px solid #3c7198;display:flex;align-items:center;justify-content:center;font-size:42px;margin:auto}
      .label{font-size:12px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:7px}
      .headline{font-size:25px;font-weight:900;line-height:1.18;color:#fff;margin-bottom:8px}
      .copy{font-size:16px;line-height:1.46;color:#dce9f8;margin-bottom:10px}
      .why{font-size:14px;line-height:1.42;color:#b9c8d9;background:#0a1d32;border-radius:8px;padding:9px 11px}
      .why b{color:#f3c743}
      .limits{background:#241e16;border:1px solid #8a6a1b;border-radius:15px;padding:17px 18px 8px;margin-top:8px}
      .limit{display:grid;grid-template-columns:58px 1fr;gap:14px;align-items:start;background:#171b23;border:1px solid #55472b;border-radius:11px;padding:14px 16px;margin-bottom:11px}
      .limit-icon{font-size:28px;text-align:center;padding-top:2px}
      .limit-title{font-size:17px;font-weight:900;color:#fff0af;margin-bottom:4px}
      .limit-copy{font-size:15px;line-height:1.43;color:#eee5d0}
      .strongest{margin-top:20px;background:#12354a;border:1px solid #58aee8;border-left:7px solid #f3c743;border-radius:13px;padding:19px 21px}
      .strongest-label{font-size:12px;font-weight:900;letter-spacing:.12em;color:#f3c743;margin-bottom:7px}
      .strongest-copy{font-size:21px;line-height:1.35;font-weight:900;color:#fff}
    </style>
    <div class='page'>
      <div class='kicker'>08 · CONTRIBUTIONS AND LIMITS</div>
      <div class='title'>What the thesis contributes — and where the claim stops.</div>
      <div class='subtitle'>The contribution is easier to defend when each part is explicit: what is statistical, what is AI, what is methodological, and what remains outside the claim.</div>

      <div class='section-title'>CONTRIBUTIONS</div>

      <div class='contrib stat'>
        <div class='icon'>📊</div>
        <div>
          <div class='label'>STATISTICAL CONTRIBUTION</div>
          <div class='headline'>Target-aware robust estimation of E[X]</div>
          <div class='copy'>A regime-conditional way to combine established location estimators while keeping the population mean fixed as the target under skew, tails and contamination.</div>
          <div class='why'><b>Why it matters:</b> the thesis does not change the estimand to make robustness easier; it asks whether a composite can estimate the same population mean with lower finite-sample risk.</div>
        </div>
      </div>

      <div class='contrib ai'>
        <div class='icon'>🤖</div>
        <div>
          <div class='label'>AI CONTRIBUTION</div>
          <div class='headline'>Interpretable evolutionary search over simplex weights</div>
          <div class='copy'>The GA searches convex weights over named estimators rather than learning an opaque prediction function. Every final recipe remains inspectable as an estimator mixture.</div>
          <div class='why'><b>Why it matters:</b> evolutionary search supplies adaptive exploration while the simplex keeps the output statistically interpretable and auditable.</div>
        </div>
      </div>

      <div class='contrib method'>
        <div class='icon'>📘</div>
        <div>
          <div class='label'>METHODOLOGICAL CONTRIBUTION</div>
          <div class='headline'>Benchmark-gated staged validation and claim control</div>
          <div class='copy'>Simulation certification, discovery, frozen confirmation, expanded rediscovery, strict validation, external calibration and the Dirichlet abstention audit are separated deliberately.</div>
          <div class='why'><b>Why it matters:</b> optimization can suggest a candidate, but only independent evidence can authorize the scientific claim.</div>
        </div>
      </div>

      <div class='section-title'>LIMITS</div>
      <div class='limits'>
        <div class='limit'><div class='limit-icon'>⚠️</div><div><div class='limit-title'>Simulated truth</div><div class='limit-copy'>The strongest known-truth validation relies on controlled data-generating distributions. Simulation makes θ observable, but it cannot represent every empirical process.</div></div></div>
        <div class='limit'><div class='limit-icon'>⚠️</div><div><div class='limit-title'>Narrow confirmed effects</div><div class='limit-copy'>The most defensible improvements are specialists. The evidence does not support a universal GA estimator or a broad family-wide winner.</div></div></div>
        <div class='limit'><div class='limit-icon'>⚠️</div><div><div class='limit-title'>Profile-dependent transfer</div><div class='limit-copy'>A frozen specialist should not be extrapolated far beyond the structural regime in which transfer was actually validated.</div></div></div>
        <div class='limit'><div class='limit-icon'>⚠️</div><div><div class='limit-title'>Real-data reference</div><div class='limit-copy'>External datasets do not reveal population θ. The full-sample empirical mean is therefore a calibration reference, not known population ground truth.</div></div></div>
      </div>

      <div class='strongest'>
        <div class='strongest-label'>SINGLE STRONGEST CONTRIBUTION</div>
        <div class='strongest-copy'>A reproducible framework that knows when to claim an improvement — and when to keep the benchmark.</div>
      </div>
    </div>
    """


def _set_view(view: str) -> None:
    st.session_state.conclusion_view = view


def render_conclusions() -> None:
    st.markdown("""
    <style>
      .layer8-nav .stButton>button{min-height:3.6rem!important;font-size:1.02rem!important;font-weight:800!important}
    </style>
    """, unsafe_allow_html=True)

    if "conclusion_view" not in st.session_state:
        st.session_state.conclusion_view = "claims"

    st.markdown('<span class="badge thesis">DISCUSSION — close the timed defense</span>', unsafe_allow_html=True)
    st.markdown('<div class="layer8-nav">', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.button("Claims · H1–H4", key="conclusion_direct_claims", use_container_width=True,
                  type="primary" if st.session_state.conclusion_view == "claims" else "secondary",
                  on_click=_set_view, args=("claims",))
    with b:
        st.button("Contributions & Limits", key="conclusion_direct_contrib", use_container_width=True,
                  type="primary" if st.session_state.conclusion_view == "contrib" else "secondary",
                  on_click=_set_view, args=("contrib",))
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.conclusion_view == "claims":
        components.html(_claims_html(), height=720, scrolling=False)
    else:
        # Deliberately tall: the browser page scrolls naturally instead of compressing
        # three contributions and four limits into one crowded slide.
        components.html(_contributions_html(), height=1530, scrolling=False)

    st.markdown("---")
    left, right = st.columns([3, 1])
    with left:
        st.info("End of timed defense. Stop here, thank the committee, and open the technical appendix only if a question requires it.")
    with right:
        if st.button("Technical Appendix →", type="primary", use_container_width=True, key="conclusion_direct_appendix"):
            st.session_state.defense_section = "09 · Technical drill-down"
            st.rerun()
