import numpy as np
from src.estimators import location_estimates


def test_estimators_are_finite():
    x = np.array([-1,-0.5,0,0.2,0.4,30.0], dtype=float)
    out = location_estimates(x)
    assert set(out) == {"Mean", "Median", "Trimmed Mean", "Huber", "Biweight"}
    assert all(np.isfinite(v) for v in out.values())


def test_upper_outlier_moves_mean_more_than_median():
    x = np.r_[np.zeros(100), 100.0]
    out = location_estimates(x)
    assert abs(out["Mean"]) > abs(out["Median"])
