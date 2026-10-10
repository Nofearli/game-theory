"""Barriers (book Ch. 3 / 3.0-3.3).

The barrier's independent variable is the ATTACKER'S INITIAL POSITION z (not a
spatial point). Here the target is the segment on y=0 from m=(0,0) to n=(l,0).

Conventions: alpha = v_P / v_E > 1.  Code sometimes uses ratio = 1/alpha.
"""
from __future__ import annotations

import numpy as np

from .geometry import norm


def barrier_1v1_points(D, alpha, l, n=300, upper_only=True):
    """Closed-form 1v1 barrier (r = 0): arc - hyperbola - arc.

    D=(xD,yD) defender, target segment [0,l] on y=0.
    Joints: delta1 = xD/alpha^2, delta2 = delta1 + (1 - 1/alpha^2) l.
    """
    D = np.asarray(D, float)
    xD, yD = D
    d1 = xD / alpha ** 2
    d2 = d1 + (1.0 - 1.0 / alpha ** 2) * l
    th = np.linspace(0.0, 2.0 * np.pi, 4000)

    # B1: circle centred at m=(0,0), radius ||D-m||/alpha, restricted to x <= d1
    R1 = norm(D) / alpha
    a1 = np.column_stack([R1 * np.cos(th), R1 * np.sin(th)])
    a1 = a1[a1[:, 0] <= d1]
    if upper_only:
        a1 = a1[a1[:, 1] >= -1e-12]
    a1 = a1[np.argsort(a1[:, 0])]

    # B2: hyperbola branch
    xs = np.linspace(d1, d2, n)
    ys = np.sqrt(np.maximum(0.0, yD ** 2 / alpha ** 2 + (xs - xD) ** 2 / (alpha ** 2 - 1.0)))
    b2 = np.column_stack([xs, ys])

    # B3: circle centred at n=(l,0), radius ||D-n||/alpha, restricted to x >= d2
    R3 = norm(D - np.array([l, 0.0])) / alpha
    a3 = np.column_stack([l + R3 * np.cos(th), R3 * np.sin(th)])
    a3 = a3[a3[:, 0] >= d2]
    if upper_only:
        a3 = a3[a3[:, 1] >= -1e-12]
    a3 = a3[np.argsort(a3[:, 0])]

    return np.vstack([a1, b2, a3])


def cartesian_oval_points(D, alpha, r, taus):
    """Parametric barrier for capture radius r (Xu 2024, Thm 4.1), r >= 0.

    z(tau) = (tau - m n, m sqrt(1 - n^2)),  m = (||tau-D|| - r)/alpha,
    n = (tau - D_x)/(alpha ||tau-D||).  Only feasible taus (m >= 0) are returned.
    """
    D = np.asarray(D, float)
    pts = []
    for tau in np.atleast_1d(taus):
        P = np.array([float(tau), 0.0])
        dP = norm(P - D)
        if dP <= 1e-12:
            continue
        m = (dP - r) / alpha
        if m < 0.0:
            continue
        nn = (float(tau) - D[0]) / (alpha * dP)
        if abs(nn) > 1.0 + 1e-12:
            continue
        zx = float(tau) - m * nn
        zy = m * np.sqrt(max(0.0, 1.0 - nn ** 2))
        pts.append((zx, zy))
    return np.array(pts) if pts else np.empty((0, 2))


def escape_point_map(x, D, alpha):
    """Escape point tau corresponding to barrier abscissa x (book 3.0 Eq. for tau(x)):

        tau(x) = (alpha^2 x - x_D) / (alpha^2 - 1)
    """
    return (alpha ** 2 * float(x) - float(np.asarray(D, float)[0])) / (alpha ** 2 - 1.0)


def bisector_split(D1, D2, l):
    """Escape-point split xz on the target line (perpendicular bisector)."""
    D1 = np.asarray(D1, float)
    D2 = np.asarray(D2, float)
    dx = D2[0] - D1[0]
    if abs(dx) < 1e-12:
        return np.nan
    return float((np.dot(D2, D2) - np.dot(D1, D1)) / (2.0 * dx))


def barrier_2v1_points(D1, D2, alpha, l, r=0.0, n=300):
    """2v1 non-overlapping barrier: D1 on [0, xz], D2 on [xz, l], joined by an arc
    centred at xz of radius (||xz - D|| - r)/alpha (equal for both defenders).

    Falls back to the 1v1 barrier if xz is outside [0, l] (degenerate deployment).
    """
    xz = bisector_split(D1, D2, l)
    if not np.isfinite(xz) or xz <= 0.0 or xz >= l:
        return barrier_1v1_points(D1, alpha, l, n=n)

    p1 = cartesian_oval_points(D1, alpha, r, np.linspace(0.0, xz, n))
    p2 = cartesian_oval_points(D2, alpha, r, np.linspace(xz, l, n))

    # joining arc: circle centred at (xz,0), radius (||xz-D||-r)/alpha
    Rj = (norm(np.array([xz, 0.0]) - np.asarray(D1, float)) - r) / alpha
    arc = []
    if Rj > 0 and len(p1) and len(p2):
        a_start = np.arctan2(p1[-1, 1], p1[-1, 0] - xz)
        a_end = np.arctan2(p2[0, 1], p2[0, 0] - xz)
        # choose the short way round
        da = a_end - a_start
        while da > np.pi:
            da -= 2 * np.pi
        while da < -np.pi:
            da += 2 * np.pi
        aa = a_start + np.linspace(0.0, da, 40)
        arc = np.column_stack([xz + Rj * np.cos(aa), Rj * np.sin(aa)])
    parts = [p1] + ([arc] if len(arc) else []) + [p2]
    parts = [p for p in parts if len(p)]
    return np.vstack(parts) if parts else np.empty((0, 2))


def on_barrier(z, D, alpha, r=0.0, l=3.0, n=20001):
    """Criticality residual for a 1v1 barrier point z.

    The attacker at z wins iff  max_{tau in [0,l]} f(tau) > 0  with
        f(tau) = ||tau - D|| - r - alpha ||tau - z|| .
    On the barrier this maximum is 0.  Returns (residual, tau_star).
    """
    z = np.asarray(z, float)
    taus = np.linspace(0.0, float(l), n)
    P = np.column_stack([taus, np.zeros_like(taus)])
    dD = np.hypot(P[:, 0] - D[0], P[:, 1] - D[1])
    val = dD - r - alpha * np.hypot(P[:, 0] - z[0], P[:, 1] - z[1])
    k = int(np.argmax(val))
    return float(val[k]), float(taus[k])
