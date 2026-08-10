import streamlit as st
import streamlit.components.v1 as components
import time
import importlib
import plotly.graph_objects as go
import numpy as np
from src.synthetic_data import DemoScenario, draw_sample
from src.estimators import location_estimates
from src.mini_ga import MiniGAConfig, run_pedagogical_ga
from src import simplex as simplex_renderer
from src.fixed_simplex import fixed_simplex_figure
from src.simplex_svg import simplex_svg
from src.cluster_evolution import cluster_map_svg, contamination_shift_svg
from src.data_loader import load_winners, load_final_decisions, load_bootstrap_ci, load_evidence_taxonomy, load_validated_specialists
from src.constants import ESTIMATOR_NAMES

# Streamlit reliably reruns the page module, but its long-lived worker can keep
# an imported helper module alive across a source-only deployment. Reload the
# renderer so Layer 2 always reflects the exact revision shipped with this app.
simplex_renderer = importlib.reload(simplex_renderer)

st.set_page_config(page_title="Robust Estimators Lab", page_icon="📊", layout="wide")
st.markdown("""<style>
.block-container{padding-top:1.5rem}.stMetric{background:#fff;border:1px solid #d9dde2;border-top:3px solid #e6533f;border-radius:10px;padding:10px}.badge{padding:6px 10px;border-radius:8px;font-size:.78rem;font-weight:700;display:inline-block}.demo{background:#fff0ed;color:#a73b2e}.thesis{background:#edf6f1;color:#246e51}
</style>""", unsafe_allow_html=True)
st.title("Robust Estimators Lab")
st.caption("Interactive teaching and evidence interface for robust estimator mixtures")

@st.cache_data(show_spinner="Building the pedagogical GA landscape…")
def build_layer2_demo(family, contamination, mutation_rate, population_size, lens, seed, renderer_version):
    """The terrain and GA share one artificial objective, changed by UI controls."""
    terrain = simplex_renderer.teaching_terrain(family, contamination, .10, 10., 0., lens)
    objective = lambda weights: simplex_renderer.demo_objective(weights[:, 0], weights[:, 1], weights[:, 2], terrain)
    run = run_pedagogical_ga(objective, MiniGAConfig(population_size=population_size, generations=150, mutation_rate=mutation_rate, seed=seed))
    rng = np.random.default_rng(seed + 91)
    contamination_schedule = np.clip(rng.normal(.16, .07, len(run["generations"])), .02, .35)
    return {"run": run, "terrain": terrain, "contamination_schedule": contamination_schedule}

tabs=st.tabs(["01 · Build the problem", "02 · GA search", "03 · Thesis results", "04 · Validation pipeline"])

