#!/usr/bin/env python3
"""L18 figures: Coulomb's law, superposition, and the first distribution.

    L18-coulomb.svg        source point r′, field point r, and R = r − r′
    L18-three-charges.svg  the worked example: the forces on q3 from q1 and q2
    L18-dipole.svg         a dipole and a field point on its bisector
    L18-line-charge.svg    a finite line charge, one element dQ, and its
                           mirror image, whose z components cancel

Labels are plain Unicode (see CLAUDE.md); vectors are bold and upright,
scalars italic. The lesson text does the explaining.

    python3 scripts/graphics/l18_figures.py   ->   book/extras/viz/img/L18-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
GREEN = "#1d7a4d"
AXIS = "#9aa8b6"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center", italic=True, bold=False):
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
    w = bb.width / fig.dpi * 72
    shift = {"center": w / 2, "left": w, "right": 0}[ha]
    ax.annotate(sub, (x, y), xytext=(shift + 0.5, -size * 0.32), textcoords="offset points",
                fontsize=size * 0.7, color=color, ha="left", va=va,
                fontweight="bold" if bold else "normal")
    return t


def vec(ax, x, y, name, sub="", size=15, color=INK, ha="center", va="center"):
    """A vector label: bold and upright."""
    return lab(ax, x, y, name, sub, size=size, color=color, ha=ha, va=va, italic=False, bold=True)


def arrow(ax, p0, p1, color=INK, lw=1.8, ls="-", ms=16):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0))


def charge(ax, x, y, sign, r=0.16, zorder=5):
    ax.add_patch(Circle((x, y), r, fc=RED if sign > 0 else NAVY, ec="none", zorder=zorder))
    ax.text(x, y - 0.01, "+" if sign > 0 else "−", color="white", fontsize=13, fontweight="bold",
            ha="center", va="center", zorder=zorder + 1)


def point(ax, x, y, color=INK):
    ax.add_patch(Circle((x, y), 0.07, fc=color, ec="none", zorder=5))


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def axes2d(ax, xr, yr, xl="x", yl="y"):
    arrow(ax, (xr[0], 0), (xr[1], 0), color=AXIS, lw=1.2, ms=12)
    arrow(ax, (0, yr[0]), (0, yr[1]), color=AXIS, lw=1.2, ms=12)
    lab(ax, xr[1], -0.28, xl, size=13, color=GRAY, ha="right", va="top")
    lab(ax, 0.18, yr[1], yl, size=13, color=GRAY, ha="left", va="top")


# ---------------------------------------------------------------------------
def coulomb():
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.6, 6.2); ax.set_ylim(-0.5, 3.6)
    axes2d(ax, (-0.4, 6.0), (-0.4, 3.5))
    src, obs = np.array([1.4, 2.4]), np.array([5.0, 1.0])
    arrow(ax, (0, 0), src, color=GRAY, lw=1.6)
    arrow(ax, (0, 0), obs, color=GRAY, lw=1.6)
    arrow(ax, src, obs, color=AMBER, lw=2.4, ms=18)
    charge(ax, *src, +1)
    point(ax, *obs, color=INK)
    vec(ax, 0.42, 1.45, "r′", color=GRAY)
    vec(ax, 2.7, 0.22, "r", color=GRAY)
    vec(ax, 3.55, 2.15, "R = r − r′", color=AMBER, ha="left")
    lab(ax, 1.4, 2.78, "Q", size=15, color=RED)
    ax.text(1.62, 2.82, "source", fontsize=11.5, color=GRAY, ha="left", va="center")
    ax.text(5.15, 0.72, "field point", fontsize=11.5, color=GRAY, ha="left", va="center")
    ax.text(-0.12, -0.18, "O", fontsize=12, color=GRAY, ha="right", va="top")
    save(fig, "L18-coulomb.svg")


# ---------------------------------------------------------------------------
def three_charges():
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-2.6, 6.0); ax.set_ylim(-2.9, 4.2)
    axes2d(ax, (-1.2, 5.8), (-2.8, 4.1), "x (m)", "y (m)")
    for k in range(-2, 5):
        if k and k not in (3, -2):          # those ticks sit under q1 and q2
            ax.plot([-0.06, 0.06], [k, k], color=AXIS, lw=1)
            ax.text(-0.14, k, str(k).replace("-", "−"), fontsize=10.5, color=GRAY, ha="right", va="center")
    for k in range(1, 6):
        ax.plot([k, k], [-0.06, 0.06], color=AXIS, lw=1)
        ax.text(k, -0.16, str(k), fontsize=10.5, color=GRAY, ha="center", va="top")
    q1, q2, q3 = np.array([0, 3.0]), np.array([0, -2.0]), np.array([4.0, 0])
    ax.plot(*zip(q1, q3), color=GRAY, lw=1.0, ls="--")
    ax.plot(*zip(q2, q3), color=GRAY, lw=1.0, ls="--")
    # forces in mN, drawn at one unit per mN
    f31, f32 = np.array([-1.726, 1.294]), np.array([0.804, 0.402])
    arrow(ax, q3, q3 + f31, color=NAVY, lw=2.0)
    arrow(ax, q3, q3 + f32, color=RED, lw=2.0)
    arrow(ax, q3, q3 + f31 + f32, color=AMBER, lw=2.6, ms=18)
    charge(ax, *q1, -1); charge(ax, *q2, +1); charge(ax, *q3, +1)
    lab(ax, -0.62, 3.2, "q", "1", color=NAVY, ha="right")
    ax.text(-0.3, 2.72, "−3 μC", fontsize=11.5, color=NAVY, ha="right", va="center")
    lab(ax, -0.62, -1.8, "q", "2", color=RED, ha="right")
    ax.text(-0.3, -2.28, "1 μC", fontsize=11.5, color=RED, ha="right", va="center")
    lab(ax, 4.22, -0.3, "q", "3", color=RED, ha="left")
    ax.text(4.22, -0.75, "2 μC", fontsize=11.5, color=RED, ha="left", va="center")
    vec(ax, *(q3 + f31 + np.array([-0.05, -0.42])), "F", "31", color=NAVY, ha="right")
    vec(ax, *(q3 + f32 + np.array([0.12, 0.12])), "F", "32", color=RED, ha="left")
    vec(ax, *(q3 + f31 + f32 + np.array([0.12, 0.2])), "F", "3", color=AMBER, ha="left")
    save(fig, "L18-three-charges.svg")


# ---------------------------------------------------------------------------
def dipole():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.4, 5.6); ax.set_ylim(-2.3, 2.3)
    axes2d(ax, (-1.0, 5.4), (-2.2, 2.2))
    d2, x = 1.0, 3.0
    p, m, P = np.array([0, d2]), np.array([0, -d2]), np.array([x, 0])
    arrow(ax, p, P, color=RED, lw=1.3, ls="--")
    arrow(ax, m, P, color=NAVY, lw=1.3, ls="--")
    # field of each charge at P, to scale with each other
    up = (P - p) / np.linalg.norm(P - p); um = (P - m) / np.linalg.norm(P - m)
    L = 1.5
    arrow(ax, P, P + L * up, color=RED, lw=2.0)
    arrow(ax, P, P - L * um, color=NAVY, lw=2.0)
    arrow(ax, P, P + L * (up - um), color=AMBER, lw=2.6, ms=18)
    charge(ax, *p, +1); charge(ax, *m, -1)
    point(ax, *P)
    lab(ax, -0.28, d2, "+q", color=RED, ha="right")
    lab(ax, -0.28, -d2, "−q", color=NAVY, ha="right")
    ax.annotate("", xy=(-0.95, d2), xytext=(-0.95, -d2),
                arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.0))
    lab(ax, -1.08, 0.3, "d", size=14, color=GRAY, ha="right")
    vec(ax, 1.75, 0.82, "R", "+", color=RED)
    vec(ax, 0.9, -0.95, "R", "−", color=NAVY)
    vec(ax, *(P + L * up + np.array([0.12, 0.05])), "E", "+", color=RED, ha="left")
    vec(ax, *(P - L * um + np.array([-0.05, 0.3])), "E", "−", color=NAVY, ha="right")
    vec(ax, *(P + L * (up - um) + np.array([0.15, 0])), "E", color=AMBER, ha="left")
    lab(ax, x + 0.1, 0.3, "(x, 0)", size=12.5, color=INK, ha="left", italic=False)
    save(fig, "L18-dipole.svg")


# ---------------------------------------------------------------------------
def line_charge():
    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.4, 5.6); ax.set_ylim(-3.0, 3.1)
    arrow(ax, (0, -2.9), (0, 3.0), color=AXIS, lw=1.2, ms=12)
    arrow(ax, (-0.6, 0), (5.3, 0), color=AXIS, lw=1.2, ms=12)
    lab(ax, 0.2, 3.0, "z", size=13, color=GRAY, ha="left", va="top")
    lab(ax, 5.3, 0.22, "ρ", size=13, color=GRAY, ha="right", va="bottom")
    h = 2.3
    ax.plot([0, 0], [-h, h], color=RED, lw=5, solid_capstyle="butt")
    for yy, txt in ((h, "L/2"), (-h, "−L/2")):
        ax.plot([-0.12, 0.12], [yy, yy], color=INK, lw=1.2)
        lab(ax, -0.22, yy, txt, size=13, color=INK, ha="right")
    lab(ax, -0.25, 0.85, "ρ", "ℓ", color=RED, ha="right")
    zp, P = 1.5, np.array([3.0, 0])
    src, img = np.array([0, zp]), np.array([0, -zp])
    ax.add_patch(Circle(src, 0.11, fc=AMBER, ec="none", zorder=5))
    ax.add_patch(Circle(img, 0.11, fc=AMBER, ec="none", zorder=5, alpha=0.55))
    lab(ax, 0.22, zp + 0.22, "dQ", size=14, color=AMBER, ha="left")
    lab(ax, -0.22, zp, "z′", size=13, color=AMBER, ha="right")
    arrow(ax, src, P, color=AMBER, lw=1.8)
    arrow(ax, img, P, color=AMBER, lw=1.2, ls="--")
    vec(ax, 1.65, 1.05, "R", color=AMBER)
    # dE from each element, and their sum along ρ
    u1 = (P - src) / np.linalg.norm(P - src); u2 = (P - img) / np.linalg.norm(P - img)
    L = 1.05
    arrow(ax, P, P + L * u1, color=NAVY, lw=2.0)
    arrow(ax, P, P + L * u2, color=NAVY, lw=1.4, ls="--")
    arrow(ax, P, P + L * (u1 + u2), color=GREEN, lw=2.6, ms=18)
    vec(ax, *(P + L * u1 + np.array([0.05, -0.28])), "dE", color=NAVY, ha="left")
    point(ax, *P)
    ax.annotate("", xy=(P[0], -0.45), xytext=(0, -0.45),
                arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.0))
    lab(ax, P[0] / 2 + 0.6, -0.68, "ρ", size=14, color=GRAY, va="top")
    save(fig, "L18-line-charge.svg")


if __name__ == "__main__":
    coulomb()
    three_charges()
    dipole()
    line_charge()
