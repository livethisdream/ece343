#!/usr/bin/env python3
"""L36 figures: plane-wave solutions in lossless and lossy media.

    L36-decaying-wave.svg   a snapshot of E_x(z) for a wave traveling in +z in a
                            lossy medium, with its envelope ±|E0+| e^(−αz) and the
                            skin depth δ = 1/α marked
    L36-regimes.svg         α and β, normalized to ω√(με), against the ratio
                            σ/(ωε), with the low-loss and good-conductor limits
                            and three materials marked

Labels are minimal and plain Unicode (see CLAUDE.md); the lesson text does the
explaining.

    python3 scripts/graphics/l36_figures.py   ->   book/extras/viz/img/L36-*.svg
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

NAVY, AMBER, GREEN, GRAY, INK = "#004a85", "#8a5a00", "#1d7a4d", "#5b6573", "#15202b"
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


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=14)


def decaying_wave():
    """E_x(z, 0) = |E0+| e^(−αz) cos(βz) for a wave traveling in +z in a lossy
    medium. Depth is in units of δ = 1/α; here β = 4π/δ, two wavelengths per
    skin depth, so the oscillation stays visible under the envelope. The
    figure is drawn at 6.2 in so its 14 pt labels stay readable on a phone."""
    z = np.linspace(0, 3, 1200)                  # z/δ
    env = np.exp(-z)
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    ax.plot(z, env * np.cos(4 * np.pi * z), color=NAVY, lw=2.4)
    ax.plot(z, env, color=AMBER, lw=1.6, ls="--")
    ax.plot(z, -env, color=AMBER, lw=1.6, ls="--")
    ax.axhline(0, color="#c7d2e0", lw=1.0)
    ax.plot([1, 1], [-1.05, np.exp(-1)], color=GRAY, lw=1.0, ls=":")
    ax.plot(1, np.exp(-1), "o", color=AMBER, ms=6)
    ax.text(1.06, np.exp(-1) + 0.1, "1/e", fontsize=15, color=AMBER)
    ax.text(1.65, 0.32, "|E₀⁺| e⁻ᵅᶻ", fontsize=15, color=AMBER)
    ax.set_xlim(0, 3); ax.set_ylim(-1.05, 1.08)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["0", "δ", "2δ", "3δ"])
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(["−|E₀⁺|", "0", "|E₀⁺|"])
    ax.set_xlabel("depth z", color=GRAY, fontsize=14)
    style(ax)
    save(fig, "L36-decaying-wave.svg")


# Materials marked on the regimes plot: name, σ/(ωε), label offset (points).
MATERIALS = [
    ("polyethylene", 2e-4, (9, -5)),
    ("seawater, 1 GHz", 0.888, (9, -16)),
    ("seawater, 10 kHz", 8.88e4, (-132, 9)),
]


def regimes():
    """α/ω√(με) and β/ω√(με) against p = σ/(ωε), exactly. The two limits are
    dashed, drawn on top, and run past the region where they hold, so the eye
    can see where each one departs from the exact curve. Three materials are
    marked on the α curve; copper (p = 10¹⁰) is off the right edge."""
    p = np.logspace(-4, 5, 500)
    g = 1j * np.sqrt(1 - 1j * p)
    a, b = g.real, g.imag
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.loglog(p, b, color=NAVY, lw=2.6, zorder=2)
    ax.loglog(p, a, color=AMBER, lw=2.6, zorder=2)
    lo = p < 10
    ax.loglog(p[lo], p[lo] / 2, color=GREEN, lw=1.8, ls=(0, (5, 3)), zorder=3)
    hi = p > 0.05
    ax.loglog(p[hi], np.sqrt(p[hi] / 2), color=GREEN, lw=1.8, ls=(0, (5, 3)), zorder=3)
    ax.axvline(1, color="#c7d2e0", lw=1.0)
    ax.text(2e-4, 1.7, "β", fontsize=17, color=NAVY)
    ax.text(0.12, 0.011, "α", fontsize=17, color=AMBER)
    ax.text(2e-4, 60, "low loss", fontsize=14, color=GRAY)
    ax.text(15, 3e-3, "good conductor", fontsize=14, color=GRAY)
    ax.text(1.2e-3, 1.3e-4, "low-loss limit", fontsize=13, color=GREEN, rotation=37)
    ax.text(150, 0.8, "good-conductor limit", fontsize=13, color=GREEN, rotation=21)
    for name, pm, off in MATERIALS:
        am = (1j * np.sqrt(1 - 1j * pm)).real
        ax.plot(pm, am, "o", color=INK, ms=7, zorder=4)
        ax.annotate(name, (pm, am), xytext=off, textcoords="offset points",
                    fontsize=13, color=INK)
    ax.annotate("copper, 100 MHz →", (1e5, 1.5e-4), xytext=(-138, 0),
                textcoords="offset points", fontsize=13, color=INK, va="center")
    ax.set_xlim(1e-4, 1e5); ax.set_ylim(2e-5, 600)
    ax.set_xticks([1e-4, 1e-2, 1, 1e2, 1e4])
    ax.set_yticks([1e-4, 1e-2, 1, 1e2])
    ax.set_xlabel("σ/(ωε)", color=GRAY, fontsize=14)
    ax.set_ylabel("divided by ω√(με)", color=GRAY, fontsize=14)
    ax.grid(True, which="major", color="#e3edf6", lw=1.0)
    style(ax)
    save(fig, "L36-regimes.svg")


if __name__ == "__main__":
    decaying_wave()
    regimes()
