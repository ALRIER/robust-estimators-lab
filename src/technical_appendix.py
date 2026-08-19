"""Layer 9 · Technical drill-down.

This is the single current implementation of the defense appendix. It is designed
for live committee Q&A: large text, visual explanations, simple diagrams, and
scrollable depth. It never reruns the thesis GA and never creates new evidence.
"""

from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
BG = "#081525"
TEXT = "#e9f4ff"
BLUE = "#58aee8"
CYAN = "#72cfff"
GOLD = "#f3c743"
GREEN = "#54c786"
RED = "#e66d4f"
PURPLE = "#a777e3"
MUTED = "#526a85"

APPENDIX_LABELS = (
    "A · Simulation", "B · Validity", "C · GA mechanics",
    "D · Metrics & gate", "E · Results", "F · Q&A",
)


def _css() -> str:
    return """
    <style>
      *{box-sizing:border-box}
      body{margin:0;background:#081525;color:#e9f4ff;font-family:Arial,sans-serif}
      .page{padding:26px 30px 34px;background:#081525}
      .kicker{font-size:14px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin-bottom:9px}
      .title{font-size:36px;line-height:1.14;font-weight:900;color:#fff;margin-bottom:10px}
      .subtitle{font-size:18px;line-height:1.48;color:#bfd0e2;margin-bottom:24px;max-width:1250px}
      .section-title{font-size:21px;font-weight:900;color:#f3c743;letter-spacing:.06em;margin:28px 0 14px}
      .story{background:#0f2b47;border:1px solid #3c7198;border-left:7px solid #72cfff;border-radius:14px;padding:18px 20px;margin:16px 0;font-size:17px;line-height:1.5;color:#eef6ff}
      .takeaway{background:#12354a;border:1px solid #58aee8;border-left:7px solid #f3c743;border-radius:14px;padding:20px 22px;margin:22px 0 2px;font-size:19px;line-height:1.45;font-weight:800;color:#fff}
      .warn{background:#342b12;border:1px solid #f3c743;border-left:7px solid #f3c743;color:#fff2b8;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:20px 0}
      .danger{background:#351f20;border:1px solid #e66d4f;border-left:7px solid #e66d4f;color:#ffd6cc;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:18px 0}
      .good{background:#10372e;border:1px solid #54c786;border-left:7px solid #54c786;color:#d7ffe5;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:18px 0}
      .card{display:grid;grid-template-columns:94px 1fr;gap:20px;align-items:center;background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:15px;padding:20px 22px;margin-bottom:16px;min-height:150px}
      .icon{width:76px;height:76px;border-radius:18px;background:#10253a;border:1px solid #3c7198;display:flex;align-items:center;justify-content:center;font-size:38px;margin:auto}
      .label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:6px}
      .headline{font-size:25px;font-weight:900;line-height:1.18;color:#fff;margin-bottom:7px}
      .copy{font-size:17px;line-height:1.48;color:#dce9f8}
      .mini{font-size:15px;line-height:1.44;color:#b9c8d9;margin-top:7px}
      .formula-card{background:#0b2138;border:1px solid #356e99;border-left:6px solid #f3c743;border-radius:14px;padding:18px 20px;margin:14px 0}
      .formula-label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:7px}
      .formula{font-family:Georgia,serif;font-size:29px;font-weight:800;line-height:1.35;color:#f7d768;margin-bottom:8px}
      .formula-copy{font-size:16px;line-height:1.48;color:#dce9f8}
      .metricrow{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:16px 0 22px}
      .metric{background:#10253a;border:1px solid #356e99;border-radius:12px;padding:16px 12px;text-align:center}
      .metric .v{font-size:31px;font-weight:900;color:#f3c743;line-height:1.1}
      .metric .l{font-size:14px;color:#c4d3e3;margin-top:7px;font-weight:800}
      .step{display:grid;grid-template-columns:64px 1fr;gap:16px;align-items:start;background:#0d2239;border:1px solid #356e99;border-radius:13px;padding:17px 18px;margin:10px 0}
      .stepno{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#173a59;border:1px solid #72cfff;color:#72cfff;font-size:20px;font-weight:900}
      .step-title{font-size:20px;font-weight:900;color:#fff;margin-bottom:5px}
      .step-copy{font-size:16px;line-height:1.46;color:#dce9f8}
      .arrow-down{text-align:center;font-size:29px;color:#72cfff;font-weight:900;line-height:1;margin:2px 0}
      .builder{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;align-items:stretch;margin:16px 0}
      .builder-box{background:#10253a;border:1px solid #356e99;border-radius:11px;padding:13px 9px;text-align:center;min-height:105px;display:flex;flex-direction:column;justify-content:center}
      .builder-box b{font-size:17px;color:#fff;margin-bottom:5px}.builder-box span{font-size:13px;color:#bfd0e2;line-height:1.35}
      .builder-box.result{border-color:#54c786;background:#10372e}
      .two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
      .three{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
      .four{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
      .small-card{background:#10253a;border:1px solid #356e99;border-radius:12px;padding:16px;min-height:120px}
      .small-card .n{font-size:27px;font-weight:900;color:#f3c743;margin-bottom:5px}.small-card .h{font-size:16px;font-weight:900;color:#fff;margin-bottom:5px}.small-card .c{font-size:14px;line-height:1.42;color:#dce9f8}
      .flow{display:flex;align-items:stretch;gap:9px;margin:16px 0;flex-wrap:wrap}
      .flowbox{flex:1;min-width:150px;background:#10253a;border:1px solid #356e99;border-radius:12px;padding:14px;text-align:center}
      .flowbox .ficon{font-size:28px;margin-bottom:7px}.flowbox .fh{font-size:16px;font-weight:900;color:#fff;margin-bottom:5px}.flowbox .fc{font-size:13px;line-height:1.36;color:#bfd0e2}
      .flowarrow{display:flex;align-items:center;justify-content:center;color:#72cfff;font-size:26px;font-weight:900}
      .gate{display:grid;grid-template-columns:1fr 100px 1fr;gap:14px;align-items:center;margin:18px 0}
      .gatebox{background:#10253a;border:1px solid #356e99;border-radius:14px;padding:19px;text-align:center}
      .gatebox.pass{border-color:#54c786;background:#10372e}.gatebox.fail{border-color:#e66d4f;background:#351f20}
      .gatebox .gh{font-size:21px;font-weight:900;color:#fff;margin-bottom:6px}.gatebox .gc{font-size:15px;line-height:1.42;color:#dce9f8}
      .gate-mid{text-align:center;color:#72cfff;font-size:18px;font-weight:900;line-height:1.3}
      .pillrow{display:flex;gap:9px;flex-wrap:wrap;margin:12px 0}.pill{background:#10253a;border:1px solid #356e99;border-radius:20px;padding:8px 12px;font-size:14px;font-weight:800;color:#e6f1fb}
      .evidence-step{display:grid;grid-template-columns:110px 1fr;gap:18px;align-items:center;background:#0d2239;border:1px solid #356e99;border-radius:14px;padding:18px 20px;margin:10px 0}
      .evidence-num{font-size:34px;font-weight:900;color:#f3c743;text-align:center}.evidence-title{font-size:20px;font-weight:900;color:#fff;margin-bottom:5px}.evidence-copy{font-size:16px;line-height:1.45;color:#dce9f8}
      .split-result{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px}
      .pass-panel,.fail-panel{border-radius:12px;padding:16px 17px}.pass-panel{background:#10372e;border:1px solid #54c786}.fail-panel{background:#351f20;border:1px solid #e66d4f}
      .result-title{font-size:18px;font-weight:900;color:#fff;margin-bottom:7px}.result-value{font-size:25px;font-weight:900;margin-bottom:5px}.pass-panel .result-value{color:#54c786}.fail-panel .result-value{color:#ff8669}.result-copy{font-size:14px;line-height:1.4;color:#e7eef7}
      .qa{background:#0b2138;border:1px solid #356e99;border-radius:14px;padding:18px 20px;margin-bottom:14px}
      .q{font-size:19px;font-weight:900;color:#72cfff;margin-bottom:7px}.a{font-size:17px;line-height:1.48;color:#edf5ff}.more{font-size:14px;line-height:1.44;color:#b9c8d9;margin-top:8px;border-top:1px solid #284c6b;padding-top:8px}
      @media(max-width:1050px){.metricrow,.four,.three,.two,.builder{grid-template-columns:1fr 1fr}.gate{grid-template-columns:1fr}.gate-mid{padding:6px}.card{grid-template-columns:74px 1fr}.flowarrow{display:none}}
    </style>
    """


