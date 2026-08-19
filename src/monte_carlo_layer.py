"""Layer 4 · Monte Carlo measurement, validation, and trust.

Layer 2 now explains why known-truth simulation is needed. Layer 4 owns the full
Monte Carlo sequence: the same five-step didactic flow that previously appeared in
Layer 2, followed by the thesis-specific risk summaries, validation stages and trust
safeguards. It never reruns the thesis GA.
"""

import streamlit as st
import streamlit.components.v1 as components

MONTE_CARLO_VIEWS = (
    "Measure repeated risk",
    "Why validate first?",
    "Validation stages",
    "Fairness & order of trust",
)


def _css() -> str:
    return """
    <style>
      *{box-sizing:border-box}
      body{margin:0;background:#081525;color:#e9f4ff;font-family:Arial,sans-serif}
      .page{padding:28px 32px 38px;background:#081525}
      .kicker{font-size:14px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin-bottom:9px}
      .title{font-size:38px;line-height:1.14;font-weight:900;color:#fff;margin-bottom:10px}
      .subtitle{font-size:19px;line-height:1.5;color:#bfd0e2;margin-bottom:25px;max-width:1280px}
      .section{font-size:21px;font-weight:900;color:#f3c743;letter-spacing:.05em;margin:30px 0 14px}
      .story{background:#0f2b47;border:1px solid #3c7198;border-left:7px solid #72cfff;border-radius:14px;padding:19px 21px;margin:17px 0;font-size:18px;line-height:1.5;color:#eef6ff}
      .takeaway{background:#12354a;border:1px solid #58aee8;border-left:7px solid #f3c743;border-radius:14px;padding:21px 23px;margin:24px 0 4px;font-size:20px;line-height:1.45;font-weight:850;color:#fff}
      .warn{background:#342b12;border:1px solid #f3c743;border-left:7px solid #f3c743;color:#fff2b8;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:20px 0}
      .danger{background:#351f20;border:1px solid #e66d4f;border-left:7px solid #e66d4f;color:#ffd6cc;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:18px 0}
      .good{background:#10372e;border:1px solid #54c786;border-left:7px solid #54c786;color:#d7ffe5;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:18px 0}
      .two{display:grid;grid-template-columns:1fr 1fr;gap:17px}
      .four{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
      .card{display:grid;grid-template-columns:96px 1fr;gap:20px;align-items:center;background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:15px;padding:21px 23px;margin-bottom:16px;min-height:150px}
      .icon{width:78px;height:78px;border-radius:19px;background:#10253a;border:1px solid #3c7198;display:flex;align-items:center;justify-content:center;font-size:39px;margin:auto}
      .label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:6px}
      .headline{font-size:25px;font-weight:900;line-height:1.18;color:#fff;margin-bottom:8px}
      .copy{font-size:17px;line-height:1.49;color:#dce9f8}
      .mini{font-size:15px;line-height:1.44;color:#b9c8d9;margin-top:8px}
      .formula-card{background:#0b2138;border:1px solid #356e99;border-left:6px solid #f3c743;border-radius:14px;padding:19px 21px;margin:15px 0}
      .formula-label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:7px}
      .formula{font-family:Georgia,serif;font-size:29px;font-weight:800;line-height:1.35;color:#f7d768;margin-bottom:9px}
      .formula-copy{font-size:17px;line-height:1.48;color:#dce9f8}
      .step{display:grid;grid-template-columns:66px 1fr;gap:17px;align-items:start;background:#0d2239;border:1px solid #356e99;border-radius:13px;padding:18px 19px;margin:10px 0}
      .stepno{width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#173a59;border:1px solid #72cfff;color:#72cfff;font-size:21px;font-weight:900}
      .step-title{font-size:21px;font-weight:900;color:#fff;margin-bottom:5px}
      .step-copy{font-size:17px;line-height:1.46;color:#dce9f8}
      .arrow{text-align:center;font-size:31px;color:#72cfff;font-weight:900;line-height:1;margin:3px 0}
      .connector{display:grid;grid-template-columns:1fr 72px 1fr;gap:14px;align-items:center;margin:19px 0}
      .connector-box{background:#10253a;border:1px solid #356e99;border-radius:13px;padding:18px;text-align:center;min-height:122px;display:flex;flex-direction:column;justify-content:center}
      .connector-box .ch{font-size:20px;font-weight:900;color:#fff;margin-bottom:6px}.connector-box .cc{font-size:15px;line-height:1.42;color:#dce9f8}.connector-arrow{text-align:center;font-size:32px;color:#72cfff;font-weight:900}
      .metricrow{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:17px 0 23px}
      .metric{background:#10253a;border:1px solid #356e99;border-radius:12px;padding:17px 12px;text-align:center}
      .metric .v{font-size:33px;font-weight:900;color:#f3c743;line-height:1.08}
      .metric .l{font-size:14px;color:#c4d3e3;margin-top:7px;font-weight:800}
      .check{display:grid;grid-template-columns:90px 1fr;gap:18px;align-items:center;background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:15px;padding:20px 22px;margin-bottom:15px}
      .check-icon{width:72px;height:72px;border-radius:18px;background:#10253a;border:1px solid #3c7198;display:flex;align-items:center;justify-content:center;font-size:36px}
      .check-title{font-size:23px;font-weight:900;color:#fff;margin-bottom:6px}
      .check-copy{font-size:16px;line-height:1.46;color:#dce9f8}
      .check-why{font-size:15px;line-height:1.42;color:#b9c8d9;margin-top:7px}
      .flow{display:flex;align-items:stretch;gap:9px;margin:17px 0;flex-wrap:wrap}
      .flowbox{flex:1;min-width:145px;background:#10253a;border:1px solid #356e99;border-radius:12px;padding:15px;text-align:center}
      .flowbox .ficon{font-size:30px;margin-bottom:7px}.flowbox .fh{font-size:17px;font-weight:900;color:#fff;margin-bottom:5px}.flowbox .fc{font-size:14px;line-height:1.37;color:#bfd0e2}
      .flowarrow{display:flex;align-items:center;justify-content:center;color:#72cfff;font-size:28px;font-weight:900}
      .guard{background:#0d2239;border:1px solid #356e99;border-radius:14px;padding:18px;min-height:185px;display:flex;flex-direction:column}
      .guard .gi{font-size:34px;margin-bottom:8px}.guard .gh{font-size:19px;font-weight:900;color:#fff;margin-bottom:7px}.guard .gc{font-size:15px;line-height:1.44;color:#dce9f8}.guard .why{margin-top:auto;padding-top:11px;border-top:1px solid #315879;font-size:13px;font-weight:900;letter-spacing:.06em;color:#72cfff}
      @media(max-width:1050px){.two,.four,.metricrow{grid-template-columns:1fr 1fr}.card{grid-template-columns:78px 1fr}.flowarrow{display:none}.connector{grid-template-columns:1fr}.connector-arrow{transform:rotate(90deg)}}
    </style>
    """


