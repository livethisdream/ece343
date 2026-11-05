#!/usr/bin/env python3
"""L39 figures: a plane wave meeting a boundary at an angle.

    L39-geometry.svg      the incident, reflected, and transmitted rays, their
                          angles from the normal, and the axes (x along the
                          boundary, z into region 2, y out of the page)
    L39-phase-match.svg   wavefronts of the incident and transmitted waves
                          meeting the boundary with the same spacing along it,
                          which is phase matching and Snell's law
    L39-te-tm.svg         the TE wave (E out of the page) beside the TM wave
                          (H out of the page)
    L39-gamma-te.svg      Gamma_TE and tau_TE against the angle of incidence,
                          air into acrylic (n = 1.49)

Region 1 is drawn on top and region 2 below, so z points down the page and y,
by the right-hand rule, points out of it. Labels are plain Unicode (see
CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l39_figures.py   ->   book/extras/viz/img/L39-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Arc

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GREEN, GRAY, INK = ("#004a85", "#0067b9", "#8a5a00", "#b01e24",
                                            "#1d7a4d", "#5b6573", "#15202b")
FILL1 = "#f2f7fb"     # region 1
FILL2 = "#d6e5f2"     # region 2
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})

N_ACRYLIC = 1.49
ETA0 = 376.73


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


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=2.0, ls="-", head=12, z=3):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", color=color,
                                 lw=lw, ls=ls, mutation_scale=head, shrinkA=0, shrinkB=0,
                                 zorder=z))


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def two_regions(ax, xlim, ylim, top="ε₁, μ₁", bot="ε₂, μ₂"):
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.add_patch(Rectangle((xlim[0], 0), xlim[1] - xlim[0], ylim[1], fc=FILL1, ec="none"))
    ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], -ylim[0], fc=FILL2, ec="none"))
    ax.plot(xlim, [0, 0], color=INK, lw=1.6)
    ax.text(xlim[0] + 0.15, ylim[1] - 0.28, "region 1:  " + top, fontsize=13, ha="left", va="center")
    ax.text(xlim[0] + 0.15, ylim[0] + 0.28, "region 2:  " + bot, fontsize=13, ha="left", va="center")


def out_of_page(ax, x, y, r=0.1, color=RED):
    """A field pointing out of the page: a circle with a dot."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.4, zorder=5))
    ax.add_patch(Circle((x, y), r * 0.3, fc=color, ec="none", zorder=6))


def axes_key(ax, ox, oy, s=0.5):
    """x to the right, z down the page, y out of the page."""
    arrow(ax, ox, oy, ox + s, oy, color=GRAY, lw=1.4, head=10)
    arrow(ax, ox, oy, ox, oy - s, color=GRAY, lw=1.4, head=10)
    lab(ax, ox + s + 0.13, oy, "x", size=13, color=GRAY, ha="left")
    lab(ax, ox, oy - s - 0.16, "z", size=13, color=GRAY)
    out_of_page(ax, ox - 0.28, oy + 0.2, r=0.08, color=GRAY)
    lab(ax, ox - 0.44, oy + 0.2, "y", size=13, color=GRAY, ha="right")


def angle_arc(ax, center, r, start_deg, end_deg, label, sub, color, lr=None, label_deg=None,
              size=14):
    ax.add_patch(Arc(center, 2 * r, 2 * r, theta1=start_deg, theta2=end_deg, color=color, lw=1.4))
    mid = np.radians(label_deg if label_deg is not None else (start_deg + end_deg) / 2)
    lr = lr or r + 0.28
    lab(ax, center[0] + lr * np.cos(mid), center[1] + lr * np.sin(mid), label, sub,
        size=size, color=color)


# ---------------------------------------------------------------------------
def rays(ax, thi, tht, L=2.3, Lt=2.1):
    """Incident, reflected, and transmitted rays meeting at the origin; angles in degrees."""
    ti, tt = np.radians(thi), np.radians(tht)
    # incident comes from the upper left and travels down and to the right
    p0 = (-L * np.sin(ti), L * np.cos(ti))
    arrow(ax, *p0, -0.42 * np.sin(ti), 0.42 * np.cos(ti), color=NAVY, lw=2.4, head=16)
    ax.plot([p0[0], 0], [p0[1], 0], color=NAVY, lw=2.4)
    # reflected leaves up and to the right
    arrow(ax, 0, 0, 0.75 * L * np.sin(ti), 0.75 * L * np.cos(ti), color=AMBER, lw=2.4, head=16)
    ax.plot([0, L * np.sin(ti)], [0, L * np.cos(ti)], color=AMBER, lw=2.4)
    # transmitted continues down and to the right, bent toward the normal
    arrow(ax, 0, 0, 0.75 * Lt * np.sin(tt), -0.75 * Lt * np.cos(tt), color=GREEN, lw=2.4, head=16)
    ax.plot([0, Lt * np.sin(tt)], [0, -Lt * np.cos(tt)], color=GREEN, lw=2.4)
    return p0


