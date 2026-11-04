#!/usr/bin/env python3
"""L21 figures: the point form of Gauss's law.

    L21-box.svg       a small box, with the flux in through the face at x and
                      out through the face at x + Δx
    L21-sources.svg   three fields: one with charge inside the region, one
                      that spreads out with no charge, and a uniform one

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l21_figures.py   ->   book/extras/viz/img/L21-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL = "#e3edf6"
CHARGE = "#f3d9d9"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center", italic=True):
    """A symbol with an optional subscript, in plain text (see l03_figures.py)."""
    t = ax.text(x, y, base, fontsize=size, color=color, ha=ha, va=va,
                fontstyle="italic" if italic else "normal")
    if not sub:
        return t
    fig = ax.figure
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    w = bb.width / fig.dpi * 72
    shift = {"center": w / 2, "left": w, "right": 0}[ha]
    ax.annotate(sub, (x, y), xytext=(shift + 0.5, -size * 0.32), textcoords="offset points",
                fontsize=size * 0.7, color=color, ha="left", va=va)
    return t


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=1.6, ms=12):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def box():
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-2.6, 5.4); ax.set_ylim(-1.0, 2.6)
    w, h, dx, dy = 2.0, 1.5, 0.9, 0.6           # width (Δx), height (Δz), depth offset (Δy)
    front = [(0, 0), (w, 0), (w, h), (0, h)]
    back = [(x + dx, y + dy) for x, y in front]
    ax.add_patch(Polygon(back, fc="none", ec=NAVY, lw=1.0, ls="--"))
    left = [(0, 0), (dx, dy), (dx, h + dy), (0, h)]
    right = [(w, 0), (w + dx, dy), (w + dx, h + dy), (w, h)]
    ax.add_patch(Polygon(left, fc=FILL, ec=NAVY, lw=1.4))
    ax.add_patch(Polygon(right, fc=FILL, ec=NAVY, lw=1.4))
    ax.add_patch(Polygon(front, fc="none", ec=NAVY, lw=1.6))
    ax.plot([0, dx], [h, h + dy], color=NAVY, lw=1.6); ax.plot([w, w + dx], [h, h + dy], color=NAVY, lw=1.6)
    ax.plot([dx, w + dx], [h + dy, h + dy], color=NAVY, lw=1.6)
    cyl, cyr = h / 2 + dy / 2, h / 2 + dy / 2
    arrow(ax, -1.7, cyl, dx / 2, cyl, color=BLUE, lw=2.0)
    arrow(ax, w + dx / 2, cyr, w + dx / 2 + 1.9, cyr, color=BLUE, lw=2.6)
    lab(ax, -1.75, cyl + 0.32, "D", "x", color=BLUE, ha="left", italic=False)
    ax.text(-1.32, cyl + 0.34, "(x)", fontsize=14, color=BLUE, ha="left")
    lab(ax, w + dx / 2 + 0.25, cyr + 0.32, "D", "x", color=BLUE, ha="left", italic=False)
    ax.text(w + dx / 2 + 0.68, cyr + 0.34, "(x + Δx)", fontsize=14, color=BLUE, ha="left")
    ax.annotate("", xy=(w, -0.3), xytext=(0, -0.3), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
    ax.text(w / 2, -0.62, "Δx", fontsize=14, color=GRAY, ha="center", fontstyle="italic")
    ax.annotate("", xy=(-0.3, h), xytext=(-0.3, 0), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
    ax.text(-0.42, h / 2 - 0.35, "Δz", fontsize=14, color=GRAY, ha="right", fontstyle="italic")
    ax.annotate("", xy=(dx - 0.15, h + dy + 0.15), xytext=(-0.15, h + 0.15),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
    ax.text(dx / 2 - 0.3, h + dy / 2 + 0.3, "Δy", fontsize=14, color=GRAY, ha="right", fontstyle="italic")
    save(fig, "L21-box.svg")


def sources():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.6))
    titles = ["charge inside: ∇·D > 0", "no charge: ∇·D = 0", "no charge: ∇·D = 0"]
    for ax, title in zip(axs, titles):
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.75, 1.6)
        ax.add_patch(Circle((0, 0), 0.75, fc="none", ec=NAVY, lw=1.2, ls="--"))
        ax.text(0, -1.7, title, ha="center", fontsize=12, color=GRAY)

    # (1) inside a uniform volume charge: D grows in proportion to r
    ax = axs[0]
    ax.add_patch(Circle((0, 0), 1.5, fc=CHARGE, ec="none", zorder=0))
    for r in (0.4, 0.8, 1.2):
        for a in np.radians(np.arange(0, 360, 45) + (22.5 if r == 0.8 else 0)):
            L = 0.32 * r
            arrow(ax, r * np.cos(a), r * np.sin(a), (r + L) * np.cos(a), (r + L) * np.sin(a), color=BLUE, lw=1.3, ms=9)
    # (2) outside a point charge: D falls as 1/r², spreading
    ax = axs[1]
    ax.plot(0, 0, "o", color=RED, ms=6)
    ax.add_patch(Circle((0, 0), 0.75, fc="none", ec="none"))
    for r in (0.45, 0.85, 1.25):
        for a in np.radians(np.arange(0, 360, 45) + (22.5 if r == 0.85 else 0)):
            L = 0.075 / r ** 2
            L = min(L, 0.36)
            arrow(ax, r * np.cos(a), r * np.sin(a), (r + L) * np.cos(a), (r + L) * np.sin(a), color=BLUE, lw=1.3, ms=9)
    # the small dashed circle in panel 2 sits away from the charge
    axs[1].patches[0].set_center((0.65, 0.55)); axs[1].patches[0].set_radius(0.42)
    # (3) uniform field
    ax = axs[2]
    for y in (-1.1, -0.55, 0.0, 0.55, 1.1):
        for x in (-1.3, -0.4, 0.5):
            arrow(ax, x, y, x + 0.55, y, color=BLUE, lw=1.3, ms=9)
    save(fig, "L21-sources.svg")


if __name__ == "__main__":
    box()
    sources()
