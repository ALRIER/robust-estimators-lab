"""Direct renderer for Layer 9 · Technical drill-down.

Single current implementation of the technical appendix. It contains no compatibility
hooks and never reruns the thesis GA.
"""

from pathlib import Path
import html
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
    "A · Simulation", "B · Validity", "C · GA code",
    "D · Metrics & gate", "E · Results", "F · Q&A",
)


def _css() -> str:
    return """
    <style>
      *{box-sizing:border-box} body{margin:0;background:#081525;color:#e9f4ff;font-family:Arial,sans-serif}
      .page{padding:20px 22px 26px;background:#081525}.kicker{font-size:13px;font-weight:900;letter-spacing:.12em;color:#72cfff;margin-bottom:7px}
      .title{font-size:30px;font-weight:900;color:#fff;line-height:1.15;margin-bottom:8px}.subtitle{font-size:15px;line-height:1.42;color:#b9c8d9;margin-bottom:18px}
      .grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
      .card{background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:12px;padding:15px 16px;min-height:135px}.small{font-size:11px;font-weight:900;letter-spacing:.10em;color:#72cfff;margin-bottom:7px}.big{font-size:22px;font-weight:900;line-height:1.16;color:#fff;margin-bottom:7px}.copy{font-size:14px;line-height:1.43;color:#dce9f8}
      .metricrow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:14px 0}.metric{background:#10253a;border:1px solid #356e99;border-radius:10px;padding:12px;text-align:center}.v{font-size:25px;font-weight:900;color:#f3c743}.l{font-size:12px;color:#b9c8d9;margin-top:4px;font-weight:700}
      .formula{font-family:Georgia,serif;font-size:21px;font-weight:700;color:#f7d768;background:#0a1d32;border:1px solid #356e99;border-radius:9px;padding:11px 13px;margin:10px 0}
      .section{background:#102a49;border:1px solid #3c7198;border-left:5px solid #72cfff;border-radius:10px;padding:11px 14px;margin:15px 0 11px;font-size:15px;font-weight:900;color:#fff}
      .pillrow{display:flex;gap:8px;flex-wrap:wrap}.pill{background:#10253a;border:1px solid #356e99;border-radius:18px;padding:7px 10px;font-size:12px;font-weight:800;color:#e6f1fb}
      .warn{background:#342b12;border:1px solid #f3c743;color:#fff0af;border-radius:10px;padding:12px 14px;font-size:14px;line-height:1.4;margin-top:12px}
      .code{font-family:Consolas,monospace;font-size:13px;line-height:1.48;background:#06101d;border:1px solid #355a78;border-radius:10px;padding:13px 15px;color:#d7e8f6;white-space:pre-wrap}
      .chain{display:flex;align-items:center;gap:8px;margin:14px 0}.node{flex:1;background:#10253a;border:1px solid #3c7198;border-radius:10px;padding:10px;text-align:center;font-weight:800;font-size:13px}.arrow{font-size:22px;color:#72cfff;font-weight:900}
      .qa{background:#0b2138;border:1px solid #356e99;border-radius:10px;padding:12px 14px;margin-bottom:10px}.q{font-size:14px;font-weight:900;color:#72cfff;margin-bottom:4px}.a{font-size:13px;line-height:1.42;color:#dce9f8}
      @media(max-width:1000px){.grid4,.grid3,.grid2,.metricrow{grid-template-columns:1fr 1fr}}
    </style>
    """


