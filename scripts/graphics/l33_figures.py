#!/usr/bin/env python3
"""L33 figures: Faraday's law, displacement current, and relaxation time.

    L33-lenz.svg         a bar magnet moving toward a ring and away from it,
                         with the induced current and the field it makes
    L33-sliding-bar.svg  a conducting bar sliding on two rails in a uniform B
                         into the page, with the induced current
    L33-capacitor.svg    a wire charging a capacitor, a path C around the wire,
                         a flat surface S1 the wire crosses and a bag S2 that
                         passes between the plates
    L33-displacement.svg the same capacitor with the repair drawn: the
                         conduction current crosses S1, the displacement
                         current crosses S2, and H circles C
    L33-coax-strip.svg   a coax in side view with the strip of length Δz,
                         its path C, and v(z), v(z+Δz) on the short sides
    L33-relaxation.svg   the free charge density in a conductor decaying as
                         exp(-t/τᵣ)

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l33_figures.py   ->   book/extras/viz/img/L33-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
GREEN = "#3f7d34"
FILL = "#e3edf6"
METAL = "#9aa8b6"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center", italic=True, bold=False):
    """A symbol with an optional subscript, in plain text (see l03_figures.py)."""
    t = ax.text(x, y, base, fontsize=size, color=color, ha=ha, va=va,
                fontstyle="italic" if italic else "normal",
                fontweight="bold" if bold else "normal")
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


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=1.8, ms=13):
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


def b_into(ax, x, y, r=0.11, color=BLUE):
    ax.add_patch(plt.Circle((x, y), r, fill=False, ec=color, lw=1.2))
    d = r * 0.62
    ax.plot([x - d, x + d], [y - d, y + d], color=color, lw=1.2)
    ax.plot([x - d, x + d], [y + d, y - d], color=color, lw=1.2)


# ---------------------------------------------------------------------------
def lenz():
    """Magnet approaching (left panel) and receding (right panel) from a ring."""
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.7))
    for ax, approach in zip(axes, (True, False)):
        blank(ax, (-0.3, 6.4), (-1.9, 2.4))
        # bar magnet, N on the right, facing the ring
        ax.add_patch(Rectangle((0.2, -0.32), 1.0, 0.64, fc="#d9e1ea", ec=GRAY, lw=1.2))
        ax.add_patch(Rectangle((1.2, -0.32), 1.0, 0.64, fc="#f3d9d9", ec=RED, lw=1.2))
        ax.text(0.7, 0, "S", ha="center", va="center", fontsize=19, color=GRAY, fontweight="bold")
        ax.text(1.7, 0, "N", ha="center", va="center", fontsize=19, color=RED, fontweight="bold")
        # the magnet's field lines leaving N, spreading toward the ring
        for yy in (-0.9, -0.45, 0.0, 0.45, 0.9):
            xs = np.linspace(2.25, 5.9, 60)
            ys = yy * (1 + 0.55 * (xs - 2.25) / 3.6) * 0.55 + 0.0
            ax.plot(xs, ys, color=BLUE, lw=1.1, alpha=0.75)
        arrow(ax, 5.55, 0.0, 5.95, 0.0, color=BLUE, lw=1.2, ms=10)
        lab(ax, 5.95, 0.5, "B", color=BLUE, size=20, ha="left", bold=True)
        # the ring, seen nearly edge on
        ax.add_patch(Ellipse((4.3, 0), 0.62, 2.5, fill=False, ec=INK, lw=2.2))
        # motion of the magnet
        if approach:
            arrow(ax, 0.5, -1.0, 1.7, -1.0, color=INK, lw=1.8)
        else:
            arrow(ax, 1.7, -1.0, 0.5, -1.0, color=INK, lw=1.8)
        lab(ax, 1.1, -1.45, "v", size=20, bold=True)
        # induced field inside the ring opposes the change in flux
        if approach:
            arrow(ax, 4.75, 0.55, 3.75, 0.55, color=AMBER, lw=2.4, ms=15)
        else:
            arrow(ax, 3.85, 0.55, 4.85, 0.55, color=AMBER, lw=2.4, ms=15)
        lab(ax, 3.55, 1.95, "B", "ind", color=AMBER, size=20, bold=True)
        # induced current on the near (lower) part of the ring
        th = np.linspace(-150, -30, 40) * np.pi / 180
        xs, ys = 4.3 + 0.36 * np.cos(th), 1.38 * np.sin(th)
        ax.plot(xs, ys, color=RED, lw=2.0)
        if approach:   # current flows so its field points back toward the magnet
            arrow(ax, xs[-3], ys[-3], xs[-1], ys[-1], color=RED, lw=2.0)
        else:
            arrow(ax, xs[2], ys[2], xs[0], ys[0], color=RED, lw=2.0)
        lab(ax, 4.85, -1.62, "I", "ind", color=RED, size=20)
        ax.text(1.2, 1.6, "approaching" if approach else "receding",
                ha="center", fontsize=18, color=GRAY)
    save(fig, "L33-lenz.svg")


def sliding_bar():
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    blank(ax, (-0.9, 6.3), (-0.8, 3.4))
    for i in range(6):
        for j in range(4):
            x = 0.45 + i * 1.0
            if abs(x - 3.7) < 0.6:
                continue      # leave room for the bar and the current label
            b_into(ax, x, 0.3 + j * 0.85)
    lab(ax, 6.05, 3.05, "B", color=BLUE, size=16, bold=True)
    # rails and the closed end on the left
    ax.plot([5.9, 0, 0, 5.9], [0, 0, 2.6, 2.6], color=GRAY, lw=4.0, solid_capstyle="butt")
    # the sliding bar
    xb = 3.7
    ax.add_patch(Rectangle((xb - 0.09, -0.25), 0.18, 3.1, fc=METAL, ec=INK, lw=1.2))
    arrow(ax, xb + 0.2, 1.3, xb + 1.25, 1.3, color=INK, lw=2.0)
    lab(ax, xb + 1.45, 1.3, "v", size=16, bold=True, ha="left")
    # induced current: up the bar, counterclockwise, so its own field inside
    # the loop points out of the page and opposes the growing flux into it
    arrow(ax, xb - 0.32, 0.65, xb - 0.32, 2.0, color=RED, lw=2.2)
    lab(ax, xb - 0.55, 1.3, "I", "ind", size=15, color=RED, ha="right")
    # dimensions
    ax.annotate("", xy=(xb, -0.55), xytext=(0, -0.55),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, xb / 2, -0.62, "x", size=15, color=INK, va="top")
    ax.annotate("", xy=(-0.45, 2.6), xytext=(-0.45, 0),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, -0.62, 1.3, "ℓ", size=16, ha="right")
    save(fig, "L33-sliding-bar.svg")


def capacitor(repaired=False):
    k = 1.3 if repaired else 1.0     # the repaired state sits in a half-width column
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    blank(ax, (-0.2, 8.0), (-2.0, 2.2))
    # wire in from the left to the left plate, out of the right plate
    ax.plot([0, 3.4], [0, 0], color=INK, lw=2.4)
    ax.plot([4.6, 7.8], [0, 0], color=INK, lw=2.4)
    for xp in (3.4, 4.6):
        ax.add_patch(Rectangle((xp - 0.07, -0.8), 0.14, 1.6, fc=METAL, ec=INK, lw=1.0))
    ax.text(3.4, -1.55, "+Q", ha="center", fontsize=14 * k, color=RED)
    ax.text(4.6, -1.55, "−Q", ha="center", fontsize=14 * k, color=NAVY)
    # D between the plates, growing as the plates charge
    for yy in (-0.55, -0.18, 0.18, 0.55):
        arrow(ax, 3.55, yy, 4.42, yy, color=AMBER, lw=1.4, ms=10)
    lab(ax, 5.0, 0.55, "D", color=AMBER, size=15 * k, bold=True)
    # conduction current in the wire
    arrow(ax, 0.3, 0.32, 1.1, 0.32, color=RED, lw=2.0)
    lab(ax, 0.7, 0.68, "i", size=16 * k, color=RED)
    # the path C around the wire, drawn edge on as an ellipse
    xc = 2.0
    ax.add_patch(Ellipse((xc, 0), 0.5, 2.2, fill=False, ec=NAVY, lw=2.0))
    lab(ax, xc - 0.45, 1.25, "C", color=NAVY, size=16 * k, ha="right")
    # S1: the flat disk inside C, which the wire crosses
    ax.add_patch(Ellipse((xc, 0), 0.5, 2.2, fc=FILL, ec="none", alpha=0.8, zorder=0))
    lab(ax, xc - 0.1, -1.55, "S", "1", color=NAVY, size=15 * k)
    # S2: a bag from C that bulges between the plates without touching the wire
    # it runs past the edge of the + plate and closes in the gap
    xa = np.linspace(xc, 3.7, 40)
    th = np.linspace(np.pi / 2, -np.pi / 2, 80)
    xr = 3.7 + 0.32 * np.cos(th)
    yr = 1.1 * np.sin(th)
    xs = np.concatenate([xa, xr, xa[::-1]])
    ys = np.concatenate([np.full_like(xa, 1.1), yr, np.full_like(xa, -1.1)])
    ax.plot(xs, ys, color=GREEN, lw=1.8, ls="--")
    lab(ax, 2.7, 1.45, "S", "2", color=GREEN, size=15 * k)
    if not repaired:
        save(fig, "L33-capacitor.svg")
        return
    # the repair: H circles C, and the displacement current crosses S2
    th = np.radians(np.linspace(200, 160, 12))      # front of C, left side
    hx, hy = xc + 0.25 * np.cos(th), 1.1 * np.sin(th)
    ax.plot(hx, hy, color=NAVY, lw=2.6)
    arrow(ax, hx[-2], hy[-2], hx[-1] - 0.01, hy[-1] + 0.06, color=NAVY, lw=2.6, ms=15)
    lab(ax, xc - 0.38, 0.5, "H", color=NAVY, size=17 * k, bold=True, ha="right")
    ax.text(4.0, 1.75, "displacement current i", ha="center", fontsize=13 * k, color=AMBER)
    ax.text(0.55, -1.3, "conduction\ncurrent i", ha="center", fontsize=11 * k, color=RED)
    save(fig, "L33-displacement.svg")


def b_out(ax, x, y, r=0.11, color=BLUE):
    ax.add_patch(plt.Circle((x, y), r, fill=False, ec=color, lw=1.2))
    ax.add_patch(plt.Circle((x, y), r * 0.28, color=color))


def coax_strip():
    """Side view of a coax: inner conductor, shield, and the strip of length Δz."""
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    blank(ax, (-0.6, 8.2), (-1.0, 2.75))
    # inner conductor and the upper half of the shield, in section
    ax.add_patch(Rectangle((0, -0.25), 7.6, 0.5, fc=METAL, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((0, 1.75), 7.6, 0.18, fc=METAL, ec=INK, lw=1.0))
    # currents
    arrow(ax, 0.3, 0.0, 1.5, 0.0, color=RED, lw=2.2)
    lab(ax, 0.9, -0.62, "i", size=20, color=RED)
    arrow(ax, 7.3, 2.25, 6.1, 2.25, color=RED, lw=2.2)
    lab(ax, 6.7, 2.55, "i", size=20, color=RED)
    # the strip between the conductors
    z0, z1, y0, y1 = 2.6, 5.0, 0.25, 1.75
    ax.add_patch(Rectangle((z0, y0), z1 - z0, y1 - y0, fc=FILL, ec="none", zorder=0))
    for xx in np.linspace(z0 + 0.45, z1 - 0.45, 4):
        for yy in (0.72, 1.28):
            b_out(ax, xx, yy, r=0.12)
    lab(ax, z1 + 0.2, 1.42, "B", color=BLUE, size=19, bold=True, ha="left")
    # the path C, counterclockwise: along the inner conductor, up, back, down
    pc = dict(color=NAVY, lw=2.0)
    ax.plot([z0, z1, z1, z0, z0], [y0, y0, y1, y1, y0], **pc)
    arrow(ax, (z0 + z1) / 2 - 0.2, y0, (z0 + z1) / 2 + 0.2, y0, color=NAVY, lw=2.0)
    arrow(ax, z1, (y0 + y1) / 2 - 0.2, z1, (y0 + y1) / 2 + 0.2, color=NAVY, lw=2.0)
    arrow(ax, (z0 + z1) / 2 + 0.2, y1, (z0 + z1) / 2 - 0.2, y1, color=NAVY, lw=2.0)
    arrow(ax, z0, (y0 + y1) / 2 + 0.2, z0, (y0 + y1) / 2 - 0.2, color=NAVY, lw=2.0)
    lab(ax, z0 - 0.2, y1 - 0.22, "C", color=NAVY, size=19, ha="right")
    # voltages on the short sides
    lab(ax, z0 - 0.15, 1.0, "v(z)", size=18, ha="right", italic=False)
    lab(ax, z1 + 0.2, 0.62, "v(z+Δz)", size=18, ha="left", italic=False)
    # length of the strip
    ax.annotate("", xy=(z1, -0.62), xytext=(z0, -0.62),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, (z0 + z1) / 2, -0.9, "Δz", size=19, va="center")
    save(fig, "L33-coax-strip.svg")


def relaxation():
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    t = np.linspace(0, 4.2, 300)
    ax.plot(t, np.exp(-t), color=NAVY, lw=2.6)
    ax.plot([0, 1, 1], [np.exp(-1), np.exp(-1), 0], color=GRAY, lw=1.1, ls="--")
    ax.plot(1, np.exp(-1), "o", color=NAVY, ms=6)
    ax.set_xlim(0, 4.3); ax.set_ylim(0, 1.08)
    ax.set_xticks([0, 1, 2, 3, 4]); ax.set_xticklabels(["0", "τᵣ", "2τᵣ", "3τᵣ", "4τᵣ"])
    ax.set_yticks([0, np.exp(-1), 1]); ax.set_yticklabels(["0", "0.37", "1"])
    ax.set_xlabel("time t", color=GRAY, fontsize=12)
    ax.text(0.15, 1.02, "ρᵥ / ρ₀", color=GRAY, fontsize=12, va="bottom")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=12)
    ax.grid(True, color="#e3edf6", lw=1.0)
    save(fig, "L33-relaxation.svg")


if __name__ == "__main__":
    lenz()
    sliding_bar()
    capacitor()
    capacitor(repaired=True)
    coax_strip()
    relaxation()
