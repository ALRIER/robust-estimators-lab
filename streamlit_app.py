import streamlit as st
import streamlit.components.v1 as components
import time
import importlib
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
from src.synthetic_data import DemoScenario, draw_sample
from src.estimators import location_estimates
from src.mini_ga import MiniGAConfig, run_pedagogical_ga
from src import simplex as simplex_renderer
from src.fixed_simplex import fixed_simplex_figure
from src.simplex_svg import simplex_svg
from src.cluster_evolution import cluster_map_svg, contamination_shift_svg
from src.experiment_pipeline import STAGES as PIPELINE_STAGES, experiment_pipeline_svg
from src.defense_mode import defense_scene_svg
from src.data_loader import load_winners, load_final_decisions, load_bootstrap_ci, load_evidence_taxonomy, load_validated_specialists, load_dirichlet_summary, load_dirichlet_signals
from src.constants import ESTIMATOR_NAMES

# Streamlit reliably reruns the page module, but its long-lived worker can keep
# an imported helper module alive across a source-only deployment. Reload the
# renderer so Layer 2 always reflects the exact revision shipped with this app.
simplex_renderer = importlib.reload(simplex_renderer)

st.set_page_config(page_title="Robust Estimators Lab", page_icon="📊", layout="wide")
pio.templates.default = "plotly_dark"
st.markdown("""<style>
.stApp{background:radial-gradient(circle at 48% -12%,#16365c 0,#08172a 35%,#040a14 76%)!important;color:#eef5ff}.block-container{padding:.45rem 2rem 3rem!important;max-width:none!important}.stMetric{background:linear-gradient(135deg,#0d2038,#081525)!important;border:1px solid #218dca!important;border-top:3px solid #9a5cff!important;border-radius:7px;padding:10px;box-shadow:inset 0 0 18px rgba(33,141,202,.08)}.stMetric label,.stMetric [data-testid="stMetricLabel"]{color:#b8c8de!important}.stMetric [data-testid="stMetricValue"]{color:#f5f8ff!important}.badge{padding:6px 10px;border-radius:6px;font-size:.78rem;font-weight:800;display:inline-block;letter-spacing:.03em}.demo{background:#28184c;color:#d7c3ff;border:1px solid #8759de}.thesis{background:#0b372d;color:#9df0b7;border:1px solid #3aaf6f}
h1{color:#f5f8ff!important;margin:0 0 .1rem!important;font-size:2rem!important;text-shadow:0 0 18px rgba(71,169,255,.34)}h2,h3{color:#f2f7ff!important}[data-testid="stCaptionContainer"],.stCaption{color:#aebed3!important}[data-baseweb="tab-list"]{border-bottom:1px solid #2374b4!important;box-shadow:none!important;margin-top:.25rem!important;gap:.4rem}[data-baseweb="tab-border"]{display:none!important}[data-testid="stTabs"]>div:first-child{border-bottom:0!important}[data-baseweb="tab"]{color:#aebed3!important;background:#0a1930!important;border:1px solid #1d5688!important;border-bottom:0!important;border-radius:6px 6px 0 0!important;font-weight:700!important}[aria-selected="true"][data-baseweb="tab"]{color:#f6fbff!important;background:#102a49!important;box-shadow:inset 0 2px #4fc3ff!important}.layer-heading{font-size:1.3rem;font-weight:800;color:#f5f8ff;margin:.3rem 0 .1rem;text-shadow:0 0 14px rgba(79,195,255,.25)}.layer-subheading{color:#aebed3;margin:0 0 .75rem}.scenario-panel{border:1px solid #237fc0;border-left:4px solid #4fc3ff;border-radius:7px;background:linear-gradient(135deg,#0e2743,#081626);padding:.8rem 1rem;margin:.45rem 0 .8rem;color:#e8f3ff}.independent-note{color:#aebed3;font-size:.86rem;border-top:1px solid #20517e;padding-top:.65rem;margin-top:.35rem}.metric-caption{font-size:.78rem;color:#aebed3;margin-top:-.4rem}
div[data-testid="stVerticalBlockBorderWrapper"],div[data-testid="stExpander"]{border-color:#236b9e!important;background:#08182b!important}.stButton>button{background:linear-gradient(135deg,#5931bd,#2575bb)!important;color:#fff!important;border:1px solid #62c7ff!important;border-radius:6px!important;font-weight:700}.stSelectbox label,.stSlider label,.stNumberInput label,.stRadio label{color:#dceaff!important}.stAlert{background:#102a49!important;border:1px solid #287db5!important;color:#e7f4ff!important}.js-plotly-plot .plotly .modebar{background:#102541!important}
.pipeline-stage{min-height:136px;padding:14px 12px;border:1px solid #2b668f;border-radius:9px;background:#0a1b30;color:#b9cae0}.pipeline-stage.active{background:linear-gradient(135deg,#203d67,#152b48);border:2px solid #f3c743;box-shadow:0 0 20px rgba(243,199,67,.22);color:#f6fbff}.pipeline-step{font-size:11px;font-weight:800;letter-spacing:.08em;color:#72cfff}.pipeline-title{font-size:16px;font-weight:800;margin:8px 0}.pipeline-mini{font-size:12px;line-height:1.35}.story-panel{min-height:245px;padding:24px;border:1px solid #367eaf;border-radius:10px;background:linear-gradient(135deg,#0d2642,#08182b)}.story-kicker{font-size:12px;font-weight:800;letter-spacing:.1em;color:#72cfff}.story-title{font-size:28px;font-weight:800;color:#f5f8ff;margin:8px 0 16px}.story-label{font-size:12px;font-weight:800;letter-spacing:.08em;color:#f3c743;margin-bottom:6px}.story-body{font-size:16px;line-height:1.48;color:#dbe9f7}.funnel-step{padding:10px 14px;margin:6px auto;border:1px solid #3c79a5;border-radius:6px;background:#0d2642;color:#dceaff;text-align:center;font-weight:700}.funnel-step.active{border-color:#4de080;color:#c8ffd7;background:#123d30}
[data-testid="stSidebar"]{min-width:215px!important;max-width:215px!important;background:#071525!important;border-right:1px solid #245f8e}[data-testid="stSidebar"] [data-testid="stRadio"] label{font-size:.78rem!important;line-height:1.15!important;padding:.18rem 0!important}
</style>""", unsafe_allow_html=True)
st.title("Robust Estimators Lab")
st.caption("Interactive teaching and evidence interface for robust estimator mixtures")