def _a_simulation() -> str:
    return _css() + """
    <div class='page'><div class='kicker'>APPENDIX A · SIMULATION</div><div class='title'>Why Monte Carlo — and what world was simulated?</div>
      <div class='grid3'>
        <div class='card'><div class='small'>CONTROLLED TRUTH</div><div class='big'>θ = E[X]</div><div class='copy'>The data-generating distribution defines the true population mean before any estimator is scored.</div></div>
        <div class='card'><div class='small'>DIRECT ERROR</div><div class='big'>Estimator vs. truth</div><div class='copy'>MSE and q95 are measured against θ rather than against a proxy.</div></div>
        <div class='card'><div class='small'>SYSTEMATIC STRESS TEST</div><div class='big'>Regime grid</div><div class='copy'>Family, n, contamination rate, outlier scale and mechanism are varied deliberately.</div></div>
      </div>
      <div class='section'>Distributional world</div>
      <div class='pillrow'><span class='pill'>Normal</span><span class='pill'>Lognormal</span><span class='pill'>Weibull</span><span class='pill'>Inverse Gaussian</span><span class='pill'>Ex-Gaussian</span><span class='pill'>Ex-Wald</span></div>
      <div class='metricrow'><div class='metric'><div class='v'>6</div><div class='l'>families</div></div><div class='metric'><div class='v'>5</div><div class='l'>sample sizes</div></div><div class='metric'><div class='v'>576</div><div class='l'>profiles / family</div></div><div class='metric'><div class='v'>2880</div><div class='l'>regimes / family</div></div></div>
      <div class='formula'>ℛ = (F₀, γ, c, m, n) &nbsp;→&nbsp; Fℛ = (1−γ)F₀ + γG<sub>m,c</sub>(F₀)</div>
      <div class='section'>Monte Carlo measurement engine</div>
      <div class='code'>for regime in grid:
    θ = analytic_mean(regime)
    for r in 1:R:
        x = simulate_sample(regime, seed_r)
        T = apply_all_estimators(x)   # same replicate for every estimator
        err2 = (T - θ)^2
    MSE = mean(err2)
    q95 = quantile(err2, 0.95)</div>
      <div class='warn'><b>Why simulation is deliberate:</b> real datasets do not reveal the population mean. They are used later for external robustness, not known-truth calibration.</div>
    </div>"""


def _b_validity() -> str:
    return _css() + """
    <div class='page'><div class='kicker'>APPENDIX B · VALIDITY</div><div class='title'>How do we know the simulated world is trustworthy?</div>
      <div class='metricrow'><div class='metric'><div class='v'>125</div><div class='l'>validation conditions</div></div><div class='metric'><div class='v' style='color:#54c786'>0</div><div class='l'>hard failures</div></div><div class='metric'><div class='v'>29</div><div class='l'>explainable warnings</div></div><div class='metric'><div class='v'>0.976%</div><div class='l'>max mean error</div></div></div>
      <div class='grid2'>
        <div class='card'><div class='small'>1 · MOMENT FIDELITY</div><div class='big'>Does the generator recover θ?</div><div class='copy'>Large generated populations recover analytic moments; maximum mean error remained below the 1% hard threshold.</div></div>
        <div class='card'><div class='small'>2 · CONTAMINATION FIDELITY</div><div class='big'>Does the regime behave as labelled?</div><div class='copy'>Realised rate, direction and MAD-based distance are checked after contamination injection.</div></div>
        <div class='card'><div class='small'>3 · THEORY RECOVERY</div><div class='big'>Do known patterns reappear?</div><div class='copy'>Classical robust-statistics behaviour is recovered before GA conclusions are interpreted.</div></div>
        <div class='card'><div class='small'>4 · EMPIRICAL ANCHORING</div><div class='big'>Is the synthetic world relevant?</div><div class='copy'>Real datasets act as structural shape anchors, not training targets and not known population truth.</div></div>
      </div>
      <div class='grid2' style='margin-top:14px'><div class='card'><div class='small'>FAIR COMPARISON</div><div class='copy'>Within a replicate, every estimator sees the same generated sample path.</div></div><div class='card'><div class='small'>REPRODUCIBILITY</div><div class='copy'>Fixed seeds and logged regime settings make the error surface auditable and repeatable.</div></div></div>
      <div class='warn'><b>29 warnings ≠ 29 failures.</b> Warnings are retained diagnostics for explainable edge cases; hard failures are counted separately and there were zero.</div>
    </div>"""


