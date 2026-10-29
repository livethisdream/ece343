#!/usr/bin/env python3
"""L07 figures: the input impedance of a terminated line.

    L07-input-impedance.svg   a load Z_L at the end of a line of length ℓ, and
                              the impedance Z_in seen looking into it at z = −ℓ
    L07-stubs.svg             shorted and open stubs, the reactances they stand in for

Labels are plain Unicode (see CLAUDE.md); the drawing helpers come from L03.

    python3 scripts/graphics/l07_figures.py   ->   book/extras/viz/img/L07-*.svg
"""

from __future__ import annotations
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from l03_figures import lab, save, terminal, inductor, capacitor, NAVY, AMBER, GRAY, INK  # noqa: E402


def line(ax, x0, x1, yt=2.0, yb=0.0):
    ax.plot([x0, x1], [yt, yt], color=NAVY, lw=5.0, solid_capstyle="butt")
    ax.plot([x0, x1], [yb, yb], color=NAVY, lw=5.0, solid_capstyle="butt")


def load_box(ax, x, yt=2.0, yb=0.0):
    ax.plot([x - 0.6, x], [yt, yt], color=INK, lw=1.6)
    ax.plot([x - 0.6, x], [yb, yb], color=INK, lw=1.6)
    ax.plot([x, x], [yt, 1.5], color=INK, lw=1.6)
    ax.plot([x, x], [0.5, yb], color=INK, lw=1.6)
    ax.add_patch(Rectangle((x - 0.22, 0.5), 0.44, 1.0, fc="white", ec=INK, lw=1.6))


def input_impedance():
    fig, ax = plt.subplots(figsize=(9.0, 3.3))
    ax.set_aspect("equal"); ax.axis("off")
    ax.plot([0, 1.0], [2, 2], color=INK, lw=1.6)
    ax.plot([0, 1.0], [0, 0], color=INK, lw=1.6)
    terminal(ax, 0, 2); terminal(ax, 0, 0)
    line(ax, 1.0, 6.8)
    lab(ax, 3.9, 1.0, "Z", "0", size=17, color=NAVY)
    load_box(ax, 7.6)
    lab(ax, 8.05, 1.0, "Z", "L", ha="left")
    ax.add_patch(FancyArrowPatch((-0.2, 1.0), (-1.4, 1.0), arrowstyle="<|-", mutation_scale=16, color=AMBER, lw=1.8))
    lab(ax, -1.55, 1.0, "Z", "in", color=AMBER, ha="right")
    for x, txt in ((1.0, "z = −ℓ"), (6.8, "z = 0")):
        ax.plot([x, x], [-0.35, -0.6], color=GRAY, lw=1.2)
        lab(ax, x, -0.72, txt, size=14, color=GRAY, va="top")
    ax.annotate("", xy=(6.8, 2.55), xytext=(1.0, 2.55), arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.2))
    lab(ax, 3.9, 2.7, "ℓ", size=15, color=GRAY, va="bottom")
    ax.set_xlim(-2.9, 9.4); ax.set_ylim(-1.4, 3.3)
    save(fig, "L07-input-impedance.svg")


def stubs():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.0))
    for ax, kind in zip(axs, ("short", "open")):
        ax.set_aspect("equal"); ax.axis("off")
        terminal(ax, 0, 2); terminal(ax, 0, 0)
        ax.plot([0, 0.6], [2, 2], color=INK, lw=1.6); ax.plot([0, 0.6], [0, 0], color=INK, lw=1.6)
        line(ax, 0.6, 3.6)
        if kind == "short":
            ax.plot([3.6, 3.6], [0, 2], color=INK, lw=2.4)
            lab(ax, 2.1, 2.45, "shorted stub", size=13, color=INK, va="bottom", italic=False)
            ax.add_patch(FancyArrowPatch((4.2, 1.0), (5.0, 1.0), arrowstyle="-|>", mutation_scale=14, color=GRAY, lw=1.4))
            ax.plot([5.6, 5.6], [2, 1.75], color=INK, lw=1.6); ax.plot([5.6, 5.6], [0.25, 0], color=INK, lw=1.6)
            # vertical inductor: draw loops on a rotated axis by hand
            import numpy as np
            for k in range(4):
                c = 1.5 - 0.375 * k - 0.1875
                th = np.linspace(-np.pi / 2, np.pi / 2, 40)
                ax.plot(5.6 + 0.19 * np.cos(th), c + 0.19 * np.sin(th), color=INK, lw=1.6)
            ax.plot([5.6, 5.6], [1.75, 1.5], color=INK, lw=1.6)
            ax.plot([5.6, 5.6], [0.0, 0.25], color=INK, lw=1.6)
            terminal(ax, 5.6, 2); terminal(ax, 5.6, 0)
            lab(ax, 2.1, -0.35, "ℓ < λ/4", size=13, color=GRAY, va="top", italic=False)
        else:
            lab(ax, 2.1, 2.45, "open stub", size=13, color=INK, va="bottom", italic=False)
            ax.add_patch(FancyArrowPatch((4.2, 1.0), (5.0, 1.0), arrowstyle="-|>", mutation_scale=14, color=GRAY, lw=1.4))
            capacitor(ax, 5.6, 2.0, 0.0)
            terminal(ax, 5.6, 2); terminal(ax, 5.6, 0)
            lab(ax, 2.1, -0.35, "ℓ < λ/4", size=13, color=GRAY, va="top", italic=False)
        ax.set_xlim(-0.4, 6.4); ax.set_ylim(-1.0, 3.0)
    fig.subplots_adjust(wspace=0.1)
    save(fig, "L07-stubs.svg")


if __name__ == "__main__":
    input_impedance()
    stubs()