@st.cache_data(show_spinner="Building the pedagogical GA landscape…")
def build_layer2_demo(family, contamination, contamination_rate, outlier_scale, mutation_rate, population_size, lens, seed, renderer_version):
    """The terrain and GA share one artificial objective, changed by UI controls."""
    terrain = simplex_renderer.teaching_terrain(family, contamination, contamination_rate, outlier_scale, 0., lens)
    objective = lambda weights: simplex_renderer.demo_objective(weights[:, 0], weights[:, 1], weights[:, 2], terrain)
    # Eight real generations keep the defense animation concise while allowing
    # every generation to dwell on its five recorded GA operations.
    run = run_pedagogical_ga(objective, MiniGAConfig(population_size=population_size, generations=8, mutation_rate=mutation_rate, seed=seed))
    return {"run": run, "terrain": terrain}

DEFENSE_INDEX = (
    "00 · Cover", "01 · Research framing", "02 · Target & simplex", "03 · Why a composite can win", "04 · Data-generating world", "05 · Monte Carlo engine",
    "06 · Simulation lab", "07 · GA search", "08 · Experiment pipeline", "09 · Thesis results", "10 · Validation", "11 · External evidence", "12 · Conclusions",
)
with st.sidebar:
    st.markdown("### DEFENSE MODE")
    st.caption("Manual presentation index")
    active_section = st.radio("Defense section", DEFENSE_INDEX, label_visibility="collapsed", key="defense_section")