def _a_simulation() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>APPENDIX A · SIMULATION</div>
      <div class='title'>Why simulate at all?</div>
      <div class='subtitle'>This page answers one question: why is Monte Carlo necessary for a thesis about estimator accuracy?</div>

      <div class='two'>
        <div class='card'><div class='icon'>🌍</div><div><div class='label'>REAL DATA</div><div class='headline'>The true population mean is hidden</div><div class='copy'>In a real dataset, we observe a sample. We do not directly observe the true population mean θ.</div></div></div>
        <div class='card'><div class='icon'>🧪</div><div><div class='label'>SIMULATION</div><div class='headline'>The truth is defined before scoring</div><div class='copy'>A synthetic generating law gives us θ = E[X]. We can then measure estimator error directly.</div></div></div>
      </div>
      <div class='story'><b>Simple idea:</b> simulation is not used because real data are unimportant. It is used because known truth is needed to measure estimation error correctly.</div>

      <div class='section-title'>1 · WHAT STAYS FIXED?</div>
      <div class='formula-card'><div class='formula-label'>TARGET</div><div class='formula'>θ(F) = μ<sub>F</sub> = E<sub>F</sub>[X]</div><div class='formula-copy'>The target is the population mean. The regime can change, but every estimator is still judged as an estimator of the mean.</div></div>

      <div class='section-title'>2 · WHAT MAKES ONE REGIME?</div>
      <div class='builder'>
        <div class='builder-box'><b>F₀</b><span>distribution family</span></div>
        <div class='builder-box'><b>γ</b><span>contamination rate</span></div>
        <div class='builder-box'><b>c</b><span>outlier scale</span></div>
        <div class='builder-box'><b>m</b><span>mechanism</span></div>
        <div class='builder-box'><b>n</b><span>sample size</span></div>
        <div class='builder-box result'><b>ℛ</b><span>one complete regime</span></div>
      </div>
      <div class='formula-card'><div class='formula-label'>INDUCED DISTRIBUTION</div><div class='formula'>F<sub>ℛ</sub> = (1−γ)F₀ + γG<sub>m,c</sub>(F₀)</div><div class='formula-copy'>This notation separates the clean baseline from the controlled contamination process.</div></div>

      <div class='section-title'>3 · HOW LARGE IS THE CONTROLLED WORLD?</div>
      <div class='metricrow'><div class='metric'><div class='v'>6</div><div class='l'>distribution families</div></div><div class='metric'><div class='v'>5</div><div class='l'>sample sizes</div></div><div class='metric'><div class='v'>576</div><div class='l'>profiles per family</div></div><div class='metric'><div class='v'>2,880</div><div class='l'>regimes per family</div></div></div>
      <div class='pillrow'><span class='pill'>Normal</span><span class='pill'>Lognormal</span><span class='pill'>Weibull</span><span class='pill'>Inverse Gaussian</span><span class='pill'>Ex-Gaussian</span><span class='pill'>Ex-Wald</span></div>

      <div class='section-title'>4 · WHAT DOES MONTE CARLO DO?</div>
      <div class='step'><div class='stepno'>1</div><div><div class='step-title'>Choose one regime</div><div class='step-copy'>Fix family, contamination, mechanism, scale and sample size.</div></div></div><div class='arrow-down'>↓</div>
      <div class='step'><div class='stepno'>2</div><div><div class='step-title'>Generate one sample</div><div class='step-copy'>Draw X₁,…,Xₙ from that regime.</div></div></div><div class='arrow-down'>↓</div>
      <div class='step'><div class='stepno'>3</div><div><div class='step-title'>Apply every estimator to the same sample</div><div class='step-copy'>This keeps the comparison fair inside each replicate.</div></div></div><div class='arrow-down'>↓</div>
      <div class='step'><div class='stepno'>4</div><div><div class='step-title'>Compare each estimate with known θ</div><div class='step-copy'>Squared error tells us how far each estimator is from the population mean.</div></div></div><div class='arrow-down'>↓</div>
      <div class='step'><div class='stepno'>5</div><div><div class='step-title'>Repeat many times</div><div class='step-copy'>The repeated errors become mean MSE and q95 difficult-case risk.</div></div></div>

      <div class='takeaway'>TAKE-HOME: Simulation gives controlled truth. Monte Carlo turns that truth into a fair repeated-sampling comparison of estimators.</div>
    </div>"""


def _b_validity() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>APPENDIX B · VALIDITY</div>
      <div class='title'>Why should we trust the simulator?</div>
      <div class='subtitle'>The simulator was checked before the GA evidence was interpreted. This page shows the audit in plain language.</div>

      <div class='metricrow'><div class='metric'><div class='v'>125</div><div class='l'>validation conditions</div></div><div class='metric'><div class='v' style='color:#54c786'>0</div><div class='l'>hard failures</div></div><div class='metric'><div class='v'>29</div><div class='l'>explainable warnings</div></div><div class='metric'><div class='v'>0.976%</div><div class='l'>maximum mean error</div></div></div>
      <div class='story'><b>Audit logic:</b> first validate the data-generating world, then trust the estimator comparison. The GA never gets to “validate” its own simulator.</div>

      <div class='section-title'>THE FOUR VALIDITY CHECKS</div>
      <div class='card'><div class='icon'>🎯</div><div><div class='label'>1 · MOMENT FIDELITY</div><div class='headline'>Does the generator recover the intended mean?</div><div class='copy'>Large generated populations are compared with the analytic mean. The maximum relative mean error was 0.976%, below the 1% hard threshold.</div><div class='mini'><b>Why it matters:</b> if the generator misses its own mean, estimator MSE would be built on the wrong target.</div></div></div>
      <div class='card'><div class='icon'>🧫</div><div><div class='label'>2 · CONTAMINATION FIDELITY</div><div class='headline'>Does the contaminated sample behave as labelled?</div><div class='copy'>The realised contamination rate, direction and MAD-based distance are checked after injection.</div><div class='mini'><b>Why it matters:</b> a regime must actually contain the stress level its label claims.</div></div></div>
      <div class='card'><div class='icon'>📐</div><div><div class='label'>3 · THEORY RECOVERY</div><div class='headline'>Do known statistical patterns reappear?</div><div class='copy'>The pipeline is checked against behaviour expected from classical robust statistics before GA conclusions are accepted.</div><div class='mini'><b>Why it matters:</b> a simulator that cannot recover known patterns should not be trusted for new claims.</div></div></div>
      <div class='card'><div class='icon'>🌐</div><div><div class='label'>4 · EMPIRICAL ANCHORING</div><div class='headline'>Is the synthetic world structurally relevant?</div><div class='copy'>Real datasets are used as shape and structure anchors. They are not treated as known population truth.</div><div class='mini'><b>Why it matters:</b> external data check realism without pretending that θ is known.</div></div></div>

      <div class='section-title'>FAIRNESS AND REPRODUCIBILITY</div>
      <div class='two'><div class='card'><div class='icon'>⚖️</div><div><div class='headline'>Same sample path</div><div class='copy'>Within one Monte Carlo replicate, every estimator sees the same generated sample.</div></div></div><div class='card'><div class='icon'>🔁</div><div><div class='headline'>Fixed seeds and logged regimes</div><div class='copy'>The sampling conditions can be reproduced and audited instead of being reconstructed from memory.</div></div></div></div>

      <div class='warn'><b>29 warnings do not mean 29 failures.</b> Warnings are retained diagnostics for explainable edge cases. Hard failures are counted separately, and there were zero.</div>
      <div class='takeaway'>TAKE-HOME: The simulator was tested independently of the GA. The evidence starts only after the data-generating world passes its own checks.</div>
    </div>"""


