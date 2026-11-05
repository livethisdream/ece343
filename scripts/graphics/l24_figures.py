#!/usr/bin/env python3
"""L24 figures: the electric boundary conditions.

    L24-loop.svg        the thin loop that straddles the boundary, for the
                        tangential condition
    L24-pillbox.svg     the flat Gaussian pillbox, for the normal condition
    L24-conductor.svg   a conductor in electrostatic equilibrium: no field
                        inside, the field outside normal to the surface

Labels are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l24_figures.py   ->   book/extras/viz/img/L24-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL1 = "#f2f7fb"     # region 1, the lower permittivity
FILL2 = "#d6e5f2"     # region 2
METAL = "#9aa8b6"     # conductor
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center",
        italic=True, bold=False):
    """A symbol with an optional subscript, in plain text: an SVG with
    svg.fonttype 'none' cannot carry matplotlib's math fonts into a browser."""
    t = ax.text(x, y, base, fontsize=size, color=color, ha=ha, va=va,
                fontstyle="italic" if italic else "normal",
                fontweight="bold" if bold else "normal")
    if not sub:
        return t
    fig = ax.figure
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    w = bb.width / fig.dpi * 72                     # base width in points
    shift = {"center": w / 2, "left": w, "right": 0}[ha]
    ax.annotate(sub, (x, y), xytext=(shift + 0.5, -size * 0.32), textcoords="offset points",
                fontsize=size * 0.7, color=color, ha="left", va=va)
    return t


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=2.0, ls="-", head=12):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", color=color,
                                 lw=lw, ls=ls, mutation_scale=head, shrinkA=0, shrinkB=0))


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def two_regions(ax, xlim=(-3.2, 3.2), ylim=(-1.6, 1.6)):
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.add_patch(Rectangle((xlim[0], 0), xlim[1] - xlim[0], ylim[1], fc=FILL1, ec="none"))
    ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], -ylim[0], fc=FILL2, ec="none"))
    ax.plot(xlim, [0, 0], color=INK, lw=1.6)
    lab(ax, xlim[0] + 0.25, ylim[1] - 0.3, "ε", "1", ha="left")
    lab(ax, xlim[0] + 0.25, ylim[0] + 0.3, "ε", "2", ha="left")
    # unit vectors, lower right
    ox, oy = xlim[1] - 0.95, ylim[0] + 0.3
    arrow(ax, ox, oy, ox + 0.55, oy, color=GRAY, lw=1.4, head=10)
    arrow(ax, ox, oy, ox, oy + 0.55, color=GRAY, lw=1.4, head=10)
    lab(ax, ox + 0.68, oy, "t̂", size=13, color=GRAY, ha="left", italic=False, bold=True)
    lab(ax, ox, oy + 0.72, "n̂", size=13, color=GRAY, italic=False, bold=True)


# ---------------------------------------------------------------------------
def loop():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    two_regions(ax)
    x0, x1, h = -1.9, 1.1, 0.8
    a, b, c, d = (x0, h / 2), (x1, h / 2), (x1, -h / 2), (x0, -h / 2)
    for p, q in ((a, b), (b, c), (c, d), (d, a)):
        mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=RED, lw=1.8)
        arrow(ax, p[0], p[1], mid[0], mid[1], color=RED, lw=1.8, head=13)
    for (px, py), name, va in ((a, "a", "bottom"), (b, "b", "bottom"), (c, "c", "top"), (d, "d", "top")):
        ax.plot(px, py, "o", color=RED, ms=4)
        ax.text(px + (-0.12 if name in "ad" else 0.12), py + (0.08 if va == "bottom" else -0.08),
                name, color=RED, fontsize=13, ha="right" if name in "ad" else "left", va=va)
    # dimensions
    ax.annotate("", xy=(x0, -1.05), xytext=(x1, -1.05),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, (x0 + x1) / 2, -1.28, "W", size=14, color=GRAY)
    ax.annotate("", xy=(x1 + 0.35, h / 2), xytext=(x1 + 0.35, -h / 2),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, x1 + 0.52, 0, "h", size=14, color=GRAY, ha="left")
    # the fields on each side: eps2 = 2 eps1, so E2 leans further from the
    # normal (30 degrees above, 49 below) with the same tangential part
    px, L = 2.3, 1.35
    t1, n1 = L * np.sin(np.radians(30)), L * np.cos(np.radians(30))
    arrow(ax, px, 0.0, px + t1, n1, color=NAVY, lw=2.2)
    lab(ax, px + t1 + 0.1, n1 - 0.05, "E", "1", color=NAVY, italic=False, bold=True, ha="left")
    arrow(ax, px - t1, -n1 / 2, px, 0.0, color=BLUE, lw=2.2)
    lab(ax, px - t1, -n1 / 2 - 0.3, "E", "2", color=BLUE, italic=False, bold=True, ha="center")
    save(fig, "L24-loop.svg")


