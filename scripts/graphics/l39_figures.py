#!/usr/bin/env python3
"""L39 figures: a plane wave meeting a boundary at an angle.

    L39-geometry.svg      the incident, reflected, and transmitted rays, their
                          angles from the normal, and the axes (x along the
                          boundary, z into region 2, y out of the page)
    L39-phase-match.svg   wavefronts of the incident and transmitted waves
                          meeting the boundary with the same spacing along it,
                          which is phase matching and Snell's law
    L39-phase-drift.svg   the two sides of the tangential-E condition along the
                          boundary: equal at x = 0 but drifting apart when the
                          rates differ, equal everywhere when they match
    L39-te-tm.svg         the TE wave (E out of the page) beside the TM wave
                          (H out of the page); L39-te-tm-phone.svg stacks them
    L39-te-fields.svg     E and H of the incident, reflected, and transmitted
                          TE waves, the twin of L40-tm-fields.svg
    L39-gamma-te.svg      Gamma_TE and tau_TE against the angle of incidence,
                          air into acrylic (n = 1.49)

Medium 1 is drawn on top and medium 2 below, so z points down the page and y,
by the right-hand rule, points out of it. Figures are sized so their labels
stay at 10.5 px or more on a 390 px phone. Labels are plain Unicode (see
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
    ax.text(xlim[0] + 0.15, ylim[1] - 0.3, "medium 1:  " + top, fontsize=15, ha="left", va="center",
            zorder=9, bbox=dict(fc=FILL1, ec="none", pad=1.5))
    ax.text(xlim[0] + 0.15, ylim[0] + 0.3, "medium 2:  " + bot, fontsize=15, ha="left", va="center",
            zorder=9, bbox=dict(fc=FILL2, ec="none", pad=1.5))


def out_of_page(ax, x, y, r=0.1, color=RED):
    """A field pointing out of the page: a circle with a dot."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.4, zorder=5))
    ax.add_patch(Circle((x, y), r * 0.3, fc=color, ec="none", zorder=6))


