#!/usr/bin/env python3
"""L19 figures: the field of charge distributions, by direct integration.

    L19-ring.svg          a ring of line charge, one element and the element
                          opposite it, and their fields on the axis
    L19-disk.svg          a disk of surface charge cut into rings of width dρ′
    L19-disk-field.svg    the disk's field on its axis, against the infinite
                          sheet and the point charge it approaches
    L19-shell.svg         a spherical shell in cross section: the ring at θ′,
                          and the triangle the law of cosines solves
    L19-sphere-field.svg  the field of a uniformly charged shell and of a
                          uniformly charged solid sphere, against r/a

Labels are plain Unicode (see CLAUDE.md); vectors are bold and upright,
scalars italic. The lesson text does the explaining.

    python3 scripts/graphics/l19_figures.py   ->   book/extras/viz/img/L19-*.svg
"""

from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent))
from l18_figures import (lab, vec, arrow, point, save,  # noqa: E402
                         NAVY, BLUE, AMBER, RED, GRAY, INK, GREEN, AXIS)

FILL = "#f6dcdd"      # surface charge


def P(x, y, z):
    """Oblique projection: x comes toward the viewer, down and to the left."""
    return np.array([y - 0.42 * x, z - 0.30 * x])


def axes3d(ax, L=2.6, zmax=3.2):
    for end, name, off in (((L, 0, 0), "x", (-0.12, -0.12)),
                           ((0, L, 0), "y", (0.05, -0.25)),
                           ((0, 0, zmax), "z", (0.15, -0.05))):
        arrow(ax, P(0, 0, 0), P(*end), color=AXIS, lw=1.2, ms=12)
        lab(ax, *(P(*end) + np.array(off)), name, size=13, color=GRAY, ha="left", va="top")


def frame(figsize, xlim, ylim):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    return fig, ax


# ---------------------------------------------------------------------------
def ring():
    fig, ax = frame((6.0, 4.9), (-2.2, 3.0), (-1.5, 3.4))
    axes3d(ax, L=2.4, zmax=3.3)
    a, h = 1.6, 2.2
    ph = np.linspace(0, 2 * np.pi, 300)
    pts = np.array([P(a * np.cos(t), a * np.sin(t), 0) for t in ph])
    ax.plot(pts[:, 0], pts[:, 1], color=RED, lw=3.2)
    Pz = P(0, 0, h)
    f1, f2 = 0.45 * np.pi, 0.45 * np.pi + np.pi
    e1 = P(a * np.cos(f1), a * np.sin(f1), 0); e2 = P(a * np.cos(f2), a * np.sin(f2), 0)
    ax.add_patch(Circle(e1, 0.1, fc=AMBER, ec="none", zorder=5))
    ax.add_patch(Circle(e2, 0.1, fc=AMBER, ec="none", zorder=5, alpha=0.55))
    arrow(ax, e1, Pz, color=AMBER, lw=1.8)
    arrow(ax, e2, Pz, color=AMBER, lw=1.2, ls="--")
    vec(ax, *(0.5 * (e1 + Pz) + np.array([0.28, 0.0])), "R", color=AMBER, ha="left")
    lab(ax, *(e1 + np.array([0.15, -0.22])), "dQ", size=14, color=AMBER, ha="left")
    # radius and angle
    ax.plot(*zip(P(0, 0, 0), e1), color=INK, lw=1.0)
    lab(ax, *(0.5 * (P(0, 0, 0) + e1) + np.array([-0.05, 0.16])), "a", size=14, color=INK)
    arc = np.array([P(0.55 * np.cos(t), 0.55 * np.sin(t), 0) for t in np.linspace(0, f1, 40)])
    ax.plot(arc[:, 0], arc[:, 1], color=INK, lw=1.0)
    lab(ax, *(P(0.75 * np.cos(f1 / 2), 0.75 * np.sin(f1 / 2), 0) + np.array([0.05, -0.2])), "φ′", size=13, color=INK)
    # field point, height, and the two dE
    point(ax, *Pz)
    lab(ax, -0.15, h / 2 + 0.2, "h", size=14, color=GRAY, ha="right")
    u1 = (P(0, 0, h) - P(a * np.cos(f1), a * np.sin(f1), 0))
    u2 = (P(0, 0, h) - P(a * np.cos(f2), a * np.sin(f2), 0))
    d1 = np.array([0, 0, h]) - np.array([a * np.cos(f1), a * np.sin(f1), 0])
    d2 = np.array([0, 0, h]) - np.array([a * np.cos(f2), a * np.sin(f2), 0])
    s = 0.75 / np.linalg.norm(d1)
    q1, q2 = P(*(s * d1)), P(*(s * d2))
    arrow(ax, Pz, Pz + q1, color=NAVY, lw=2.0)
    arrow(ax, Pz, Pz + q2, color=NAVY, lw=1.4, ls="--")
    arrow(ax, Pz, Pz + q1 + q2, color=GREEN, lw=2.6, ms=18)
    vec(ax, *(Pz + q1 + np.array([-0.1, 0.05])), "dE", color=NAVY, ha="right")
    lab(ax, *(P(a * np.cos(0.15 * np.pi), a * np.sin(0.15 * np.pi), 0) + np.array([0.0, -0.3])), "ρ", "ℓ", color=RED, va="top")
    save(fig, "L19-ring.svg")


