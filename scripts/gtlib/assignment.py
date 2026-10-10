"""Task assignment (book Ch. 1 / 1.5, Ch. 2 / 2.2, Ch. 6 / 6.2)."""
from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import LinearConstraint, Bounds, milp, linear_sum_assignment

from .geometry import judge_interception


def make_combos(n_defenders, sizes=(1, 2)):
    """All defender combinations of the given sizes (0-based indices)."""
    out = []
    for s in sizes:
        out.extend(itertools.combinations(range(n_defenders), s))
    return out


def build_xcj(combos, defenders, attackers, r, x_d, defender_a=None, **kw):
    """Feasibility matrix xcj[i, j] = 1 iff combo i alone intercepts attacker j.

    defender_a : optional per-defender speed ratio a = v_p/v_e (heterogeneous
                 defenders).  If None, the attacker's own `a` is used for all.
    """
    xcj = np.zeros((len(combos), len(attackers)), dtype=int)
    x1 = np.full_like(xcj, np.nan, dtype=float)
    for i, combo in enumerate(combos):
        for j, (pe, a) in enumerate(attackers):
            pp = []
            for k in combo:
                ak = a if defender_a is None else defender_a[k]
                pp.append((defenders[k], ak))
            res = judge_interception(pp, pe, r, x_d, **kw)
            xcj[i, j] = 1 if res["intercepted"] else 0
            x1[i, j] = res["x1"]
    return xcj, x1


def solve_assignment(rewards, xcj, combos=None):
    """0-1 ILP: max sum rewards*x s.t. row/col <= 1, x <= xcj, shared-defender
    exclusion.  Returns dict(x (matrix), objective, success, message)."""
    rewards = np.asarray(rewards, float)
    xcj = np.asarray(xcj, float)
    R, C = rewards.shape
    n = R * C

    def idx(i, j):
        return i * C + j

    c = -rewards.ravel()                      # milp minimises
    lb, ub, rows = [], [], []

    def add(row):
        rows.append(row)

    # x <= xcj
    for i in range(R):
        for j in range(C):
            row = np.zeros(n)
            row[idx(i, j)] = 1.0
            add(row)
            lb.append(-np.inf)
            ub.append(xcj[i, j])
    # sum_j x_ij <= 1
    for i in range(R):
        row = np.zeros(n)
        for j in range(C):
            row[idx(i, j)] = 1.0
        add(row)
        lb.append(-np.inf)
        ub.append(1.0)
    # sum_i x_ij <= 1
    for j in range(C):
        row = np.zeros(n)
        for i in range(R):
            row[idx(i, j)] = 1.0
        add(row)
        lb.append(-np.inf)
        ub.append(1.0)
    # shared-defender exclusion
    if combos is not None:
        for i, i2 in itertools.combinations(range(R), 2):
            if set(combos[i]) & set(combos[i2]):
                row = np.zeros(n)
                for j in range(C):
                    row[idx(i, j)] = 1.0
                    row[idx(i2, j)] = 1.0
                add(row)
                lb.append(-np.inf)
                ub.append(1.0)

    A = np.array(rows)
    constraints = LinearConstraint(A, np.array(lb), np.array(ub))
    res = milp(c=c, constraints=constraints, integrality=np.ones(n),
               bounds=Bounds(0, 1))
    x = np.round(res.x).astype(int).reshape(R, C) if res.x is not None else None
    obj = float(np.sum(rewards * x)) if x is not None else float("nan")
    return {"x": x, "objective": obj, "success": bool(res.success),
            "message": str(res.message)}


def max_weight_matching(weights):
    """Maximum-weight bipartite matching (Hungarian). Returns (rows, cols, total).

    Use `-inf`/large-negative to forbid an edge; the returned total is the sum of
    the selected weights.
    """
    w = np.asarray(weights, float)
    r, c = linear_sum_assignment(-w)
    return r, c, float(w[r, c].sum())
