#!/usr/bin/env python3
"""L31 figures: the magnetic boundary conditions.

    L31-loop.svg      the thin loop that straddles the boundary, with a surface
                      current crossing it, for the tangential condition
    L31-pillbox.svg   the flat pillbox, for the normal condition on B
    L31-iron.svg      an iron cylinder (mu_r = 1000) in a uniform field: the
                      lines of B bend to meet the iron almost along the normal,
                      with one surface point marked (80 deg inside, 0.32 deg out)

The layout follows L24's figures, so the two lessons read as a pair. Labels
are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l31_figures.py   ->   book/extras/viz/img/L31-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, FancyArrowPatch, Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL1 = "#f2f7fb"     # region 1
FILL2 = "#d6e5f2"     # region 2
IRON = "#b7c3cf"      # a high-permeability material
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


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def two_regions(ax, xlim=(-3.2, 3.2), ylim=(-1.6, 1.6), fill2=FILL2, sym="μ"):
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.add_patch(Rectangle((xlim[0], 0), xlim[1] - xlim[0], ylim[1], fc=FILL1, ec="none"))
    ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], -ylim[0], fc=fill2, ec="none"))
    ax.plot(xlim, [0, 0], color=INK, lw=1.6)
    lab(ax, xlim[0] + 0.25, ylim[1] - 0.3, sym, "1", ha="left")
    lab(ax, xlim[0] + 0.25, ylim[0] + 0.3, sym, "2", ha="left")


def unit_vectors(ax, xlim=(-3.2, 3.2), ylim=(-1.6, 1.6)):
    ox, oy = xlim[1] - 0.95, ylim[0] + 0.3
    arrow(ax, ox, oy, ox + 0.55, oy, color=GRAY, lw=1.4, head=10)
    arrow(ax, ox, oy, ox, oy + 0.55, color=GRAY, lw=1.4, head=10)
    lab(ax, ox + 0.68, oy, "t̂", size=13, color=GRAY, ha="left", italic=False, bold=True)
    lab(ax, ox, oy + 0.72, "n̂", size=13, color=GRAY, italic=False, bold=True)


def into_page(ax, x, y, r=0.085, color=RED):
    """The symbol for a current flowing into the page: a circle with a cross."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.2, zorder=4))
    d = r * 0.62
    ax.plot([x - d, x + d], [y - d, y + d], color=color, lw=1.1, zorder=5)
    ax.plot([x - d, x + d], [y + d, y - d], color=color, lw=1.1, zorder=5)


