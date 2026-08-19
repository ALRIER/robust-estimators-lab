"""Layer 2 · Data-generating world.

Three didactic views used in the timed defense:
1) why simulation is needed,
2) how one regime is built,
3) why the simulator is trustworthy.

The full repeated-sampling Monte Carlo engine now lives in Layer 4. Layer 2 only
establishes why known-truth simulation is needed and hands the story forward.
"""

DATA_WORLD_VIEWS = (
    "Why simulation?",
    "Build a regime",
    "Trust the simulator",
)


def _css() -> str:
    return """
    <style>
      *{box-sizing:border-box}
      body{margin:0;background:#081525;color:#e9f4ff;font-family:Arial,sans-serif}
      .page{padding:28px 32px 36px;background:#081525}
      .kicker{font-size:14px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin-bottom:9px}
      .title{font-size:38px;line-height:1.14;font-weight:900;color:#fff;margin-bottom:10px}
      .subtitle{font-size:19px;line-height:1.5;color:#bfd0e2;margin-bottom:25px;max-width:1280px}
      .section{font-size:21px;font-weight:900;color:#f3c743;letter-spacing:.05em;margin:30px 0 14px}
      .story{background:#0f2b47;border:1px solid #3c7198;border-left:7px solid #72cfff;border-radius:14px;padding:19px 21px;margin:17px 0;font-size:18px;line-height:1.5;color:#eef6ff}
      .takeaway{background:#12354a;border:1px solid #58aee8;border-left:7px solid #f3c743;border-radius:14px;padding:21px 23px;margin:24px 0 4px;font-size:20px;line-height:1.45;font-weight:850;color:#fff}
      .warn{background:#342b12;border:1px solid #f3c743;border-left:7px solid #f3c743;color:#fff2b8;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:20px 0}
      .two{display:grid;grid-template-columns:1fr 1fr;gap:17px}
      .three{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}
      .card{display:grid;grid-template-columns:96px 1fr;gap:20px;align-items:center;background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:15px;padding:21px 23px;margin-bottom:16px;min-height:150px}
      .icon{width:78px;height:78px;border-radius:19px;background:#10253a;border:1px solid #3c7198;display:flex;align-items:center;justify-content:center;font-size:39px;margin:auto}
      .label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:6px}
      .headline{font-size:26px;font-weight:900;line-height:1.18;color:#fff;margin-bottom:8px}
      .copy{font-size:17px;line-height:1.49;color:#dce9f8}
      .mini{font-size:15px;line-height:1.44;color:#b9c8d9;margin-top:8px}
      .formula-card{background:#0b2138;border:1px solid #356e99;border-left:6px solid #f3c743;border-radius:14px;padding:19px 21px;margin:15px 0}
      .formula-label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:7px}
      .formula{font-family:Georgia,serif;font-size:31px;font-weight:800;line-height:1.35;color:#f7d768;margin-bottom:9px}
      .formula-copy{font-size:17px;line-height:1.48;color:#dce9f8}
      .bridge{display:grid;grid-template-columns:1fr 65px 1fr 65px 1fr;gap:10px;align-items:center;margin:18px 0}
      .bridge-box{background:#10253a;border:1px solid #356e99;border-radius:13px;padding:20px 16px;text-align:center;min-height:145px;display:flex;flex-direction:column;justify-content:center}
      .bridge-icon{font-size:34px;margin-bottom:8px}.bridge-title{font-size:20px;font-weight:900;color:#fff;margin-bottom:6px}.bridge-copy{font-size:15px;line-height:1.42;color:#bfd0e2}.bridge-arrow{text-align:center;font-size:30px;color:#72cfff;font-weight:900}
      .builder{display:grid;grid-template-columns:repeat(6,1fr);gap:11px;align-items:stretch;margin:17px 0}
      .builder-box{background:#10253a;border:1px solid #356e99;border-radius:12px;padding:15px 10px;text-align:center;min-height:116px;display:flex;flex-direction:column;justify-content:center}
      .builder-box b{font-size:23px;color:#fff;margin-bottom:6px}.builder-box span{font-size:14px;color:#bfd0e2;line-height:1.36}
      .builder-box.result{border-color:#54c786;background:#10372e}
      .metricrow{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:17px 0 23px}
      .metric{background:#10253a;border:1px solid #356e99;border-radius:12px;padding:17px 12px;text-align:center}
      .metric .v{font-size:33px;font-weight:900;color:#f3c743;line-height:1.08}
      .metric .l{font-size:14px;color:#c4d3e3;margin-top:7px;font-weight:800}
      .family-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
      .family{background:#0d2239;border:1px solid #356e99;border-radius:13px;padding:17px 18px;min-height:128px}
      .family .name{font-size:20px;font-weight:900;color:#fff;margin-bottom:5px}
      .family .shape{font-size:13px;font-weight:900;letter-spacing:.08em;color:#72cfff;margin-bottom:7px}
      .family .desc{font-size:15px;line-height:1.43;color:#dce9f8}
      .check{display:grid;grid-template-columns:88px 1fr;gap:18px;align-items:center;background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:15px;padding:20px 22px;margin-bottom:15px}
      .check-icon{width:70px;height:70px;border-radius:18px;background:#10253a;border:1px solid #3c7198;display:flex;align-items:center;justify-content:center;font-size:35px}
      .check-title{font-size:23px;font-weight:900;color:#fff;margin-bottom:6px}
      .check-copy{font-size:16px;line-height:1.46;color:#dce9f8}
      .check-why{font-size:15px;line-height:1.42;color:#b9c8d9;margin-top:7px}
      @media(max-width:1050px){.two,.three,.metricrow,.builder,.family-grid{grid-template-columns:1fr 1fr}.bridge{grid-template-columns:1fr}.bridge-arrow{transform:rotate(90deg)}.card{grid-template-columns:78px 1fr}}
    </style>
    """


