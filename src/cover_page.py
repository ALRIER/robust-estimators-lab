"""Full-width cinematic cover for the thesis defense.

The cover follows the original visual concept: large academic title hierarchy,
centered author/institution identity, and one continuous illustrated journey from
Question & Objective to the final result taxonomy.  A small parent-page CSS hook
expands the historical cover column so the modular cover uses the full audience
canvas instead of being trapped inside the old logo column.
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


def _host_layout_css() -> None:
    """Make the legacy cover column occupy the full Streamlit content row."""
    st.markdown(
        """
        <div id="defense-cover-host-marker"></div>
        <style>
          [data-testid="stHorizontalBlock"]:has(#defense-cover-host-marker){
            display:block!important;width:100%!important;max-width:none!important;
          }
          [data-testid="stHorizontalBlock"]:has(#defense-cover-host-marker) > [data-testid="stColumn"]{
            width:100%!important;max-width:none!important;flex:1 1 100%!important;
          }
          [data-testid="stHorizontalBlock"]:has(#defense-cover-host-marker) > [data-testid="stColumn"]:not(:has(#defense-cover-host-marker)){
            display:none!important;
          }
          [data-testid="stColumn"]:has(#defense-cover-host-marker){
            width:100%!important;max-width:none!important;flex:1 1 100%!important;
          }
          [data-testid="stColumn"]:has(#defense-cover-host-marker) iframe{
            width:100%!important;max-width:none!important;
          }
          .block-container:has(#defense-cover-host-marker){
            max-width:none!important;padding-left:.7rem!important;padding-right:.7rem!important;
          }
          #defense-cover-host-marker{display:none}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _cover_html() -> str:
    """Build the 16:9-style audience cover as one self-contained HTML document."""
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:#06111f;color:#eef6ff;font-family:Arial,sans-serif;overflow:hidden}}
.canvas{{position:relative;width:100%;height:850px;overflow:hidden;background:
  radial-gradient(circle at 50% 29%,rgba(28,75,126,.58),transparent 41%),
  radial-gradient(circle at 89% 13%,rgba(30,98,158,.24),transparent 28%),
  radial-gradient(circle at 8% 61%,rgba(18,78,126,.15),transparent 29%),
  linear-gradient(180deg,#041020 0%,#07182c 51%,#061321 100%);
  border:1px solid #214f78;border-radius:20px;box-shadow:0 24px 70px rgba(0,0,0,.28)}}
.canvas:before{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.72;background-image:
  radial-gradient(circle at 5% 48%,#145b91 0 2px,transparent 2.5px),
  radial-gradient(circle at 8% 56%,#145b91 0 2px,transparent 2.5px),
  radial-gradient(circle at 12% 65%,#145b91 0 2px,transparent 2.5px),
  radial-gradient(circle at 84% 10%,#145b91 0 2px,transparent 2.5px),
  radial-gradient(circle at 89% 16%,#145b91 0 2px,transparent 2.5px),
  radial-gradient(circle at 94% 24%,#145b91 0 2px,transparent 2.5px),
  radial-gradient(circle at 82% 31%,#145b91 0 2px,transparent 2.5px)}}
.net-right,.net-left{{position:absolute;pointer-events:none;opacity:.22;background:
  linear-gradient(32deg,transparent 48%,#2470a6 49%,#2470a6 50%,transparent 51%),
  linear-gradient(151deg,transparent 48%,#2470a6 49%,#2470a6 50%,transparent 51%),
  linear-gradient(83deg,transparent 49%,#2470a6 49.5%,#2470a6 50%,transparent 50.5%)}}
.net-right{{right:-25px;top:26px;width:350px;height:315px;transform:rotate(7deg)}}
.net-left{{left:-90px;top:390px;width:330px;height:250px;transform:rotate(-13deg);opacity:.13}}
.top{{position:relative;z-index:4;text-align:center;padding:24px 55px 0}}
.kicker{{font-size:15px;font-weight:900;letter-spacing:.17em;color:#ffbd2e;margin-bottom:9px}}
.title{{font-family:Georgia,serif;font-size:58px;line-height:1.02;font-weight:800;color:#fff;letter-spacing:.005em;text-transform:uppercase;text-shadow:0 0 28px rgba(86,174,239,.12)}}
.title2{{font-family:Georgia,serif;font-size:34px;line-height:1.12;font-weight:800;color:#f6f8fb;max-width:1250px;margin:4px auto 0}}
.rule{{display:flex;align-items:center;gap:16px;max-width:690px;margin:16px auto 12px}}
.rule span{{height:1px;flex:1;background:linear-gradient(90deg,transparent,#d89e25)}}
.rule span:last-child{{background:linear-gradient(90deg,#d89e25,transparent)}}
.diamond{{width:12px;height:12px;background:#ffbd2e;border:2px solid #ffd15a;transform:rotate(45deg)}}
.tagline{{font-size:18px;line-height:1.4;color:#ffbd2e;font-style:italic;max-width:1040px;margin:0 auto}}
.identity{{position:relative;z-index:4;text-align:center;margin-top:15px}}
.name{{font-size:31px;font-weight:900;color:#fff;letter-spacing:.01em}}
.program{{font-size:15px;font-weight:850;letter-spacing:.10em;color:#8fcfff;margin-top:3px}}
.uni-row{{display:flex;align-items:center;justify-content:center;gap:17px;margin-top:9px}}
.uni-row img{{width:205px;max-height:76px;object-fit:contain;background:#fff;padding:5px;border-radius:6px}}
.supervisor{{text-align:left;border-left:1px solid #376789;padding-left:17px}}
.supervisor .lab{{font-size:10px;font-weight:900;letter-spacing:.13em;color:#8fcfff;margin-bottom:4px}}
.supervisor .value{{font-size:15px;font-weight:850;color:#eef6ff}}
.arc{{position:absolute;z-index:1;left:-95px;right:-95px;top:486px;height:125px;border-top:2px solid #3893d7;border-radius:50% 50% 0 0/100% 100% 0 0;transform:rotate(-1.5deg);opacity:.95}}
.path-label{{position:absolute;z-index:4;left:0;right:0;top:505px;text-align:center;font-size:10px;font-weight:900;letter-spacing:.14em;color:#8fcfff}}
.path{{position:absolute;z-index:4;left:20px;right:20px;top:526px;display:grid;grid-template-columns:1.08fr 34px 1.12fr 34px 1.10fr 34px 1.15fr 34px 1.08fr;align-items:start;gap:2px}}
.stage{{height:220px;padding:11px 11px 9px;text-align:center;border-left:1px solid rgba(72,130,173,.36);display:flex;flex-direction:column;justify-content:flex-start}}
.stage:first-child{{border-left:0}}
.icon{{height:56px;display:flex;align-items:center;justify-content:center;margin-bottom:4px}}
.bulb{{position:relative;width:38px;height:38px;border-radius:50%;border:2px solid #f3c743;display:flex;align-items:center;justify-content:center;color:#f3c743;font-size:20px;box-shadow:0 0 18px rgba(243,199,67,.18)}}
.bulb:after{{content:"";position:absolute;width:12px;height:7px;border:2px solid #f3c743;border-top:0;bottom:-8px;border-radius:0 0 4px 4px}}
.dist{{position:relative;width:150px;height:52px;margin:auto}}
.dist:before{{content:"";position:absolute;left:4px;right:4px;bottom:4px;height:44px;background:linear-gradient(180deg,rgba(64,166,238,.04),rgba(64,166,238,.26));clip-path:polygon(0 100%,7% 96%,15% 85%,24% 60%,34% 28%,44% 8%,50% 2%,56% 8%,66% 28%,76% 60%,85% 85%,93% 96%,100% 100%)}}
.dist:after{{content:"";position:absolute;left:75px;top:0;bottom:0;border-left:2px dashed #b9dcf6}}
.ga-icon{{font-size:41px;color:#a777e3;line-height:1;text-shadow:0 0 16px rgba(167,119,227,.22)}}
.trophy{{font-size:42px;color:#ffbd2e;line-height:1;text-shadow:0 0 16px rgba(255,189,46,.20)}}
.scatter{{position:relative;width:152px;height:54px;margin:auto;border-left:1px solid #d6e6f5;border-bottom:1px solid #d6e6f5}}
.scatter i{{position:absolute;width:7px;height:7px;border-radius:50%}}
.scatter .b1{{left:20px;bottom:13px;background:#3aa5ef}}.scatter .b2{{left:38px;bottom:29px;background:#3aa5ef}}.scatter .b3{{left:55px;bottom:18px;background:#8f63da}}.scatter .b4{{left:74px;bottom:35px;background:#8f63da}}.scatter .b5{{left:98px;bottom:22px;background:#ffbd2e}}.scatter .b6{{left:116px;bottom:38px;background:#ffbd2e}}.scatter .b7{{left:128px;bottom:15px;background:#ffbd2e}}
.stage-num{{font-size:9px;font-weight:900;letter-spacing:.11em;color:#8ca8bd;margin-bottom:3px}}
.stage-head{{font-size:19px;line-height:1.1;font-weight:900;margin-bottom:6px}}
.s1 .stage-head{{color:#f3c743}}.s2 .stage-head{{color:#55b5f3}}.s3 .stage-head{{color:#a777e3}}.s4 .stage-head{{color:#ffbd2e}}.s5 .stage-head{{color:#72cfff}}
.stage-copy{{font-size:12.5px;line-height:1.38;color:#dce8f4;max-width:215px;margin:0 auto}}
.arrow{{font-size:31px;font-weight:900;color:#6dc5ff;text-align:center;margin-top:42px}}
.outcomes{{display:flex;justify-content:center;gap:7px;margin-top:8px}}
.pill{{padding:4px 8px;border-radius:12px;font-size:9.5px;font-weight:900;white-space:nowrap}}
.replace{{border:1px solid #ffbd2e;color:#ffbd2e;background:rgba(255,189,46,.08)}}
.retain{{border:1px solid #55b5f3;color:#72cfff;background:rgba(85,181,243,.08)}}
.footer{{position:absolute;z-index:5;left:0;right:0;bottom:0;height:84px;border-top:1px solid #2e5978;background:rgba(5,18,33,.94);display:grid;grid-template-columns:.8fr 1.3fr 1.1fr 1.45fr;align-items:center}}
.foot{{height:58px;padding:8px 20px;display:flex;align-items:center;justify-content:center;gap:11px;border-left:1px solid #2b536f;color:#d9e7f3}}
.foot:first-child{{border-left:0}}
.foot-icon{{font-size:25px;color:#91a8bc}}
.foot-copy{{font-size:12.5px;line-height:1.35}}
.foot-copy b{{display:block;font-size:11px;letter-spacing:.06em;color:#fff;margin-bottom:2px}}
@media(max-width:1350px){{.title{{font-size:50px}}.title2{{font-size:30px}}.stage-head{{font-size:17px}}.stage-copy{{font-size:11.5px}}.path{{grid-template-columns:1fr 26px 1fr 26px 1fr 26px 1fr 26px 1fr}}}}
</style>
</head>
<body>
<div class="canvas">
  <div class="net-right"></div><div class="net-left"></div>
  <div class="top">
    <div class="kicker">MASTER'S THESIS DEFENSE</div>
    <div class="title">Building Better Estimators</div>
    <div class="title2">An Interpretable GA Framework for Conditional Estimator Discovery and Validation</div>
    <div class="rule"><span></span><div class="diamond"></div><span></span></div>
    <div class="tagline">A staged study of estimator discovery, validation, and evidence control under simulated and external data regimes.</div>
  </div>

  <div class="identity">
    <div class="name">Álvaro Rivera-Eraso</div>
    <div class="program">MSc ARTIFICIAL INTELLIGENCE</div>
    <div class="uni-row">
      <img src="{_LOGO}" alt="University of Hull">
      <div class="supervisor"><div class="lab">SUPERVISOR</div><div class="value">Debarati Chakraborty, Ph.D.</div></div>
    </div>
  </div>

  <div class="arc"></div>
  <div class="path-label">FROM QUESTION TO EVIDENCE · THE STUDY AT A GLANCE</div>
  <div class="path">
    <div class="stage s1">
      <div class="icon"><div class="bulb">✦</div></div>
      <div class="stage-num">01 · FRAMING</div>
      <div class="stage-head">Question &amp; Objective</div>
      <div class="stage-copy">What problem are we solving, what stays fixed, and what must the study establish?</div>
    </div>
    <div class="arrow">›</div>

    <div class="stage s2">
      <div class="icon"><div class="dist"></div></div>
      <div class="stage-num">02 · CONTROLLED TRUTH</div>
      <div class="stage-head">Monte Carlo World</div>
      <div class="stage-copy">Controlled regimes, known population target θ, repeated sampling, and measurable finite-sample risk.</div>
    </div>
    <div class="arrow">›</div>

    <div class="stage s3">
      <div class="icon ga-icon">⌬</div>
      <div class="stage-num">03 · SEARCH</div>
      <div class="stage-head">GA Search Design</div>
      <div class="stage-copy">Simplex mixtures, evolutionary search, candidate discovery, and frozen interpretable weights.</div>
    </div>
    <div class="arrow">›</div>

    <div class="stage s4">
      <div class="icon trophy">♛</div>
      <div class="stage-num">04 · CHALLENGE</div>
      <div class="stage-head">Tournament of Evidence</div>
      <div class="stage-copy">Staged validation, stronger benchmarks, transfer checks, and explicit benchmark retention.</div>
    </div>
    <div class="arrow">›</div>

    <div class="stage s5">
      <div class="icon"><div class="scatter"><i class="b1"></i><i class="b2"></i><i class="b3"></i><i class="b4"></i><i class="b5"></i><i class="b6"></i><i class="b7"></i></div></div>
      <div class="stage-num">05 · INTERPRETATION</div>
      <div class="stage-head">Results &amp; Taxonomy</div>
      <div class="stage-copy">Classify the evidence: supported specialists, transfer signals, near-gate cases, and retained benchmarks.</div>
      <div class="outcomes"><span class="pill replace">SUPPORTED</span><span class="pill retain">RETAINED</span></div>
    </div>
  </div>

  <div class="footer">
    <div class="foot"><div class="foot-icon">▣</div><div class="foot-copy"><b>AUGUST 2026</b>Master's Thesis Defense</div></div>
    <div class="foot"><div class="foot-icon">♙</div><div class="foot-copy"><b>SUPERVISOR</b>Debarati Chakraborty, Ph.D.</div></div>
    <div class="foot"><div class="foot-icon">⚗</div><div class="foot-copy"><b>RESEARCH LAB</b>Robust Estimators Lab</div></div>
    <div class="foot"><div class="foot-icon">◎</div><div class="foot-copy"><b>PUBLIC APP</b>robust-estimators-lab.streamlit.app</div></div>
  </div>
</div>
</body>
</html>"""


def render_cover_page() -> None:
    """Render the cinematic cover and keep navigation as native Streamlit."""
    _host_layout_css()
    components.html(_cover_html(), height=870, scrolling=False)

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