def _c_ga() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>APPENDIX C · GA MECHANICS</div>
      <div class='title'>What exactly did the thesis GA do?</div>
      <div class='subtitle'>The GA searches estimator weights. It does not learn a black-box predictor and it does not decide the final scientific claim.</div>

      <div class='section-title'>1 · REPRESENTATION</div>
      <div class='card'><div class='icon'>🧮</div><div><div class='label'>ESTIMATOR OUTPUT MATRIX</div><div class='headline'>C stores what every base estimator did</div><div class='copy'>Rows are Monte Carlo replications. Columns are named estimators. This lets the GA evaluate mixtures without changing the raw samples.</div></div></div>
      <div class='formula-card'><div class='formula-label'>COMPOSITE CANDIDATE</div><div class='formula'>T<sub>mix</sub> = Cw</div><div class='formula-copy'><b>C</b> = estimator outputs · <b>w</b> = simplex weight vector · <b>Cw</b> = one interpretable estimator mixture.</div></div>
      <div class='formula-card'><div class='formula-label'>VALID CHROMOSOME</div><div class='formula'>w ∈ Δ<sub>L</sub>, &nbsp; wⱼ ≥ 0, &nbsp; Σwⱼ = 1</div><div class='formula-copy'>Weights are non-negative and sum to 100%, so the final recipe remains a convex mixture of named estimators.</div></div>

      <div class='section-title'>2 · HOW ONE GENERATION EVOLVES</div>
      <div class='flow'>
        <div class='flowbox'><div class='ficon'>🎲</div><div class='fh'>Dirichlet start</div><div class='fc'>Create valid simplex weights.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>🏁</div><div class='fh'>Selection</div><div class='fc'>Better candidates reproduce more often.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>🔀</div><div class='fh'>Convex crossover</div><div class='fc'>Mix two parents and stay on the simplex.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>🧬</div><div class='fh'>Mutation</div><div class='fc'>Nudge weights toward a fresh simplex direction.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>⭐</div><div class='fh'>Elitism</div><div class='fc'>Keep strong candidates.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>🌱</div><div class='fh'>Immigration</div><div class='fc'>Inject fresh candidates to protect diversity.</div></div>
      </div>

      <div class='section-title'>3 · WARM STARTS</div>
      <div class='card'><div class='icon'>🔥</div><div><div class='headline'>Warm-started does not mean privileged</div><div class='copy'>Previously confirmed candidates can enter a new search as starting points, but they must compete again with the expanded estimator basis.</div></div></div>

      <div class='section-title'>4 · SEARCH SETTINGS</div>
      <div class='two'>
        <div class='small-card'><div class='h'>Search budget</div><div class='c'>Population ≈ 100 · 20 generations per fold · 3 folds.</div></div>
        <div class='small-card'><div class='h'>Exploration controls</div><div class='c'>Dirichlet α 0.5 or 1.0 · tournament 2 or 3 · mutation μ₀ 0.12 or 0.18 · μmin 0.05 · immigration 5–10%.</div></div>
      </div>

      <div class='section-title'>5 · FITNESS VS. ACCEPTANCE</div>
      <div class='gate'>
        <div class='gatebox'><div class='gh'>FITNESS</div><div class='gc'>Guides the search inside evolution. It answers: “where should the GA look next?”</div></div>
        <div class='gate-mid'>SEARCH<br>PROPOSES<br>→</div>
        <div class='gatebox pass'><div class='gh'>HELD-OUT GATE</div><div class='gc'>Controls the scientific claim. It answers: “is replacement supported after search is over?”</div></div>
      </div>
      <div class='takeaway'>TAKE-HOME: Fitness guides search. The gate controls acceptance. Optimization can propose a candidate; independent evidence decides whether we are allowed to claim it.</div>
    </div>"""


def _d_metrics() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>APPENDIX D · METRICS AND GATE</div>
      <div class='title'>How is a candidate judged?</div>
      <div class='subtitle'>Three quantities matter: the fixed target, average risk, and difficult-case risk. The final decision uses both risk criteria together.</div>

      <div class='section-title'>1 · THE TARGET</div>
      <div class='formula-card'><div class='formula-label'>POPULATION MEAN</div><div class='formula'>θ(F) = μ<sub>F</sub> = E<sub>F</sub>[X]</div><div class='formula-copy'>The estimand is fixed. We change the regime, not the type of quantity being estimated.</div></div>

      <div class='section-title'>2 · TWO RISK VIEWS</div>
      <div class='card'><div class='icon'>📉</div><div><div class='label'>AVERAGE RISK</div><div class='headline'>Mean MSE</div><div class='formula' style='font-size:25px'>MSE = E[(θ̂ − θ)²]</div><div class='copy'>This measures typical finite-sample squared error across replications.</div></div></div>
      <div class='card'><div class='icon'>⛰️</div><div><div class='label'>DIFFICULT-CASE RISK</div><div class='headline'>q95 of squared error</div><div class='formula' style='font-size:25px'>q<sub>.95</sub>{(θ̂ − θ)²}</div><div class='copy'>This measures the upper tail of the squared-error distribution. <b>q95 is not a p-value.</b></div></div></div>

      <div class='section-title'>3 · WHAT DOES “GAIN” MEAN?</div>
      <div class='formula-card'><div class='formula-label'>RELATIVE IMPROVEMENT</div><div class='formula'>Gain% = 100 × (Risk<sub>benchmark</sub> − Risk<sub>candidate</sub>) / Risk<sub>benchmark</sub></div><div class='formula-copy'><b>Positive gain:</b> candidate has lower risk. &nbsp; <b>Negative gain:</b> benchmark remains better.</div></div>

      <div class='section-title'>4 · THE DUAL GATE</div>
      <div class='gate'>
        <div class='gatebox'><div class='gh'>CHECK 1</div><div class='gc'>Mean MSE gain ≥ 0</div></div>
        <div class='gate-mid'>AND</div>
        <div class='gatebox'><div class='gh'>CHECK 2</div><div class='gc'>q95 gain ≥ 0</div></div>
      </div>
      <div class='two'>
        <div class='good'><b>IF BOTH PASS:</b><br>the candidate can move forward as a supported replacement.</div>
        <div class='danger'><b>IF ONE FAILS:</b><br>the benchmark is retained. Discovery alone is not enough.</div>
      </div>

      <div class='section-title'>5 · UNCERTAINTY AND FAIR COMPARATORS</div>
      <div class='card'><div class='icon'>🧷</div><div><div class='headline'>Paired bootstrap CI</div><div class='copy'>Bootstrap intervals quantify uncertainty around the gain. If an interval crosses zero, the replacement claim becomes weaker.</div></div></div>
      <div class='card'><div class='icon'>🥇</div><div><div class='headline'>Best admissible benchmark</div><div class='copy'>The GA candidate is compared with the strongest benchmark that is valid for that support and criterion — not with a deliberately weak baseline.</div></div></div>
      <div class='pillrow'><span class='pill'>Mean</span><span class='pill'>Median</span><span class='pill'>Trimmed / Winsorized</span><span class='pill'>Huber / Biweight</span><span class='pill'>Catoni</span><span class='pill'>Median-of-Means</span><span class='pill'>Trimean / HSM / Parzen where admissible</span></div>

      <div class='takeaway'>TAKE-HOME: A candidate does not win because its fitness is high. It wins only when independent evidence supports lower average risk and lower difficult-case risk against the strongest admissible benchmark.</div>
    </div>"""


