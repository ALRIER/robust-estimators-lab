import numpy as np
import plotly.graph_objects as go


def barycentric_grid(step=.025):
    rows=[]
    vals=np.arange(0,1+1e-9,step)
    for a in vals:
        for b in vals:
            c=1-a-b
            if c>=-1e-9: rows.append((a,b,max(0.,c)))
    return np.asarray(rows)


def barycentric_to_xy(weights):
    weights=np.asarray(weights,dtype=float)
    return weights[...,1]+.5*weights[...,2], np.sqrt(3)/2*weights[...,2]


def demo_objective(a,b,c):
    return .04+(a-.42)**2+1.25*(b-.33)**2+.8*(c-.25)**2+.10*np.sin(8*a)*np.cos(7*b)


def empirical_landscape(bootstrap_locations, metric='q95', step=.025):
    """Evaluate a visible 3-weight slice from bootstrap teaching samples."""
    grid=barycentric_grid(step)
    mixed=np.asarray(bootstrap_locations) @ grid.T
    loss=mixed**2
    mean=loss.mean(axis=0)
    q95=np.quantile(loss,.95,axis=0)
    return {"grid":grid,"mean":mean,"q95":q95,"z":q95 if metric=='q95' else mean,"metric":metric}


def landscape_figure(surface, population, path, objective, labels, benchmark_weights=None):
    grid=surface['grid']; x,y=barycentric_to_xy(grid); z=surface['z']
    fig=go.Figure(go.Mesh3d(x=x,y=y,z=z,intensity=z,colorscale='RdYlGn_r',opacity=.96,alphahull=0,
        customdata=grid,hovertemplate=(f"{labels[0]}=%{{customdata[0]:.2f}}<br>{labels[1]}=%{{customdata[1]:.2f}}<br>{labels[2]}=%{{customdata[2]:.2f}}<br>{surface['metric']} loss=%{{z:.5f}}<extra></extra>")))
    px,py=barycentric_to_xy(population); pz=np.asarray(objective(population))
    fig.add_trace(go.Scatter3d(x=px,y=py,z=pz,mode='markers',name='GA population',marker=dict(size=4,color='#24313a',opacity=.6)))
    tx,ty=barycentric_to_xy(path); tz=np.asarray(objective(path))
    fig.add_trace(go.Scatter3d(x=tx,y=ty,z=tz,mode='lines+markers',name='Best-so-far path',line=dict(color='#e6533f',width=7),marker=dict(size=4,color='#e6533f')))
    if benchmark_weights is not None:
        bx,by=barycentric_to_xy(np.asarray(benchmark_weights)); bz=float(np.asarray(objective(np.asarray(benchmark_weights)[None,:]))[0])
        fig.add_trace(go.Scatter3d(x=[bx],y=[by],z=[bz],mode='markers',name='Best single-estimator benchmark',marker=dict(size=8,color='#ffd166',symbol='diamond')))
    fig.update_layout(height=800,margin=dict(l=0,r=0,t=45,b=0),title=f"DEMO MODE — {surface['metric']} loss across a three-estimator simplex slice",legend=dict(orientation='h',y=1.02),scene=dict(xaxis=dict(title='Simplex coordinate'),yaxis=dict(title='Simplex coordinate'),zaxis=dict(title=f"{surface['metric']} loss"),aspectratio=dict(x=1.35,y=1.15,z=.75),camera=dict(eye=dict(x=1.5,y=-1.7,z=1.1))))
    return fig
