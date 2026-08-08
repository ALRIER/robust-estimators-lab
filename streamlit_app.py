import streamlit as st
import time
import plotly.graph_objects as go
import numpy as np
from src.synthetic_data import DemoScenario, draw_sample
from src.estimators import location_estimates
from src.mini_ga import MiniGAConfig, run_pedagogical_ga
from src.simplex import empirical_landscape, landscape_figure
from src.data_loader import load_winners, load_final_decisions, load_bootstrap_ci, load_evidence_taxonomy, load_validated_specialists
from src.constants import ESTIMATOR_NAMES

st.set_page_config(page_title="Robust Estimators Lab", page_icon="📊", layout="wide")
st.markdown("""<style>
.block-container{padding-top:1.5rem}.stMetric{background:#fff;border:1px solid #d9dde2;border-top:3px solid #e6533f;border-radius:10px;padding:10px}.badge{padding:6px 10px;border-radius:8px;font-size:.78rem;font-weight:700;display:inline-block}.demo{background:#fff0ed;color:#a73b2e}.thesis{background:#edf6f1;color:#246e51}
</style>""", unsafe_allow_html=True)
st.title("Robust Estimators Lab")
st.caption("Interactive teaching and evidence interface for robust estimator mixtures")

@st.cache_data(show_spinner="Evaluating the pedagogical simplex landscape…")
def build_layer2_demo(family, contamination, rate, scale, n, ga_population, coverage, metric, seed):
    """Build a cached, scenario-conditioned mini-GA demonstration."""
    scenario = DemoScenario(family, contamination, rate, scale, n, seed)
    sample = draw_sample(scenario)
    rng = np.random.default_rng(seed + 77)
    bootstrap_count = {"HPF1-style · 25%": 18, "HPF2-style · 50%": 36, "Full demo · 90%": 60}[coverage]
    # The three visible estimators are a teaching slice, not the 26-D thesis vector.
    locations = []
    for _ in range(bootstrap_count):
        x = sample.values[rng.integers(0, len(sample.values), len(sample.values))]
        e = location_estimates(x)
        locations.append([e["Mean"], e["Huber"], e["Biweight"]])
    locations = np.asarray(locations)
    metric_fn = (lambda weights: np.quantile((locations @ weights.T - sample.true_location) ** 2, .95, axis=0)) if metric == "q95" else (lambda weights: ((locations @ weights.T - sample.true_location) ** 2).mean(axis=0))
    config = MiniGAConfig(population_size=ga_population, generations=40, mutation_rate=.18, seed=seed)
    run = run_pedagogical_ga(metric_fn, config)
    surface = empirical_landscape(locations - sample.true_location, metric=metric, step=.025)
    singleton = np.eye(3)
    benchmark_index = int(np.argmin(metric_fn(singleton)))
    return {"run": run, "surface": surface, "locations": locations, "labels": ["Mean", "Huber", "Biweight"], "benchmark": singleton[benchmark_index], "benchmark_label": ["Mean", "Huber", "Biweight"][benchmark_index], "bootstrap_count": bootstrap_count}

tabs=st.tabs(["01 · Build the problem", "02 · GA search", "03 · Thesis results", "04 · Validation pipeline"])

with tabs[0]:
    st.markdown('<span class="badge demo">DEMO MODE — pedagogical simulation</span>', unsafe_allow_html=True)
    a,b=st.columns([1,3])
    with a:
        family=st.selectbox("Distribution family",["normal","lognormal","weibull","exgaussian"])
        contamination=st.selectbox("Contamination",["none","upper_tail","symmetric","bimodal","point_mass"])
        rate=st.slider("Contamination rate",0.,.30,.10,.01); scale=st.slider("Outlier scale",1.5,20.,10.,.5)
        n=st.select_slider("Sample size",[100,200,500,1000,1500],value=500)
        seed=st.number_input("Demo seed",value=20260808,step=1)
    sample=draw_sample(DemoScenario(family,contamination,float(rate),float(scale),int(n),int(seed)))
    est=location_estimates(sample.values)
    with b:
        metrics=st.columns(5)
        for col,(name,value) in zip(metrics,est.items()): col.metric(name,f"{value:.3f}")
        fig=go.Figure()
        fig.add_trace(go.Histogram(x=sample.values[~sample.is_outlier],nbinsx=45,histnorm='probability density',name='Inliers',opacity=.6,marker_color='#3576a8'))
        if sample.is_outlier.any(): fig.add_trace(go.Histogram(x=sample.values[sample.is_outlier],nbinsx=45,histnorm='probability density',name='Outliers',opacity=.75,marker_color='#e6533f'))
        for name,value in est.items(): fig.add_vline(x=value,line_width=2,annotation_text=name,annotation_position='top')
        fig.add_vline(x=sample.true_location,line_dash='dash',annotation_text='True location')
        fig.update_layout(barmode='overlay',height=420,xaxis_title='Value',yaxis_title='Density',margin=dict(l=10,r=10,t=35,b=20))
        st.plotly_chart(fig,use_container_width=True)
    c,d=st.columns([1.4,1])
    with c:
        errors={name:abs(value-sample.true_location) for name,value in est.items()}
        st.plotly_chart(go.Figure(go.Bar(x=list(errors.values()),y=list(errors.keys()),orientation='h',marker_color='#e6533f')).update_layout(title='Absolute deviation from synthetic target',height=300,margin=dict(l=10,r=10,t=35,b=20)),use_container_width=True)
    with d:
        st.subheader("Why this matters"); st.info("No single estimator is uniformly best. The data-generating regime can change the ranking of estimators.")

