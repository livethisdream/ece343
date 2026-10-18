#!/usr/bin/env python3
"""L03 figures: what a transmission line is, and the lumped-element model.

    L03-line-types.svg         cross sections: coaxial, two-wire, microstrip
    L03-electrical-length.svg  the voltage along a short line and a long one,
                               at one instant
    L03-two-port.svg           source, line, and load, with the z axis
    L03-lumped-cell.svg        one section of length dz: R', L', G', C'

Labels are minimal; the lesson text does the explaining.

    python3 scripts/graphics/l03_figures.py   ->   book/extras/viz/img/L03-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#5b6573", "#15202b"
FILL = "#e3edf6"      # dielectric
METAL = "#9aa8b6"     # conductor
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center", italic=True):
    """A symbol with an optional subscript, in plain text: an SVG with
    svg.fonttype 'none' cannot carry matplotlib's math fonts into a browser."""
    t = ax.text(x, y, base, fontsize=size, color=color, ha=ha, va=va,
                fontstyle="italic" if italic else "normal")
    if not sub:
        return t
    fig = ax.figure
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    w = bb.width / fig.dpi * 72                     # base width in points
    shift = {"center": w / 2, "left": w, "right": 0}[ha]
    ax.annotate(sub, (x, y), xytext=(shift + 0.5, -size * 0.32), textcoords="offset points",
                fontsize=size * 0.7, color=color, ha="left", va=va)
    return t


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


# ---------------------------------------------------------------------------
def line_types():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.3))
    for ax in axs:
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.9, 1.9)

    ax = axs[0]                                         # coaxial
    ax.add_patch(Circle((0, 0), 1.55, fc=METAL, ec=INK, lw=1.2))
    ax.add_patch(Circle((0, 0), 1.35, fc=FILL, ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), 0.38, fc=METAL, ec=INK, lw=1.2))
    ax.annotate("", xy=(0.38 * np.cos(0.6), 0.38 * np.sin(0.6)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4))
    lab(ax, 0.48, -0.12, "a", size=14, color=NAVY, ha="left", va="top")
    ax.annotate("", xy=(1.35 * np.cos(2.4), 1.35 * np.sin(2.4)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4))
    lab(ax, -0.55, 0.62, "b", size=14, color=NAVY)
    ax.set_title("coaxial", fontsize=13, color=INK, y=-0.08)

    ax = axs[1]                                         # two-wire
    ax.add_patch(Rectangle((-1.75, -0.55), 3.5, 1.1, fc=FILL, ec="none"))
    for x in (-1.0, 1.0):
        ax.add_patch(Circle((x, 0), 0.42, fc=METAL, ec=INK, lw=1.2))
    ax.annotate("", xy=(1.0, -0.95), xytext=(-1.0, -0.95),
                arrowprops=dict(arrowstyle="<|-|>", color=NAVY, lw=1.2))
    lab(ax, 0, -1.15, "D", size=14, color=NAVY, va="top")
    ax.set_title("two-wire", fontsize=13, color=INK, y=-0.08)

    ax = axs[2]                                         # microstrip
    ax.add_patch(Rectangle((-2.0, -1.05), 4.0, 0.16, fc=METAL, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((-2.0, -0.89), 4.0, 0.95, fc=FILL, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((-0.6, 0.06), 1.2, 0.16, fc=METAL, ec=INK, lw=1.0))
    ax.annotate("", xy=(0.6, 0.55), xytext=(-0.6, 0.55),
                arrowprops=dict(arrowstyle="<|-|>", color=NAVY, lw=1.2))
    lab(ax, 0, 0.68, "W", size=14, color=NAVY, va="bottom")
    ax.annotate("", xy=(1.55, 0.06), xytext=(1.55, -0.89),
                arrowprops=dict(arrowstyle="<|-|>", color=NAVY, lw=1.2))
    lab(ax, 1.72, -0.42, "h", size=14, color=NAVY, ha="left")
    ax.text(0, -1.30, "ground plane", color=GRAY, fontsize=11, ha="center", va="top")
    ax.set_title("microstrip", fontsize=13, color=INK, y=-0.08)

    fig.subplots_adjust(wspace=0.15)
    save(fig, "L03-line-types.svg")


# ---------------------------------------------------------------------------
def electrical_length():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.0), sharey=True)
    for ax, (lam_frac, label) in zip(axs, [(1 / 20, "ℓ = λ/20"),
                                           (1.5, "ℓ = 1.5λ")]):
        z = np.linspace(0, 1, 600)                       # position along the line, 0 = source
        v = np.cos(2 * np.pi * lam_frac * z)             # forward wave at t = 0
        ax.axhline(0, color="#c7d2e0", lw=1.0)
        ax.plot(z, v, color=NAVY, lw=2.6)
        ax.plot([0, 1], [v[0], v[-1]], "o", color=AMBER, ms=6, zorder=3)
        ax.set_xlim(-0.03, 1.03); ax.set_ylim(-1.35, 1.35)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["source", "load"])
        ax.set_yticks([])
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color("#c7d2e0")
        ax.tick_params(colors=GRAY, length=0, labelsize=12)
        ax.set_title(label, fontsize=15, color=INK, pad=6)
    axs[0].set_ylabel("voltage at one instant", color=GRAY, fontsize=12)
    fig.subplots_adjust(wspace=0.22)
    save(fig, "L03-electrical-length.svg")


