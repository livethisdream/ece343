#!/usr/bin/env python3
"""L35 figures: decoupling Maxwell's equations.

    L35-coupling.svg    the two curl equations as a loop, E feeding H and H
                        feeding E, beside the telegrapher's equations of
                        Lesson 4 as the same loop, V feeding I and I feeding V

Labels are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l35_figures.py   ->   book/extras/viz/img/L35-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, AMBER, GRAY, INK = "#004a85", "#8a5a00", "#5b6573", "#15202b"
FILL = "#e3edf6"
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


def node(ax, x, y, text, color):
    ax.add_patch(FancyBboxPatch((x - 0.55, y - 0.32), 1.1, 0.64,
                                boxstyle="round,pad=0.04,rounding_size=0.12",
                                fc=FILL, ec=color, lw=1.6))
    ax.text(x, y, text, ha="center", va="center", fontsize=19, color=color,
            fontweight="bold")


def loop(ax, x0, top, bottom, color):
    """Two curved arrows between nodes at (x0 - 1.1, y) and (x0 + 1.1, y)."""
    y = 0.0
    a = FancyArrowPatch((x0 - 0.5, y + 0.36), (x0 + 0.5, y + 0.36),
                        connectionstyle="arc3,rad=-0.55", arrowstyle="-|>",
                        mutation_scale=14, color=color, lw=1.6)
    b = FancyArrowPatch((x0 + 0.5, y - 0.36), (x0 - 0.5, y - 0.36),
                        connectionstyle="arc3,rad=-0.55", arrowstyle="-|>",
                        mutation_scale=14, color=color, lw=1.6)
    ax.add_patch(a); ax.add_patch(b)
    ax.text(x0, y + 1.0, top, ha="center", va="center", fontsize=13, color=GRAY)
    ax.text(x0, y - 1.0, bottom, ha="center", va="center", fontsize=13, color=GRAY)


def coupling():
    fig, ax = plt.subplots(figsize=(8.2, 2.9))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.9, 8.1); ax.set_ylim(-1.45, 1.75)
    # transmission line, Lesson 4
    node(ax, 0.3, 0.0, "V", AMBER); node(ax, 2.9, 0.0, "I", AMBER)
    loop(ax, 1.6, "R′ + jωL′", "G′ + jωC′", AMBER)
    ax.text(1.6, 1.55, "line (Lesson 4)", ha="center", fontsize=13, color=AMBER)
    # source-free region, today
    node(ax, 4.9, 0.0, "E", NAVY); node(ax, 7.5, 0.0, "H", NAVY)
    loop(ax, 6.2, "jωμ", "jωε", NAVY)
    ax.text(6.2, 1.55, "fields (today)", ha="center", fontsize=13, color=NAVY)
    save(fig, "L35-coupling.svg")


if __name__ == "__main__":
    coupling()