def _measurement() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>04 · MONTE CARLO · MEASURE REPEATED RISK</div>
      <div class='title'>How Monte Carlo turns known truth into estimator evidence.</div>
      <div class='subtitle'>This is now the single full explanation of the repeated-sampling engine. Layer 2 only establishes why known-truth simulation is needed.</div>

      <div class='section'>THE SAME FIVE STEPS, NOW IN THEIR FINAL HOME</div>
      <div class='step'><div class='stepno'>1</div><div><div class='step-title'>Choose one regime</div><div class='step-copy'>Fix the family, contamination conditions and sample size.</div></div></div><div class='arrow'>↓</div>
      <div class='step'><div class='stepno'>2</div><div><div class='step-title'>Generate one synthetic sample</div><div class='step-copy'>Draw observations from the chosen regime.</div></div></div><div class='arrow'>↓</div>
      <div class='step'><div class='stepno'>3</div><div><div class='step-title'>Apply every estimator to the same sample</div><div class='step-copy'>This keeps the comparison fair inside that replicate.</div></div></div><div class='arrow'>↓</div>
      <div class='step'><div class='stepno'>4</div><div><div class='step-title'>Compare every estimate with known θ</div><div class='step-copy'>Squared error measures how far each estimator is from the same population mean.</div></div></div><div class='arrow'>↓</div>
      <div class='step'><div class='stepno'>5</div><div><div class='step-title'>Repeat many times</div><div class='step-copy'>Repeated errors become average risk and difficult-case risk.</div></div></div>

      <div class='section'>WHAT LAYER 4 ADDS</div>
      <div class='connector'>
        <div class='connector-box'><div class='ch'>Repeated replicate losses</div><div class='cc'>For every estimator Tⱼ and replicate r, compare the estimate with the same known θ.</div></div>
        <div class='connector-arrow'>→</div>
        <div class='connector-box'><div class='ch'>Risk summaries</div><div class='cc'>Aggregate those repeated losses into mean MSE and q95.</div></div>
      </div>

      <div class='formula-card'><div class='formula-label'>REPLICATE-LEVEL LOSS</div><div class='formula'>(Tⱼ(x⁽ʳ⁾) − θ)²</div><div class='formula-copy'>Every estimator is put on the same loss scale because every estimate is compared with the same known population mean.</div></div>
      <div class='formula-card'><div class='formula-label'>MONTE CARLO SUMMARY</div><div class='formula'>MSE ≈ (1/B) Σᵣ (Tⱼ(x⁽ʳ⁾) − θ)² &nbsp;&nbsp; · &nbsp;&nbsp; q95 = Q₀.₉₅[(Tⱼ−θ)²]</div><div class='formula-copy'>MSE summarizes average squared error. q95 summarizes the difficult upper-tail part of the error distribution.</div></div>

      <div class='story'><b>Important connection:</b> Step 3 gives every estimator the same sample path; Step 4 puts them on the same known-truth loss scale; Step 5 creates the repeated error distribution summarized by MSE and q95.</div>
      <div class='takeaway'>TAKE-HOME: choose one regime → generate a sample → apply every estimator → compare with known θ → repeat → summarize risk.</div>
    </div>"""


def _why_validate() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>04 · VALIDATION · WHY VALIDATE FIRST?</div>
      <div class='title'>A search result is only meaningful if the world being searched is trustworthy.</div>
      <div class='subtitle'>The simulator is audited before the GA evidence is interpreted. The algorithm is not allowed to validate its own environment.</div>

      <div class='two'>
        <div class='card'><div class='icon'>⚠️</div><div><div class='label'>IF VALIDATION IS SKIPPED</div><div class='headline'>A strong search result can be misleading</div><div class='copy'>A GA could optimize perfectly inside a generator with the wrong mean, the wrong contamination severity or an unrealistic regime label.</div></div></div>
        <div class='card'><div class='icon'>🛡️</div><div><div class='label'>INDEPENDENT VALIDATION FIRST</div><div class='headline'>The world must pass before search matters</div><div class='copy'>The data-generating process is checked against analytic moments, contamination design, known statistical behaviour and empirical structure.</div></div></div>
      </div>

      <div class='section'>THE ORDER IS DELIBERATE</div>
      <div class='flow'><div class='flowbox'><div class='ficon'>🌍</div><div class='fh'>Build world</div><div class='fc'>Define regime and target.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>✅</div><div class='fh'>Validate world</div><div class='fc'>Check generator behaviour.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>📉</div><div class='fh'>Measure risk</div><div class='fc'>Estimate MSE and q95.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>🧬</div><div class='fh'>Run search</div><div class='fc'>Only now interpret GA candidates.</div></div></div>

      <div class='danger'><b>What the design avoids:</b> “the GA found a winner, therefore the simulator must be good.” That would be circular evidence.</div>
      <div class='good'><b>What the design does instead:</b> validate the simulator independently, then let search and held-out evidence succeed or fail inside that certified world.</div>

      <div class='takeaway'>TAKE-HOME: the simulator earns trust before the GA is allowed to support a scientific claim.</div>
    </div>"""