def geometry():
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    xlim, ylim = (-3.3, 3.3), (-2.35, 2.35)
    two_regions(ax, xlim, ylim)
    ax.plot([0, 0], [-2.2, 2.2], color=GRAY, lw=1.1, ls="--")
    thi = 50
    tht = np.degrees(np.arcsin(np.sin(np.radians(thi)) / N_ACRYLIC))
    rays(ax, thi, tht)
    ti, tt = np.radians(thi), np.radians(tht)
    lab(ax, -1.45 * np.sin(ti) - 0.32, 1.45 * np.cos(ti) + 0.12, "k̂", "i", size=16,
        color=NAVY, italic=False, bold=True)
    lab(ax, 1.45 * np.sin(ti) + 0.34, 1.45 * np.cos(ti) + 0.1, "k̂", "r", size=16,
        color=AMBER, italic=False, bold=True)
    lab(ax, 1.25 * np.sin(tt) + 0.34, -1.25 * np.cos(tt) - 0.05, "k̂", "t", size=16,
        color=GREEN, italic=False, bold=True)
    angle_arc(ax, (0, 0), 0.8, 90, 90 + thi, "θ", "i", NAVY, lr=1.08)
    angle_arc(ax, (0, 0), 0.8, 90 - thi, 90, "θ", "r", AMBER, lr=1.08)
    angle_arc(ax, (0, 0), 0.8, 270, 270 + tht, "θ", "t", GREEN, lr=1.1)
    axes_key(ax, 2.35, 1.95)
    save(fig, "L39-geometry.svg")


def phase_match():
    """Wavefronts: lines of constant phase, one wavelength apart along each ray,
    meet the boundary at the same points from both sides."""
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    xlim, ylim = (-3.3, 3.3), (-2.2, 2.2)
    two_regions(ax, xlim, ylim, top="n₁ = 1", bot="n₂ = 1.49")
    thi = 50
    tht = np.degrees(np.arcsin(np.sin(np.radians(thi)) / N_ACRYLIC))
    ti, tt = np.radians(thi), np.radians(tht)
    lam1 = 0.62
    lam2 = lam1 / N_ACRYLIC
    d = lam1 / np.sin(ti)                     # spacing of the crossings along x
    xs = np.arange(-2.6, 2.7, d)
    half = 2.4
    # incident wavefronts: perpendicular to k_i, ending on the boundary at xs
    # A front is perpendicular to its ray. The incident ray runs down and to the
    # right, so its fronts run up and to the right from the boundary; the
    # transmitted fronts run down and to the left from the same points.
    ui = np.array([np.cos(ti), np.sin(ti)])
    ut = np.array([np.cos(tt), np.sin(tt)])
    for x0 in xs:
        p = np.array([x0, 0.0])
        a = p + ui * half
        ax.plot([a[0], p[0]], [a[1], p[1]], color=NAVY, lw=1.3)
        b = p - ut * half
        ax.plot([p[0], b[0]], [p[1], b[1]], color=GREEN, lw=1.3)
        ax.plot([x0], [0], "o", ms=5, color=RED, zorder=6)
    # clip by redrawing the region fills outside the picture area is not needed:
    # the axes limits clip the lines.
    # ray arrows
    arrow(ax, -2.75, 1.45, -2.75 + 0.9 * np.sin(ti), 1.45 - 0.9 * np.cos(ti), color=NAVY, lw=2.2, head=15, z=7)
    lab(ax, -2.95, 1.15, "k̂", "i", size=15, color=NAVY, italic=False, bold=True)
    arrow(ax, 2.55, -0.75, 2.55 + 0.8 * np.sin(tt), -0.75 - 0.8 * np.cos(tt), color=GREEN, lw=2.2, head=15, z=7)
    lab(ax, 2.6, -1.75, "k̂", "t", size=15, color=GREEN, italic=False, bold=True)
    # spacing along the boundary
    x0, x1 = xs[3], xs[4]
    ax.annotate("", (x0, 0.2), (x1, 0.2),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.3, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, 0.45, "λ₁ / sin θᵢ  =  λ₂ / sin θₜ", fontsize=13, color=RED,
            ha="center", va="center", zorder=8,
            bbox=dict(fc=FILL1, ec="none", pad=2.0))
    save(fig, "L39-phase-match.svg")


