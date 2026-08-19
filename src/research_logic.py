"""Layer 1 · Research logic.

Five didactic views for the opening of the timed defense. The scientific content
is unchanged: fixed population-mean target, regime-dependent finite-sample risk,
H1–H4, interpretable simplex mixtures, and the bias–variance condition for
conditional improvement.
"""

PANELS = (
    ("Why a problem?", "The target stays fixed while risk rankings can change.", "No universal estimator is assumed.", "Change the regime, and the best choice may change."),
    ("What are we asking?", "Can search find an interpretable improvement that survives validation?", "Search proposes; evidence decides.", "The question is conditional, not universal."),
    ("What should happen?", "H1–H4 turn the intuition into testable predictions.", "The study can succeed by retaining the benchmark.", "The hypotheses define what counts as evidence."),
    ("What can GA change?", "The target is fixed; only the estimator recipe evolves.", "Simplex weights keep the recipe interpretable.", "Valid weights are not proof of better performance."),
    ("When can it win?", "A mixture wins only through a favourable bias–variance trade-off.", "Variance reduction must pay for squared bias.", "Improvement is conditional and must pass the gate."),
)


def _css() -> str:
    return """
    <style>
      *{box-sizing:border-box}
      body{margin:0;background:#081525;color:#e9f4ff;font-family:Arial,sans-serif}
      .page{padding:28px 32px 38px;background:#081525}
      .kicker{font-size:14px;font-weight:900;letter-spacing:.13em;color:#72cfff;margin-bottom:9px}
      .title{font-size:39px;line-height:1.14;font-weight:900;color:#fff;margin-bottom:10px}
      .subtitle{font-size:19px;line-height:1.5;color:#bfd0e2;margin-bottom:25px;max-width:1280px}
      .section{font-size:21px;font-weight:900;color:#f3c743;letter-spacing:.05em;margin:30px 0 14px}
      .story{background:#0f2b47;border:1px solid #3c7198;border-left:7px solid #72cfff;border-radius:14px;padding:19px 21px;margin:17px 0;font-size:18px;line-height:1.5;color:#eef6ff}
      .takeaway{background:#12354a;border:1px solid #58aee8;border-left:7px solid #f3c743;border-radius:14px;padding:21px 23px;margin:24px 0 4px;font-size:20px;line-height:1.45;font-weight:850;color:#fff}
      .warn{background:#342b12;border:1px solid #f3c743;border-left:7px solid #f3c743;color:#fff2b8;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:20px 0}
      .good{background:#10372e;border:1px solid #54c786;border-left:7px solid #54c786;color:#d7ffe5;border-radius:14px;padding:18px 20px;font-size:17px;line-height:1.48;margin:18px 0}
      .two{display:grid;grid-template-columns:1fr 1fr;gap:17px}
      .three{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}
      .four{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
      .card{display:grid;grid-template-columns:96px 1fr;gap:20px;align-items:center;background:linear-gradient(145deg,#0e2945,#0a1d32);border:1px solid #356e99;border-radius:15px;padding:21px 23px;margin-bottom:16px;min-height:150px}
      .icon{width:78px;height:78px;border-radius:19px;background:#10253a;border:1px solid #3c7198;display:flex;align-items:center;justify-content:center;font-size:39px;margin:auto}
      .label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:6px}
      .headline{font-size:26px;font-weight:900;line-height:1.18;color:#fff;margin-bottom:8px}
      .copy{font-size:17px;line-height:1.49;color:#dce9f8}
      .mini{font-size:15px;line-height:1.44;color:#b9c8d9;margin-top:8px}
      .formula-card{background:#0b2138;border:1px solid #356e99;border-left:6px solid #f3c743;border-radius:14px;padding:19px 21px;margin:15px 0}
      .formula-label{font-size:13px;font-weight:900;letter-spacing:.11em;color:#72cfff;margin-bottom:7px}
      .formula{font-family:Georgia,serif;font-size:30px;font-weight:800;line-height:1.35;color:#f7d768;margin-bottom:9px}
      .formula-copy{font-size:17px;line-height:1.48;color:#dce9f8}
      .flow{display:flex;align-items:stretch;gap:9px;margin:17px 0;flex-wrap:wrap}
      .flowbox{flex:1;min-width:150px;background:#10253a;border:1px solid #356e99;border-radius:12px;padding:15px;text-align:center}
      .flowbox .ficon{font-size:30px;margin-bottom:7px}.flowbox .fh{font-size:17px;font-weight:900;color:#fff;margin-bottom:5px}.flowbox .fc{font-size:14px;line-height:1.37;color:#bfd0e2}
      .flowarrow{display:flex;align-items:center;justify-content:center;color:#72cfff;font-size:28px;font-weight:900}
      .hyp{background:#0d2239;border:1px solid #356e99;border-radius:14px;padding:18px;min-height:255px;display:flex;flex-direction:column}
      .hyp .hn{font-size:31px;font-weight:900;color:#f3c743;margin-bottom:7px}.hyp .hh{font-size:20px;font-weight:900;color:#fff;margin-bottom:8px}.hyp .hc{font-size:15px;line-height:1.43;color:#dce9f8}.hyp .role{margin-top:auto;padding-top:12px;border-top:1px solid #315879;font-size:13px;font-weight:900;letter-spacing:.08em;color:#72cfff}
      .builder{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:17px 0}
      .weight-card{background:#10253a;border:1px solid #356e99;border-radius:13px;padding:16px 17px}.weight-name{font-size:16px;font-weight:900;color:#fff;margin-bottom:9px}.bar{height:18px;background:#071525;border:1px solid #315879;border-radius:9px;overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,#58aee8,#a777e3)}.weight-value{font-size:14px;color:#bfd0e2;margin-top:7px;text-align:right}
      .balance{display:grid;grid-template-columns:1fr 90px 1fr;gap:16px;align-items:center;margin:18px 0}.balance-box{background:#10253a;border:1px solid #356e99;border-radius:14px;padding:20px;text-align:center}.balance-box .bh{font-size:23px;font-weight:900;color:#fff;margin-bottom:7px}.balance-box .bc{font-size:16px;line-height:1.44;color:#dce9f8}.balance-mid{text-align:center;font-size:44px;color:#f3c743;font-weight:900}
      .condition{background:#10372e;border:1px solid #54c786;border-radius:14px;padding:20px 22px;margin:17px 0}.condition .ch{font-size:20px;font-weight:900;color:#d7ffe5;margin-bottom:8px}.condition .cc{font-size:18px;line-height:1.47;color:#e9fff0}
      @media(max-width:1050px){.two,.three,.four,.builder{grid-template-columns:1fr 1fr}.balance{grid-template-columns:1fr}.balance-mid{font-size:30px}.card{grid-template-columns:78px 1fr}.flowarrow{display:none}}
    </style>
    """