def _c_ga() -> str:
    return _css() + """
    <div class='page'><div class='kicker'>APPENDIX C · GA CODE</div><div class='title'>What did the actual thesis GA do?</div>
      <div class='grid3'>
        <div class='card'><div class='small'>REPRESENTATION</div><div class='formula'>T<sub>mix</sub> = Cw</div><div class='copy'>Rows of C are Monte Carlo replications; columns are named estimators. The GA searches weights, not raw observations.</div></div>
        <div class='card'><div class='small'>INITIALIZATION</div><div class='formula'>w⁽⁰⁾ ~ Dirichlet(α·1)</div><div class='copy'>Every chromosome is simplex-valid by construction. Warm starts compete without automatic privilege.</div></div>
        <div class='card'><div class='small'>ACCEPTANCE</div><div class='formula'>ΔMSE ≥ 0 AND Δq95 ≥ 0</div><div class='copy'>Fitness guides search; held-out evidence controls the claim.</div></div>
      </div>
      <div class='section'>Evolutionary operators</div>
      <div class='grid4'><div class='card'><div class='small'>SELECTION</div><div class='big'>Tournament</div><div class='copy'>Better candidates are more likely to reproduce.</div></div><div class='card'><div class='small'>CROSSOVER</div><div class='big'>Convex</div><div class='copy'>λpA+(1−λ)pB stays inside the simplex.</div></div><div class='card'><div class='small'>MUTATION</div><div class='big'>Dirichlet nudge</div><div class='copy'>A fresh simplex direction perturbs a child while preserving valid weights.</div></div><div class='card'><div class='small'>DIVERSITY</div><div class='big'>Elitism + immigration</div><div class='copy'>Strong candidates survive while fresh vectors prevent collapse.</div></div></div>
      <div class='section'>Search configuration</div>
      <div class='pillrow'><span class='pill'>Population 100</span><span class='pill'>20 generations / fold</span><span class='pill'>3 folds</span><span class='pill'>Dirichlet α 0.5 or 1.0</span><span class='pill'>Tournament 2 or 3</span><span class='pill'>Mutation μ₀ 0.12 or 0.18</span><span class='pill'>μmin 0.05</span><span class='pill'>Immigration 5–10%</span></div>
      <div class='warn'><b>Key distinction:</b> fitness answers “where should the GA search next?” The held-out gate answers “is the replacement claim allowed?”</div>
    </div>"""


def _d_metrics() -> str:
    return _css() + """
    <div class='page'><div class='kicker'>APPENDIX D · METRICS AND GATE</div><div class='title'>How is a candidate judged?</div>
      <div class='grid3'><div class='card'><div class='small'>TARGET</div><div class='formula'>θ(F)=μF=E<sub>F</sub>[X]</div><div class='copy'>The estimand is fixed; the regime changes.</div></div><div class='card'><div class='small'>AVERAGE RISK</div><div class='formula'>MSE=E[(θ̂−θ)²]</div><div class='copy'>Typical finite-sample squared error.</div></div><div class='card'><div class='small'>DIFFICULT-CASE RISK</div><div class='formula'>q<sub>.95</sub> of squared error</div><div class='copy'>Upper-tail error risk. q95 is not a p-value.</div></div></div>
      <div class='formula'>Gain% = 100 × (Risk<sub>benchmark</sub> − Risk<sub>candidate</sub>) / Risk<sub>benchmark</sub></div>
      <div class='grid2'><div class='card'><div class='small'>DUAL BENCHMARK GATE</div><div class='big'>Both criteria must support replacement</div><div class='copy'>gain_MSE ≥ 0 <b>AND</b> gain_q95 ≥ 0.</div></div><div class='card'><div class='small'>BOOTSTRAP EVIDENCE</div><div class='big'>CI around gain</div><div class='copy'>Paired bootstrap intervals quantify uncertainty. Intervals crossing zero weaken the replacement claim.</div></div></div>
      <div class='section'>Benchmark families</div><div class='pillrow'><span class='pill'>Mean</span><span class='pill'>Median</span><span class='pill'>Trimmed / Winsorized</span><span class='pill'>Huber / Biweight</span><span class='pill'>Catoni</span><span class='pill'>Median-of-Means</span><span class='pill'>Trimean / HSM / Parzen where admissible</span></div>
      <div class='warn'><b>Admissibility matters:</b> the comparator is the best admissible benchmark, not a deliberately weak baseline.</div>
    </div>"""