def pillbox():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    two_regions(ax)
    cx, w, h, e = -0.5, 2.6, 1.0, 0.32
    # surface charge along the boundary
    for x in np.arange(-3.0, 2.0, 0.3):
        ax.text(x, 0.0, "+", color=RED, fontsize=11, ha="center", va="center")
    ax.plot([cx - w / 2, cx - w / 2], [-h / 2, h / 2], color=NAVY, lw=1.6)
    ax.plot([cx + w / 2, cx + w / 2], [-h / 2, h / 2], color=NAVY, lw=1.6)
    ax.add_patch(Ellipse((cx, h / 2), w, e, fc="none", ec=NAVY, lw=1.6))
    ax.add_patch(Ellipse((cx, -h / 2), w, e, fc="none", ec=NAVY, lw=1.6, ls="--"))
    lab(ax, cx + w / 2 + 0.12, h / 2 + 0.12, "ΔA", size=14, color=NAVY, ha="left")
    ax.annotate("", xy=(cx - w / 2 - 0.3, h / 2), xytext=(cx - w / 2 - 0.3, -h / 2),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, cx - w / 2 - 0.48, 0.28, "h", size=14, color=GRAY, ha="right")
    # outward normals of the two caps
    arrow(ax, cx - 0.55, h / 2, cx - 0.55, h / 2 + 0.75, color=GRAY, lw=1.4, head=10)
    lab(ax, cx - 0.7, h / 2 + 0.62, "n̂", size=13, color=GRAY, ha="right", italic=False, bold=True)
    arrow(ax, cx - 0.55, -h / 2, cx - 0.55, -h / 2 - 0.75, color=GRAY, lw=1.4, head=10)
    lab(ax, cx - 0.7, -h / 2 - 0.62, "−n̂", size=13, color=GRAY, ha="right", italic=False, bold=True)
    # the flux densities
    arrow(ax, cx + 0.45, h / 2, cx + 0.95, h / 2 + 1.0, color=NAVY, lw=2.2)
    lab(ax, cx + 1.05, h / 2 + 0.95, "D", "1", color=NAVY, italic=False, bold=True, ha="left")
    arrow(ax, cx + 0.05, -h / 2 - 0.85, cx + 0.45, -h / 2, color=BLUE, lw=2.2)
    lab(ax, cx + 0.5, -h / 2 - 0.6, "D", "2", color=BLUE, italic=False, bold=True, ha="left")
    lab(ax, 2.05, 0.18, "ρ", "s", size=14, color=RED, ha="left")
    save(fig, "L24-pillbox.svg")


def conductor():
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-1.5, 1.7)
    ax.add_patch(Rectangle((-3.2, 0), 6.4, 1.7, fc=FILL1, ec="none"))
    ax.add_patch(Rectangle((-3.2, -1.5), 6.4, 1.5, fc=METAL, ec="none"))
    ax.plot([-3.2, 3.2], [0, 0], color=INK, lw=1.6)
    for x in np.arange(-2.9, 3.0, 0.3):
        ax.text(x, -0.13, "+", color=RED, fontsize=11, ha="center", va="center")
    for x in (-2.1, -1.0, 0.1, 1.2, 2.3):
        arrow(ax, x, 0.08, x, 1.05, color=NAVY, lw=2.0)
    lab(ax, 2.6, 0.75, "E", "", color=NAVY, italic=False, bold=True, ha="left")
    lab(ax, -2.95, 1.4, "ε", ha="left")
    ax.text(0.15, -0.8, "conductor:", fontsize=14, color=INK, ha="right", va="center")
    lab(ax, 0.3, -0.8, "E = 0", size=14, italic=False, bold=True, ha="left")
    lab(ax, 2.75, -0.42, "ρ", "s", size=14, color=RED, ha="left")
    save(fig, "L24-conductor.svg")


if __name__ == "__main__":
    loop()
    pillbox()
    conductor()
