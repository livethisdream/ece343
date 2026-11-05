#!/usr/bin/env python3
"""L27 figures: current density, conductivity, and resistance.

    L27-charge-tube.svg     charge moving at velocity u through a small area
                            ΔS: in a time Δt it sweeps out a tube of length uΔt
    L27-conductivity.svg    the conductivity of common materials on a log axis,
                            from free space to copper
    L27-wire.svg            a straight wire of length ℓ and radius a, with the
                            uniform field and current density along its axis
    L27-coax-leak.svg       coaxial cross section with a slightly conducting
                            dielectric: the leakage current flows radially

Labels are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l27_figures.py   ->   book/extras/viz/img/L27-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402
from l24_figures import lab, arrow  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL = "#e3edf6"      # dielectric or the swept tube
METAL = "#9aa8b6"     # conductor
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


# ---------------------------------------------------------------------------
def charge_tube():
    """A tube of length uΔt behind a small area ΔS: every charge inside it
    crosses ΔS in the time Δt."""
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.6, 7.4); ax.set_ylim(-1.3, 1.6)
    x0, x1, h, w = 1.2, 4.6, 0.75, 0.32          # tube from x0 to the area at x1
    ax.add_patch(Polygon([(x0, -h), (x1, -h), (x1, h), (x0, h)], closed=True,
                         fc=FILL, ec="none"))
    ax.plot([x0, x1], [h, h], color=GRAY, lw=1.0, ls="--")
    ax.plot([x0, x1], [-h, -h], color=GRAY, lw=1.0, ls="--")
    ax.add_patch(Ellipse((x0, 0), 2 * w, 2 * h, fc=FILL, ec=GRAY, lw=1.0, ls="--"))
    ax.add_patch(Ellipse((x1, 0), 2 * w, 2 * h, fc="#c9dcee", ec=NAVY, lw=1.8))
    lab(ax, x1 + 0.05, h + 0.32, "ΔS", size=14, color=NAVY)
    rng = np.random.default_rng(4)
    for _ in range(26):                          # charges spread through and beyond the tube
        x = rng.uniform(0.0, 6.4)
        y = rng.uniform(-h + 0.12, h - 0.12)
        inside = x0 < x < x1
        ax.text(x, y, "+", color=RED if inside else GRAY, fontsize=12,
                ha="center", va="center", alpha=1.0 if inside else 0.55)
    arrow(ax, 5.3, 0.0, 6.6, 0.0, color=AMBER, lw=2.2, head=13)
    lab(ax, 6.0, 0.32, "u", size=15, color=AMBER, bold=True, italic=False)
    ax.annotate("", xy=(x0, -h - 0.3), xytext=(x1, -h - 0.3),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, (x0 + x1) / 2, -h - 0.55, "u Δt", size=14, color=GRAY)
    save(fig, "L27-charge-tube.svg")


# ---------------------------------------------------------------------------
MATERIALS = [            # S/m, the Spring 2025 table
    ("copper", 5.8e7),
    ("gold", 4.4e7),
    ("aluminum", 3.7e7),
    ("iron", 1.0e7),
    ("carbon", 1.3e5),
    ("seawater", 5.0),
    ("tap water", 1.0e-2),
    ("distilled water", 6.0e-6),
    ("dry soil", 1.0e-4),
    ("silicon", 4.4e-4),
]


SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def sci(v):
    """5.8e7 as '5.8 × 10⁷', in plain Unicode."""
    m, e = f"{v:.1e}".split("e")
    e = int(e)
    return m if e == 0 else f"{m} × 10{str(e).translate(SUP)}"


def conductivity():
    rows = sorted(MATERIALS, key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    y = np.arange(len(rows))
    vals = np.array([r[1] for r in rows])
    good = vals > 1e5
    ax.barh(y, np.log10(vals) + 12, left=-12, height=0.6,
            color=[NAVY if g else "#8fb0cf" for g in good])
    for yi, (name, v) in zip(y, rows):
        ax.text(-12.3, yi, name, ha="right", va="center", fontsize=12)
        ax.text(np.log10(v) + 0.3, yi, sci(v), ha="left", va="center", fontsize=11, color=GRAY)
    ax.axvline(5, color=AMBER, lw=1.4, ls="--")
    ax.text(5.15, len(rows) - 0.35, "good conductor", color=AMBER, fontsize=12,
            ha="left", va="center")
    ax.set_xlim(-12, 11.5)
    ax.set_ylim(-0.7, len(rows) - 0.2)
    ax.set_xticks(range(-12, 9, 2))
    ax.set_xticklabels([f"10{s}" for s in ("⁻¹²", "⁻¹⁰", "⁻⁸", "⁻⁶", "⁻⁴", "⁻²", "⁰",
                                          "²", "⁴", "⁶", "⁸")])
    ax.set_xlabel("conductivity σ (S/m)", color=GRAY, fontsize=12)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=11)
    save(fig, "L27-conductivity.svg")


# ---------------------------------------------------------------------------
def wire():
    fig, ax = plt.subplots(figsize=(7.4, 2.8))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.1, 7.6); ax.set_ylim(-1.35, 1.35)
    x0, x1, r, w = 0.6, 5.8, 0.6, 0.22
    ax.add_patch(Rectangle((x0, -r), x1 - x0, 2 * r, fc=METAL, ec="none"))
    ax.plot([x0, x1], [r, r], color=INK, lw=1.2)
    ax.plot([x0, x1], [-r, -r], color=INK, lw=1.2)
    ax.add_patch(Ellipse((x1, 0), 2 * w, 2 * r, fc="#b8c4d0", ec=INK, lw=1.2))
    ax.add_patch(Ellipse((x0, 0), 2 * w, 2 * r, fc="#b8c4d0", ec=INK, lw=1.2))
    for yy in (-0.3, 0.0, 0.3):
        arrow(ax, 1.3, yy, 4.9, yy, color=NAVY, lw=1.8, head=12)
    lab(ax, 3.1, 0.82, "E,  J = σE", size=14, color=NAVY, italic=False, bold=True)
    ax.plot([x1, x1 + 0.9], [0, 0], color=INK, lw=1.0)
    ax.plot([x0 - 0.9, x0], [0, 0], color=INK, lw=1.0)
    ax.text(x0 - 1.0, 0, "+V", fontsize=14, ha="right", va="center")
    ax.text(x1 + 1.0, 0, "0", fontsize=14, ha="left", va="center")
    ax.annotate("", xy=(x0, -r - 0.38), xytext=(x1, -r - 0.38),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, (x0 + x1) / 2, -r - 0.62, "ℓ", size=15, color=GRAY)
    ax.plot([x1, x1], [0, r], color=AMBER, lw=1.3)
    lab(ax, x1 + 0.38, 0.32, "a", size=14, color=AMBER)
    arrow(ax, 6.6, -0.85, 7.4, -0.85, color=GRAY, lw=1.1, head=9)
    lab(ax, 7.0, -0.6, "z", size=13, color=GRAY)
    save(fig, "L27-wire.svg")


# ---------------------------------------------------------------------------
def coax_leak():
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    ax.set_aspect("equal"); ax.axis("off")
    a, b, t = 0.55, 1.7, 0.18
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.1, 2.1)
    ax.add_patch(Circle((0, 0), b + t, fc=METAL, ec=INK, lw=1.2))
    ax.add_patch(Circle((0, 0), b, fc=FILL, ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), a, fc=METAL, ec=INK, lw=1.2))
    for th in np.linspace(0, 2 * np.pi, 8, endpoint=False) + np.pi / 8:
        arrow(ax, (a + 0.15) * np.cos(th), (a + 0.15) * np.sin(th),
              (b - 0.15) * np.cos(th), (b - 0.15) * np.sin(th), color=NAVY, lw=1.8, head=11)
    lab(ax, 0.95, 0.12, "J", size=15, color=NAVY, italic=False, bold=True)
    ax.plot([0, -a], [0, 0], color=INK, lw=1.0)
    lab(ax, -a / 2, 0.14, "a", size=14)
    ax.plot([0, b * np.cos(-np.pi / 2.6)], [0, b * np.sin(-np.pi / 2.6)], color=INK, lw=1.0)
    lab(ax, 0.82, -1.15, "b", size=14)
    lab(ax, 0.0, 1.32, "σ,  ε", size=14)
    save(fig, "L27-coax-leak.svg")


if __name__ == "__main__":
    charge_tube()
    conductivity()
    wire()
    coax_leak()