def te_tm():
    fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.3))
    xlim, ylim = (-2.6, 2.6), (-2.0, 2.0)
    thi = 50
    tht = np.degrees(np.arcsin(np.sin(np.radians(thi)) / N_ACRYLIC))
    ti, tt = np.radians(thi), np.radians(tht)
    for ax, mode in zip(axs, ("TE", "TM")):
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(*xlim); ax.set_ylim(*ylim)
        ax.add_patch(Rectangle((xlim[0], 0), xlim[1] - xlim[0], ylim[1], fc=FILL1, ec="none"))
        ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], -ylim[0], fc=FILL2, ec="none"))
        ax.plot(xlim, [0, 0], color=INK, lw=1.6)
        ax.plot([0, 0], [-1.9, 1.9], color=GRAY, lw=1.0, ls="--")
        L = 1.9
        p0 = (-L * np.sin(ti), L * np.cos(ti))
        ax.plot([p0[0], 0], [p0[1], 0], color=NAVY, lw=2.0)
        arrow(ax, *p0, -0.5 * np.sin(ti), 0.5 * np.cos(ti), color=NAVY, lw=2.0, head=14)
        ax.plot([0, L * np.sin(ti)], [0, L * np.cos(ti)], color=AMBER, lw=2.0)
        arrow(ax, 0, 0, 0.8 * L * np.sin(ti), 0.8 * L * np.cos(ti), color=AMBER, lw=2.0, head=14)
        ax.plot([0, L * np.sin(tt)], [0, -L * np.cos(tt)], color=GREEN, lw=2.0)
        arrow(ax, 0, 0, 0.8 * L * np.sin(tt), -0.8 * L * np.cos(tt), color=GREEN, lw=2.0, head=14)
        # The incident ray's fields. TE: E along +y (out of the page) and
        # H = k x E / eta, down and to the left. TM: H along +y and
        # E = x cos(theta) - z sin(theta), up and to the right (z points down).
        m = np.array([-1.1 * np.sin(ti), 1.1 * np.cos(ti)])
        perp = np.array([-np.cos(ti), -np.sin(ti)])      # in the plane, perpendicular to k_i
        if mode == "TE":
            dot_name, arr_name, dot_col, arr_col, d = "E", "H", RED, BLUE, perp
        else:
            dot_name, arr_name, dot_col, arr_col, d = "H", "E", BLUE, RED, -perp
        out_of_page(ax, m[0], m[1], r=0.13, color=dot_col)
        arrow(ax, m[0], m[1], m[0] + 0.75 * d[0], m[1] + 0.75 * d[1],
              color=arr_col, lw=2.4, head=15, z=6)
        lab(ax, m[0] + (0.3 if mode == "TE" else -0.34), m[1] + (0.3 if mode == "TE" else -0.08), dot_name, size=17, color=dot_col, italic=False, bold=True)
        lab(ax, m[0] + 0.95 * d[0], m[1] + 0.95 * d[1] + (0.12 if mode == "TE" else 0.05),
            arr_name, size=17, color=arr_col, italic=False, bold=True)
        ax.text(0, ylim[1] + 0.18, mode + (": E out of the page" if mode == "TE"
                                           else ": H out of the page"),
                fontsize=15, ha="center", va="bottom", fontweight="bold", color=INK)
    save(fig, "L39-te-tm.svg")


def gamma_te():
    th = np.linspace(0, 89.9, 600)
    t = np.radians(th)
    n1, n2 = 1.0, N_ACRYLIC
    e1, e2 = ETA0 / n1, ETA0 / n2
    ct = np.sqrt(1 - (n1 * np.sin(t) / n2) ** 2)
    G = (e2 * np.cos(t) - e1 * ct) / (e2 * np.cos(t) + e1 * ct)
    tau = 1 + G
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.axhline(0, color="#9fb6cc", lw=1.0)
    ax.plot(th, G, color=RED, lw=2.6)
    ax.plot(th, tau, color=GREEN, lw=2.2, ls="--")
    lab(ax, 70, -0.33, "Γ", "TE", size=15, color=RED)
    lab(ax, 70, 0.66, "τ", "TE", size=15, color=GREEN)
    g45 = np.interp(45, th, G)
    ax.plot([45], [g45], "o", color=RED, ms=7, zorder=5)
    ax.annotate(f"{g45:.3f} at 45°".replace("-", "−"), (45, g45), xytext=(-12, -18), textcoords="offset points",
                ha="right", fontsize=12, color=RED)
    ax.set_xlim(0, 90); ax.set_ylim(-1.05, 1.05)
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_xticklabels(["0°", "15°", "30°", "45°", "60°", "75°", "90°"])
    ax.set_xlabel("angle of incidence  θᵢ", color=GRAY, fontsize=12)
    ax.grid(True, color="#e3edf6", lw=1.0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=11)
    save(fig, "L39-gamma-te.svg")


if __name__ == "__main__":
    geometry()
    phase_match()
    te_tm()
    gamma_te()
