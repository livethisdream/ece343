#!/usr/bin/env python3
"""L38 figures: a plane wave at normal incidence on a planar boundary.

    L38-geometry.svg  the boundary at z = 0, with the incident and reflected
                      waves in medium 1 and the transmitted wave in medium 2,
                      each drawn with its E (along x), H (along y), and
                      direction of travel
    L38-pec.svg       the standing wave in front of a perfect conductor:
                      the envelopes of |E| and |H| against z, with the E null
                      and H maximum at the wall

Labels are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l38_figures.py   ->   book/extras/viz/img/L38-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, GREEN, RED, AMBER, GRAY, INK = (
    "#004a85", "#0067b9", "#1d7a4d", "#b3213a", "#8a5a00", "#5b6573", "#15202b")
FILL1 = "#f2f7fb"     # medium 1
FILL2 = "#d6e5f2"     # medium 2
PEC = "#c9d0d8"       # a perfect conductor
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center",
        italic=True, bold=False):
    """A symbol with an optional subscript, in plain text: an SVG with
    svg.fonttype 'none' cannot carry matplotlib's math fonts into a browser."""
    t = ax.text(x, y, base, fontsize=size, color=color, ha=ha, va=va,
                fontstyle="italic" if italic else "normal",
                fontweight="bold" if bold else "normal")
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


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=2.0, ls="-", head=12):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", color=color,
                                 lw=lw, ls=ls, mutation_scale=head, shrinkA=0, shrinkB=0))


def dot_out(ax, x, y, r=0.13, color=NAVY):
    """A vector out of the page."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.8, zorder=4))
    ax.add_patch(Circle((x, y), r * 0.32, fc=color, ec="none", zorder=5))


def cross_in(ax, x, y, r=0.13, color=NAVY):
    """A vector into the page."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.8, zorder=4))
    d = r * 0.62
    ax.plot([x - d, x + d], [y - d, y + d], color=color, lw=1.6, zorder=5)
    ax.plot([x - d, x + d], [y + d, y - d], color=color, lw=1.6, zorder=5)


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def wave(ax, x0, x1, y, k, amp, color, lw=2.0, alpha=1.0):
    x = np.linspace(x0, x1, 300)
    ax.plot(x, y + amp * np.sin(k * (x - x0)), color=color, lw=lw, alpha=alpha)


