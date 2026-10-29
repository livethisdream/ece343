#!/usr/bin/env python3
"""L13 figures: single-stub matching.

    L13-stub-tuner.svg   the circuit: a line of length d from the load, then a
                         shunt stub of length l, shorted or open at its end
    L13-stub-match.svg   left: y_L = 1.153 - j0.609 (read at -Gamma) rotated
                         0.0189 wavelength to 1 - j0.585, then the stub's
                         +j0.585 moves it to the center; right: the stub
                         itself, from the short (y infinite) or the open
                         (y = 0) around the outer circle to +j0.585

    python3 scripts/graphics/l13_figures.py   ->   book/extras/viz/img/L13-*.svg
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

from l10_smith_base import (chart, gamma, gamma_circle, dot, rotate_arc, path_const_r, r_circle,
                            save, NAVY, GREEN, AMBER, RED, BLUE, GRAY, INK)


def stub_tuner():
    fig, ax = plt.subplots(figsize=(9.4, 3.6))
    ax.set_aspect("equal"); ax.axis("off")
    yt, yb = 2.0, 1.2
    # main line: source side at left, load at right
    for y in (yt, yb):
        ax.plot([0.4, 8.0], [y, y], color=NAVY, lw=4.0, solid_capstyle="butt")
    ax.add_patch(plt.Rectangle((8.2, yb - 0.05), 0.5, yt - yb + 0.1, fc="white", ec=INK, lw=1.6))
    ax.plot([8.0, 8.45], [yt, yt], color=INK, lw=1.6); ax.plot([8.0, 8.45], [yb, yb], color=INK, lw=1.6)
    ax.text(8.9, (yt + yb) / 2, "load", fontsize=13, va="center")
    ax.text(0.3, (yt + yb) / 2, "to source", fontsize=12, va="center", ha="right", color=GRAY)
    # stub at x = 3.6, hanging down
    xs = 3.6
    for x in (xs, xs + 0.6):
        ax.plot([x, x], [yb, -1.6], color=AMBER, lw=4.0, solid_capstyle="butt")
    ax.plot([xs - 0.1, xs + 0.7], [-1.6, -1.6], color=INK, lw=3.0)
    ax.text(xs + 0.85, -1.6, "short or open", fontsize=12, va="center", color=GRAY)
    ax.plot([xs + 0.6, xs + 0.6], [yt, yb], color=AMBER, lw=1.2, ls=":")
    # dimensions
    ax.annotate("", xy=(8.0, 2.55), xytext=(xs + 0.3, 2.55), arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.2))
    ax.text((8.0 + xs + 0.3) / 2, 2.7, "d", fontsize=15, style="italic", ha="center", color=GRAY)
    ax.annotate("", xy=(xs - 0.4, -1.6), xytext=(xs - 0.4, yb), arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.2))
    ax.text(xs - 0.55, (yb - 1.6) / 2, "ℓ", fontsize=16, style="italic", ha="right", color=GRAY)
    ax.set_xlim(-1.3, 10.0); ax.set_ylim(-2.0, 3.0)
    save(fig, "L13-stub-tuner.svg")


def stub_match():
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.8))
    zl = (33.9 + 17.9j) / 50
    gy = -gamma(zl)                       # the load admittance, read on the same grid
    chart(a); r_circle(a, 1, BLUE, lw=1.8); gamma_circle(a, abs(gy))
    gi = rotate_arc(a, gy, 0.0189)
    path_const_r(a, 1, -0.585, 0.0, AMBER)
    dot(a, gy, NAVY, "load", dx=0.06, dy=-0.02)
    dot(a, gi, GREEN, "1 − j0.585", dx=-0.04, dy=-0.13, ha="right")
    dot(a, 0j, AMBER, "match", dx=-0.04, dy=0.1, ha="right")
    a.set_title("the load, read as admittance", fontsize=12.5, color=INK)

    chart(b)
    target = gamma(0.585j)                # +j0.585 on the outer circle
    th_t = np.angle(target)
    for start, color, label, dy in ((0.0, RED, "short: 0.334λ", 0.0), (np.pi, GREEN, "open: 0.084λ", 0.0)):
        sweep = (start - th_t) % (2 * np.pi)
        th = start - np.linspace(0, sweep, 300)
        b.plot(np.cos(th) * 0.97, np.sin(th) * 0.97, color=color, lw=2.6)
        b.add_patch(FancyArrowPatch((0.97 * np.cos(th[-8]), 0.97 * np.sin(th[-8])),
                                    (0.97 * np.cos(th[-1]), 0.97 * np.sin(th[-1])),
                                    arrowstyle="-|>", mutation_scale=14, color=color, lw=0))
    dot(b, 1 + 0j, RED, "short", dx=-0.04, dy=-0.1, ha="right")
    dot(b, -1 + 0j, GREEN, "open", dx=0.05, dy=-0.1)
    dot(b, target, AMBER, "+j0.585", dx=-0.05, dy=0.08, ha="right")
    b.set_title("the stub, read as admittance", fontsize=12.5, color=INK)
    fig.subplots_adjust(wspace=0.12)
    save(fig, "L13-stub-match.svg")


if __name__ == "__main__":
    stub_tuner()
    stub_match()
