#!/usr/bin/env python3
"""L29 figures: Ampere's law and the field of a line current.

    L29-circulation.svg   a line current inside a closed path and outside it,
                          with one step dl and the angle dφ it sweeps
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
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.0))
    t = np.linspace(0, 2 * np.pi, 400)
    r = blob(t)
    wires = [(0.0, 0.0), (-2.75, -0.35)]
    for ax, w in zip(axs, wires):
        blank(ax, (-3.3, 2.6), (-2.1, 2.1))
        xs, ys = r * np.cos(t), r * np.sin(t)
        ax.fill(xs, ys, fc=FILL, ec=NAVY, lw=1.6)
        path_arrows(ax, xs, ys, [60, 160, 260, 360])
        wire_out(ax, *w)
        lab(ax, w[0] - 0.2, w[1] - 0.3, "I", color=RED, ha="right")
    lab(axs[0], 1.25, -1.45, "C", color=NAVY, italic=True)
    lab(axs[1], 1.25, -1.45, "C", color=NAVY, italic=True)

    # inside: one step dl, its radial ray, and the angle it sweeps
    ax = axs[0]
    th0, dth = 0.75, 0.2
    for th in (th0 - dth / 2, th0 + dth / 2):
        rr = blob(th)
        ax.plot([0, rr * np.cos(th)], [0, rr * np.sin(th)], color=GRAY, lw=1.0, ls="--")
    tt = np.linspace(th0 - dth / 2, th0 + dth / 2, 30)
    ax.plot(blob(tt) * np.cos(tt), blob(tt) * np.sin(tt), color=AMBER, lw=4, zorder=4)
    ax.add_patch(Wedge((0, 0), 0.6, np.degrees(th0 - dth / 2), np.degrees(th0 + dth / 2),
                       fc=AMBER, ec="none", alpha=0.45))
    lab(ax, 0.42, 0.62, "dφ", size=13, color=AMBER, ha="left", italic=False)
    rr = blob(th0 + dth / 2)
    lab(ax, rr * np.cos(th0 + dth / 2) - 0.1, rr * np.sin(th0 + dth / 2) + 0.22, "dl",
        size=13, color=AMBER, ha="right", italic=False)
    ax.text(-0.35, -2.05, "current inside C", ha="center", fontsize=12, color=GRAY)

    # outside: the angle swept forward on the near side and back on the far side
    ax = axs[1]
    qx, qy = wires[1]
    for ang in (0.13, 0.32):
        ax.plot([qx, qx + 4.9 * np.cos(ang)], [qy, qy + 4.9 * np.sin(ang)],
                color=GRAY, lw=1.0, ls="--")
    ax.add_patch(Wedge((qx, qy), 0.6, np.degrees(0.13), np.degrees(0.32),
                       fc=AMBER, ec="none", alpha=0.45))
    lab(ax, qx + 0.5, qy - 0.32, "dφ", size=13, color=AMBER, ha="left", italic=False)
    ang = 0.225
    s = np.linspace(0, 5, 4000)
    xs, ys = qx + s * np.cos(ang), qy + s * np.sin(ang)
    inside = np.hypot(xs, ys) < blob(np.arctan2(ys, xs))
    idx = np.nonzero(np.diff(inside.astype(int)))[0]
    for k, sign in zip(idx[:2], ("−dφ", "+dφ")):
        ax.plot(xs[k], ys[k], "s", color=AMBER, ms=7, zorder=5)
        ax.text(xs[k], ys[k] + 0.32, sign, ha="center", fontsize=12, color=AMBER)
    ax.text(-0.35, -2.05, "current outside C", ha="center", fontsize=12, color=GRAY)
    save(fig, "L29-circulation.svg")


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
    line_current()
    solid_wire()
