"""Example: mv1 combination selection + mvn task assignment  [book Ch. 1 / 1.4-1.5]

Run:  python assignment_mvn.py
Outputs: out/assignment_mvn_1.{svg,png}

Builds the pairwise feasibility matrix xcj (can a combo alone stop an attacker?),
solves the 0-1 ILP "stop as many attackers as possible", and prints the assignment.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from gtlib import assignment as A        # noqa: E402
from gtlib import geometry as G          # noqa: E402
from gtlib import plotting as P          # noqa: E402

# 4 defenders (blue, heterogeneous speed ratios), 3 attackers (red)
DEFENDERS = [(3.0, 2.0), (3.0, -2.0), (-1.0, 3.0), (-1.0, -3.0)]
DEFENDER_A = [1.6667, 1.6667, 1.1, 1.6667]   # D3 is only slightly faster than E
ATTACKERS = [((-1.0, 0.0), 1.6667), ((-2.0, 3.0), 1.6667), ((-2.0, -3.0), 1.6667)]
R = 0.4
X_D = 3.0


def run(make_figure=True):
    out_dir = pathlib.Path(__file__).resolve().parent / "out"
    combos = A.make_combos(len(DEFENDERS), sizes=(1, 2))
    xcj, x1 = A.build_xcj(combos, DEFENDERS, ATTACKERS, R, X_D,
                          defender_a=DEFENDER_A, bounds=(-6, 6, -6, 6))
    print(f"combos: {combos}")
    print("xcj (rows=combos, cols=attackers):")
    for c, row in zip(combos, xcj):
        print(f"  {c}: {row.tolist()}")

    # reward = suppression tightness (only where feasible)
    rewards = np.zeros_like(x1)
    for i in range(x1.shape[0]):
        for j in range(x1.shape[1]):
            if xcj[i, j]:
                rewards[i, j] = 1.0 / max(1e-6, X_D - x1[i, j])
    sol = A.solve_assignment(rewards, xcj, combos=combos)
    print(f"ILP success={sol['success']}  objective={sol['objective']:.4f}")
    if sol["x"] is not None:
        for i in range(sol["x"].shape[0]):
            for j in range(sol["x"].shape[1]):
                if sol["x"][i, j]:
                    print(f"  assign defenders {combos[i]} -> attacker {j}")

    # mv1: minimum headcount to stop attacker 0
    mv1 = []
    for j in range(len(ATTACKERS)):
        single_ok = any(xcj[i, j] for i, c in enumerate(combos) if len(c) == 1)
        pair_ok = any(xcj[i, j] for i, c in enumerate(combos) if len(c) == 2)
        mv1.append(("1" if single_ok else ("2" if pair_ok else "-")))
    print(f"mv1 minimum headcount per attacker: {mv1}")

    if make_figure:
        P.ieee_style()
        fig, ax = P.new_axes(110, 80)
        for k, (px, py) in enumerate(DEFENDERS):
            ax.plot(px, py, "o", color=P.C_DEFENDER, ms=5)
            ax.annotate(f"$D_{k+1}$", (px, py), textcoords="offset points",
                        xytext=(3, 3), fontsize=6)
        for j, (pe, _) in enumerate(ATTACKERS):
            ax.plot(pe[0], pe[1], "o", color=P.C_ATTACKER, ms=5)
            ax.annotate(f"$E_{j+1}$", pe, textcoords="offset points",
                        xytext=(3, 3), fontsize=6)
        if sol["x"] is not None:
            for i in range(sol["x"].shape[0]):
                for j in range(sol["x"].shape[1]):
                    if sol["x"][i, j]:
                        for k in combos[i]:
                            ax.annotate("", xy=ATTACKERS[j][0], xytext=DEFENDERS[k],
                                        arrowprops=dict(arrowstyle="->",
                                                        color=P.C_ACCENT, lw=0.8))
        P.draw_arena(ax, (-6, 6), (-6, 6), x_d=X_D)
        ax.set_title("mvn assignment (green = assigned)")
        P.save_figs(fig, out_dir / "assignment_mvn_1")
        print("figures saved to", out_dir)
    return xcj, sol


if __name__ == "__main__":
    run()
