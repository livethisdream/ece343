#!/usr/bin/env python3
"""L41 figures: the Incidence Lab's grids.

    L41-yee.svg     the one-dimensional Yee grid: E_x at whole cells and whole
                    time steps, H_y halfway between in space and in time
    L41-setup.svg   the two-dimensional simulation: the absorbing layer around
                    the edge, the source line, the beam at an angle, the
                    boundary between the media, and the two lines where the
                    power is measured

Labels are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l41_figures.py   ->   book/extras/viz/img/L41-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402
from l24_figures import lab, arrow  # noqa: E402

NAVY, AMBER, GREEN, GRAY, INK = "#004a85", "#8a5a00", "#1d7a4d", "#5b6573", "#15202b"
FILL = "#e3edf6"       # medium 2
PML = "#eef0f3"        # the absorbing layer
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 14, "text.color": INK})


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def yee():
    """Space runs to the right in cells, time runs up in half steps."""
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ks = np.arange(0, 5)
    for t, kind in ((0.0, "E"), (0.5, "H"), (1.0, "E")):
        ax.plot([-0.4, 4.4], [t, t], color=GRAY, lw=0.8, ls=":")
        if kind == "E":
            ax.plot(ks, np.full_like(ks, t, dtype=float), "o", color=NAVY, ms=11)
        else:
            ax.plot(ks[:-1] + 0.5, np.full(4, t), "s", color=AMBER, ms=10)
    # the stencil for one E update: E at k from E at k (below) and H at k ± 1/2
    arrow(ax, 2.0, 0.08, 2.0, 0.9, color=NAVY, lw=1.6, head=12)
    arrow(ax, 1.5, 0.56, 1.93, 0.93, color=AMBER, lw=1.6, head=12)
    arrow(ax, 2.5, 0.56, 2.07, 0.93, color=AMBER, lw=1.6, head=12)
    # labels
    lab(ax, -0.62, 0.0, "n", size=15, ha="right")
    lab(ax, -0.62, 0.5, "n + ½", size=15, ha="right")
    lab(ax, -0.62, 1.0, "n + 1", size=15, ha="right")
    for k in range(5):
        lab(ax, k, -0.2, f"{k}" if k else "k = 0", size=13, italic=False, color=GRAY)
    ax.plot([4.75], [1.0], "o", color=NAVY, ms=11)
    lab(ax, 4.95, 1.0, "E", "x", size=15, ha="left", color=NAVY)
    ax.plot([4.75], [0.5], "s", color=AMBER, ms=10)
    lab(ax, 4.95, 0.5, "H", "y", size=15, ha="left", color=AMBER)
    ax.text(2.0, -0.42, "z", ha="center", fontsize=15, fontstyle="italic", color=GRAY)
    ax.set_xlim(-1.3, 5.6); ax.set_ylim(-0.5, 1.15)
    ax.axis("off")
    save(fig, "L41-yee.svg")


def setup():
    """A schematic, not to scale: the vertical spacing is stretched for room."""
    W, H, P = 24.0, 12.0, 1.0
    yb = 6.0                              # the boundary
    zs, zm, zt = 9.6, 7.6, 4.4            # source line and measurement lines
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.add_patch(Rectangle((0, 0), W, H, facecolor=PML, edgecolor=GRAY, lw=1.0))
    ax.add_patch(Rectangle((P, P), W - 2 * P, H - 2 * P, facecolor="white", edgecolor=GRAY, lw=0.8))
    ax.add_patch(Rectangle((P, P), W - 2 * P, yb - P, facecolor=FILL, edgecolor="none"))
    ax.plot([P, W - P], [yb, yb], color=INK, lw=1.6)
    ax.plot([P, W - P], [zs, zs], color=GREEN, lw=2.0)
    ax.plot([P, W - P], [zm, zm], color=AMBER, lw=1.4, ls="--")
    ax.plot([P, W - P], [zt, zt], color=AMBER, lw=1.4, ls="--")
    # the beam meets the boundary at x = xh
    xh = 12.0
    th, tt = np.radians(45), np.radians(28.3)
    arrow(ax, xh - (zs - yb) * np.tan(th), zs, xh, yb, color=NAVY, lw=2.6, head=16)
    arrow(ax, xh, yb, xh + 3.3 * np.sin(th), yb + 3.3 * np.cos(th), color=NAVY, lw=1.6, ls="--", head=14)
    arrow(ax, xh, yb, xh + 4.6 * np.sin(tt), yb - 4.6 * np.cos(tt), color=NAVY, lw=2.0, head=15)
    ax.plot([xh, xh], [yb - 3.4, yb + 3.4], color=GRAY, lw=0.8, ls=":")
    lab(ax, xh - 0.75, yb + 2.0, "θ", "i", size=16)
    lab(ax, xh + 0.7, yb - 2.3, "θ", "t", size=16)
    # labels, each in clear space beside its line
    ax.text(W - P - 0.3, yb + 0.3, "medium 1", ha="right", va="bottom", fontsize=14)
    ax.text(W - P - 0.3, yb - 0.3, "medium 2", ha="right", va="top", fontsize=14)
    ax.text(P + 0.3, zs + 0.25, "source line", ha="left", va="bottom", fontsize=14, color=GREEN)
    ax.text(P + 0.3, zm + 0.25, "power measured", ha="left", va="bottom", fontsize=14, color=AMBER)
    ax.text(P + 0.3, zt - 0.25, "power measured", ha="left", va="top", fontsize=14, color=AMBER)
    ax.text(W / 2, H - 0.5, "absorbing layer (PML)", ha="center", va="center", fontsize=13, color=GRAY)
    ax.set_xlim(-0.2, W + 0.2); ax.set_ylim(-0.2, H + 0.2)
    ax.set_aspect("equal"); ax.axis("off")
    save(fig, "L41-setup.svg")


if __name__ == "__main__":
    yee()
    setup()
