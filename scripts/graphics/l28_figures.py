#!/usr/bin/env python3
"""L28 figures: the Biot-Savart law and Gauss's law for magnetism.

    L28-biot-savart.svg   a current element I dl, the vector R to the field
                          point, and the field dH it makes there (into the page)
    L28-finite-wire.svg   a finite straight wire, one element and its mirror
                          image, and the field point on the bisecting plane
    L28-loop.svg          a circular loop, one element and the element
                          opposite it, and their fields on the axis
    L28-field-lines.svg   field lines of an electric dipole beside the field
                          lines of a current loop, both in cross section

Labels are plain Unicode (see CLAUDE.md); vectors are bold and upright,
scalars italic. The lesson text does the explaining.

The field lines are contours of each field's flux function, so every line
carries the same flux and the spacing shows the strength. For the charges,
psi = sum q_i cos(theta_i); for the loop, psi = rho A_phi, with A_phi from a
direct numerical integral around the loop.

    python3 scripts/graphics/l28_figures.py   ->   book/extras/viz/img/L28-*.svg
"""

from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from l18_figures import (lab, vec, arrow, charge, point, save,  # noqa: E402
                         NAVY, BLUE, AMBER, RED, GRAY, INK, GREEN, AXIS)
from l19_figures import P, axes3d, frame  # noqa: E402

LINE = "#7fa3c4"      # field lines


def into(ax, x, y, r=0.17, color=NAVY):
    """A vector pointing into the page: a circle with a cross."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.8, zorder=6))
    d = r * 0.62
    ax.plot([x - d, x + d], [y - d, y + d], color=color, lw=1.8, zorder=7)
    ax.plot([x - d, x + d], [y + d, y - d], color=color, lw=1.8, zorder=7)


def outof(ax, x, y, r=0.17, color=NAVY):
    """A vector pointing out of the page: a circle with a dot."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.8, zorder=6))
    ax.add_patch(Circle((x, y), r * 0.28, fc=color, ec="none", zorder=7))


def wire(ax, z0, z1, x=0.0):
    ax.plot([x, x], [z0, z1], color=RED, lw=4, solid_capstyle="round", zorder=3)


# ---------------------------------------------------------------------------
def biot_savart():
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.2, 5.0); ax.set_ylim(-1.6, 3.0)
    wire(ax, -1.5, 2.9)
    arrow(ax, (0, 1.8), (0, 2.6), color=RED, lw=2.0, ms=16)
    lab(ax, -0.18, 2.3, "I", size=15, color=RED, ha="right")
    # the element
    e0, e1 = np.array([0, -0.15]), np.array([0, 0.55])
    ax.plot(*zip(e0, e1), color=AMBER, lw=6, solid_capstyle="butt", zorder=4)
    arrow(ax, e0, e1 + np.array([0, 0.12]), color=AMBER, lw=2.2, ms=16)
    vec(ax, -0.2, 0.2, "I dl", color=AMBER, ha="right")
    # R to the field point
    src, obs = np.array([0, 0.2]), np.array([3.6, 1.7])
    arrow(ax, src, obs, color=AMBER, lw=2.0)
    vec(ax, 1.75, 1.25, "R", color=AMBER, ha="left")
    # angle between dl and R
    ang = np.linspace(np.pi / 2, np.arctan2(obs[1] - src[1], obs[0] - src[0]), 40)
    ax.plot(src[0] + 0.7 * np.cos(ang), src[1] + 0.7 * np.sin(ang), color=INK, lw=1.0)
    lab(ax, 0.42, 0.95, "θ", size=14, color=INK)
    into(ax, *obs, r=0.2)
    vec(ax, obs[0] + 0.32, obs[1] + 0.05, "dH", color=NAVY, ha="left")
    ax.text(obs[0] + 0.05, obs[1] - 0.42, "field point", fontsize=11.5, color=GRAY, ha="center", va="center")
    save(fig, "L28-biot-savart.svg")


