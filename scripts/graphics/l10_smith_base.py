#!/usr/bin/env python3
"""Shared Smith chart drawing for the L10-L13 figures.

Every chart here is the Gamma plane with the impedance grid. An admittance
is read off the same grid at -Gamma, the point opposite through the center,
which is how L11 teaches it; there is no second, mirrored grid. Labels are
plain Unicode (CLAUDE.md), and the chart carries only a minimal key: the
lesson text explains it.

Imported by l10_figures.py ... l13_figures.py; it writes nothing itself.
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

NAVY, BLUE, AMBER, GREEN, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#1d7a4d", "#b01e24", "#5b6573", "#15202b"
GRID = "#cfdbe7"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"
plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})

R_VALUES = (0.2, 0.5, 1, 2, 5)
X_VALUES = (0.2, 0.5, 1, 2, 5)


def gamma(z):
    return (z - 1) / (z + 1)


def zof(g):
    return (1 + g) / (1 - g)


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.06, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def chart(ax, labels=True, r_color=GRID, x_color=GRID, lw=0.9):
    """Unit circle, constant-r circles, constant-x arcs, the real axis."""
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.12, 1.12)
    clip = Circle((0, 0), 1, transform=ax.transData)
    for r in R_VALUES:
        c = Circle((r / (1 + r), 0), 1 / (1 + r), fill=False, ec=r_color, lw=lw)
        ax.add_patch(c); c.set_clip_path(clip)
    for x in X_VALUES:
        for s in (1, -1):
            c = Circle((1, s / x), 1 / x, fill=False, ec=x_color, lw=lw)
            ax.add_patch(c); c.set_clip_path(clip)
    ax.add_patch(Circle((0, 0), 1, fill=False, ec="#8fa5bb", lw=1.3))
    ax.plot([-1, 1], [0, 0], color="#8fa5bb", lw=1.1)
    if labels:
        for r in R_VALUES:
            ax.text((r - 1) / (r + 1), 0.025, f"{r:g}", fontsize=9, color=GRAY, ha="center", va="bottom")
    return ax


def r_circle(ax, r, color, lw=2.2, ls="-"):
    ax.add_patch(Circle((r / (1 + r), 0), 1 / (1 + r), fill=False, ec=color, lw=lw, ls=ls))


def x_arc(ax, x, color, lw=2.2, ls="-"):
    clip = Circle((0, 0), 1, transform=ax.transData)
    c = Circle((1, 1 / x), 1 / abs(x), fill=False, ec=color, lw=lw, ls=ls)
    ax.add_patch(c); c.set_clip_path(clip)


def gamma_circle(ax, mag, color=NAVY, lw=1.4, ls="--"):
    ax.add_patch(Circle((0, 0), mag, fill=False, ec=color, lw=lw, ls=ls))


def dot(ax, g, color, label=None, dx=0.05, dy=0.05, ha="left", size=7, fs=12):
    ax.plot(g.real, g.imag, "o", color=color, ms=size, zorder=5)
    if label:
        ax.text(g.real + dx, g.imag + dy, label, color=color, fontsize=fs, ha=ha, va="center", zorder=6)


def rotate_arc(ax, g0, turns_lambda, color=GREEN, lw=2.6, arrow=True):
    """Clockwise rotation of g0 by 2*beta*d, with d = turns_lambda wavelengths."""
    th0 = np.angle(g0)
    th = th0 - 4 * np.pi * np.linspace(0, turns_lambda, 200)
    m = abs(g0)
    ax.plot(m * np.cos(th), m * np.sin(th), color=color, lw=lw, solid_capstyle="round")
    if arrow:
        ax.add_patch(FancyArrowPatch((m * np.cos(th[-6]), m * np.sin(th[-6])),
                                     (m * np.cos(th[-1]), m * np.sin(th[-1])),
                                     arrowstyle="-|>", mutation_scale=14, color=color, lw=0))
    return m * np.exp(1j * th[-1])


def path_const_r(ax, r, x0, x1, color, lw=2.6):
    """Move along the constant-r circle from x0 to x1 (a series reactance)."""
    xs = np.linspace(x0, x1, 200)
    g = gamma(r + 1j * xs)
    ax.plot(g.real, g.imag, color=color, lw=lw, solid_capstyle="round")
    ax.add_patch(FancyArrowPatch((g[-6].real, g[-6].imag), (g[-1].real, g[-1].imag),
                                 arrowstyle="-|>", mutation_scale=14, color=color, lw=0))
