"""Tests: uncertainty, filtering, assignment (book Ch. 2)."""
from __future__ import annotations

import itertools

import numpy as np

from gtlib import assignment as A
from gtlib import filters as F
from gtlib import uncertainty as U


def test_kesai_zero_at_contact():
    assert abs(float(U.kesai_ij(0.4, 0.4, 1.6667))) < 1e-12


def test_kesai_increases_with_distance():
    vals = [float(U.kesai_ij(d, 0.4, 1.6667)) for d in (1.0, 2.0, 4.0)]
    assert vals[0] <= vals[1] <= vals[2], vals


def test_kesai_shrinks_with_smaller_speed_advantage():
    """a -> 1 must make the model demand a more accurate estimate."""
    v_small = float(U.kesai_ij(3.0, 0.4, 1.05))
    v_large = float(U.kesai_ij(3.0, 0.4, 5.0))
    assert v_small <= v_large + 1e-12, (v_small, v_large)


def test_effective_radius_can_go_negative():
    assert U.effective_radius(0.4, 3.0, 0.5) < 0


def test_monte_carlo_zero_uncertainty_is_deterministic():
    out = U.monte_carlo_judgement([((3.0, 2.0), 5.0 / 3.0)], (-3.0, 0.0), 0.4, 3.0,
                                  0.0, n=20, seed=0)
    assert out["p_success"] in (0.0, 1.0)


def test_kalman_filter_reduces_error():
    rng = np.random.default_rng(0)
    kf = F.constant_velocity_filter(dt=0.1, q_acc=0.05, r_meas=0.5,
                                    x0=-3.0, y0=0.0, vx0=0.3, vy0=0.0)
    err_raw, err_filt = [], []
    true = np.array([-3.0, 0.0])
    for _ in range(120):
        true = true + np.array([0.03, 0.0])
        z = true + rng.normal(0, np.sqrt(0.5), 2)
        kf.predict()
        est = kf.update(z)
        err_raw.append(np.linalg.norm(z - true))
        err_filt.append(np.linalg.norm(est[:2] - true))
    assert np.mean(err_filt) < np.mean(err_raw), (np.mean(err_filt), np.mean(err_raw))


def test_assignment_ilp_matches_brute_force():
    """On a small instance the ILP optimum must equal the brute-force optimum."""
    rewards = np.array([[3.0, 1.0], [1.0, 2.0]])
    xcj = np.ones_like(rewards)
    combos = [(0,), (1,)]
    sol = A.solve_assignment(rewards, xcj, combos=combos)
    # brute force over 0-1 matrices with row/col <= 1 and shared-defender exclusion
    best = 0.0
    for mask in itertools.product([0, 1], repeat=4):
        m = np.array(mask).reshape(2, 2)
        if m.sum(1).max() > 1 or m.sum(0).max() > 1:
            continue
        # combos (0,) and (1,) do not share a defender -> no extra exclusion
        best = max(best, float(np.sum(rewards * m)))
    assert abs(sol["objective"] - best) < 1e-6, (sol["objective"], best)


def test_assignment_respects_shared_defender():
    """Two combos sharing a defender cannot both be selected."""
    rewards = np.array([[5.0, 5.0], [5.0, 5.0]])
    xcj = np.ones_like(rewards)
    combos = [(0, 1), (0, 2)]      # share defender 0
    sol = A.solve_assignment(rewards, xcj, combos=combos)
    assert sol["x"].sum() <= 1, sol["x"]


def test_matching_optimal_small():
    w = np.array([[4.0, 1.0], [2.0, 3.0]])
    r, c, tot = A.max_weight_matching(w)
    assert abs(tot - 7.0) < 1e-9, tot
