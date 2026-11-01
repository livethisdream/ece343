#!/usr/bin/env python3
"""L22 figures: work around a point charge, and a finite line of charge.

    L22-paths.svg        two paths from A to B near a point charge; the
                         staircase path splits into radial and circular steps
    L22-finite-line.svg  a line charge from z = -a to z = a, a field point at
                         radius rho, and the distance R to a charge element

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l22_figures.py   ->   book/extras/viz/img/L22-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
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


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def arrow(ax, p0, p1, color, lw=1.6, style="-|>"):
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                                     shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------------------
def paths():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.6, 4.6); ax.set_ylim(-0.5, 3.6)

    # faint equipotential circles around the charge
    for r in (1.0, 1.6, 2.2, 2.8, 3.4, 4.0):
        th = np.linspace(-0.15, np.pi / 2 + 0.15, 200)
        ax.plot(r * np.cos(th), r * np.sin(th), color="#e3edf6", lw=1.0, zorder=0)
    ax.add_patch(Circle((0, 0), 0.16, fc=RED, ec=INK, lw=1.0, zorder=3))
    lab(ax, -0.32, -0.26, "Q", size=15, color=RED)

    A = np.array([1.0, 0.0]) * 1.0
    thB, rB = np.deg2rad(62), 3.4
    B = rB * np.array([np.cos(thB), np.sin(thB)])

    # path 1: a smooth curve, amber
    t = np.linspace(0, 1, 120)
    r1 = 1.0 + (rB - 1.0) * t
    th1 = thB * t ** 0.6
    curve = np.c_[r1 * np.cos(th1), r1 * np.sin(th1)]
    curve[:, 0] += 0.55 * np.sin(np.pi * t)
    ax.plot(curve[:, 0], curve[:, 1], color=AMBER, lw=2.0)
    arrow(ax, curve[70], curve[74], AMBER, lw=2.0)

    # path 2: a staircase of radial steps and circular arcs, navy
    rs = np.linspace(1.0, rB, 5)
    ths = np.linspace(0, thB, 5)
    pts = [A]
    for k in range(4):
        r0, r1_ = rs[k], rs[k + 1]
        a0, a1 = ths[k], ths[k + 1]
        # arc at radius r0 from a0 to a1
        aa = np.linspace(a0, a1, 30)
        arc = np.c_[r0 * np.cos(aa), r0 * np.sin(aa)]
        ax.plot(arc[:, 0], arc[:, 1], color=NAVY, lw=2.0, ls=(0, (4, 2)))
        # radial step out from r0 to r1 at angle a1
        p0 = r0 * np.array([np.cos(a1), np.sin(a1)])
        p1 = r1_ * np.array([np.cos(a1), np.sin(a1)])
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=NAVY, lw=2.6)
    ax.plot(*A, "o", color=INK, ms=7, zorder=4)
    ax.plot(*B, "o", color=INK, ms=7, zorder=4)
    lab(ax, A[0] - 0.12, A[1] - 0.28, "A", size=15, italic=False)
    lab(ax, B[0] + 0.22, B[1] + 0.12, "B", size=15, italic=False)

    # legend-like labels, minimal
    ax.plot([2.9, 3.35], [0.55, 0.55], color=NAVY, lw=2.6)
    ax.text(3.45, 0.55, "radial step: work", fontsize=12, color=NAVY, va="center")
    ax.plot([2.9, 3.35], [0.15, 0.15], color=NAVY, lw=2.0, ls=(0, (4, 2)))
    ax.text(3.45, 0.15, "circular step: none", fontsize=12, color=NAVY, va="center")
    save(fig, "L22-paths.svg")


def finite_line():
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.4, 3.4); ax.set_ylim(-2.4, 2.5)

    a = 1.8
    ax.annotate("", xy=(0, 2.35), xytext=(0, -2.3),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.0))
    lab(ax, 0.2, 2.35, "z", size=14, color=GRAY, ha="left")
    ax.annotate("", xy=(3.2, 0), xytext=(-0.3, 0),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.0))
    ax.plot([0, 0], [-a, a], color=RED, lw=5, solid_capstyle="butt")
    lab(ax, -0.32, 1.1, "ρ", "ℓ", size=15, color=RED, ha="right")
    ax.plot([-0.12, 0.12], [a, a], color=INK, lw=1.2)
    ax.plot([-0.12, 0.12], [-a, -a], color=INK, lw=1.2)
    lab(ax, -0.22, a, "a", size=14, ha="right")
    lab(ax, -0.22, -a, "−a", size=14, ha="right")

    # charge element dz at z'
    zp = 0.9
    ax.plot([0, 0], [zp - 0.14, zp + 0.14], color=INK, lw=7, solid_capstyle="butt")
    lab(ax, 0.2, zp + 0.18, "dz", size=13, ha="left")
    P = np.array([2.3, 0.0])
    ax.plot(*P, "o", color=NAVY, ms=7)
    lab(ax, P[0] + 0.05, P[1] - 0.3, "P", size=14, italic=False, color=NAVY)
    ax.plot([0, P[0]], [zp, P[1]], color=NAVY, lw=1.6, ls=(0, (4, 2)))
    lab(ax, 1.35, 0.72, "R", size=15, color=NAVY)
    lab(ax, 1.15, -0.3, "ρ", size=14, color=GRAY)
    save(fig, "L22-finite-line.svg")


if __name__ == "__main__":
    paths()
    finite_line()
