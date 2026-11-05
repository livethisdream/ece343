#!/usr/bin/env python3
"""L27 figures: current density, conductivity, and resistance.

    L27-charge-tube.svg     charge moving at velocity u, at an angle to the normal
                            of a small area ΔS: in a time Δt it fills a slanted
                            tube of height u·n̂ Δt along the normal
    L27-drift.svg           a free electron accelerating and colliding in a
                            lattice, with a net drift opposite E
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
import matplotlib.path

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
    """Side view of a small area ΔS (edge-on) with normal n̂. Charge moves with
    velocity u at an angle to n̂, so the charges that cross ΔS in Δt fill a
    slanted tube whose height along n̂ is u·n̂ Δt."""
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.2, 7.6); ax.set_ylim(-2.75, 1.85)
    th = np.radians(35)                          # angle of u from the normal
    L = 2.6                                      # slant length u Δt
    dx, dy = L * np.cos(th), L * np.sin(th)
    x1, h = 4.8, 0.75                            # ΔS: the segment x = x1, |y| <= h
    tube = [(x1 - dx, -h - dy), (x1, -h), (x1, h), (x1 - dx, h - dy)]
    ax.add_patch(Polygon(tube, closed=True, fc=FILL, ec=GRAY, lw=1.0, ls="--"))
    ax.plot([x1, x1], [-h, h], color=NAVY, lw=3.2, solid_capstyle="butt")
    lab(ax, x1 + 0.05, h + 0.3, "ΔS", size=14, color=NAVY)
    arrow(ax, x1, 0.0, x1 + 1.0, 0.0, color=NAVY, lw=1.8, head=11)
    lab(ax, x1 + 1.2, 0.0, "n̂", size=15, color=NAVY, bold=True, italic=False)
    rng = np.random.default_rng(4)
    poly = matplotlib.path.Path(tube)
    for _ in range(40):
        x = rng.uniform(0.4, 7.2)
        y = rng.uniform(-2.2, 1.25)
        inside = poly.contains_point((x, y))
        if not inside and (abs(x - x1) < 0.25 or (2.6 < x < 4.6 and 0.5 < y < 1.25)):
            continue
        ax.text(x, y, "+", color=RED if inside else GRAY, fontsize=12,
                ha="center", va="center", alpha=1.0 if inside else 0.5)
    ux, uy = 5.9, 1.05                           # velocity arrow, clear of the tube
    arrow(ax, ux, uy, ux + 0.95 * np.cos(th), uy + 0.95 * np.sin(th), color=AMBER, lw=2.2, head=13)
    lab(ax, ux + 0.25, uy + 0.58, "u", size=15, color=AMBER, bold=True, italic=False)
    ax.annotate("", xy=(x1 - dx, h - dy + 0.12), xytext=(x1, h + 0.12),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.1))
    lab(ax, x1 - dx / 2 - 0.35, h - dy / 2 + 0.45, "u Δt", size=13, color=AMBER)
    yb = -h - dy - 0.3                           # the height measured along n̂
    ax.annotate("", xy=(x1 - dx, yb), xytext=(x1, yb),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    ax.plot([x1, x1], [-h, yb - 0.05], color=GRAY, lw=0.8, ls=":")
    lab(ax, x1 - dx / 2, yb - 0.25, "u·n̂ Δt", size=13, color=GRAY)
    save(fig, "L27-charge-tube.svg")


# ---------------------------------------------------------------------------
def drift():
    """Free electrons in a lattice: each accelerates opposite E, collides with
    an ion, and starts again. The path zigzags, with a net drift u opposite E."""
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.3, 8.3); ax.set_ylim(-2.0, 1.75)
    for xi in np.arange(0.3, 8.0, 0.9):
        for yi in np.arange(-1.2, 1.3, 0.8):
            ax.add_patch(Circle((xi, yi), 0.12, fc="#c7d2e0", ec="none"))
    rng = np.random.default_rng(7)
    p = np.array([7.4, 0.05]); acc = np.array([-1.3, 0.0])
    pts = [p.copy()]; hits = []
    for _ in range(30):
        ang = rng.uniform(0, 2 * np.pi)
        v0 = 0.9 * np.array([np.cos(ang), np.sin(ang)])
        T = rng.uniform(0.55, 0.85)
        for t in np.linspace(0, T, 12)[1:]:
            q = p + v0 * t + 0.5 * acc * t * t
            q[1] = np.clip(q[1], -1.15, 1.15)
            pts.append(q)
        p = pts[-1].copy(); hits.append(p.copy())
        if p[0] < 1.0:
            break
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=RED, lw=1.4)
    for hpt in hits[:-1]:
        ax.plot(*hpt, "o", ms=3.5, color=RED)
    ax.plot(*pts[0], "o", ms=7, color=RED)
    lab(ax, pts[0, 0] + 0.1, pts[0, 1] + 0.32, "e⁻", size=13, color=RED, italic=False)
    arrow(ax, 0.6, 1.5, 2.4, 1.5, color=NAVY, lw=2.0, head=12)
    lab(ax, 2.7, 1.5, "E", size=15, color=NAVY, bold=True, italic=False)
    arrow(ax, 7.4, -1.45, 1.2, -1.45, color=AMBER, lw=2.0, head=12)
    lab(ax, 4.3, -1.75, "net drift u", size=13, color=AMBER, italic=False)
    save(fig, "L27-drift.svg")


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
    ax.axvline(-10, color=GRAY, lw=1.4, ls="--")
    ax.text(-9.85, len(rows) - 0.35, "good insulator",
            color=GRAY, fontsize=11, ha="left", va="center")
    xr = np.log10(2.5e-6)                      # RG-58 dielectric at 100 MHz (L27, L5)
    ax.plot(xr, -0.62, marker="^", ms=9, color=RED, clip_on=False)
    ax.text(xr + 0.25, -0.62, "RG-58 dielectric, 100 MHz", color=RED, fontsize=11,
            ha="left", va="center")
    ax.set_xlim(-12, 11.5)
    ax.set_ylim(-0.95, len(rows) - 0.2)
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
    ax.add_patch(Circle((0, 0), 1.1, fc="none", ec=RED, lw=1.3, ls="--"))
    rt = np.radians(180)
    ax.plot([0, 1.1 * np.cos(rt)], [0, 1.1 * np.sin(rt)], color=RED, lw=1.0)
    lab(ax, -0.85, -0.17, "ρ", size=14, color=RED)
    ax.plot([0, -a * 0.0], [0, a], color=INK, lw=1.0)
    lab(ax, 0.14, a / 2, "a", size=14)
    tb = np.radians(-90)                        # between two J arrows
    ax.plot([0, b * np.cos(tb)], [0, b * np.sin(tb)], color=INK, lw=1.0)
    lab(ax, 0.17, -1.2, "b", size=14)
    lab(ax, 0.0, 1.32, "σ,  ε", size=14)
    ax.text(-0.25, 0.22, "V", fontsize=13, ha="center", va="center", color=INK)
    ax.text(1.55, 1.55, "0", fontsize=13, ha="center", va="center", color=INK)
    save(fig, "L27-coax-leak.svg")


if __name__ == "__main__":
    charge_tube()
    drift()
    conductivity()
    wire()
    coax_leak()
