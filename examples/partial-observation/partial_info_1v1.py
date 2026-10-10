"""Example: partial-information 1v1 — deployment, detection, capture  [book Ch. 4]

Run:  python partial_info_1v1.py
Outputs: out/partial_info_1.{svg,png}, out/partial_info_2.{svg,png}

Shows (a) the optimal deployment point vs sensing radius r (Theorem 2) and
(b) a scenario where the defender waits at the deployment point until the
attacker enters the sensing disk, then switches to the capture law Gamma_P^delta.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from gtlib import partial_info as PI     # noqa: E402
from gtlib import plotting as P          # noqa: E402

L = 3.0          # target segment length
ALPHA = 3.0      # v_P / v_E
DT = 0.05


def deployment_curve(r_values):
    xs, ys, kinds = [], [], []
    for r in r_values:
        p, kind = PI.optimal_defensive_point(L, ALPHA, r)
        xs.append(p[0]); ys.append(p[1]); kinds.append(kind)
    return np.array(xs), np.array(ys), kinds


def simulate(r_sense=1.2, x_P=None, p_e0=None, v_e=0.2, steps=4000):
    """Deployment -> detection -> capture simulation.

    Local frame (book Ch. 4): goal segment on y = 0 from (0,0) to (l,0); the
    attacker approaches from below (y < 0) and runs straight up (+y) for the gate.
    """
    alpha = ALPHA
    v_p = alpha * v_e
    if x_P is None:
        x_P, _ = PI.optimal_defensive_point(L, ALPHA, r_sense)
    x_P = np.asarray(x_P, float)
    if p_e0 is None:
        p_e0 = (x_P[0], -4.0)
    x_E = np.asarray(p_e0, float)
    t = 0.0
    det = None
    lock = None
    P_hist, E_hist = [x_P.copy()], [x_E.copy()]
    for _ in range(steps):
        d = np.linalg.norm(x_E - x_P)
        if det is None and d <= r_sense:
            det = t
            x_A, R_A = PI.apollonius_center_radius(x_E, x_P, alpha)
            lock = (x_A.copy(), R_A + 0.5 * d)     # R_Adelta
        if det is None:
            u_P = np.zeros(2)                       # wait at the deployment point
        else:
            x_A, R_A = PI.apollonius_center_radius(x_E, x_P, alpha)
            u_P, _ = PI.law_p_optimal_capture(x_E, x_P, x_A, lock[0], lock[1], alpha)
            u_P = u_P * v_p
        x_E = x_E + np.array([0.0, v_e]) * DT        # attacker runs straight for the gate
        x_P = x_P + u_P * DT
        t += DT
        P_hist.append(x_P.copy()); E_hist.append(x_E.copy())
        if np.linalg.norm(x_E - x_P) <= 0.05:
            return {"result": "captured", "t": t, "t_detect": det,
                    "P": np.array(P_hist), "E": np.array(E_hist)}
        if x_E[1] >= 0.0:
            return {"result": "escaped", "t": t, "t_detect": det,
                    "P": np.array(P_hist), "E": np.array(E_hist)}
    return {"result": "timeout", "t": t, "t_detect": det,
            "P": np.array(P_hist), "E": np.array(E_hist)}


def run(make_figure=True):
    out_dir = pathlib.Path(__file__).resolve().parent / "out"
    r_vals = np.linspace(0.2, 3.0, 60)
    xs, ys, kinds = deployment_curve(r_vals)
    R_alpha = PI.R_alpha_required(L, ALPHA)
    print(f"R_alpha = (1+1/alpha) l/2 = {R_alpha:.3f}")
    print(f"for r > R_alpha: midpoint;  for r <= R_alpha: {ys.min():.3f} below goal line")

    sim = simulate(r_sense=1.2)
    print(f"simulation: result={sim['result']} at t={sim['t']:.2f}s "
          f"(detection at t={sim['t_detect']})")

    if make_figure:
        P.ieee_style()
        fig, ax = P.new_axes(89, 70)
        ax.plot(r_vals, ys, color=P.C_DEFENDER, label="$y_{opt}$")
        ax.axvline(R_alpha, color=P.C_NEUTRAL, ls="--", lw=0.8)
        ax.text(R_alpha, ys.min() * 0.5, "$R_\\alpha$", fontsize=6)
        ax.set_xlabel("sensing radius $r$ (m)")
        ax.set_ylabel("deployment $y$ (m)")
        ax.set_title("Optimal deployment vs sensing radius")
        ax.legend(frameon=False)
        P.save_figs(fig, out_dir / "partial_info_1")

        fig2, ax2 = P.new_axes(89, 80)
        x_P, _ = PI.optimal_defensive_point(L, ALPHA, 1.2)
        th = np.linspace(0, 2 * np.pi, 200)
        ax2.plot(x_P[0] + 1.2 * np.cos(th), x_P[1] + 1.2 * np.sin(th),
                 color=P.C_NEUTRAL, lw=0.7, ls=":", label="sensing disk")
        ax2.plot(sim["P"][:, 0], sim["P"][:, 1], color=P.C_DEFENDER, label="Defender")
        ax2.plot(sim["E"][:, 0], sim["E"][:, 1], color=P.C_ATTACKER, label="Attacker")
        ax2.plot([0, L], [0, 0], color=P.C_TARGET, lw=2.5, label="target segment")
        P.draw_arena(ax2, (-1.0, L + 1.0), (-4.5, 1.5))
        ax2.set_title("Deployment -> detection -> capture")
        ax2.legend(frameon=False, fontsize=5)
        P.save_figs(fig2, out_dir / "partial_info_2")
        print("figures saved to", out_dir)
    return sim


if __name__ == "__main__":
    run()