def axes_key(ax, ox, oy, s=0.5):
    """x to the right, z down the page, y out of the page."""
    arrow(ax, ox, oy, ox + s, oy, color=GRAY, lw=1.4, head=10)
    arrow(ax, ox, oy, ox, oy - s, color=GRAY, lw=1.4, head=10)
    lab(ax, ox + s + 0.13, oy, "x", size=15, color=GRAY, ha="left")
    lab(ax, ox, oy - s - 0.18, "z", size=15, color=GRAY)
    out_of_page(ax, ox - 0.28, oy + 0.2, r=0.08, color=GRAY)
    lab(ax, ox - 0.44, oy + 0.2, "y", size=15, color=GRAY, ha="right")


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
    fig, ax = plt.subplots(figsize=(6.2, 4.1))
    xlim, ylim = (-3.3, 3.3), (-2.35, 2.35)
    two_regions(ax, xlim, ylim)
    ax.plot([0, 0], [-2.2, 2.2], color=GRAY, lw=1.1, ls="--")
    thi = 50
    tht = np.degrees(np.arcsin(np.sin(np.radians(thi)) / N_ACRYLIC))
    rays(ax, thi, tht)
    ti, tt = np.radians(thi), np.radians(tht)
    lab(ax, -1.45 * np.sin(ti) - 0.5, 1.45 * np.cos(ti) - 0.12, "k̂", "i", size=16,
        color=NAVY, italic=False, bold=True)
    lab(ax, 1.45 * np.sin(ti) + 0.52, 1.45 * np.cos(ti) - 0.12, "k̂", "r", size=16,
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
    fig, ax = plt.subplots(figsize=(6.2, 3.95))
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
    ax.text((x0 + x1) / 2, 0.45, "same spacing along the boundary", fontsize=14, color=RED,
            ha="center", va="center", zorder=8,
            bbox=dict(fc=FILL1, ec="none", pad=2.0))
    save(fig, "L39-phase-match.svg")


def te_tm(phone=False):
    if phone:
        fig, axs = plt.subplots(2, 1, figsize=(4.6, 7.0))
        xlim, ylim = (-2.3, 2.3), (-1.75, 1.95)
    else:
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
        ax.plot([0, 0], [ylim[0] + 0.1, ylim[1] - 0.1], color=GRAY, lw=1.0, ls="--")
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
    save(fig, "L39-te-tm-phone.svg" if phone else "L39-te-tm.svg")


def gamma_te():
    th = np.linspace(0, 89.9, 600)
    t = np.radians(th)
    n1, n2 = 1.0, N_ACRYLIC
    e1, e2 = ETA0 / n1, ETA0 / n2
    ct = np.sqrt(1 - (n1 * np.sin(t) / n2) ** 2)
    G = (e2 * np.cos(t) - e1 * ct) / (e2 * np.cos(t) + e1 * ct)
    tau = 1 + G
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.axhline(0, color="#9fb6cc", lw=1.0)
    ax.plot(th, G, color=RED, lw=2.6)
    ax.plot(th, tau, color=GREEN, lw=2.2, ls="--")
    lab(ax, 68, -0.30, "Γ", "TE", size=17, color=RED)
    lab(ax, 68, 0.62, "τ", "TE", size=17, color=GREEN)
    g45 = np.interp(45, th, G)
    ax.plot([45], [g45], "o", color=RED, ms=7, zorder=5)
    ax.annotate(f"{g45:.3f} at 45°".replace("-", "−"), (45, g45), xytext=(-12, -18), textcoords="offset points",
                ha="right", fontsize=14, color=RED)
    ax.set_xlim(0, 90); ax.set_ylim(-1.05, 1.05)
    ax.set_xticks([0, 30, 60, 90])
    ax.set_xticklabels(["0°", "30°", "60°", "90°"])
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticklabels(["−1", "−0.5", "0", "0.5", "1"])
    ax.set_xlabel("angle of incidence  θᵢ", color=GRAY, fontsize=14)
    ax.grid(True, color="#e3edf6", lw=1.0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=14)
    save(fig, "L39-gamma-te.svg")


def mark_dot(ax, x, y, r=0.13, color=RED):
    """Out of the page."""
    out_of_page(ax, x, y, r=r, color=color)


def te_fields():
    """E (out of the page, +y) and H = k x E / eta for each TE wave, drawn for
    Gamma, tau > 0. On the page +x is right and +z is down, so a vector
    a x + b z is drawn as (a, -b)."""
    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    xlim, ylim = (-3.2, 3.2), (-2.4, 2.4)
    two_regions(ax, xlim, ylim, top="η₁", bot="η₂")
    ax.plot([0, 0], [-2.25, 2.25], color=GRAY, lw=1.1, ls="--")
    thi = 50
    tht = np.degrees(np.arcsin(np.sin(np.radians(thi)) / N_ACRYLIC))
    rays(ax, thi, tht)
    ti, tt = np.radians(thi), np.radians(tht)
    Hi = np.array([-np.cos(ti), -np.sin(ti)])      # -x cos + z sin
    Hr = np.array([np.cos(ti), -np.sin(ti)])       #  x cos + z sin
    Ht = np.array([-np.cos(tt), -np.sin(tt)])      # -x cos_t + z sin_t
    pts = [(np.array([-1.45 * np.sin(ti), 1.45 * np.cos(ti)]), Hi, "i", (0.36, 0.34)),
           (np.array([1.5 * np.sin(ti), 1.5 * np.cos(ti)]), Hr, "r", (0.36, 0.24)),
           (np.array([1.35 * np.sin(tt), -1.35 * np.cos(tt)]), Ht, "t", (0.42, 0.05))]
    for p, h, sub, eoff in pts:
        mark_dot(ax, p[0], p[1])
        arrow(ax, p[0], p[1], p[0] + 0.72 * h[0], p[1] + 0.72 * h[1], color=BLUE, lw=2.4, head=15, z=8)
        lab(ax, p[0] + 0.98 * h[0], p[1] + 0.98 * h[1] - 0.05, "H", sub, size=16, color=BLUE,
            italic=False, bold=True)
        lab(ax, p[0] + eoff[0], p[1] + eoff[1], "E", sub, size=16, color=RED,
            italic=False, bold=True)
    axes_key(ax, 2.35, 1.95)
    save(fig, "L39-te-fields.svg")


def phase_drift():
    """Re of each side of the TE tangential-E condition along z = 0, in units
    of the incident wave's spacing along the boundary, d = lambda_1 / sin(theta_i).
    Top: the transmitted rate is 1.3 times the incident rate. Bottom: matched."""
    x = np.linspace(0, 3.0, 600)
    k1 = 2 * np.pi                      # one cycle per d
    left = np.cos(k1 * x)               # incident + reflected, (1 + Gamma) normalized to 1
    fig, axs = plt.subplots(2, 1, figsize=(5.8, 4.6), sharex=True, gridspec_kw=dict(height_ratios=[1.45, 1]))
    for ax, ratio, title in ((axs[0], 1.3, "rates differ"), (axs[1], 1.0, "rates match")):
        right = np.cos(ratio * k1 * x)
        ax.fill_between(x, left, right, color="#f4d7d8" if ratio != 1 else "none", lw=0)
        ax.plot(x, left, color=NAVY, lw=2.4)
        ax.plot(x, right, color=GREEN, lw=2.2, ls="--")
        ax.axhline(0, color="#9fb6cc", lw=0.9)
        top = 2.75 if ratio != 1 else 1.6
        ax.set_ylim(-1.25, top); ax.set_yticks([])
        ax.text(0.02, top - 0.32, title, fontsize=17, fontweight="bold", color=INK, ha="left", va="center")
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color("#c7d2e0")
        ax.tick_params(colors=GRAY, labelsize=16)
    axs[0].text(2.98, 1.92, "medium 1: incident + reflected", fontsize=15, color=NAVY, ha="right", va="center")
    axs[0].text(2.98, 1.42, "medium 2: transmitted", fontsize=15, color=GREEN, ha="right", va="center")
    axs[1].set_xticks([0, 1, 2, 3])
    axs[1].set_xlabel("distance along the boundary,  x / d", color=GRAY, fontsize=16)
    fig.tight_layout(h_pad=0.6)
    save(fig, "L39-phase-drift.svg")


if __name__ == "__main__":
    geometry()
    phase_match()
    phase_drift()
    te_tm()
    te_tm(phone=True)
    te_fields()
    gamma_te()