def _e_results() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>APPENDIX E · RESULTS</div>
      <div class='title'>What exact evidence survived?</div>
      <div class='subtitle'>This appendix restates the technical evidence behind Layer 7. It does not rerun the GA and it does not create new claims.</div>

      <div class='section-title'>1 · EVIDENCE MAP</div>
      <div class='evidence-step'><div class='evidence-num'>36 → 16 → 2</div><div><div class='evidence-title'>Cycle I · discovery became frozen evidence</div><div class='evidence-copy'>Thirty-six controlled regimes produced 16 discovery wins. Only two Lognormal signals survived frozen confirmation.</div></div></div><div class='arrow-down'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>10 → 26</div><div><div class='evidence-title'>Cycle II · the learnable basis became stronger</div><div class='evidence-copy'>The search reopened with 26 learnable estimators and stronger HPF2 exposure.</div></div></div><div class='arrow-down'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>12</div><div><div class='evidence-title'>Expanded rediscovery winners</div><div class='evidence-copy'>The new search produced 12 discovery winners across five of six families.</div></div></div><div class='arrow-down'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>2</div><div><div class='evidence-title'>Frozen Validation II · transfer specialists</div><div class='evidence-copy'>Two Weibull candidates transferred to related locked-unseen regimes, but failed in original-regime mode.</div></div></div><div class='arrow-down'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>26/43 · 255</div><div><div class='evidence-title'>External evidence</div><div class='evidence-copy'>Twenty-six of 43 eligible parent datasets showed at least one corrected win, with 255 profile-level confirmations.</div></div></div><div class='arrow-down'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>23/34</div><div><div class='evidence-title'>Dirichlet abstention audit</div><div class='evidence-copy'>Most benchmark-retained cells had no random-simplex pass; 11/34 showed some signal and 8/8 strongest positive controls passed.</div></div></div>

      <div class='section-title'>2 · FROZEN CONFIRMATION I</div>
      <div class='card'><div class='icon'>✅</div><div><div class='headline'>CV-019 · Lognormal</div><div class='copy'>q95 gain: <b>+16.3%</b> · survived <b>8/8</b> validation seeds · bootstrap CI approximately <b>7.6% to 23.2%</b>.</div></div></div>
      <div class='card'><div class='icon'>✅</div><div><div class='headline'>CV-010 · Lognormal</div><div class='copy'>q95 gain: <b>+2.2%</b> · survived <b>8/8</b> validation seeds · bootstrap CI approximately <b>1.9% to 2.8%</b>.</div></div></div>

      <div class='section-title'>3 · EXPANDED REDISCOVERY MAP</div>
      <div class='three'><div class='small-card'><div class='n'>1</div><div class='h'>Normal</div></div><div class='small-card'><div class='n'>2</div><div class='h'>Lognormal</div></div><div class='small-card'><div class='n'>2</div><div class='h'>Weibull</div></div><div class='small-card'><div class='n'>4</div><div class='h'>Inverse Gaussian</div></div><div class='small-card'><div class='n'>0</div><div class='h'>Ex-Gaussian</div></div><div class='small-card'><div class='n'>3</div><div class='h'>Ex-Wald</div></div></div>
      <div class='story'><b>Interpretation:</b> changing the estimator library changed where useful mixtures appeared. The opportunity map is regime-conditional, not universal.</div>

      <div class='section-title'>4 · TWO WEIBULL TRANSFER SPECIALISTS</div>
      <div class='card'><div class='icon'>W1</div><div><div class='headline'>FWVR011</div><div class='split-result'><div class='pass-panel'><div class='result-title'>LOCKED-UNSEEN · PASS</div><div class='result-value'>+2.79% mean · +2.72% q95</div><div class='result-copy'>Related unseen regime, same frozen weights.</div></div><div class='fail-panel'><div class='result-title'>ORIGINAL-REGIME · FAIL</div><div class='result-value'>−15.77% mean · −45.06% q95</div><div class='result-copy'>The same candidate is not broadly valid everywhere.</div></div></div></div></div>
      <div class='card'><div class='icon'>W2</div><div><div class='headline'>FWVR012</div><div class='split-result'><div class='pass-panel'><div class='result-title'>LOCKED-UNSEEN · PASS</div><div class='result-value'>+3.18% mean · +1.25% q95</div><div class='result-copy'>Related unseen regime, same frozen weights.</div></div><div class='fail-panel'><div class='result-title'>ORIGINAL-REGIME · FAIL</div><div class='result-value'>−15.20% mean · −34.56% q95</div><div class='result-copy'>Correct claim: narrow transfer specialist, not family-wide winner.</div></div></div></div></div>

      <div class='section-title'>5 · EXTERNAL BATTERY</div>
      <div class='flow'><div class='flowbox'><div class='fh'>264</div><div class='fc'>requested targets</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='fh'>228</div><div class='fc'>loaded</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='fh'>120</div><div class='fc'>evaluated</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='fh'>43</div><div class='fc'>eligible parents</div></div></div>
      <div class='two'><div class='small-card'><div class='n'>26 / 43</div><div class='h'>Breadth</div><div class='c'>Parent datasets with at least one corrected specialist win.</div></div><div class='small-card'><div class='n'>255</div><div class='h'>Depth</div><div class='c'>Profile-level confirmations inside eligible parents.</div></div></div>
      <div class='warn'><b>Important:</b> 255 confirmations are not 255 independent datasets. Real data also do not reveal population θ.</div>

      <div class='section-title'>6 · DIRICHLET ABSTENTION AUDIT</div>
      <div class='three'><div class='small-card'><div class='n'>23 / 34</div><div class='h'>No random pass</div><div class='c'>Benchmark retention resisted random simplex challenge.</div></div><div class='small-card'><div class='n'>11 / 34</div><div class='h'>Some signal</div><div class='c'>These abstentions deserve more investigation.</div></div><div class='small-card'><div class='n'>8 / 8</div><div class='h'>Positive controls pass</div><div class='c'>The audit detects strong signal when it is present.</div></div></div>

      <div class='takeaway'>TAKE-HOME: The evidence becomes narrower as validation becomes harder. That is a feature of the design, not a failure of the GA.</div>
    </div>"""


def _f_qa() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>APPENDIX F · COMMITTEE Q&A</div>
      <div class='title'>Short answers to the questions most likely to matter</div>
      <div class='subtitle'>Answer the first sentence first. Add the second paragraph only if the committee wants more detail.</div>

      <div class='qa'><div class='q'>Why use simulation instead of only real data?</div><div class='a'><b>Because simulation gives known truth.</b> I need the true population mean to measure estimator error directly.</div><div class='more'>Real data are still used later for external calibration, but they cannot provide known population θ.</div></div>
      <div class='qa'><div class='q'>Why use a genetic algorithm?</div><div class='a'><b>Because I am searching many interpretable weight combinations across generations.</b></div><div class='more'>The GA is useful for adaptive search over the simplex. It proposes candidates; it does not decide the final claim.</div></div>
      <div class='qa'><div class='q'>Why not just select one robust estimator?</div><div class='a'><b>Because no single estimator is best across all regimes.</b></div><div class='more'>The thesis tests whether a convex mixture can exploit a useful bias–variance trade-off in selected regimes.</div></div>
      <div class='qa'><div class='q'>What does q95 measure?</div><div class='a'><b>It measures difficult-case squared error.</b></div><div class='more'>It is the 95th percentile of replicate squared errors. It is not a p-value.</div></div>
      <div class='qa'><div class='q'>Why do you need both mean MSE and q95?</div><div class='a'><b>Because a method can look good on average and still fail badly in difficult cases.</b></div><div class='more'>The dual gate protects both typical error and upper-tail error.</div></div>
      <div class='qa'><div class='q'>What is frozen validation?</div><div class='a'><b>The weights are locked before new evidence is evaluated.</b></div><div class='more'>There is no retraining, so the candidate cannot adapt to the validation data.</div></div>
      <div class='qa'><div class='q'>Why do FWVR011 and FWVR012 pass locked-unseen but fail original-regime mode?</div><div class='a'><b>Because they are narrow transfer specialists, not general Weibull winners.</b></div><div class='more'>The contrast defines the boundary of the claim instead of hiding it.</div></div>
      <div class='qa'><div class='q'>What do real-data results prove?</div><div class='a'><b>They show external empirical support, not known-truth validation.</b></div><div class='more'>The full-sample mean is a reference. The population mean is still unknown.</div></div>
      <div class='qa'><div class='q'>Why is benchmark retention a result?</div><div class='a'><b>Because the design allows the GA to lose.</b></div><div class='more'>If independent evidence does not support replacement, keeping the strongest admissible benchmark is the correct scientific decision.</div></div>
      <div class='qa'><div class='q'>What does the 11/34 Dirichlet signal mean?</div><div class='a'><b>It means some retained cells deserve another look.</b></div><div class='more'>It does not erase the 23/34 no-pass cells, and it does not replace fixed-weight confirmation.</div></div>
      <div class='qa'><div class='q'>What is the strongest contribution?</div><div class='a'><b>A reproducible framework that knows when to claim improvement and when to keep the benchmark.</b></div><div class='more'>The contribution combines statistical targeting, interpretable AI search, and explicit claim control.</div></div>
      <div class='qa'><div class='q'>What is the main limitation?</div><div class='a'><b>The strongest known-truth evidence is still simulation-based and the confirmed gains are narrow.</b></div><div class='more'>Future work should test more domains, more transfer settings, and independent replications.</div></div>
      <div class='qa'><div class='q'>What would you do next?</div><div class='a'><b>I would test transfer prospectively in new domains without changing the frozen specialists.</b></div><div class='more'>I would also investigate the 11 Dirichlet-signal cells and replicate the external evidence with independently defined targets.</div></div>

      <div class='takeaway'>Q&A RULE: give the short answer first. Then use Appendix A–E only if the committee asks for the technical proof behind it.</div>
    </div>"""


