#!/usr/bin/env python3
"""L30 figures: Ampere's law for the coax, the current sheet, the solenoid, and
the toroid, and the flux that gives the coaxial inductance.

    L30-coax.svg        coax cross section with three Amperian circles, and H
                        against radius
    L30-sheet.svg       edge view of a current sheet with a rectangular
                        Amperian path through it
    L30-solenoid.svg    side section of a long solenoid with a rectangular
                        Amperian path, one side inside the coil
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


def style_plot(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY)


# ---------------------------------------------------------------------------
def coax():
    a, b = 0.55, 1.5
    fig, (ax, ay) = plt.subplots(1, 2, figsize=(9.6, 4.0), gridspec_kw={"width_ratios": [1, 1.25]})
    blank(ax, (-2.1, 2.1), (-2.0, 2.0))
    ax.add_patch(Circle((0, 0), b + 0.09, fc=METAL, ec="none"))
    ax.add_patch(Circle((0, 0), b, fc=FILL, ec="none"))
    ax.add_patch(Circle((0, 0), a, fc=CURRENT, ec=RED, lw=1.2))
    dot(ax, 0, 0, r=0.13)
    for th in np.radians(np.arange(0, 360, 45)):
        cross(ax, (b + 0.045) * np.cos(th), (b + 0.045) * np.sin(th), r=0.075)
    t = np.linspace(0, 2 * np.pi, 300)
    for r, txt, ang in ((0.32, "1", 40), (1.0, "2", 40), (1.85, "3", 40)):
        ax.plot(r * np.cos(t), r * np.sin(t), color=NAVY, lw=1.3, ls="--")
        th = np.radians(ang)
        ax.text((r + 0.12) * np.cos(th), (r + 0.12) * np.sin(th), txt, fontsize=12, color=NAVY,
                ha="center", va="center", fontweight="bold")
    ax.plot([0, -a * np.cos(np.radians(30))], [0, -a * np.sin(np.radians(30))], color=INK, lw=1)
    lab(ax, -0.3, -0.33, "a", size=13)
    ax.plot([0, -b * np.cos(np.radians(-60))], [0, b * np.sin(np.radians(-60))], color=INK, lw=1)
    lab(ax, -0.55, -0.95, "b", size=13)

    rho = np.linspace(0, 2.4, 700)
    H = np.where(rho < a, rho / a, np.where(rho < b, a / np.maximum(rho, 1e-9), 0.0))
    ay.axvspan(0, a, color=CURRENT, alpha=0.7, lw=0)
    ay.axvspan(a, b, color=FILL, alpha=0.8, lw=0)
    ay.plot(rho, H, color=NAVY, lw=2.4)
    ay.set_xlim(0, 2.4); ay.set_ylim(0, 1.18)
    ay.set_xticks([0, a, b]); ay.set_xticklabels(["0", "a", "b"], fontsize=13)
    ay.set_yticks([0, 1]); ay.set_yticklabels(["0", "I/2πa"], fontsize=13)
    ay.set_xlabel("ρ", fontsize=14, fontstyle="italic", color=INK)
    ay.text(0.06, 0.9, "∝ ρ", fontsize=13, color=NAVY)
    ay.text(0.95, 0.62, "∝ 1/ρ", fontsize=13, color=NAVY)
    ay.text(1.75, 0.08, "0", fontsize=13, color=NAVY)
    lab(ay, 2.15, 0.5, "H", "φ", color=NAVY)
    style_plot(ay)
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
    lab(ax, -2.0, 1.12, "H", color=BLUE, italic=False)
    lab(ax, 2.0, -1.12, "H", color=BLUE, italic=False)
    ax.annotate("", xy=(x1, 1.45), xytext=(x0, 1.45),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    lab(ax, 0, 1.62, "w", size=13, color=GRAY)
    lab(ax, 1.05, 0.45, "C", size=13, color=NAVY)
    lab(ax, 2.75, 0.32, "J", "s", size=13, color=RED)
    ax.text(-2.95, 1.5, "z", fontsize=13, fontstyle="italic", color=GRAY)
    arrow(ax, -2.85, 1.0, -2.85, 1.35, color=GRAY, lw=1.0, ms=9)
    save(fig, "L30-sheet.svg")


# ---------------------------------------------------------------------------
def solenoid():
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    blank(ax, (-3.9, 3.9), (-1.85, 1.85))
    R = 0.85
    xs = np.arange(-3.4, 3.45, 0.3)
    for x in xs:
        dot(ax, x, R, r=0.1)
        cross(ax, x, -R, r=0.1)
    for x in (-2.6, -1.0, 0.6, 2.2):
        arrow(ax, x - 0.4, 0, x + 0.4, 0, color=BLUE, lw=2.0, ms=14)
    lab(ax, -2.6, 0.28, "H", color=BLUE, italic=False)
    # the Amperian rectangle: one long side inside, one outside
    x0, x1, yin, yout = -0.6, 1.2, 0.35, 1.45
    ax.plot([x0, x1, x1, x0, x0], [yin, yin, yout, yout, yin], color=NAVY, lw=1.6)
    arrow(ax, 0.0, yin, 0.45, yin, color=NAVY)
    arrow(ax, x1, 0.65, x1, 1.05, color=NAVY)
    arrow(ax, 0.6, yout, 0.15, yout, color=NAVY)
    arrow(ax, x0, 1.15, x0, 0.75, color=NAVY)
    ax.annotate("", xy=(x1, 1.7), xytext=(x0, 1.7),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    lab(ax, 0.3, 1.85, "ℓ′", size=13, color=GRAY)
    lab(ax, 1.5, 1.62, "C", size=13, color=NAVY)
    ax.text(3.75, 0, "z", fontsize=13, fontstyle="italic", color=GRAY, va="center")
    ax.text(-3.7, -1.55, "n turns per meter, current I", fontsize=12, color=GRAY)
    save(fig, "L30-solenoid.svg")


# ---------------------------------------------------------------------------
def toroid():
    fig, ax = plt.subplots(figsize=(4.4, 4.2))
    blank(ax, (-2.1, 2.1), (-2.05, 2.05))
    r1, r2 = 1.05, 1.75
    ax.add_patch(Circle((0, 0), r2, fc=FILL, ec=GRAY, lw=1.0))
    ax.add_patch(Circle((0, 0), r1, fc="white", ec=GRAY, lw=1.0))
    for th in np.radians(np.arange(0, 360, 20)):
        dot(ax, (r1 - 0.06) * np.cos(th), (r1 - 0.06) * np.sin(th), r=0.075)
        cross(ax, (r2 + 0.06) * np.cos(th), (r2 + 0.06) * np.sin(th), r=0.075)
    rm = 1.4
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(rm * np.cos(t), rm * np.sin(t), color=NAVY, lw=1.5, ls="--")
    for th in np.radians([30, 150, 270]):
        x, y = rm * np.cos(th), rm * np.sin(th)
        arrow(ax, x, y, x - 0.42 * np.sin(th), y + 0.42 * np.cos(th), color=BLUE, lw=2.0, ms=14)
    lab(ax, 1.1, 0.92, "H", color=BLUE, italic=False)
    ax.plot([0, rm * np.cos(np.radians(-60))], [0, rm * np.sin(np.radians(-60))], color=INK, lw=1)
    lab(ax, 0.55, -0.42, "ρ", size=13)
    ax.text(0, 0, "N turns", ha="center", va="center", fontsize=12, color=GRAY)
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
    for x in np.linspace(x0 + 0.3, x1 - 0.3, 5):
        for y in (a + 0.2, (a + b) / 2, b - 0.2):
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
    toroid()
    coax_flux()
