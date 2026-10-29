#!/usr/bin/env python3
"""L12 figures: matching with a length of line and one lumped component.

    L12-element-moves.svg   left: a series reactance moves z along its
                            constant-r circle; right: a shunt susceptance moves
                            y along its constant-g circle (the same grid, read
                            as admittance)
    L12-series-match.svg    the worked example: z_L = 0.678 + j0.358, rotated
                            0.0642 wavelength to 1 + j0.585, then a series
                            capacitor of -j0.585 moves it to the center

    python3 scripts/graphics/l12_figures.py   ->   book/extras/viz/img/L12-*.svg
"""

from __future__ import annotations
import matplotlib.pyplot as plt

from l10_smith_base import (chart, gamma, gamma_circle, dot, rotate_arc, path_const_r, r_circle,
                            save, NAVY, GREEN, AMBER, RED, BLUE, INK)


def element_moves():
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.8))
    chart(a); r_circle(a, 0.5, BLUE, lw=1.6)
    path_const_r(a, 0.5, 0.05, 0.9, RED)
    path_const_r(a, 0.5, -0.05, -0.9, AMBER)
    p = gamma(0.5 + 0.5j); a.text(p.real - 0.05, p.imag + 0.08, "series L", color=RED, fontsize=12, ha="right")
    p = gamma(0.5 - 0.5j); a.text(p.real - 0.05, p.imag - 0.08, "series C", color=AMBER, fontsize=12, ha="right")
    a.set_title("impedance z: constant r", fontsize=12.5, color=INK)

    chart(b); r_circle(b, 0.5, BLUE, lw=1.6)
    path_const_r(b, 0.5, 0.05, 0.9, RED)
    path_const_r(b, 0.5, -0.05, -0.9, AMBER)
    p = gamma(0.5 + 0.5j); b.text(p.real - 0.05, p.imag + 0.08, "shunt C", color=RED, fontsize=12, ha="right")
    p = gamma(0.5 - 0.5j); b.text(p.real - 0.05, p.imag - 0.08, "shunt L", color=AMBER, fontsize=12, ha="right")
    b.set_title("admittance y: constant g", fontsize=12.5, color=INK)
    fig.subplots_adjust(wspace=0.12)
    save(fig, "L12-element-moves.svg")


def series_match():
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    chart(ax)
    r_circle(ax, 1, BLUE, lw=1.8)
    zl = (33.9 + 17.9j) / 50
    g = gamma(zl)
    gamma_circle(ax, abs(g))
    gi = rotate_arc(ax, g, 0.0642)
    path_const_r(ax, 1, 0.585, 0.0, AMBER)
    dot(ax, g, NAVY, "load", dx=-0.06, dy=0.06, ha="right")
    dot(ax, gi, GREEN, "1 + j0.585", dx=0.05, dy=0.07)
    dot(ax, 0j, AMBER, "match", dx=-0.04, dy=-0.1, ha="right")
    save(fig, "L12-series-match.svg")


if __name__ == "__main__":
    element_moves()
    series_match()
