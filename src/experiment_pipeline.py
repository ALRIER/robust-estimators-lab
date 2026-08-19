"""Five-stage visual protocol of the written thesis; it never runs a GA."""

STAGES = (
    ("Initial discovery", "Discovery candidate only — not validated yet", "10 learnable estimators enter GA search under HPF1 / HPF2, specialist halving and an internal held-out gate.", "Find opportunities efficiently without converting discovery into a final claim."),
    ("Frozen confirmation I", "Frozen vector — confirmation mode", "The 10-component discovery vector is frozen; new validation seeds and 26 modern comparators challenge it under original and locked-unseen modes.", "Separate a search signal from post-search evidence under stronger benchmark pressure."),
    ("Expanded rediscovery", "Discovery reopened — stronger library", "The learnable basis expands 10 → 26; the modern gate is active from HPF1 and confirmed Lognormal priors can enter as protected warm starts.", "Test whether stronger robust pressure changes what the GA can discover from the beginning."),
    ("Frozen validation II", "Frozen vector — scope is tested", "The 26-component candidates are frozen again and evaluated across original and locked-unseen related regimes with an evidence taxonomy.", "Distinguish transfer specialists, local evidence, near-gate cases and benchmark retention."),
    ("External evidence + audit", "External calibration + abstain audit", "Frozen specialists face the real-world battery without reoptimization; a separate Dirichlet audit probes whether random simplex vectors reveal missed signal.", "Separate empirical transfer from random-search evidence about benchmark-retained regimes."),
)

STAGE_FACTS = (
    ("10 learnable", "HPF1 60%", "HPF2 80%", "seeds 101 / 202", "Top-5 held-out"),
    ("weights frozen", "26 comparators", "8 validation seeds", "R=500 · B=500", "original + locked-unseen"),
    ("10 → 26 learnable", "HPF1 60%", "HPF2 90%", "CV-019 / CV-010", "modern gate from HPF1"),
    ("26-component frozen", "original + locked-unseen", "paired bootstrap", "evidence taxonomy", "no adaptation"),
    ("264 → 228 → 120 → 43", "26 / 43 parent wins", "255 confirmations", "4,000 Dirichlet draws", "8 audit seeds"),
)


