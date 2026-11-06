#!/usr/bin/env python3
"""L34 figures: Faraday's law on a wire loop, and the ideal transformer.

    L34-loop.svg         a wire loop of radius a in the xy plane with a resistor
                         in a small gap, and a uniform B along +z through it
    L34-ramp.svg         Example 1: B(t) ramps from 0 to B0 over t0, and the
                         resistor voltage is a constant pulse during the ramp
    L34-sine.svg         Example 2: B(t) = B0 sin(2πft), and the EMF around
                         the loop, which lags B by a quarter period
    L34-transformer.svg  a closed core with two windings, N1 and N2 turns, the
                         core flux Φ, and the terminal voltages and currents
    L34-equations.svg    four panels, one per law: D leaving a charge, closed
                         B lines, E circling a growing B, H circling a current

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l34_figures.py   ->   book/extras/viz/img/L34-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL = "#e3edf6"      # core
METAL = "#9aa8b6"     # wire
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})

# Example values (the lesson recomputes every number from these).
A_LOOP, B0, T0, R, F = 0.10, 0.2, 3.0, 1e3, 1e3


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
                fontsize=size * 0.72, color=color, ha="left", va="center",
                fontstyle="italic" if italic else "normal")
    return t


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def arrow(ax, p, q, color=INK, lw=1.8, ms=14, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0))


def loop():
    """Oblique view of the loop: the xy plane is squashed vertically."""
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    sq = 0.38                                   # vertical squash of the xy plane
    th = np.linspace(0, 2 * np.pi, 400)
    gap = np.deg2rad(9)                         # half-angle of the gap at phi = -90 deg
    keep = np.abs(((th + np.pi / 2 + np.pi) % (2 * np.pi)) - np.pi) > gap
    x, y = np.cos(th), sq * np.sin(th)
    xs, ys = np.where(keep, x, np.nan), np.where(keep, y, np.nan)
    # B arrows behind the loop's front edge first, then the wire, then the front arrows
    pts = [(-0.55, 0.05), (0.0, 0.16), (0.55, 0.05), (-0.3, -0.12), (0.3, -0.12)]
    for (px, py) in pts:
        arrow(ax, (px, py), (px, py + 1.05), color=BLUE, lw=1.6, ms=12)
    ax.plot(xs, ys, color=NAVY, lw=3.2, solid_capstyle="round")
    # resistor across the gap (front, at phi = -90 deg)
    gx = np.sin(gap)
    zig = np.linspace(-gx, gx, 9)
    zy = -sq + 0.045 * np.array([0, 1, -1, 1, -1, 1, -1, 1, 0])
    ax.plot(zig, zy, color=INK, lw=2.0)
    ax.text(0.0, -sq - 0.17, "R", fontsize=15, fontstyle="italic", ha="center", va="top")
    # radius
    ax.plot([0, np.cos(np.deg2rad(20))], [0, sq * np.sin(np.deg2rad(20))], color=GRAY, lw=1.2)
    ax.text(0.5, 0.17, "a", fontsize=15, fontstyle="italic", color=GRAY, ha="center")
    ax.text(0.62, 1.12, "B(t)", fontsize=16, color=BLUE, ha="left", va="center")
    # positive direction of travel (counterclockwise seen from +z)
    ta = np.linspace(np.deg2rad(200), np.deg2rad(240), 30)
    rr = 1.16
    ax.plot(rr * np.cos(ta), rr * sq * np.sin(ta), color=AMBER, lw=1.8)
    arrow(ax, (rr * np.cos(ta[-2]), rr * sq * np.sin(ta[-2])),
          (rr * np.cos(ta[-1]), rr * sq * np.sin(ta[-1])), color=AMBER, lw=1.8, ms=14)
    ax.text(-1.3, -0.12, "C", fontsize=15, fontstyle="italic", color=AMBER, ha="center")
    # axes key
    ox, oy = -1.25, -0.72
    arrow(ax, (ox, oy), (ox + 0.32, oy), color=GRAY, lw=1.2, ms=10)
    arrow(ax, (ox, oy), (ox + 0.2, oy + 0.11), color=GRAY, lw=1.2, ms=10)
    arrow(ax, (ox, oy), (ox, oy + 0.32), color=GRAY, lw=1.2, ms=10)
    for (tx, ty, s) in [(ox + 0.4, oy, "x"), (ox + 0.26, oy + 0.16, "y"), (ox, oy + 0.4, "z")]:
        ax.text(tx, ty, s, fontsize=12, fontstyle="italic", color=GRAY, ha="center", va="center")
    ax.set_xlim(-1.5, 1.3); ax.set_ylim(-0.85, 1.3)
    ax.set_aspect("equal"); ax.axis("off")
    save(fig, "L34-loop.svg")


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=11)
    ax.grid(True, color="#e3edf6", lw=1.0)


def ramp():
    area = np.pi * A_LOOP ** 2
    v = area * B0 / T0 * 1e3                    # mV
    t = np.linspace(-1, 5, 1201)
    B = np.clip(t / T0, 0, 1) * B0
    vr = np.where((t > 0) & (t < T0), v, 0.0)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.2, 4.4), sharex=True)
    a1.plot(t, B, color=BLUE, lw=2.6)
    a1.set_ylabel("B (T)", color=GRAY, fontsize=12)
    a1.set_ylim(-0.02, 0.26); a1.set_yticks([0, 0.1, 0.2])
    a2.plot(t, vr, color=AMBER, lw=2.6)
    a2.set_ylabel("|v| (mV)", color=GRAY, fontsize=12)
    a2.set_ylim(-0.2, 2.6); a2.set_yticks([0, 1, 2])
    a2.annotate(f"{v:.2f} mV", (1.5, v), xytext=(0, 8), textcoords="offset points",
                ha="center", color=AMBER, fontsize=12)
    a2.set_xlabel("t (s)", color=GRAY, fontsize=12)
    a2.set_xticks([0, 1, 2, 3, 4, 5])
    for ax in (a1, a2):
        style(ax)
        ax.axvline(0, color=GRAY, lw=0.8, ls=":")
        ax.axvline(T0, color=GRAY, lw=0.8, ls=":")
    fig.tight_layout()
    save(fig, "L34-ramp.svg")


def sine():
    area = np.pi * A_LOOP ** 2
    w = 2 * np.pi * F
    t = np.linspace(0, 2e-3, 800)
    B = B0 * np.sin(w * t)
    vr = -area * B0 * w * np.cos(w * t)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.2, 4.4), sharex=True)
    a1.plot(t * 1e3, B, color=BLUE, lw=2.6)
    a1.set_ylabel("B (T)", color=GRAY, fontsize=12)
    a1.set_yticks([-0.2, 0, 0.2])
    a2.plot(t * 1e3, vr, color=AMBER, lw=2.6)
    a2.set_ylabel("v (V)", color=GRAY, fontsize=12)
    a2.set_yticks([-40, 0, 40])
    a2.set_xlabel("t (ms)", color=GRAY, fontsize=12)
    a2.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    for ax in (a1, a2):
        style(ax)
        ax.axhline(0, color=GRAY, lw=0.8)
    fig.tight_layout()
    save(fig, "L34-sine.svg")


def transformer():
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    # core: outer and inner rectangles
    ax.add_patch(Rectangle((0, 0), 6, 4, facecolor=FILL, edgecolor=GRAY, lw=1.4))
    ax.add_patch(Rectangle((1.1, 1.1), 3.8, 1.8, facecolor="white", edgecolor=GRAY, lw=1.4))
    # flux path (dashed, clockwise) through the middle of the core
    path = np.array([[0.55, 0.55], [5.45, 0.55], [5.45, 3.45], [0.55, 3.45], [0.55, 0.55]])
    ax.plot(path[:, 0], path[:, 1], color=BLUE, lw=1.4, ls="--")
    arrow(ax, (3.2, 3.45), (2.8, 3.45), color=BLUE, lw=1.4, ms=14)
    arrow(ax, (2.8, 0.55), (3.2, 0.55), color=BLUE, lw=1.4, ms=14)
    ax.text(3.0, 3.1, "Φ", fontsize=16, color=BLUE, ha="center", va="center")
    # windings: turns drawn across each leg
    for xleg, n in ((0.55, 6), (5.45, 4)):
        for k in range(n):
            yk = 1.25 + k * (1.5 / max(n - 1, 1))
            ax.plot([xleg - 0.75, xleg + 0.75], [yk - 0.12, yk + 0.12], color=AMBER, lw=2.4,
                    solid_capstyle="round")
    # leads and terminals
    for (x0, x1, ytop, ybot) in ((-0.2, -1.2, 2.75 + 0.12, 1.25 - 0.12),
                                  (6.2, 7.2, 2.75 + 0.12, 1.25 - 0.12)):
        ax.plot([x0, x1], [ytop, ytop], color=AMBER, lw=1.8)
        ax.plot([x0, x1], [ybot, ybot], color=AMBER, lw=1.8)
        ax.plot([x1], [ytop], "o", color=INK, ms=5)
        ax.plot([x1], [ybot], "o", color=INK, ms=5)
    lab(ax, -1.55, 2.0, "v", "1", size=16)
    lab(ax, 7.55, 2.0, "v", "2", size=16)
    ax.text(-1.5, 3.05, "+", fontsize=15, ha="center"); ax.text(-1.5, 0.75, "−", fontsize=15, ha="center")
    ax.text(7.5, 3.05, "+", fontsize=15, ha="center"); ax.text(7.5, 0.75, "−", fontsize=15, ha="center")
    arrow(ax, (-1.0, 3.12), (-0.45, 3.12), color=INK, lw=1.2, ms=11)
    lab(ax, -0.72, 3.42, "i", "1", size=14)
    arrow(ax, (6.45, 3.12), (7.0, 3.12), color=INK, lw=1.2, ms=11)
    lab(ax, 6.72, 3.42, "i", "2", size=14)
    lab(ax, 0.55, -0.35, "N", "1", size=15)
    lab(ax, 5.45, -0.35, "N", "2", size=15)
    ax.set_xlim(-2.0, 8.0); ax.set_ylim(-0.7, 4.2)
    ax.set_aspect("equal"); ax.axis("off")
    save(fig, "L34-transformer.svg")


def circle_arrows(ax, r, color, ccw=True, n=4, lw=1.8):
    """A circle of radius r about the origin with n arrowheads along it."""
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(r * np.cos(th), r * np.sin(th), color=color, lw=lw)
    for k in range(n):
        a = 2 * np.pi * k / n + np.pi / 4
        d = 0.08 if ccw else -0.08
        arrow(ax, (r * np.cos(a), r * np.sin(a)), (r * np.cos(a + d), r * np.sin(a + d)),
              color=color, lw=lw, ms=13)


def equations():
    """One panel per law; the page states each equation and says what it means."""
    fig, axs = plt.subplots(2, 2, figsize=(6.6, 6.0))
    titles = ["Gauss's law", "Gauss's law for magnetism", "Faraday's law", "Ampere–Maxwell law"]
    for ax, t in zip(axs.flat, titles):
        ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.15, 1.25)
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(t, fontsize=16, color=INK, pad=4)
    # 1: D leaves a positive charge
    a = axs[0, 0]
    for k in range(8):
        th = 2 * np.pi * k / 8
        arrow(a, (0.28 * np.cos(th), 0.28 * np.sin(th)), (1.1 * np.cos(th), 1.1 * np.sin(th)),
              color=BLUE, lw=1.8, ms=13)
    a.add_patch(plt.Circle((0, 0), 0.2, color=RED))
    a.text(0, 0, "+", fontsize=18, color="white", ha="center", va="center", fontweight="bold")
    a.text(0.75, 1.05, "D", fontsize=17, color=BLUE, fontweight="bold", ha="center")
    # 2: closed B lines around a current loop seen edge-on: out at left, in at right
    a = axs[0, 1]
    th = np.linspace(0, 2 * np.pi, 300)
    for cx in (-0.6, 0.6):
        for r in (0.28, 0.55):
            a.plot(cx + r * np.cos(th), r * 1.25 * np.sin(th), color=BLUE, lw=1.6)
            xi = cx - np.sign(cx) * r           # the side of each loop facing the center
            arrow(a, (xi, -0.06), (xi, 0.08), color=BLUE, lw=1.6, ms=12)
    a.text(-0.6, 0.0, "⊙", fontsize=15, color=AMBER, ha="center", va="center")
    a.text(0.6, 0.0, "⊗", fontsize=15, color=AMBER, ha="center", va="center")
    a.text(1.05, 1.0, "B", fontsize=17, color=BLUE, fontweight="bold", ha="center")
    # 3: E circles a B that points out of the page and grows
    a = axs[1, 0]
    for (x, y) in [(0, 0), (0.32, 0.2), (-0.32, 0.2), (0.32, -0.2), (-0.32, -0.2)]:
        a.text(x, y, "⊙", fontsize=15, color=BLUE, ha="center", va="center")
    a.text(0, -0.55, "B growing", fontsize=15, color=BLUE, ha="center")
    circle_arrows(a, 0.95, AMBER, ccw=False)
    a.text(0.95, 0.95, "E", fontsize=17, color=AMBER, fontweight="bold", ha="center")
    # 4: H circles a current (or a changing D) out of the page
    a = axs[1, 1]
    a.text(0, 0, "⊙", fontsize=22, color=RED, ha="center", va="center")
    a.text(0, -0.45, "J or ∂D/∂t", fontsize=15, color=RED, ha="center")
    circle_arrows(a, 0.95, NAVY, ccw=True)
    a.text(0.95, 0.95, "H", fontsize=17, color=NAVY, fontweight="bold", ha="center")
    fig.tight_layout()
    save(fig, "L34-equations.svg")


if __name__ == "__main__":
    loop()
    ramp()
    sine()
    transformer()
    equations()