# ---------------------------------------------------------------------------
def loop():
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    xlim, ylim = (-3.2, 3.4), (-1.6, 1.6)
    two_regions(ax, xlim, ylim)
    unit_vectors(ax, xlim, ylim)
    x0, x1, h = -1.9, 1.1, 0.8
    px = 2.05                                  # where the two fields meet the boundary
    # surface current along the boundary, flowing into the page (along n x t);
    # leave room for the h dimension and the field arrows
    for x in np.arange(-2.95, 3.2, 0.3):
        if abs(x - (x1 + 0.35)) > 0.17 and abs(x - px) > 0.2:
            into_page(ax, x, 0.0)
    lab(ax, -2.2, -0.32, "J", "s", size=14, color=RED, italic=False, bold=True)
    a, b, c, d = (x0, h / 2), (x1, h / 2), (x1, -h / 2), (x0, -h / 2)
    for p, q in ((a, b), (b, c), (c, d), (d, a)):
        mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=NAVY, lw=1.8)
        arrow(ax, p[0], p[1], mid[0], mid[1], color=NAVY, lw=1.8, head=13)
    for (qx, qy), name, va in ((a, "a", "bottom"), (b, "b", "bottom"), (c, "c", "top"), (d, "d", "top")):
        ax.plot(qx, qy, "o", color=NAVY, ms=4)
        ax.text(qx + (-0.12 if name in "ad" else 0.12), qy + (0.08 if va == "bottom" else -0.08),
                name, color=NAVY, fontsize=13, ha="right" if name in "ad" else "left", va=va)
    ax.annotate("", xy=(x0, -1.05), xytext=(x1, -1.05),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, (x0 + x1) / 2, -1.28, "W", size=14, color=GRAY)
    ax.annotate("", xy=(x1 + 0.35, h / 2), xytext=(x1 + 0.35, -h / 2),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, x1 + 0.52, 0.22, "h", size=14, color=GRAY, ha="left")
    # the fields on each side: the surface current makes the tangential parts
    # differ, H_t1 > H_t2. Dashed lines resolve each into its tangential and
    # normal parts, the components the two conditions compare.
    t1, n1, t2, n2 = 0.75, 1.0, 0.25, 0.7
    for (x0_, y0_, x1_, y1_) in ((px, n1, px + t1, n1), (px, 0.0, px, n1),
                                 (px - t2, -n2, px, -n2), (px, -n2, px, 0.0)):
        ax.plot([x0_, x1_], [y0_, y1_], color=AMBER, lw=1.4, ls=(0, (4, 3)))
    arrow(ax, px, 0.0, px + t1, n1, color=NAVY, lw=2.2)
    lab(ax, px + t1 + 0.1, n1 * 0.55, "H", "1", color=NAVY, italic=False, bold=True, ha="left")
    lab(ax, px + t1 / 2, n1 + 0.2, "H", "t1", size=13, color=AMBER, ha="center")
    lab(ax, px - 0.2, n1 * 0.5, "H", "n1", size=13, color=AMBER, ha="right")
    arrow(ax, px - t2, -n2, px, 0.0, color=BLUE, lw=2.2)
    lab(ax, px - t2 - 0.12, -n2 * 0.45, "H", "2", color=BLUE, italic=False, bold=True, ha="right")
    lab(ax, px - t2 / 2, -n2 - 0.2, "H", "t2", size=13, color=AMBER, ha="center")
    lab(ax, px + 0.1, -n2 * 0.45, "H", "n2", size=13, color=AMBER, ha="left")
    save(fig, "L31-loop.svg")


