#!/usr/bin/env python3
"""L32 figures: the Magnetostatics Lab's bench setup.

    L32-setup.svg   side view of the coil wound on its tube, the Hall sensor
                    on the coil's axis at distance z, and the ruler it slides on

Labels are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l32_figures.py   ->   book/extras/viz/img/L32-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402
from l24_figures import lab, arrow  # noqa: E402

NAVY, AMBER, GRAY, INK = "#004a85", "#8a5a00", "#5b6573", "#15202b"
FILL = "#e3edf6"      # the tube
COPPER = "#c98a4b"    # the winding
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


def setup():
    """Units are centimeters: tube radius 2, coil band 1 cm wide at z = 0."""
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    # the tube, seen from the side; it ends at the coil
    ax.add_patch(Rectangle((-4.0, -2.0), 4.5, 4.0, facecolor=FILL, edgecolor=GRAY, lw=1.2))
    # the winding: a band at the top and bottom of the tube's outline
    for y0 in (2.0, -2.35):
        ax.add_patch(Rectangle((-0.5, y0), 1.0, 0.35, facecolor=COPPER, edgecolor=AMBER, lw=1.0))
    ax.plot([0, 0], [-2.6, 2.6], color=AMBER, lw=1.0, ls=":")          # plane of the coil
    # the axis
    ax.plot([-4.3, 9.3], [0, 0], color=GRAY, lw=1.0, ls="--")
    lab(ax, 9.45, 0.0, "z", size=14, ha="left")
    # the sensor on the axis
    zs = 5.0
    ax.add_patch(Rectangle((zs - 0.15, -0.45), 0.3, 0.9, facecolor=INK, edgecolor=INK))
    ax.text(zs, 0.75, "Hall sensor", ha="center", va="bottom", fontsize=12, color=INK)
    # the ruler
    ax.add_patch(Rectangle((-0.3, -3.6), 9.0, 0.5, facecolor="white", edgecolor=GRAY, lw=1.0))
    for k in range(0, 9):
        ax.plot([k, k], [-3.1, -3.3], color=GRAY, lw=1.0)
        ax.text(k, -3.75, str(k), ha="center", va="top", fontsize=10, color=GRAY)
    ax.text(8.85, -3.35, "cm", ha="left", va="center", fontsize=10, color=GRAY)
    # dimensions: radius a and distance z
    arrow(ax, -2.6, 0.0, -2.6, 2.0, color=NAVY, lw=1.6, head=10)
    lab(ax, -2.85, 1.0, "a", size=14, color=NAVY, ha="right")
    arrow(ax, 0.0, -1.2, zs, -1.2, color=NAVY, lw=1.6, head=10)
    lab(ax, zs / 2, -1.55, "z", size=14, color=NAVY, va="top")
    # the field on the axis
    arrow(ax, 1.4, 0.0, 3.2, 0.0, color=NAVY, lw=2.4, head=14)
    lab(ax, 2.3, 0.7, "B", "z", size=14, color=NAVY, italic=False, bold=True)
    ax.text(0.0, 2.75, "N turns", ha="center", va="bottom", fontsize=12, color=AMBER)
    ax.set_xlim(-4.5, 10.0)
    ax.set_ylim(-4.3, 3.4)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "L32-setup.svg")


if __name__ == "__main__":
    setup()