def _e_results() -> str:
    return _css() + """
    <div class='page'><div class='kicker'>APPENDIX E · RESULTS</div><div class='title'>Evidence map: where did the claim narrow?</div>
      <div class='chain'><div class='node'>Cycle I<br>36 → 16 → 2</div><div class='arrow'>→</div><div class='node'>Cycle II<br>26-component basis · 12 discovery</div><div class='arrow'>→</div><div class='node'>Frozen II<br>2 Weibull transfer specialists</div><div class='arrow'>→</div><div class='node'>External<br>26/43 · 255 confirmations</div></div>
      <div class='grid3'><div class='card'><div class='small'>FROZEN CONFIRMATION I</div><div class='big'>CV-019 · +16.3% q95</div><div class='copy'>CV-010 also survives at +2.2% q95. Both are Lognormal and survive 8/8 validation seeds.</div></div><div class='card'><div class='small'>STRICT VALIDATION</div><div class='big'>2 transfer specialists</div><div class='copy'>FWVR011 and FWVR012 pass related locked-unseen Weibull regimes while failing original-regime mode.</div></div><div class='card'><div class='small'>ABSTENTION AUDIT</div><div class='big'>23 / 34 no random pass</div><div class='copy'>11/34 show some signal; 8/8 strongest positive controls pass.</div></div></div>
      <div class='warn'><b>Interpretation:</b> harder evidence makes the claim smaller and more credible.</div>
    </div>"""


def _f_qa() -> str:
    qs = [
        ("Isn't simulation artificial?", "It is deliberate: true estimator error requires a known θ. Real data are used later for robustness and transfer."),
        ("Why use a GA?", "Because the search space is a constrained mixture of many named estimators; the final simplex recipe remains interpretable."),
        ("Is q95 a p-value?", "No. It is the 95th percentile of squared error and measures difficult-case risk."),
        ("Why freeze candidates?", "Discovery is adaptive. The exact weights must face fresh evidence without retraining before a replacement claim is defensible."),
        ("How can locked-unseen pass while original mode fails?", "Performance is regime-conditional. Transfer can be local without implying family-wide superiority."),
        ("Does benchmark retention mean the GA failed?", "No. Retention is an intended scientific outcome when replacement is unsupported."),
        ("How can real data help without true θ?", "They support robustness and transfer against an empirical reference, not known-truth error recovery."),
        ("What do the 11/34 Dirichlet-signal cells mean?", "They are honest follow-up targets; random search found some opportunity there, so those abstentions deserve another look."),
        ("Strongest contribution?", "A disciplined framework for knowing when a composite is justified and when the benchmark should remain the answer."),
        ("What next?", "Broader structural coverage, more empirical domains, and better rules for predicting specialist transfer regions."),
    ]
    qa = "".join(f"<div class='qa'><div class='q'>{html.escape(q)}</div><div class='a'>{html.escape(a)}</div></div>" for q,a in qs)
    return _css() + f"<div class='page'><div class='kicker'>APPENDIX F · Q&A</div><div class='title'>Likely committee questions — short answers first.</div><div class='subtitle'>Use these as speaking prompts. Expand only when the examiner asks for more.</div><div class='grid2'>{qa}</div></div>"


def _set_section(section: int) -> None:
    st.session_state.appendix_section = section


