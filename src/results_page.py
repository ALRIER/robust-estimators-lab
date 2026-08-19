"""Direct, single-source renderer for Layer 7 · Results journey.

This module contains the audience-facing navigation and interpretation rail. The
actual narrative figures come from results_journey_polished.py. No runtime hooks,
monkey-patching, or evidence recomputation are used here.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from src.results_journey_polished import result_figure

ROOT = Path(__file__).resolve().parents[1]

RESULT_STAGES = (
    {
        "label": "1–2 · Discovery + Frozen I",
        "question": "What survived the first search?",
        "claim": "TWO CONFIRMED SIGNALS",
        "plain": "Many opportunities appeared. Only two survived frozen confirmation.",
        "color": "#e66d4f",
        "what": "The first GA search produced candidate wins, and then the exact same weights were tested again without retraining.",
        "happened": "36 controlled regimes produced 16 discovery wins. Frozen confirmation reduced that set to two Lognormal signals: CV-019 and CV-010.",
        "means": "Discovery tells us where to look. Frozen confirmation tells us what we can defend.",
        "not_claim": "Do not call all 16 discovery wins confirmed results.",
        "key": "36 → 16 → 2",
    },
    {
        "label": "3 · Expanded rediscovery",
        "question": "What changed when the search space became stronger?",
        "claim": "OPPORTUNITY MAP CHANGED",
        "plain": "A stronger 26-component search found a different pattern of opportunity.",
        "color": "#a777e3",
        "what": "The search was reopened with 26 learnable estimators instead of 10, stronger HPF2 exposure, and the modern benchmark gate active from the start.",
        "happened": "Twelve discovery winners appeared across five of the six families. Inverse Gaussian contributed the largest number of winners; Ex-Gaussian contributed none.",
        "means": "Changing the estimator library changes where useful mixtures can be found. The opportunity is structural, not universal.",
        "not_claim": "Do not treat these twelve discovery wins as fixed-weight confirmations.",
        "key": "10 → 26 components · 12 discovery winners",
    },
    {
        "label": "4 · Strict validation",
        "question": "Did the new candidates really transfer?",
        "claim": "TWO WEIBULL TRANSFER SPECIALISTS",
        "plain": "They worked in related unseen regimes, but not everywhere.",
        "color": "#54c786",
        "what": "The exact frozen 26-component candidates were tested in two modes: their original regime and a related locked-unseen regime.",
        "happened": "FWVR011 and FWVR012 passed both mean and q95 gates in locked-unseen validation, but both performed substantially worse in original-regime validation.",
        "means": "These are narrow specialists. Their value is real, but their scope is limited to a validated profile.",
        "not_claim": "Do not say that the GA found a generally better estimator for Weibull data.",
        "key": "2 transfer specialists · original FAIL / locked-unseen PASS",
    },
    {
        "label": "5A · Real-world battery",
        "question": "Does the signal appear in real data?",
        "claim": "EXTERNAL CALIBRATION",
        "plain": "The signal appears in real data, but external evidence is not known-truth validation.",
        "color": "#58aee8",
        "what": "Frozen specialists were applied to external datasets without retraining, after the data passed loading, preparation, and eligibility filters.",
        "happened": "264 targets were requested, 228 loaded, 120 evaluated, and 43 parent datasets were eligible. Twenty-six of those 43 parents had at least one corrected win, producing 255 profile-matched confirmations.",
        "means": "Breadth is 26 of 43 independent parent datasets. Depth is 255 repeated profile-level confirmations inside that external battery.",
        "not_claim": "Do not describe the 255 confirmations as 255 independent datasets or as population-ground-truth validation.",
        "key": "264 → 228 → 120 → 43 · 26/43 parents · 255 confirmations",
    },
    {
        "label": "5B · Dirichlet audit",
        "question": "Was benchmark retention meaningful?",
        "claim": "ABSTENTION AUDIT",
        "plain": "In most retained cells, even random simplex search could not beat the benchmark.",
        "color": "#4fc3ff",
        "what": "Random Dirichlet weight vectors were tested in benchmark-retained cells using the original dual gate. This is an audit of abstention, not a new GA search.",
        "happened": "Twenty-three of 34 audited cells had no random pass. Eleven showed some random signal. All eight strongest positive controls passed.",
        "means": "Benchmark retention was often a substantive result rather than simply a weak GA search.",
        "not_claim": "Do not assume that every retained benchmark would have been easy to beat with more GA generations.",
        "key": "23/34 no random pass · 11/34 some signal · 8/8 controls pass",
    },
)

EXPLAIN_STEPS = (
    (
        "1 · SIGNAL — The first search produced 16 apparent wins across 36 controlled regimes.",
        "2 · PRESSURE — The weights were frozen and tested again on fresh validation seeds.",
        "3 · MEANING — Only CV-019 and CV-010 remained defensible Lognormal signals.",
    ),
    (
        "1 · CHANGE — The learnable basis expanded from 10 to 26 estimators.",
        "2 · PRESSURE — HPF2 increased to 90% and modern robust competition was active from the beginning.",
        "3 · MEANING — The family map changed, showing that opportunity depends on the search basis and regime.",
    ),
    (
        "1 · SIGNAL — Two Weibull candidates looked strong after expanded rediscovery.",
        "2 · PRESSURE — Their frozen weights were tested in original and locked-unseen regimes.",
        "3 · MEANING — Only narrow transfer survived, so the correct label is specialist, not universal winner.",
    ),
    (
        "1 · FILTER — The external battery narrowed from 264 requested targets to 43 eligible parents.",
        "2 · EVIDENCE — Twenty-six parents produced at least one corrected win, with 255 profile-matched confirmations.",
        "3 · MEANING — This supports empirical transfer, while Monte Carlo remains the known-truth validation layer.",
    ),
    (
        "1 · QUESTION — Could arbitrary simplex weights easily beat cells where the benchmark was retained?",
        "2 · AUDIT — 4,000 random vectors across eight seeds were used as an independent abstention probe.",
        "3 · MEANING — No random pass in 23 of 34 cells supports the interpretation that retention was often meaningful.",
    ),
)


def _set_stage(stage: int) -> None:
    st.session_state.results_stage = stage
    st.session_state.results_explanation = 0


def _message_html(stage: int) -> str:
    item = RESULT_STAGES[stage]
    return f"""
    <div class="results-rail" style="border-left-color:{item['color']}">
      <div class="results-kicker">CLAIM STATUS</div>
      <div class="results-title" style="color:{item['color']}">{item['claim']}</div>
      <div class="results-plain">{item['plain']}</div>
      <div class="results-rule"></div>
      <div class="results-label">WHAT YOU ARE SEEING</div><div class="results-copy">{item['what']}</div>
      <div class="results-label">WHAT HAPPENED</div><div class="results-copy">{item['happened']}</div>
      <div class="results-label">WHAT IT MEANS</div><div class="results-copy">{item['means']}</div>
      <div class="results-label danger">DO NOT OVERCLAIM</div><div class="results-copy">{item['not_claim']}</div>
    </div>
    """


def render_results_journey() -> None:
    st.markdown("""
    <style>
    .results-nav .stButton>button{min-height:3.55rem!important;padding:.6rem .45rem!important;font-size:.94rem!important;font-weight:800!important;white-space:normal!important}
    .results-key{background:#0d2842;border:1px solid #326188;border-radius:9px;padding:11px 14px;margin:.55rem 0 .7rem;text-align:center;font-weight:800;color:#eef6ff;font-size:1rem}
    .results-rail{background:#0b2138;border:1px solid #356e99;border-left:5px solid;border-radius:13px;padding:17px 18px;min-height:640px}
    .results-kicker{font-size:.75rem;font-weight:900;letter-spacing:.12em;color:#72cfff;margin-bottom:8px}
    .results-title{font-size:1.25rem;font-weight:900;line-height:1.15;margin-bottom:8px}
    .results-plain{font-size:1rem;font-weight:800;line-height:1.38;color:#f2f7ff}
    .results-rule{border-top:1px solid #356e99;margin:13px 0}
    .results-label{font-size:.72rem;font-weight:900;letter-spacing:.08em;color:#f3c743;margin:13px 0 5px}
    .results-label.danger{color:#ff7c69}
    .results-copy{font-size:.95rem;line-height:1.43;color:#e3edf8}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<span class="badge thesis">RESULTS JOURNEY — precomputed thesis evidence</span>', unsafe_allow_html=True)
    st.caption("Each screen tells one result story: what entered, what disappeared, what survived, and how far the claim can go.")

    if "results_stage" not in st.session_state:
        st.session_state.results_stage = 0
    if "results_explanation" not in st.session_state:
        st.session_state.results_explanation = 0

    stage = max(0, min(int(st.session_state.results_stage), 4))
    item = RESULT_STAGES[stage]
    st.markdown(f'<div class="results-key">QUESTION: {item["question"]} &nbsp;&nbsp;|&nbsp;&nbsp; KEY EVIDENCE: {item["key"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="results-nav">', unsafe_allow_html=True)
    cols = st.columns(5, gap="small")
    for i, spec in enumerate(RESULT_STAGES):
        with cols[i]:
            st.button(spec["label"], key=f"results_direct_{i}", use_container_width=True,
                      type="primary" if i == stage else "secondary",
                      on_click=_set_stage, args=(i,))
    st.markdown('</div>', unsafe_allow_html=True)

    hero, rail = st.columns([3.25, 1.1], gap="medium")
    with hero:
        st.plotly_chart(result_figure(stage), use_container_width=True)
    with rail:
        st.markdown(_message_html(stage), unsafe_allow_html=True)

    left, right = st.columns([1, 4])
    with left:
        if st.button("Explain this result →", key="results_direct_explain"):
            st.session_state.results_explanation = min(2, st.session_state.results_explanation + 1)
    with right:
        st.info(EXPLAIN_STEPS[stage][st.session_state.results_explanation])

    show_detail = st.toggle("Show technical detail", value=False, key="results_direct_technical")
    if show_detail:
        winners_path = ROOT / "data/processed/winners_all.csv"
        st.caption("Backup only · fixed exported thesis results · nothing is recomputed here.")
        if winners_path.exists():
            winners = pd.read_csv(winners_path)
            columns = [c for c in ["distribution", "specialist_regime_id", "gate_pass", "final_selected_type", "ga_rel_improvement_q95"] if c in winners.columns]
            if columns:
                st.dataframe(winners[columns].head(12), use_container_width=True, hide_index=True)
