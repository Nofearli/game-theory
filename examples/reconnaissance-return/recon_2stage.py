"""Example: reconnaissance-return — 2-stage barrier, dwell time  [book Ch. 6]

Run:  python recon_2stage.py
Outputs: out/recon_2stage_1.{svg,png}

PROVENANCE: the book gives closed-form dome/wedge barriers by reference to the
source papers.  This example uses the *independent numerical model* in
`gtlib.recon` (documented there): the barrier is the zero level set of the
evader's success margin.  Numbers are illustrative, not the paper's.

Convention (book Ch. 6.3-6.5): goal line x = 0, reconnaissance boundary x = l.
"""
from __future__ import annotations

import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from gtlib import plotting as P          # noqa: E402
from gtlib import recon as RC            # noqa: E402

L = 3.0
ALPHA = 1.2          # v_P / v_E
R_C = 0.5
X_P = (1.5, 0.0)
CASE_A = (2.05, 2.80)   # book: inside W_P (pursuer wins)
CASE_B = (2.05, 3.30)   # book: inside W_E (evader wins)


def run(make_figure=True, grid=28):
    out_dir = pathlib.Path(__file__).resolve().parent / "out"
    for name, z in (("Case A", CASE_A), ("Case B", CASE_B)):
        m0, args = RC.success_margin(z, X_P, L, ALPHA, R_C, tau=0.0)
        tmax = RC.max_dwell_time(z, X_P, L, ALPHA, R_C)
        verdict = "W_E (evader)" if m0 > 0 else "W_P (pursuer)"
        print(f"{name} {z}: margin(tau=0)={m0:+.3f} -> {verdict};  "
              f"tau_max={tmax:.3f}s")

    print(f"virtual evader of Case B at tau=1: "
          f"{np.round(RC.virtual_evader(*CASE_B, L, 1, 0.5, 1.0), 3)}")

    if make_figure:
        t0 = time.time()
        X, Y, M0 = RC.barrier_contour(X_P, L, ALPHA, R_C, tau=0.0,
                                      nx=grid, ny=grid, y_span=(-2.0, 6.0))
        X3, Y3, M3 = RC.barrier_contour(X_P, L, ALPHA, R_C, tau=1.0,
                                        nx=grid, ny=grid, y_span=(-2.0, 6.0))
        print(f"barrier grids computed in {time.time()-t0:.1f}s")

        P.ieee_style()
        fig, ax = P.new_axes(89, 80)
        ax.contourf(X, Y, M0, levels=[0, 1e9], colors=[P.C_ATTACKER], alpha=0.10)
        ax.contour(X, Y, M0, levels=[0.0], colors=[P.C_ACCENT], linewidths=1.3)
        ax.contour(X3, Y3, M3, levels=[0.0], colors=[P.C_ACCENT],
                   linewidths=1.0, linestyles="--")
        ax.plot([0, 0], [-2, 6], color=P.C_NEUTRAL, lw=1.0)
        ax.plot([L, L], [-2, 6], color=P.C_NEUTRAL, lw=1.0, ls=":")
        ax.plot(*X_P, "o", color=P.C_DEFENDER, ms=5)
        ax.plot(*CASE_A, "s", color=P.C_DEFENDER, ms=4)
        ax.plot(*CASE_B, "s", color=P.C_ATTACKER, ms=4)
        ax.annotate("A", CASE_A, textcoords="offset points", xytext=(4, -6))
        ax.annotate("B", CASE_B, textcoords="offset points", xytext=(4, 4))
        ax.set_xlim(-0.2, L + 0.2); ax.set_ylim(-2, 6)
        ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
        ax.set_title("2-stage recon barrier (solid $\\tau$=0, dashed $\\tau$=1)")
        P.save_figs(fig, out_dir / "recon_2stage_1")
        print("figures saved to", out_dir)
    return {"A": RC.success_margin(CASE_A, X_P, L, ALPHA, R_C)[0],
            "B": RC.success_margin(CASE_B, X_P, L, ALPHA, R_C)[0]}


if __name__ == "__main__":
    run()
