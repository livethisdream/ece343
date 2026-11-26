#!/usr/bin/env python3
"""L10 figures: what the Smith chart plots.

    L10-mapping.svg     the right half of the z plane (constant-r lines and
                        constant-x lines) and the same lines mapped into the
                        Gamma plane by Gamma = (z - 1)/(z + 1)
    L10-landmarks.svg   the chart with the short, the open, the match, and
                        the example load z = 1.5 + j1.2 with its |Gamma| circle
    L10-paper-chart.svg the parts of the printed chart: r values on the real
                        axis, x values at the rim, the three rim scales, and
                        the radial ruler for |Gamma| and VSWR

    python3 scripts/graphics/l10_figures.py   ->   book/extras/viz/img/L10-*.svg
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from l10_smith_base import (X_VALUES, chart, gamma, gamma_circle, dot, r_circle, x_arc, save,
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
    for r, c in ((0.5, BLUE), (1, NAVY), (2, BLUE)):
        b.text((r - 1) / (r + 1) + 0.03, -0.03, f"{r:g}", color=c, fontsize=11, ha="left", va="top")
    b.text(-1.03, -0.03, "r =", color=GRAY, fontsize=11, ha="right", va="top")
    b.text(0, 1.04, "x = +1", color=RED, fontsize=11, ha="center", va="bottom")
    b.text(0, -1.04, "x = \u22121", color=AMBER, fontsize=11, ha="center", va="top")
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


def paper_chart():
    """The scales of the printed chart (handouts/SmithChart_blank.pdf)."""
    fig, ax = plt.subplots(figsize=(6.4, 7.8))
    chart(ax)
    ax.set_xlim(-1.68, 1.68); ax.set_ylim(-2.45, 1.68)
    # x values where each arc meets the rim
    for x in X_VALUES:
        for s in (1, -1):
            g = gamma(1j * s * x)
            ax.text(0.9 * g.real, 0.9 * g.imag, f"{s * x:+g}".replace("-", "\u2212"),
                    fontsize=9, color=RED, ha="center", va="center")
    # the three rim scales, inside to outside as on the handout
    rings = ((1.2, GREEN), (1.41, AMBER), (1.62, NAVY))
    for rad, c in rings:
        ax.add_patch(Circle((0, 0), rad, fill=False, ec=c, lw=1.1))
    def tick(rad, deg, text, c):
        th = np.radians(deg)
        ax.plot([rad * np.cos(th), (rad - 0.03) * np.cos(th)],
                [rad * np.sin(th), (rad - 0.03) * np.sin(th)], color=c, lw=1.1)
        ax.text((rad - 0.105) * np.cos(th), (rad - 0.105) * np.sin(th), text,
                fontsize=8, color=c, ha="center", va="center")
    for deg in (0, 45, 90, 135, 180, -135, -90, -45):
        tick(rings[0][0], deg, f"{deg}\u00b0".replace("-", "\u2212"), GREEN)
    for k in range(4):                       # 1/8 wavelength steps
        wl = k / 8
        tick(rings[2][0], 180 - 720 * wl, f"{wl:g}", NAVY)      # toward generator, clockwise
        tick(rings[1][0], 180 + 720 * wl, f"{wl:g}", AMBER)     # toward load, counterclockwise
    # the example load and the ray that carries it out to the scales
    g = gamma(1.5 + 1.2j)
    gamma_circle(ax, abs(g))
    th = np.angle(g)
    ax.plot([0, rings[2][0] * np.cos(th)], [0, rings[2][0] * np.sin(th)], color=GRAY, lw=1.0)
    dot(ax, g, GREEN)
    # the radial ruler under the chart: |Gamma| and VSWR against distance from the center
    y0 = -1.95
    ax.plot([-1, 0], [y0, y0], color=INK, lw=1.2)
    for m in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        ax.plot([-m, -m], [y0, y0 - 0.04], color=INK, lw=1.0)
        ax.text(-m, y0 - 0.07, f"{m:g}", fontsize=9, color=INK, ha="center", va="top")
    for v in (1, 1.5, 2, 3, 5, 10):
        m = (v - 1) / (v + 1)
        ax.plot([-m, -m], [y0, y0 + 0.04], color=INK, lw=1.0)
        ax.text(-m, y0 + 0.07, f"{v:g}", fontsize=9, color=INK, ha="center", va="bottom")
    ax.text(-1, y0 + 0.07, "\u221e", fontsize=10, color=INK, ha="center", va="bottom")
    ax.text(0.06, y0 + 0.11, "VSWR", fontsize=10, color=INK, ha="left", va="center")
    ax.text(0.06, y0 - 0.11, "|\u0393|", fontsize=10, color=INK, ha="left", va="center")
    for xx in (0, -abs(g)):
        ax.plot([xx, xx], [0 if xx == 0 else 0, y0], color=GRAY, lw=0.8, ls=":")
    ax.plot(-abs(g), 0, "o", color=NAVY, ms=4)
    # key
    key = ((NAVY, "outer scale: wavelengths toward generator"),
           (AMBER, "middle scale: wavelengths toward load"),
           (GREEN, "inner scale: angle of \u0393"),
           (RED, "x values, at the rim"))
    for i, (c, t) in enumerate(key):
        ax.text(0.42, -1.8 - 0.14 * i, t, fontsize=9.5, color=c, ha="left", va="center")
    save(fig, "L10-paper-chart.svg")


if __name__ == "__main__":
    mapping()
    landmarks()
    paper_chart()
