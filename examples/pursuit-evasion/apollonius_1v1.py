"""Example: 1v1 interception judgement & Apollonius circle  [book Ch. 1 / 1.1]

Run:  python apollonius_1v1.py
Outputs: out/pursuit_evasion_1.{svg,png}

Reproduces the book's console value: p_p=(3,2), p_e=(-3,0), a=5/3, r=0.4, x_d=3
=> optimal breakthrough point x* ~= (-0.6204, -0.9819) -> interception succeeds.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from gtlib import geometry as G          # noqa: E402
from gtlib import plotting as P          # noqa: E402

# ---------------------------------------------------------------- parameters
P_P = (3.0, 2.0)      # defender
P_E = (-3.0, 0.0)     # attacker
V_P, V_E = 0.5, 0.3   # speeds
R = 0.4               # capture radius
X_D = 3.0             # defence line x = x_d
LIM = 5.0


def run(make_figure=True):
    a = round(V_P / V_E, 5)
    res = G.judge_interception([(P_P, a)], P_E, R, X_D,
                               bounds=(-LIM, LIM, -LIM, LIM))
    out_dir = pathlib.Path(__file__).resolve().parent / "out"

    print(f"a = v_p/v_e = {a}")
    print(f"optimal breakthrough point x* = {np.round(res['x'], 4)}")
    print(f"x1* = {res['x1']:.4f}  vs defence line {X_D}  ->  {res['verdict']}")

    if make_figure:
        P.ieee_style()
        fig, ax = P.new_axes(89, 80)
        xs = np.linspace(-LIM, LIM, 400)
        ys = np.linspace(-LIM, LIM, 400)
        X, Y, Gm = G.safe_set_grid([(P_P, a)], P_E, R, xs, ys)
        ax.contourf(X, Y, Gm, levels=[-1e9, 0.0], colors=[P.C_ATTACKER],
                    alpha=0.12)
        ax.contour(X, Y, Gm, levels=[0.0], colors=[P.C_ACCENT], linewidths=1.2)
        ax.plot(*P_P, "o", color=P.C_DEFENDER, ms=4)
        ax.plot(*P_E, "o", color=P.C_ATTACKER, ms=4)
        ax.plot(res["x"][0], res["x"][1], "*", color=P.C_ACCENT, ms=9)
        ax.annotate("$x^*$", res["x"], textcoords="offset points", xytext=(4, 4))
        P.draw_arena(ax, (-LIM, LIM), (-LIM, LIM), x_d=X_D)
        ax.set_title("1v1 interception judgement")
        outs = P.save_figs(fig, out_dir / "pursuit_evasion_1")
        print("figures:", [str(o) for o in outs])
    return res


if __name__ == "__main__":
    run()
