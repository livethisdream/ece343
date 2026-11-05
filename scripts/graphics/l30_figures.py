#!/usr/bin/env python3
"""L30 figures: Ampere's law for the coax, the current sheet, the solenoid, and
the toroid, and the flux that gives the coaxial inductance.

    L30-coax.svg        coax cross section with three Amperian circles, and H
                        against radius
    L30-sheet.svg       edge view of a current sheet with a rectangular
                        Amperian path through it
    L30-solenoid.svg    side section of a long solenoid with a rectangular
                        Amperian path, one side inside the coil
    L30-finite-solenoid.svg
                        side section of a finite solenoid with one slice dz′
                        at z′ and the field point z on the axis
    L30-toroid.svg      top view of a toroid with a circular Amperian path in
                        the core
    L30-coax-flux.svg   a long section of the coax, with the strip between the
                        conductors that the magnetic flux crosses

Current out of the page is a dot, into the page a cross. Labels are plain
Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l30_figures.py   ->   book/extras/viz/img/L30-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL = "#e3edf6"      # dielectric, core
METAL = "#9aa8b6"     # conductor
CURRENT = "#f3d9d9"   # region carrying current
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center", italic=True):
    """A symbol with an optional subscript, in plain text (see l03_figures.py)."""
    t = ax.text(x, y, base, fontsize=size, color=color, ha=ha, va=va,
                fontstyle="italic" if italic else "normal")
    if not sub:
        return t
    fig = ax.figure
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    w = bb.width / fig.dpi * 72
    shift = {"center": w / 2, "left": w, "right": 0}[ha]
    ax.annotate(sub, (x, y), xytext=(shift + 0.5, -size * 0.32), textcoords="offset points",
                fontsize=size * 0.7, color=color, ha="left", va=va)
    return t


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=1.6, ms=12):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def blank(ax, xl, yl):
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*xl); ax.set_ylim(*yl)


def dot(ax, x, y, r=0.1, color=RED):
    """A current out of the page."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.5, zorder=6))
    ax.add_patch(Circle((x, y), r * 0.32, fc=color, ec="none", zorder=7))