if active_section == "06 · Simulation lab":
    # Layer 1 is a real, deterministic sample construction, not an analogy.
    # A fixed internal seed makes parameter changes directly comparable without
    # exposing an unnecessary defense-time control.
    L1_SEED = 20260808
    if "l1_next_stage" in st.session_state:
        st.session_state.l1_stage = st.session_state.pop("l1_next_stage")
    controls, visual = st.columns([.72, 5.28])
    with controls:
        st.markdown("**DATA-GENERATING REGIME**")
        l1_family = st.selectbox("Distribution family", ["normal", "lognormal", "weibull", "exgaussian"], key="l1_family")
        l1_contam = st.selectbox("Contamination structure", ["none", "upper_tail", "symmetric", "bimodal", "point_mass"], index=1, key="l1_contam")
        l1_rate = st.slider("Contamination rate", 0.0, .30, .10, .01, key="l1_rate")
        l1_scale = st.slider("Outlier scale", 1.5, 20.0, 10.0, .5, key="l1_scale")
        l1_n = st.select_slider("Population / sample size", [100, 300, 500, 1000, 1500, 2500, 5000], value=1500, key="l1_n")
    l1_key=(l1_family,l1_contam,l1_rate,l1_scale,l1_n)
    if "l1_key" not in st.session_state or st.session_state.l1_key != l1_key:
        st.session_state.l1_key=l1_key; st.session_state.l1_stage=9; st.session_state.l1_playing=False
    with controls:
        st.markdown("**CONSTRUCTION PLAYBACK**")
        play, pause, reset = st.columns(3)
        if play.button("▶", use_container_width=True, key="l1_play"):
            st.session_state.l1_playing=True
        if pause.button("❚❚", use_container_width=True, key="l1_pause"):
            st.session_state.l1_playing=False
        if reset.button("↺", use_container_width=True, key="l1_reset"):
            st.session_state.l1_stage=0; st.session_state.l1_playing=False
        l1_speed=st.select_slider("Animation pace", ["Slow", "Normal", "Fast"], value="Normal", key="l1_speed")
        stage=st.select_slider("Construction stage", options=list(range(10)), value=9, format_func=lambda item: f"Step {item + 1} / 10", key="l1_stage")
    sample=draw_sample(DemoScenario(l1_family,l1_contam,float(l1_rate),float(l1_scale),int(l1_n),L1_SEED))
    # A real contaminated sample arrives as one mixed random sequence; the
    # original baseline-then-outliers ordering was only a teaching convention.
    construction_order=np.random.default_rng(L1_SEED + 77).permutation(l1_n)
    progress=(stage + 1) / 10
    stage_names=("mixed sample begins", "early mixed draw", "mixed draw grows", "mixed draw grows", "half the sample visible", "mixed draw grows", "contamination becomes clearer", "near-complete mixed sample", "near-complete mixed sample", "full contaminated sample")
    visible_ids=construction_order[:int(round(l1_n * progress))]
    values=sample.values[visible_ids]; visible_outliers=sample.is_outlier[visible_ids]
    full_estimates=location_estimates(sample.values)
    with visual:
        summary, *metric_cards = st.columns([2.1,1,1,1,1,1])
        with summary:
            st.markdown(f'''<div class="scenario-panel"><b>{l1_family.replace('exgaussian', 'Ex-Gaussian').title()}</b> · {l1_contam.replace('_', ' ').title()}<br>ε = {l1_rate:.0%} · scale = {l1_scale:g}× · n = {l1_n:,}<br>Expected outliers: {int(round(l1_rate*l1_n)):,}</div>''', unsafe_allow_html=True)
        for card,(name,value) in zip(metric_cards,full_estimates.items()):
            card.metric(name, f"{value:.3f}")
        st.caption(f"Step {stage + 1} of 10 · {len(values):,} visible observations: {(~visible_outliers).sum():,} inliers and {visible_outliers.sum():,} generated outliers · {stage_names[stage]}")
        fig=go.Figure()
        peak=1.0
        if len(values)>8:
            density,edges=np.histogram(values,bins=48,density=True); centers=(edges[:-1]+edges[1:])/2; peak=max(float(density.max()),.01)
            fig.add_trace(go.Scatter(x=centers,y=density,mode='lines',fill='tozeroy',name='Density',line=dict(color='#79b9e6',width=2.5),fillcolor='rgba(121,185,230,.24)'))
        if (~visible_outliers).any():
            fig.add_trace(go.Scatter(x=values[~visible_outliers],y=np.full((~visible_outliers).sum(),-.055*peak),mode='markers',name='Inliers',marker=dict(size=6,color='#6398d0',opacity=.78)))
        if visible_outliers.any():
            fig.add_trace(go.Scatter(x=values[visible_outliers],y=np.full(visible_outliers.sum(),-.055*peak),mode='markers',name='Outliers',marker=dict(size=10,color='#ff5b49',symbol='x',line=dict(width=1,color='#ffb0a7'))))
        if len(values)>8:
            current=location_estimates(values)
            for name,value in current.items(): fig.add_vline(x=value,line_width=1.5,line_dash='dot',annotation_text=name,annotation_position='top')
        fig.add_vline(x=sample.true_location,line_dash='dash',line_width=2,annotation_text='Synthetic target')
        fig.add_annotation(xref='paper',yref='paper',x=.01,y=.98,xanchor='left',yanchor='top',align='left',showarrow=False,bgcolor='rgba(8,21,37,.82)',bordercolor='#326188',borderwidth=1,text=f"<b>Mixed generated draw</b><br>Blue = inlier · Red × = generated outlier<br>{visible_outliers.sum():,} of {len(values):,} visible observations are contamination")
        fig.update_layout(height=500,xaxis_title='Observed value',yaxis_title='Density',margin=dict(l=10,r=10,t=35,b=20),legend=dict(orientation='h',y=1.02),plot_bgcolor='#081525',paper_bgcolor='#081525',yaxis=dict(range=[-.14*peak,1.15*peak]))
        st.plotly_chart(fig,use_container_width=True)
        strip=go.Figure()
        strip.add_trace(go.Scatter(x=np.arange(len(values))[~visible_outliers],y=values[~visible_outliers],mode='markers',name='Inliers',marker=dict(size=5,color='#3576a8',opacity=.55)))
        if visible_outliers.any(): strip.add_trace(go.Scatter(x=np.arange(len(values))[visible_outliers],y=values[visible_outliers],mode='markers',name='Outliers',marker=dict(size=9,color='#ff5b49',symbol='x',opacity=.9)))
        strip.add_annotation(xref='paper',yref='paper',x=.01,y=.98,xanchor='left',yanchor='top',showarrow=False,bgcolor='rgba(8,21,37,.82)',bordercolor='#326188',borderwidth=1,text='Random observation order: contamination is interleaved with inliers.')
        strip.update_layout(title='Actual generated observation order',height=390,xaxis_title='Random draw order',yaxis_title='Observed value',margin=dict(l=10,r=10,t=40,b=20),legend=dict(orientation='h',y=1.04),plot_bgcolor='#081525',paper_bgcolor='#081525')
        st.plotly_chart(strip,use_container_width=True)
    if st.session_state.l1_playing:
        if stage < 9:
            # Nine well-spaced transitions make the real mixed draw observable
            # without the 50-update websocket flood of the original animation.
            time.sleep({"Slow":3.5,"Normal":1.8,"Fast":.8}[l1_speed])
            st.session_state.l1_next_stage=stage+1
            st.rerun()
        else:
            st.session_state.l1_playing=False

