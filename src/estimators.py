import numpy as np
from scipy import stats


def _mad(x):
    med = np.median(x)
    return np.median(np.abs(x - med))


def huber_location(x, k=1.5, max_iter=50, tol=1e-8):
    x = np.asarray(x, dtype=float)
    mu = np.median(x)
    scale = 1.4826 * _mad(x)
    if not np.isfinite(scale) or scale <= 1e-12:
        return float(mu)
    for _ in range(max_iter):
        r = (x - mu) / scale
        w = np.ones_like(r)
        nz = np.abs(r) > k
        w[nz] = k / np.abs(r[nz])
        new_mu = np.sum(w * x) / np.sum(w)
        if abs(new_mu - mu) < tol:
            break
        mu = new_mu
    return float(mu)


def biweight_location(x, c=4.685, max_iter=50, tol=1e-8):
    x = np.asarray(x, dtype=float)
    mu = np.median(x)
    mad = _mad(x)
    if not np.isfinite(mad) or mad <= 1e-12:
        return float(mu)
    scale = 1.4826 * mad
    for _ in range(max_iter):
        u = (x - mu) / (c * scale)
        keep = np.abs(u) < 1
        if not np.any(keep):
            return float(mu)
        w = (1 - u[keep] ** 2) ** 2
        new_mu = np.sum(w * x[keep]) / np.sum(w)
        if abs(new_mu - mu) < tol:
            break
        mu = new_mu
    return float(mu)


def location_estimates(x):
    x = np.asarray(x, dtype=float)
    return {
        "Mean": float(np.mean(x)),
        "Median": float(np.median(x)),
        "Trimmed Mean": float(stats.trim_mean(x, 0.20)),
        "Huber": huber_location(x),
        "Biweight": biweight_location(x),
    }
