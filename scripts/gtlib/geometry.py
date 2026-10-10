"""Core geometry for pursuit-evasion games (book Ch. 1 / 1.1).

Conventions
-----------
- `a = v_p / v_e > 1` is the speed ratio (defender faster).
- Capture is `||p_p - p_e|| <= r`.
- The attacker's SAFE SET is `g(x) <= 0` with
      g(x) = -||x - p_p|| + a*||x - p_e|| + r .
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


def norm(v) -> float:
    v = np.asarray(v, dtype=float)
    return float(np.hypot(v[0], v[1])) if v.size == 2 else float(np.linalg.norm(v))


def time_to_go(x, p, v) -> float:
    """Time for an agent at `p` moving at speed `v` to reach `x`."""
    return norm(np.asarray(x, float) - np.asarray(p, float)) / float(v)


def apollonius_g(x, p_p, p_e, a, r) -> float:
    """Attacker safe-set function: g <= 0 means the attacker reaches `x` first."""
    x = np.asarray(x, float)
    p_p = np.asarray(p_p, float)
    p_e = np.asarray(p_e, float)
    return -norm(x - p_p) + a * norm(x - p_e) + r


def apollonius_circle(p_p, p_e, a):
    """Circle {x : ||x-p_p|| = a ||x-p_e||}. Returns (center, radius) or None if a==1."""
    p_p = np.asarray(p_p, float)
    p_e = np.asarray(p_e, float)
    if abs(a - 1.0) < 1e-12:
        return None  # parabola / line
    c = (p_p - a * a * p_e) / (1.0 - a * a)
    rho = a * norm(p_p - p_e) / abs(1.0 - a * a)
    return c, rho


def solve_breakthrough(pursuers, p_e, r, x0=None, bounds=None, max_iter=400):
    """Attacker's optimal breakthrough point: maximise x1 s.t. g_i(x) <= 0 for all pursuers.

    Parameters
    ----------
    pursuers : iterable of (position, a)  -- one entry per defender (a = v_p/v_e)
    p_e      : attacker position (used as default initial guess)
    r        : capture radius
    x0       : initial guess (default = attacker position; never the defender!)
    bounds : optional 4-tuple (xmin, xmax, ymin, ymax) for the search box

    Returns
    -------
    dict with keys: x (np.ndarray), x1, success, message
    """
    pursuers = [(np.asarray(p, float), float(a)) for p, a in pursuers]
    p_e = np.asarray(p_e, float)
    x0 = p_e.copy() if x0 is None else np.asarray(x0, float)

    def neg_obj(x):
        return -x[0]

    cons = [{"type": "ineq",
             "fun": (lambda x, pp=pp, aa=aa: -apollonius_g(x, pp, p_e, aa, r))}
            for pp, aa in pursuers]

    kw = {}
    if bounds is not None:
        xmin, xmax, ymin, ymax = bounds
        if not (xmin < xmax and ymin < ymax):
            raise ValueError("bounds must satisfy xmin<xmax and ymin<ymax")
        kw["bounds"] = [(xmin, xmax), (ymin, ymax)]
    res = minimize(neg_obj, x0, method="SLSQP", constraints=cons,
                   options={"maxiter": max_iter, "ftol": 1e-12}, **kw)
    return {"x": res.x, "x1": float(res.x[0]), "success": bool(res.success),
            "message": str(res.message)}


def judge_interception(pursuers, p_e, r, x_d, **kw):
    """Return dict(x1*, success(bool), verdict(str)) for the defence line x = x_d."""
    out = solve_breakthrough(pursuers, p_e, r, **kw)
    ok = out["x1"] < x_d
    out["verdict"] = "interception succeeds" if ok else "interception fails"
    out["intercepted"] = bool(ok)
    return out


def safe_set_grid(pursuers, p_e, r, xs, ys):
    """Evaluate min_i g_i on a grid (<=0 inside the attacker safe set)."""
    X, Y = np.meshgrid(np.asarray(xs, float), np.asarray(ys, float))
    G = np.full_like(X, np.inf)
    for pp, a in pursuers:
        G = np.minimum(G, -np.hypot(X - pp[0], Y - pp[1])
                       + a * np.hypot(X - p_e[0], Y - p_e[1]) + r)
    return X, Y, G
