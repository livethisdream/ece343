#!/usr/bin/env python3
"""L37 figures: the uniform plane wave and its polarization.

    L37-wavefronts.svg   circular wavefronts around a small source, and a
                         patch far from it where the fronts are nearly flat
    L37-fields.svg       one snapshot of a plane wave along z: E along x, H
                         along y, and the direction of travel
    L37-polarization.svg the path the tip of E traces in the transverse plane
                         for a linear, a circular, and an elliptical wave
    L37-handedness.svg   right- and left-hand circular polarization for a wave
                         traveling out of the page, with the tip's position at
                         t = 0 and t = T/4

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l37_figures.py   ->   book/extras/viz/img/L37-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GREEN, GRAY, INK = (
    "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#1d7a4d", "#5b6573", "#15202b")
ECOL, HCOL = "#0067b9", "#b3213a"     # E blue, H red, as in the widgets
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center", italic=True,
        bold=False):
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


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=1.6, ms=12, z=5):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0), zorder=z)


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


def out_of_page(ax, x, y, r=0.11, color=INK):
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.5, zorder=6))
    ax.add_patch(Circle((x, y), r * 0.32, fc=color, ec="none", zorder=7))


# ---------------------------------------------------------------------------
def wavefronts():
    """Spherical fronts near a small source are nearly flat over a small patch far away."""
    fig, (ax, az) = plt.subplots(1, 2, figsize=(9.0, 3.9), gridspec_kw={"width_ratios": [1.35, 1]})
    blank(ax, (-0.6, 6.6), (-2.6, 2.6))
    ax.add_patch(Circle((0, 0), 0.12, fc=NAVY, ec="none", zorder=5))
    lab(ax, 0, -0.45, "source", size=12, color=NAVY, italic=False)
    for r in np.arange(0.5, 6.41, 0.5):
        th = np.linspace(-np.arcsin(min(1, 2.5 / r)), np.arcsin(min(1, 2.5 / r)), 200)
        ax.plot(r * np.cos(th), r * np.sin(th), color=BLUE, lw=1.2, alpha=0.75)
    # the patch far from the source
    x0, half = 5.25, 0.9
    ax.add_patch(plt.Rectangle((x0 - half, -half), 2 * half, 2 * half, fc="none", ec=AMBER,
                               lw=1.8, zorder=6))
    arrow(ax, x0 + half + 0.05, 0.0, 6.55, 0.0, color=AMBER, lw=1.2, ms=10)

    # zoom: the same fronts across the patch, now nearly straight and parallel
    blank(az, (-1.25, 1.35), (-1.25, 1.25))
    az.add_patch(plt.Rectangle((-1.1, -1.1), 2.2, 2.2, fc="none", ec=AMBER, lw=1.8))
    scale = 1.1 / half
    for r in np.arange(0.5, 6.41, 0.5):
        if abs(r - x0) > half + 0.2:
            continue
        yy = np.linspace(-half, half, 100)
        xx = np.sqrt(np.maximum(r * r - yy * yy, 0)) - x0
        m = np.abs(xx * scale) <= 1.1
        az.plot((xx * scale)[m], (yy * scale)[m], color=BLUE, lw=1.8)
    arrow(az, -0.95, -0.75, -0.05, -0.75, color=NAVY, lw=2.0, ms=14)
    lab(az, -0.5, -0.95, "k̂", size=16, color=NAVY, bold=True, italic=False)
    save(fig, "L37-wavefronts.svg")


# ---------------------------------------------------------------------------
def fields():
    """A snapshot of E (along x) and H (along y) on a wave traveling along +z."""
    # Oblique projection: z to the right, x up, y toward the viewer (down-left).
    ex, ey, ez = np.array([0, 1.0]), np.array([-0.3, -0.62]), np.array([1.0, 0])
    P = lambda x, y, z: x * ex + y * ey + z * ez
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    ax.set_aspect("equal"); ax.axis("off")
    L, A, Ah = 9.0, 1.35, 1.05
    z = np.linspace(0, L, 600)
    k = 2 * np.pi / 4.0
    # axes
    for v, name, length in ((P(0, 0, L + 0.8), "z", 1), (P(A + 0.5, 0, 0), "x", 1),
                            (P(0, Ah + 0.9, 0), "y", 1)):
        arrow(ax, 0, 0, v[0], v[1], color=GRAY, lw=1.1, ms=10, z=2)
        off = {"z": (0.25, 0), "x": (0, 0.25), "y": (-0.2, -0.22)}[name]
        lab(ax, v[0] + off[0], v[1] + off[1], name, size=15, color=GRAY)
    # E in the xz plane, H in the yz plane
    Ex = A * np.cos(k * z)
    Hy = Ah * np.cos(k * z)
    pe = np.array([P(Ex[i], 0, z[i]) for i in range(len(z))])
    ph = np.array([P(0, Hy[i], z[i]) for i in range(len(z))])
    for zi in np.arange(0, L + 1e-9, 0.25):
        a = P(A * np.cos(k * zi), 0, zi); b0 = P(0, 0, zi)
        ax.plot([b0[0], a[0]], [b0[1], a[1]], color=ECOL, lw=0.9, alpha=0.55)
        hb = P(0, Ah * np.cos(k * zi), zi)
        ax.plot([b0[0], hb[0]], [b0[1], hb[1]], color=HCOL, lw=0.9, alpha=0.55)
    ax.plot(ph[:, 0], ph[:, 1], color=HCOL, lw=2.4)
    ax.plot(pe[:, 0], pe[:, 1], color=ECOL, lw=2.4)
    # labels on the first crest
    pE = P(A, 0, 0); lab(ax, pE[0] + 0.45, pE[1] + 0.2, "E", size=17, color=ECOL, bold=True,
                         italic=False)
    pH = P(0, Ah, 0); lab(ax, pH[0] - 0.4, pH[1] - 0.05, "H", size=17, color=HCOL, bold=True,
                          italic=False)
    # direction of travel
    s = P(0, 0, L * 0.62); s[1] += 2.0
    arrow(ax, s[0], s[1], s[0] + 1.6, s[1], color=NAVY, lw=2.2, ms=16)
    lab(ax, s[0] + 0.8, s[1] + 0.32, "k̂", size=17, color=NAVY, bold=True, italic=False)
    # one wavelength
    y0 = -1.75
    ax.annotate("", xy=(4.0, y0), xytext=(0.0, y0),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.1, shrinkA=0, shrinkB=0))
    lab(ax, 2.0, y0 - 0.3, "λ", size=16)
    ax.set_xlim(-1.4, L + 1.4); ax.set_ylim(-2.3, 2.8)
    save(fig, "L37-fields.svg")


# ---------------------------------------------------------------------------
def trace_axes(ax, r=1.35, k_out=True):
    blank(ax, (-1.6, 1.6), (-1.6, 1.75))
    arrow(ax, -r, 0, r, 0, color=GRAY, lw=1.0, ms=9, z=1)
    arrow(ax, 0, -r, 0, r, color=GRAY, lw=1.0, ms=9, z=1)
    lab(ax, r + 0.06, -0.17, "x", size=14, color=GRAY)
    lab(ax, -0.17, r + 0.04, "y", size=14, color=GRAY)
    if k_out:
        out_of_page(ax, 0, 0, r=0.1, color=NAVY)


def direction_marks(ax, x, y, color, n=(0.32, 0.57)):
    """Two arrowheads along a closed path, showing the sense of rotation in time."""
    N = len(x)
    for f in n:
        i = int(f * N) % N
        j = (i + 4) % N
        ax.annotate("", xy=(x[j], y[j]), xytext=(x[i], y[i]),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16,
                                    shrinkA=0, shrinkB=0), zorder=6)


def polarization():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.6))
    t = np.linspace(0, 2 * np.pi, 400)
    cases = [("linear", 0.6 * np.sqrt(2), 0.6 * np.sqrt(2), 0.0),     # tilted 45°
             ("circular", 1.0, 1.0, -np.pi / 2),
             ("elliptical", 1.0, 1.0, 3 * np.pi / 4)]
    for ax, (name, a, b, d) in zip(axs, cases):
        trace_axes(ax)
        x, y = a * np.cos(t), b * np.cos(t + d)
        ax.plot(x, y, color=ECOL, lw=2.6, zorder=4)
        if name != "linear":
            direction_marks(ax, x, y, ECOL)
        else:
            ax.plot([x[0]], [y[0]], "o", color=ECOL, ms=5)
            ax.plot([-x[0]], [-y[0]], "o", color=ECOL, ms=5)
        ax.text(0, -1.62, name, ha="center", va="center", fontsize=15, color=INK)
    save(fig, "L37-polarization.svg")


def handedness():
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.8))
    t = np.linspace(0, 2 * np.pi, 400)
    for ax, (name, d, col) in zip(axs, [("right-hand", -np.pi / 2, GREEN),
                                        ("left-hand", np.pi / 2, AMBER)]):
        trace_axes(ax)
        x, y = np.cos(t), np.cos(t + d)
        ax.plot(x, y, color=col, lw=2.6, zorder=4)
        direction_marks(ax, x, y, col, n=(0.08, 0.58))
        # tip at t = 0 and t = T/4
        for tt, txt, off in ((0.0, "t = 0", (0.08, 0.2)),
                             (np.pi / 2, "t = T/4", (0.12, 0.17))):
            px, py = np.cos(tt), np.cos(tt + d)
            ax.plot([px], [py], "o", color=col, ms=8, zorder=7, mec="white", mew=1.2)
            ox = off[0] if px >= 0 else -off[0]
            oy = off[1] if py >= 0 else -off[1] - 0.05
            ha = "left" if px >= 0 else "right"
            if abs(px) < 0.1:
                ha, ox = "left", 0.12
            ax.text(px + ox, py + oy, txt, fontsize=12.5, color=col, ha=ha, va="center",
                    fontstyle="italic")
        ax.text(0, -1.62, name, ha="center", va="center", fontsize=15, color=INK)
    save(fig, "L37-handedness.svg")


if __name__ == "__main__":
    wavefronts()
    fields()
    polarization()
    handedness()