def pillbox():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    two_regions(ax)
    unit_vectors(ax)
    cx, w, h, e = -0.5, 2.6, 1.0, 0.32
    ax.plot([cx - w / 2, cx - w / 2], [-h / 2, h / 2], color=NAVY, lw=1.6)
    ax.plot([cx + w / 2, cx + w / 2], [-h / 2, h / 2], color=NAVY, lw=1.6)
    ax.add_patch(Ellipse((cx, h / 2), w, e, fc="none", ec=NAVY, lw=1.6))
    ax.add_patch(Ellipse((cx, -h / 2), w, e, fc="none", ec=NAVY, lw=1.6, ls="--"))
    lab(ax, cx + w / 2 + 0.12, h / 2 + 0.12, "ΔA", size=14, color=NAVY, ha="left")
    ax.annotate("", xy=(cx - w / 2 - 0.3, h / 2), xytext=(cx - w / 2 - 0.3, -h / 2),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
    lab(ax, cx - w / 2 - 0.48, 0.28, "h", size=14, color=GRAY, ha="right")
    arrow(ax, cx - 0.55, h / 2, cx - 0.55, h / 2 + 0.75, color=GRAY, lw=1.4, head=10)
    lab(ax, cx - 0.7, h / 2 + 0.62, "n̂", size=13, color=GRAY, ha="right", italic=False, bold=True)
    arrow(ax, cx - 0.55, -h / 2, cx - 0.55, -h / 2 - 0.75, color=GRAY, lw=1.4, head=10)
    lab(ax, cx - 0.7, -h / 2 - 0.62, "−n̂", size=13, color=GRAY, ha="right", italic=False, bold=True)
    arrow(ax, cx + 0.45, h / 2, cx + 0.95, h / 2 + 1.0, color=NAVY, lw=2.2)
    lab(ax, cx + 1.05, h / 2 + 0.95, "B", "1", color=NAVY, italic=False, bold=True, ha="left")
    arrow(ax, cx - 0.35, -h / 2 - 0.85, cx + 0.45, -h / 2, color=BLUE, lw=2.2)
    lab(ax, cx + 0.5, -h / 2 - 0.6, "B", "2", color=BLUE, italic=False, bold=True, ha="left")
    save(fig, "L31-pillbox.svg")


def iron():
    """An iron cylinder (mu_r = 1000) in a uniform applied field, the exact
    two-dimensional solution. With alpha = (1 - mu_r)/(1 + mu_r) and the
    cylinder's radius a,
        outside:  H = H0 [ (1 - alpha a^2/r^2) cos(phi) r - (1 + alpha a^2/r^2) sin(phi) phi ]
        inside:   H = H0 2/(1 + mu_r) x
    which keeps tangential H and normal B continuous at r = a. B = mu H on
    each side; the streamlines are lines of B."""
    mur, a = 1000.0, 1.0
    alpha = (1 - mur) / (1 + mur)
    x, y = np.meshgrid(np.linspace(-3.2, 3.2, 401), np.linspace(-1.9, 1.9, 241))
    r, ph = np.hypot(x, y), np.arctan2(y, x)
    rr = np.maximum(r, 1e-9)
    hr = (1 - alpha * a**2 / rr**2) * np.cos(ph)
    hp = -(1 + alpha * a**2 / rr**2) * np.sin(ph)
    bx = hr * np.cos(ph) - hp * np.sin(ph)
    by = hr * np.sin(ph) + hp * np.cos(ph)
    inside = r < a
    bx[inside] = mur * 2 / (1 + mur)          # B inside, in units of mu0 H0
    by[inside] = 0.0

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-1.9, 1.9)
    ax.add_patch(Rectangle((-3.2, -1.9), 6.4, 3.8, fc=FILL1, ec="none", zorder=0))
    ax.add_patch(Circle((0, 0), a, fc=IRON, ec=INK, lw=1.4, zorder=1))
    seeds = np.column_stack([np.full(15, -3.15), np.linspace(-1.75, 1.75, 15)])
    ax.streamplot(x, y, bx, by, start_points=seeds, color=NAVY, linewidth=1.3,
                  arrowsize=1.1, density=4, broken_streamlines=False, zorder=2)
    ax.text(0, -0.55, "iron", fontsize=13, color=INK, ha="center", va="center", zorder=3,
            bbox=dict(boxstyle="round,pad=0.2", fc=IRON, ec="none"))
    ax.text(2.9, 1.65, "air", fontsize=13, color=GRAY, ha="right", va="center", zorder=3)
    lab(ax, -2.95, 1.62, "B", "", color=NAVY, italic=False, bold=True, ha="left")
    # direction arrows on the far-left lines, where the applied field is uniform
    for yy in (-1.5, -0.75, 0.75, 1.5):
        arrow(ax, -2.75, yy, -2.45, yy, color=NAVY, lw=1.3, head=11)
    # one surface point at 80 degrees around the cylinder: the field inside is
    # 80 degrees from the normal, the field just outside 0.32 degrees from it
    phi = np.radians(80)
    sx, sy = a * np.cos(phi), a * np.sin(phi)
    nx, ny = np.cos(phi), np.sin(phi)
    ax.plot([sx - 0.75 * nx, sx + 0.75 * nx], [sy - 0.75 * ny, sy + 0.75 * ny],
            color=GRAY, lw=1.1, ls=(0, (3, 3)), zorder=4)
    arrow(ax, sx - 0.4, sy - 0.04, sx, sy, color=AMBER, lw=2.0, head=11)
    th_out = np.arctan(np.tan(phi) / mur)
    ox, oy = np.cos(phi - th_out), np.sin(phi - th_out)
    arrow(ax, sx, sy, sx + 0.62 * ox, sy + 0.62 * oy, color=AMBER, lw=2.0, head=11)
    ax.text(sx - 0.3, sy - 0.26, "80°", fontsize=12, color=AMBER, ha="center", va="center", zorder=5,
            bbox=dict(boxstyle="round,pad=0.12", fc=IRON, ec="none"))
    ax.text(sx + 0.62 * ox + 0.12, sy + 0.62 * oy, f"{np.degrees(th_out):.2f}° from the normal",
            fontsize=12, color=AMBER, ha="left", va="center", zorder=5,
            bbox=dict(boxstyle="round,pad=0.12", fc=FILL1, ec="none"))
    save(fig, "L31-iron.svg")


if __name__ == "__main__":
    loop()
    pillbox()
    iron()
