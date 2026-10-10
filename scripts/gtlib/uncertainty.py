"""Parameter uncertainty (book Ch. 2 / 2.0-2.2)."""
from __future__ import annotations

import numpy as np

from .geometry import apollonius_g, solve_breakthrough


def kesai_ij(d, r, a, k=3.0):
    """Distance-dependent uncertainty radius (book 2.0 Eq. 2).

        xi = (1/k) * min( d - r ,  min(a-1,1)/a * d + r/a )

    Smaller k => larger xi => coarser observation.  xi -> 0 as d -> r.
    """
    d = np.asarray(d, float)
    r = float(r)
    a = float(a)
    branch1 = d - r
    branch2 = min(a - 1.0, 1.0) / a * d + r / a
    return np.maximum(0.0, np.minimum(branch1, branch2) / float(k))


def effective_radius(r, a, xi):
    """r_eff = r - a * xi  (may be negative under large uncertainty)."""
    return float(r) - float(a) * np.asarray(xi, float)


def conservative_boundary_r_eff(r, a, d, k=3.0):
    """Convenience: r_eff from distance d via the kesai_ij model."""
    return effective_radius(r, a, kesai_ij(d, r, a, k))


def monte_carlo_judgement(pursuers, p_e, r, x_d, xi, n=500, seed=0, **kw):
    """Robust interception probability: perturb positions inside the uncertainty
    disks (radius xi) and count the fraction judged 'interception succeeds'.

    `xi` may be a scalar or an array of per-agent radii (pursuers..., attacker last).
    Returns dict(p_success, n, x1_mean, x1_std, x1_values).
    """
    rng = np.random.default_rng(seed)
    pursuers = [(np.asarray(p, float), float(a)) for p, a in pursuers]
    p_e = np.asarray(p_e, float)
    m = len(pursuers)
    xi = np.broadcast_to(np.asarray(xi, float), (m + 1,)).astype(float)

    def perturb(v, rad):
        if rad <= 0:
            return v
        ang = rng.uniform(0, 2 * np.pi)
        rad_ = rad * np.sqrt(rng.uniform(0, 1))
        return v + rad_ * np.array([np.cos(ang), np.sin(ang)])

    x1 = np.empty(n)
    for i in range(n):
        pp = [(perturb(p, xi[j]), a) for j, (p, a) in enumerate(pursuers)]
        pe = perturb(p_e, xi[m])
        out = solve_breakthrough(pp, pe, r, **kw)
        x1[i] = out["x1"]
    ok = x1 < x_d
    return {"p_success": float(np.mean(ok)), "n": int(n),
            "x1_mean": float(np.mean(x1)), "x1_std": float(np.std(x1)),
            "x1_values": x1}


def robust_feasibility(pursuers, p_e, r, x_d, xi, n=200, seed=0, need_all=True):
    """Robust pairwise feasibility flag (book 2.0 Sec. 5): 1 iff the pair still
    intercepts after perturbation.  `need_all=True` requires all n draws to succeed."""
    out = monte_carlo_judgement(pursuers, p_e, r, x_d, xi, n=n, seed=seed)
    p = out["p_success"]
    return 1 if (p >= 1.0 - 1e-12 if need_all else p >= 0.5) else 0


def reward_suppression(x1_star, x_e_x):
    """Assignment reward = 1 / (x1* - x_e_x)  (tighter suppression => larger)."""
    denom = float(x1_star) - float(x_e_x)
    if denom <= 1e-9:
        return 1e6
    return 1.0 / denom
