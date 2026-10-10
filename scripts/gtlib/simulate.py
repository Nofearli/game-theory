"""Generic closed-loop simulation framework (book Ch. 1 / 1.3).

Layers are separated: dynamics (step_toward), strategy (callables), optimiser
(solve_breakthrough), termination (predicates).  Plotting is NOT imported here.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .geometry import solve_breakthrough


@dataclass
class GameParams:
    """All tunable parameters in one place (see references/coding/coding-conventions.md)."""
    v_p: float = 0.5
    v_e: float = 0.3
    r: float = 0.4
    x_d: float = 3.0
    x_max: float = 5.0
    y_max: float = 5.0
    dt: float = 0.1
    t_max: float = 200.0
    seed: int = 0

    def __post_init__(self):
        if not (self.v_p > 0 and self.v_e > 0):
            raise ValueError("speeds must be positive")
        if self.dt <= 0:
            raise ValueError("dt must be positive")
        if self.r < 0:
            raise ValueError("capture radius must be non-negative")

    @property
    def a(self):
        return self.v_p / self.v_e


def step_toward(pos, target, speed, dt):
    """One full-speed step toward `target`; returns (new_pos, control_vector)."""
    d = np.asarray(target, float) - np.asarray(pos, float)
    n = float(np.linalg.norm(d))
    if n < 1e-12:
        return np.asarray(pos, float).copy(), np.zeros(2)
    u = speed * d / n
    return np.asarray(pos, float) + u * dt, u


def policy_straight(p, target, params):
    return np.array([params.v_e, 0.0])


def policy_optimal(p, target, params):
    d = np.asarray(target, float) - np.asarray(p, float)
    n = float(np.linalg.norm(d))
    return params.v_e * d / n if n > 1e-12 else np.zeros(2)


def policy_sinusoidal(p, target, params, amplitude=1.0, period=2.0):
    """A manoeuvring attacker: drift right while oscillating in y."""
    return np.array([params.v_e * 0.8,
                     params.v_e * amplitude * np.sin(2 * np.pi * p[0] / period)])


def run_closed_loop(pursuers, p_e, params: GameParams, evader_policy=policy_optimal):
    """Receding-horizon 1v1/mv1 closed loop.

    pursuers : list of initial defender positions (all share params.v_p/v_e ratio)
    evader_policy : callable(p_e, target, params) -> velocity (magnitude <= v_e)

    Returns dict(t, P (list of arrays), E (array), dist (array), result).
    """
    P = [np.asarray(p, float).copy() for p in pursuers]
    E = np.asarray(p_e, float).copy()
    t = 0.0
    P_hist = [[p.copy() for p in P]]
    E_hist = [E.copy()]
    dist_hist = []
    t_hist = [0.0]
    result = {"who": "timeout", "t": params.t_max}

    n_steps = int(params.t_max / params.dt)
    for _ in range(n_steps):
        pursuer_cfg = [(p, params.a) for p in P]
        bt = solve_breakthrough(pursuer_cfg, E, params.r,
                                bounds=(-params.x_max, params.x_max,
                                        -params.y_max, params.y_max))
        target = bt["x"]
        # defenders step toward the breakthrough point
        newP = []
        for p in P:
            np_, _ = step_toward(p, target, params.v_p, params.dt)
            newP.append(np_)
        # attacker moves per its policy
        ue = evader_policy(E, target, params)
        nrm = float(np.linalg.norm(ue))
        if nrm > params.v_e:
            ue = ue * (params.v_e / nrm)
        E = E + ue * params.dt
        P = newP
        t += params.dt
        P_hist.append([p.copy() for p in P])
        E_hist.append(E.copy())
        d = min(float(np.linalg.norm(p - E)) for p in P)
        dist_hist.append(d)
        t_hist.append(t)
        if d <= params.r:
            result = {"who": "interception", "t": t}
            break
        if E[0] >= params.x_d:
            result = {"who": "breakthrough", "t": t}
            break

    return {"t": np.array(t_hist), "P": np.array(P_hist), "E": np.array(E_hist),
            "dist": np.array(dist_hist), "result": result, "params": params}
