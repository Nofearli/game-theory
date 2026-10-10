"""Tests: core geometry & closed loop (book Ch. 1)."""
from __future__ import annotations

import numpy as np

from gtlib import geometry as G
from gtlib import simulate as S


def test_breakthrough_matches_book_value():
    """book 1.1 console: p_p=(3,2), p_e=(-3,0), a=5/3, r=0.4 -> x* = (-0.6204,-0.9819)."""
    res = G.judge_interception([((3.0, 2.0), 5.0 / 3.0)], (-3.0, 0.0), 0.4, 3.0)
    assert abs(res["x1"] - (-0.6204)) < 5e-4, res["x1"]
    assert res["intercepted"] is True


def test_breakthrough_on_constraint_boundary():
    """The optimal breakthrough point must be feasible (g <= 0) and tight."""
    a = 5.0 / 3.0
    res = G.solve_breakthrough([((3.0, 2.0), a)], (-3.0, 0.0), 0.4)
    gval = G.apollonius_g(res["x"], (3.0, 2.0), (-3.0, 0.0), a, 0.4)
    assert gval <= 1e-6, gval
    assert abs(gval) < 1e-4, f"constraint should be active, g={gval}"


def test_apollonius_circle_geometry():
    """||x-p_p|| = a||x-p_e|| holds on the circle."""
    a = 2.0
    c, rho = G.apollonius_circle((2.0, 0.0), (-2.0, 0.0), a)
    x = c + np.array([rho, 0.0])
    lhs = G.norm(x - np.array([2.0, 0.0]))
    rhs = a * G.norm(x - np.array([-2.0, 0.0]))
    assert abs(lhs - rhs) < 1e-9, (lhs, rhs)


def test_interception_flip():
    """A defender far away cannot intercept; a close, fast one can."""
    far = G.judge_interception([((3.0, 2.0), 5.0 / 3.0)], (-3.0, 0.0), 0.4, -1.0)
    assert far["intercepted"] is False
    close = G.judge_interception([((0.0, 0.0), 3.0)], (-3.0, 0.0), 0.4, 3.0)
    assert close["intercepted"] is True


def test_closed_loop_optimal_attacker_is_intercepted():
    p = S.GameParams()
    out = S.run_closed_loop([(3.0, 2.0)], (-3.0, 0.0), p)
    assert out["result"]["who"] == "interception", out["result"]


def test_closed_loop_distance_decreases():
    p = S.GameParams()
    out = S.run_closed_loop([(3.0, 2.0)], (-3.0, 0.0), p)
    d = out["dist"]
    assert d[0] > d[-1], (d[0], d[-1])
