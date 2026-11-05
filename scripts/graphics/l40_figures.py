#!/usr/bin/env python3
"""L40 figures: TM incidence, the Brewster angle, and total internal reflection.

    L40-tm-fields.svg   the TM sign convention: H of each wave along +y or -y
                        and E in the plane of incidence, drawn for positive
                        Gamma_TM and tau_TM
    L40-brewster.svg    a wave at the Brewster angle on acrylic: the reflected
                        and transmitted rays are perpendicular, and only the TE
                        part reflects
    L40-tir.svg         the instantaneous TE field when acrylic meets air at
                        50 degrees, past the critical angle: a standing pattern
                        in the acrylic and an evanescent field that decays in
                        the air within a fraction of a wavelength
    L40-water.svg       the reflected power fraction of each polarization for
                        light in air striking water (n = 1.33), with the
                        Brewster angle marked

Region 1 is on top, z points down the page, and y points out of it, as in
L39's figures. Labels are plain Unicode (see CLAUDE.md).

    python3 scripts/graphics/l40_figures.py   ->   book/extras/viz/img/L40-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Arc

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GREEN, GRAY, INK = ("#004a85", "#0067b9", "#8a5a00", "#b01e24",
                                            "#1d7a4d", "#5b6573", "#15202b")
FILL1 = "#f2f7fb"
FILL2 = "#d6e5f2"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})

N_ACRYLIC = 1.49
N_WATER = 1.33
ETA0 = 376.73


def lab(ax, x, y, base, sub="", size=15, color=INK, ha="center", va="center",
        italic=True, bold=False):
    """A symbol with an optional subscript, in plain text (see CLAUDE.md)."""
    t = ax.text(x, y, base, fontsize=size, color=color, ha=ha, va=va,
                fontstyle="italic" if italic else "normal",
                fontweight="bold" if bold else "normal", zorder=9)
    if not sub:
        return t
    fig = ax.figure
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    w = bb.width / fig.dpi * 72
    shift = {"center": w / 2, "left": w, "right": 0}[ha]
    ax.annotate(sub, (x, y), xytext=(shift + 0.5, -size * 0.32), textcoords="offset points",
                fontsize=size * 0.7, color=color, ha="left", va=va, zorder=9)
    return t


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=2.0, ls="-", head=12, z=4):
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


def regions(ax, xlim, ylim, top, bot):
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.add_patch(Rectangle((xlim[0], 0), xlim[1] - xlim[0], ylim[1], fc=FILL1, ec="none"))
    ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], -ylim[0], fc=FILL2, ec="none"))
    ax.plot(xlim, [0, 0], color=INK, lw=1.6)
    ax.plot([0, 0], [ylim[0] + 0.1, ylim[1] - 0.1], color=GRAY, lw=1.0, ls="--")
    ax.text(xlim[0] + 0.15, ylim[1] - 0.25, top, fontsize=13, ha="left", va="center")
    ax.text(xlim[0] + 0.15, ylim[0] + 0.25, bot, fontsize=13, ha="left", va="center")


def dot(ax, x, y, r=0.12, color=BLUE):
    """Out of the page."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.5, zorder=6))
    ax.add_patch(Circle((x, y), r * 0.3, fc=color, ec="none", zorder=7))