def _why_simulation() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>02 · DATA-GENERATING WORLD · WHY SIMULATION?</div>
      <div class='title'>To measure estimator error, we first need to know the truth.</div>
      <div class='subtitle'>Real data are essential later, but they do not reveal the true population mean. Simulation gives a controlled target before any estimator is tested.</div>

      <div class='two'>
        <div class='card'><div class='icon'>🌍</div><div><div class='label'>REAL DATA</div><div class='headline'>The population mean is hidden</div><div class='copy'>We observe a dataset, but we do not directly observe the true population mean θ. That makes exact estimator error impossible to know.</div></div></div>
        <div class='card'><div class='icon'>🧪</div><div><div class='label'>SIMULATION</div><div class='headline'>The target is known before scoring</div><div class='copy'>The generating distribution defines θ first. Every estimator can then be compared with the same known target.</div></div></div>
      </div>

      <div class='story'><b>Simple idea:</b> simulation is a measurement tool. It gives known truth for validation; it does not replace the external real-data stage.</div>

      <div class='section'>THE FIXED TARGET</div>
      <div class='formula-card'><div class='formula-label'>POPULATION-MEAN ESTIMAND</div><div class='formula'>θ(F) = μ<sub>F</sub> = E<sub>F</sub>[X]</div><div class='formula-copy'>The type of target stays the same throughout the thesis: the population mean. What changes is the data-generating regime around that target.</div></div>

      <div class='section'>FROM KNOWN TRUTH TO MEASURABLE RISK</div>
      <div class='bridge'>
        <div class='bridge-box'><div class='bridge-icon'>🎯</div><div class='bridge-title'>Known truth</div><div class='bridge-copy'>Simulation defines θ before scoring.</div></div>
        <div class='bridge-arrow'>→</div>
        <div class='bridge-box'><div class='bridge-icon'>🔁</div><div class='bridge-title'>Repeated samples</div><div class='bridge-copy'>Layer 4 repeats sampling from the same regime.</div></div>
        <div class='bridge-arrow'>→</div>
        <div class='bridge-box'><div class='bridge-icon'>📊</div><div class='bridge-title'>Measurable risk</div><div class='bridge-copy'>Repeated errors become MSE and q95.</div></div>
      </div>

      <div class='takeaway'>TAKE-HOME: Layer 2 explains why known-truth simulation is needed. Layer 4 shows exactly how repeated sampling turns that truth into evidence.</div>
    </div>"""


def _build_regime() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>02 · DATA-GENERATING WORLD · BUILD A REGIME</div>
      <div class='title'>A regime is one complete statistical environment.</div>
      <div class='subtitle'>The target remains the population mean, while family, contamination and sample size create different finite-sample risk environments.</div>

      <div class='section'>WHAT DEFINES ONE REGIME?</div>
      <div class='builder'>
        <div class='builder-box'><b>F₀</b><span>baseline family</span></div>
        <div class='builder-box'><b>γ</b><span>contamination rate</span></div>
        <div class='builder-box'><b>c</b><span>outlier scale</span></div>
        <div class='builder-box'><b>m</b><span>contamination mechanism</span></div>
        <div class='builder-box'><b>n</b><span>sample size</span></div>
        <div class='builder-box result'><b>ℛ</b><span>one complete regime</span></div>
      </div>
      <div class='formula-card'><div class='formula-label'>REGIME</div><div class='formula'>ℛ = (F₀, γ, c, m, n)</div><div class='formula-copy'>Change any one of these ingredients and the sampling environment can change.</div></div>
      <div class='formula-card'><div class='formula-label'>INDUCED DISTRIBUTION</div><div class='formula'>F<sub>ℛ</sub> = (1−γ)F₀ + γG<sub>m,c</sub>(F₀)</div><div class='formula-copy'>The first term is the clean baseline. The second term adds the designed contamination process.</div></div>

      <div class='section'>SIX STRUCTURAL FAMILIES</div>
      <div class='family-grid'>
        <div class='family'><div class='name'>Normal</div><div class='shape'>SYMMETRIC BASELINE</div><div class='desc'>A clean reference world where the sample mean is difficult to improve.</div></div>
        <div class='family'><div class='name'>Lognormal</div><div class='shape'>POSITIVE RIGHT-SKEW</div><div class='desc'>Strong asymmetry and an upper tail create a different bias–variance problem.</div></div>
        <div class='family'><div class='name'>Weibull</div><div class='shape'>FLEXIBLE POSITIVE SHAPE</div><div class='desc'>A survival-like family with changing shape and tail behaviour.</div></div>
        <div class='family'><div class='name'>Inverse Gaussian</div><div class='shape'>ASYMMETRIC DURATION</div><div class='desc'>A positive duration family with pronounced asymmetry.</div></div>
        <div class='family'><div class='name'>Ex-Gaussian</div><div class='shape'>REACTION-TIME-LIKE TAIL</div><div class='desc'>A Gaussian component plus an exponential tail produces reaction-time-like skew.</div></div>
        <div class='family'><div class='name'>Ex-Wald</div><div class='shape'>FIRST-PASSAGE PROCESS</div><div class='desc'>A positive first-passage family used to stress a different tail structure.</div></div>
      </div>

      <div class='section'>CONTROLLED COVERAGE</div>
      <div class='metricrow'><div class='metric'><div class='v'>6</div><div class='l'>distribution families</div></div><div class='metric'><div class='v'>5</div><div class='l'>sample sizes</div></div><div class='metric'><div class='v'>576</div><div class='l'>profiles per family</div></div><div class='metric'><div class='v'>2,880</div><div class='l'>regimes per family</div></div></div>

      <div class='story'><b>Why this matters:</b> change the regime → change finite-sample risk → potentially change the estimator ranking. This is why the thesis tests conditional performance rather than a universal winner.</div>
      <div class='takeaway'>TAKE-HOME: the regime changes the sampling environment; θ(F)=E[X] remains the population-mean target.</div>
    </div>"""


