"""Reconnaissance-return (capture-the-flag) game (book Ch. 6).

Convention used here (book Ch. 6.3-6.5): goal line x = 0, reconnaissance boundary
x = l, play region 0 < x < l.  alpha = v_P / v_E > 1, r_c capture radius.

PROVENANCE
----------
The book states the closed-form dome / wedge barriers and the tau_max theorem by
reference to the source papers.  This module provides (a) the exact *virtual
evader* transformation from the book and (b) an **independent, numerically
evaluated** barrier / dwell-time model `[new]`.  It is self-consistent; for
publication numbers use the paper's closed form.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize, brentq

from .geometry import norm


def virtual_evader(x_E, y_E, l, sigma, v_E, tau):
    """Virtual (reflected + translated) evader (book 6.0 symbol table):

        x_tilde_E = (2l - x_E, y_E + sigma * v_E * tau)
    """
    return np.array([2.0 * l - float(x_E), float(y_E) + sigma * float(v_E) * float(tau)])


def _path_time_2stage(z_E, l, y_I, y_r, v_E):
    d1 = norm(np.array([l, y_I]) - z_E)
    d2 = norm(np.array([0.0, y_r]) - np.array([l, y_I]))
    return (d1 + d2) / v_E


def _path_time_3stage(z_E, l, y_I, y_r, v_E, sigma, tau):
    d1 = norm(np.array([l, y_I]) - z_E)
    d2 = norm(np.array([0.0, y_r]) - np.array([l, y_I + sigma * v_E * tau]))
    return (d1 + v_E * tau + d2) / v_E


def success_margin(z_E, x_P, l, alpha, r_c, tau=0.0, sigma=1.0, v_E=1.0,
                   y_span=None, n_starts=2):
    """Max over (y_I, y_r) of  [T_P - T_E - r_c/v_P].

    Positive => the evader can complete the (recon + dwell + return) task before the
    pursuer reaches the return point.  Simplified model: the pursuer is assumed to
    guard the goal (it is not allowed to intercept during the reconnaissance leg).
    """
    z_E = np.asarray(z_E, float)
    x_P = np.asarray(x_P, float)
    v_P = alpha * v_E
    span = y_span if y_span is not None else 6.0

    def neg_margin(p):
        y_I, y_r = p
        if tau <= 0.0:
            T_E = _path_time_2stage(z_E, l, y_I, y_r, v_E)
        else:
            T_E = _path_time_3stage(z_E, l, y_I, y_r, v_E, sigma, tau)
        T_P = norm(np.array([0.0, y_r]) - x_P) / v_P
        return -(T_P - T_E - r_c / v_P)

    starts = [(float(z_E[1]), float(x_P[1])), (0.0, 0.0),
              (float(z_E[1]), 0.0), (0.0, float(x_P[1]))]
    starts += [(a, b) for a in np.linspace(-span, span, n_starts)
               for b in np.linspace(-span, span, n_starts)]
    best = None
    for s in starts:
        res = minimize(neg_margin, s, method="Nelder-Mead",
                       options={"xatol": 1e-6, "fatol": 1e-9, "maxiter": 800})
        if best is None or res.fun < best.fun:
            best = res
    return -float(best.fun), best.x


def barrier_contour(x_P, l, alpha, r_c, tau=0.0, sigma=1.0,
                    x_span=(0.05, None), y_span=(-5.0, 5.0), nx=120, ny=120):
    """Numerically evaluated barrier: the zero level set of `success_margin` over
    the evader's initial position.  Returns (X, Y, M) with M the margin grid
    (M > 0 => evader wins).
    """
    x0, x1 = x_span
    x1 = l - 0.05 if x1 is None else x1
    xs = np.linspace(x0, x1, nx)
    ys = np.linspace(y_span[0], y_span[1], ny)
    X, Y = np.meshgrid(xs, ys)
    M = np.empty_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            m, _ = success_margin((X[i, j], Y[i, j]), x_P, l, alpha, r_c,
                                  tau=tau, sigma=sigma)
            M[i, j] = m
    return X, Y, M


def max_dwell_time(z_E, x_P, l, alpha, r_c, sigma=1.0, v_E=1.0,
                   tau_hi=20.0, tol=1e-4):
    """Largest dwell time tau with success_margin >= 0 (scalar root-finding).

    Theorem (book 6.5): tau_max exists and is unique under the stated assumptions;
    here it is obtained by bisection on the scalar margin.
    """
    def m(t):
        return success_margin(z_E, x_P, l, alpha, r_c, tau=t, sigma=sigma, v_E=v_E)[0]

    if m(0.0) < 0:
        return 0.0
    if m(tau_hi) > 0:
        return tau_hi
    return float(brentq(m, 0.0, tau_hi, xtol=tol))


def two_stage_vs_three_stage(z_E, x_P, l, alpha, r_c, sigma=1.0):
    """Convenience: margins at tau = 0 (two-stage) and at tau_max (three-stage)."""
    m0 = success_margin(z_E, x_P, l, alpha, r_c, tau=0.0, sigma=sigma)[0]
    tmax = max_dwell_time(z_E, x_P, l, alpha, r_c, sigma=sigma)
    return {"margin_tau0": m0, "tau_max": tmax}
