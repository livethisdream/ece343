#!/usr/bin/env python3
"""L08 figure: matching with a length of line and a series reactance.

    L08-series-match.svg   the source sees Z_0: a series element jX at distance d
                           from the load, where z_in = 1 + jx

    python3 scripts/graphics/l08_figures.py   ->   book/extras/viz/img/L08-*.svg
"""

from __future__ import annotations
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from l03_figures import lab, save, terminal, NAVY, AMBER, GRAY, INK  # noqa: E402
from l07_figures import line, load_box  # noqa: E402


def series_match():
    fig, ax = plt.subplots(figsize=(9.6, 3.4))
    ax.set_aspect("equal"); ax.axis("off")
    terminal(ax, 0, 2); terminal(ax, 0, 0)
    line(ax, 0.0, 1.6)
    # series element on the top conductor
    ax.plot([1.6, 2.0], [2, 2], color=INK, lw=1.6)
    ax.add_patch(Rectangle((2.0, 1.78), 1.0, 0.44, fc="white", ec=AMBER, lw=2.0))
    lab(ax, 2.5, 2.45, "−jX", size=14, color=AMBER, va="bottom")
    ax.plot([3.0, 3.4], [2, 2], color=INK, lw=1.6)
    ax.plot([1.6, 3.4], [0, 0], color=NAVY, lw=5.0, solid_capstyle="butt")
    line(ax, 3.4, 8.2)
    lab(ax, 5.8, 1.0, "Z", "0", size=16, color=NAVY)
    load_box(ax, 9.0)
    lab(ax, 9.45, 1.0, "Z", "L", ha="left")
    # what each port sees
    lab(ax, 3.55, 1.55, "z = 1 + jx here", size=13, color=GRAY, ha="left", italic=False)
    lab(ax, 0.8, 1.0, "z = 1", size=13, color=NAVY, italic=False)
    ax.annotate("", xy=(8.2, -0.48), xytext=(3.4, -0.48), arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.2))
    lab(ax, 5.8, -0.62, "d", size=15, color=GRAY, va="top")
    ax.set_xlim(-0.6, 10.6); ax.set_ylim(-1.3, 3.1)
    save(fig, "L08-series-match.svg")


if __name__ == "__main__":
    series_match()