# ---------------------------------------------------------------------------
def resistor(ax, x0, y0, x1, y1, n=6, amp=0.16, lw=1.6, color=INK):
    """Zigzag between two points (horizontal or vertical)."""
    t = np.linspace(0, 1, 2 * n + 1)
    off = np.zeros_like(t); off[1:-1:2] = amp; off[2:-1:2] = -amp
    if y0 == y1:
        ax.plot(x0 + (x1 - x0) * t, y0 + off, color=color, lw=lw, solid_joinstyle="miter")
    else:
        ax.plot(x0 + off, y0 + (y1 - y0) * t, color=color, lw=lw, solid_joinstyle="miter")


def inductor(ax, x0, x1, y, n=4, r=None, lw=1.6, color=INK):
    r = r or (x1 - x0) / (2 * n)
    for k in range(n):
        c = x0 + r + 2 * r * k
        th = np.linspace(np.pi, 0, 40)
        ax.plot(c + r * np.cos(th), y + r * np.sin(th), color=color, lw=lw)


def capacitor(ax, x, y0, y1, gap=0.14, w=0.34, lw=1.6, color=INK):
    ym = (y0 + y1) / 2
    ax.plot([x, x], [y0, ym + gap / 2], color=color, lw=lw)
    ax.plot([x, x], [ym - gap / 2, y1], color=color, lw=lw)
    ax.plot([x - w, x + w], [ym + gap / 2] * 2, color=color, lw=2.4)
    ax.plot([x - w, x + w], [ym - gap / 2] * 2, color=color, lw=2.4)


def terminal(ax, x, y):
    ax.add_patch(Circle((x, y), 0.08, fc="white", ec=INK, lw=1.4, zorder=4))


def lumped_cell():
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    ax.set_aspect("equal"); ax.axis("off")
    yt, yb = 2.0, 0.0
    # top rail: terminal, R'dz, L'dz, junction, terminal
    ax.plot([0, 0.8], [yt, yt], color=INK, lw=1.6)
    resistor(ax, 0.8, yt, 2.4, yt)
    ax.plot([2.4, 2.8], [yt, yt], color=INK, lw=1.6)
    inductor(ax, 2.8, 4.4, yt)
    ax.plot([4.4, 8.6], [yt, yt], color=INK, lw=1.6)
    ax.plot([0, 8.6], [yb, yb], color=INK, lw=1.6)
    # shunt G'dz and C'dz
    ax.plot([5.6, 5.6], [yt, 1.65], color=INK, lw=1.6)
    resistor(ax, 5.6, 1.65, 5.6, 0.35)
    ax.plot([5.6, 5.6], [0.35, yb], color=INK, lw=1.6)
    capacitor(ax, 7.2, yt, yb)
    for x in (5.6, 7.2):
        for y in (yt, yb):
            ax.add_patch(Circle((x, y), 0.05, fc=INK, ec=INK, zorder=3))
    for x in (0, 8.6):
        for y in (yt, yb):
            terminal(ax, x, y)
    # element labels
    lab(ax, 1.6, yt + 0.32, "R′Δz", color=NAVY, va="bottom")
    lab(ax, 3.6, yt + 0.48, "L′Δz", color=NAVY, va="bottom")
    lab(ax, 5.25, 1.0, "G′Δz", color=NAVY, ha="right")
    lab(ax, 7.62, 1.0, "C′Δz", color=NAVY, ha="left")
    # port voltages and currents
    lab(ax, -0.2, 1.0, "v(z, t)", size=14, ha="right")
    ax.text(0, 1.55, "+", ha="center", va="center", fontsize=13, color=INK)
    ax.text(0, 0.42, "−", ha="center", va="center", fontsize=15, color=INK)
    lab(ax, 8.8, 1.0, "v(z + Δz, t)", size=14, ha="left")
    ax.text(8.6, 1.55, "+", ha="center", va="center", fontsize=13, color=INK)
    ax.text(8.6, 0.42, "−", ha="center", va="center", fontsize=15, color=INK)
    ax.add_patch(FancyArrowPatch((0.15, yt + 0.0), (0.7, yt), arrowstyle="-|>",
                                 mutation_scale=14, color=AMBER, lw=1.6))
    lab(ax, 0.62, yt - 0.25, "i(z, t)", size=13, color=AMBER, va="top")
    ax.add_patch(FancyArrowPatch((7.9, yt), (8.45, yt), arrowstyle="-|>",
                                 mutation_scale=14, color=AMBER, lw=1.6))
    lab(ax, 8.15, yt + 0.25, "i(z + Δz, t)", size=13, color=AMBER, va="bottom")
    # length bracket
    ax.annotate("", xy=(8.6, -0.55), xytext=(0, -0.55),
                arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.2))
    lab(ax, 4.3, -0.7, "Δz", color=GRAY, va="top")
    ax.set_xlim(-1.6, 10.9); ax.set_ylim(-1.2, 2.9)
    save(fig, "L03-lumped-cell.svg")


