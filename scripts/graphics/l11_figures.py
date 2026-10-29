#!/usr/bin/env python3
"""L11 figures: moving along the line on the Smith chart.

    L11-rotation.svg   left: z_L = 1.5 + j1.2 rotated 0.1 wavelength toward
                       the source, to z_in = 1.90 - j1.15; right: a quarter
                       wavelength is a half turn, which lands on y_L = 1/z_L

    python3 scripts/graphics/l11_figures.py   ->   book/extras/viz/img/L11-*.svg
"""

from __future__ import annotations
import matplotlib.pyplot as plt

from l10_smith_base import chart, gamma, gamma_circle, dot, rotate_arc, save, NAVY, GREEN, AMBER, INK


def rotation():
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.8))
    g = gamma(1.5 + 1.2j)
    chart(a); gamma_circle(a, abs(g))
    gi = rotate_arc(a, g, 0.1)
    dot(a, g, NAVY, "load", dx=0.06, dy=0.05)
    dot(a, gi, GREEN, "input, d = 0.1λ", dx=0.04, dy=-0.1)
    a.set_title("toward the source: clockwise", fontsize=12.5, color=INK)

    chart(b); gamma_circle(b, abs(g))
    gq = rotate_arc(b, g, 0.25, color=AMBER)
    dot(b, g, NAVY, "z", dx=0.06, dy=0.05)
    dot(b, gq, AMBER, "1/z", dx=-0.06, dy=-0.07, ha="right")
    b.plot([g.real, gq.real], [g.imag, gq.imag], color=AMBER, lw=1.0, ls=":")
    b.set_title("d = λ/4: a half turn", fontsize=12.5, color=INK)
    fig.subplots_adjust(wspace=0.12)
    save(fig, "L11-rotation.svg")


if __name__ == "__main__":
    rotation()
