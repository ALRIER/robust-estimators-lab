"""Five-stage visual protocol of the written thesis; it never runs a GA."""

STAGES = (
    ("Initial discovery", "Discovery candidate only — not validated yet", "10 estimators enter GA search under HPF1 / HPF2 and held-out discovery.", "Find opportunities cheaply without declaring final truth."),
    ("Frozen confirmation I", "Frozen vector — confirmation mode", "Weights lock; new seeds and 26 comparators challenge the candidate.", "Separate a search signal from post-search evidence."),
    ("Expanded rediscovery", "Discovery reopened — stronger library", "The basis expands 10 → 26; warm starts compete but receive no privilege.", "Test whether robust-component pressure changes the specialist map."),
    ("Frozen validation II", "Frozen vector — scope is tested", "Weights lock again across original and locked-unseen related regimes.", "Distinguish transfer specialists from local or retained cases."),
    ("External evidence + audit", "External calibration — not known-θ validation", "Frozen candidates face real data; Dirichlet probes random simplex weights.", "Separate empirical transfer from random-search abstention."),
)

def _t(x, y, value, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{value}</text>'

def experiment_pipeline_svg(stage: int) -> str:
    stage=max(0,min(int(stage),len(STAGES)-1)); title,claim,what,why=STAGES[stage]
    w,h=1600,650; body=['<rect x="22" y="18" width="1556" height="610" rx="16" class="canvas"/>']
    xs=(190,465,740,1015,1290)
    for i,(name,_,_,_) in enumerate(STAGES):
        active=i==stage; body += [f'<rect x="{xs[i]-110}" y="90" width="220" height="72" rx="10" fill="{"#3a275f" if active else "#0c2035"}" stroke="{"#f3c743" if active else "#38719a"}" stroke-width="{"2.5" if active else "1.2"}"/>',_t(xs[i],120,f"{i+1}. {name.upper()}","stageon" if active else "stage","middle")]
        if i<4: body.append(f'<path d="M{xs[i]+112} 126 L{xs[i+1]-115} 126" class="arrow" marker-end="url(#arr)"/>')
    body += [_t(75,215,f"STAGE {stage+1} OF 5 — {title.upper()}","kicker"),f'<rect x="70" y="245" width="1030" height="290" rx="14" class="scene"/>']
    if stage==0:
        for i in range(10): body.append(f'<circle cx="{180+(i%5)*55}" cy="{325+(i//5)*60}" r="11" class="dot"/>')
        body += ['<path d="M475 365 L640 365" class="arrow" marker-end="url(#arr)"/>', '<rect x="650" y="290" width="210" height="150" rx="12" class="ga"/>',_t(755,343,"GA SEARCH","big","middle"),_t(755,377,"HPF1 → HPF2","sub","middle"),_t(755,407,"held-out discovery","sub","middle"), '<path d="M870 365 L970 365" class="arrow" marker-end="url(#arr)"/>', '<circle cx="1020" cy="365" r="24" class="goldot"/>',_t(755,490,"10 estimator components → feasible mixtures → candidate", "caption","middle")]
    elif stage==1:
        body += [_t(400,310,"DISCOVERED WEIGHTS", "big","middle")]
        for i,v in enumerate((65,110,145,170)):
            body += [f'<rect x="200" y="{350+i*35}" width="{v}" height="18" rx="4" class="bar"/>']
        body += [f'<rect x="560" y="310" width="220" height="150" rx="14" class="freeze"/>',_t(670,370,"🔒", "lock","middle"),_t(670,420,"WEIGHTS LOCKED", "big","middle"),'<path d="M790 385 L895 385" class="arrow" marker-end="url(#arr)"/>']
        for i in range(12): body.append(f'<circle cx="{940+(i%4)*36}" cy="{320+(i//4)*45}" r="8" class="comp"/>')
        body += [_t(1010,485,"26 comparators · new seeds", "caption","middle")]
    elif stage==2:
        body += [_t(310,310,"CYCLE I", "big","middle"),_t(310,350,"10 components", "sub","middle"), '<path d="M410 380 L620 380" class="arrow" marker-end="url(#arr)"/>',_t(515,350,"stronger pressure", "caption","middle"),_t(770,310,"CYCLE II", "big","middle"),_t(770,350,"26 components", "sub","middle")]
        for i in range(10): body.append(f'<circle cx="{205+(i%5)*40}" cy="{410+(i//5)*45}" r="9" class="dot"/>')
        for i in range(26): body.append(f'<circle cx="{680+(i%9)*38}" cy="{400+(i//9)*40}" r="7" class="purple"/>')
        body += [_t(770,505,"protected warm starts: compete, never privileged", "caption","middle")]
    elif stage==3:
        body += [_t(310,300,"ORIGINAL REGIME", "big","middle"),_t(310,337,"frozen weights", "sub","middle"), '<path d="M430 365 L590 365" class="arrow" marker-end="url(#arr)"/>', f'<rect x="610" y="285" width="230" height="155" rx="12" class="freeze"/>',_t(725,348,"🔒 FREEZE", "big","middle"),_t(725,390,"no adaptation", "sub","middle"), '<path d="M850 365 L955 365" class="arrow" marker-end="url(#arr)"/>',_t(1035,300,"LOCKED-UNSEEN", "big","middle"),_t(1035,337,"related regimes", "sub","middle")]
        for i,name in enumerate(("transfer","local","near-gate","retained")):
            body += [f'<rect x="{940+(i%2)*125}" y="{395+(i//2)*55}" width="110" height="38" rx="8" class="tax"/>',_t(995+(i%2)*125,420+(i//2)*55,name,"tiny","middle")]
    else:
        body += [_t(590,295,"FINAL FROZEN SPECIALIST", "big","middle"), '<circle cx="590" cy="340" r="20" class="goldot"/>','<path d="M590 365 L405 440" class="arrow" marker-end="url(#arr)"/>','<path d="M590 365 L780 440" class="arrow" marker-end="url(#arr)"/>',f'<rect x="180" y="440" width="390" height="70" rx="10" class="ga"/>',_t(375,470,"REAL-WORLD BATTERY", "big","middle"),_t(375,495,"Does the signal transfer?", "sub","middle"),f'<rect x="650" y="440" width="390" height="70" rx="10" class="ga"/>',_t(845,470,"DIRICHLET AUDIT", "big","middle"),_t(845,495,"Could random weights pass?", "sub","middle")]
    body += [f'<rect x="1140" y="245" width="385" height="290" rx="14" class="note"/>',_t(1170,290,"CLAIM STATUS", "kicker"),_t(1170,330,claim,"claim"),_t(1170,385,"WHAT HAPPENS", "kicker"),_t(1170,420,what,"noteText"),_t(1170,470,"WHY INCLUDED", "kicker"),_t(1170,505,why,"noteText")]
    return f'''<html><style>body{{margin:0;background:#081525;font-family:Arial,sans-serif}}svg{{width:100%;height:650px}}.canvas{{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}}.stage{{font-size:11px;font-weight:700;fill:#a9c1d8}}.stageon{{font-size:11px;font-weight:800;fill:#fff}}.arrow{{stroke:#72cfff;stroke-width:3;fill:none}}.kicker{{font-size:13px;font-weight:800;letter-spacing:1.5px;fill:#72cfff}}.scene{{fill:#0b2036;stroke:#3d749b;stroke-width:1.4}}.big{{font-size:17px;font-weight:800;fill:#f5f9ff}}.sub{{font-size:14px;fill:#c4d5e7}}.caption{{font-size:13px;fill:#a9c0d5}}.dot{{fill:#58aee8}}.goldot{{fill:#f3c743}}.purple{{fill:#a777e3}}.comp{{fill:#54c786}}.ga{{fill:#193d5e;stroke:#72cfff;stroke-width:1.7}}.freeze{{fill:#193d5e;stroke:#f3c743;stroke-width:2}}.lock{{font-size:31px}}.bar{{fill:#58aee8}}.tax{{fill:#1b4b3a;stroke:#5ee393}}.tiny{{font-size:11px;fill:#dfffee}}.note{{fill:#0d2842;stroke:#4c86ad;stroke-width:1.5}}.claim{{font-size:16px;font-weight:800;fill:#f3c743}}.noteText{{font-size:14px;fill:#dce9f8}}</style><svg viewBox="0 0 {w} {h}"><defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4z" fill="#dceaff"/></marker></defs>{''.join(body)}</svg></html>'''