with tabs[1]:
    st.markdown('<span class="badge demo">DEMO MODE — scenario-conditioned pedagogical simulation</span>', unsafe_allow_html=True)
    st.caption("Low-dimensional slice of the full 26-dimensional simplex; shown for visualization only. The animated path is a live mini-GA, not a recorded thesis trajectory.")
    controls, visual = st.columns([1, 3])
    with controls:
        st.subheader("Build a search regime")
        l2_family = st.selectbox("Family", ["normal", "lognormal", "weibull", "exgaussian"], key="l2_family")
        l2_contam = st.selectbox("Contamination structure", ["none", "upper_tail", "symmetric", "bimodal", "point_mass"], key="l2_contam")
        l2_rate = st.slider("Contamination rate", 0.0, .30, .10, .01, key="l2_rate")
        l2_scale = st.slider("Outlier scale", 1.5, 20.0, 10.0, .5, key="l2_scale")
        l2_n = st.select_slider("Sample size", [300, 500, 1000, 2500, 5000], value=1000, key="l2_n")
        l2_pop = st.select_slider("GA population", [36, 54, 72, 96], value=72, key="l2_pop")
        l2_coverage = st.selectbox("Screening budget (HPF analogy)", ["HPF1-style · 25%", "HPF2-style · 50%", "Full demo · 90%"], index=1, help="HPF1/HPF2 are screening stages in the thesis. Here the setting controls only the amount of demo resampling; it is not a thesis replay.")
        l2_metric = st.radio("Demo objective", ["q95", "mean"], horizontal=True, format_func=lambda x: "q95(MSE) — tail risk" if x == "q95" else "Mean MSE")
        l2_seed = int(st.number_input("Reproducible seed", value=20260808, step=1, key="l2_seed"))
        load = st.button("Load this regime", type="primary", use_container_width=True)
    key = (l2_family,l2_contam,l2_rate,l2_scale,l2_n,l2_pop,l2_coverage,l2_metric,l2_seed)
    if "l2_key" not in st.session_state or st.session_state.l2_key != key or load:
        st.session_state.l2_key = key; st.session_state.l2_frame = 0; st.session_state.l2_playing = False
    demo = build_layer2_demo(*key)
    with visual:
        play_col, pause_col, reset_col, speed_col = st.columns([1,1,1,1.4])
        if play_col.button("▶ Play GA", use_container_width=True): st.session_state.l2_playing = True
        if pause_col.button("❚❚ Pause", use_container_width=True): st.session_state.l2_playing = False
        if reset_col.button("↺ Reset", use_container_width=True): st.session_state.l2_frame = 0; st.session_state.l2_playing = False
        speed = speed_col.select_slider("Animation pace", ["Slow", "Normal", "Fast"], value="Normal")
        frame = st.slider("Generation (manual scrubber)", 0, len(demo["run"]["generations"]) - 1, int(st.session_state.l2_frame), key="l2_scrubber")
        st.session_state.l2_frame = frame
        objective = (lambda weights: np.quantile((demo["locations"] @ weights.T) ** 2, .95, axis=0)) if l2_metric == "q95" else (lambda weights: ((demo["locations"] @ weights.T) ** 2).mean(axis=0))
        fig = landscape_figure(demo["surface"], demo["run"]["populations"][frame], demo["run"]["best_path"][:frame+1], objective, demo["labels"], demo["benchmark"])
        st.plotly_chart(fig, use_container_width=True)
    a,b,c,d = st.columns(4)
    a.metric("Generation", f"{frame} / 40")
    b.metric("Best demo objective", f"{demo['run']['best_scores'][frame]:.5f}")
    c.metric("Population diversity", f"{demo['run']['diversity'][frame]:.4f}")
    d.metric("Best single benchmark", demo["benchmark_label"])
    st.info(f"Narration cue: the black points are the generation-{frame} population. The red line is the best solution found so far. Each candidate is compared against the selected {l2_metric} objective over {demo['bootstrap_count']} resampled datasets; the yellow diamond is the strongest single-estimator benchmark in this pedagogical slice.")
    if st.session_state.l2_playing:
        if st.session_state.l2_frame < 40:
            time.sleep({"Slow": .8, "Normal": .35, "Fast": .12}[speed])
            st.session_state.l2_frame += 1
            st.rerun()
        else:
            st.session_state.l2_playing = False
            st.success("Demo run complete. Scrub the timeline or change the regime to compare a new search landscape.")

