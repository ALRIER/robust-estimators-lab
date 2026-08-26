"""Audience-facing cover for the thesis defense.

The cover introduces the formal thesis title, candidate and supervisor, and a
compact four-step preview of the defense journey. The visual is rendered inside
an isolated Streamlit HTML component so raw HTML can never leak into the
presentation as Markdown/code.
"""

from __future__ import annotations

from base64 import b64encode
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parents[1]
_LOGO = "data:image/jpeg;base64," + b64encode(
    (ROOT / "assets" / "university_of_hull_logo.jpeg").read_bytes()
).decode("ascii")


def _go(section: str) -> None:
    st.session_state.defense_section = section


def _cover_html() -> str:
    """Build one self-contained HTML document for the audience-facing cover."""
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:#071525;color:#eef6ff;font-family:Arial,sans-serif;overflow:hidden}}
.cover-wrap{{width:100%;max-width:1500px;margin:0 auto;padding:4px 6px 8px}}
.cover-hero{{position:relative;overflow:hidden;border:1px solid #2d6d9c;border-radius:22px;background:radial-gradient(circle at 78% 8%,rgba(61,133,195,.20),transparent 31%),radial-gradient(circle at 10% 82%,rgba(88,174,232,.12),transparent 28%),linear-gradient(145deg,#071426 0%,#07182c 52%,#06101e 100%);box-shadow:0 24px 70px rgba(0,0,0,.25);padding:30px 38px 28px}}
.cover-hero:before,.cover-hero:after{{content:"";position:absolute;border:1px solid rgba(88,174,232,.20);border-radius:50%;pointer-events:none}}
.cover-hero:before{{width:760px;height:245px;right:-180px;bottom:155px;transform:rotate(-8deg)}}
.cover-hero:after{{width:720px;height:220px;left:-285px;bottom:62px;transform:rotate(7deg)}}
.cover-top{{position:relative;z-index:2;text-align:center;max-width:1240px;margin:0 auto}}
.cover-kicker{{font-size:13px;font-weight:900;letter-spacing:.16em;color:#f3c743;margin-bottom:10px}}
.cover-title{{font-family:Georgia,serif;font-size:50px;line-height:1.07;font-weight:800;color:#fff;margin:0 auto 10px;text-shadow:0 0 28px rgba(88,174,232,.13)}}
.cover-subtitle{{font-size:20px;line-height:1.38;font-weight:750;color:#cfe2f5;max-width:1090px;margin:0 auto}}
.cover-rule{{display:flex;align-items:center;justify-content:center;gap:14px;margin:15px auto 12px;max-width:760px}}
.cover-rule span{{height:1px;background:linear-gradient(90deg,transparent,#f3c743);flex:1}}
.cover-rule span:last-child{{background:linear-gradient(90deg,#f3c743,transparent)}}
.cover-diamond{{width:10px;height:10px;background:#f3c743;transform:rotate(45deg);border:2px solid #ffc94f}}
.cover-descriptor{{font-size:16px;line-height:1.43;color:#f3c743;font-style:italic;max-width:1010px;margin:0 auto 18px}}
.identity{{position:relative;z-index:2;display:grid;grid-template-columns:1fr 1fr .9fr;gap:0;align-items:center;max-width:1120px;margin:0 auto 22px;background:rgba(9,30,51,.54);border:1px solid #244f72;border-radius:14px;overflow:hidden}}
.identity-block{{padding:14px 19px;min-height:78px;display:flex;flex-direction:column;justify-content:center}}
.identity-block+.identity-block{{border-left:1px solid #2c5c82}}
.identity-label{{font-size:10px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin-bottom:5px}}
.identity-value{{font-size:20px;font-weight:900;color:#fff;line-height:1.18}}
.identity-sub{{font-size:12px;line-height:1.38;color:#b9ccdf;margin-top:4px}}
.uni{{text-align:center;align-items:center}}
.uni img{{display:block;max-width:245px;width:100%;margin:auto;background:#fff;border-radius:7px;padding:6px}}
.journey-label{{position:relative;z-index:2;text-align:center;font-size:12px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin:2px 0 10px}}
.journey{{position:relative;z-index:2;display:grid;grid-template-columns:1fr 34px 1fr 34px 1fr 34px 1fr;gap:8px;align-items:stretch;margin-top:4px}}
.journey-card{{background:linear-gradient(145deg,rgba(15,43,71,.95),rgba(8,29,50,.95));border:1px solid #356e99;border-radius:16px;padding:15px 14px 14px;min-height:180px;text-align:center}}
.journey-card.qo{{border-top:3px solid #f3c743}}.journey-card.mc{{border-top:3px solid #58aee8}}.journey-card.ga{{border-top:3px solid #a777e3}}.journey-card.ev{{border-top:3px solid #54c786}}
.journey-icon{{width:48px;height:48px;border-radius:50%;margin:0 auto 8px;display:flex;align-items:center;justify-content:center;background:#102a45;border:1px solid #3c7198;font-size:23px;font-weight:900;color:#fff}}
.journey-num{{font-size:9.5px;font-weight:900;letter-spacing:.11em;color:#9db5ca;margin-bottom:4px}}
.journey-head{{font-size:18px;font-weight:900;color:#fff;margin-bottom:6px;line-height:1.18}}
.journey-copy{{font-size:13px;line-height:1.4;color:#c9d9e8}}
.journey-arrow{{display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:#72cfff}}
.cover-boundary{{position:relative;z-index:2;background:#0f2d46;border:1px solid #3d7197;border-left:5px solid #f3c743;border-radius:12px;margin-top:15px;padding:11px 15px;text-align:center;font-size:14px;line-height:1.43;color:#e8f4ff}}
.cover-foot{{position:relative;z-index:2;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:13px;padding-top:12px;border-top:1px solid #244f72}}
.foot-item{{text-align:center;font-size:12px;line-height:1.38;color:#aebfd0}}
.foot-item b{{display:block;color:#eaf4ff;font-size:12px;letter-spacing:.04em;margin-bottom:2px}}
@media(max-width:1180px){{.cover-title{{font-size:42px}}.identity{{grid-template-columns:1fr 1fr}}.uni{{grid-column:1/3;border-left:0!important;border-top:1px solid #2c5c82}}.journey{{grid-template-columns:1fr 26px 1fr;row-gap:14px}}}}
@media(max-width:760px){{html,body{{overflow:auto}}.cover-hero{{padding:24px 20px}}.cover-title{{font-size:35px}}.cover-subtitle{{font-size:17px}}.identity{{grid-template-columns:1fr}}.identity-block+.identity-block{{border-left:0;border-top:1px solid #2c5c82}}.uni{{grid-column:auto}}.journey{{grid-template-columns:1fr}}.journey-arrow{{transform:rotate(90deg)}}.cover-foot{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
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
      <div class="identity-block">
        <div class="identity-label">CANDIDATE</div>
        <div class="identity-value">Álvaro Rivera-Eraso</div>
        <div class="identity-sub">MSc Artificial Intelligence · Thesis Defense</div>
      </div>
      <div class="identity-block">
        <div class="identity-label">SUPERVISOR</div>
        <div class="identity-value">Debarati Chakraborty, Ph.D.</div>
        <div class="identity-sub">University of Hull</div>
      </div>
      <div class="identity-block uni"><img src="{_LOGO}" alt="University of Hull"></div>
    </div>

    <div class="journey-label">FROM QUESTION TO EVIDENCE · A PREVIEW OF THE DEFENSE JOURNEY</div>
    <div class="journey">
      <div class="journey-card qo">
        <div class="journey-icon">💡</div><div class="journey-num">01 · FRAMING</div>
        <div class="journey-head">Question &amp; Objective</div>
        <div class="journey-copy">Define the statistical problem, keep the population-mean target explicit, and ask when an interpretable composite can be justified.</div>
      </div>
      <div class="journey-arrow">→</div>
      <div class="journey-card mc">
        <div class="journey-icon">θ</div><div class="journey-num">02 · CONTROLLED WORLD</div>
        <div class="journey-head">Monte Carlo World</div>
        <div class="journey-copy">Define regimes, know the population truth, generate repeated samples, and measure finite-sample risk under controlled conditions.</div>
      </div>
      <div class="journey-arrow">→</div>
      <div class="journey-card ga">
        <div class="journey-icon">w</div><div class="journey-num">03 · INTERPRETABLE SEARCH</div>
        <div class="journey-head">GA Search Design</div>
        <div class="journey-copy">Search simplex-safe estimator mixtures, evolve candidate weight vectors, and freeze promising recipes before confirmation.</div>
      </div>
      <div class="journey-arrow">→</div>
      <div class="journey-card ev">
        <div class="journey-icon">✓</div><div class="journey-num">04 · CLAIM CONTROL</div>
        <div class="journey-head">Tournament of Evidence</div>
        <div class="journey-copy">Challenge frozen candidates through staged validation, stronger benchmarks, transfer checks, and the final evidence taxonomy.</div>
      </div>
    </div>

    <div class="cover-boundary"><b>Scope:</b> conditional estimator discovery and validation — not universal GA superiority.</div>
    <div class="cover-foot">
      <div class="foot-item"><b>PROGRAMME</b>MSc Artificial Intelligence</div>
      <div class="foot-item"><b>INSTITUTION</b>University of Hull</div>
      <div class="foot-item"><b>DEFENSE PATH</b>Question → World → Search → Evidence → Meaning</div>
    </div>
  </div>
</div>
</body>
</html>"""


def render_cover_page() -> None:
    """Render the cover as real HTML, then keep navigation as native Streamlit."""
    components.html(_cover_html(), height=790, scrolling=False)

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