def _candidate_explorer() -> None:
    decisions_path = ROOT / "data/raw/validation/final_decision_table.csv"
    ci_path = ROOT / "data/raw/validation/bootstrap_ci.csv"
    evidence_path = ROOT / "data/raw/evidence/evidence_taxonomy_all_candidates.csv"
    if not decisions_path.exists():
        st.info("Candidate-level validation files are not exported in this dashboard bundle.")
        return
    decisions = pd.read_csv(decisions_path)
    ci = pd.read_csv(ci_path) if ci_path.exists() else pd.DataFrame()
    evidence = pd.read_csv(evidence_path) if evidence_path.exists() else pd.DataFrame()
    ids = list(decisions.get("validation_id", pd.Series(dtype=str)).dropna().astype(str).unique())
    if not ids:
        st.info("No validation IDs are available.")
        return
    st.markdown("### Candidate-level evidence explorer")
    st.caption("Backup only · fixed thesis outputs · no candidate is retrained here.")
    vid = st.selectbox("Validation candidate", ids, key="appendix_direct_candidate")
    dr = decisions[decisions["validation_id"].astype(str) == vid].iloc[0]
    c1,c2,c3 = st.columns(3)
    c1.metric("Final decision", str(dr.get("final_fixed_weight_validation_decision", "Not exported")))
    c2.metric("Original gate", str(dr.get("expanded_gate_pass_mean.original_regime", "Not exported")))
    c3.metric("Locked-unseen gate", str(dr.get("expanded_gate_pass_mean.locked_unseen_similar", "Not exported")))
    if not evidence.empty and "validation_id" in evidence.columns:
        er = evidence[evidence["validation_id"].astype(str) == vid]
        if not er.empty:
            st.info(f"Evidence taxonomy: {er.iloc[0].get('evidence_grade','Not exported')} · {er.iloc[0].get('interpretive_note','')}")
    if not ci.empty and "validation_id" in ci.columns:
        sub = ci[ci["validation_id"].astype(str) == vid]
        needed = {"validation_mode","mean_gain","validation_seed","mean_gain_ci_high","mean_gain_ci_low"}
        if not sub.empty and needed.issubset(sub.columns):
            fig = go.Figure()
            for mode,color in [("original_regime",RED),("locked_unseen_similar",BLUE)]:
                x = sub[sub["validation_mode"].astype(str) == mode]
                if x.empty: continue
                fig.add_trace(go.Scatter(x=x["mean_gain"], y=x["validation_seed"], mode="markers", name=mode,
                    error_x=dict(type="data", symmetric=False, array=x["mean_gain_ci_high"]-x["mean_gain"], arrayminus=x["mean_gain"]-x["mean_gain_ci_low"]), marker=dict(size=9,color=color)))
            fig.add_vline(x=0,line_dash="dash")
            fig.update_layout(title="Mean gain with paired bootstrap CI",height=390,xaxis_title="Mean gain",yaxis_title="Validation seed",plot_bgcolor=BG,paper_bgcolor=BG,font_color=TEXT)
            st.plotly_chart(fig,use_container_width=True)


def render_technical_appendix() -> None:
    st.markdown("""
    <style>.appendix-nav .stButton>button{min-height:3.75rem!important;padding:.55rem .35rem!important;font-size:.9rem!important;line-height:1.15!important;font-weight:800!important;white-space:normal!important}</style>
    """, unsafe_allow_html=True)
    if "appendix_section" not in st.session_state:
        st.session_state.appendix_section = 0
    st.markdown('<span class="badge thesis">TECHNICAL APPENDIX — use only when asked</span>', unsafe_allow_html=True)
    st.caption("A–F mirrors the defense deck: simulation, validity, GA mechanics, metrics, results, and committee Q&A.")
    st.markdown('<div class="appendix-nav">', unsafe_allow_html=True)
    cols = st.columns(6,gap="small")
    for i,label in enumerate(APPENDIX_LABELS):
        with cols[i]:
            st.button(label,key=f"appendix_direct_{i}",use_container_width=True,type="primary" if i==st.session_state.appendix_section else "secondary",on_click=_set_section,args=(i,))
    st.markdown('</div>', unsafe_allow_html=True)
    docs = (_a_simulation,_b_validity,_c_ga,_d_metrics,_e_results,_f_qa)
    heights=(820,760,760,700,560,1000)
    sec=max(0,min(int(st.session_state.appendix_section),5))
    components.html(docs[sec](),height=heights[sec],scrolling=True if sec==5 else False)
    if sec==4:
        st.markdown("---")
        if st.toggle("Open candidate-level evidence explorer",value=False,key="appendix_direct_explorer"):
            _candidate_explorer()