def _problem() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>01 · RESEARCH LOGIC · WHY A PROBLEM?</div>
      <div class='title'>The target stays fixed. The statistical environment does not.</div>
      <div class='subtitle'>The opening problem is not “which estimator is best?” It is “does the best choice change when the data-generating regime changes?”</div>

      <div class='two'>
        <div class='card'><div class='icon'>🎯</div><div><div class='label'>WHAT STAYS FIXED</div><div class='headline'>The population mean</div><div class='copy'>Every estimator is judged against the same type of target: θ(F)=μ<sub>F</sub>=E<sub>F</sub>[X].</div></div></div>
        <div class='card'><div class='icon'>🌦️</div><div><div class='label'>WHAT CAN CHANGE</div><div class='headline'>The sampling environment</div><div class='copy'>Family, contamination, outlier severity, mechanism and sample size change finite-sample risk.</div></div></div>
      </div>

      <div class='section'>TWO SIMPLE WORLDS</div>
      <div class='two'>
        <div class='card'><div class='icon'>🔔</div><div><div class='headline'>Clean / near-symmetric</div><div class='copy'>The sample mean can be very efficient. There may be little room for a composite to improve.</div><div class='mini'>Audience inference: if the mean is already strong, replacement should be difficult.</div></div></div>
        <div class='card'><div class='icon'>🌪️</div><div><div class='headline'>Skewed / contaminated</div><div class='copy'>Extreme observations can change the error distribution. Robust estimators may move less and the ranking can change.</div><div class='mini'>Audience inference: different regimes can create different opportunities.</div></div></div>
      </div>

      <div class='flow'><div class='flowbox'><div class='ficon'>🔄</div><div class='fh'>Change regime</div><div class='fc'>Change the data-generating environment.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>📉</div><div class='fh'>Change risk</div><div class='fc'>Bias, variance and difficult-case error can move.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>🏆</div><div class='fh'>Change ranking</div><div class='fc'>The best admissible estimator may change.</div></div></div>

      <div class='takeaway'>TAKE-HOME: no universal winner is assumed. The thesis asks which estimator is justified inside a defined regime.</div>
    </div>"""


def _question() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>01 · RESEARCH LOGIC · WHAT ARE WE ASKING?</div>
      <div class='title'>Can evolutionary search find an interpretable improvement that survives independent evidence?</div>
      <div class='subtitle'>This separates the optimization problem from the scientific claim. A promising candidate is not yet a result.</div>

      <div class='section'>THE RESEARCH PROGRAMME IN ONE LINE</div>
      <div class='flow'><div class='flowbox'><div class='ficon'>🔎</div><div class='fh'>SEARCH</div><div class='fc'>Propose simplex weight vectors.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>🧊</div><div class='fh'>FREEZE</div><div class='fc'>Lock the candidate recipe.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>🥊</div><div class='fh'>CHALLENGE</div><div class='fc'>Use fresh evidence and stronger comparators.</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='ficon'>🚪</div><div class='fh'>ACCEPT / ABSTAIN</div><div class='fc'>Replace only if the gate supports it.</div></div></div>

      <div class='section'>FOUR QUESTIONS, ONE LOGIC</div>
      <div class='two'>
        <div class='card'><div class='icon'>1</div><div><div class='label'>RQ1 · DISCOVERY</div><div class='headline'>Where can a composite improve?</div><div class='copy'>Search controlled regimes for promising interpretable mixtures.</div></div></div>
        <div class='card'><div class='icon'>2</div><div><div class='label'>RQ2 · CONFIRMATION</div><div class='headline'>Do the gains survive frozen weights?</div><div class='copy'>Retest the same recipe on independent evidence without retraining.</div></div></div>
        <div class='card'><div class='icon'>3</div><div><div class='label'>RQ3 · EXPANDED BASIS</div><div class='headline'>What changes when the search basis becomes stronger?</div><div class='copy'>Reopen the search from 10 to 26 learnable components.</div></div></div>
        <div class='card'><div class='icon'>4</div><div><div class='label'>RQ4 · TRANSFER</div><div class='headline'>Do validated specialists travel?</div><div class='copy'>Test related regimes and external empirical data without changing the frozen recipe.</div></div></div>
      </div>

      <div class='good'><b>Success is deliberately two-sided:</b> a supported specialist is useful evidence, but justified benchmark retention is also a valid scientific outcome.</div>
      <div class='takeaway'>TAKE-HOME: search proposes. Validation decides. The question is “when is replacement justified?” — not “can the GA always win?”</div>
    </div>"""


