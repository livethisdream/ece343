#!/usr/bin/env python3
"""L36 figures: plane-wave solutions in lossless and lossy media.

    L36-decaying-wave.svg   a snapshot of E_x(z) for a wave traveling in +z in a
                            lossy medium, with its envelope ±E0 e^(−αz) and the
                            skin depth δ = 1/α marked
    L36-regimes.svg         α and β, normalized to ω√(με), against the ratio
                            σ/ωε, with the low-loss and good-conductor limits

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
    ax.tick_params(colors=GRAY, labelsize=11)


def decaying_wave():
    """E_x(z, 0) = E0 e^(−αz) cos(βz) for a wave traveling in +z in a lossy
    medium. Depth is in units of δ = 1/α; here β = 4π/δ, two wavelengths per
    skin depth, so the oscillation stays visible under the envelope."""
    z = np.linspace(0, 3, 1200)                  # z/δ
    env = np.exp(-z)
    fig, ax = plt.subplots(figsize=(8.0, 3.4))
    ax.plot(z, env * np.cos(4 * np.pi * z), color=NAVY, lw=2.4)
    ax.plot(z, env, color=AMBER, lw=1.4, ls="--")
    ax.plot(z, -env, color=AMBER, lw=1.4, ls="--")
    ax.axhline(0, color="#c7d2e0", lw=1.0)
    ax.plot([1, 1], [-1.05, np.exp(-1)], color=GRAY, lw=1.0, ls=":")
    ax.plot(1, np.exp(-1), "o", color=AMBER, ms=6)
    ax.text(1.05, np.exp(-1) + 0.1, "1/e", fontsize=13, color=AMBER)
    ax.text(1.75, 0.3, "E₀ e⁻ᵅᶻ", fontsize=14, color=AMBER)
    ax.set_xlim(0, 3); ax.set_ylim(-1.05, 1.08)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["0", "δ", "2δ", "3δ"])
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(["−E₀", "0", "E₀"])
    ax.set_xlabel("depth z", color=GRAY, fontsize=12)
    style(ax)
    save(fig, "L36-decaying-wave.svg")


def regimes():
    """α/ω√(με) and β/ω√(με) against p = σ/ωε, exactly, with the two limits."""
    p = np.logspace(-3, 3, 400)
    g = 1j * np.sqrt(1 - 1j * p)
    a, b = g.real, g.imag
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    ax.loglog(p, b, color=NAVY, lw=2.6, label="β")
    ax.loglog(p, a, color=AMBER, lw=2.6, label="α")
    lo = p < 0.3
    ax.loglog(p[lo], p[lo] / 2, color=AMBER, lw=1.2, ls=":")
    hi = p > 3
    ax.loglog(p[hi], np.sqrt(p[hi] / 2), color=GRAY, lw=1.2, ls=":")
    ax.axvline(1, color="#c7d2e0", lw=1.0)
    ax.text(0.0016, 1.6, "low loss", fontsize=13, color=GRAY)
    ax.text(40, 0.25, "good conductor", fontsize=13, color=GRAY)
    ax.text(0.05, 0.0011, "α ≈ (σ/2)√(μ/ε)", fontsize=12, color=AMBER)
    ax.text(2.2, 22, "α ≈ β ≈ √(πfμσ)", fontsize=12, color=GRAY)
    ax.set_xlim(1e-3, 1e3); ax.set_ylim(1e-4, 40)
    ax.set_xlabel("σ/ωε", color=GRAY, fontsize=12)
    ax.set_ylabel("divided by ω√(με)", color=GRAY, fontsize=12)
    ax.grid(True, which="major", color="#e3edf6", lw=1.0)
    ax.legend(frameon=False, fontsize=13, loc="lower right")
    style(ax)
    save(fig, "L36-regimes.svg")


if __name__ == "__main__":
    decaying_wave()
    regimes()
