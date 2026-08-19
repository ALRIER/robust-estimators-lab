"""Layer 9 · Technical drill-down.

The timed defense now explains simulation and simulator validity in Layer 2.
Layer 9 is intentionally narrower: GA mechanics, metrics/gate, detailed results,
and committee Q&A. It is a backup layer only and never reruns the thesis GA.
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
GOLD = "#f3c743"
GREEN = "#54c786"
RED = "#e66d4f"

APPENDIX_LABELS = (
    "A · GA mechanics",
    "B · Metrics & gate",
    "C · Results",
    "D · Q&A",
)


def _css() -> str:
    return """
    <style>
      *{box-sizing:border-box}
      body{margin:0;background:#081525;color:#e9f4ff;font-family:Arial,sans-serif}
      .page{padding:27px 31px 36px;background:#081525}
      .kicker{font-size:14px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin-bottom:9px}
      .title{font-size:37px;line-height:1.14;font-weight:900;color:#fff;margin-bottom:10px}
      .subtitle{font-size:19px;line-height:1.49;color:#bfd0e2;margin-bottom:25px;max-width:1280px}
      .section{font-size:21px;font-weight:900;color:#f3c743;letter-spacing:.05em;margin:30px 0 14px}
      .story{background:#0f2b47;border:1px solid #3c7198;border-left:7px solid #72cfff;border-radius:14px;padding:19px 21px;margin:17px 0;font-size:18px;line-height:1.5;color:#eef6ff}
      .takeaway{background:#12354a;border:1px solid #58aee8;border-left:7px solid #f3c743;border-radius:14px;padding:21px 23px;margin:24px 0 4px;font-size:20px;line-height:1.45;font-weight:850;color:#fff}
      .warn{background:#342b12;border:1px solid #f3c743;border-left:7px solid #f3c743;color:#fff2b8;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:20px 0}
      .good{background:#10372e;border:1px solid #54c786;border-left:7px solid #54c786;color:#d7ffe5;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:18px 0}
      .danger{background:#351f20;border:1px solid #e66d4f;border-left:7px solid #e66d4f;color:#ffd6cc;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:18px 0}
      .card{display:grid;grid-template-columns:96px 1fr;gap:20px;align-items:center;background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:15px;padding:21px 23px;margin-bottom:16px;min-height:150px}
      .icon{width:78px;height:78px;border-radius:19px;background:#10253a;border:1px solid #3c7198;display:flex;align-items:center;justify-content:center;font-size:39px;margin:auto}
      .label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:6px}
      .headline{font-size:26px;font-weight:900;line-height:1.18;color:#fff;margin-bottom:8px}
      .copy{font-size:17px;line-height:1.49;color:#dce9f8}
      .mini{font-size:15px;line-height:1.44;color:#b9c8d9;margin-top:8px}
      .formula-card{background:#0b2138;border:1px solid #356e99;border-left:6px solid #f3c743;border-radius:14px;padding:19px 21px;margin:15px 0}
      .formula-label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:7px}
      .formula{font-family:Georgia,serif;font-size:30px;font-weight:800;line-height:1.35;color:#f7d768;margin-bottom:9px}
      .formula-copy{font-size:17px;line-height:1.48;color:#dce9f8}
      .flow{display:flex;align-items:stretch;gap:9px;margin:17px 0;flex-wrap:wrap}
      .flowbox{flex:1;min-width:145px;background:#10253a;border:1px solid #356e99;border-radius:12px;padding:15px;text-align:center}
      .flowbox .ficon{font-size:30px;margin-bottom:7px}.flowbox .fh{font-size:17px;font-weight:900;color:#fff;margin-bottom:5px}.flowbox .fc{font-size:14px;line-height:1.37;color:#bfd0e2}
      .flowarrow{display:flex;align-items:center;justify-content:center;color:#72cfff;font-size:28px;font-weight:900}
      .two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
      .three{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
      .gate{display:grid;grid-template-columns:1fr 110px 1fr;gap:14px;align-items:center;margin:19px 0}
      .gatebox{background:#10253a;border:1px solid #356e99;border-radius:14px;padding:20px;text-align:center}
      .gatebox.pass{border-color:#54c786;background:#10372e}.gatebox.fail{border-color:#e66d4f;background:#351f20}
      .gatebox .gh{font-size:22px;font-weight:900;color:#fff;margin-bottom:7px}.gatebox .gc{font-size:16px;line-height:1.43;color:#dce9f8}
      .gate-mid{text-align:center;color:#72cfff;font-size:18px;font-weight:900;line-height:1.3}
      .pillrow{display:flex;gap:9px;flex-wrap:wrap;margin:13px 0}.pill{background:#10253a;border:1px solid #356e99;border-radius:20px;padding:9px 13px;font-size:14px;font-weight:800;color:#e6f1fb}
      .small-card{background:#10253a;border:1px solid #356e99;border-radius:12px;padding:17px;min-height:125px}
      .small-card .n{font-size:29px;font-weight:900;color:#f3c743;margin-bottom:5px}.small-card .h{font-size:17px;font-weight:900;color:#fff;margin-bottom:5px}.small-card .c{font-size:15px;line-height:1.42;color:#dce9f8}
      .evidence-step{display:grid;grid-template-columns:125px 1fr;gap:18px;align-items:center;background:#0d2239;border:1px solid #356e99;border-radius:14px;padding:19px 21px;margin:10px 0}
      .evidence-num{font-size:34px;font-weight:900;color:#f3c743;text-align:center}.evidence-title{font-size:21px;font-weight:900;color:#fff;margin-bottom:5px}.evidence-copy{font-size:16px;line-height:1.46;color:#dce9f8}
      .arrow{text-align:center;font-size:30px;color:#72cfff;font-weight:900;line-height:1;margin:3px 0}
      .split-result{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:11px}
      .pass-panel,.fail-panel{border-radius:12px;padding:17px 18px}.pass-panel{background:#10372e;border:1px solid #54c786}.fail-panel{background:#351f20;border:1px solid #e66d4f}
      .result-title{font-size:18px;font-weight:900;color:#fff;margin-bottom:7px}.result-value{font-size:25px;font-weight:900;margin-bottom:5px}.pass-panel .result-value{color:#54c786}.fail-panel .result-value{color:#ff8669}.result-copy{font-size:14px;line-height:1.4;color:#e7eef7}
      .qa{background:#0b2138;border:1px solid #356e99;border-radius:14px;padding:19px 21px;margin-bottom:14px}.q{font-size:20px;font-weight:900;color:#72cfff;margin-bottom:7px}.a{font-size:18px;line-height:1.48;color:#edf5ff}.more{font-size:15px;line-height:1.44;color:#b9c8d9;margin-top:9px;border-top:1px solid #284c6b;padding-top:9px}
      @media(max-width:1050px){.two,.three{grid-template-columns:1fr}.gate{grid-template-columns:1fr}.gate-mid{padding:6px}.card{grid-template-columns:78px 1fr}.flowarrow{display:none}.split-result{grid-template-columns:1fr}}
    </style>
    """


def _ga_mechanics() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>TECHNICAL APPENDIX A · GA MECHANICS</div>
      <div class='title'>What exactly did the thesis GA do?</div>
      <div class='subtitle'>Use this page only when the committee asks about representation, operators, warm starts, hyperparameters or interpretability.</div>

      <div class='section'>1 · WHAT DOES ONE GA INDIVIDUAL REPRESENT?</div>
      <div class='card'><div class='icon'>🧮</div><div><div class='label'>ESTIMATOR OUTPUT MATRIX</div><div class='headline'>C stores the base estimators</div><div class='copy'>Rows are Monte Carlo replications. Columns are named estimators. The GA changes weights over these columns; it does not change the raw samples.</div></div></div>
      <div class='formula-card'><div class='formula-label'>COMPOSITE CANDIDATE</div><div class='formula'>T<sub>mix</sub> = Cw</div><div class='formula-copy'><b>C</b> = estimator outputs · <b>w</b> = weight vector · <b>Cw</b> = one interpretable composite estimator.</div></div>
      <div class='formula-card'><div class='formula-label'>SIMPLEX CONSTRAINT</div><div class='formula'>w ∈ Δ<sub>L</sub>, &nbsp; wⱼ ≥ 0, &nbsp; Σwⱼ = 1</div><div class='formula-copy'>Every recipe is a convex mixture. The weights are non-negative and add to 100%.</div></div>

      <div class='section'>2 · HOW DOES ONE GENERATION EVOLVE?</div>
      <div class='flow'>
        <div class='flowbox'><div class='ficon'>🎲</div><div class='fh'>Dirichlet start</div><div class='fc'>Generate valid simplex weights.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>🏁</div><div class='fh'>Selection</div><div class='fc'>Better candidates reproduce more often.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>🔀</div><div class='fh'>Convex crossover</div><div class='fc'>Mix parents while staying on the simplex.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>🧬</div><div class='fh'>Mutation</div><div class='fc'>Nudge a child toward a fresh simplex direction.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>⭐</div><div class='fh'>Elitism</div><div class='fc'>Keep strong candidates.</div></div><div class='flowarrow'>→</div>
        <div class='flowbox'><div class='ficon'>🌱</div><div class='fh'>Immigration</div><div class='fc'>Inject fresh candidates to protect diversity.</div></div>
      </div>

      <div class='section'>3 · WHAT ABOUT WARM STARTS?</div>
      <div class='card'><div class='icon'>🔥</div><div><div class='headline'>Warm-started does not mean privileged</div><div class='copy'>Previously confirmed candidates can enter a later search as starting points, but they must compete again against the expanded estimator basis.</div></div></div>

      <div class='section'>4 · SEARCH SETTINGS</div>
      <div class='two'>
        <div class='small-card'><div class='h'>Search budget</div><div class='c'>Population ≈ 100 · 20 generations per fold · 3 folds.</div></div>
        <div class='small-card'><div class='h'>Exploration controls</div><div class='c'>Dirichlet α 0.5 or 1.0 · tournament 2 or 3 · mutation μ₀ 0.12 or 0.18 · μmin 0.05 · immigration 5–10%.</div></div>
      </div>

      <div class='section'>5 · FITNESS IS NOT THE FINAL CLAIM</div>
      <div class='gate'><div class='gatebox'><div class='gh'>FITNESS</div><div class='gc'>Guides search inside evolution. It answers: where should the GA look next?</div></div><div class='gate-mid'>SEARCH<br>PROPOSES<br>→</div><div class='gatebox pass'><div class='gh'>HELD-OUT GATE</div><div class='gc'>Controls the scientific claim after search is over.</div></div></div>
      <div class='takeaway'>TAKE-HOME: fitness guides search. The gate controls acceptance. The GA proposes; independent evidence decides.</div>
    </div>"""


def _metrics_gate() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>TECHNICAL APPENDIX B · METRICS AND GATE</div>
      <div class='title'>How is a candidate judged?</div>
      <div class='subtitle'>Use this page for questions about MSE, q95, relative gain, bootstrap confidence intervals, benchmark admissibility or the dual gate.</div>

      <div class='section'>1 · FIXED TARGET</div>
      <div class='formula-card'><div class='formula-label'>POPULATION MEAN</div><div class='formula'>θ(F) = μ<sub>F</sub> = E<sub>F</sub>[X]</div><div class='formula-copy'>The estimand is the population mean. The regime changes; the type of target does not.</div></div>

      <div class='section'>2 · TWO RISK VIEWS</div>
      <div class='card'><div class='icon'>📉</div><div><div class='label'>AVERAGE RISK</div><div class='headline'>Mean MSE</div><div class='formula' style='font-size:25px'>MSE = E[(θ̂ − θ)²]</div><div class='copy'>Typical finite-sample squared error across repeated samples.</div></div></div>
      <div class='card'><div class='icon'>⛰️</div><div><div class='label'>DIFFICULT-CASE RISK</div><div class='headline'>q95 of squared error</div><div class='formula' style='font-size:25px'>q<sub>.95</sub>{(θ̂ − θ)²}</div><div class='copy'>Upper-tail squared error. <b>q95 is not a p-value.</b></div></div></div>

      <div class='section'>3 · RELATIVE GAIN</div>
      <div class='formula-card'><div class='formula-label'>BENCHMARK-RELATIVE IMPROVEMENT</div><div class='formula'>Gain% = 100 × (Risk<sub>benchmark</sub> − Risk<sub>candidate</sub>) / Risk<sub>benchmark</sub></div><div class='formula-copy'><b>Positive:</b> candidate has lower risk. &nbsp; <b>Negative:</b> benchmark remains better.</div></div>

      <div class='section'>4 · DUAL BENCHMARK GATE</div>
      <div class='gate'><div class='gatebox'><div class='gh'>CHECK 1</div><div class='gc'>Mean MSE gain ≥ 0</div></div><div class='gate-mid'>AND</div><div class='gatebox'><div class='gh'>CHECK 2</div><div class='gc'>q95 gain ≥ 0</div></div></div>
      <div class='two'><div class='good'><b>IF BOTH PASS:</b><br>the candidate can move forward as a supported replacement.</div><div class='danger'><b>IF ONE FAILS:</b><br>keep the benchmark. Discovery is not enough.</div></div>

      <div class='section'>5 · UNCERTAINTY AND FAIR COMPARISON</div>
      <div class='card'><div class='icon'>🧷</div><div><div class='headline'>Paired bootstrap confidence interval</div><div class='copy'>The interval shows uncertainty around the gain. If it crosses zero, the replacement claim becomes weaker.</div></div></div>
      <div class='card'><div class='icon'>🥇</div><div><div class='headline'>Best admissible benchmark</div><div class='copy'>The candidate is compared with the strongest comparator that is valid for that support and criterion — not with a deliberately weak baseline.</div></div></div>
      <div class='pillrow'><span class='pill'>Mean</span><span class='pill'>Median</span><span class='pill'>Trimmed / Winsorized</span><span class='pill'>Huber / Biweight</span><span class='pill'>Catoni</span><span class='pill'>Median-of-Means</span><span class='pill'>Trimean / HSM / Parzen where admissible</span></div>

      <div class='takeaway'>TAKE-HOME: a candidate wins only when independent evidence supports lower average risk and lower difficult-case risk against the strongest admissible benchmark.</div>
    </div>"""


def _results() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>TECHNICAL APPENDIX C · RESULTS</div>
      <div class='title'>What exact evidence survived?</div>
      <div class='subtitle'>This is the technical backup behind Layer 7. It restates fixed thesis evidence; it does not rerun the search.</div>

      <div class='section'>1 · EVIDENCE MAP</div>
      <div class='evidence-step'><div class='evidence-num'>36 → 16 → 2</div><div><div class='evidence-title'>Cycle I · discovery became frozen evidence</div><div class='evidence-copy'>Thirty-six controlled regimes produced 16 discovery wins. Only two Lognormal signals survived frozen confirmation.</div></div></div><div class='arrow'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>10 → 26</div><div><div class='evidence-title'>Cycle II · stronger estimator basis</div><div class='evidence-copy'>The search reopened with 26 learnable estimators and stronger exposure.</div></div></div><div class='arrow'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>12</div><div><div class='evidence-title'>Expanded rediscovery winners</div><div class='evidence-copy'>Twelve discovery winners appeared across five of six families.</div></div></div><div class='arrow'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>2</div><div><div class='evidence-title'>Frozen Validation II · transfer specialists</div><div class='evidence-copy'>Two Weibull candidates transferred to related locked-unseen regimes, but failed in original-regime mode.</div></div></div><div class='arrow'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>26/43 · 255</div><div><div class='evidence-title'>External evidence</div><div class='evidence-copy'>Twenty-six of 43 eligible parent datasets showed at least one corrected win, with 255 profile-level confirmations.</div></div></div><div class='arrow'>↓</div>
      <div class='evidence-step'><div class='evidence-num'>23/34</div><div><div class='evidence-title'>Dirichlet abstention audit</div><div class='evidence-copy'>Most benchmark-retained cells had no random-simplex pass. Eleven showed some signal; 8/8 strongest positive controls passed.</div></div></div>

      <div class='section'>2 · FROZEN CONFIRMATION I</div>
      <div class='card'><div class='icon'>✅</div><div><div class='headline'>CV-019 · Lognormal</div><div class='copy'>q95 gain <b>+16.3%</b> · survived <b>8/8</b> validation seeds · bootstrap CI approximately <b>7.6% to 23.2%</b>.</div></div></div>
      <div class='card'><div class='icon'>✅</div><div><div class='headline'>CV-010 · Lognormal</div><div class='copy'>q95 gain <b>+2.2%</b> · survived <b>8/8</b> validation seeds · bootstrap CI approximately <b>1.9% to 2.8%</b>.</div></div></div>

      <div class='section'>3 · EXPANDED REDISCOVERY MAP</div>
      <div class='three'><div class='small-card'><div class='n'>1</div><div class='h'>Normal</div></div><div class='small-card'><div class='n'>2</div><div class='h'>Lognormal</div></div><div class='small-card'><div class='n'>2</div><div class='h'>Weibull</div></div><div class='small-card'><div class='n'>4</div><div class='h'>Inverse Gaussian</div></div><div class='small-card'><div class='n'>0</div><div class='h'>Ex-Gaussian</div></div><div class='small-card'><div class='n'>3</div><div class='h'>Ex-Wald</div></div></div>
      <div class='story'><b>Meaning:</b> changing the estimator library changed where useful mixtures appeared. The opportunity map is conditional, not universal.</div>

      <div class='section'>4 · TWO WEIBULL TRANSFER SPECIALISTS</div>
      <div class='card'><div class='icon'>W1</div><div><div class='headline'>FWVR011</div><div class='split-result'><div class='pass-panel'><div class='result-title'>LOCKED-UNSEEN · PASS</div><div class='result-value'>+2.79% mean · +2.72% q95</div><div class='result-copy'>Related unseen regime, same frozen weights.</div></div><div class='fail-panel'><div class='result-title'>ORIGINAL-REGIME · FAIL</div><div class='result-value'>−15.77% mean · −45.06% q95</div><div class='result-copy'>Not a broad family-wide winner.</div></div></div></div></div>
      <div class='card'><div class='icon'>W2</div><div><div class='headline'>FWVR012</div><div class='split-result'><div class='pass-panel'><div class='result-title'>LOCKED-UNSEEN · PASS</div><div class='result-value'>+3.18% mean · +1.25% q95</div><div class='result-copy'>Related unseen regime, same frozen weights.</div></div><div class='fail-panel'><div class='result-title'>ORIGINAL-REGIME · FAIL</div><div class='result-value'>−15.20% mean · −34.56% q95</div><div class='result-copy'>Correct claim: narrow transfer specialist.</div></div></div></div></div>

      <div class='section'>5 · EXTERNAL BATTERY AND AUDIT</div>
      <div class='two'><div class='small-card'><div class='n'>26 / 43</div><div class='h'>External breadth</div><div class='c'>Eligible parent datasets with at least one corrected specialist win.</div></div><div class='small-card'><div class='n'>255</div><div class='h'>External depth</div><div class='c'>Profile-level confirmations inside eligible parents.</div></div></div>
      <div class='warn'><b>Important:</b> 255 confirmations are not 255 independent datasets. Real data also do not reveal population θ.</div>
      <div class='three'><div class='small-card'><div class='n'>23 / 34</div><div class='h'>No random pass</div><div class='c'>Benchmark retention resisted random simplex challenge.</div></div><div class='small-card'><div class='n'>11 / 34</div><div class='h'>Some signal</div><div class='c'>These abstentions deserve more investigation.</div></div><div class='small-card'><div class='n'>8 / 8</div><div class='h'>Positive controls pass</div><div class='c'>The audit detects strong signal when present.</div></div></div>

      <div class='takeaway'>TAKE-HOME: the evidence becomes narrower as validation becomes harder. That is the intended behaviour of the design.</div>
    </div>"""


def _qa() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>TECHNICAL APPENDIX D · COMMITTEE Q&A</div>
      <div class='title'>Short answers to difficult questions</div>
      <div class='subtitle'>Say the bold sentence first. Expand only if the committee asks for more detail.</div>

      <div class='qa'><div class='q'>Why use a genetic algorithm?</div><div class='a'><b>Because I am searching many interpretable weight combinations across generations.</b></div><div class='more'>The GA proposes candidates on the simplex. It does not decide the final scientific claim.</div></div>
      <div class='qa'><div class='q'>Why not just select one robust estimator?</div><div class='a'><b>Because no single estimator is best across all regimes.</b></div><div class='more'>The thesis tests whether a convex mixture can improve the bias–variance trade-off in selected regimes.</div></div>
      <div class='qa'><div class='q'>Why q95?</div><div class='a'><b>Because average performance can hide difficult cases.</b></div><div class='more'>q95 is the 95th percentile of replicate squared errors. It is not a p-value.</div></div>
      <div class='qa'><div class='q'>What is frozen validation?</div><div class='a'><b>The weights are locked before new evidence is evaluated.</b></div><div class='more'>There is no retraining, so the candidate cannot adapt to the validation data.</div></div>
      <div class='qa'><div class='q'>Why do FWVR011 and FWVR012 pass locked-unseen but fail original-regime validation?</div><div class='a'><b>Because they are narrow transfer specialists, not general Weibull winners.</b></div><div class='more'>That contrast defines the boundary of the claim instead of hiding it.</div></div>
      <div class='qa'><div class='q'>What do real-data results prove?</div><div class='a'><b>They show external empirical support, not known-truth validation.</b></div><div class='more'>The full-sample empirical mean is a reference; the population mean remains unknown.</div></div>
      <div class='qa'><div class='q'>Why is benchmark retention a result?</div><div class='a'><b>Because the design allows the GA to lose.</b></div><div class='more'>If independent evidence does not support replacement, keeping the strongest admissible benchmark is the correct scientific decision.</div></div>
      <div class='qa'><div class='q'>What does the 11/34 Dirichlet signal mean?</div><div class='a'><b>It means some retained cells deserve another look.</b></div><div class='more'>It does not erase the 23/34 no-pass cells, and it does not replace fixed-weight confirmation.</div></div>
      <div class='qa'><div class='q'>What is the strongest contribution?</div><div class='a'><b>A reproducible framework that knows when to claim improvement and when to keep the benchmark.</b></div><div class='more'>The contribution combines statistical targeting, interpretable AI search and explicit claim control.</div></div>
      <div class='qa'><div class='q'>What is the main limitation?</div><div class='a'><b>The strongest known-truth evidence is simulation-based and the confirmed gains are narrow.</b></div><div class='more'>That is why the final claim is conditional rather than universal.</div></div>
      <div class='qa'><div class='q'>What would you do next?</div><div class='a'><b>I would test prospective transfer in new domains without changing the frozen specialists.</b></div><div class='more'>I would also investigate the Dirichlet-signal cells and seek independent external replications.</div></div>

      <div class='takeaway'>Q&A RULE: answer the question first. Then open Appendix A–C only if the committee asks for the technical evidence behind the answer.</div>
    </div>"""


def _read_csv(rel: str) -> pd.DataFrame:
    path = ROOT / rel
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def _candidate_explorer() -> None:
    st.markdown("### Candidate-level evidence explorer")
    st.caption("Open this only if the committee asks for an exact candidate, validation mode, seed, decision or confidence interval.")
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
        x, y, metric = [], [], []
        for _, row in sub.iterrows():
            for c in gain_cols:
                x.append(str(row.get("validation_mode", "mode")))
                y.append(row.get(c))
                metric.append(c.replace("_gain", ""))
        fig = go.Figure()
        for name, color in (("mean", BLUE), ("q95", GOLD)):
            xx = [a for a, mm in zip(x, metric) if mm == name]
            yy = [b for b, mm in zip(y, metric) if mm == name]
            if xx:
                fig.add_trace(go.Bar(name=name, x=xx, y=yy, marker_color=color))
        fig.add_hline(y=0, line_dash="dash")
        fig.update_layout(barmode="group", height=370, title="Candidate gain by validation mode", yaxis_title="Gain", plot_bgcolor=BG, paper_bgcolor=BG, font_color=TEXT)
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
      .appendix-nav .stButton>button{min-height:4.3rem!important;padding:.7rem .5rem!important;font-size:1.05rem!important;line-height:1.15!important;font-weight:850!important;white-space:normal!important}
    </style>
    """, unsafe_allow_html=True)

    max_section = len(APPENDIX_LABELS) - 1
    if "appendix_section" not in st.session_state:
        st.session_state.appendix_section = 0
    st.session_state.appendix_section = max(0, min(int(st.session_state.appendix_section), max_section))

    st.markdown('<span class="badge thesis">TECHNICAL APPENDIX — open only when the committee asks</span>', unsafe_allow_html=True)
    st.caption("Simulation and simulator validity now live in Layer 2. This appendix keeps only the deeper technical backup needed for Q&A.")
    st.markdown('<div class="appendix-nav">', unsafe_allow_html=True)
    cols = st.columns(len(APPENDIX_LABELS), gap="small")
    for i, label in enumerate(APPENDIX_LABELS):
        with cols[i]:
            st.button(label, key=f"appendix_direct_{i}", use_container_width=True,
                      type="primary" if i == st.session_state.appendix_section else "secondary",
                      on_click=_set_section, args=(i,))
    st.markdown('</div>', unsafe_allow_html=True)

    docs = (_ga_mechanics, _metrics_gate, _results, _qa)
    heights = (1800, 1850, 3000, 2200)
    sec = st.session_state.appendix_section
    components.html(docs[sec](), height=heights[sec], scrolling=False)

    if sec == 2:
        st.markdown("---")
        if st.toggle("Open candidate-level evidence explorer", value=False, key="appendix_direct_explorer"):
            _candidate_explorer()
