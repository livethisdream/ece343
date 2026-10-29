#!/usr/bin/env python3
"""L16 figures: the two mismatched loads of the L15-L16 lab on the Smith chart.

    L16-lab-loads.svg   the 1 kohm resistor, a fixed point at r = 20; and the
                        50 ohm resistor in series with 470 pF, which rides the
                        r = 1 circle from 50 kHz to 5 MHz, marked at 2 MHz.
                        Each Gamma is drawn as a ray from the center.

    python3 scripts/graphics/l16_figures.py   ->   book/extras/viz/img/L16-*.svg
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

from l10_smith_base import chart, gamma, dot, r_circle, save, NAVY, GREEN, AMBER, INK

Z0, C = 50.0, 470e-12


def zl(f):
    """Normalized impedance of 50 ohm in series with 470 pF."""
    return (Z0 - 1j / (2 * np.pi * f * C)) / Z0


def ray(ax, g, color):
    ax.annotate("", xy=(g.real, g.imag), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=12))


def lab_loads():
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    chart(ax)
    r_circle(ax, 1, AMBER, lw=1.2, ls="--")

    f = np.logspace(np.log10(50e3), np.log10(5e6), 300)
    g = gamma(zl(f))
    ax.plot(g.real, g.imag, color=GREEN, lw=2.8, solid_capstyle="round", zorder=4)
    g2 = gamma(zl(2e6))
    ray(ax, g2, GREEN)
    dot(ax, g[0], GREEN, "50 kHz", dx=-0.05, dy=-0.1, ha="right", size=5, fs=11)
    dot(ax, g[-1], GREEN, "5 MHz", dx=0.0, dy=-0.1, ha="center", size=5, fs=11)
    dot(ax, g2, GREEN, "2 MHz", dx=0.06, dy=-0.06, size=7, fs=12)

    g1k = gamma(1000 / Z0)
    ray(ax, g1k, NAVY)
    dot(ax, g1k, NAVY, "1 kΩ", dx=-0.02, dy=0.11, ha="right")

    ax.text(-0.1, -0.78, "50 Ω + 470 pF", color=GREEN, fontsize=12, ha="center")
    ax.text(0.5, 0.53, "r = 1", color=AMBER, fontsize=11, ha="center", va="bottom")
    save(fig, "L16-lab-loads.svg")


if __name__ == "__main__":
    lab_loads()
