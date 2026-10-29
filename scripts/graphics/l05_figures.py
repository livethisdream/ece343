#!/usr/bin/env python3
"""L05 figures: attenuation of RG-58 against frequency.

    L05-attenuation.svg   conductor loss, dielectric loss, and their sum, in
                          dB per 100 m, from the low-loss formula
                          alpha = R'/(2 Z0) + G' Z0 / 2

RG-58 as the course models it (project/ROADMAP.md): copper conductors,
a = 0.405 mm, b = 1.475 mm, polyethylene with eps_r = 2.25 and a loss tangent
of 2e-4. R' comes from the skin-effect formula on the equation sheet, and
G' = omega C' tan(delta). Labels are plain Unicode (see CLAUDE.md).

    python3 scripts/graphics/l05_figures.py   ->   book/extras/viz/img/L05-*.svg
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

A, B, ER, SIGMA, TAN_D = 0.405e-3, 1.475e-3, 2.25, 5.8e7, 2e-4
MU0, EPS0 = 4e-7 * np.pi, 8.854e-12
LN = np.log(B / A)
L_P = MU0 / (2 * np.pi) * LN
C_P = 2 * np.pi * ER * EPS0 / LN
Z0 = np.sqrt(L_P / C_P)
NP_TO_DB_PER_100M = 100 * 20 / np.log(10)          # 8.686 dB/Np, times 100 m


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def alphas(f):
    """Conductor and dielectric attenuation in dB per 100 m at frequency f."""
    w = 2 * np.pi * f
    rs = np.sqrt(np.pi * f * MU0 / SIGMA)
    r_p = (1 / A + 1 / B) * rs / (2 * np.pi)
    g_p = w * C_P * TAN_D
    return r_p / (2 * Z0) * NP_TO_DB_PER_100M, g_p * Z0 / 2 * NP_TO_DB_PER_100M


def attenuation():
    f = np.logspace(6, 10, 400)
    a_c, a_d = alphas(f)

    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    ax.loglog(f, a_c + a_d, color=NAVY, lw=2.8, label="total")
    ax.loglog(f, a_c, color=AMBER, lw=1.6, ls="--", label="conductors, R′")
    ax.loglog(f, a_d, color=GREEN, lw=1.6, ls="--", label="dielectric, G′")
    for fm in (1e8, 1e9):
        tot = sum(alphas(fm))
        ax.plot(fm, tot, "o", color=NAVY, ms=6, zorder=3)
        ax.annotate(f"{tot:.1f}", (fm, tot), xytext=(-8, 8),
                    textcoords="offset points", ha="right", fontsize=12, color=NAVY)
    ax.set_xlim(1e6, 1e10); ax.set_ylim(1e-3, 300)
    ax.set_xticks([1e6, 1e7, 1e8, 1e9, 1e10])
    ax.set_xticklabels(["1 MHz", "10 MHz", "100 MHz", "1 GHz", "10 GHz"])
    ax.set_ylabel("attenuation (dB per 100 m)", color=GRAY, fontsize=12)
    ax.grid(True, which="major", color="#e3edf6", lw=1.0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c7d2e0")
    ax.tick_params(colors=GRAY, labelsize=11)
    ax.legend(frameon=False, fontsize=12, loc="upper left")
    save(fig, "L05-attenuation.svg")


if __name__ == "__main__":
    attenuation()
