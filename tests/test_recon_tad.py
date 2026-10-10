"""Tests: partial information, TAD, reconnaissance-return (book Ch. 4-6)."""
from __future__ import annotations

import numpy as np

from gtlib import partial_info as PI
from gtlib import recon as RC
from gtlib import tad as T


# ---------------------------------------------------------------- Ch. 4
def test_R_alpha_formula():
    assert abs(PI.R_alpha_required(3.0, 3.0) - 2.0) < 1e-12


def test_deployment_switches_at_R_alpha():
    p_big, kind_big = PI.optimal_defensive_point(3.0, 3.0, 2.5)   # r > R_alpha=2
    p_small, kind_small = PI.optimal_defensive_point(3.0, 3.0, 1.0)
    assert p_big[1] == 0.0 and kind_big == "midpoint"
    assert p_small[1] < 0.0


def test_apollonius_center_outside_pair():
    """The escape-set centre lies outside the segment joining the two players."""
    x_A, R_A = PI.apollonius_center_radius((0.0, 0.0), (1.0, 0.0), 3.0)
    assert x_A[0] < 0.0 and R_A > 0


def test_capture_law_is_unit():
    u, z = PI.law_p_optimal_capture((0.0, 0.0), (1.0, 0.0), (-0.5, 0.0),
                                    (-0.5, 0.0), 1.0, 3.0)
    assert abs(np.linalg.norm(u) - 1.0) < 1e-9


# ---------------------------------------------------------------- Ch. 5
def test_tad_zstar_on_oval():
    z, oval, margin = T.optimal_capture_point((0.0, 0.0), (-2.0, 0.0), (2.0, 2.0),
                                              0.8, 0.5, n=720)
    x_A = np.array([0.0, 0.0]); x_T = np.array([2.0, 2.0])
    lhs = np.linalg.norm(z - x_A)
    rhs = np.linalg.norm(z - x_T) / 0.8 + 0.5
    assert abs(lhs - rhs) < 1e-9, (lhs, rhs)


def test_tad_margin_sign_matches_prediction():
    z, oval, margin = T.optimal_capture_point((0.0, 0.0), (-2.0, 0.0), (2.0, 2.0),
                                              0.8, 0.5, n=720)
    winner, _ = T.predict_winner((0.0, 0.0), (-2.0, 0.0), (2.0, 2.0), 0.8, 0.5)
    assert (winner == "A") == (margin > 0)


# ---------------------------------------------------------------- Ch. 6
def test_virtual_evader_transform():
    v = RC.virtual_evader(2.0, 3.0, l=3.0, sigma=1.0, v_E=0.5, tau=2.0)
    assert abs(v[0] - 4.0) < 1e-12 and abs(v[1] - 4.0) < 1e-12


def test_recon_case_A_pursuer_wins():
    m, _ = RC.success_margin((2.05, 2.80), (1.5, 0.0), 3.0, 1.2, 0.5, tau=0.0)
    assert m < 0, m


def test_recon_case_B_evader_wins():
    m, _ = RC.success_margin((2.05, 3.30), (1.5, 0.0), 3.0, 1.2, 0.5, tau=0.0)
    assert m > 0, m


def test_dwell_time_shrinks_margin():
    z = (2.05, 3.30)
    m0, _ = RC.success_margin(z, (1.5, 0.0), 3.0, 1.2, 0.5, tau=0.0)
    m1, _ = RC.success_margin(z, (1.5, 0.0), 3.0, 1.2, 0.5, tau=1.0)
    assert m1 < m0, (m0, m1)


def test_max_dwell_time_zero_when_losing():
    assert RC.max_dwell_time((2.05, 2.80), (1.5, 0.0), 3.0, 1.2, 0.5) == 0.0