# ---------------------------------------------------------------------------
def disk():
    fig, ax = frame((6.0, 4.9), (-2.2, 3.0), (-1.5, 3.4))
    a, h, rp, dr = 1.7, 2.3, 1.05, 0.22
    ph = np.linspace(0, 2 * np.pi, 300)
    outer = np.array([P(a * np.cos(t), a * np.sin(t), 0) for t in ph])
    ax.add_patch(Polygon(outer, closed=True, fc=FILL, ec=RED, lw=1.8))
    ring_o = np.array([P((rp + dr) * np.cos(t), (rp + dr) * np.sin(t), 0) for t in ph])
    ring_i = np.array([P(rp * np.cos(t), rp * np.sin(t), 0) for t in ph])
    ax.add_patch(Polygon(np.vstack([ring_o, ring_i[::-1]]), closed=True, fc="#e7a9ac", ec=RED, lw=0.8))
    axes3d(ax, L=2.5, zmax=3.6)
    Pz = P(0, 0, h)
    f1 = 0.45 * np.pi
    e1 = P((rp + dr / 2) * np.cos(f1), (rp + dr / 2) * np.sin(f1), 0)
    ax.add_patch(Circle(e1, 0.09, fc=AMBER, ec="none", zorder=5))
    arrow(ax, e1, Pz, color=AMBER, lw=1.8)
    vec(ax, *(0.5 * (e1 + Pz) + np.array([0.25, 0.0])), "R", color=AMBER, ha="left")
    ax.plot([0, -rp], [0, 0], color=INK, lw=1.0)
    lab(ax, -rp / 2, 0.16, "ρ′", size=13, color=INK)
    lab(ax, -rp - dr / 2, -0.2, "dρ′", size=13, color=INK, va="top")
    lab(ax, -a - 0.1, 0, "a", size=14, color=RED, ha="right")
    point(ax, *Pz)
    lab(ax, -0.15, h / 2 + 0.25, "h", size=14, color=GRAY, ha="right")
    arrow(ax, Pz, Pz + np.array([0, 0.75]), color=GREEN, lw=2.6, ms=18)
    vec(ax, *(Pz + np.array([-0.15, 0.5])), "E", color=GREEN, ha="right")
    lab(ax, *(P(a, 0, 0) + np.array([0.3, -0.12])), "ρ", "s", color=RED, ha="left")
    save(fig, "L19-disk.svg")


# ---------------------------------------------------------------------------
def style(ax):
    ax.grid(True, color="#e3edf6", lw=1.0)
    for sname in ("top", "right"):
        ax.spines[sname].set_visible(False)
    for sname in ("left", "bottom"):
        ax.spines[sname].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=11)


def disk_field():
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    u = np.linspace(0.001, 4, 500)                    # h / a
    ax.plot(u, 1 - u / np.sqrt(1 + u ** 2), color=NAVY, lw=2.8, label="disk of radius a")
    ax.plot(u, np.ones_like(u), color=AMBER, lw=1.6, ls="--", label="infinite sheet")
    up = u[u > 0.35]
    ax.plot(up, 0.5 / up ** 2, color=GREEN, lw=1.6, ls="--", label="point charge, same total charge")
    ax.set_xlim(0, 4); ax.set_ylim(0, 1.15)
    ax.set_xlabel("height above the disk, h/a", color=GRAY, fontsize=12)
    ax.set_ylabel("field ÷ sheet field", color=GRAY, fontsize=12)
    style(ax)
    ax.legend(frameon=False, fontsize=12, loc="upper right")
    save(fig, "L19-disk-field.svg")