# ---------------------------------------------------------------------------
def finite_wire():
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.6, 4.2); ax.set_ylim(-2.7, 2.9)
    Lh = 2.2
    arrow(ax, (-0.9, 0), (4.0, 0), color=AXIS, lw=1.2, ms=12)
    lab(ax, 4.0, -0.22, "ρ", size=13, color=GRAY, ha="right", va="top")
    wire(ax, -Lh, Lh)
    arrow(ax, (0, Lh - 0.7), (0, Lh - 0.05), color=RED, lw=2.0, ms=16)
    lab(ax, -0.2, Lh - 0.35, "I", size=15, color=RED, ha="right")
    lab(ax, -0.18, Lh, "L/2", size=13, color=GRAY, ha="right")
    lab(ax, -0.18, -Lh, "−L/2", size=13, color=GRAY, ha="right")
    lab(ax, 0.1, 2.75, "z", size=13, color=GRAY, ha="left", va="top")
    zp, rho = 1.25, 3.0
    obs = np.array([rho, 0])
    for z, ls, w in ((zp, "-", 2.0), (-zp, "--", 1.3)):
        ax.plot([0, 0], [z - 0.17, z + 0.17], color=AMBER, lw=6, solid_capstyle="butt", zorder=4)
        arrow(ax, (0, z), obs, color=AMBER, lw=w, ls=ls)
    lab(ax, 0.2, zp + 0.12, "dz′", size=13, color=AMBER, ha="left")
    lab(ax, -0.2, zp, "z′", size=13, color=GRAY, ha="right")
    lab(ax, -0.2, -zp, "−z′", size=13, color=GRAY, ha="right")
    vec(ax, 1.55, 1.0, "R", color=AMBER, ha="left")
    into(ax, *obs, r=0.2)
    vec(ax, rho + 0.3, 0.38, "H", color=NAVY, ha="left")
    lab(ax, rho / 2, -0.25, "ρ", size=14, color=INK, va="top")
    save(fig, "L28-finite-wire.svg")


# ---------------------------------------------------------------------------
def loop():
    fig, ax = frame((6.0, 4.9), (-2.2, 3.0), (-1.5, 3.4))
    axes3d(ax, L=2.4, zmax=3.3)
    a, h = 1.6, 2.2
    ph = np.linspace(0, 2 * np.pi, 300)
    pts = np.array([P(a * np.cos(t), a * np.sin(t), 0) for t in ph])
    ax.plot(pts[:, 0], pts[:, 1], color=RED, lw=3.2)
    # current direction: counterclockwise seen from +z
    t0 = -0.25 * np.pi
    arrow(ax, P(a * np.cos(t0), a * np.sin(t0), 0), P(a * np.cos(t0 + 0.25), a * np.sin(t0 + 0.25), 0),
          color=RED, lw=2.0, ms=16)
    lab(ax, *(P(a * np.cos(t0), a * np.sin(t0), 0) + np.array([0.2, -0.15])), "I", size=15, color=RED, ha="left")
    Pz = P(0, 0, h)
    f1, f2 = 0.45 * np.pi, 0.45 * np.pi + np.pi
    for f, w, ls, alpha in ((f1, 1.8, "-", 1.0), (f2, 1.2, "--", 0.55)):
        e = P(a * np.cos(f), a * np.sin(f), 0)
        # the element dl along phi-hat
        tip = P(a * np.cos(f) - 0.45 * np.sin(f), a * np.sin(f) + 0.45 * np.cos(f), 0)
        arrow(ax, e, tip, color=AMBER, lw=2.2 if alpha == 1 else 1.4, ms=14)
        arrow(ax, e, Pz, color=AMBER, lw=w, ls=ls)
    e1 = P(a * np.cos(f1), a * np.sin(f1), 0)
    vec(ax, *(e1 + np.array([0.12, -0.28])), "dl", color=AMBER, ha="left")
    vec(ax, *(0.5 * (e1 + Pz) + np.array([0.25, 0.0])), "R", color=AMBER, ha="left")
    ax.plot(*zip(P(0, 0, 0), e1), color=INK, lw=1.0)
    lab(ax, *(0.5 * (P(0, 0, 0) + e1) + np.array([-0.05, 0.16])), "a", size=14, color=INK)
    point(ax, *Pz)
    lab(ax, -0.15, h / 2 + 0.2, "z", size=14, color=GRAY, ha="right")
    # dH from each element: perpendicular to R and to dl, in the plane of R and z-hat
    s = 0.85
    for f, w, ls in ((f1, 2.0, "-"), (f2, 1.4, "--")):
        src = np.array([a * np.cos(f), a * np.sin(f), 0])
        R = np.array([0, 0, h]) - src
        dl = np.array([-np.sin(f), np.cos(f), 0])
        d = np.cross(dl, R); d = s * d / np.linalg.norm(d)
        arrow(ax, Pz, Pz + P(*d), color=NAVY, lw=w, ls=ls)
        if f == f1:
            vec(ax, *(Pz + P(*d) + np.array([0.1, 0.12])), "dH", color=NAVY, ha="left")
    # their sum points along z
    arrow(ax, Pz, Pz + np.array([0, 0.95]), color=GREEN, lw=2.6, ms=18)
    vec(ax, *(Pz + np.array([-0.15, 0.75])), "H", color=GREEN, ha="right")
    save(fig, "L28-loop.svg")


