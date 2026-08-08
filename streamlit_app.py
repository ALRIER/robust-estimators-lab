import streamlit as st
import plotly.graph_objects as go
import numpy as np
from src.synthetic_data import DemoScenario, draw_sample
from src.estimators import location_estimates
from src.mini_ga import MiniGAConfig, demo_ga
from src.simplex import demo_surface_with_population
from src.data_loader import load_winners, load_final_decisions, load_bootstrap_ci, load_evidence_taxonomy, load_validated_specialists
from src.constants import ESTIMATOR_NAMES

st.set_page_config(page_title="Robust Estimators Lab", page_icon="📊", layout="wide")
st.markdown("""<style>
.block-container{padding-top:1.5rem}.stMetric{background:#fff;border:1px solid #d9dde2;border-top:3px solid #e6533f;border-radius:10px;padding:10px}.badge{padding:6px 10px;border-radius:8px;font-size:.78rem;font-weight:700;display:inline-block}.demo{background:#fff0ed;color:#a73b2e}.thesis{background:#edf6f1;color:#246e51}
</style>""", unsafe_allow_html=True)
st.title("Robust Estimators Lab")
st.caption("Interactive teaching and evidence interface for robust estimator mixtures")
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
    st.markdown('<span class="badge demo">DEMO MODE — pedagogical simulation</span>', unsafe_allow_html=True)
    st.caption("Low-dimensional slice of the full 26-dimensional simplex; shown for visualization only.")
    run=demo_ga(MiniGAConfig())
    gen=st.slider("Generation",0,30,30)
    st.plotly_chart(demo_surface_with_population(run['populations'][gen],run['best_path'][:gen+1]),use_container_width=True)
    c,d=st.columns([2,1])
    with c:
        cv=go.Figure(go.Scatter(x=run['generations'],y=run['best_scores'],mode='lines',line=dict(color='#e6533f')));cv.add_vline(x=gen,line_dash='dash');cv.update_layout(title='Convergence — pedagogical objective',height=300,xaxis_title='Generation',yaxis_title='Demo error')
        st.plotly_chart(cv,use_container_width=True)
    with d:
        w=run['best_path'][gen];st.metric('Best demo error',f"{run['best_scores'][gen]:.4f}");st.write(f"A Biweight: {w[0]:.2f}  ");st.write(f"B Median: {w[1]:.2f}  ");st.write(f"C Trimean: {w[2]:.2f}")
        st.warning("This is not a recorded thesis trajectory. Real final weights appear in Thesis results.")

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
