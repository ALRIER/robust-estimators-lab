from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class DemoScenario:
    family: str = "normal"
    contamination: str = "upper_tail"
    contamination_rate: float = 0.10
    outlier_scale: float = 10.0
    n: int = 500
    seed: int = 20260808

@dataclass(frozen=True)
class DemoSample:
    values: np.ndarray
    is_outlier: np.ndarray
    true_location: float


def _base_sample(rng: np.random.Generator, family: str, n: int):
    if family == "normal":
        x = rng.normal(0.0, 1.0, n)
        target = 0.0
    elif family == "lognormal":
        # shifted so the demonstration target is the known population mean after centering
        raw = rng.lognormal(mean=0.0, sigma=0.55, size=n)
        pop_mean = np.exp(0.55**2 / 2)
        x = raw - pop_mean
        target = 0.0
    elif family == "weibull":
        shape = 1.7
        raw = rng.weibull(shape, n)
        # Center empirically only for teaching visualization; do not treat as thesis evidence.
        x = raw - np.mean(raw)
        target = 0.0
    elif family == "exgaussian":
        x = rng.normal(0.0, 1.0, n) + rng.exponential(0.7, n) - 0.7
        target = 0.0
    else:
        x = rng.normal(0.0, 1.0, n)
        target = 0.0
    return x, target


def draw_sample(s: DemoScenario) -> DemoSample:
    rng = np.random.default_rng(s.seed)
    x, target = _base_sample(rng, s.family, s.n)
    m = int(round(np.clip(s.contamination_rate, 0, 0.95) * s.n))
    mask = np.zeros(s.n, dtype=bool)
    if s.contamination == "none" or m == 0:
        return DemoSample(x, mask, target)
    idx = rng.choice(s.n, size=m, replace=False)
    mask[idx] = True
    if s.contamination == "upper_tail":
        x[idx] += abs(s.outlier_scale) + rng.normal(0, 0.5, m)
    elif s.contamination == "symmetric":
        signs = rng.choice([-1.0, 1.0], size=m)
        x[idx] += signs * abs(s.outlier_scale)
    elif s.contamination == "bimodal":
        signs = rng.choice([-1.0, 1.0], size=m)
        x[idx] = signs * abs(s.outlier_scale) + rng.normal(0, 0.7, m)
    elif s.contamination == "point_mass":
        x[idx] = abs(s.outlier_scale)
    return DemoSample(x, mask, target)