# ---------------------------------------------------------------------------
def two_port():
    fig, ax = plt.subplots(figsize=(9.6, 3.4))
    ax.set_aspect("equal"); ax.axis("off")
    yt, yb = 2.0, 0.0
    # source: circle with a sine, series Zs
    ax.plot([0, 0], [yb, 0.55], color=INK, lw=1.6)
    ax.plot([0, 0], [1.45, yt], color=INK, lw=1.6)
    ax.add_patch(Circle((0, 1.0), 0.45, fc="white", ec=INK, lw=1.6))
    s = np.linspace(-0.25, 0.25, 50)
    ax.plot(s, 1.0 + 0.14 * np.sin(2 * np.pi * s / 0.5), color=INK, lw=1.4)
    lab(ax, -0.95, 1.0, "V", "s", ha="right")
    ax.plot([0, 0.4], [yt, yt], color=INK, lw=1.6)
    ax.add_patch(Rectangle((0.4, yt - 0.22), 1.0, 0.44, fc="white", ec=INK, lw=1.6))
    lab(ax, 0.85, yt + 0.35, "Z", "s", va="bottom")
    ax.plot([1.4, 2.0], [yt, yt], color=INK, lw=1.6)
    ax.plot([0, 2.0], [yb, yb], color=INK, lw=1.6)
    # the line: two thick conductors
    ax.plot([2.0, 7.6], [yt, yt], color=NAVY, lw=5.0, solid_capstyle="butt")
    ax.plot([2.0, 7.6], [yb, yb], color=NAVY, lw=5.0, solid_capstyle="butt")
    lab(ax, 4.75, 1.0, "Z", "0", size=17, color=NAVY)
    # load
    ax.plot([7.6, 8.4], [yt, yt], color=INK, lw=1.6)
    ax.plot([7.6, 8.4], [yb, yb], color=INK, lw=1.6)
    ax.plot([8.4, 8.4], [yt, 1.5], color=INK, lw=1.6)
    ax.plot([8.4, 8.4], [0.5, yb], color=INK, lw=1.6)
    ax.add_patch(Rectangle((8.18, 0.5), 0.44, 1.0, fc="white", ec=INK, lw=1.6))
    lab(ax, 8.85, 1.0, "Z", "L", ha="left")
    # z axis
    for x, txt in ((2.0, "z = −ℓ"), (7.6, "z = 0")):
        ax.plot([x, x], [-0.35, -0.6], color=GRAY, lw=1.2)
        lab(ax, x, -0.72, txt, size=14, color=GRAY, va="top")
    ax.annotate("", xy=(9.4, -0.48), xytext=(1.2, -0.48),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
    lab(ax, 9.5, -0.48, "z", color=GRAY, ha="left")
    ax.set_xlim(-1.4, 10.0); ax.set_ylim(-1.4, 2.8)
    save(fig, "L03-two-port.svg")


if __name__ == "__main__":
    line_types()
    electrical_length()
    two_port()
    lumped_cell()