with tabs[0]:
    st.markdown('<span class="badge demo">DEMO MODE — pedagogical sample construction</span>', unsafe_allow_html=True)
    st.caption("Build a regime, then watch inliers accumulate before the selected contamination is added. For skewed families this shows a density profile, not a symmetric bell curve.")
    controls, visual = st.columns([1, 3])
    with controls:
        st.subheader("Build a data-generating regime")
        l1_family = st.selectbox("Distribution family", ["normal", "lognormal", "weibull", "exgaussian"], key="l1_family")
        l1_contam = st.selectbox("Contamination structure", ["none", "upper_tail", "symmetric", "bimodal", "point_mass"], index=1, key="l1_contam")
        l1_rate = st.slider("Contamination rate", 0.0, .30, .10, .01, key="l1_rate")
        l1_scale = st.slider("Outlier scale", 1.5, 20.0, 10.0, .5, key="l1_scale")
        l1_n = st.select_slider("Population / sample size", [100, 300, 500, 1000, 1500, 2500, 5000], value=1500, key="l1_n")
        l1_seed = int(st.number_input("Reproducible seed", value=20260808, step=1, key="l1_seed"))
        rebuild = st.button("Generate this regime", type="primary", use_container_width=True)
    l1_key=(l1_family,l1_contam,l1_rate,l1_scale,l1_n,l1_seed)
    if "l1_next_frame" in st.session_state:
        st.session_state.l1_scrubber=st.session_state.pop("l1_next_frame")
    if "l1_key" not in st.session_state or st.session_state.l1_key != l1_key or rebuild:
        st.session_state.l1_key=l1_key; st.session_state.l1_scrubber=0; st.session_state.l1_playing=False
    sample=draw_sample(DemoScenario(l1_family,l1_contam,float(l1_rate),float(l1_scale),int(l1_n),l1_seed))
    # Pedagogical ordering: the baseline distribution forms first, contamination follows.
    build_order=np.r_[np.flatnonzero(~sample.is_outlier),np.flatnonzero(sample.is_outlier)]
    batch=max(20,int(np.ceil(l1_n/50)))
    frames=list(range(0,l1_n+1,batch))
    if frames[-1] != l1_n: frames.append(l1_n)
    with visual:
        play,pause,reset,speed_col=st.columns([1,1,1,1.4])
        if play.button("▶ Play construction",use_container_width=True,key="l1_play"): st.session_state.l1_playing=True
        if pause.button("❚❚ Pause",use_container_width=True,key="l1_pause"): st.session_state.l1_playing=False
        if reset.button("↺ Reset",use_container_width=True,key="l1_reset"): st.session_state.l1_scrubber=0; st.session_state.l1_playing=False
        l1_speed=speed_col.select_slider("Animation pace",["Slow","Normal","Fast"],value="Normal",key="l1_speed")
        frame_index=st.slider("Construction progress",0,len(frames)-1,key="l1_scrubber")
        visible_ids=build_order[:frames[frame_index]]
        values=sample.values[visible_ids]; visible_outliers=sample.is_outlier[visible_ids]
        phase="baseline inliers" if not visible_outliers.any() else ("contamination arriving" if (~visible_outliers).any() else "contamination segment")
        st.caption(f"Step {frame_index+1} / {len(frames)} · {len(values):,} of {l1_n:,} observations · phase: {phase}")
        fig=go.Figure()
        if (~visible_outliers).any(): fig.add_trace(go.Histogram(x=values[~visible_outliers],nbinsx=48,histnorm='probability density',name='Inliers',opacity=.62,marker_color='#3576a8'))
        if visible_outliers.any(): fig.add_trace(go.Histogram(x=values[visible_outliers],nbinsx=48,histnorm='probability density',name='Contamination',opacity=.78,marker_color='#e6533f'))
        if len(values)>8:
            current=location_estimates(values)
            for name,value in current.items(): fig.add_vline(x=value,line_width=1.5,line_dash='dot',annotation_text=name,annotation_position='top')
        fig.add_vline(x=sample.true_location,line_dash='dash',line_width=2,annotation_text='Synthetic target')
        fig.update_layout(barmode='overlay',height=460,xaxis_title='Observed value',yaxis_title='Density',margin=dict(l=10,r=10,t=35,b=20),legend=dict(orientation='h',y=1.02))
        st.plotly_chart(fig,use_container_width=True)
    p1,p2=st.columns([1.45,1])
    with p1:
        strip=go.Figure()
        strip.add_trace(go.Scatter(x=np.arange(len(values))[~visible_outliers],y=values[~visible_outliers],mode='markers',name='Inliers',marker=dict(size=5,color='#3576a8',opacity=.55)))
        if visible_outliers.any(): strip.add_trace(go.Scatter(x=np.arange(len(values))[visible_outliers],y=values[visible_outliers],mode='markers',name='Contamination',marker=dict(size=6,color='#e6533f',opacity=.8)))
        strip.update_layout(title='Observation stream used to build the displayed density',height=280,xaxis_title='Construction order',yaxis_title='Value',margin=dict(l=10,r=10,t=40,b=20),legend=dict(orientation='h',y=1.04))
        st.plotly_chart(strip,use_container_width=True)
    with p2:
        st.subheader("Teaching cue")
        st.info("The blue baseline establishes the family profile. Red observations then alter the location and tail behaviour. The estimator markers move as the evidence arrives.")
        if len(values)>8:
            current=location_estimates(values)
            for name,value in current.items(): st.metric(name,f"{value:.3f}")
    if st.session_state.l1_playing:
        if frame_index < len(frames)-1:
            time.sleep({"Slow":.65,"Normal":.28,"Fast":.10}[l1_speed])
            st.session_state.l1_next_frame=frame_index+1
            st.rerun()
        else:
            st.session_state.l1_playing=False
            st.success("Construction complete. Layer 2 can now use this same kind of regime logic for its mini-GA demonstration.")

