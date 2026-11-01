#!/usr/bin/env python3
"""L20 figures: Gauss's law and the four symmetric charge distributions.

    L20-solid-angle.svg   a cone from a point charge through a closed surface,
                          with the charge inside and outside
    L20-sphere.svg        a spherical Gaussian surface around a point charge
    L20-cylinder.svg      a cylindrical Gaussian surface around a line charge
    L20-pillbox.svg       a pillbox through a sheet of charge
    L20-coax.svg          the coax cross section with three Gaussian circles,
                          and the field against radius
    L20-rod.svg           the field of a uniformly charged cylinder against radius

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l20_figures.py   ->   book/extras/viz/img/L20-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Wedge

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL = "#e3edf6"      # dielectric, Gaussian surface fill
METAL = "#9aa8b6"     # conductor
CHARGE = "#f3d9d9"    # charged region
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


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=1.6, ms=12):
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


# ---------------------------------------------------------------------------
def blob(t):
    """A lumpy closed curve, radius as a function of angle."""
    return 1.55 + 0.28 * np.cos(2 * t) + 0.16 * np.sin(3 * t + 0.4)


def solid_angle():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.0))
    t = np.linspace(0, 2 * np.pi, 400)
    r = blob(t)
    for ax, q in zip(axs, [(0.0, 0.0), (-2.75, -0.35)]):
        blank(ax, (-3.3, 2.6), (-2.1, 2.1))
        ax.fill(r * np.cos(t), r * np.sin(t), fc=FILL, ec=NAVY, lw=1.6)
        ax.plot(*q, "o", color=RED, ms=8, zorder=5)
        lab(ax, q[0] - 0.12, q[1] - 0.28, "Q", color=RED, ha="right")

    # inside: one crossing
    ax = axs[0]
    th0, dth = 0.55, 0.16
    for th in (th0 - dth / 2, th0 + dth / 2):
        rr = blob(th)
        ax.plot([0, rr * np.cos(th)], [0, rr * np.sin(th)], color=GRAY, lw=1.0, ls="--")
    tt = np.linspace(th0 - dth / 2, th0 + dth / 2, 30)
    ax.plot(blob(tt) * np.cos(tt), blob(tt) * np.sin(tt), color=AMBER, lw=4)
    ax.add_patch(Wedge((0, 0), 0.55, np.degrees(th0 - dth / 2), np.degrees(th0 + dth / 2),
                       fc=AMBER, ec="none", alpha=0.45))
    lab(ax, 0.62, 0.05, "dΩ", size=13, color=AMBER, ha="left", italic=False)
    rr = blob(th0); px, py = rr * np.cos(th0), rr * np.sin(th0)
    # outward normal from the curve's tangent
    dt = 1e-3
    x2, y2 = blob(th0 + dt) * np.cos(th0 + dt), blob(th0 + dt) * np.sin(th0 + dt)
    tx, ty = x2 - px, y2 - py
    nx, ny = ty, -tx; n = np.hypot(nx, ny); nx, ny = nx / n, ny / n
    arrow(ax, px, py, px + 0.7 * nx, py + 0.7 * ny, color=NAVY)
    lab(ax, px + 0.78 * nx + 0.05, py + 0.78 * ny + 0.12, "n̂", color=NAVY, ha="left", italic=False)
    arrow(ax, px, py, px + 0.7 * np.cos(th0), py + 0.7 * np.sin(th0), color=RED)
    lab(ax, px + 0.8 * np.cos(th0) + 0.05, py + 0.8 * np.sin(th0) - 0.05, "r̂", color=RED, ha="left", italic=False)
    lab(ax, px - 0.45, py + 0.05, "dS", size=13, color=AMBER, ha="right", italic=False)
    ax.text(-0.35, -2.05, "charge inside", ha="center", fontsize=12, color=GRAY)

    # outside: the cone crosses twice
    ax = axs[1]
    qx, qy = -2.75, -0.35
    for ang in (0.17, 0.28):
        ax.plot([qx, qx + 4.9 * np.cos(ang)], [qy, qy + 4.9 * np.sin(ang)],
                color=GRAY, lw=1.0, ls="--")
    ax.add_patch(Wedge((qx, qy), 0.55, np.degrees(0.17), np.degrees(0.28),
                       fc=AMBER, ec="none", alpha=0.45))
    lab(ax, qx + 0.6, qy - 0.05, "dΩ", size=13, color=AMBER, ha="left", italic=False)
    # crossings with the blob, found numerically along the mid ray
    ang = 0.225
    s = np.linspace(0, 5, 4000)
    xs, ys = qx + s * np.cos(ang), qy + s * np.sin(ang)
    inside = np.hypot(xs, ys) < blob(np.arctan2(ys, xs))
    idx = np.nonzero(np.diff(inside.astype(int)))[0]
    for k, sign in zip(idx[:2], ("in: −", "out: +")):
        ax.plot(xs[k], ys[k], "s", color=AMBER, ms=7)
        ax.text(xs[k], ys[k] + 0.32, sign + "dΩ", ha="center", fontsize=12, color=AMBER)
    ax.text(-0.35, -2.05, "charge outside", ha="center", fontsize=12, color=GRAY)
    save(fig, "L20-solid-angle.svg")


# ---------------------------------------------------------------------------
def sphere():
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    blank(ax, (-2.0, 2.0), (-1.9, 1.9))
    ax.add_patch(Circle((0, 0), 1.25, fc=FILL, ec=NAVY, lw=1.6))
    ax.add_patch(Ellipse((0, 0), 2.5, 0.6, fc="none", ec=NAVY, lw=1.0, ls="--"))
    ax.plot(0, 0, "o", color=RED, ms=8, zorder=5)
    lab(ax, -0.15, -0.25, "Q", color=RED, ha="right")
    for a in np.radians([20, 70, 110, 160, 200, 250, 290, 340]):
        arrow(ax, 1.25 * np.cos(a), 1.25 * np.sin(a), 1.8 * np.cos(a), 1.8 * np.sin(a), color=BLUE, lw=1.4)
    ax.plot([0, 1.25 * np.cos(np.radians(45))], [0, 1.25 * np.sin(np.radians(45))], color=GRAY, lw=1.0)
    lab(ax, 0.32, 0.58, "r", color=GRAY)
    lab(ax, 1.62, 1.18, "D", color=BLUE, italic=False)
    save(fig, "L20-sphere.svg")


def cylinder():
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    blank(ax, (-1.9, 2.0), (-2.0, 2.1))
    R, H, e = 0.9, 1.4, 0.28
    ax.add_patch(Polygon([(-R, -H), (-R, H), (R, H), (R, -H)], fc=FILL, ec="none"))
    ax.plot([-R, -R], [-H, H], color=NAVY, lw=1.6); ax.plot([R, R], [-H, H], color=NAVY, lw=1.6)
    ax.add_patch(Ellipse((0, H), 2 * R, 2 * e, fc=FILL, ec=NAVY, lw=1.6))
    t = np.linspace(np.pi, 2 * np.pi, 60)
    ax.plot(R * np.cos(t), -H + e * np.sin(t), color=NAVY, lw=1.6)
    t = np.linspace(0, np.pi, 60)
    ax.plot(R * np.cos(t), -H + e * np.sin(t), color=NAVY, lw=1.0, ls="--")
    ax.plot([0, 0], [-1.95, 1.95], color=RED, lw=3)
    lab(ax, -0.18, 1.85, "ρ", "l", color=RED, ha="right")
    for y in (-0.8, 0.0, 0.8):
        arrow(ax, R, y, R + 0.65, y, color=BLUE, lw=1.4)
        arrow(ax, -R, y, -R - 0.65, y, color=BLUE, lw=1.4)
    ax.plot([0, R], [0.4, 0.4], color=GRAY, lw=1.0)
    lab(ax, 0.45, 0.58, "ρ", color=GRAY)
    ax.annotate("", xy=(R + 0.95, H), xytext=(R + 0.95, -H),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
    lab(ax, R + 1.1, 0.0, "L", color=GRAY, ha="left")
    arrow(ax, 0.45, H, 0.45, H + 0.55, color=AMBER, lw=1.2)
    lab(ax, 0.58, H + 0.45, "ẑ", color=AMBER, ha="left", italic=False)
    save(fig, "L20-cylinder.svg")


def pillbox():
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    blank(ax, (-2.7, 2.9), (-1.9, 1.9))
    sheet = [(-2.5, -0.55), (1.6, -0.55), (2.6, 0.55), (-1.5, 0.55)]
    ax.add_patch(Polygon(sheet, fc=CHARGE, ec=RED, lw=1.4))
    lab(ax, -1.95, -0.25, "ρ", "s", color=RED)
    w, d, h = 1.4, 0.5, 0.8                 # box half-width, depth offset, half-height
    def face(z):
        return [(-w / 2, z - d / 2), (w / 2, z - d / 2), (w / 2 + d, z + d / 2), (-w / 2 + d, z + d / 2)]
    for z in (h, -h):
        ax.add_patch(Polygon(face(z), fc=FILL, ec=NAVY, lw=1.5, alpha=0.95))
    for x in (-w / 2, w / 2):
        ax.plot([x, x], [-h - d / 2, h - d / 2], color=NAVY, lw=1.5)
    ax.plot([w / 2 + d] * 2, [-h + d / 2, h + d / 2], color=NAVY, lw=1.5)
    cx = d / 2
    arrow(ax, cx, h, cx, h + 0.85, color=BLUE)
    arrow(ax, cx, -h, cx, -h - 0.85, color=BLUE)
    lab(ax, cx + 0.15, h + 0.7, "D", color=BLUE, ha="left", italic=False)
    lab(ax, cx + 0.15, -h - 0.7, "D", color=BLUE, ha="left", italic=False)
    lab(ax, -w / 2 + d / 2 - 0.05, h + 0.12, "A", size=13, color=NAVY, ha="right")
    arrow(ax, 2.45, -1.2, 2.45, -0.4, color=AMBER, lw=1.2)
    lab(ax, 2.58, -0.55, "ẑ", color=AMBER, ha="left", italic=False)
    save(fig, "L20-pillbox.svg")


# ---------------------------------------------------------------------------
def coax():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.6, 3.9), gridspec_kw=dict(width_ratios=[1, 1.35]))
    blank(ax, (-2.0, 2.0), (-2.0, 2.0))
    a, b, t = 0.42, 1.35, 0.14
    ax.add_patch(Circle((0, 0), b + t, fc=METAL, ec=INK, lw=1.2))
    ax.add_patch(Circle((0, 0), b, fc=FILL, ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), a, fc=METAL, ec=INK, lw=1.2))
    for rr, c in ((0.25, AMBER), (0.88, NAVY), (1.75, GRAY)):
        ax.add_patch(Circle((0, 0), rr, fc="none", ec=c, lw=1.4, ls="--"))
    for ang, rr, lbl in ((-0.6, a, "a"), (2.5, b, "b")):
        ax.plot([0, rr * np.cos(ang)], [0, rr * np.sin(ang)], color=INK, lw=1.0)
    lab(ax, 0.30, -0.36, "a", size=13)
    lab(ax, -0.5, 0.62, "b", size=13)
    lab(ax, 0.0, 0.62, "+ρ", "l", size=12, color=RED)
    lab(ax, 1.25, -1.62, "−ρ", "l", size=12, color=RED, ha="left")

    rho = np.linspace(0.0, 2.0, 600)
    E = np.where((rho > a) & (rho < b), a / np.maximum(rho, 1e-9), 0.0)
    bx.plot(rho, E, color=BLUE, lw=2.6)
    bx.axvspan(a, b, color=FILL, zorder=0)
    bx.set_xlim(0, 2.0); bx.set_ylim(0, 1.15)
    bx.set_xticks([a, b]); bx.set_xticklabels(["a", "b"], fontstyle="italic", fontsize=14)
    bx.set_yticks([])
    bx.set_xlabel("ρ", fontstyle="italic", fontsize=14, color=GRAY)
    bx.text(0.04, 1.08, "E", fontsize=14, color=GRAY, fontstyle="italic", transform=bx.transData)
    bx.text(0.8, 0.55, "∝ 1/ρ", fontsize=13, color=BLUE)
    bx.text(0.2, 0.06, "0", fontsize=12, color=BLUE, ha="center")
    bx.text(1.7, 0.06, "0", fontsize=12, color=BLUE, ha="center")
    for s in ("top", "right"):
        bx.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        bx.spines[s].set_color("#c7d2e0")
    bx.tick_params(colors=GRAY)
    save(fig, "L20-coax.svg")


def rod():
    fig, bx = plt.subplots(figsize=(7.2, 3.3))
    a = 1.0
    rho = np.linspace(0.0, 3.0, 600)
    E = np.where(rho < a, rho / a, a / np.maximum(rho, 1e-9))
    bx.axvspan(0, a, color=CHARGE, zorder=0)
    bx.plot(rho, E, color=BLUE, lw=2.6)
    bx.set_xlim(0, 3.0); bx.set_ylim(0, 1.2)
    bx.set_xticks([a]); bx.set_xticklabels(["a"], fontstyle="italic", fontsize=14)
    bx.set_yticks([])
    bx.set_xlabel("ρ", fontstyle="italic", fontsize=14, color=GRAY)
    bx.text(0.04, 1.1, "E", fontsize=14, color=GRAY, fontstyle="italic")
    bx.text(0.28, 0.12, "∝ ρ", fontsize=13, color=BLUE)
    bx.text(1.9, 0.62, "∝ 1/ρ", fontsize=13, color=BLUE)
    bx.text(0.5, 1.03, "inside the charge", fontsize=11, color=RED, ha="center")
    for s in ("top", "right"):
        bx.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        bx.spines[s].set_color("#c7d2e0")
    bx.tick_params(colors=GRAY)
    save(fig, "L20-rod.svg")


if __name__ == "__main__":
    solid_angle()
    sphere()
    cylinder()
    pillbox()
    coax()
    rod()