def _validation_stages() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>04 · VALIDATION · FOUR STAGES</div>
      <div class='title'>What exactly was checked before search evidence was trusted?</div>
      <div class='subtitle'>The validation battery tests the generator from analytic truth to empirical relevance.</div>

      <div class='metricrow'><div class='metric'><div class='v'>125</div><div class='l'>validation conditions</div></div><div class='metric'><div class='v' style='color:#54c786'>0</div><div class='l'>hard failures</div></div><div class='metric'><div class='v'>29</div><div class='l'>warnings retained</div></div><div class='metric'><div class='v'>0.976%</div><div class='l'>maximum mean error</div></div></div>

      <div class='check'><div class='check-icon'>🎯</div><div><div class='label'>1 · MOMENT FIDELITY</div><div class='check-title'>Do large generated populations recover their analytic moments?</div><div class='check-copy'>Representative parameter-grid rows were checked with large synthetic draws. The empirical mean stayed within the hard 1% tolerance; maximum relative mean error was 0.976%.</div><div class='check-why'><b>Why it matters:</b> if θ is wrong here, every later squared-error calculation is wrong.</div></div></div>

      <div class='check'><div class='check-icon'>🧫</div><div><div class='label'>2 · CONTAMINATION FIDELITY</div><div class='check-title'>Does injection produce the designed rate and severity?</div><div class='check-copy'>Realised contamination rate and robust MAD-based outlier scale are checked after injection.</div><div class='check-why'><b>Why it matters:</b> a regime labelled “10% upper-tail contamination” must actually behave like one before it enters Monte Carlo.</div></div></div>

      <div class='check'><div class='check-icon'>📐</div><div><div class='label'>3 · STATISTICAL SANITY</div><div class='check-title'>Does the engine recover known robust-statistics behaviour?</div><div class='check-copy'>Under clean Normal data, the expected textbook ordering reappears: the sample mean should outperform the median in MSE.</div><div class='check-why'><b>Why it matters:</b> the simulator is checked against known theory before it is used to discover anything new.</div></div></div>

      <div class='check'><div class='check-icon'>🌐</div><div><div class='label'>4 · EMPIRICAL ANCHORING</div><div class='check-title'>Does the synthetic grid cover relevant real-data shapes?</div><div class='check-copy'>Shape diagnostics from five public datasets were compared with matched synthetic coverage. This is calibration, not known-θ validation.</div><div class='check-why'><b>Why it matters:</b> the synthetic study stays connected to empirical structure without pretending real-data population truth is known.</div></div></div>

      <div class='warn'><b>29 warnings do not mean 29 failures.</b> Warnings are retained diagnostic cases. Hard failures are counted separately, and there were zero.</div>
      <div class='takeaway'>TAKE-HOME: population truth → contamination design → theory sanity → empirical anchoring. Trust is built in stages.</div>
    </div>"""


def _fairness() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>04 · VALIDATION · FAIRNESS & ORDER OF TRUST</div>
      <div class='title'>The pipeline is designed so that no single stage can certify itself.</div>
      <div class='subtitle'>These safeguards separate data generation, risk measurement, search and final acceptance.</div>

      <div class='four'>
        <div class='guard'><div class='gi'>🎯</div><div class='gh'>Known target first</div><div class='gc'>θ comes from the generating distribution before any estimator or GA candidate is evaluated.</div><div class='why'>PREVENTS TARGET DRIFT</div></div>
        <div class='guard'><div class='gi'>⚖️</div><div class='gh'>Common sample paths</div><div class='gc'>Inside each replicate, every estimator receives the same generated sample.</div><div class='why'>FAIR COMPARISON</div></div>
        <div class='guard'><div class='gi'>🔁</div><div class='gh'>Fixed seeds & logged regimes</div><div class='gc'>Sampling conditions are reproducible and auditable instead of reconstructed later.</div><div class='why'>REPRODUCIBILITY</div></div>
        <div class='guard'><div class='gi'>📝</div><div class='gh'>Warnings are retained</div><div class='gc'>Diagnostic edge cases remain visible rather than being silently removed from the validation record.</div><div class='why'>TRANSPARENCY</div></div>
      </div>

      <div class='section'>ORDER OF TRUST ACROSS THE THESIS</div>
      <div class='flow'><div class='flowbox'><div class='ficon'>🌍</div><div class='fh'>1 · Build</div><div class='fc'>Define the controlled world.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>✅</div><div class='fh'>2 · Validate</div><div class='fc'>Audit the generator.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>📊</div><div class='fh'>3 · Measure</div><div class='fc'>Estimate repeated-sampling risk.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>🧬</div><div class='fh'>4 · Search</div><div class='fc'>Propose a candidate.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>🧊</div><div class='fh'>5 · Freeze</div><div class='fc'>Lock the recipe.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>🚪</div><div class='fh'>6 · Gate</div><div class='fc'>Independent evidence controls the claim.</div></div></div>

      <div class='story'><b>The key separation:</b> simulator validation answers “is the world credible?” Monte Carlo answers “what is the risk?” GA search answers “where is opportunity?” Frozen validation answers “is replacement supported?”</div>
      <div class='takeaway'>TAKE-HOME: build → validate → measure → search → freeze → gate. Each stage has a different job, and that separation is part of the thesis contribution.</div>
    </div>"""