def _read_csv(rel: str) -> pd.DataFrame:
    path = ROOT / rel
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def _candidate_explorer() -> None:
    st.markdown("### Candidate-level evidence explorer")
    st.caption("Use this only if the committee asks for an exact candidate, validation mode, seed, decision, or confidence interval.")
    decisions = _read_csv("data/raw/validation/final_decision_table.csv")
    cis = _read_csv("data/raw/validation/bootstrap_ci.csv")
    if decisions.empty:
        st.info("Candidate-level validation table is not available in this bundle.")
        return

    id_col = next((c for c in ("candidate_id", "validation_id", "candidate", "id") if c in decisions.columns), None)
    if id_col is None:
        st.dataframe(decisions, use_container_width=True)
        return

    ids = sorted(decisions[id_col].dropna().astype(str).unique().tolist())
    chosen = st.selectbox("Candidate", ids, key="appendix_candidate_id")
    sub = decisions[decisions[id_col].astype(str) == str(chosen)].copy()
    st.dataframe(sub, use_container_width=True, hide_index=True)

    gain_cols = [c for c in ("mean_gain", "q95_gain") if c in sub.columns]
    if gain_cols and "validation_mode" in sub.columns:
        plot = sub.copy()
        x = []
        y = []
        metric = []
        for _, row in plot.iterrows():
            for c in gain_cols:
                x.append(str(row.get("validation_mode", "mode")))
                y.append(row.get(c))
                metric.append(c.replace("_gain", ""))
        fig = go.Figure()
        for m, color in [("mean", BLUE), ("q95", GOLD)]:
            xx = [a for a, mm in zip(x, metric) if mm == m]
            yy = [b for b, mm in zip(y, metric) if mm == m]
            if xx:
                fig.add_trace(go.Bar(name=m, x=xx, y=yy, marker_color=color))
        fig.add_hline(y=0, line_dash="dash")
        fig.update_layout(barmode="group", height=360, title="Candidate gain by validation mode", yaxis_title="Gain", plot_bgcolor=BG, paper_bgcolor=BG, font_color=TEXT)
        st.plotly_chart(fig, use_container_width=True)

    if not cis.empty:
        ci_id = next((c for c in (id_col, "candidate_id", "validation_id") if c in cis.columns), None)
        if ci_id is not None:
            ci_sub = cis[cis[ci_id].astype(str) == str(chosen)]
            if not ci_sub.empty:
                st.markdown("#### Bootstrap confidence intervals")
                st.dataframe(ci_sub, use_container_width=True, hide_index=True)


