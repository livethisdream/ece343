#!/usr/bin/env python3
"""L14 figures: the step transient on a lossless line.

The worked example throughout L14: a 10 V step source with Rs = 25 ohm, a
50 ohm line 400 m long with v_p = 2e8 m/s (so the one-way delay T = 2 us),
and a 150 ohm load. Then V1+ = 6.67 V, Gamma_L = 0.5, Gamma_s = -1/3, and the
voltage settles to the DC divider value 10 x 150/175 = 8.57 V.

    L14-bounce.svg        the bounce diagram: position across, time down, each
                          wave labeled with its amplitude
    L14-load-voltage.svg  the voltage at the load and at the source against
                          time, settling to the DC value

Labels are plain Unicode (see CLAUDE.md).

    python3 scripts/graphics/l14_figures.py   ->   book/extras/viz/img/L14-*.svg
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

NAVY, BLUE, AMBER, RED, GREEN, GRAY, INK = "#004a85", "#0067b9", "#8a5a00", "#b3213a", "#1d7a4d", "#5b6573", "#15202b"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"
plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})

VS, RS, Z0, RL = 10.0, 25.0, 50.0, 150.0
V1 = VS * Z0 / (RS + Z0)
GL = (RL - Z0) / (RL + Z0)
GS = (RS - Z0) / (RS + Z0)
VSS = VS * RL / (RL + RS)


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def waves(n):
    """Amplitudes of the first n waves: forward, reflected, re-reflected, ..."""
    a = [V1]
    for k in range(1, n):
        a.append(a[-1] * (GL if k % 2 else GS))
    return a


def fmt(v):
    return f"{v:+.2f} V".replace("+", "+").replace("-", "−")


def bounce():
    n = 5
    a = waves(n)
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    # x: 0 = source (z = -l), 1 = load (z = 0); y: time in units of T, increasing downward
    for k in range(n):
        x0, x1 = (0, 1) if k % 2 == 0 else (1, 0)
        ax.annotate("", xy=(x1, k + 1), xytext=(x0, k),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY if k % 2 == 0 else RED, lw=2.0,
                                    mutation_scale=14, shrinkA=0, shrinkB=0))
        ax.text(0.5 + (0.04 if k % 2 == 0 else -0.04), k + 0.5, fmt(a[k]),
                ha="left" if k % 2 == 0 else "right", va="bottom",
                color=NAVY if k % 2 == 0 else RED, fontsize=13, fontweight="bold")
    for x in (0, 1):
        ax.plot([x, x], [0, n + 0.2], color=INK, lw=1.6)
    for k in range(1, n + 1):
        ax.plot([-0.03, 1.03], [k, k], color="#e3edf6", lw=1.0, zorder=0)
        ax.text(1.06, k, f"{k}T", ha="left", va="center", color=GRAY, fontsize=12)
    ax.text(0, -0.25, "source, z = −ℓ", ha="center", va="bottom", fontsize=12, color=INK)
    ax.text(1, -0.25, "load, z = 0", ha="center", va="bottom", fontsize=12, color=INK)
    ax.text(0, -0.62, f"Γs = {GS:.2f}".replace("-", "−"), ha="center", va="bottom", color=GRAY, fontsize=12)
    ax.text(1, -0.62, f"ΓL = {GL:.2f}", ha="center", va="bottom", color=GRAY, fontsize=12)
    ax.annotate("", xy=(-0.12, n), xytext=(-0.12, 0.2),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
    ax.text(-0.15, 0.2, "t", ha="right", va="top", color=GRAY, fontsize=13, fontstyle="italic")
    ax.set_xlim(-0.3, 1.3); ax.set_ylim(n + 0.35, -0.9)
    ax.axis("off")
    save(fig, "L14-bounce.svg")


def load_voltage():
    n = 14
    a = waves(n)
    tmax = 12
    t = np.linspace(0, tmax, 2401)
    vl = np.zeros_like(t)
    vs = np.zeros_like(t)
    for k in range(n):
        # wave k reaches the load at time k+1 if it travels toward the load (k even),
        # and leaves the load at time k if it travels away from it (k odd)
        t_load = k + 1 if k % 2 == 0 else k
        t_src = k if k % 2 == 0 else k + 1
        vl += a[k] * (t >= t_load)
        vs += a[k] * (t >= t_src)
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.axhline(VSS, color=GRAY, lw=1.2, ls="--")
    ax.text(tmax, VSS + 0.25, f"DC value {VSS:.2f} V", ha="right", va="bottom", color=GRAY, fontsize=12)
    ax.step(t, vs, where="post", color=AMBER, lw=1.8, label="at the source, z = −ℓ")
    ax.step(t, vl, where="post", color=NAVY, lw=2.6, label="at the load, z = 0")
    ax.set_xlim(0, tmax); ax.set_ylim(0, 11)
    ax.set_xticks(range(0, tmax + 1))
    ax.set_xticklabels(["0"] + [f"{k}T" for k in range(1, tmax + 1)])
    ax.set_ylabel("voltage (V)", color=GRAY, fontsize=12)
    ax.set_xlabel("time", color=GRAY, fontsize=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=11)
    ax.legend(frameon=False, fontsize=12, loc="lower right")
    save(fig, "L14-load-voltage.svg")


if __name__ == "__main__":
    bounce()
    load_voltage()
