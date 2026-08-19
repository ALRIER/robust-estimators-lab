"""Final defense pages for Layer 8 (conclusions) and Layer 9 (technical appendix).

Presentation-only. The module summarizes fixed thesis design/results and never reruns
any GA search. It is installed as a lightweight render hook from data_loader.py so the
legacy Layer 8/9 blocks can remain untouched while the defense UI gets a clean final
presentation layer.
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
_LAYER8 = "08 · Conclusions"
_LAYER9 = "09 · Technical drill-down"

COLORS = {
    "bg": "#081525",
    "panel": "#0d2842",
    "panel2": "#102f4d",
    "blue": "#58aee8",
    "cyan": "#72cfff",
    "gold": "#f3c743",
    "green": "#54c786",
    "red": "#e66d4f",
    "purple": "#a777e3",
    "muted": "#526a85",
    "text": "#e9f4ff",
    "subtle": "#b9c8d9",
}

APPENDIX_LABELS = (
    "A · Simulation",
    "B · Validity",
    "C · GA code",
    "D · Metrics & gate",
    "E · Results",
    "F · Q&A",
)


def _css() -> str:
    return f"""
    <style>
    *{{box-sizing:border-box}}
    body{{margin:0;background:{COLORS['bg']};color:{COLORS['text']};font-family:Arial,sans-serif}}
    .page{{padding:18px 22px 22px;background:{COLORS['bg']};min-height:690px}}
    .kicker{{font-size:13px;font-weight:900;letter-spacing:.13em;color:{COLORS['cyan']};margin-bottom:7px}}
    .title{{font-size:31px;line-height:1.14;font-weight:900;color:#fff;margin:0 0 7px}}
    .subtitle{{font-size:16px;line-height:1.4;color:{COLORS['subtle']};margin-bottom:20px}}
    .grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
    .grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}}
    .grid2{{display:grid;grid-template-columns:repeat(2,1fr);gap:15px}}
    .card{{background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:13px;padding:17px 18px;min-height:145px}}
    .card.green{{border-top:4px solid {COLORS['green']}}}
    .card.gold{{border-top:4px solid {COLORS['gold']}}}
    .card.blue{{border-top:4px solid {COLORS['blue']}}}
    .card.purple{{border-top:4px solid {COLORS['purple']}}}
    .card.red{{border-top:4px solid {COLORS['red']}}}
    .smallhead{{font-size:12px;font-weight:900;letter-spacing:.10em;color:{COLORS['cyan']};margin-bottom:8px}}
    .big{{font-size:25px;font-weight:900;line-height:1.16;margin-bottom:8px}}
    .copy{{font-size:15px;line-height:1.45;color:#dce9f8}}
    .status{{display:inline-block;margin-top:11px;padding:5px 9px;border-radius:16px;font-size:12px;font-weight:900;letter-spacing:.04em}}
    .status.pass{{background:#103b31;color:#a9f3c2;border:1px solid {COLORS['green']}}}
    .status.caution{{background:#3a3214;color:#ffe387;border:1px solid {COLORS['gold']}}}
    .chain{{display:flex;align-items:center;gap:8px;margin:16px 0 18px}}
    .chain .node{{flex:1;background:#10253a;border:1px solid #3c7198;border-radius:11px;padding:11px;text-align:center;font-weight:800;font-size:14px}}
    .chain .arrow{{font-size:25px;color:{COLORS['cyan']};font-weight:900}}
    .takehome{{margin-top:17px;background:#0e3047;border:1px solid {COLORS['cyan']};border-left:6px solid {COLORS['gold']};border-radius:12px;padding:16px 19px;font-size:17px;line-height:1.4;font-weight:800;color:#f4f8ff}}
    .limitband{{margin-top:17px;background:#2a2017;border:1px solid #9a7920;border-radius:12px;padding:15px 17px}}
    .limitgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:11px;margin-top:9px}}
    .limit{{background:#171b23;border:1px solid #55472b;border-radius:9px;padding:11px 12px;color:#efe6d0;font-size:14px;line-height:1.35}}
    .metricrow{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:15px 0}}
    .metric{{background:#10253a;border:1px solid #356e99;border-radius:11px;padding:13px;text-align:center}}
    .metric .v{{font-size:27px;font-weight:900;color:{COLORS['gold']}}}
    .metric .l{{font-size:12px;color:{COLORS['subtle']};margin-top:4px;font-weight:700}}
    .formula{{font-family:Georgia,serif;font-size:22px;font-weight:700;color:#f7d768;background:#0a1d32;border:1px solid #356e99;border-radius:10px;padding:12px 14px;margin:10px 0}}
    .pillrow{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}
    .pill{{background:#10253a;border:1px solid #356e99;border-radius:18px;padding:7px 11px;font-size:13px;font-weight:800;color:#e6f1fb}}
    .warn{{background:#342b12;border:1px solid {COLORS['gold']};color:#fff0af;border-radius:10px;padding:12px 14px;font-size:14px;line-height:1.4;margin-top:12px}}
    .qa{{background:#0b2138;border:1px solid #356e99;border-radius:11px;padding:13px 15px;margin-bottom:10px}}
    .qa .q{{font-size:15px;font-weight:900;color:{COLORS['cyan']};margin-bottom:5px}}
    .qa .a{{font-size:14px;line-height:1.42;color:#dce9f8}}
    .code{{font-family:Consolas,monospace;font-size:13px;line-height:1.48;background:#06101d;border:1px solid #355a78;border-radius:10px;padding:13px 15px;color:#d7e8f6;white-space:pre-wrap}}
    .sectionbar{{background:#102a49;border:1px solid #3c7198;border-left:5px solid {COLORS['cyan']};border-radius:11px;padding:12px 15px;margin:16px 0 12px;font-size:16px;font-weight:900;color:#fff}}
    @media(max-width:1000px){{.grid4,.limitgrid{{grid-template-columns:repeat(2,1fr)}}.grid3{{grid-template-columns:1fr}}}}
    </style>
    """


def _conclusion_claims_html() -> str:
    return _css() + f"""
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
      <div class='grid4'>
        <div class='card green'><div class='smallhead'>H1</div><div class='big'>No universal estimator</div><div class='copy'>Estimator rankings change across incompatible distributional and contamination regimes.</div><div class='status pass'>SUPPORTED</div></div>
        <div class='card green'><div class='smallhead'>H2</div><div class='big'>Performance depends on regime</div><div class='copy'>The useful estimator changes with family, contamination, scale, mechanism and sample size.</div><div class='status pass'>SUPPORTED</div></div>
        <div class='card gold'><div class='smallhead'>H3</div><div class='big'>GA helps selected regimes</div><div class='copy'>Real gains exist, but they are narrow and profile-bound rather than general.</div><div class='status caution'>CONSERVATIVE SUPPORT</div></div>
        <div class='card green'><div class='smallhead'>H4</div><div class='big'>The gate prevents false claims</div><div class='copy'>Discovery can be rejected. Benchmark retention is an intended scientific outcome.</div><div class='status pass'>SUPPORTED</div></div>
      </div>
      <div class='takehome'><b>TAKE-HOME:</b> the contribution is not a universal GA winner. It is a disciplined way to know when a composite estimator is justified — and when the benchmark should remain the answer.</div>
    </div>
    """


def _conclusion_contrib_html() -> str:
    return _css() + f"""
    <div class='page'>
      <div class='kicker'>08 · CONTRIBUTIONS AND LIMITS</div>
      <div class='title'>What the thesis contributes — and where the claim stops.</div>
      <div class='subtitle'>Three contributions work together: a statistical target, an interpretable AI search mechanism, and a validation design that controls overstatement.</div>
      <div class='grid3'>
        <div class='card blue'><div class='smallhead'>STATISTICAL CONTRIBUTION</div><div class='big'>Target-aware robust estimation of E[X]</div><div class='copy'>A regime-conditional way to combine established location estimators while keeping the population mean fixed as the target under skew, tails and contamination.</div></div>
        <div class='card purple'><div class='smallhead'>AI CONTRIBUTION</div><div class='big'>Interpretable evolutionary search</div><div class='copy'>The GA searches simplex-constrained weights over named estimators. The final recipe is auditable, not a black-box prediction function.</div></div>
        <div class='card green'><div class='smallhead'>METHODOLOGICAL CONTRIBUTION</div><div class='big'>Claim control by design</div><div class='copy'>Simulation certification, staged discovery, frozen validation, benchmark retention, external calibration and an independent random-simplex audit.</div></div>
      </div>
      <div class='limitband'>
        <div class='smallhead' style='color:#ffe387'>LIMITS I WOULD NAME BEFORE THE COMMITTEE DOES</div>
        <div class='limitgrid'>
          <div class='limit'><b>Simulated truth.</b><br>The main known-truth validation relies on controlled data-generating distributions.</div>
          <div class='limit'><b>Narrow confirmed effects.</b><br>The strongest supported improvements are specialists, not broad family-wide winners.</div>
          <div class='limit'><b>Profile-dependent transfer.</b><br>Evidence does not justify extrapolating a frozen specialist far outside its validated regime.</div>
          <div class='limit'><b>Real-data reference.</b><br>External data do not reveal population θ; the full-sample mean is a reference, so that layer supports robustness and transfer, not known-truth error recovery.</div>
        </div>
      </div>
      <div class='takehome'><b>SINGLE STRONGEST CONTRIBUTION:</b> a reproducible framework that knows when to claim an improvement and when to keep the benchmark.</div>
    </div>
    """


def _appendix_a() -> str:
    return _css() + f"""
    <div class='page'>
      <div class='kicker'>APPENDIX A · SIMULATION</div><div class='title'>Why Monte Carlo — and what world was simulated?</div>
      <div class='grid3'>
        <div class='card blue'><div class='smallhead'>CONTROLLED TRUTH</div><div class='big'>θ = E[X]</div><div class='copy'>The data-generating distribution defines the true population mean before any estimator is scored.</div></div>
        <div class='card green'><div class='smallhead'>DIRECT ERROR</div><div class='big'>Estimator vs. truth</div><div class='copy'>Squared error, MSE and q95 can be measured against θ rather than against a proxy.</div></div>
        <div class='card purple'><div class='smallhead'>SYSTEMATIC STRESS TEST</div><div class='big'>Regime grid</div><div class='copy'>Family, sample size, contamination rate, outlier scale and mechanism are varied deliberately.</div></div>
      </div>
      <div class='sectionbar'>Distributional world</div>
      <div class='pillrow'><span class='pill'>Normal · symmetric baseline</span><span class='pill'>Lognormal · positive right-skew</span><span class='pill'>Weibull · survival-like positive shape</span><span class='pill'>Inverse Gaussian · asymmetric duration</span><span class='pill'>Ex-Gaussian · reaction-time-like tail</span><span class='pill'>Ex-Wald · first-passage process</span></div>
      <div class='metricrow'><div class='metric'><div class='v'>6</div><div class='l'>families</div></div><div class='metric'><div class='v'>5</div><div class='l'>sample sizes · 300–5000</div></div><div class='metric'><div class='v'>576</div><div class='l'>contamination profiles / family</div></div><div class='metric'><div class='v'>2880</div><div class='l'>regimes / family after n</div></div></div>
      <div class='formula'>ℛ = (F₀, γ, c, m, n) &nbsp;&nbsp;→&nbsp;&nbsp; F_ℛ = (1−γ)F₀ + γG<sub>m,c</sub>(F₀)</div>
      <div class='sectionbar'>Monte Carlo measurement engine</div>
      <div class='code'>for regime in grid:
    θ &lt;- analytic_mean(regime)
    for r in 1:R:
        x_r    &lt;- simulate_sample(regime, seed_r)
        T_r    &lt;- apply_all_estimators(x_r)   # same replicate for every estimator
        err2_r &lt;- (T_r - θ)^2
    MSE &lt;- mean(err2_r)
    q95 &lt;- quantile(err2_r, 0.95)</div>
      <div class='warn'><b>Why simulation is deliberate:</b> real datasets do not reveal the population mean. They are used later for external robustness, not for true-error calibration.</div>
    </div>"""


def _appendix_b() -> str:
    return _css() + f"""
    <div class='page'>
      <div class='kicker'>APPENDIX B · VALIDITY</div><div class='title'>How do we know the simulated world is trustworthy?</div>
      <div class='metricrow'><div class='metric'><div class='v'>125</div><div class='l'>validation conditions</div></div><div class='metric'><div class='v' style='color:{COLORS['green']}'>0</div><div class='l'>hard failures</div></div><div class='metric'><div class='v'>29</div><div class='l'>explainable warnings</div></div><div class='metric'><div class='v'>0.976%</div><div class='l'>max mean error · below 1%</div></div></div>
      <div class='grid2'>
        <div class='card blue'><div class='smallhead'>1 · MOMENT FIDELITY</div><div class='big'>Does the generator recover θ?</div><div class='copy'>Large generated populations recover analytic moments. Maximum reported mean error: 0.976%, below the 1% hard threshold.</div></div>
        <div class='card green'><div class='smallhead'>2 · CONTAMINATION FIDELITY</div><div class='big'>Does the injected regime behave as labelled?</div><div class='copy'>Realised rate, direction and MAD-based distance are checked after contamination is injected.</div></div>
        <div class='card purple'><div class='smallhead'>3 · THEORY RECOVERY</div><div class='big'>Do known statistical patterns reappear?</div><div class='copy'>Classical robust-statistics behaviour is recovered before GA conclusions are interpreted.</div></div>
        <div class='card gold'><div class='smallhead'>4 · EMPIRICAL ANCHORING</div><div class='big'>Is the synthetic world structurally relevant?</div><div class='copy'>Real datasets are used as shape anchors, not as training targets and not as known population truth.</div></div>
      </div>
      <div class='grid2' style='margin-top:15px'>
        <div class='card'><div class='smallhead'>FAIR COMPARISON</div><div class='copy'>Within a Monte Carlo replicate, every estimator sees the same generated sample. Differences therefore come from the estimator, not from different random samples.</div></div>
        <div class='card'><div class='smallhead'>REPRODUCIBILITY</div><div class='copy'>Fixed seeds and logged regime settings make the error surface auditable and repeatable.</div></div>
      </div>
      <div class='warn'><b>What do the 29 warnings mean?</b> They are retained diagnostics, not hidden failures. A warning marks an explainable edge case that deserves interpretation; a hard failure would invalidate the condition.</div>
    </div>"""


def _appendix_c() -> str:
    return _css() + f"""
    <div class='page'>
      <div class='kicker'>APPENDIX C · GA CODE</div><div class='title'>What did the actual thesis GA do?</div>
      <div class='grid3'>
        <div class='card blue'><div class='smallhead'>REPRESENTATION</div><div class='formula'>T<sub>mix</sub> = Cw</div><div class='copy'>Rows of C are Monte Carlo replications; columns are named base estimators. The GA searches weights, not raw observations.</div></div>
        <div class='card purple'><div class='smallhead'>INITIALIZATION</div><div class='formula'>w⁽⁰⁾ ~ Dirichlet(α·1)</div><div class='copy'>Every chromosome is simplex-valid by construction. Confirmed priors may enter as warm starts but receive no automatic win.</div></div>
        <div class='card green'><div class='smallhead'>ACCEPTANCE</div><div class='formula'>ΔMSE ≥ 0 AND Δq95 ≥ 0</div><div class='copy'>Fitness guides the search. Held-out evidence controls the claim.</div></div>
      </div>
      <div class='sectionbar'>Evolutionary operators</div>
      <div class='grid4'>
        <div class='card'><div class='smallhead'>SELECTION</div><div class='big'>Tournament</div><div class='copy'>Better candidates are more likely to reproduce.</div></div>
        <div class='card'><div class='smallhead'>CROSSOVER</div><div class='big'>Convex</div><div class='copy'>child = λpA + (1−λ)pB keeps offspring inside the simplex.</div></div>
        <div class='card'><div class='smallhead'>MUTATION</div><div class='big'>Dirichlet nudge</div><div class='copy'>A fresh simplex direction perturbs the child while preserving valid weights.</div></div>
        <div class='card'><div class='smallhead'>DIVERSITY</div><div class='big'>Elitism + immigration</div><div class='copy'>Strong candidates survive while fresh simplex vectors prevent collapse.</div></div>
      </div>
      <div class='sectionbar'>Final search configuration</div>
      <div class='metricrow'><div class='metric'><div class='v'>100</div><div class='l'>population N</div></div><div class='metric'><div class='v'>20</div><div class='l'>generations / fold</div></div><div class='metric'><div class='v'>3</div><div class='l'>folds K</div></div><div class='metric'><div class='v'>101 / 202</div><div class='l'>discovery seeds</div></div></div>
      <div class='pillrow'><span class='pill'>Dirichlet α = 0.5 or 1.0</span><span class='pill'>Tournament = 2 or 3</span><span class='pill'>Elitism = 1 or 2</span><span class='pill'>Mutation μ₀ = 0.12 or 0.18</span><span class='pill'>μmin = 0.05</span><span class='pill'>Immigration = 5–10% every 15 generations</span><span class='pill'>Early-stop checks every 5 generations</span></div>
      <div class='takehome'>Fitness answers: <b>“where should the GA search next?”</b> &nbsp; The gate answers: <b>“is the scientific replacement claim allowed?”</b></div>
    </div>"""


def _appendix_d() -> str:
    return _css() + f"""
    <div class='page'>
      <div class='kicker'>APPENDIX D · METRICS AND GATE</div><div class='title'>How is a candidate judged?</div>
      <div class='grid3'>
        <div class='card blue'><div class='smallhead'>TARGET</div><div class='formula'>θ(F) = μ<sub>F</sub> = E<sub>F</sub>[X]</div><div class='copy'>The estimand is fixed. The regime changes; the definition of success does not.</div></div>
        <div class='card green'><div class='smallhead'>AVERAGE RISK</div><div class='formula'>MSE = E[(θ̂−θ)²]</div><div class='copy'>Typical finite-sample squared error across repeated samples.</div></div>
        <div class='card purple'><div class='smallhead'>DIFFICULT-CASE RISK</div><div class='formula'>q<sub>.95</sub>({(θ̂−θ)²})</div><div class='copy'>The upper-tail error boundary. q95 is an error-risk metric — not a p-value and not a confidence interval.</div></div>
      </div>
      <div class='formula'>Gain% = 100 × (Risk<sub>benchmark</sub> − Risk<sub>candidate</sub>) / Risk<sub>benchmark</sub></div>
      <div class='grid2'>
        <div class='card green'><div class='smallhead'>DUAL BENCHMARK GATE</div><div class='big'>PASS only if both criteria support replacement</div><div class='copy'>gain_MSE ≥ 0 <b>AND</b> gain_q95 ≥ 0. Improving only one metric is insufficient.</div></div>
        <div class='card blue'><div class='smallhead'>BOOTSTRAP EVIDENCE</div><div class='big'>CI around gain</div><div class='copy'>Paired bootstrap intervals quantify uncertainty around benchmark-minus-candidate improvement. Intervals crossing zero weaken a replacement claim.</div></div>
      </div>
      <div class='sectionbar'>Benchmark families</div>
      <div class='pillrow'><span class='pill'>Mean · efficient clean baseline</span><span class='pill'>Median · high robustness</span><span class='pill'>Trimmed / Winsorized</span><span class='pill'>Huber / Biweight</span><span class='pill'>Catoni</span><span class='pill'>Median-of-Means</span><span class='pill'>Trimean / HSM / Parzen where admissible</span></div>
      <div class='warn'><b>Admissibility matters:</b> support restrictions are respected. For example, geometric and harmonic means require positive observations. The comparator is the best admissible benchmark, not a weak baseline.</div>
    </div>"""


def _appendix_e_summary() -> str:
    return _css() + f"""
    <div class='page' style='min-height:570px'>
      <div class='kicker'>APPENDIX E · RESULTS</div><div class='title'>Evidence map: where did the claim narrow?</div>
      <div class='chain'>
        <div class='node'><b>Cycle I</b><br>36 → 16 → 2 confirmed</div><div class='arrow'>→</div>
        <div class='node'><b>Cycle II</b><br>10 → 26 basis · 12 discovery</div><div class='arrow'>→</div>
        <div class='node'><b>Frozen II</b><br>2 Weibull transfer specialists</div><div class='arrow'>→</div>
        <div class='node'><b>External</b><br>26/43 parents · 255 confirmations</div>
      </div>
      <div class='grid3'>
        <div class='card green'><div class='smallhead'>FROZEN CONFIRMATION I</div><div class='big'>CV-019 · +16.3% q95</div><div class='copy'>CV-010 also survives at +2.2% q95. Both are Lognormal and survive 8/8 validation seeds.</div></div>
        <div class='card purple'><div class='smallhead'>STRICT VALIDATION</div><div class='big'>2 transfer specialists</div><div class='copy'>FWVR011 and FWVR012 pass in related locked-unseen Weibull regimes while failing original-regime mode — narrow transfer, not family-wide superiority.</div></div>
        <div class='card blue'><div class='smallhead'>ABSTENTION AUDIT</div><div class='big'>23 / 34 no random pass</div><div class='copy'>11/34 show some random signal; all 8/8 strongest positive controls pass.</div></div>
      </div>
      <div class='takehome'>Harder evidence makes the claim <b>smaller and more credible</b>: discovery opportunity → frozen confirmation → local transfer → external calibration → abstention audit.</div>
    </div>"""


def _appendix_f() -> str:
    questions = [
        ("Isn't simulation artificial?", "It is deliberate. True estimator error requires a known θ. Real data are used later for robustness and transfer, not known-truth calibration."),
        ("Why use a GA at all?", "Because the search space is a constrained mixture of many named estimators. The GA explores that simplex while keeping the final recipe interpretable."),
        ("Is q95 a p-value?", "No. q95 is the 95th percentile of squared error. It measures difficult-case risk."),
        ("Why not just pick the estimator with the lowest discovery MSE?", "Because discovery is adaptive. The candidate must be frozen and challenged again before the result becomes a defensible replacement claim."),
        ("How can locked-unseen pass while original-regime mode fails?", "Performance is regime-conditional. A frozen recipe can transfer to one related profile without being uniformly good across the whole family."),
        ("Does benchmark retention mean the GA failed?", "No. Retention is an intended result when the gate finds no defensible opportunity to replace the best admissible benchmark."),
        ("How can real data validate anything without true θ?", "They cannot provide known-truth error. The external layer tests robustness and profile transfer against a full-sample empirical reference."),
        ("What do the 11 of 34 Dirichlet-signal cells mean?", "They are honest follow-up targets. Random search found some composite opportunity there, so those abstentions deserve another look; the audit does not automatically overturn them."),
        ("What is the single strongest contribution?", "A disciplined framework for knowing when a composite estimator is justified and when the benchmark should remain the answer."),
        ("What would you do next?", "Broaden structural coverage, test more empirical domains, study specialist-selection rules, and investigate whether transfer regions can be predicted before running a full search."),
    ]
    qa = "".join(f"<div class='qa'><div class='q'>{html.escape(q)}</div><div class='a'>{html.escape(a)}</div></div>" for q,a in questions)
    return _css() + f"""
    <div class='page'>
      <div class='kicker'>APPENDIX F · Q&A</div><div class='title'>Likely committee questions — short answers first.</div>
      <div class='subtitle'>Use these as speaking prompts, not as a script. Start with the first sentence; expand only if the examiner wants more detail.</div>
      <div class='grid2'>{qa}</div>
    </div>"""


def _render_candidate_explorer() -> None:
    decisions_path = ROOT / "data/raw/validation/final_decision_table.csv"
    ci_path = ROOT / "data/raw/validation/bootstrap_ci.csv"
    evidence_path = ROOT / "data/raw/evidence/evidence_taxonomy_all_candidates.csv"
    winners_path = ROOT / "data/processed/winners_all.csv"
    if not decisions_path.exists():
        st.info("Candidate-level validation files are not exported in this dashboard bundle.")
        return

    decisions = pd.read_csv(decisions_path)
    ci = pd.read_csv(ci_path) if ci_path.exists() else pd.DataFrame()
    evidence = pd.read_csv(evidence_path) if evidence_path.exists() else pd.DataFrame()
    winners = pd.read_csv(winners_path) if winners_path.exists() else pd.DataFrame()

    st.markdown("### Candidate-level evidence explorer")
    st.caption("Backup only · fixed thesis outputs · no candidate is retrained here.")
    ids = [x for x in decisions.get("validation_id", pd.Series(dtype=str)).dropna().astype(str).unique()]
    if not ids:
        st.info("No validation IDs are available.")
        return
    vid = st.selectbox("Validation candidate", ids, key="appendix_candidate_id")
    dr = decisions[decisions["validation_id"].astype(str) == vid].iloc[0]
    er = evidence[evidence.get("validation_id", pd.Series(dtype=str)).astype(str) == vid] if not evidence.empty and "validation_id" in evidence else pd.DataFrame()

    c1, c2, c3 = st.columns(3)
    c1.metric("Final decision", str(dr.get("final_fixed_weight_validation_decision", "Not exported")))
    c2.metric("Original gate", str(dr.get("expanded_gate_pass_mean.original_regime", "Not exported")))
    c3.metric("Locked-unseen gate", str(dr.get("expanded_gate_pass_mean.locked_unseen_similar", "Not exported")))
    if not er.empty:
        st.info(f"Evidence taxonomy: {er.iloc[0].get('evidence_grade','Not exported')} · {er.iloc[0].get('interpretive_note','')}")

    if not ci.empty and "validation_id" in ci:
        sub = ci[ci["validation_id"].astype(str) == vid]
        if not sub.empty and all(c in sub.columns for c in ["validation_mode","mean_gain","validation_seed","mean_gain_ci_high","mean_gain_ci_low"]):
            fig = go.Figure()
            for mode, color in [("original_regime", COLORS["red"]), ("locked_unseen_similar", COLORS["blue"])]:
                x = sub[sub["validation_mode"].astype(str) == mode]
                if x.empty:
                    continue
                fig.add_trace(go.Scatter(
                    x=x["mean_gain"], y=x["validation_seed"], mode="markers", name=mode,
                    error_x=dict(type="data", symmetric=False,
                                 array=x["mean_gain_ci_high"]-x["mean_gain"],
                                 arrayminus=x["mean_gain"]-x["mean_gain_ci_low"]),
                    marker=dict(size=9, color=color),
                ))
            fig.add_vline(x=0, line_dash="dash")
            fig.update_layout(title="Mean gain with paired bootstrap CI", height=390,
                              xaxis_title="Mean gain", yaxis_title="Validation seed",
                              plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                              font_color=COLORS["text"])
            st.plotly_chart(fig, use_container_width=True)

    if not winners.empty and "specialist_regime_id" in winners.columns:
        matching = winners[winners["specialist_regime_id"].astype(str).str.contains(vid, case=False, na=False)]
        if not matching.empty:
            row = matching.iloc[0]
            weight_cols = [c for c in winners.columns if c.startswith("w_")]
            vals = []
            for c in weight_cols:
                try:
                    v = float(row[c])
                except Exception:
                    continue
                if v > 0:
                    vals.append((c[2:], v))
            vals.sort(key=lambda z: z[1], reverse=True)
            if vals:
                wf = go.Figure(go.Bar(x=[v for _,v in vals], y=[n for n,_ in vals], orientation="h"))
                wf.update_layout(title="Frozen weight vector", height=max(320, 24*len(vals)),
                                 yaxis=dict(autorange="reversed"), xaxis_title="Weight",
                                 plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                                 font_color=COLORS["text"])
                st.plotly_chart(wf, use_container_width=True)


def _simple_notes(title: str, sections: Iterable[tuple[str, Iterable[str]]], questions: Iterable[tuple[str,str]]) -> str:
    sec_html = ""
    for heading, items in sections:
        lis = "".join(f"<li>{html.escape(str(x))}</li>" for x in items)
        sec_html += f"<div class='helpsec'><h2>{html.escape(heading)}</h2><ul>{lis}</ul></div>"
    q_html = "".join(f"<div class='qa'><div class='q'>{html.escape(q)}</div><div class='a'>{html.escape(a)}</div></div>" for q,a in questions)
    return f"""<style>
    body{{background:#071525;color:#eef5ff;font-family:Arial,sans-serif;margin:0}}.wrap{{max-width:1050px;margin:auto;padding:25px}}
    h1{{font-size:2rem;color:#fff}}.helpsec{{background:#0b2138;border:1px solid #356e99;border-left:5px solid #f3c743;border-radius:12px;padding:1rem 1.35rem;margin:0 0 1rem}}
    .helpsec h2{{font-size:1.05rem;letter-spacing:.08em;color:#f3c743}}li{{font-size:1.18rem;line-height:1.45;margin:.45rem 0}}
    .qa{{background:#091a2e;border:1px solid #2f6287;border-radius:10px;padding:.9rem 1.1rem;margin:.75rem 0}}.q{{font-size:1.12rem;font-weight:800;color:#72cfff}}.a{{font-size:1.08rem;line-height:1.42;margin-top:.35rem;color:#e4eef8}}
    </style><div class='wrap'><h1>{html.escape(title)}</h1>{sec_html}<div class='helpsec'><h2>POSSIBLE QUESTIONS</h2>{q_html}</div></div>"""


def _presenter_notes(section: str) -> str | None:
    if section == "conclusions_claims":
        return _simple_notes("Layer 8 · Claims", [
            ("WHAT AM I LOOKING AT?", ["This closes H1 to H4. The point is not that the GA wins everywhere; the point is that the evidence behaves exactly like a regime-conditional framework should."]),
            ("HOW DO I SAY IT?", ["H1, H2 and H4 are supported. H3 has conservative support because the gains are real but narrow.", "Harder evidence made the claim smaller, which makes it more credible."]),
            ("WHAT SHOULD I NOT CLAIM?", ["Do not say the GA is universally better.", "Do not turn specialist evidence into a family-wide claim."]),
        ], [("What is the main conclusion?", "No universal winner exists; the framework identifies conditional opportunity and retains the benchmark when replacement is unsupported."), ("Why conservative support for H3?", "Because the GA gains survive, but only in narrow validated profiles.")])
    if section == "conclusions_contrib":
        return _simple_notes("Layer 8 · Contributions & limits", [
            ("WHAT AM I LOOKING AT?", ["Three contributions: statistical, AI, and methodological. The bottom band names the limits before the committee has to ask."]),
            ("HOW DO I SAY IT?", ["Statistically, I keep E[X] fixed and search for regime-aware robust mixtures.", "From AI, I contribute interpretable evolutionary search over simplex weights.", "Methodologically, I contribute staged validation and claim control."]),
            ("WHAT ARE THE LIMITS?", ["Known truth is simulated.", "Confirmed effects are narrow.", "Transfer is profile-dependent.", "Real data use a reference mean rather than known population theta."]),
        ], [("What is the single strongest contribution?", "A reproducible framework that knows when to claim improvement and when to keep the benchmark."), ("What would you extend next?", "Broader structural coverage, more empirical domains, and methods for predicting transfer regions before a full search.")])

    appendix_notes = {
        "appendix_A": ("Appendix A · Simulation", ["Use this if they ask why simulation is necessary, what a regime is, or how Monte Carlo produces MSE and q95.", "Key sentence: simulation gives known theta; every estimator sees the same replicate."], [("Is simulation artificial?", "It is deliberate because true estimator error requires known theta.")]),
        "appendix_B": ("Appendix B · Validity", ["Use this if they challenge the generator or reproducibility.", "Remember the numbers: 125 checks, 0 hard failures, 29 warnings, maximum mean error 0.976%."], [("Do warnings mean failure?", "No. They are retained diagnostic cases; hard failures are counted separately and there were zero.")]),
        "appendix_C": ("Appendix C · GA code", ["Use this for operators, hyperparameters, or why the GA remains interpretable.", "Key sentence: the GA searches weights over C; fitness guides search and the held-out gate controls acceptance."], [("Is the GA a black box?", "No. The output is a simplex weight vector over named estimators.")]),
        "appendix_D": ("Appendix D · Metrics & gate", ["Use this for MSE, q95, effect size, benchmark admissibility or bootstrap questions.", "Key sentence: q95 is tail-risk error, not a p-value; both MSE and q95 must support replacement."], [("Why require both metrics?", "To prevent a candidate from winning on average while failing badly in difficult cases.")]),
        "appendix_E": ("Appendix E · Results", ["Use this when they want exact candidate-level evidence or confidence intervals.", "Start with the evidence map, then open the candidate explorer only if they want detail."], [("Why does the claim narrow?", "Because each frozen stage applies harder evidence without allowing the candidate to adapt.")]),
        "appendix_F": ("Appendix F · Q&A", ["Short answers first. Expand only when asked.", "The recurring theme is conditional improvement, frozen validation, and honest benchmark retention."], [("What is the practical value?", "Honest conditional estimator discovery and claim control.")]),
    }
    if section in appendix_notes:
        title, bullets, qs = appendix_notes[section]
        return _simple_notes(title, [("HELP", bullets)], qs)
    return None


def _render_layer8() -> None:
    st.markdown("""<style>
    .layer8-nav .stButton>button{min-height:3.6rem!important;font-size:1.05rem!important;font-weight:800!important}
    </style>""", unsafe_allow_html=True)
    if "conclusion_view" not in st.session_state:
        st.session_state.conclusion_view = "claims"
    st.markdown('<span class="badge thesis">DISCUSSION — close the timed defense</span>', unsafe_allow_html=True)
    st.markdown('<div class="layer8-nav">', unsafe_allow_html=True)
    a,b = st.columns(2)
    with a:
        if st.button("Claims · H1–H4", key="conclusion_claims", use_container_width=True, type="primary" if st.session_state.conclusion_view == "claims" else "secondary"):
            st.session_state.conclusion_view = "claims"; st.rerun()
    with b:
        if st.button("Contributions & Limits", key="conclusion_contrib", use_container_width=True, type="primary" if st.session_state.conclusion_view == "contrib" else "secondary"):
            st.session_state.conclusion_view = "contrib"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    html_doc = _conclusion_claims_html() if st.session_state.conclusion_view == "claims" else _conclusion_contrib_html()
    components.html(html_doc, height=735, scrolling=False)
    st.markdown("---")
    left,right = st.columns([3,1])
    with left:
        st.info("End of timed defense. Stop here, thank the committee, and open the technical appendix only if a question requires it.")
    with right:
        if st.button("Technical Appendix →", type="primary", use_container_width=True, key="open_appendix"):
            st.session_state.defense_section = _LAYER9; st.rerun()


def _render_layer9() -> None:
    st.markdown("""<style>
    .appendix-nav .stButton>button{min-height:3.8rem!important;padding:.55rem .35rem!important;font-size:.92rem!important;line-height:1.15!important;font-weight:800!important;white-space:normal!important}
    </style>""", unsafe_allow_html=True)
    if "appendix_section" not in st.session_state:
        st.session_state.appendix_section = 0
    st.markdown('<span class="badge thesis">TECHNICAL APPENDIX — use only when asked</span>', unsafe_allow_html=True)
    st.caption("A–F mirrors the defense deck: simulation, validity, GA mechanics, metrics, results, and committee Q&A.")
    st.markdown('<div class="appendix-nav">', unsafe_allow_html=True)
    cols = st.columns(6, gap="small")
    for i,label in enumerate(APPENDIX_LABELS):
        with cols[i]:
            if st.button(label, key=f"appendix_nav_{i}", use_container_width=True, type="primary" if st.session_state.appendix_section == i else "secondary"):
                st.session_state.appendix_section = i; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    sec = int(st.session_state.appendix_section)
    docs = (_appendix_a, _appendix_b, _appendix_c, _appendix_d, _appendix_e_summary, _appendix_f)
    heights = (880, 780, 860, 780, 610, 1040)
    components.html(docs[sec](), height=heights[sec], scrolling=True if sec == 5 else False)
    if sec == 4:
        st.markdown("---")
        open_explorer = st.toggle("Open candidate-level evidence explorer", value=False, key="appendix_results_explorer")
        if open_explorer:
            _render_candidate_explorer()


def install_layer89_pages() -> None:
    """Render Layer 8/9 after the sidebar is complete and stop legacy page blocks."""
    if getattr(st, "_layer89_pages_installed", False):
        return
    st._layer89_pages_installed = True

    base_markdown = st.markdown
    base_warning = st.warning
    armed = False
    rendering = False

    def markdown(body, *args, **kwargs):
        nonlocal armed, rendering
        if rendering:
            return base_markdown(body, *args, **kwargs)
        text = str(body)
        active = st.session_state.get("defense_section")
        # The presenter-notes logo is the last markdown call in the sidebar.
        if active in (_LAYER8, _LAYER9) and "presenter_notes=1" in text:
            if active == _LAYER8:
                key = "conclusions_contrib" if st.session_state.get("conclusion_view", "claims") == "contrib" else "conclusions_claims"
                text = text.replace("section=conclusions", f"section={key}")
            else:
                letter = "ABCDEF"[max(0,min(int(st.session_state.get("appendix_section",0)),5))]
                text = text.replace("section=technical", f"section=appendix_{letter}")
            armed = True
            return base_markdown(text, *args, **kwargs)

        if armed and active in (_LAYER8, _LAYER9):
            armed = False
            rendering = True
            try:
                if active == _LAYER8:
                    _render_layer8()
                else:
                    _render_layer9()
            finally:
                rendering = False
            st.stop()
        return base_markdown(body, *args, **kwargs)

    def warning(body, *args, **kwargs):
        try:
            qp = st.query_params
            presenter = str(qp.get("presenter_notes", "")) == "1"
            section = str(qp.get("section", ""))
        except Exception:
            presenter, section = False, ""
        if presenter:
            note = _presenter_notes(section)
            if note is not None and "No hay notas configuradas" in str(body):
                return base_markdown(note, unsafe_allow_html=True)
        return base_warning(body, *args, **kwargs)

    st.markdown = markdown
    st.warning = warning