if active_section == "07 · GA search":
    if "l2_from_layer1" in st.session_state:
        scenario_from_l1=st.session_state.pop("l2_from_layer1")
        st.session_state.l2_family=scenario_from_l1["family"]
        st.session_state.l2_contam=scenario_from_l1["contamination"]
        st.session_state.l2_rate=scenario_from_l1["rate"]
        st.session_state.l2_scale=scenario_from_l1["scale"]
        st.session_state.l2_sample_n=scenario_from_l1["n"]
        st.success("Layer 1 regime loaded. This mini-GA now optimizes the same pedagogical scenario.")
    controls, visual = st.columns([.72, 5.28])
    with controls:
        st.markdown("**SEARCH CONTEXT**")
        l2_family = st.selectbox("Distribution family", ["normal", "lognormal", "weibull", "exgaussian"], key="l2_family")
        l2_contam = st.selectbox("Contamination structure", ["none", "upper_tail", "symmetric", "bimodal", "point_mass"], index=1, key="l2_contam")
        l2_rate = st.slider("Contamination rate", 0.0, .30, .10, .01, key="l2_rate")
        l2_scale = st.slider("Outlier scale", 1.5, 20.0, 10.0, .5, key="l2_scale")
        l2_sample_n = st.select_slider("Teaching sample size", [100, 300, 500, 1000, 1500, 2500, 5000], value=500, key="l2_sample_n")
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
    if "l2_next_phase" in st.session_state:
        st.session_state.l2_phase = st.session_state.pop("l2_next_phase")
    key = (l2_family, l2_contam, l2_rate, l2_scale, l2_mutation, l2_pop, l2_lens, l2_seed)
    if "l2_key" not in st.session_state or st.session_state.l2_key != key or load:
        st.session_state.l2_key = key
        st.session_state.l2_scrubber = 0
        st.session_state.l2_phase = 0
        st.session_state.l2_playing = False
    demo = build_layer2_demo(*key, "generation-steps-v1")
    run, terrain = demo["run"], demo["terrain"]
    max_generation = int(run["generations"][-1])
    frame = int(st.session_state.get("l2_scrubber", 0))
    with controls:
        frame = st.slider("Generation", 0, max_generation, key="l2_scrubber")
        phase = st.select_slider("Operation inside this generation", options=list(range(5)), value=0, format_func=lambda item: ("Evaluate", "Select", "Crossover", "Mutation", "Next generation")[item], key="l2_phase")
        st.markdown("**MAP VIEW**")
        show_population = st.toggle("Population", value=True, key="l2_show_population")
        show_path = st.toggle("Best path", value=True, key="l2_show_path")
        show_contours = st.toggle("Inheritance", value=True, key="l2_show_contours")
        show_grid = st.toggle("Grid", value=True, key="l2_show_grid")
        show_contamination = st.toggle("Eliminated", value=True, key="l2_show_contamination")
    active_rate = float(l2_rate)
    with visual:
        # The generation map is the instructional focus: keep it first and tall
        # enough to be fully visible without the former summary-card row.
        components.html(cluster_map_svg(run, frame, phase, show_inheritance=show_contours, show_eliminated=show_contamination, show_grid=show_grid, show_path=show_path), height=940, scrolling=False)
        observations, target_shift = st.columns(2)
        with observations:
            sample = draw_sample(DemoScenario(l2_family, l2_contam, active_rate, l2_scale, int(l2_sample_n), l2_seed))
            obs = go.Figure()
            inliers = sample.values[~sample.is_outlier]
            outliers = sample.values[sample.is_outlier]
            density, edges = np.histogram(inliers, bins=42, density=True)
            density = np.convolve(density, np.array([1, 2, 3, 2, 1]) / 9, mode="same")
            centers = (edges[:-1] + edges[1:]) / 2
            jitter = np.random.default_rng(l2_seed + 31 * frame)
            obs.add_trace(go.Scatter(x=centers, y=density, mode="lines", line=dict(color="#8b5cf6", width=2.5, shape="spline"), fill="tozeroy", fillcolor="rgba(139,92,246,.20)", hoverinfo="skip"))
            obs.add_trace(go.Scatter(x=inliers, y=jitter.uniform(-density.max()*.075, -density.max()*.015, len(inliers)), mode="markers", marker=dict(size=4, color="#8b5cf6", opacity=.42), hoverinfo="skip"))
            if len(outliers):
                obs.add_trace(go.Scatter(x=outliers, y=jitter.uniform(-density.max()*.20, -density.max()*.09, len(outliers)), mode="markers", marker=dict(size=7, color="#ef4444", opacity=.90), hovertemplate="Outlier<extra></extra>"))
            obs.update_layout(height=190, margin=dict(l=18,r=8,t=8,b=18), showlegend=False, xaxis=dict(showgrid=True, gridcolor="#214664", griddash="dot", zeroline=False), yaxis=dict(showgrid=True, gridcolor="#214664", griddash="dot", zeroline=False, showticklabels=False), plot_bgcolor="#081525", paper_bgcolor="#081525")
            st.plotly_chart(obs, use_container_width=True)
        with target_shift:
            components.html(contamination_shift_svg(active_rate), height=190, scrolling=False)
        score_history, survivor_history = st.columns(2)
        visible_generations = run["generations"][:frame + 1]
        all_scores = run["best_scores"]
        score_span = max(float(all_scores[0] - all_scores[-1]), 1e-9)
        visible_scores = 100 * (all_scores[0] - all_scores[:frame + 1]) / score_span
        visible_scores = np.maximum.accumulate(visible_scores)
        progress = visible_generations / max_generation
        # Count actual parent indices represented in recorded offspring events.
        lineage_counts=[]
        for gen in visible_generations:
            if gen >= max_generation:
                lineage_counts.append(0); continue
            event_set=run["events"][int(gen)+1]
            parents={event.get("parent_a_index") for event in event_set if event.get("event_type")=="offspring"}
            parents|={event.get("parent_b_index") for event in event_set if event.get("event_type")=="offspring"}
            lineage_counts.append(len(parents))
        soft_grid = dict(showgrid=True, gridcolor="#214664", griddash="dot", zeroline=False)
        with score_history:
            best_score = go.Figure(go.Scatter(x=visible_generations, y=visible_scores, mode="lines", line=dict(color="#6534e8", width=3, shape="spline"), hovertemplate="Generation %{x}<br>Score %{y:.1f}<extra></extra>"))
            best_score.update_layout(title="Best demo score by generation", height=210, margin=dict(l=24,r=10,t=35,b=22), showlegend=False, xaxis=soft_grid, yaxis=soft_grid, plot_bgcolor="#081525", paper_bgcolor="#081525")
            st.plotly_chart(best_score, use_container_width=True)
        with survivor_history:
            survivors = go.Figure(go.Bar(x=visible_generations, y=lineage_counts, marker_color="#59c977", hovertemplate="Generation %{x}<br>Parents contributing %{y}<extra></extra>"))
            survivors.update_layout(title="Selected lineages by generation", height=210, margin=dict(l=24,r=10,t=35,b=22), showlegend=False, xaxis=soft_grid, yaxis=soft_grid, plot_bgcolor="#081525", paper_bgcolor="#081525", yaxis_title="Parents")
            st.plotly_chart(survivors, use_container_width=True)
        st.caption("Low-dimensional slice of the full 26-dimensional simplex; shown for visualization only.")
    st.markdown('<div class="independent-note">This layer runs its own seeded mini-GA. It does not reuse the Layer 1 sample as evidence and never represents this animated path as a thesis trajectory.</div>', unsafe_allow_html=True)
    if st.session_state.l2_playing:
        if frame < max_generation or phase < 4:
            # A complete generation has five teaching scenes; normal playback
            # deliberately leaves time to narrate each one during a defense.
            time.sleep({"Slow": 4.5, "Normal": 2.0, "Fast": .75}[speed])
            if phase < 4:
                st.session_state.l2_next_phase = phase + 1
            else:
                st.session_state.l2_next_phase = 0
                st.session_state.l2_next_frame = frame + 1
            st.rerun()
        else:
            st.session_state.l2_playing = False
            st.success("Demo run complete. Scrub the timeline or change the regime to compare a new search landscape.")

