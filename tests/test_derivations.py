"""Tests: claims made in references/derivations/*.

These verify the *derivations*, not just the library: reflection lemma, joining-arc
radius equality, similar-points collinearity, and branch continuity.
"""
from __future__ import annotations

import numpy as np

from gtlib import barrier as B
from gtlib import recon as RC


def test_reflection_lemma_two_leg_equals_reflected_straight():
    """min over boundary points of (||A-x_I|| + ||x_I-G||) == ||A_reflected - G||."""
    l = 3.0
    A = np.array([0.8, 1.3])
    G = np.array([0.0, -2.0])
    A_ref = np.array([2 * l - A[0], A[1]])
    best = np.inf
    for y_I in np.linspace(-10, 10, 20001):
        x_I = np.array([l, y_I])
        best = min(best, np.linalg.norm(A - x_I) + np.linalg.norm(x_I - G))
    straight = np.linalg.norm(A_ref - G)
    assert abs(best - straight) < 1e-3, (best, straight)


def test_reflection_optimal_boundary_point_is_collinear():
    """The optimal x_I must lie on the segment A_ref -> G."""
    l = 3.0
    A = np.array([0.8, 1.3])
    G = np.array([0.0, -2.0])
    A_ref = np.array([2 * l - A[0], A[1]])
    t = (l - A_ref[0]) / (G[0] - A_ref[0])          # param where x = l
    x_I = A_ref + t * (G - A_ref)
    assert abs(x_I[0] - l) < 1e-9
    # collinear => cross product ~ 0
    # NB: use an explicit 2-D cross; np.cross dropped 2-D support in NumPy 2.
    u, v = G - A_ref, x_I - A_ref
    cross = u[0] * v[1] - u[1] * v[0]
    assert abs(cross) < 1e-9, cross


def test_2v1_joining_arc_radius_equality():
    """||xz - D1|| == ||xz - D2|| makes the joining radii match automatically."""
    D1, D2, l = (1.0, 1.5), (2.0, -1.0), 3.0
    xz = B.bisector_split(D1, D2, l)
    r1 = np.linalg.norm(np.array([xz, 0.0]) - np.array(D1))
    r2 = np.linalg.norm(np.array([xz, 0.0]) - np.array(D2))
    assert abs(r1 - r2) < 1e-9, (r1, r2)


def test_similar_points_collinear_in_r():
    """For fixed tau, barrier points for different r lie on one ray through tau."""
    D, alpha, tau = (2.0, 1.5), 2.0, 1.6
    pts = [B.cartesian_oval_points(D, alpha, r, [tau])[0] for r in (0.0, 0.2, 0.4)]
    p = np.array([tau, 0.0])
    v = [q - p for q in pts]
    # all direction vectors must be parallel
    for a, b in ((v[0], v[1]), (v[1], v[2])):
        cross = a[0] * b[1] - a[1] * b[0]
        assert abs(cross) < 1e-9, cross
    # and the radii shrink with r
    rad = [np.linalg.norm(q - p) for q in pts]
    assert rad[0] > rad[1] > rad[2], rad


def test_virtual_evader_reduces_three_stage_to_one_leg():
    """Total three-stage path length equals the reflected straight distance."""
    l, sigma, v_E, tau = 3.0, 1.0, 0.5, 1.2
    x_E, y_E = 1.2, 1.0
    G = np.array([0.0, 0.7])
    xt = RC.virtual_evader(x_E, y_E, l, sigma, v_E, tau)
    # enumerate over the boundary entry/exit points respecting the dwell shift
    best = np.inf
    for y_I in np.linspace(-8, 8, 8001):
        entry = np.array([l, y_I])
        exit_ = np.array([l, y_I + sigma * v_E * tau])
        total = (np.linalg.norm(np.array([x_E, y_E]) - entry)
                 + v_E * tau + np.linalg.norm(exit_ - G)) / v_E
        best = min(best, total)
    straight = (np.linalg.norm(xt - G) + v_E * tau) / v_E
    assert abs(best - straight) < 2e-3, (best, straight)