def _t(x, y, value, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{value}</text>'


def _wrap(value: str, max_chars: int = 34):
    words = str(value).split()
    if not words:
        return []
    lines, current = [], words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _multiline(x, y, value, cls="noteText", max_chars=38, line_height=20):
    return [_t(x, y + i * line_height, line, cls) for i, line in enumerate(_wrap(value, max_chars))]


def experiment_pipeline_svg(stage: int) -> str:
    stage = max(0, min(int(stage), len(STAGES) - 1))
    title, claim, what, why = STAGES[stage]
    w, h = 1600, 760
    body = ['<rect x="22" y="18" width="1556" height="720" rx="16" class="canvas"/>']

    xs = (190, 465, 740, 1015, 1290)
    short_names = ("DISCOVERY", "FROZEN I", "REDISCOVERY", "FROZEN II", "EXTERNAL + AUDIT")
    for i, short_name in enumerate(short_names):
        active = i == stage
        body += [
            f'<rect x="{xs[i]-110}" y="78" width="220" height="72" rx="10" fill="{"#3a275f" if active else "#0c2035"}" stroke="{"#f3c743" if active else "#38719a"}" stroke-width="{"2.5" if active else "1.2"}"/>',
            _t(xs[i], 108, f"{i+1}. {short_name}", "stageon" if active else "stage", "middle"),
            _t(xs[i], 132, STAGES[i][0], "stagetiny", "middle"),
        ]
        if i < 4:
            body.append(f'<path d="M{xs[i]+112} 114 L{xs[i+1]-115} 114" class="arrow" marker-end="url(#arr)"/>')

    body += [
        _t(75, 196, f"STAGE {stage+1} OF 5 — {title.upper()}", "kicker"),
        '<rect x="70" y="222" width="1030" height="335" rx="14" class="scene"/>',
    ]

    if stage == 0:
        body += [_t(205, 270, "10 LEARNABLE COMPONENTS", "big", "middle")]
        for i in range(10):
            body.append(f'<circle cx="{120+(i%5)*43}" cy="{315+(i//5)*48}" r="10" class="dot"/>')
        body += [
            '<path d="M350 342 L510 342" class="arrow" marker-end="url(#arr)"/>',
            '<rect x="525" y="275" width="245" height="142" rx="12" class="ga"/>',
            _t(648, 315, "GA SEARCH", "big", "middle"),
            _t(648, 346, "HPF1 60%  →  HPF2 80%", "formula", "middle"),
            _t(648, 374, "specialist halving", "sub", "middle"),
            _t(648, 397, "internal held-out gate", "sub", "middle"),
            '<path d="M780 342 L895 342" class="arrow" marker-end="url(#arr)"/>',
            '<circle cx="955" cy="342" r="28" class="goldot"/>',
            _t(955, 347, "w*", "candidateText", "middle"),
            _t(512, 480, "Discovery nominates a candidate; it does not establish final evidence.", "caption", "middle"),
        ]
    elif stage == 1:
        body += [_t(305, 280, "DISCOVERY VECTOR", "big", "middle")]
        for i, v in enumerate((72, 118, 153, 187)):
            body += [f'<rect x="150" y="{320+i*38}" width="{v}" height="19" rx="4" class="bar"/>']
        body += [
            '<path d="M385 372 L515 372" class="arrow" marker-end="url(#arr)"/>',
            '<rect x="530" y="300" width="220" height="150" rx="14" class="freeze"/>',
            _t(640, 350, "FROZEN", "big", "middle"),
            _t(640, 382, "no retraining", "sub", "middle"),
            _t(640, 413, "10-component vector", "sub", "middle"),
            '<path d="M760 372 L875 372" class="arrow" marker-end="url(#arr)"/>',
            _t(965, 290, "MODERN PRESSURE", "big", "middle"),
        ]
        for i in range(16):
            body.append(f'<circle cx="{895+(i%4)*42}" cy="{330+(i//4)*38}" r="8" class="comp"/>')
        body += [
            _t(960, 505, "26 comparators · 8 validation seeds", "caption", "middle"),
            _t(960, 528, "R=500 · B=500 · original + locked-unseen", "caption", "middle"),
        ]
    elif stage == 2:
        body += [
            _t(250, 282, "CYCLE I", "big", "middle"), _t(250, 313, "10 learnable", "sub", "middle"),
            _t(250, 345, "60% → 80%", "formula", "middle"),
            '<path d="M365 360 L575 360" class="arrow" marker-end="url(#arr)"/>',
            _t(470, 337, "reopen discovery", "caption", "middle"),
            _t(735, 282, "CYCLE II", "big", "middle"), _t(735, 313, "26 learnable", "sub", "middle"),
            _t(735, 345, "60% → 90%", "formula", "middle"),
        ]
        for i in range(10):
            body.append(f'<circle cx="{165+(i%5)*42}" cy="{410+(i//5)*44}" r="9" class="dot"/>')
        for i in range(26):
            body.append(f'<circle cx="{610+(i%9)*39}" cy="{395+(i//9)*40}" r="7" class="purple"/>')
        body += [
            '<rect x="875" y="300" width="175" height="65" rx="10" class="warm"/>',
            _t(962, 328, "CV-019", "warmText", "middle"), _t(962, 350, "CV-010", "warmText", "middle"),
            _t(825, 505, "Protected warm starts preserve provenance but receive no fitness bonus.", "caption", "middle"),
        ]
    elif stage == 3:
        body += [
            _t(260, 285, "26-COMPONENT CANDIDATE", "big", "middle"),
            '<rect x="150" y="315" width="220" height="115" rx="12" class="freeze"/>',
            _t(260, 362, "FROZEN WEIGHTS", "big", "middle"),
            _t(260, 394, "no adaptation", "sub", "middle"),
            '<path d="M380 372 L525 372" class="arrow" marker-end="url(#arr)"/>',
            _t(630, 300, "ORIGINAL", "big", "middle"), _t(630, 330, "regime", "sub", "middle"),
            _t(820, 300, "LOCKED-UNSEEN", "big", "middle"), _t(820, 330, "related regimes", "sub", "middle"),
        ]
        for cx in (630, 820):
            body += [f'<circle cx="{cx}" cy="385" r="32" class="mode"/>', _t(cx, 390, "test", "tiny", "middle")]
        body += ['<path d="M865 420 L930 465" class="arrow" marker-end="url(#arr)"/>']
        tax = (("TRANSFER", 780, 455), ("LOCAL", 900, 455), ("NEAR-GATE", 780, 505), ("RETAINED", 900, 505))
        for name, x, y in tax:
            body += [f'<rect x="{x}" y="{y}" width="105" height="35" rx="7" class="tax"/>', _t(x+52, y+23, name, "tiny", "middle")]
    else:
        body += [
            _t(340, 270, "5A · REAL-WORLD BATTERY", "big", "middle"),
            _t(340, 300, "frozen specialists · no reoptimization", "sub", "middle"),
        ]
        funnel = (("264", "requested"), ("228", "loaded"), ("120", "evaluated"), ("43", "eligible"))
        for i, (num, lab) in enumerate(funnel):
            x = 110 + i * 150
            body += [f'<rect x="{x}" y="340" width="120" height="80" rx="10" class="funnel"/>', _t(x+60, 372, num, "factNum", "middle"), _t(x+60, 399, lab, "tiny", "middle")]
            if i < 3:
                body.append(f'<path d="M{x+122} 380 L{x+145} 380" class="arrow" marker-end="url(#arr)"/>')
        body += [
            _t(335, 470, "26 / 43 parent datasets · 255 corrected confirmations", "caption", "middle"),
            '<path d="M620 382 L700 382" class="split"/>',
            _t(865, 270, "5B · DIRICHLET AUDIT", "big", "middle"),
            _t(865, 300, "separate abstain / random-simplex check", "sub", "middle"),
            '<circle cx="800" cy="380" r="42" class="purpleRing"/>', _t(800, 374, "4,000", "factNum", "middle"), _t(800, 398, "vectors", "tiny", "middle"),
            '<circle cx="930" cy="380" r="42" class="purpleRing"/>', _t(930, 374, "8", "factNum", "middle"), _t(930, 398, "seeds", "tiny", "middle"),
            _t(865, 470, "23 / 34 no random pass · 11 / 34 some signal · 8 / 8 controls pass", "caption", "middle"),
        ]

    # Right interpretation rail
    body += [
        '<rect x="1140" y="222" width="385" height="335" rx="14" class="note"/>',
        _t(1170, 266, "CLAIM STATUS", "kicker"),
    ]
    body.extend(_multiline(1170, 302, claim, "claim", 31, 20))
    body += [_t(1170, 372, "WHAT HAPPENS", "kicker")]
    body.extend(_multiline(1170, 404, what, "noteText", 34, 19))
    body += [_t(1170, 490, "WHY INCLUDED", "kicker")]
    body.extend(_multiline(1170, 521, why, "noteText", 34, 19))

    # Prominent stage-facts band
    body += ['<rect x="70" y="585" width="1455" height="122" rx="14" class="factsBand"/>', _t(92, 616, "STAGE FACTS", "kicker")]
    facts = STAGE_FACTS[stage]
    fact_width = 265
    for i, fact in enumerate(facts):
        x = 92 + i * 282
        body += [f'<rect x="{x}" y="635" width="{fact_width}" height="50" rx="8" class="fact"/>', _t(x+fact_width/2, 666, fact, "factText", "middle")]

    css = """
    body{margin:0;background:#081525;font-family:Arial,sans-serif}svg{width:100%;height:760px}
    .canvas{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}.stage{font-size:11px;font-weight:700;fill:#a9c1d8}.stageon{font-size:11px;font-weight:800;fill:#fff}.stagetiny{font-size:9px;fill:#91abc1}.arrow{stroke:#72cfff;stroke-width:3;fill:none}.split{stroke:#507a9d;stroke-width:2.2;fill:none;stroke-dasharray:6 5}.kicker{font-size:13px;font-weight:800;letter-spacing:1.5px;fill:#72cfff}.scene{fill:#0b2036;stroke:#3d749b;stroke-width:1.4}.big{font-size:17px;font-weight:800;fill:#f5f9ff}.sub{font-size:14px;fill:#c4d5e7}.caption{font-size:13px;fill:#a9c0d5}.dot{fill:#58aee8}.goldot{fill:#f3c743}.candidateText{font-family:Georgia,serif;font-size:16px;font-weight:800;fill:#18324a}.purple{fill:#a777e3}.comp{fill:#54c786}.ga{fill:#193d5e;stroke:#72cfff;stroke-width:1.7}.freeze{fill:#193d5e;stroke:#f3c743;stroke-width:2}.bar{fill:#58aee8}.warm{fill:#2f2550;stroke:#a777e3;stroke-width:1.5}.warmText{font-size:13px;font-weight:800;fill:#e8dbff}.mode{fill:#153b55;stroke:#72cfff;stroke-width:1.5}.tax{fill:#1b4b3a;stroke:#5ee393}.tiny{font-size:11px;fill:#dff1ff}.note{fill:#0d2842;stroke:#4c86ad;stroke-width:1.5}.claim{font-size:14px;font-weight:800;fill:#f3c743}.noteText{font-size:13px;fill:#dce9f8}.formula{font-family:Georgia,serif;font-size:18px;font-weight:700;fill:#f3c743}.funnel{fill:#132d47;stroke:#58aee8;stroke-width:1.4}.factNum{font-size:21px;font-weight:800;fill:#f3c743}.purpleRing{fill:#251d43;stroke:#a777e3;stroke-width:2}.factsBand{fill:#0a1d32;stroke:#315f84;stroke-width:1.3}.fact{fill:#102b47;stroke:#397daa;stroke-width:1.2}.factText{font-size:12px;font-weight:800;fill:#eef6ff}
    """
    return f'''<html><style>{css}</style><svg viewBox="0 0 {w} {h}"><defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4z" fill="#dceaff"/></marker></defs>{''.join(body)}</svg></html>'''