if active_section == "08 · Experiment pipeline":
    if "story_stage" not in st.session_state:
        st.session_state.story_stage = 0
    stage_buttons = st.columns(3)
    for index, (title, _what, _why) in enumerate(PIPELINE_STAGES):
        with stage_buttons[index % 3]:
            if st.button(f"{index + 1}. {title}", key=f"story_stage_{index}", use_container_width=True, type="primary" if index == st.session_state.story_stage else "secondary"):
                st.session_state.story_stage = index
    components.html(experiment_pipeline_svg(st.session_state.story_stage), height=790, scrolling=False)
    st.caption("Select a stage to inspect the written-thesis protocol manually. This visual narrative does not rerun the thesis GA or claim a new result.")

if active_section == "09 · Thesis results":
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

if active_section == "10 · Validation":
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

if active_section == "11 · External evidence":
    st.markdown('<span class="badge thesis">THESIS RESULTS — external evidence</span>', unsafe_allow_html=True)
    st.caption("These two audits answer different questions and neither retrains a discovered estimator.")
    real, audit = st.columns(2)
    with real:
        st.markdown('''<div class="story-panel"><div class="story-kicker">REAL-WORLD EXTERNAL BATTERY</div><div class="story-title">Empirical calibration</div><div class="story-label">WHAT IT TESTS</div><div class="story-body">Frozen specialists are applied to public datasets without retraining. Repeated subsamples are assessed against the empirical full-sample mean.</div><div class="story-label" style="margin-top:20px">THESIS RESULT</div><div class="story-body">At least one corrected win occurred in 26 of 43 eligible parent datasets; 255 profile-matched comparisons survived false-discovery-rate control.</div><div class="story-label" style="margin-top:20px">QUESTION</div><div class="story-body">Does the supported signal transfer to empirical data?</div></div>''', unsafe_allow_html=True)
    with audit:
        st.markdown('''<div class="story-panel"><div class="story-kicker">RANDOM DIRICHLET ABSTAIN AUDIT</div><div class="story-title">Simplex sanity check</div><div class="story-label">WHAT IT TESTS</div><div class="story-body">Random Dirichlet composites are evaluated in benchmark-retained regimes under the original dual gate. This audit does not rerun the GA.</div><div class="story-label" style="margin-top:20px">QUESTION</div><div class="story-body">Could arbitrary weight vectors reveal composite signal where the selected GA candidate was retained by the benchmark?</div></div>''', unsafe_allow_html=True)
    dirichlet_summary, dirichlet_signals = load_dirichlet_summary(), load_dirichlet_signals()
    if not dirichlet_summary.empty:
        signal_count=int(dirichlet_summary["dirichlet_signal"].astype(str).str.lower().eq("true").sum())
        total=len(dirichlet_summary)
        metric_a, metric_b, metric_c = st.columns(3)
        metric_a.metric("Audited regimes", total)
        metric_b.metric("Regimes with Dirichlet signal", signal_count)
        metric_c.metric("Audit rule", "4,000 draws · 8 seeds")
        plot_data=dirichlet_summary.sort_values("total_seed_stable_passes", ascending=False).head(12)
        audit_fig=go.Figure(go.Bar(x=plot_data["validation_id"], y=plot_data["total_seed_stable_passes"], marker_color=["#f3c743" if str(v).lower()=="true" else "#526a85" for v in plot_data["dirichlet_signal"]], hovertemplate="%{x}<br>Seed-stable passes: %{y}<extra></extra>"))
        audit_fig.update_layout(title="Dirichlet audit: seed-stable random-search passes by regime", height=350, yaxis_title="Passes across audit seeds", plot_bgcolor="#081525", paper_bgcolor="#081525")
        st.plotly_chart(audit_fig, use_container_width=True)
        st.caption("Gold bars indicate a reported Dirichlet signal. A signal calls for the abstention to be revisited; it is not a replacement for fixed-weight confirmation.")
    else:
        st.info("Dirichlet audit results were not exported to this dashboard bundle.")

DEFENSE_SCENE_SECTION = {
    "00 · Cover": 0,
    "01 · Research framing": 1,
    "02 · Target & simplex": 2,
    "03 · Why a composite can win": 3,
    "04 · Data-generating world": 4,
    "05 · Monte Carlo engine": 5,
    "12 · Conclusions": 6,
}
if active_section in DEFENSE_SCENE_SECTION:
    components.html(defense_scene_svg(DEFENSE_SCENE_SECTION[active_section]), height=770, scrolling=False)
    st.caption("Defense Mode follows the written thesis and current defense deck. Continue through the index to enter the live simulation, GA, evidence and external-audit layers.")