def geometry():
    """Incident, reflected, and transmitted waves at a boundary at z = 0, each with
    its E (along x), H (along y), and direction of travel."""
    fig, ax = plt.subplots(figsize=(7.4, 4.9))
    ax.set_aspect("equal"); ax.axis("off")
    X0, X1, Y0, Y1 = -5.2, 4.0, -2.75, 2.65
    ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1)
    ax.add_patch(Rectangle((X0, Y0), -X0, Y1 - Y0, fc=FILL1, ec="none"))
    ax.add_patch(Rectangle((0, Y0), X1, Y1 - Y0, fc=FILL2, ec="none"))
    ax.plot([0, 0], [Y0, Y1], color=INK, lw=1.8)

    # medium labels
    ax.text(-2.6, 2.3, "medium 1:  ε₁, μ₁, η₁", fontsize=16, ha="center", va="center")
    ax.text(2.0, 2.3, "medium 2:  ε₂, μ₂, η₂", fontsize=16, ha="center", va="center")
    ax.text(0.1, Y0 + 0.15, "z = 0", fontsize=17, color=GRAY, ha="left", va="bottom",
            fontstyle="italic")

    k1, k2 = 2 * np.pi / 1.6, 2 * np.pi / 1.13      # shorter wavelength in medium 2
    S = 18                                           # label size

    def fields(x, y, color, h_out, e_name, h_name):
        """E up along x at (x, y) and H out of (dot) or into (cross) the page."""
        arrow(ax, x, y - 0.05, x, y + 0.8, color=color, lw=2.4, head=14)
        lab(ax, x - 0.3, y + 0.62, "E", e_name, size=S, color=color, ha="right",
            bold=True, italic=False)
        hx = x + 0.6
        (dot_out if h_out else cross_in)(ax, hx, y, r=0.17, color=color)
        lab(ax, hx + 0.27, y - 0.02, "H", h_name, size=S, color=color, ha="left",
            bold=True, italic=False)

    # incident wave, upper row, traveling +z
    yi = 1.05
    wave(ax, -4.7, -0.15, yi, k1, 0.3, BLUE, alpha=0.6)
    fields(-4.0, yi, NAVY, True, "", "")
    ax.texts[-2].set_text("Eᵢ"); ax.texts[-1].set_text("Hᵢ")
    arrow(ax, -2.1, yi + 0.68, -1.0, yi + 0.68, color=BLUE, lw=2.2, head=14)
    lab(ax, -0.85, yi + 0.68, "kᵢ", size=S, color=BLUE, ha="left", bold=True, italic=False)

    # reflected wave, lower row, traveling -z: H reverses (into the page)
    yr = -1.15
    wave(ax, -4.7, -0.15, yr, k1, 0.2, RED, alpha=0.6)
    fields(-4.0, yr, RED, False, "", "")
    ax.texts[-2].set_text("Eᵣ"); ax.texts[-1].set_text("Hᵣ")
    arrow(ax, -1.0, yr - 0.62, -2.1, yr - 0.62, color=RED, lw=2.2, head=14)
    lab(ax, -0.85, yr - 0.62, "kᵣ", size=S, color=RED, ha="left", bold=True, italic=False)

    # transmitted wave, traveling +z
    yt = 0.0
    wave(ax, 0.15, 3.7, yt, k2, 0.25, GREEN, alpha=0.6)
    fields(0.75, yt, GREEN, True, "", "")
    ax.texts[-2].set_text("Eₜ"); ax.texts[-1].set_text("Hₜ")
    ax.texts[-2].set_position((0.75 + 0.33, yt + 0.62)); ax.texts[-2].set_ha("left")
    arrow(ax, 2.2, yt + 0.68, 3.3, yt + 0.68, color=GREEN, lw=2.2, head=14)
    lab(ax, 2.05, yt + 0.68, "kₜ", size=S, color=GREEN, ha="right", bold=True, italic=False)

    # axis key, lower right
    ox, oy = 2.6, -2.0
    arrow(ax, ox, oy, ox + 0.75, oy, color=GRAY, lw=1.5, head=11)
    arrow(ax, ox, oy, ox, oy + 0.75, color=GRAY, lw=1.5, head=11)
    lab(ax, ox + 0.98, oy, "z", size=16, color=GRAY)
    lab(ax, ox, oy + 0.98, "x", size=16, color=GRAY)
    dot_out(ax, ox, oy, r=0.11, color=GRAY)
    lab(ax, ox - 0.34, oy - 0.3, "y", size=16, color=GRAY)
    save(fig, "L38-geometry.svg")


def pec():
    """|E| and |H| in front of a perfect conductor at z = 0, in units of E0 and E0/eta1."""
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    u = np.linspace(-1.25, 0, 600)                  # z / lambda1
    e = 2 * np.abs(np.sin(2 * np.pi * u))
    h = 2 * np.abs(np.cos(2 * np.pi * u))
    ax.add_patch(Rectangle((0, -0.2), 0.3, 2.6, fc=PEC, ec="none"))
    ax.axvline(0, color=INK, lw=1.8)
    ax.plot(u, e, color=BLUE, lw=2.6)
    ax.plot(u, h, color=AMBER, lw=2.2, ls="--")
    for z in (0, -0.5, -1.0):
        ax.plot(z, 0, "o", color=BLUE, ms=6, zorder=5)
    ax.text(-0.25, 2.12, "|E|", color=BLUE, fontsize=14, ha="center", fontweight="bold")
    ax.text(-0.5, 2.12, "|H|", color=AMBER, fontsize=14, ha="center", fontweight="bold")
    ax.text(0.15, 1.1, "conductor", rotation=90, ha="center", va="center", fontsize=12,
            color=GRAY)
    ax.set_xlim(-1.25, 0.3); ax.set_ylim(-0.1, 2.45)
    ax.set_xticks([-1.25, -1.0, -0.75, -0.5, -0.25, 0])
    ax.set_xticklabels(["−1.25", "−1", "−0.75", "−0.5", "−0.25", "0"])
    ax.set_yticks([0, 1, 2])
    ax.set_xlabel("z / λ₁", color=GRAY, fontsize=13)
    ax.set_ylabel("|E| / E₀,   |H| η₁ / E₀", color=GRAY, fontsize=13)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=13)
    ax.grid(True, color="#e3edf6", lw=1.0)
    save(fig, "L38-pec.svg")


if __name__ == "__main__":
    geometry()
    pec()
