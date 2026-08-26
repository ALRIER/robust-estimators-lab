"""Audience-facing cover for the thesis defense.

The cover is intentionally lightweight: it introduces the formal thesis title,
a short bounded descriptor, and a three-engine preview of the defense journey.
It does not recompute evidence or replace the later roadmap / methods layers.
"""

from __future__ import annotations

from base64 import b64encode
from pathlib import Path
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
_LOGO = "data:image/jpeg;base64," + b64encode(
    (ROOT / "assets" / "university_of_hull_logo.jpeg").read_bytes()
).decode("ascii")


def _go(section: str) -> None:
    st.session_state.defense_section = section


def render_cover_page() -> None:
    """Render the redesigned cover and preserve the original navigation actions."""
    st.markdown(
        """
        <style>
          .cover-wrap{max-width:1460px;margin:.25rem auto 0;font-family:Arial,sans-serif;color:#eef6ff}
          .cover-hero{position:relative;overflow:hidden;border:1px solid #2d6d9c;border-radius:22px;
            background:
              radial-gradient(circle at 78% 8%,rgba(61,133,195,.20),transparent 31%),
              radial-gradient(circle at 10% 82%,rgba(88,174,232,.12),transparent 28%),
              linear-gradient(145deg,#071426 0%,#07182c 52%,#06101e 100%);
            box-shadow:0 24px 70px rgba(0,0,0,.25);padding:38px 46px 34px}
          .cover-hero:before,.cover-hero:after{content:"";position:absolute;border:1px solid rgba(88,174,232,.22);border-radius:50%;pointer-events:none}
          .cover-hero:before{width:720px;height:240px;right:-150px;bottom:170px;transform:rotate(-8deg)}
          .cover-hero:after{width:690px;height:220px;left:-260px;bottom:80px;transform:rotate(7deg)}
          .cover-top{position:relative;z-index:2;text-align:center;max-width:1220px;margin:0 auto}
          .cover-kicker{font-size:14px;font-weight:900;letter-spacing:.16em;color:#f3c743;margin-bottom:14px}
          .cover-title{font-family:Georgia,serif;font-size:54px;line-height:1.08;font-weight:800;color:#fff;margin:0 auto 13px;text-shadow:0 0 28px rgba(88,174,232,.13)}
          .cover-subtitle{font-size:22px;line-height:1.38;font-weight:750;color:#cfe2f5;max-width:1080px;margin:0 auto}
          .cover-rule{display:flex;align-items:center;justify-content:center;gap:14px;margin:20px auto 16px;max-width:780px}
          .cover-rule span{height:1px;background:linear-gradient(90deg,transparent,#f3c743);flex:1}.cover-rule span:last-child{background:linear-gradient(90deg,#f3c743,transparent)}
          .cover-diamond{width:11px;height:11px;background:#f3c743;transform:rotate(45deg);border:2px solid #ffc94f}
          .cover-descriptor{font-size:18px;line-height:1.45;color:#f3c743;font-style:italic;max-width:990px;margin:0 auto 22px}
          .identity{display:grid;grid-template-columns:1.2fr .8fr;gap:24px;align-items:center;max-width:940px;margin:0 auto 28px;position:relative;z-index:2}
          .person{text-align:right;border-right:1px solid #356e99;padding-right:24px}.person-name{font-size:28px;font-weight:900;color:#fff}.person-program{font-size:15px;font-weight:850;letter-spacing:.10em;color:#72cfff;margin-top:5px}
          .uni{text-align:left}.uni img{display:block;max-width:285px;width:100%;background:#fff;border-radius:8px;padding:7px}
          .journey-label{position:relative;z-index:2;text-align:center;font-size:12px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin:4px 0 11px}
          .journey{position:relative;z-index:2;display:grid;grid-template-columns:1fr 52px 1fr 52px 1fr;gap:10px;align-items:stretch;margin-top:4px}
          .journey-card{background:linear-gradient(145deg,rgba(15,43,71,.95),rgba(8,29,50,.95));border:1px solid #356e99;border-radius:16px;padding:20px 20px 18px;min-height:170px;text-align:center}
          .journey-card.mc{border-top:3px solid #58aee8}.journey-card.ga{border-top:3px solid #a777e3}.journey-card.ev{border-top:3px solid #f3c743}
          .journey-icon{width:48px;height:48px;border-radius:50%;margin:0 auto 10px;display:flex;align-items:center;justify-content:center;background:#102a45;border:1px solid #3c7198;font-size:21px;font-weight:900;color:#fff}
          .journey-num{font-size:10px;font-weight:900;letter-spacing:.11em;color:#9db5ca;margin-bottom:4px}
          .journey-head{font-size:20px;font-weight:900;color:#fff;margin-bottom:7px}.journey-copy{font-size:14px;line-height:1.42;color:#c9d9e8}
          .journey-arrow{display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;color:#72cfff}
          .cover-foot{position:relative;z-index:2;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:19px;padding-top:17px;border-top:1px solid #244f72}
          .foot-item{text-align:center;font-size:13px;line-height:1.4;color:#aebfd0}.foot-item b{display:block;color:#eaf4ff;font-size:13px;letter-spacing:.04em;margin-bottom:2px}
          .cover-boundary{position:relative;z-index:2;background:#0f2d46;border:1px solid #3d7197;border-left:5px solid #f3c743;border-radius:12px;margin-top:18px;padding:13px 16px;text-align:center;font-size:15px;line-height:1.45;color:#e8f4ff}
          .cover-actions{max-width:1020px;margin:18px auto 0}.cover-actions [data-testid="stHorizontalBlock"]{gap:.75rem!important}
          @media(max-width:1000px){.cover-title{font-size:42px}.identity{grid-template-columns:1fr}.person{text-align:center;border-right:0;border-bottom:1px solid #356e99;padding:0 0 16px}.uni{text-align:center}.uni img{margin:0 auto}.journey{grid-template-columns:1fr}.journey-arrow{transform:rotate(90deg)}.cover-foot{grid-template-columns:1fr}}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="cover-wrap">
          <div class="cover-hero">
            <div class="cover-top">
              <div class="cover-kicker">MASTER'S THESIS DEFENSE</div>
              <div class="cover-title">Building Better Estimators</div>
              <div class="cover-subtitle">Benchmark-gated, regime-conditional composite mean estimation via genetic search</div>
              <div class="cover-rule"><span></span><div class="cover-diamond"></div><span></span></div>
              <div class="cover-descriptor">A staged framework for generating controlled evidence, searching interpretable mixtures, and deciding when a replacement claim is justified.</div>
            </div>

            <div class="identity">
              <div class="person">
                <div class="person-name">Álvaro Rivera-Eraso</div>
                <div class="person-program">MSC ARTIFICIAL INTELLIGENCE · THESIS DEFENSE</div>
              </div>
              <div class="uni"><img src="{_LOGO}" alt="University of Hull" /></div>
            </div>

            <div class="journey-label">THE STUDY IN THREE ENGINES · A PREVIEW OF THE DEFENSE JOURNEY</div>
            <div class="journey">
              <div class="journey-card mc">
                <div class="journey-icon">θ</div><div class="journey-num">01 · CONTROLLED WORLD</div>
                <div class="journey-head">Monte Carlo World</div>
                <div class="journey-copy">Define regimes, keep the population-mean target known, generate repeated samples, and measure finite-sample risk.</div>
              </div>
              <div class="journey-arrow">→</div>
              <div class="journey-card ga">
                <div class="journey-icon">w</div><div class="journey-num">02 · INTERPRETABLE SEARCH</div>
                <div class="journey-head">GA Search Design</div>
                <div class="journey-copy">Search simplex-safe estimator mixtures, evolve candidate weight vectors, then freeze promising recipes before confirmation.</div>
              </div>
              <div class="journey-arrow">→</div>
              <div class="journey-card ev">
                <div class="journey-icon">✓</div><div class="journey-num">03 · CLAIM CONTROL</div>
                <div class="journey-head">Tournament of Evidence</div>
                <div class="journey-copy">Challenge frozen candidates with stronger benchmarks and staged validation, then classify what survives and what is retained.</div>
              </div>
            </div>

            <div class="cover-boundary"><b>Scope:</b> conditional estimator discovery and validation — not universal GA superiority.</div>
            <div class="cover-foot">
              <div class="foot-item"><b>PROGRAMME</b>MSc Artificial Intelligence</div>
              <div class="foot-item"><b>INSTITUTION</b>University of Hull</div>
              <div class="foot-item"><b>DEFENSE MODE</b>Problem → World → Search → Evidence → Meaning</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="cover-actions">', unsafe_allow_html=True)
    start, results, appendix = st.columns([1.45, 1, 1])
    with start:
        st.button(
            "Start Defense →",
            key="cover_start_defense",
            type="primary",
            use_container_width=True,
            on_click=_go,
            args=("01 · Research logic",),
        )
    with results:
        st.button(
            "Jump to Results",
            key="cover_jump_results",
            use_container_width=True,
            on_click=_go,
            args=("07 · Results journey",),
        )
    with appendix:
        st.button(
            "Technical Appendix",
            key="cover_jump_appendix",
            use_container_width=True,
            on_click=_go,
            args=("09 · Technical drill-down",),
        )
    st.markdown('</div>', unsafe_allow_html=True)