# ---------------------------------------------------------------------------
def a_phi(rho, z, a=1.0, n=720):
    """A_phi of a unit loop of radius a, up to the constant mu0 I a / 4 pi."""
    ph = (np.arange(n) + 0.5) * 2 * np.pi / n
    r = np.sqrt(rho[..., None] ** 2 + a ** 2 + z[..., None] ** 2 - 2 * a * rho[..., None] * np.cos(ph))
    return (np.cos(ph) / r).sum(-1) * 2 * np.pi / n


def field_lines():
    fig, (axe, axm) = plt.subplots(1, 2, figsize=(9.6, 4.6))
    for ax in (axe, axm):
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6)
    x = np.linspace(-2.6, 2.6, 521); z = np.linspace(-2.6, 2.6, 521)
    X, Z = np.meshgrid(x, z)

    # electric dipole: +q at z = +0.7, -q at z = -0.7; psi = cos(theta+) - cos(theta-)
    d = 0.7
    rp = np.hypot(X, Z - d); rm = np.hypot(X, Z + d)
    psi = (Z - d) / np.maximum(rp, 1e-9) - (Z + d) / np.maximum(rm, 1e-9)
    axe.contour(X, Z, psi, levels=np.linspace(-1.88, -0.12, 9), colors=LINE, linewidths=1.2,
                linestyles="solid")
    charge(axe, 0, d, +1, r=0.17); charge(axe, 0, -d, -1, r=0.17)
    arrow(axe, (0, 0.18), (0, -0.18), color=LINE, lw=1.4, ms=12)
    axe.text(0, -2.5, "electric dipole", fontsize=12.5, color=GRAY, ha="center", va="center")

    # current loop of radius 1 in the plane z = 0, seen in cross section:
    # out of the page at x = -1, into the page at x = +1, so B points up through the middle
    rho = np.abs(X)
    psi_m = rho * a_phi(rho, Z)
    lv = [0.12, 0.3, 0.55, 0.85, 1.2, 1.65, 2.2, 3.0, 4.0]
    axm.contour(X, Z, psi_m, levels=lv, colors=LINE, linewidths=1.2, linestyles="solid")
    outof(axm, -1, 0, r=0.17, color=RED); into(axm, 1, 0, r=0.17, color=RED)
    arrow(axm, (0, -0.2), (0, 0.2), color=LINE, lw=1.4, ms=12)
    arrow(axm, (-2.15, 0.2), (-2.15, -0.2), color=LINE, lw=1.4, ms=12)
    arrow(axm, (2.15, 0.2), (2.15, -0.2), color=LINE, lw=1.4, ms=12)
    axm.text(0, -2.5, "current loop", fontsize=12.5, color=GRAY, ha="center", va="center")
    save(fig, "L28-field-lines.svg")


if __name__ == "__main__":
    biot_savart()
    finite_wire()
    loop()
    field_lines()