with tabs[1]:
    controls, visual = st.columns([1.0, 4.2])
    with controls:
        st.markdown("**SEARCH CONTEXT**")
        l2_family = st.selectbox("Distribution family", ["normal", "lognormal", "weibull", "exgaussian"], key="l2_family")
        l2_contam = st.selectbox("Contamination structure", ["none", "upper_tail", "symmetric", "bimodal", "point_mass"], index=1, key="l2_contam")
        l2_mutation = st.select_slider("Mutation level", options=[.05, .10, .18, .28], value=.18, format_func=lambda value: f"{value:.0%}", key="l2_mutation")
        l2_lens = st.radio("Target metric", ["MSE", "q95(MSE)"], index=1, horizontal=True, key="l2_lens", help="A pedagogical lens that changes only the synthetic terrain's shape.")
        l2_pop = st.select_slider("GA population", [36, 48, 60, 72], value=48, key="l2_pop")
        l2_seed = 20260810
        load = st.button("Generate landscape", type="primary", use_container_width=True)
        st.markdown("**GA PLAYBACK**")
        play_side, pause_side, reset_side = st.columns(3)
        if play_side.button("▶", use_container_width=True, key="l2_play"):
            st.session_state.l2_playing = True
        if pause_side.button("❚❚", use_container_width=True, key="l2_pause"):
            st.session_state.l2_playing = False
        if reset_side.button("↺", use_container_width=True, key="l2_reset"):
            st.session_state.l2_scrubber = 0; st.session_state.l2_playing = False
        speed = st.select_slider("Animation pace", ["Slow", "Normal", "Fast"], value="Normal", key="l2_speed")
    # Apply queued animation progress before the generation widget is created.
    if "l2_next_frame" in st.session_state:
        st.session_state.l2_scrubber = st.session_state.pop("l2_next_frame")
    key = (l2_family, l2_contam, l2_mutation, l2_pop, l2_lens, l2_seed)
    if "l2_key" not in st.session_state or st.session_state.l2_key != key or load:
        st.session_state.l2_key = key
        st.session_state.l2_scrubber = 0
        st.session_state.l2_playing = False
    demo = build_layer2_demo(*key, "cluster-map-v2")
    run, terrain = demo["run"], demo["terrain"]
    max_generation = int(run["generations"][-1])
    frame = int(st.session_state.get("l2_scrubber", 0))
    with controls:
        frame = st.slider("Generation", 0, max_generation, key="l2_scrubber")
        st.markdown("**MAP VIEW**")
        show_population = st.toggle("Population", value=True, key="l2_show_population")
        show_path = st.toggle("Best path", value=True, key="l2_show_path")
        show_contours = st.toggle("Inheritance", value=True, key="l2_show_contours")
        show_grid = st.toggle("Grid", value=True, key="l2_show_grid")
        show_contamination = st.toggle("Eliminated", value=True, key="l2_show_contamination")
    active_rate = float(demo["contamination_schedule"][frame])
    with visual:
        components.html(cluster_map_svg(run, frame, active_rate, show_inheritance=show_contours, show_eliminated=show_contamination, show_grid=show_grid, show_path=show_path), height=500, scrolling=False)
        observations, target_shift = st.columns(2)
        with observations:
            sample = draw_sample(DemoScenario(l2_family, l2_contam, active_rate, 10.0, 360, l2_seed + frame))
            obs = go.Figure()
            obs.add_trace(go.Histogram(x=sample.values[~sample.is_outlier], histnorm="probability density", nbinsx=35, marker_color="#8b5cf6", opacity=.55, hoverinfo="skip"))
            if sample.is_outlier.any(): obs.add_trace(go.Histogram(x=sample.values[sample.is_outlier], histnorm="probability density", nbinsx=35, marker_color="#ef4444", opacity=.72, hoverinfo="skip"))
            obs.update_layout(barmode="overlay", height=235, margin=dict(l=18,r=8,t=8,b=18), showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False), plot_bgcolor="#ffffff", paper_bgcolor="#ffffff")
            st.plotly_chart(obs, use_container_width=True)
        with target_shift:
            components.html(contamination_shift_svg(active_rate), height=235, scrolling=False)
    if st.session_state.l2_playing:
        if frame < max_generation:
            time.sleep({"Slow": .8, "Normal": .35, "Fast": .12}[speed])
            # A widget value cannot be mutated after rendering; queue it for the next rerun.
            st.session_state.l2_next_frame = frame + 1
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
