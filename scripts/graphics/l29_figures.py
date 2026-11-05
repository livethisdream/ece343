#!/usr/bin/env python3
"""L29 figures: Ampere's law and the field of a line current.

    L29-circulation.svg   a line current inside a closed path and outside it,
                          with a near and a far step that sweep the same
                          angle dφ, and H at each
    L29-two-caps.svg      a path C, a flat surface and a dome that share it as
                          their edge, and one current through both
    L29-line-current.svg  a circular Amperian path around a line current, with
                          H along φ̂
    L29-solid-wire.svg    H against radius for a round wire carrying a uniform
                          current: rising linearly inside, falling as 1/ρ outside

The current flows along +z, out of the page, so H circles counterclockwise.
Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l29_figures.py   ->   book/extras/viz/img/L29-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
FILL = "#e3edf6"      # region inside the path
METAL = "#9aa8b6"     # conductor
CURRENT = "#f3d9d9"   # region carrying current
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


def wire_out(ax, x, y, r=0.13, color=RED):
    """A current out of the page: a circle with a dot."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.8, zorder=6))
    ax.add_patch(Circle((x, y), r * 0.3, fc=color, ec="none", zorder=7))


def path_arrows(ax, xs, ys, idx, color=NAVY):
    for k in idx:
        arrow(ax, xs[k], ys[k], xs[k + 3], ys[k + 3], color=color, lw=1.6, ms=13)


# ---------------------------------------------------------------------------
def blob(t):
    """A lumpy closed path, radius as a function of angle."""
    return 1.55 + 0.26 * np.cos(2 * t + 0.3) + 0.15 * np.sin(3 * t)


def circulation():
    # Sized for the half-width present block (about 480 px), so 16 pt text
    # lands near 16 px on screen.
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.6))
    t = np.linspace(0, 2 * np.pi, 400)
    r = blob(t)
    wires = [(0.0, 0.0), (-2.75, -0.35)]
    for ax, w in zip(axs, wires):
        blank(ax, (-3.3, 2.6), (-2.25, 2.2))
        xs, ys = r * np.cos(t), r * np.sin(t)
        ax.fill(xs, ys, fc=FILL, ec=NAVY, lw=1.8)
        path_arrows(ax, xs, ys, [60, 160, 260, 360])
        wire_out(ax, *w, r=0.16)
        lab(ax, w[0] - 0.24, w[1] - 0.34, "I", size=17, color=RED, ha="right")
        lab(ax, 1.35, -1.55, "C", size=17, color=NAVY)

    # inside: a near step and a far step that sweep the same angle dφ. The far
    # step is longer and its H is weaker, in proportion.
    ax = axs[0]
    dth = 0.34
    for th0, name in ((1.51, "near"), (2.78, "far")):
        t0, t1 = th0 - dth / 2, th0 + dth / 2
        rr = blob(th0)
        ax.add_patch(Wedge((0, 0), rr, np.degrees(t0), np.degrees(t1),
                           fc=AMBER, ec="none", alpha=0.22))
        tt = np.linspace(t0, t1, 30)
        ax.plot(blob(tt) * np.cos(tt), blob(tt) * np.sin(tt), color=AMBER, lw=4.5, zorder=4)
        x, y = rr * np.cos(th0), rr * np.sin(th0)
        L = 1.0 * 1.15 / rr
        arrow(ax, x, y, x - L * np.sin(th0), y + L * np.cos(th0), color=BLUE, lw=2.6, ms=17)
        if name == "near":
            ax.text(x - 0.55, y + 0.22, "H", fontsize=16, color=BLUE, ha="center")
            ax.text(0.16, 0.42, "dφ", fontsize=16, color=AMBER, ha="left")
        else:
            ax.text(x - 0.55, y - 0.15, "H", fontsize=16, color=BLUE, ha="right")
            ax.text(-0.95, 0.12, "dφ", fontsize=16, color=AMBER, ha="center")
    ax.text(-0.35, -2.2, "current inside C", ha="center", fontsize=15, color=GRAY)

    # outside: the angle swept forward on the near side and back on the far side
    ax = axs[1]
    qx, qy = wires[1]
    for ang in (0.08, 0.37):
        ax.plot([qx, qx + 4.9 * np.cos(ang)], [qy, qy + 4.9 * np.sin(ang)],
                color=GRAY, lw=1.1, ls="--")
    ax.add_patch(Wedge((qx, qy), 4.9, np.degrees(0.08), np.degrees(0.37),
                       fc=AMBER, ec="none", alpha=0.18))
    ax.text(qx + 0.55, qy - 0.5, "dφ", fontsize=16, color=AMBER, ha="left")
    ang = 0.225
    s = np.linspace(0, 5, 4000)
    xs, ys = qx + s * np.cos(ang), qy + s * np.sin(ang)
    inside = np.hypot(xs, ys) < blob(np.arctan2(ys, xs))
    idx = np.nonzero(np.diff(inside.astype(int)))[0]
    for k, sign, dy in zip(idx[:2], ("−dφ", "+dφ"), (0.42, 0.42)):
        ax.plot(xs[k], ys[k], "s", color=AMBER, ms=8, zorder=5)
        ax.text(xs[k], ys[k] + dy, sign, ha="center", fontsize=15, color=AMBER)
    ax.text(-0.35, -2.2, "current outside C", ha="center", fontsize=15, color=GRAY)
    save(fig, "L29-circulation.svg")


