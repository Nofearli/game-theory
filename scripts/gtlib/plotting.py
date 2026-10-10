"""IEEE-style plotting helpers (see references/simulation/plotting-standards.md)."""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")  # headless-safe; override before import if interactive needed
import matplotlib.pyplot as plt
import numpy as np

C_DEFENDER = "#2166AC"
C_ATTACKER = "#B2182B"
C_ACCENT = "#1B7837"
C_TARGET = "#F1A340"
C_EXTRA = "#762A83"
C_NEUTRAL = "#666666"
PALETTE = [C_DEFENDER, C_ATTACKER, C_ACCENT, C_TARGET, C_EXTRA, C_NEUTRAL]


def ieee_style():
    """Apply the journal rcParams (serif fonts, thin spines, no frame legend)."""
    matplotlib.rcParams.update({
        "font.family": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "svg.fonttype": "none",
        "font.size": 7,
        "axes.labelsize": 7,
        "axes.titlesize": 8,
        "legend.fontsize": 6,
        "axes.linewidth": 0.6,
        "lines.linewidth": 1.2,
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 120,
        "savefig.bbox": "tight",
    })


def save_figs(fig, path, svg=True, png=True, dpi=300):
    """Save a figure as editable SVG + 300 dpi PNG; creates parent dirs."""
    path = str(path)
    if path.lower().endswith((".svg", ".png")):
        path = os.path.splitext(path)[0]
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    outs = []
    if svg:
        f = path + ".svg"
        fig.savefig(f)
        outs.append(f)
    if png:
        f = path + ".png"
        fig.savefig(f, dpi=dpi)
        outs.append(f)
    return outs


def new_axes(width_mm=89.0, height_mm=75.0, equal=True):
    """Create a figure sized in millimetres (single 89 / double 183 column)."""
    fig, ax = plt.subplots(figsize=(width_mm / 25.4, height_mm / 25.4))
    if equal:
        ax.set_aspect("equal", adjustable="box")
    return fig, ax


def draw_arena(ax, x_lim, y_lim, x_d=None):
    """Draw the arena box and an optional vertical defence line."""
    ax.set_xlim(*x_lim)
    ax.set_ylim(*y_lim)
    if x_d is not None:
        ax.axvline(x_d, color=C_NEUTRAL, lw=0.8, ls="--")
    ax.set_xlabel("$x$ (m)")
    ax.set_ylabel("$y$ (m)")


def plot_trajectories(ax, defender_xy, attacker_xy, capture=None, goal=None):
    """Standard trajectory plot: defender blue, attacker red."""
    defender_xy = np.asarray(defender_xy)
    attacker_xy = np.asarray(attacker_xy)
    ax.plot(defender_xy[:, 0], defender_xy[:, 1], color=C_DEFENDER, label="Defender")
    ax.plot(attacker_xy[:, 0], attacker_xy[:, 1], color=C_ATTACKER, label="Attacker")
    ax.plot(defender_xy[0, 0], defender_xy[0, 1], "o", color=C_DEFENDER, ms=3)
    ax.plot(attacker_xy[0, 0], attacker_xy[0, 1], "o", color=C_ATTACKER, ms=3)
    if capture is not None:
        ax.plot(capture[0], capture[1], "*", color=C_ACCENT, ms=8, label="Capture")
    if goal is not None:
        ax.plot(goal[0], goal[1], "s", color=C_TARGET, ms=4, label="Goal")
    ax.legend(frameon=False)
