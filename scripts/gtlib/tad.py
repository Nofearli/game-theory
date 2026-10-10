"""TAD three-body game (book Ch. 5 / 5.1-5.2).

NOTE ON PROVENANCE
------------------
The source book states the TAD results by reference to the paper's Eq. (14) and
Eq. (15) but does not reproduce those equations verbatim.  The implementation
below is an **independent reconstruction** `[new]`, not a transcription of the
paper's formulas.  It is self-consistent and useful for experimentation, but any
quantitative claim derived from it must be re-verified against the paper.

Conventions: v_A = v_D = 1 (normalised), gamma = v_T / v_A < 1, r = A's capture
radius on T.  A captures T if ||x_T - x_A|| <= r; D captures A at distance 0.
"""
from __future__ import annotations

import numpy as np

from .geometry import norm


def escape_oval_points(x_A, x_T, gamma, r, n=360):
    """Boundary of T's escape set: ||z - x_A|| = ||z - x_T|| / gamma + r.

    Parametrised by the direction u from T; for z = x_T + s u solve
        ||d0 + s u|| = s/gamma + r,   d0 = x_T - x_A,
    which is a quadratic in s (positive root).
    """
    x_A = np.asarray(x_A, float)
    x_T = np.asarray(x_T, float)
    d0 = x_T - x_A
    a_ = 1.0 / gamma ** 2 - 1.0
    pts = []
    for th in np.linspace(0.0, 2.0 * np.pi, n, endpoint=False):
        u = np.array([np.cos(th), np.sin(th)])
        A = a_
        B = -2.0 * (float(np.dot(d0, u)) - r / gamma)
        C = -(float(np.dot(d0, d0)) - r ** 2)
        # A s^2 + B s + C = 0
        disc = B * B - 4.0 * A * C
        if disc < 0:
            continue
        roots = [(-B + np.sqrt(disc)) / (2 * A), (-B - np.sqrt(disc)) / (2 * A)]
        s_pos = [s for s in roots if s > 1e-9]
        if not s_pos:
            continue
        pts.append(x_T + min(s_pos) * u)
    return np.array(pts) if pts else np.empty((0, 2))


def optimal_capture_point(x_A, x_D, x_T, gamma, r, n=720):
    """Reconstruction of z*: the point on T's escape oval that maximises A's safety
    margin ||z - x_D|| - ||z - x_A||  (equal speed => A is unharmed iff this > 0).
    Returns (z_star, oval_points, margin).
    """
    oval = escape_oval_points(x_A, x_T, gamma, r, n=n)
    if not len(oval):
        return None, oval, float("nan")
    x_A = np.asarray(x_A, float)
    x_D = np.asarray(x_D, float)
    margin = (np.hypot(oval[:, 0] - x_D[0], oval[:, 1] - x_D[1])
              - np.hypot(oval[:, 0] - x_A[0], oval[:, 1] - x_A[1]))
    k = int(np.argmax(margin))
    return oval[k], oval, float(margin[k])


def hji_residual(x_A, x_D, x_T, z_star, gamma):
    """A cheap consistency check: the normalised gradients of the two
    arrival-time fields at z* should be anti-parallel along the line of sight.

    Returns a scalar in [0, 2]; ~0 means the terminal conditions are aligned.
    """
    x_A = np.asarray(x_A, float)
    x_T = np.asarray(x_T, float)
    z = np.asarray(z_star, float)
    gA = (z - x_A) / (norm(z - x_A) + 1e-12)
    gT = (z - x_T) / (norm(z - x_T) + 1e-12)
    return float(norm(gA - gT))


def predict_winner(x_A, x_D, x_T, gamma, r):
    """Coarse Kind prediction: A wins iff the best oval point gives a strictly
    positive safety margin (equal speed)."""
    z_star, oval, margin = optimal_capture_point(x_A, x_D, x_T, gamma, r)
    if z_star is None:
        return "T-D", None
    return ("A" if margin > 0 else "T-D"), z_star