def two_caps():
    """A path C, two surfaces with C as their edge, and one current through both."""
    fig, ax = plt.subplots(figsize=(4.6, 3.8))
    blank(ax, (-2.3, 2.3), (-1.55, 2.35))
    a, b = 1.6, 0.42                       # the ellipse that draws C in perspective
    t = np.linspace(0, 2 * np.pi, 400)
    # S2: a dome above C, drawn as a half ellipse
    tt = np.linspace(0, np.pi, 200)
    ax.fill(np.r_[a * np.cos(tt), a * np.cos(tt[::-1])],
            np.r_[1.45 * np.sin(tt), -b * np.sin(tt[::-1]) * 0],
            fc="#f6ead6", ec="none", alpha=0.8)
    ax.plot(a * np.cos(tt), 1.45 * np.sin(tt), color=AMBER, lw=1.6, ls="--")
    # S1: the flat disk inside C
    ax.fill(a * np.cos(t), b * np.sin(t), fc=FILL, ec="none", alpha=0.95, zorder=2)
    ax.plot(a * np.cos(t), b * np.sin(t), color=NAVY, lw=2.0, zorder=3)
    for k in (60, 260):
        arrow(ax, a * np.cos(t[k]), b * np.sin(t[k]), a * np.cos(t[k + 6]), b * np.sin(t[k + 6]),
              color=NAVY, lw=1.8, ms=15)
    # the current, piercing both surfaces
    ax.plot([0.35, 0.35], [-1.45, -0.05], color=RED, lw=2.4, zorder=4)
    ax.plot([0.35, 0.35], [0.05, 1.32], color=RED, lw=2.4, ls=(0, (4, 3)), zorder=1)
    arrow(ax, 0.35, 1.32, 0.35, 2.15, color=RED, lw=2.4, ms=16)
    ax.text(0.5, 1.95, "I", fontsize=17, color=RED, fontstyle="italic")
    # normals from the right-hand rule
    arrow(ax, -0.75, 0.0, -0.75, 0.75, color=NAVY, lw=2.0, ms=14)
    ax.text(-0.95, 0.5, "n̂", fontsize=16, color=NAVY, ha="right")
    arrow(ax, -0.95, 1.12, -1.25, 1.75, color=AMBER, lw=2.0, ms=14)
    ax.text(-1.33, 1.6, "n̂", fontsize=16, color=AMBER, ha="right")
    lab(ax, 1.05, -0.12, "S", "1", size=16, color=NAVY)
    lab(ax, 1.3, 1.25, "S", "2", size=16, color=AMBER)
    lab(ax, 1.85, -0.35, "C", size=17, color=NAVY)
    save(fig, "L29-two-caps.svg")


# ---------------------------------------------------------------------------
def line_current():
    fig, ax = plt.subplots(figsize=(4.2, 4.0))
    blank(ax, (-2.0, 2.0), (-1.9, 1.9))
    R = 1.35
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(R * np.cos(t), R * np.sin(t), color=NAVY, lw=1.6, ls="--")
    for th in np.radians([20, 110, 200, 290]):
        x, y = R * np.cos(th), R * np.sin(th)
        arrow(ax, x, y, x - 0.55 * np.sin(th), y + 0.55 * np.cos(th), color=BLUE, lw=2.0, ms=14)
    th = np.radians(110)
    lab(ax, R * np.cos(th) - 0.62 * np.sin(th) - 0.05, R * np.sin(th) + 0.62 * np.cos(th) + 0.12,
        "H", color=BLUE, ha="right", italic=False)
    ax.plot([0, R * np.cos(np.radians(-40))], [0, R * np.sin(np.radians(-40))], color=GRAY, lw=1.1)
    lab(ax, 0.62, -0.22, "ρ", color=GRAY)
    wire_out(ax, 0, 0)
    lab(ax, -0.22, 0.28, "I", color=RED, ha="right")
    lab(ax, 1.05, 1.35, "C", color=NAVY)
    save(fig, "L29-line-current.svg")


# ---------------------------------------------------------------------------
def solid_wire():
    a = 1.0
    rho = np.linspace(0, 4, 600)
    H = np.where(rho < a, rho / a, a / np.maximum(rho, 1e-9))
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.axvspan(0, a, color=CURRENT, alpha=0.7, lw=0)
    ax.plot(rho, H, color=NAVY, lw=2.4)
    ax.set_xlim(0, 4); ax.set_ylim(0, 1.18)
    ax.set_xticks([0, a]); ax.set_xticklabels(["0", "a"], fontsize=13)
    ax.set_yticks([0, 1]); ax.set_yticklabels(["0", "I/2πa"], fontsize=13)
    ax.set_xlabel("ρ", fontsize=14, fontstyle="italic", color=INK)
    ax.text(0.5, 1.07, "wire", ha="center", fontsize=12, color=RED)
    ax.text(2.4, 0.62, "∝ 1/ρ", fontsize=13, color=NAVY)
    ax.text(0.62, 0.35, "∝ ρ", fontsize=13, color=NAVY)
    lab(ax, 3.7, 0.12, "H", "φ", color=NAVY)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY)
    save(fig, "L29-solid-wire.svg")


if __name__ == "__main__":
    circulation()
    two_caps()
    line_current()
    solid_wire()