with tabs[2]:
    st.markdown('<span class="badge thesis">THESIS RESULTS — precomputed research output</span>', unsafe_allow_html=True)
    winners=load_winners()
    if winners.empty: st.error('Not exported'); st.stop()
    family=st.selectbox('Distribution',sorted(winners.distribution.dropna().unique()),key='l3fam')
    subset=winners[winners.distribution==family]
    regime=st.selectbox('Regime',list(subset.specialist_regime_id.dropna().unique()))
    row=subset[subset.specialist_regime_id==regime].iloc[0]
    st.subheader(f"{family} — {regime}");st.caption(str(row.get('condition_summary',row.get('regime_key',''))))
    c1,c2,c3=st.columns(3);c1.metric('Discovery gate pass',str(row.get('gate_pass')));c2.metric('Final selected type',str(row.get('final_selected_type')));c3.metric('Best q95 benchmark',str(row.get('best_benchmark_q95_estimator')))
    weights=sorted([(name,float(row.get(f'w_{name}',0) or 0)) for name in ESTIMATOR_NAMES],key=lambda x:x[1],reverse=True)
    wf=go.Figure(go.Bar(x=[x[1] for x in weights],y=[x[0] for x in weights],orientation='h',marker_color='#e6533f'));wf.update_layout(title='26-component final weight vector',height=680,yaxis=dict(autorange='reversed'),xaxis_title='Weight')
    st.plotly_chart(wf,use_container_width=True)
    st.info(f"Relative gain in q95(MSE): {row.get('ga_rel_improvement_q95','Not exported')} · Relative gain in mean MSE: {row.get('ga_rel_improvement_mean','Not exported')}. Discovery does not equal fixed-weight confirmation.")

with tabs[3]:
    st.markdown('<span class="badge thesis">THESIS RESULTS — precomputed research output</span>', unsafe_allow_html=True)
    st.caption('Discovery → locked / fixed weights → bootstrap CI → evidence taxonomy')
    decisions,ci,evidence,validated=load_final_decisions(),load_bootstrap_ci(),load_evidence_taxonomy(),load_validated_specialists()
    ids=list(decisions.validation_id.dropna().unique()) if not decisions.empty else []
    if not ids: st.error('Not exported'); st.stop()
    vid=st.selectbox('Candidate',ids)
    dr=decisions[decisions.validation_id==vid].iloc[0];er=evidence[evidence.validation_id==vid]
    a,b=st.columns(2)
    with a: st.subheader('Fixed-weight decision');st.write(dr.get('final_fixed_weight_validation_decision','Not exported'));st.write('Original-regime gate:',dr.get('expanded_gate_pass_mean.original_regime','Not exported'));st.write('Locked-unseen gate:',dr.get('expanded_gate_pass_mean.locked_unseen_similar','Not exported'))
    with b: st.subheader('Evidence taxonomy');st.write(er.iloc[0].get('evidence_grade','Not exported') if not er.empty else 'Not exported');st.caption(er.iloc[0].get('interpretive_note','Not exported') if not er.empty else 'Not exported')
    sub=ci[ci.validation_id==vid];fig=go.Figure()
    for mode,color in [('original_regime','#e6533f'),('locked_unseen_similar','#3576a8')]:
        x=sub[sub.validation_mode==mode]
        fig.add_trace(go.Scatter(x=x.mean_gain,y=x.validation_seed,error_x=dict(type='data',symmetric=False,array=x.mean_gain_ci_high-x.mean_gain,arrayminus=x.mean_gain-x.mean_gain_ci_low),mode='markers',name=mode,marker=dict(color=color)))
    fig.add_vline(x=0,line_dash='dash');fig.update_layout(title='Mean gain with bootstrap CI',height=400,xaxis_title='Mean gain',yaxis_title='Validation seed')
    st.plotly_chart(fig,use_container_width=True);st.caption(f'Validated specialists in curated taxonomy: {len(validated)}')