def _set_section(index: int) -> None:
    st.session_state.appendix_section = index


def render_technical_appendix() -> None:
    st.markdown("""
    <style>
      .appendix-nav .stButton>button{min-height:4.2rem!important;padding:.65rem .45rem!important;font-size:1rem!important;line-height:1.15!important;font-weight:850!important;white-space:normal!important}
    </style>
    """, unsafe_allow_html=True)

    if "appendix_section" not in st.session_state:
        st.session_state.appendix_section = 0

    st.markdown('<span class="badge thesis">TECHNICAL APPENDIX — open only when the committee asks</span>', unsafe_allow_html=True)
    st.caption("Each tab answers one technical question. The pages are deliberately larger and scrollable so nothing has to be compressed.")
    st.markdown('<div class="appendix-nav">', unsafe_allow_html=True)
    cols = st.columns(6, gap="small")
    for i, label in enumerate(APPENDIX_LABELS):
        with cols[i]:
            st.button(
                label,
                key=f"appendix_direct_{i}",
                use_container_width=True,
                type="primary" if i == st.session_state.appendix_section else "secondary",
                on_click=_set_section,
                args=(i,),
            )
    st.markdown('</div>', unsafe_allow_html=True)

    docs = (_a_simulation, _b_validity, _c_ga, _d_metrics, _e_results, _f_qa)
    heights = (1800, 1700, 1750, 1800, 2850, 2450)
    sec = max(0, min(int(st.session_state.appendix_section), 5))
    components.html(docs[sec](), height=heights[sec], scrolling=False)

    if sec == 4:
        st.markdown("---")
        if st.toggle("Open candidate-level evidence explorer", value=False, key="appendix_direct_explorer"):
            _candidate_explorer()