# ---------------------------------------------------------------------------
def shell():
    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-2.6, 2.9); ax.set_ylim(-2.2, 3.9)
    a, r, th = 1.6, 3.3, np.radians(50)
    ax.add_patch(Circle((0, 0), a, fc=FILL, ec=RED, lw=2.4))
    # the ring of charge at θ′ (seen edge-on as an ellipse) and its width
    zr, xr = a * np.cos(th), a * np.sin(th)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(xr * np.cos(t), zr + 0.16 * xr * np.sin(t), color=RED, lw=1.0, ls=":")
    arrow(ax, (0, -2.1), (0, 3.8), color=AXIS, lw=1.2, ms=12)
    lab(ax, 0.15, 3.8, "z", size=13, color=GRAY, ha="left", va="top")
    src = np.array([xr, zr]); Pz = np.array([0, r])
    ax.plot([0, src[0]], [0, src[1]], color=INK, lw=1.2)
    lab(ax, 0.5 * xr + 0.18, 0.5 * zr - 0.08, "a", size=14, color=INK, ha="left")
    arc = np.linspace(np.pi / 2, np.pi / 2 - th, 40)
    ax.plot(0.5 * np.cos(arc), 0.5 * np.sin(arc), color=INK, lw=1.0)
    lab(ax, 0.32, 0.75, "θ′", size=13, color=INK)
    ax.add_patch(Circle(src, 0.1, fc=AMBER, ec="none", zorder=5))
    lab(ax, src[0] + 0.15, src[1] - 0.1, "dQ", size=14, color=AMBER, ha="left", va="top")
    arrow(ax, src, Pz, color=AMBER, lw=1.8)
    vec(ax, 0.5 * (src[0] + Pz[0]) + 0.2, 0.5 * (src[1] + Pz[1]) + 0.12, "R", color=AMBER, ha="left")
    point(ax, *Pz)
    lab(ax, -0.15, r, "(0, 0, r)", size=12.5, color=INK, ha="right", italic=False)
    ax.annotate("", xy=(-2.0, r), xytext=(-2.0, 0),
                arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.0))
    ax.plot([-2.1, 0], [0, 0], color=GRAY, lw=0.8, ls=":")
    ax.plot([-2.1, -1.2], [r, r], color=GRAY, lw=0.8, ls=":")
    lab(ax, -2.13, 0.5 * r, "r", size=14, color=GRAY, ha="right")
    lab(ax, -1.25, -1.35, "ρ", "s", color=RED, ha="right")
    save(fig, "L19-shell.svg")


def sphere_field():
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    u = np.linspace(0, 4, 800)                        # r / a
    solid = np.where(u < 1, u, 1 / np.maximum(u, 1e-9) ** 2)
    shellE = np.where(u < 1, 0, 1 / np.maximum(u, 1e-9) ** 2)
    ax.plot(u, solid, color=NAVY, lw=2.8, label="solid sphere, uniform charge")
    ax.plot(u[u < 1], shellE[u < 1], color=RED, lw=2.0, ls="--", label="shell, same total charge")
    ax.plot(u[u > 1], shellE[u > 1], color=RED, lw=2.0, ls="--")
    ax.plot([1, 1], [0, 1], color=RED, lw=1.0, ls=":")
    ax.axvline(1, color="#c7d2e0", lw=1.0)
    ax.text(1.04, 1.05, "r = a", fontsize=12, color=GRAY, ha="left", va="center", fontstyle="italic")
    ax.set_xlim(0, 4); ax.set_ylim(-0.03, 1.15)
    ax.set_xlabel("distance from the center, r/a", color=GRAY, fontsize=12)
    ax.set_ylabel("field ÷ field at r = a", color=GRAY, fontsize=12)
    style(ax)
    ax.legend(frameon=False, fontsize=12, loc="upper right")
    save(fig, "L19-sphere-field.svg")


if __name__ == "__main__":
    ring()
    disk()
    disk_field()
    shell()
    sphere_field()
