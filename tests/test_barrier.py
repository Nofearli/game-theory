"""Tests: barriers (book Ch. 3)."""
from __future__ import annotations

import numpy as np

from gtlib import barrier as B

D = (2.0, 1.5)
ALPHA = 2.0
L = 3.0


def test_barrier_joint_continuity():
    """The arc-hyperbola-arc branches must meet continuously at delta1, delta2."""
    pts = B.barrier_1v1_points(D, ALPHA, L, n=400)
    d1 = D[0] / ALPHA ** 2
    d2 = d1 + (1 - 1 / ALPHA ** 2) * L
    y1_cf = np.sqrt(D[1] ** 2 / ALPHA ** 2 + (d1 - D[0]) ** 2 / (ALPHA ** 2 - 1))
    R1 = np.hypot(*D) / ALPHA
    y1_arc = np.sqrt(max(0.0, R1 ** 2 - d1 ** 2))
    assert abs(y1_cf - y1_arc) < 1e-9, (y1_cf, y1_arc)
    # right joint
    R3 = np.hypot(D[0] - L, D[1]) / ALPHA
    y2_arc = np.sqrt(max(0.0, R3 ** 2 - (d2 - L) ** 2))
    y2_cf = np.sqrt(D[1] ** 2 / ALPHA ** 2 + (d2 - D[0]) ** 2 / (ALPHA ** 2 - 1))
    assert abs(y2_cf - y2_arc) < 1e-9, (y2_cf, y2_arc)
    assert len(pts) > 100


def test_barrier_points_are_critical():
    """Every barrier point must have a near-zero criticality residual."""
    pts = B.barrier_1v1_points(D, ALPHA, L, n=200)
    idx = np.linspace(0, len(pts) - 1, 12).astype(int)
    worst = 0.0
    for k in idx:
        resid, _ = B.on_barrier(pts[k], D, ALPHA, 0.0, l=L)
        worst = max(worst, abs(resid))
    assert worst < 1e-5, worst


def test_oval_degenerates_to_closed_form():
    """r -> 0 parametric barrier must equal the closed-form middle branch."""
    for x in np.linspace(0.6, 2.6, 7):
        tau = B.escape_point_map(x, D, ALPHA)
        z = B.cartesian_oval_points(D, ALPHA, 0.0, [tau])
        assert len(z) == 1
        y_cf = np.sqrt(D[1] ** 2 / ALPHA ** 2 + (x - D[0]) ** 2 / (ALPHA ** 2 - 1))
        assert abs(z[0, 0] - x) < 1e-9, (z[0, 0], x)
        assert abs(z[0, 1] - y_cf) < 1e-9, (z[0, 1], y_cf)


def test_oval_radius_shrinks_with_r():
    """For a fixed escape point, larger r moves the barrier point closer to tau."""
    tau = 1.5
    z0 = B.cartesian_oval_points(D, ALPHA, 0.0, [tau])[0]
    z1 = B.cartesian_oval_points(D, ALPHA, 0.3, [tau])[0]
    assert np.hypot(*(z1 - np.array([tau, 0.0]))) < np.hypot(*(z0 - np.array([tau, 0.0])))


def test_2v1_degenerate_falls_back_to_1v1():
    """If xz is outside [0,l] the 2v1 barrier degenerates to the 1v1 one."""
    pts = B.barrier_2v1_points((2.0, 1.5), (2.0, -1.5), ALPHA, L)
    assert len(pts) > 50


def test_bisector_split_equidistant():
    xz = B.bisector_split((0.5, 1.0), (2.5, -0.5), L)
    d1 = np.hypot(xz - 0.5, 0.0 - 1.0)
    d2 = np.hypot(xz - 2.5, 0.0 + 0.5)
    assert abs(d1 - d2) < 1e-9, (d1, d2)