def _hypotheses() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>01 · RESEARCH LOGIC · WHAT SHOULD HAPPEN?</div>
      <div class='title'>H1–H4 make the expected pattern explicit before looking at results.</div>
      <div class='subtitle'>The hypotheses form one reasoning chain: scope → regime dependence → selective opportunity → claim control.</div>

      <div class='four'>
        <div class='hyp'><div class='hn'>H1</div><div class='hh'>No universal estimator</div><div class='hc'>Different regimes can have different winners.</div><div class='role'>SCOPE</div></div>
        <div class='hyp'><div class='hn'>H2</div><div class='hh'>Performance depends on regime</div><div class='hc'>Finite-sample risk changes with F<sub>ℛ</sub> and n.</div><div class='role'>MECHANISM</div></div>
        <div class='hyp'><div class='hn'>H3</div><div class='hh'>GA helps selectively</div><div class='hc'>Only some regimes should create enough opportunity for replacement.</div><div class='role'>OPPORTUNITY</div></div>
        <div class='hyp'><div class='hn'>H4</div><div class='hh'>The gate controls claims</div><div class='hc'>Unsupported candidates must return to the benchmark.</div><div class='role'>CLAIM CONTROL</div></div>
      </div>

      <div class='flow'><div class='flowbox'><div class='fh'>H1</div><div class='fc'>No universal winner</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='fh'>H2</div><div class='fc'>Risk depends on regime</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='fh'>H3</div><div class='fc'>Opportunity should be selective</div></div><div class='flowarrow'>→</div><div class='flowbox'><div class='fh'>H4</div><div class='fc'>Evidence can reject replacement</div></div></div>

      <div class='story'><b>What should the audience infer?</b> If the final results show only a few narrow winners and many benchmark-retained cases, that pattern is compatible with the hypotheses — it is not a failed GA story.</div>
      <div class='takeaway'>TAKE-HOME: the expected result is selective improvement under explicit claim control, not widespread GA dominance.</div>
    </div>"""


def _target_simplex() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>01 · RESEARCH LOGIC · WHAT CAN THE GA CHANGE?</div>
      <div class='title'>The GA evolves the estimator recipe — never the scientific target.</div>
      <div class='subtitle'>This separates the estimand from the estimator and keeps every candidate inspectable.</div>

      <div class='section'>1 · FIXED TARGET</div>
      <div class='formula-card'><div class='formula-label'>ESTIMAND</div><div class='formula'>θ(F) = μ<sub>F</sub> = E<sub>F</sub>[X]</div><div class='formula-copy'>Every candidate estimates the population mean. The target is not moved to make the problem easier.</div></div>

      <div class='section'>2 · EVOLVING RECIPE</div>
      <div class='formula-card'><div class='formula-label'>COMPOSITE ESTIMATOR</div><div class='formula'>θ̂<sub>w,n</sub> = Σ<sub>j=1</sub><sup>L</sup> wⱼTⱼ,n</div><div class='formula-copy'>Each GA individual is a vector of weights over named base estimators.</div></div>
      <div class='builder'>
        <div class='weight-card'><div class='weight-name'>Mean</div><div class='bar'><div class='fill' style='width:18%'></div></div><div class='weight-value'>18%</div></div>
        <div class='weight-card'><div class='weight-name'>Median</div><div class='bar'><div class='fill' style='width:27%'></div></div><div class='weight-value'>27%</div></div>
        <div class='weight-card'><div class='weight-name'>Huber</div><div class='bar'><div class='fill' style='width:24%'></div></div><div class='weight-value'>24%</div></div>
        <div class='weight-card'><div class='weight-name'>Biweight</div><div class='bar'><div class='fill' style='width:31%'></div></div><div class='weight-value'>31%</div></div>
      </div>

      <div class='section'>3 · SIMPLEX RULE</div>
      <div class='formula-card'><div class='formula-label'>INTERPRETABLE SEARCH SPACE</div><div class='formula'>w ∈ Δ<sub>L</sub>, &nbsp; wⱼ ≥ 0, &nbsp; Σwⱼ = 1</div><div class='formula-copy'>No negative weights. All weights add to 100%. The final recipe remains a convex mixture of named estimators.</div></div>

      <div class='warn'><b>Important distinction:</b> a simplex-valid vector is interpretable, but it is not automatically robust, admissible on every support, or better than the benchmark.</div>
      <div class='takeaway'>TAKE-HOME: the estimand never moves. Only the estimator recipe evolves, and evidence must still prove lower finite-sample risk.</div>
    </div>"""