def cross(ax, x, y, r=0.12, color=BLUE):
    """Into the page."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.5, zorder=6))
    d = r * 0.62
    ax.plot([x - d, x + d], [y - d, y + d], color=color, lw=1.3, zorder=7)
    ax.plot([x - d, x + d], [y + d, y - d], color=color, lw=1.3, zorder=7)


def ray(ax, ang_from_down, sign_up, L, color, inward):
    """A ray through the origin. Direction (sin a, -cos a) points down-right;
    sign_up=+1 flips it to up-right. inward=True draws it arriving at the origin."""
    a = np.radians(ang_from_down)
    d = np.array([np.sin(a), -np.cos(a) * sign_up])   # travel direction (page coords)
    if inward:
        start = -d * L
        ax.plot([start[0], 0], [start[1], 0], color=color, lw=2.2)
        arrow(ax, *start, *(-d * 0.45 * L), color=color, lw=2.2, head=15)
    else:
        end = d * L
        ax.plot([0, end[0]], [0, end[1]], color=color, lw=2.2)
        arrow(ax, 0, 0, *(d * 0.7 * L), color=color, lw=2.2, head=15)
    return d


# ---------------------------------------------------------------------------
def tm_fields():
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    xlim, ylim = (-3.2, 3.2), (-2.4, 2.4)
    regions(ax, xlim, ylim, "region 1:  η₁", "region 2:  η₂")
    thi = 50
    tht = np.degrees(np.arcsin(np.sin(np.radians(thi)) / N_ACRYLIC))
    L = 2.3
    # incident arrives traveling down-right; its direction is (sin, -cos) on the page
    di = ray(ax, thi, +1, L, NAVY, inward=True)
    dr = ray(ax, thi, -1, L, AMBER, inward=False)
    dt = ray(ax, tht, +1, L, GREEN, inward=False)
    # Field reference directions (Gamma, tau > 0). On the page, +x is right and
    # +z is down, so a vector a x + b z is drawn as (a, -b).
    ti, tt = np.radians(thi), np.radians(tht)
    Ei = np.array([np.cos(ti), np.sin(ti)])        # x cos - z sin  -> (cos, +sin)
    Er = np.array([np.cos(ti), -np.sin(ti)])       # x cos + z sin  -> (cos, -sin)
    Et = np.array([np.cos(tt), np.sin(tt)])
    pts = [(-di * 1.35, Ei, dot, "E", "i", "H", "i", (-0.36, 0.05)),
           (dr * 1.4, Er, cross, "E", "r", "H", "r", (0.36, 0.06)),
           (dt * 1.3, Et, dot, "E", "t", "H", "t", (0.36, 0.0))]
    for p, e, mark, en, es, hn, hs, hoff in pts:
        mark(ax, p[0], p[1])
        arrow(ax, p[0], p[1], p[0] + 0.75 * e[0], p[1] + 0.75 * e[1], color=RED, lw=2.4, head=15, z=8)
        lab(ax, p[0] + 0.95 * e[0] + 0.05, p[1] + 0.95 * e[1] + 0.12, en, es, size=15, color=RED,
            italic=False, bold=True)
        lab(ax, p[0] + hoff[0], p[1] + hoff[1] - 0.28, hn, hs, size=15, color=BLUE,
            italic=False, bold=True)
    # axes key
    ox, oy = 2.4, 1.9
    arrow(ax, ox, oy, ox + 0.5, oy, color=GRAY, lw=1.4, head=10)
    arrow(ax, ox, oy, ox, oy - 0.5, color=GRAY, lw=1.4, head=10)
    lab(ax, ox + 0.63, oy, "x", size=13, color=GRAY, ha="left")
    lab(ax, ox, oy - 0.66, "z", size=13, color=GRAY)
    dot(ax, ox - 0.28, oy + 0.2, r=0.08, color=GRAY)
    lab(ax, ox - 0.44, oy + 0.2, "y", size=13, color=GRAY, ha="right")
    save(fig, "L40-tm-fields.svg")


def brewster():
    fig, ax = plt.subplots(figsize=(7.6, 4.9))
    xlim, ylim = (-3.2, 3.2), (-2.35, 2.35)
    regions(ax, xlim, ylim, "air,  n₁ = 1", "acrylic,  n₂ = 1.49")
    thB = np.degrees(np.arctan(N_ACRYLIC))
    tht = 90 - thB
    L = 2.3
    ray(ax, thB, +1, L, NAVY, inward=True)
    dr = ray(ax, thB, -1, L, AMBER, inward=False)
    dt = ray(ax, tht, +1, L, GREEN, inward=False)
    # angles
    ax.add_patch(Arc((0, 0), 1.5, 1.5, theta1=90, theta2=90 + thB, color=NAVY, lw=1.4))
    lab(ax, -1.75, 0.3, "θ", "B", size=14, color=NAVY)
    ax.text(-1.55, 0.3, f"= {thB:.1f}°", fontsize=13, color=NAVY, ha="left", va="center")
    ax.add_patch(Arc((0, 0), 1.5, 1.5, theta1=270, theta2=270 + tht, color=GREEN, lw=1.4))
    ax.text(0.95, -1.05, f"θₜ = {tht:.1f}°", fontsize=12, color=GREEN, ha="left")
    # right angle between reflected and transmitted rays, at the origin
    a = np.arctan2(dr[1], dr[0]); b = np.arctan2(dt[1], dt[0])
    ax.add_patch(Arc((0, 0), 1.0, 1.0, theta1=np.degrees(b), theta2=np.degrees(a),
                     color=RED, lw=1.4, ls="--"))
    m = (a + b) / 2
    ax.text(0.78 * np.cos(m) + 0.22, 0.78 * np.sin(m), "90°", fontsize=13, color=RED,
            ha="left", va="center", fontweight="bold",
            bbox=dict(fc="white", ec="none", pad=1.0, alpha=0.8))
    ax.text(dr[0] * 2.25 + 0.05, dr[1] * 2.25 + 0.05, "TE only", fontsize=13, color=AMBER,
            ha="left", va="bottom", fontweight="bold")
    ax.text(-dr[0] * 2.25 + 0.1, dr[1] * 2.25 + 0.05, "TE + TM", fontsize=13, color=NAVY,
            ha="right", va="bottom", fontweight="bold")
    save(fig, "L40-brewster.svg")


def tir():
    """Re{E_y} at one instant, in units of the free-space wavelength."""
    n1, n2 = N_ACRYLIC, 1.0
    th = np.radians(50.0)
    k0 = 2 * np.pi
    k1 = n1 * k0
    kx = k1 * np.sin(th)
    q = np.sqrt((n1 * np.sin(th) / n2) ** 2 - 1)
    alpha = k0 * n2 * q
    eta1, eta2 = ETA0 / n1, ETA0 / n2
    ct = -1j * q
    G = (eta2 * np.cos(th) - eta1 * ct) / (eta2 * np.cos(th) + eta1 * ct)
    tau = 1 + G
    x = np.linspace(-1.6, 1.6, 520)
    zz = np.linspace(-1.1, 0.9, 340)        # page-down coordinate z (into region 2 for z > 0)
    X, Z = np.meshgrid(x, zz)
    E = np.where(Z < 0,
                 np.exp(-1j * k1 * (X * np.sin(th) + Z * np.cos(th)))
                 + G * np.exp(-1j * k1 * (X * np.sin(th) - Z * np.cos(th))),
                 tau * np.exp(-1j * kx * X) * np.exp(-alpha * np.clip(Z, 0, None)))
    cmap = LinearSegmentedColormap.from_list("rb", [BLUE, "#ffffff", RED])
    fig, ax = plt.subplots(figsize=(7.8, 4.9))
    ax.imshow(E.real, extent=(x[0], x[-1], -zz[-1], -zz[0]), origin="upper", cmap=cmap,
              vmin=-2, vmax=2, aspect="equal", interpolation="bilinear")
    # The image's vertical axis is -z, so region 1 (z < 0) is on top.
    ax.plot([x[0], x[-1]], [0, 0], color=INK, lw=1.6)
    d = 1 / alpha
    ax.annotate("", (1.42, 0), (1.42, -d),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3, shrinkA=0, shrinkB=0))
    ax.text(1.36, -d / 2 - 0.02, "1/α", fontsize=13, ha="right", va="center", color=INK,
            bbox=dict(fc="white", ec="none", pad=1.0, alpha=0.85))
    ax.text(x[0] + 0.05, 1.0, "acrylic,  n₁ = 1.49,  θᵢ = 50°", fontsize=13, ha="left", va="center",
            bbox=dict(fc="white", ec="none", pad=1.5, alpha=0.85))
    ax.text(x[0] + 0.05, -0.75, "air,  n₂ = 1", fontsize=13, ha="left", va="center",
            bbox=dict(fc="white", ec="none", pad=1.5, alpha=0.85))
    ax.set_xticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5])
    ax.set_yticks([-0.5, 0, 0.5, 1])
    ax.set_yticklabels(["0.5", "0", "−0.5", "−1"])
    ax.set_xticklabels(["−1.5", "−1", "−0.5", "0", "0.5", "1", "1.5"])
    ax.set_xlabel("x / λ₀", color=GRAY, fontsize=12)
    ax.set_ylabel("z / λ₀", color=GRAY, fontsize=12)
    ax.tick_params(colors=GRAY, labelsize=11)
    for s in ax.spines.values():
        s.set_color("#c7d2e0")
    save(fig, "L40-tir.svg")


def water():
    th = np.linspace(0, 89.9, 700)
    t = np.radians(th)
    n1, n2 = 1.0, N_WATER
    e1, e2 = ETA0 / n1, ETA0 / n2
    ct = np.sqrt(1 - (n1 * np.sin(t) / n2) ** 2)
    Gte = (e2 * np.cos(t) - e1 * ct) / (e2 * np.cos(t) + e1 * ct)
    Gtm = (e2 * ct - e1 * np.cos(t)) / (e2 * ct + e1 * np.cos(t))
    thB = np.degrees(np.arctan(n2 / n1))
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.plot(th, 100 * Gte ** 2, color=RED, lw=2.6)
    ax.plot(th, 100 * Gtm ** 2, color=BLUE, lw=2.6, ls="--")
    ax.axvline(thB, color=GRAY, lw=1.2, ls=":")
    ax.text(thB - 1.2, 62, f"Brewster angle, {thB:.1f}°", fontsize=12, color=GRAY, ha="right")
    rte = 100 * np.interp(thB, th, Gte ** 2)
    ax.plot([thB], [rte], "o", color=RED, ms=7)
    ax.annotate(f"{rte:.1f}%", (thB, rte), xytext=(-10, 10), textcoords="offset points",
                fontsize=12, color=RED, ha="right")
    ax.text(72, 33, "TE", fontsize=14, color=RED, fontweight="bold")
    ax.text(80, 8, "TM", fontsize=14, color=BLUE, fontweight="bold")
    ax.set_xlim(0, 90); ax.set_ylim(0, 100)
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_xticklabels(["0°", "15°", "30°", "45°", "60°", "75°", "90°"])
    ax.set_xlabel("angle of incidence  θᵢ", color=GRAY, fontsize=12)
    ax.set_ylabel("reflected power (%)", color=GRAY, fontsize=12)
    ax.grid(True, color="#e3edf6", lw=1.0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=11)
    save(fig, "L40-water.svg")


if __name__ == "__main__":
    tm_fields()
    brewster()
    tir()
    water()
