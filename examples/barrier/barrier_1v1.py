"""Example: 1v1 analytic barrier & Cartesian-oval parameterisation  [book Ch. 3]

Run:  python barrier_1v1.py
Outputs: out/barrier_1v1.{svg,png}

Shows (a) the three-branch closed-form barrier (arc-hyperbola-arc), (b) the
parametric barrier for r > 0 and its exact degeneration to (a) as r -> 0.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from gtlib import barrier as B           # noqa: E402
from gtlib import plotting as P          # noqa: E402

D = (2.0, 1.5)      # defender
ALPHA = 2.0         # v_P / v_E
L = 3.0             # target segment [0, l] on y = 0


def run(make_figure=True):
    out_dir = pathlib.Path(__file__).resolve().parent / "out"
    pts = B.barrier_1v1_points(D, ALPHA, L, n=400)
    print(f"1v1 barrier: {len(pts)} points, x in [{pts[:,0].min():.3f}, {pts[:,0].max():.3f}]")

    # criticality check on a middle point
    mid = pts[len(pts) // 2]
    resid, tau = B.on_barrier(mid, D, ALPHA, 0.0, l=L)
    print(f"on_barrier residual at {np.round(mid,3)} = {resid:.2e} (tau* = {tau:.3f})")

    # r -> 0 degeneration of the parametric form: compare at the SAME escape point
    print("parametric (r=0) vs closed-form, aligned by escape point tau(x):")
    for x in np.linspace(0.5, 2.7, 5):
        tau = B.escape_point_map(x, D, ALPHA)
        z = B.cartesian_oval_points(D, ALPHA, 0.0, [tau])
        if not len(z):
            continue
        y_c = np.sqrt(D[1] ** 2 / ALPHA ** 2 + (x - D[0]) ** 2 / (ALPHA ** 2 - 1))
        print(f"  x={x:.2f} tau={tau:.3f}  z=({z[0,0]:.4f},{z[0,1]:.4f})"
              f"  closed-form y={y_c:.4f}  |dx|={abs(z[0,0]-x):.2e} |dy|={abs(z[0,1]-y_c):.2e}")

    if make_figure:
        P.ieee_style()
        fig, ax = P.new_axes(89, 80)
        ax.plot(pts[:, 0], pts[:, 1], color=P.C_ACCENT, lw=1.3, label="barrier (r=0)")
        for r, c in [(0.2, P.C_DEFENDER), (0.4, P.C_ATTACKER)]:
            ov = B.cartesian_oval_points(D, ALPHA, r, np.linspace(0.1, 2.9, 200))
            if len(ov):
                ax.plot(ov[:, 0], ov[:, 1], color=c, lw=1.0, ls="--",
                        label=f"oval (r={r})")
        ax.plot([0, L], [0, 0], color=P.C_TARGET, lw=2.0, label="target segment")
        ax.plot(*D, "o", color=P.C_DEFENDER, ms=4)
        P.draw_arena(ax, (-0.6, L + 0.6), (-0.6, 3.2))
        ax.set_title("1v1 barrier and capture-radius ovals")
        ax.legend(frameon=False, loc="upper left")
        outs = P.save_figs(fig, out_dir / "barrier_1v1")
        print("figures:", [str(o) for o in outs])
    return pts


if __name__ == "__main__":
    run()