def _why_win() -> str:
    return _css() + """
    <div class='page'>
      <div class='kicker'>01 · RESEARCH LOGIC · WHEN CAN A MIXTURE WIN?</div>
      <div class='title'>Only when variance reduction is large enough to pay for squared bias.</div>
      <div class='subtitle'>This is the statistical reason a composite can help in some regimes and still lose in others.</div>

      <div class='section'>FINITE-SAMPLE RISK</div>
      <div class='formula-card'><div class='formula-label'>MSE DECOMPOSITION</div><div class='formula'>MSE<sub>F,n</sub>(θ̂<sub>w,n</sub>) = B<sub>n</sub>(w,F)² + V<sub>n</sub>(w,F)</div><div class='formula-copy'>MSE is squared bias plus variance. Robust components may introduce some bias but can reduce sampling variability or sensitivity to extremes.</div></div>

      <div class='balance'>
        <div class='balance-box'><div class='bh'>Squared bias cost</div><div class='bc'>Moving weight away from the sample mean can move the expected estimate away from μ<sub>F</sub>.</div></div>
        <div class='balance-mid'>⚖️</div>
        <div class='balance-box'><div class='bh'>Variance reduction</div><div class='bc'>Robust components can reduce instability created by skew, tails or contamination.</div></div>
      </div>

      <div class='condition'><div class='ch'>WHEN DOES IT BEAT THE SAMPLE MEAN?</div><div class='cc'>B<sub>n</sub>(w,F)² + V<sub>n</sub>(w,F) &lt; Var<sub>F</sub>(X̄<sub>n</sub>)</div></div>

      <div class='two'>
        <div class='card'><div class='icon'>🔔</div><div><div class='headline'>Clean light-tailed symmetry</div><div class='copy'>The sample mean is already highly efficient. There may be little variance reduction available to justify added bias.</div></div></div>
        <div class='card'><div class='icon'>🌪️</div><div><div class='headline'>Skew / tails / contamination</div><div class='copy'>Extremes can increase finite-sample instability. A robust mixture may sometimes reduce risk enough to compensate for bias.</div></div></div>
      </div>

      <div class='story'><b>And the thesis is stricter than this equation:</b> the final candidate must beat the strongest admissible benchmark on both mean MSE and q95 MSE.</div>
      <div class='takeaway'>TAKE-HOME: a composite can win, but only conditionally. Validity creates a candidate; the bias–variance trade-off creates opportunity; the gate decides the claim.</div>
    </div>"""


def research_logic_svg(panel: int) -> str:
    """Return the current didactic HTML for one of the five Layer 1 views."""
    panel = max(0, min(int(panel), 4))
    return (_problem, _question, _hypotheses, _target_simplex, _why_win)[panel]()
