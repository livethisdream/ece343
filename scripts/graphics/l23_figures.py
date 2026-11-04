#!/usr/bin/env python3
"""L23 figures: Laplace's equation solved between conductors.

    L23-parallel-plate.svg  two plates at z = 0 and z = d, with the linear
                            potential V(z) beside them
    L23-coax.svg            coax cross section with equipotential circles and
                            radial field, beside V(rho) and |E(rho)|
    L23-relaxation.svg      a grounded square trough with a lid at V0, solved
                            by averaging neighbors; equipotential contours

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l23_figures.py   ->   book/extras/viz/img/L23-*.svg
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
FILL = "#e3edf6"
METAL = "#9aa8b6"
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


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=11)


# ---------------------------------------------------------------------------
def parallel_plate():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.8, 3.6), gridspec_kw={"width_ratios": [1.15, 1]})
    a1.set_aspect("equal"); a1.axis("off")
    a1.set_xlim(-0.3, 4.4); a1.set_ylim(-0.6, 2.7)
    a1.add_patch(Rectangle((0, 2.0), 3.4, 0.16, fc=METAL, ec=INK, lw=1.0))
    a1.add_patch(Rectangle((0, -0.16), 3.4, 0.16, fc=METAL, ec=INK, lw=1.0))
    a1.add_patch(Rectangle((0, 0), 3.4, 2.0, fc=FILL, ec="none"))
    for x in np.linspace(0.4, 3.0, 5):
        a1.annotate("", xy=(x, 0.15), xytext=(x, 1.85),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4))
    for z in (0.5, 1.0, 1.5):
        a1.plot([0.05, 3.35], [z, z], color=AMBER, lw=1.0, ls=(0, (3, 3)))
    lab(a1, 3.55, 2.08, "V = V", "0", size=13, ha="left", italic=False)
    lab(a1, 3.55, -0.08, "V = 0", size=13, ha="left", italic=False)
    lab(a1, -0.12, 2.08, "z = d", size=12, ha="right", italic=False, color=GRAY)
    lab(a1, -0.12, -0.08, "z = 0", size=12, ha="right", italic=False, color=GRAY)
    lab(a1, 1.7, 2.45, "E", size=15, color=NAVY)

    z = np.linspace(0, 1, 50)
    a2.plot(z, z, color=NAVY, lw=2.6)
    a2.set_xlim(0, 1.05); a2.set_ylim(0, 1.1)
    a2.set_xticks([0, 1]); a2.set_xticklabels(["0", "d"])
    a2.set_yticks([0, 1]); a2.set_yticklabels(["0", ""])
    a2.text(-0.07, 1.0, "V", fontsize=12, color=GRAY, ha="right", va="center", clip_on=False)
    a2.text(-0.07, 0.975, "0", fontsize=8.4, color=GRAY, ha="left", va="center", clip_on=False)
    a2.set_xlabel("z", color=GRAY, fontstyle="italic")
    a2.set_ylabel("V(z)", color=GRAY, fontstyle="italic")
    style(a2)
    save(fig, "L23-parallel-plate.svg")


def coax():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.8, 3.9), gridspec_kw={"width_ratios": [1, 1.15]})
    a1.set_aspect("equal"); a1.axis("off")
    a, b = 0.405, 1.475
    s = 1.0 / b
    A, B = a * s * 1.6, 1.0   # the inner radius drawn larger, for legibility
    a1.set_xlim(-1.25, 1.25); a1.set_ylim(-1.25, 1.25)
    a1.add_patch(Circle((0, 0), 1.12, fc=METAL, ec=INK, lw=1.0))
    a1.add_patch(Circle((0, 0), B, fc=FILL, ec=INK, lw=1.0))
    for frac in (0.25, 0.5, 0.75):
        r = A * (B / A) ** frac
        a1.add_patch(Circle((0, 0), r, fc="none", ec=AMBER, lw=1.0, ls=(0, (3, 3))))
    for th in np.linspace(0, 2 * np.pi, 9)[:-1] + np.pi / 8:
        a1.annotate("", xy=(0.93 * np.cos(th), 0.93 * np.sin(th)),
                    xytext=((A + 0.04) * np.cos(th), (A + 0.04) * np.sin(th)),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.3))
    a1.add_patch(Circle((0, 0), A, fc=METAL, ec=INK, lw=1.0))
    lab(a1, -0.04, 0, "V", "0", size=12, italic=False)
    lab(a1, 0, -1.2, "V = 0", size=12, italic=False, color=GRAY, va="top")

    rho = np.linspace(a, b, 200)
    V = np.log(b / rho) / np.log(b / a)
    E = 1 / (rho * np.log(b / a))
    E = E / E[0]
    a2.plot(rho * 1e3 / 1e3, V, color=AMBER, lw=2.4, label="potential V(ρ)")
    a2.plot(rho, E, color=NAVY, lw=2.4, label="field |E(ρ)|")
    a2.set_xlim(0, b * 1.05); a2.set_ylim(0, 1.1)
    a2.set_xticks([0, a, b]); a2.set_xticklabels(["0", "a", "b"])
    a2.set_yticks([0, 1]); a2.set_yticklabels(["0", "max"])
    a2.set_xlabel("ρ", color=GRAY, fontstyle="italic")
    a2.axvline(a, color="#c7d2e0", lw=1.0, ls=(0, (3, 3)))
    a2.legend(frameon=False, fontsize=12, loc="upper right")
    style(a2)
    save(fig, "L23-coax.svg")


def relaxation():
    n = 41
    V = np.zeros((n, n))
    V[-1, 1:-1] = 1.0             # the lid, at V0; the other three walls at 0
    for _ in range(6000):
        V[1:-1, 1:-1] = 0.25 * (V[2:, 1:-1] + V[:-2, 1:-1] + V[1:-1, 2:] + V[1:-1, :-2])
    x = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, x)

    fig, ax = plt.subplots(figsize=(4.8, 4.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.12, 1.3); ax.set_ylim(-0.12, 1.14)
    cs = ax.contour(X, Y, V, levels=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    colors=AMBER, linewidths=1.2)
    ax.clabel(cs, fmt=lambda v: f"{v:.2g}", fontsize=10, inline=True)
    ax.plot([0, 0, 1, 1], [1, 0, 0, 1], color=INK, lw=2.4)
    ax.plot([0.02, 0.98], [1.02, 1.02], color=RED, lw=3.0)
    lab(ax, 0.46, 1.09, "V = V", "0", size=12, italic=False, color=RED)
    lab(ax, 1.04, 0.5, "V = 0", size=12, italic=False, color=GRAY, ha="left")
    save(fig, "L23-relaxation.svg")


if __name__ == "__main__":
    parallel_plate()
    coax()
    relaxation()
