#!/usr/bin/env python3
"""L10 figures: what the Smith chart plots.

    L10-mapping.svg     the right half of the z plane (constant-r lines and
                        constant-x lines) and the same lines mapped into the
                        Gamma plane by Gamma = (z - 1)/(z + 1)
    L10-landmarks.svg   the chart with the short, the open, the match, and
                        the example load z = 1.5 + j1.2 with its |Gamma| circle

    python3 scripts/graphics/l10_figures.py   ->   book/extras/viz/img/L10-*.svg
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

from l10_smith_base import (chart, gamma, gamma_circle, dot, r_circle, x_arc, save,
                            NAVY, BLUE, AMBER, GREEN, RED, GRAY, INK)


def mapping():
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.4), gridspec_kw={"width_ratios": [1, 1.05]})
    # z plane: constant r vertical lines, constant x horizontal lines
    a.set_xlim(-0.3, 3.2); a.set_ylim(-2.4, 2.4); a.set_aspect("equal")
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
    a.spines["left"].set_position(("data", 0)); a.spines["bottom"].set_position(("data", 0))
    a.spines["left"].set_color(GRAY); a.spines["bottom"].set_color(GRAY)
    a.set_xticks([]); a.set_yticks([])
    for r, c in ((0.5, BLUE), (1, NAVY), (2, BLUE)):
        a.plot([r, r], [-2.3, 2.3], color=c, lw=2.2 if r == 1 else 1.5)
        a.text(r, -2.45, f"{r:g}", color=c, fontsize=11, ha="center", va="top")
    for x, c in ((1, RED), (-1, AMBER)):
        a.plot([0, 3.1], [x, x], color=c, lw=1.5)
        a.text(3.15, x, f"x = {x:+g}", color=c, fontsize=11, ha="left", va="center")
    a.plot(1.5, 1.2, "o", color=GREEN, ms=7)
    a.text(1.6, 1.4, "z = 1.5 + j1.2", color=GREEN, fontsize=11)
    a.text(3.15, -0.15, "r", color=GRAY, fontsize=13, style="italic", va="top")
    a.text(-0.08, -2.45, "r =", color=GRAY, fontsize=11, ha="right", va="top")
    a.text(0.08, 2.35, "x", color=GRAY, fontsize=13, style="italic", va="top")
    a.set_title("z plane", fontsize=13, color=INK)

    chart(b, labels=False)
    for r, c in ((0.5, BLUE), (1, NAVY), (2, BLUE)):
        r_circle(b, r, c, lw=2.2 if r == 1 else 1.5)
    x_arc(b, 1, RED, lw=1.5); x_arc(b, -1, AMBER, lw=1.5)
    g = gamma(1.5 + 1.2j)
    dot(b, g, GREEN)
    b.set_title("Γ plane: the Smith chart", fontsize=13, color=INK)
    fig.subplots_adjust(wspace=0.25)
    save(fig, "L10-mapping.svg")


def landmarks():
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    chart(ax)
    g = gamma(1.5 + 1.2j)
    gamma_circle(ax, abs(g))
    dot(ax, -1 + 0j, RED, "short", dx=0.06, dy=-0.09)
    dot(ax, 1 + 0j, RED, "open", dx=-0.06, dy=-0.09, ha="right")
    dot(ax, 0j, NAVY, "match", dx=0.04, dy=-0.08)
    dot(ax, g, GREEN, "load", dx=0.06, dy=0.04)
    s = (1 + abs(g)) / (1 - abs(g))
    sg = gamma(s)
    dot(ax, sg, AMBER, f"r = {s:.2f}", dx=0.0, dy=-0.2, ha="center", size=5, fs=10)
    ax.text(0, 1.06, "x > 0", color=GRAY, fontsize=11, ha="center", va="bottom")
    ax.text(0, -1.06, "x < 0", color=GRAY, fontsize=11, ha="center", va="top")
    save(fig, "L10-landmarks.svg")


if __name__ == "__main__":
    mapping()
    landmarks()
