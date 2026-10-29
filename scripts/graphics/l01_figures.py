#!/usr/bin/env python3
"""L01 figures: where electromagnetics shows up on the spectrum.

    L01-spectrum.svg   frequency on a log axis, wavelength on the axis above
                       it, and a handful of systems a cadet will meet, from a
                       60 Hz power line to visible light

Wavelengths are free-space, lambda = c/f with c = 3e8 m/s. Labels are plain
Unicode (see CLAUDE.md).

    python3 scripts/graphics/l01_figures.py   ->   book/extras/viz/img/L01-*.svg
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

NAVY, BLUE, AMBER, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#5b6573", "#15202b"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"
plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})
C = 3e8

# (frequency in Hz, label, label height) -- positive above the axis, negative
# below; X-band sits on a higher tier so it clears FM radio
SYSTEMS = [
    (60, "power grid\n60 Hz", 0.75),
    (1e6, "AM radio\n1 MHz", -0.75),
    (1e8, "FM radio\n100 MHz", 0.75),
    (1.57542e9, "GPS L1\n1.575 GHz", -0.75),
    (1e10, "X-band radar\n10 GHz", 1.75),
    (5e14, "visible light\n500 THz", -0.75),
]


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def fmt_len(m):
    if m >= 1e3:
        return f"{m/1e3:g} km"
    if m >= 1:
        return f"{m:g} m"
    if m >= 1e-2:
        return f"{m*100:.3g} cm"
    if m >= 1e-6:
        return f"{m*1e6:g} µm"
    return f"{m*1e9:g} nm"


def spectrum():
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.set_xscale("log")
    ax.set_xlim(10, 1e16)
    ax.set_ylim(-1.6, 2.6)
    ax.axhline(0, color=NAVY, lw=2.4)
    ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c7d2e0")
    ax.set_xticks([1e2, 1e4, 1e6, 1e8, 1e10, 1e12, 1e14, 1e16])
    ax.set_xticklabels(["100 Hz", "10 kHz", "1 MHz", "100 MHz", "10 GHz", "1 THz", "100 THz", "10 PHz"])
    ax.tick_params(colors=GRAY, labelsize=10.5)
    ax.set_xlabel("frequency", color=GRAY, fontsize=12)

    top = ax.secondary_xaxis("top", functions=(lambda f: C / np.maximum(f, 1e-30), lambda lam: C / np.maximum(lam, 1e-30)))
    top.set_xticks([1e6, 1e4, 1e2, 1, 1e-2, 1e-4, 1e-6, 1e-8])
    top.set_xticklabels(["1000 km", "10 km", "100 m", "1 m", "1 cm", "100 µm", "1 µm", "10 nm"])
    top.tick_params(colors=GRAY, labelsize=10.5)
    top.set_xlabel("wavelength", color=GRAY, fontsize=12)
    top.spines["top"].set_color("#c7d2e0")

    for f, label, y in SYSTEMS:
        ax.plot([f, f], [0, y - 0.12 * np.sign(y)], color=AMBER, lw=1.2)
        ax.plot(f, 0, "o", color=AMBER, ms=6, zorder=3)
        name, freq = label.split("\n")
        ax.text(f, y, f"{name}\n{freq}, λ = {fmt_len(C / f)}", ha="center",
                va="bottom" if y > 0 else "top", fontsize=10.5, color=INK, linespacing=1.25)
    save(fig, "L01-spectrum.svg")


if __name__ == "__main__":
    spectrum()
