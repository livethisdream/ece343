#!/usr/bin/env python3
"""L02 figures: scalar and vector fields, and a traveling wave.

    L02-fields.svg          a scalar field (the potential of two charges, as a
                            colored map) beside a vector field (the electric
                            field of the same charges, as arrows)
    L02-traveling-pulse.svg a pulse f(x) and the same pulse a time later,
                            f(x - v dt): same shape, moved a distance v dt

Labels are plain Unicode (see CLAUDE.md).

    python3 scripts/graphics/l02_figures.py   ->   book/extras/viz/img/L02-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, RED, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b"
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


# Two point charges, +q at (-1, 0) and -q at (+1, 0), in arbitrary units.
CHARGES = [(-1.0, 0.0, 1.0), (1.0, 0.0, -1.0)]


def potential(x, y):
    v = np.zeros_like(x)
    for cx, cy, q in CHARGES:
        v += q / np.hypot(x - cx, y - cy)
    return v


def efield(x, y):
    ex, ey = np.zeros_like(x), np.zeros_like(y)
    for cx, cy, q in CHARGES:
        dx, dy = x - cx, y - cy
        r3 = np.hypot(dx, dy) ** 3
        ex += q * dx / r3
        ey += q * dy / r3
    return ex, ey


def fields():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9))
    lim = 2.6

    ax = axs[0]
    x, y = np.meshgrid(np.linspace(-lim, lim, 300), np.linspace(-1.9, 1.9, 220))
    v = np.clip(potential(x, y), -3, 3)
    ax.contourf(x, y, v, levels=24, cmap="RdBu_r", vmin=-3, vmax=3)
    ax.contour(x, y, v, levels=np.linspace(-2.5, 2.5, 11), colors="white", linewidths=0.6)
    ax.set_title("scalar field: potential V(x, y)", fontsize=13, color=INK, pad=8)

    ax = axs[1]
    x, y = np.meshgrid(np.linspace(-lim, lim, 17), np.linspace(-1.8, 1.8, 13))
    ex, ey = efield(x, y)
    mag = np.hypot(ex, ey)
    near = np.zeros_like(mag, dtype=bool)
    for cx, cy, _ in CHARGES:
        near |= np.hypot(x - cx, y - cy) < 0.35
    ux, uy = np.where(near, np.nan, ex / mag), np.where(near, np.nan, ey / mag)
    ax.quiver(x, y, ux, uy, np.log(mag), cmap="Blues", clim=(-3.5, 2.5),
              scale=26, width=0.0055, headwidth=3.6)
    ax.set_title("vector field: E(x, y)", fontsize=13, color=INK, pad=8)

    for ax in axs:
        for cx, cy, q in CHARGES:
            ax.plot(cx, cy, "o", ms=13, color=RED if q > 0 else BLUE, mec="white", mew=1.2, zorder=4)
            ax.text(cx, cy, "+" if q > 0 else "−", ha="center", va="center", color="white",
                    fontsize=13, fontweight="bold", zorder=5)
        ax.set_aspect("equal")
        ax.set_xlim(-lim, lim); ax.set_ylim(-1.9, 1.9)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#c7d2e0")
    fig.subplots_adjust(wspace=0.08)
    save(fig, "L02-fields.svg")


def traveling_pulse():
    fig, ax = plt.subplots(figsize=(9.0, 2.9))
    x = np.linspace(0, 10, 800)
    a, shift = 2.5, 4.0
    f = lambda u: np.exp(-((u - a) / 0.7) ** 2)
    ax.plot(x, f(x), color=GRAY, lw=2.2, ls="--")
    ax.plot(x, f(x - shift), color=NAVY, lw=2.8)
    ax.text(a, 1.08, "f(x) at t", ha="center", va="bottom", fontsize=12.5, color=GRAY, fontstyle="italic")
    ax.text(a + shift, 1.08, "f(x − vΔt) at t + Δt", ha="center", va="bottom", fontsize=12.5,
            color=NAVY, fontstyle="italic")
    ax.annotate("", xy=(a + shift, 0.55), xytext=(a, 0.55),
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.8))
    ax.text(a + shift / 2, 0.6, "vΔt", ha="center", va="bottom", fontsize=13, color=AMBER, fontstyle="italic")
    ax.axhline(0, color="#c7d2e0", lw=1.2)
    ax.set_xlim(0, 10); ax.set_ylim(-0.08, 1.35)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.text(10, -0.04, "x", ha="right", va="top", fontsize=13, color=GRAY, fontstyle="italic")
    save(fig, "L02-traveling-pulse.svg")


if __name__ == "__main__":
    fields()
    traveling_pulse()