def _trust_simulator() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>02 · DATA-GENERATING WORLD · VALIDITY</div>
      <div class='title'>The simulated world was audited before the GA evidence was trusted.</div>
      <div class='subtitle'>The generator must first show that it behaves as designed. These checks are independent of whether the GA later wins or loses.</div>

      <div class='metricrow'><div class='metric'><div class='v'>125</div><div class='l'>validation conditions</div></div><div class='metric'><div class='v' style='color:#54c786'>0</div><div class='l'>hard failures</div></div><div class='metric'><div class='v'>29</div><div class='l'>explainable warnings</div></div><div class='metric'><div class='v'>0.976%</div><div class='l'>maximum mean error</div></div></div>

      <div class='story'><b>Validation order:</b> first test the simulator, then interpret estimator performance, and only later interpret GA evidence.</div>

      <div class='section'>FOUR CHECKS</div>
      <div class='check'><div class='check-icon'>🎯</div><div><div class='label'>1 · MOMENT FIDELITY</div><div class='check-title'>Does the generator recover the intended mean?</div><div class='check-copy'>Large generated populations are compared with the analytic mean. Maximum relative mean error was 0.976%, below the 1% hard threshold.</div><div class='check-why'><b>Why it matters:</b> the error surface must be centred on the correct target.</div></div></div>
      <div class='check'><div class='check-icon'>🧫</div><div><div class='label'>2 · CONTAMINATION FIDELITY</div><div class='check-title'>Does the sample contain the stress condition we asked for?</div><div class='check-copy'>Realised contamination rate, direction and MAD-based distance are checked after injection.</div><div class='check-why'><b>Why it matters:</b> regime labels must match what was actually generated.</div></div></div>
      <div class='check'><div class='check-icon'>📐</div><div><div class='label'>3 · THEORY RECOVERY</div><div class='check-title'>Do expected statistical patterns reappear?</div><div class='check-copy'>Known robust-statistics behaviour is checked before new GA conclusions are interpreted.</div><div class='check-why'><b>Why it matters:</b> a pipeline that cannot recover known behaviour should not support new claims.</div></div></div>
      <div class='check'><div class='check-icon'>🌐</div><div><div class='label'>4 · EMPIRICAL ANCHORING</div><div class='check-title'>Is the synthetic world structurally relevant?</div><div class='check-copy'>Real datasets are used as structural anchors. They are not treated as training targets or known population truth.</div><div class='check-why'><b>Why it matters:</b> realism can be checked without pretending that real-data θ is known.</div></div></div>

      <div class='section'>FAIRNESS AND REPRODUCIBILITY</div>
      <div class='two'>
        <div class='card'><div class='icon'>⚖️</div><div><div class='headline'>Same sample path</div><div class='copy'>Inside each Monte Carlo replicate, every estimator sees the same generated sample.</div></div></div>
        <div class='card'><div class='icon'>🔁</div><div><div class='headline'>Fixed seeds and logged regimes</div><div class='copy'>The conditions can be reproduced and audited instead of reconstructed from memory.</div></div></div>
      </div>

      <div class='warn'><b>29 warnings ≠ 29 failures.</b> Warnings are retained diagnostic cases. They can reflect natural 3-MAD flags, dilution, masking, scale effects or empirical anchoring mismatch. Hard failures are counted separately, and there were zero.</div>
      <div class='takeaway'>TAKE-HOME: the simulator is validated independently of the GA. The search is allowed to start only after the data-generating world is credible.</div>
    </div>"""


def data_world_detail_svg(view: int) -> str:
    """Return the current didactic HTML for one of the three Layer 2 views."""
    view = max(0, min(int(view), 2))
    return (_why_simulation, _build_regime, _trust_simulator)[view]()
