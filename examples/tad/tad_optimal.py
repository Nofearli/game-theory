"""Example: TAD three-body game — escape oval, optimal capture point, closed loop
[book Ch. 5 / 5.1]

Run:  python tad_optimal.py
Outputs: out/tad_optimal_1.{svg,png}

PROVENANCE: the book states the TAD results via the paper's Eq. (14)/(15) without
reproducing them.  This example uses the *independent reconstruction* in
`gtlib.tad` (documented there).  Treat the numbers as illustrative, not as the
paper's values.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from gtlib import plotting as P          # noqa: E402
from gtlib import tad as T               # noqa: E402

A0 = (0.0, 0.0)      # attacker
D0 = (-2.0, 0.0)     # defender
T0 = (2.0, 2.0)      # target
GAMMA = 0.8          # v_T / v_A
R = 0.5              # A's capture radius


def simulate_closed_loop(x_A, x_D, x_T, z_star, v=1.0, gamma=GAMMA, r=R, dt=0.05,
                         steps=2000):
    """All three head straight for z*; check whether D intercepts A before A hits T."""
    x_A = np.array(x_A, float); x_D = np.array(x_D, float); x_T = np.array(x_T, float)
    z = np.array(z_star, float)
    t = 0.0
    for _ in range(steps):
        for X, vv in ((x_A, v), (x_D, v), (x_T, gamma * v)):
            d = z - X
            n = np.linalg.norm(d)
            if n > 1e-9:
                X += vv * d / n * dt
        t += dt
        if np.linalg.norm(x_T - x_A) <= r:
            return {"who": "A captures T", "t": t}
        if np.linalg.norm(x_D - x_A) <= 1e-2:
            return {"who": "D intercepts A", "t": t}
    return {"who": "timeout", "t": t}


def run(make_figure=True):
    out_dir = pathlib.Path(__file__).resolve().parent / "out"
    z_star, oval, margin = T.optimal_capture_point(A0, D0, T0, GAMMA, R, n=720)
    winner, _ = T.predict_winner(A0, D0, T0, GAMMA, R)
    resid = T.hji_residual(A0, D0, T0, z_star, GAMMA)
    print(f"z* = {np.round(z_star, 3)}   safety margin = {margin:.3f}")
    print(f"Kind prediction: {winner}")
    print(f"terminal-alignment residual at z* = {resid:.3f} (0 = perfectly aligned)")
    sim = simulate_closed_loop(A0, D0, T0, z_star)
    print(f"closed loop: {sim['who']} at t={sim['t']:.2f}s")

    if make_figure:
        P.ieee_style()
        fig, ax = P.new_axes(89, 80)
        ax.plot(oval[:, 0], oval[:, 1], color=P.C_NEUTRAL, lw=1.2, label="escape oval")
        for pt, c, lbl in ((A0, P.C_ATTACKER, "A"), (D0, P.C_DEFENDER, "D"),
                           (T0, P.C_TARGET, "T")):
            ax.plot(*pt, "o", color=c, ms=5)
            ax.annotate(lbl, pt, textcoords="offset points", xytext=(4, 4))
        ax.plot(*z_star, "*", color=P.C_ACCENT, ms=10)
        ax.annotate("$z^*$", z_star, textcoords="offset points", xytext=(5, 5))
        ax.plot([A0[0], z_star[0]], [A0[1], z_star[1]], ls="--", color=P.C_ATTACKER, lw=0.8)
        ax.plot([D0[0], z_star[0]], [D0[1], z_star[1]], ls="--", color=P.C_DEFENDER, lw=0.8)
        ax.plot([T0[0], z_star[0]], [T0[1], z_star[1]], ls="--", color=P.C_TARGET, lw=0.8)
        ax.set_xlim(-6, 14); ax.set_ylim(-6, 12)
        ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
        ax.set_title("TAD escape oval and optimal capture point")
        ax.legend(frameon=False, fontsize=5, loc="lower right")
        P.save_figs(fig, out_dir / "tad_optimal_1")
        print("figures saved to", out_dir)
    return z_star, winner


if __name__ == "__main__":
    run()