def cross(ax, x, y, r=0.1, color=RED):
    """A current into the page."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.5, zorder=6))
    d = r * 0.6
    ax.plot([x - d, x + d], [y - d, y + d], color=color, lw=1.4, zorder=7)
    ax.plot([x - d, x + d], [y + d, y - d], color=color, lw=1.4, zorder=7)


def ienc0(ax, x, y, size=11, color=GRAY):
    """The label I_encl = 0, centered near (x, y), with a real subscript."""
    ax.annotate("I", (x, y), xytext=(-size * 1.6, 0), textcoords="offset points",
                fontsize=size, color=color, ha="right", va="center", fontstyle="italic")
    ax.annotate("encl", (x, y), xytext=(-size * 1.6 + 0.5, -size * 0.32), textcoords="offset points",
                fontsize=size * 0.7, color=color, ha="left", va="center")
    ax.annotate("= 0", (x, y), xytext=(size * 0.55, 0), textcoords="offset points",
                fontsize=size, color=color, ha="left", va="center")


def style_plot(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY)


# ---------------------------------------------------------------------------
def coax():
    # Drawn at a modest size with large labels: in present mode the figure sits
    # in a block about 476 px wide, and the labels must stay above 10.5 px.
    a, b = 0.55, 1.5
    fs = 20
    fig, (ax, ay) = plt.subplots(1, 2, figsize=(8.6, 3.7), gridspec_kw={"width_ratios": [1, 1.25]})
    blank(ax, (-2.1, 2.1), (-2.0, 2.0))
    ax.add_patch(Circle((0, 0), b + 0.09, fc=METAL, ec="none"))
    ax.add_patch(Circle((0, 0), b, fc=FILL, ec="none"))
    ax.add_patch(Circle((0, 0), a, fc=CURRENT, ec=RED, lw=1.2))
    dot(ax, 0, 0, r=0.15)
    for th in np.radians(np.arange(0, 360, 45)):
        cross(ax, (b + 0.045) * np.cos(th), (b + 0.045) * np.sin(th), r=0.09)
    t = np.linspace(0, 2 * np.pi, 300)
    for r in (0.32, 1.0, 1.85):
        ax.plot(r * np.cos(t), r * np.sin(t), color=NAVY, lw=1.5, ls="--")
    ax.plot([0, -a * np.cos(np.radians(30))], [0, -a * np.sin(np.radians(30))], color=INK, lw=1.2)
    lab(ax, -0.3, -0.42, "a", size=fs)
    ax.plot([0, -b * np.cos(np.radians(-60))], [0, b * np.sin(np.radians(-60))], color=INK, lw=1.2)
    lab(ax, -0.62, -1.02, "b", size=fs)

    rho = np.linspace(0, 2.4, 700)
    H = np.where(rho < a, rho / a, np.where(rho < b, a / np.maximum(rho, 1e-9), 0.0))
    ay.axvspan(0, a, color=CURRENT, alpha=0.7, lw=0)
    ay.axvspan(a, b, color=FILL, alpha=0.8, lw=0)
    ay.plot(rho, H, color=NAVY, lw=2.6)
    ay.set_xlim(0, 2.4); ay.set_ylim(0, 1.2)
    ay.set_xticks([0, a, b]); ay.set_xticklabels(["0", "a", "b"], fontsize=fs)
    ay.set_yticks([0, 1]); ay.set_yticklabels(["0", "I/2πa"], fontsize=fs)
    ay.set_xlabel("ρ", fontsize=fs + 2, fontstyle="italic", color=INK)
    ay.text(0.04, 1.02, "∝ ρ", fontsize=fs, color=NAVY)
    ay.text(0.9, 0.62, "∝ 1/ρ", fontsize=fs, color=NAVY)
    ay.text(1.75, 0.08, "0", fontsize=fs, color=NAVY)
    lab(ay, 2.15, 0.5, "H", "φ", size=fs + 2, color=NAVY)
    style_plot(ay)
    ay.tick_params(labelsize=fs)
    save(fig, "L30-coax.svg")


# ---------------------------------------------------------------------------
def sheet():
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    blank(ax, (-3.0, 3.0), (-1.75, 1.75))
    ax.plot([-2.9, 2.9], [0, 0], color=RED, lw=2.2, alpha=0.35)
    for x in np.arange(-2.7, 2.75, 0.3):
        dot(ax, x, 0, r=0.09)
    # rectangular path a-b-c-d, counterclockwise
    x0, x1, h = -0.7, 0.7, 1.05
    xs = [x1, x1, x0, x0, x1]
    ys = [-h, h, h, -h, -h]
    ax.plot(xs, ys, color=NAVY, lw=1.6)
    arrow(ax, x1, -0.6, x1, -0.15, color=NAVY)
    arrow(ax, 0.25, h, -0.2, h, color=NAVY)
    arrow(ax, x0, 0.6, x0, 0.15, color=NAVY)
    arrow(ax, -0.25, -h, 0.2, -h, color=NAVY)
    # H above (to the left, -x) and below (to the right, +x)
    for x in (-2.3, -1.6, 1.6, 2.3):
        arrow(ax, x + 0.3, 0.75, x - 0.3, 0.75, color=BLUE, lw=2.0, ms=14)
        arrow(ax, x - 0.3, -0.75, x + 0.3, -0.75, color=BLUE, lw=2.0, ms=14)
    lab(ax, 2.0, 1.12, "H", color=BLUE, italic=False)
    lab(ax, -2.0, -1.12, "H", color=BLUE, italic=False)
    ax.annotate("", xy=(x1, 1.45), xytext=(x0, 1.45),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    lab(ax, 0, 1.62, "w", size=13, color=GRAY)
    lab(ax, 1.05, 0.45, "C", size=13, color=NAVY)
    lab(ax, 2.75, 0.32, "J", "s", size=13, color=RED)
    # axis key: z up, y to the right, x out of the page
    kx, ky = -2.85, 1.0
    arrow(ax, kx, ky, kx, ky + 0.42, color=GRAY, lw=1.0, ms=9)
    ax.text(kx - 0.05, ky + 0.56, "z", fontsize=13, fontstyle="italic", color=GRAY, ha="center")
    arrow(ax, kx, ky, kx + 0.42, ky, color=GRAY, lw=1.0, ms=9)
    ax.text(kx + 0.56, ky, "y", fontsize=13, fontstyle="italic", color=GRAY, va="center")
    ax.add_patch(Circle((kx, ky), 0.07, fc="white", ec=GRAY, lw=1.0, zorder=6))
    ax.add_patch(Circle((kx, ky), 0.022, fc=GRAY, ec="none", zorder=7))
    ax.text(kx - 0.12, ky - 0.2, "x", fontsize=13, fontstyle="italic", color=GRAY, ha="right")
    save(fig, "L30-sheet.svg")


# ---------------------------------------------------------------------------
def solenoid():
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    blank(ax, (-3.9, 3.9), (-2.0, 1.95))
    R = 0.85
    xs = np.arange(-3.4, 3.45, 0.3)
    for x in xs:
        dot(ax, x, R, r=0.1)
        cross(ax, x, -R, r=0.1)
    for x in (-2.6, -1.0, 0.6, 2.2):
        arrow(ax, x - 0.4, 0, x + 0.4, 0, color=BLUE, lw=2.0, ms=14)
    lab(ax, -2.6, 0.28, "H", color=BLUE, italic=False)
    # the Amperian rectangle: one long side inside, one outside; its short
    # sides pass through gaps between turns
    x0, x1, yin, yout = -0.65, 1.25, 0.35, 1.45
    ax.plot([x0, x1, x1, x0, x0], [yin, yin, yout, yout, yin], color=NAVY, lw=1.6)
    arrow(ax, 0.0, yin, 0.45, yin, color=NAVY)
    arrow(ax, x1, 0.65, x1, 1.05, color=NAVY)
    arrow(ax, 0.6, yout, 0.15, yout, color=NAVY)
    arrow(ax, x0, 1.15, x0, 0.75, color=NAVY)
    ax.annotate("", xy=(x1, 1.7), xytext=(x0, 1.7),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    lab(ax, 0.3, 1.85, "ℓ′", size=13, color=GRAY)
    lab(ax, 1.55, 1.62, "C", size=13, color=NAVY)
    # two rectangles that enclose no current: both long sides outside, and
    # both long sides inside
    for (u0, u1, v0, v1, lx, ly) in ((-3.1, -1.6, -1.25, -1.7, -2.35, -1.9),
                                     (1.85, 3.25, -0.2, -0.6, 2.55, -0.4)):
        ax.plot([u0, u1, u1, u0, u0], [v0, v0, v1, v1, v0], color=NAVY, lw=1.1, alpha=0.55)
    ienc0(ax, -2.35, -1.475)
    ienc0(ax, 2.55, -0.4, size=10.5)
    ax.text(3.75, 0, "z", fontsize=13, fontstyle="italic", color=GRAY, va="center")
    ax.text(-3.75, 1.55, "n turns per meter, current I", fontsize=12, color=GRAY)
    save(fig, "L30-solenoid.svg")


# ---------------------------------------------------------------------------
def finite_solenoid():
    fig, ax = plt.subplots(figsize=(7.6, 3.3))
    blank(ax, (-3.9, 3.9), (-1.55, 1.65))
    R, half = 0.75, 2.4
    ax.add_patch(Rectangle((-half, -R), 2 * half, 2 * R, fc=FILL, ec="none"))
    for x in np.arange(-half + 0.15, half, 0.3):
        dot(ax, x, R, r=0.09)
        cross(ax, x, -R, r=0.09)
    # one slice of thickness dz' at z'
    zp, dz = -0.9, 0.3
    ax.add_patch(Rectangle((zp - dz / 2, -R - 0.12), dz, 2 * R + 0.24, fc=AMBER, ec=AMBER,
                           alpha=0.28, lw=1.0, zorder=5))
    ax.plot([-3.7, 3.6], [0, 0], color=GRAY, lw=1.0, ls="--")
    ax.text(3.75, 0, "z", fontsize=13, fontstyle="italic", color=GRAY, va="center")
    # field point z on the axis
    zf = 1.4
    ax.plot(zf, 0, "o", color=NAVY, ms=7, zorder=8)
    lab(ax, zf, -0.25, "z", size=14, color=NAVY)
    # u = z - z'
    ax.annotate("", xy=(zf, 0.28), xytext=(zp, 0.28),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.3, shrinkA=0, shrinkB=0))
    ax.text((zp + zf) / 2, 0.36, "u = z − z′", fontsize=13, color=NAVY, ha="center", va="bottom",
            fontstyle="italic")
    # labels: the slice, its position, and the coil ends
    ax.text(zp, R + 0.42, "n dz′ turns", fontsize=12, color=AMBER, ha="center")
    lab(ax, zp, -R - 0.35, "z′", size=14, color=AMBER)
    for x, t in ((-half, "−ℓ/2"), (half, "ℓ/2")):
        ax.plot([x, x], [-R - 0.15, -R - 0.32], color=GRAY, lw=1.0)
        ax.text(x, -R - 0.5, t, fontsize=13, color=GRAY, ha="center", va="center")
    ax.annotate("", xy=(-3.3, R), xytext=(-3.3, 0),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    lab(ax, -3.5, R / 2, "a", size=13, color=GRAY)
    save(fig, "L30-finite-solenoid.svg")


# ---------------------------------------------------------------------------
def toroid():
    fig, ax = plt.subplots(figsize=(4.6, 4.9))
    blank(ax, (-2.25, 2.25), (-2.45, 2.45))
    r1, r2 = 1.05, 1.75
    ax.add_patch(Circle((0, 0), r2, fc=FILL, ec=GRAY, lw=1.0))
    ax.add_patch(Circle((0, 0), r1, fc="white", ec=GRAY, lw=1.0))
    for th in np.radians(np.arange(0, 360, 20)):
        dot(ax, (r1 - 0.06) * np.cos(th), (r1 - 0.06) * np.sin(th), r=0.075)
        cross(ax, (r2 + 0.06) * np.cos(th), (r2 + 0.06) * np.sin(th), r=0.075)
    t = np.linspace(0, 2 * np.pi, 300)
    rm = 1.4
    ax.plot(rm * np.cos(t), rm * np.sin(t), color=NAVY, lw=1.5, ls="--")
    for th in np.radians([30, 150, 270]):
        x, y = rm * np.cos(th), rm * np.sin(th)
        arrow(ax, x, y, x - 0.42 * np.sin(th), y + 0.42 * np.cos(th), color=BLUE, lw=2.0, ms=14)
    lab(ax, 0.12, -1.62, "H", color=BLUE, italic=False)
    # the two circles that enclose no net current: in the hole, and outside
    for r in (0.5, 2.05):
        ax.plot(r * np.cos(t), r * np.sin(t), color=GRAY, lw=1.1, ls=":")
    ienc0(ax, 0.0, 0.18, size=9.5)
    ienc0(ax, 0.02, -2.28, size=11)
    # rho runs at -70 degrees, through a gap between the inner turns
    th = np.radians(-70)
    ax.plot([0, rm * np.cos(th)], [0, rm * np.sin(th)], color=INK, lw=1)
    lab(ax, 0.06, -0.72, "ρ", size=13)
    ax.text(0, 2.3, "N turns, current I", ha="center", va="center", fontsize=12, color=GRAY)
    save(fig, "L30-toroid.svg")


# ---------------------------------------------------------------------------
def coax_flux():
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    blank(ax, (-3.6, 3.6), (-1.75, 1.75))
    a, b, L = 0.32, 1.25, 3.3
    ax.add_patch(Rectangle((-L, b), 2 * L, 0.1, fc=METAL, ec="none"))
    ax.add_patch(Rectangle((-L, -b - 0.1), 2 * L, 0.1, fc=METAL, ec="none"))
    ax.add_patch(Rectangle((-L, a), 2 * L, b - a, fc=FILL, ec="none"))
    ax.add_patch(Rectangle((-L, -b), 2 * L, b - a, fc=FILL, ec="none"))
    ax.add_patch(Rectangle((-L, -a), 2 * L, 2 * a, fc=CURRENT, ec=RED, lw=1.0))
    arrow(ax, -2.6, 0, -1.6, 0, color=RED, lw=2.0, ms=14)
    lab(ax, -2.1, 0.13, "I", size=13, color=RED, va="bottom")
    arrow(ax, -1.6, b + 0.25, -2.6, b + 0.25, color=RED, lw=1.6, ms=12)
    lab(ax, -2.1, b + 0.42, "I", size=13, color=RED)
    # the strip between the conductors, length l; above the axis B points out of the page
    x0, x1 = -0.7, 1.9
    ax.add_patch(Rectangle((x0, a), x1 - x0, b - a, fc="none", ec=NAVY, lw=1.6))
    # B falls as 1/rho across the strip, so the number of flux symbols in
    # each row does too: denser near the inner conductor
    for y in (0.47, 0.70, 0.94, 1.12):
        n = int(round(3.6 / y))
        for x in np.linspace(x0 + 0.22, x1 - 0.22, n):
            ax.add_patch(Circle((x, y), 0.07, fc="white", ec=BLUE, lw=1.3))
            ax.add_patch(Circle((x, y), 0.025, fc=BLUE, ec="none"))
    lab(ax, x1 + 0.2, (a + b) / 2, "B", color=BLUE, italic=False, ha="left")
    ax.annotate("", xy=(x1, -0.62), xytext=(x0, -0.62),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    lab(ax, (x0 + x1) / 2, -0.85, "ℓ", size=14, color=GRAY)
    ax.annotate("", xy=(3.0, a), xytext=(3.0, 0),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    lab(ax, 3.2, a / 2, "a", size=13, color=GRAY)
    ax.annotate("", xy=(3.45, b), xytext=(3.45, 0),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    lab(ax, 3.62, b / 2 + 0.2, "b", size=13, color=GRAY)
    save(fig, "L30-coax-flux.svg")


if __name__ == "__main__":
    coax()
    sheet()
    solenoid()
    finite_solenoid()
    toroid()
    coax_flux()
