#!/usr/bin/env python3
"""L09 figure: single-stub matching.

    L09-stub-match.svg   a shorted stub of length ℓ_s in shunt at distance d
                         from the load, where y = 1 + jb

    python3 scripts/graphics/l09_figures.py   ->   book/extras/viz/img/L09-*.svg
"""

from __future__ import annotations
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from l03_figures import lab, save, terminal, NAVY, AMBER, GRAY, INK  # noqa: E402
from l07_figures import line, load_box  # noqa: E402


def stub_match():
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    ax.set_aspect("equal"); ax.axis("off")
    terminal(ax, 0, 2); terminal(ax, 0, 0)
    line(ax, 0.0, 8.2)
    lab(ax, 1.4, 1.0, "Z", "0", size=16, color=NAVY)
    lab(ax, 6.0, 1.0, "Z", "0", size=16, color=NAVY)
    load_box(ax, 9.0)
    lab(ax, 9.45, 1.0, "Z", "L", ha="left")
    # The stub hangs below the line at x = xs, in shunt: its right conductor
    # joins the bottom conductor, and its left conductor reaches up to the top
    # conductor, hopping over the bottom one.
    xs = 3.4
    xl, xr = xs - 0.3, xs + 0.3
    ax.plot([xl, xl], [2.0, 0.22], color=INK, lw=1.6)
    th = np.linspace(np.pi / 2, -np.pi / 2, 30)
    ax.plot(xl + 0.22 * np.cos(th), 0.22 * np.sin(th), color=INK, lw=1.6)
    ax.add_patch(Rectangle((xl - 0.05, -0.12), 0.1, 0.24, fc="white", ec="none", zorder=3))
    ax.plot([xl, xl], [-0.22, -0.45], color=INK, lw=1.6)
    ax.plot([xr, xr], [0.0, -0.45], color=INK, lw=1.6)
    for x in (xl,):
        ax.add_patch(Circle((x, 2.0), 0.06, fc=INK, ec=INK, zorder=4))
    ax.add_patch(Circle((xr, 0.0), 0.06, fc=INK, ec=INK, zorder=4))
    ax.plot([xl, xl], [-0.45, -2.6], color=AMBER, lw=4.0, solid_capstyle="butt")
    ax.plot([xr, xr], [-0.45, -2.6], color=AMBER, lw=4.0, solid_capstyle="butt")
    ax.plot([xl, xr], [-2.6, -2.6], color=INK, lw=2.4)
    lab(ax, xl - 0.3, -1.5, "ℓ", "s", color=AMBER, ha="right")
    lab(ax, xr + 0.3, -2.45, "short", size=12, color=GRAY, ha="left", italic=False)
    lab(ax, xs + 0.15, 2.35, "y = 1 + jb", size=13, color=GRAY, ha="left", va="bottom", italic=False)
    ax.annotate("", xy=(8.2, -0.5), xytext=(xr + 0.1, -0.5), arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.2))
    lab(ax, 5.8, -0.65, "d", size=15, color=GRAY, va="top")
    ax.set_xlim(-0.6, 10.6); ax.set_ylim(-3.0, 2.9)
    save(fig, "L09-stub-match.svg")


if __name__ == "__main__":
    stub_match()
