#!/usr/bin/env python3
"""L25 figures: capacitance from the field.

    L25-parallel-plate.svg   two plates of area A, d apart, charged +Q and -Q,
                             with the uniform field between them
    L25-coax.svg             coaxial cross section: +Q on the inner conductor,
                             -Q on the shield, the radial field, and the
                             Gaussian cylinder of radius rho
    L25-two-layer.svg        parallel plates with two dielectric layers: the
                             same D in both, a larger E in the thin air layer

Labels are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l25_figures.py   ->   book/extras/viz/img/L25-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402
from l24_figures import lab, arrow  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL = "#e3edf6"      # dielectric
FILL2 = "#c9dcee"     # the higher-permittivity layer
METAL = "#9aa8b6"     # conductor
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def plates(ax, x0, x1, ytop, ybot, sign_top="+", sign_bot="−"):
    for y, s in ((ytop, sign_top), (ybot, sign_bot)):
        ax.add_patch(Rectangle((x0, y - 0.06), x1 - x0, 0.12, fc=METAL, ec=INK, lw=1.0))
        off = 0.22 if y == ytop else -0.22
        for x in np.linspace(x0 + 0.2, x1 - 0.2, 12):
            ax.text(x, y + off, s, color=RED if s == "+" else BLUE, fontsize=12,
                    ha="center", va="center")


# ---------------------------------------------------------------------------
def parallel_plate():
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.8, 6.4); ax.set_ylim(-0.45, 2.2)
    x0, x1, yb, yt = 0.0, 4.6, 0.0, 1.5
    ax.add_patch(Rectangle((x0, yb), x1 - x0, yt - yb, fc=FILL, ec="none"))
    plates(ax, x0, x1, yt, yb)
    for x in np.linspace(0.5, 4.1, 6):
        arrow(ax, x, yt - 0.12, x, yb + 0.12, color=NAVY, lw=1.8)
    lab(ax, 4.35, 0.75, "E", color=NAVY, italic=False, bold=True, ha="left")
    lab(ax, 0.15, 1.2, "ε", ha="left", size=14)
    ax.text(x1 + 0.3, yt, "+Q,  z = d", fontsize=13, ha="left", va="center")
    ax.text(x1 + 0.3, yb, "−Q,  z = 0", fontsize=13, ha="left", va="center")
    lab(ax, (x0 + x1) / 2, yt + 0.5, "area A", size=13, color=GRAY, italic=False)
    ax.annotate("", xy=(-0.35, yb), xytext=(-0.35, yt),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, -0.5, (yb + yt) / 2, "d", size=14, color=GRAY, ha="right")
    save(fig, "L25-parallel-plate.svg")


def coax():
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    ax.set_aspect("equal"); ax.axis("off")
    a, b, t = 0.55, 1.7, 0.18
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.1, 2.1)
    ax.add_patch(Circle((0, 0), b + t, fc=METAL, ec=INK, lw=1.2))
    ax.add_patch(Circle((0, 0), b, fc=FILL, ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), a, fc=METAL, ec=INK, lw=1.2))
    for th in np.linspace(0, 2 * np.pi, 14, endpoint=False):
        ax.text((a + 0.13) * np.cos(th), (a + 0.13) * np.sin(th), "+", color=RED,
                fontsize=10, ha="center", va="center")
        ax.text((b - 0.13) * np.cos(th + 0.22), (b - 0.13) * np.sin(th + 0.22), "−",
                color=BLUE, fontsize=11, ha="center", va="center")
    for th in np.linspace(0, 2 * np.pi, 8, endpoint=False) + np.pi / 8:
        arrow(ax, (a + 0.3) * np.cos(th), (a + 0.3) * np.sin(th),
              (b - 0.3) * np.cos(th), (b - 0.3) * np.sin(th), color=NAVY, lw=1.8, head=11)
    r = 1.1
    ax.add_patch(Circle((0, 0), r, fc="none", ec=AMBER, lw=1.6, ls="--"))
    # radii
    ax.plot([0, a * np.cos(np.pi)], [0, 0], color=INK, lw=1.0)
    lab(ax, -a / 2, 0.14, "a", size=14)
    ax.plot([0, b * np.cos(-np.pi / 2.6)], [0, b * np.sin(-np.pi / 2.6)], color=INK, lw=1.0)
    lab(ax, 0.82, -1.15, "b", size=14)
    ax.plot([0, r * np.cos(np.pi * 0.62)], [0, r * np.sin(np.pi * 0.62)], color=AMBER, lw=1.2)
    lab(ax, -0.5, 0.62, "ρ", size=14, color=AMBER)
    lab(ax, 1.2, 1.25, "ε", size=14)
    save(fig, "L25-coax.svg")


def two_layer():
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.0, 6.6); ax.set_ylim(-0.6, 2.3)
    x0, x1, yb, ym, yt = 0.0, 4.6, 0.0, 1.1, 1.7
    ax.add_patch(Rectangle((x0, yb), x1 - x0, ym - yb, fc=FILL2, ec="none"))
    ax.add_patch(Rectangle((x0, ym), x1 - x0, yt - ym, fc="#f6f9fc", ec="none"))
    ax.plot([x0, x1], [ym, ym], color=INK, lw=1.0, ls="--")
    plates(ax, x0, x1, yt, yb)
    for x in np.linspace(0.5, 3.6, 5):        # long arrows: the strong field in air
        arrow(ax, x, yt - 0.1, x, ym + 0.02, color=NAVY, lw=2.4, head=12)
        arrow(ax, x, ym - 0.06, x, ym - 0.36, color=NAVY, lw=1.4, head=9)
    lab(ax, 4.0, 1.4, "E", "1", color=NAVY, italic=False, bold=True, ha="left")
    lab(ax, 4.0, 0.85, "E", "2", color=NAVY, italic=False, bold=True, ha="left")
    ax.text(x1 + 0.35, (ym + yt) / 2, "air,  ε₁,  d₁", fontsize=13, ha="left", va="center")
    ax.text(x1 + 0.35, (yb + ym) / 2, "glass,  ε₂,  d₂", fontsize=13, ha="left", va="center")
    lab(ax, -0.25, 1.95, "+Q", size=13, ha="right", italic=False)
    lab(ax, -0.25, -0.25, "−Q", size=13, ha="right", italic=False)
    save(fig, "L25-two-layer.svg")


if __name__ == "__main__":
    parallel_plate()
    coax()
    two_layer()