def _set_view(index: int) -> None:
    st.session_state.monte_carlo_didactic_view = index


def render_monte_carlo_layer() -> None:
    st.markdown("""
    <style>
      .mc-didactic-nav .stButton>button{min-height:4.2rem!important;padding:.7rem .55rem!important;font-size:1.02rem!important;line-height:1.15!important;font-weight:850!important;white-space:normal!important}
    </style>
    """, unsafe_allow_html=True)

    if "monte_carlo_didactic_view" not in st.session_state:
        st.session_state.monte_carlo_didactic_view = 0
    st.session_state.monte_carlo_didactic_view = max(0, min(int(st.session_state.monte_carlo_didactic_view), 3))

    st.markdown("<div class='layer-heading'>Monte Carlo measurement & validation: how the evidence earns trust</div>", unsafe_allow_html=True)
    st.caption("From repeated-sampling risk to simulator certification and anti-leakage safeguards.")
    st.markdown('<div class="mc-didactic-nav">', unsafe_allow_html=True)
    cols = st.columns(4, gap="small")
    for i, label in enumerate(MONTE_CARLO_VIEWS):
        with cols[i]:
            st.button(label, key=f"mc_didactic_{i}", use_container_width=True,
                      type="primary" if i == st.session_state.monte_carlo_didactic_view else "secondary",
                      on_click=_set_view, args=(i,))
    st.markdown('</div>', unsafe_allow_html=True)

    docs = (_measurement, _why_validate, _validation_stages, _fairness)
    heights = (2150, 1500, 2300, 1650)
    view = st.session_state.monte_carlo_didactic_view
    components.html(docs[view](), height=heights[view], scrolling=False)
