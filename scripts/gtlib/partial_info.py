"""Partial-information games (book Ch. 4 / 4.0-4.1)."""
from __future__ import annotations

import numpy as np

from .geometry import norm


def apollonius_center_radius(x_E, x_P, alpha):
    """Centre and radius of the escape-set (Apollonius) circle (book 4.0 Eq. 2)."""
    x_E = np.asarray(x_E, float)
    x_P = np.asarray(x_P, float)
    x_A = (alpha ** 2 * x_E - x_P) / (alpha ** 2 - 1.0)
    R_A = alpha * norm(x_E - x_P) / (alpha ** 2 - 1.0)
    return x_A, float(R_A)


def law_p_optimal_capture(x_E, x_P, x_A, x_A_lock, R_Adelta, alpha, eps=1e-12):
    """Capture law Gamma_P^delta (book 4.0 Eq. 4):

        z_P = (R_Adelta - R_A) d_hat + alpha^-1 y ,  u_P = z_P / ||z_P||
    with d_hat the line-of-sight unit vector and y = x_A - x_A_lock.
    """
    x_E = np.asarray(x_E, float)
    x_P = np.asarray(x_P, float)
    x_A = np.asarray(x_A, float)
    x_A_lock = np.asarray(x_A_lock, float)
    d = x_E - x_P
    d_hat = d / (norm(d) + eps)
    _, R_A = apollonius_center_radius(x_E, x_P, alpha)
    y = x_A - x_A_lock
    z_P = (R_Adelta - R_A) * d_hat + y / alpha
    nz = norm(z_P)
    u_P = z_P / nz if nz > eps else np.zeros(2)
    return u_P, z_P


def R_alpha_required(l, alpha):
    """Minimum sensing radius to cover the whole barrier (book 4.0 Eq. 6)."""
    return (1.0 + 1.0 / alpha) * l / 2.0


def optimal_defensive_point(l, alpha, r):
    """Theorem 2 deployment (book 4.0 Eq. 6): midpoint if r > R_alpha, else below."""
    Ra = R_alpha_required(l, alpha)
    if r > Ra:
        return np.array([l / 2.0, 0.0]), "midpoint"
    return np.array([l / 2.0, -r / (1.0 - 1.0 / alpha)]), "below goal line"


def ambiguity_region(x_P, r, alpha, xs, ys):
    """Ambiguity region F = W_B^P \\ S (attacker-winning but outside the sensing disk).

    Here the barrier is approximated by the 1v1 critical condition against a single
    defender at x_P; `S` is the disk of radius r about x_P.
    Returns (X, Y, F_mask) on the grid.
    """
    X, Y = np.meshgrid(np.asarray(xs, float), np.asarray(ys, float))
    x_P = np.asarray(x_P, float)
    # a point is "winning for the attacker" if it lies outside the defender's reach
    # (a coarse barrier proxy: distance from x_P beyond a multiple of the goal reach)
    win = np.hypot(X - x_P[0], Y - x_P[1]) > (1.0 + 1.0 / alpha)
    seen = np.hypot(X - x_P[0], Y - x_P[1]) <= r
    return X, Y, (win & ~seen)
