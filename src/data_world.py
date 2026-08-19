"""Additional presentation views for Layer 2: Data-generating world."""

DATA_WORLD_VIEWS = (
    "Experimental Grid",
    "Six Families",
    "Simulator Certification",
)


def _t(x, y, value, cls="body", anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{value}</text>'


def _wrap(value: str, max_chars: int = 40):
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


def _multiline(x, y, value, cls="body", max_chars=40, line_height=23, anchor="start"):
    return [
        _t(x, y + i * line_height, line, cls, anchor)
        for i, line in enumerate(_wrap(value, max_chars))
    ]


def data_world_detail_svg(view: int) -> str:
    """Render Layer 2 support views 1 and 2; view 0 remains the original scene."""
    view = max(1, min(int(view), 2))
    w, h = 1600, 850
    body = [f'<rect x="28" y="25" width="1544" height="800" rx="18" class="canvas"/>']

    if view == 1:
        body += [
            _t(90, 100, "DATA-GENERATING WORLD · STRUCTURAL COVERAGE", "kicker"),
            _t(90, 153, "Six families create qualitatively different risk environments.", "title"),
            _t(90, 194, "Same population-mean estimand; different symmetry, skewness, tail and hazard structure.", "subtitle"),
        ]
        families = (
            ("NORMAL", "SYMMETRIC BASELINE", "Classical reference world", "classical inference"),
            ("LOGNORMAL", "POSITIVE RIGHT-SKEW", "Strong asymmetry and upper tail", "income / expenditure"),
            ("WEIBULL", "SURVIVAL-LIKE POSITIVE SHAPE", "Flexible shape and hazard", "survival / reliability"),
            ("INVERSE GAUSSIAN", "ASYMMETRIC DURATION", "Positive asymmetric duration tail", "duration processes"),
            ("EX-GAUSSIAN", "REACTION-TIME-LIKE TAIL", "Skew plus exponential tail", "reaction times"),
            ("EX-WALD", "FIRST-PASSAGE POSITIVE PROCESS", "First-passage dynamics", "cognitive RT"),
        )
        for i, (name, structure, meaning, domain) in enumerate(families):
            row, col = divmod(i, 3)
            x = 92 + col * 505
            y = 245 + row * 245
            body.append(f'<rect x="{x}" y="{y}" width="455" height="205" rx="14" class="card"/>')
            body.append(_t(x + 25, y + 42, name, "family"))
            body.extend(_multiline(x + 25, y + 78, structure, "structure", 34, 21))
            body.extend(_multiline(x + 25, y + 126, meaning, "body", 38, 22))
            body.append(_t(x + 25, y + 177, domain, "domain"))
        body += [
            '<rect x="105" y="742" width="1390" height="55" rx="10" class="takeaway"/>',
            _t(800, 777, "F₀ changes the sampling environment; θ(F) = μ_F = E_F[X] remains the population-mean target.", "gold", "middle"),
        ]
    else:
        body += [
            _t(90, 100, "DATA-GENERATING WORLD · SIMULATOR CERTIFICATION", "kicker"),
            _t(90, 153, "Four checks run before any GA result is trusted.", "title"),
            _t(90, 194, "Certification tests the simulated world independently of the algorithm's conclusions.", "subtitle"),
        ]
        metrics = (
            ("125", "VALIDATION CONDITIONS"),
            ("0", "HARD FAILURES"),
            ("29", "EXPLAINABLE WARNINGS"),
        )
        for i, (number, label) in enumerate(metrics):
            x = 150 + i * 475
            body += [
                f'<rect x="{x}" y="235" width="400" height="145" rx="14" class="metric"/>',
                _t(x + 200, 300, number, "number", "middle"),
                _t(x + 200, 347, label, "metriclabel", "middle"),
            ]
        checks = (
            ("1", "MOMENT FIDELITY", "Max mean error 0.976%, below the 1% threshold."),
            ("2", "CONTAMINATION FIDELITY", "Rate, direction and MAD distance behave as designed."),
            ("3", "THEORY RECOVERY", "Median/mean ratios and Huber behaviour match classical expectations."),
            ("4", "EMPIRICAL ANCHORING", "Real datasets are structural anchors, not training targets."),
        )
        for i, (n, title, detail) in enumerate(checks):
            col = i % 2
            row = i // 2
            x = 105 + col * 760
            y = 430 + row * 145
            body += [
                f'<rect x="{x}" y="{y}" width="705" height="118" rx="12" class="check"/>',
                _t(x + 30, y + 48, n, "checknum"),
                _t(x + 82, y + 42, title, "checktitle"),
            ]
            body.extend(_multiline(x + 82, y + 73, detail, "body", 66, 20))
        body += [
            '<rect x="105" y="738" width="1390" height="58" rx="10" class="takeaway"/>',
            _t(800, 766, "Warnings are diagnostic, not failures: they reflect expected variance, dilution, masking or anchoring mismatch.", "gold", "middle"),
            _t(800, 787, "The simulator is certified before the GA is allowed to support a scientific claim.", "smallgold", "middle"),
        ]

    return f'''<html><style>
body{{margin:0;background:#081525;font-family:Arial,sans-serif}}
svg{{width:100%;height:{h}px}}
.canvas{{fill:#091a2e;stroke:#2d6d9c;stroke-width:1.5}}
.kicker{{font-size:15px;font-weight:800;letter-spacing:1.8px;fill:#72cfff}}
.title{{font-size:32px;font-weight:800;fill:#f5f9ff}}
.subtitle{{font-size:18px;fill:#bdd0e2}}
.card,.check{{fill:#0d2741;stroke:#397daa;stroke-width:1.4}}
.family{{font-size:20px;font-weight:800;fill:#f5f9ff}}
.structure{{font-size:13px;font-weight:800;letter-spacing:1px;fill:#72cfff}}
.body{{font-size:16px;fill:#dce9f8}}
.domain{{font-size:14px;font-style:italic;fill:#9fb8cf}}
.takeaway{{fill:#102d4b;stroke:#f3c743;stroke-width:1.6}}
.gold{{font-size:16px;font-weight:800;fill:#f3c743}}
.smallgold{{font-size:13px;fill:#e7cf78}}
.metric{{fill:#102d4b;stroke:#4b84ad;stroke-width:1.5}}
.number{{font-size:46px;font-weight:800;fill:#f3c743}}
.metriclabel{{font-size:13px;font-weight:800;letter-spacing:1.2px;fill:#72cfff}}
.checknum{{font-size:31px;font-weight:800;fill:#f3c743}}
.checktitle{{font-size:16px;font-weight:800;fill:#f5f9ff}}
</style><svg viewBox="0 0 {w} {h}">{''.join(body)}</svg></html>'''
