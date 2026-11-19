#!/usr/bin/env python3
"""L41 figures: the Incidence Lab's grids, setup, and results.

    L41-yee.svg            the 1D Yee grid: E_x at whole cells and steps, H_y
                           halfway between, with the stencils of both updates
    L41-yee2d.svg          one TE cell of the 2D grid: E_y at the nodes, H_x
                           halfway along z, H_z halfway along x
    L41-line.svg           Part A's 1D run: source, probe, boundary, the
                           transmitted probe, and the optional layer
    L41-setup.svg          Part B's 2D run (and L41-setup-phone.svg, stacked
                           larger for a phone)
    L41-separation.svg     a real 45° TE run: full field, reference field, and
                           their difference, the reflected beam alone (and a
                           phone variant)
    L41-beam-brewster.svg  |Γ_TM| near the Brewster angle: one plane wave, the
                           average over the beam's spread of angles, and the
                           notebook's FDTD points
    L41-dispersion.svg     the grid's phase velocity against cells per
                           wavelength, with the notebook's operating points
    L41-mur.svg            the Mur boundary's stencil
    L41-arcoat.svg         |Γ(f)| of the quarter-wave layer (Lesson 7's line
                           theory)

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.
L41-separation.svg runs the notebook's solver (l41_fdtd.py), about 30 s.

    python3 scripts/graphics/l41_figures.py   ->   book/extras/viz/img/L41-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402
from l24_figures import lab, arrow  # noqa: E402

NAVY, AMBER, GREEN, GRAY, INK, RED = "#004a85", "#8a5a00", "#1d7a4d", "#5b6573", "#15202b", "#b3213a"
FILL = "#e3edf6"       # medium 2
PML = "#eef0f3"        # the absorbing layer
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 15, "text.color": INK})


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
    ax.grid(True, color="#e3edf6", lw=1.0)


# --------------------------------------------------------------------------
def yee():
    """Space runs to the right in cells, time runs up in half steps."""
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ks = np.arange(0, 5)
    rows = ((-0.5, "H"), (0.0, "E"), (0.5, "H"), (1.0, "E"))
    for t, kind in rows:
        ax.plot([-0.4, 4.4], [t, t], color=GRAY, lw=0.8, ls=":")
        if kind == "E":
            ax.plot(ks, np.full_like(ks, t, dtype=float), "o", color=NAVY, ms=12)
        else:
            ax.plot(ks[:-1] + 0.5, np.full(4, t), "s", color=AMBER, ms=11)
    # the E update at node k = 2: E at n+1 from E at n and H at n+1/2 on each side
    arrow(ax, 2.0, 0.08, 2.0, 0.9, color=NAVY, lw=1.8, head=13)
    arrow(ax, 1.5, 0.56, 1.93, 0.93, color=NAVY, lw=1.8, head=13)
    arrow(ax, 2.5, 0.56, 2.07, 0.93, color=NAVY, lw=1.8, head=13)
    # the H update at node 3 + 1/2: H at n+1/2 from H at n-1/2 and E at n on each side
    arrow(ax, 3.5, -0.42, 3.5, 0.4, color=AMBER, lw=1.8, head=13)
    arrow(ax, 3.0, 0.06, 3.43, 0.43, color=AMBER, lw=1.8, head=13)
    arrow(ax, 4.0, 0.06, 3.57, 0.43, color=AMBER, lw=1.8, head=13)
    for t, txt in ((-0.5, "n − ½"), (0.0, "n"), (0.5, "n + ½"), (1.0, "n + 1")):
        lab(ax, -0.6, t, txt, size=17, ha="right")
    lab(ax, 2.0, -0.78, "k", size=17, color=NAVY)
    lab(ax, 3.5, -0.78, "k + ½", size=17, color=AMBER)
    arrow(ax, -1.75, -0.55, -1.75, 1.05, color=GRAY, lw=1.2, head=11)
    ax.text(-1.95, 0.25, "t", ha="right", va="center", fontsize=18, fontstyle="italic", color=GRAY)
    arrow(ax, 0.0, -1.0, 4.3, -1.0, color=GRAY, lw=1.2, head=11)
    ax.text(4.45, -1.0, "z", ha="left", va="center", fontsize=18, fontstyle="italic", color=GRAY)
    ax.plot([4.85], [0.75], "o", color=NAVY, ms=12)
    lab(ax, 5.05, 0.75, "E", "x", size=18, ha="left", color=NAVY)
    ax.plot([4.85], [0.25], "s", color=AMBER, ms=11)
    lab(ax, 5.05, 0.25, "H", "y", size=18, ha="left", color=AMBER)
    ax.set_xlim(-2.4, 5.9); ax.set_ylim(-1.15, 1.15)
    ax.axis("off")
    save(fig, "L41-yee.svg")


def yee2d():
    """One TE cell: x to the right, z down (as in the notebook's maps)."""
    fig, ax = plt.subplots(figsize=(5.4, 4.4))
    for i in range(3):
        ax.plot([i, i], [-0.3, 2.3], color="#d5dee8", lw=1.0)
        ax.plot([-0.3, 2.3], [i, i], color="#d5dee8", lw=1.0)
    ax.add_patch(Rectangle((0.5, 0.5), 1, 1, facecolor="none", edgecolor=GRAY, lw=1.0, ls="--"))
    for i in range(3):
        for k in range(3):
            ax.plot(i, k, "o", color=NAVY, ms=13)
    for i in range(3):
        for k in range(2):
            ax.plot(i, k + 0.5, "s", color=AMBER, ms=11)
    for i in range(2):
        for k in range(3):
            ax.plot(i + 0.5, k, "^", color=GREEN, ms=12)
    ax.annotate("", (2, 2.45), (1, 2.45), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
    ax.text(1.5, 2.6, "Δ", ha="center", va="top", fontsize=18, color=GRAY)
    lab(ax, 1, -0.55, "i", size=17, color=GRAY)
    lab(ax, -0.55, 1, "k", size=17, color=GRAY)
    arrow(ax, -0.6, -0.95, 2.4, -0.95, color=GRAY, lw=1.2, head=11)
    ax.text(2.5, -0.95, "x", ha="left", va="center", fontsize=18, fontstyle="italic", color=GRAY)
    arrow(ax, -0.95, -0.6, -0.95, 2.4, color=GRAY, lw=1.2, head=11)
    ax.text(-0.95, 2.55, "z", ha="center", va="top", fontsize=18, fontstyle="italic", color=GRAY)
    ax.plot([2.95], [0.1], "o", color=NAVY, ms=13)
    lab(ax, 3.15, 0.1, "E", "y", size=18, ha="left", color=NAVY)
    ax.plot([2.95], [0.75], "s", color=AMBER, ms=11)
    lab(ax, 3.15, 0.75, "H", "x", size=18, ha="left", color=AMBER)
    ax.plot([2.95], [1.4], "^", color=GREEN, ms=12)
    lab(ax, 3.15, 1.4, "H", "z", size=18, ha="left", color=GREEN)
    ax.set_xlim(-1.2, 4.2); ax.set_ylim(2.75, -1.2)
    ax.set_aspect("equal"); ax.axis("off")
    save(fig, "L41-yee2d.svg")


def line1d():
    """Part A's grid, a schematic: positions in order, not to scale."""
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    L, xs, xp, xb, xt, wl = 1100, 80, 250, 580, 800, 70
    y0, h = 0.0, 1.0
    ax.add_patch(Rectangle((0, y0), L, h, facecolor="white", edgecolor=GRAY, lw=1.0))
    ax.add_patch(Rectangle((xb, y0), L - xb, h, facecolor=FILL, edgecolor="none"))
    ax.add_patch(Rectangle((xb - wl, y0), wl, h, facecolor="#f6ead3", edgecolor=AMBER, lw=0.8, ls="--"))
    ax.plot([xb, xb], [y0 - 0.1, y0 + h + 0.1], color=INK, lw=1.6)
    for x, txt, col in ((xs, "source", GREEN), (xp, "probe", NAVY), (xt, "probe", NAVY)):
        ax.plot([x, x], [y0, y0 + h], color=col, lw=2.4)
        ax.text(x, y0 - 0.18, txt, ha="center", va="top", fontsize=15, color=col)
    ax.text(xb - wl / 2, y0 - 0.18, "layer (A3)", ha="center", va="top", fontsize=15, color=AMBER)
    ax.text(xb, y0 + h + 0.15, "boundary", ha="center", va="bottom", fontsize=15)
    ax.text(410, y0 + h / 2, "air", ha="center", va="center", fontsize=16)
    lab(ax, 940, y0 + h / 2, "ε", "r", size=17)
    ax.text(975, y0 + h / 2, " = 4", ha="left", va="center", fontsize=16)
    ax.text(-15, y0 + h / 2, "Mur", ha="right", va="center", fontsize=14, color=GRAY)
    ax.text(L + 15, y0 + h / 2, "Mur", ha="left", va="center", fontsize=14, color=GRAY)
    arrow(ax, xs + 20, 2.25, xb - 40, 2.25, color=NAVY, lw=2.0, head=14)
    ax.text((xs + xb) / 2, 2.4, "incident", ha="center", va="bottom", fontsize=15, color=NAVY)
    arrow(ax, xb - 20, 1.75, xp + 30, 1.75, color=RED, lw=1.8, ls="--", head=13)
    ax.text(xp + 10, 1.75, "reflected ", ha="right", va="center", fontsize=15, color=RED)
    arrow(ax, xb + 20, 2.25, L - 60, 2.25, color=NAVY, lw=2.0, head=14)
    ax.text((xb + L) / 2, 2.4, "transmitted", ha="center", va="bottom", fontsize=15, color=NAVY)
    ax.set_xlim(-130, L + 130); ax.set_ylim(-0.7, 2.85)
    ax.axis("off")
    save(fig, "L41-line.svg")


def _setup(ax, fs, sub, W=24.0):
    """A schematic, not to scale: the vertical spacing is stretched for room."""
    H, P = 12.0, 1.0
    yb = 6.0
    zs, zm, zt = 9.6, 7.6, 4.4
    ax.add_patch(Rectangle((0, 0), W, H, facecolor=PML, edgecolor=GRAY, lw=1.0))
    ax.add_patch(Rectangle((P, P), W - 2 * P, H - 2 * P, facecolor="white", edgecolor=GRAY, lw=0.8))
    ax.add_patch(Rectangle((P, P), W - 2 * P, yb - P, facecolor=FILL, edgecolor="none"))
    ax.plot([P, W - P], [yb, yb], color=INK, lw=1.6)
    ax.plot([P, W - P], [zs, zs], color=GREEN, lw=2.0)
    ax.plot([P, W - P], [zm, zm], color=AMBER, lw=1.4, ls="--")
    ax.plot([P, W - P], [zt, zt], color=AMBER, lw=1.4, ls="--")
    xh = W / 2
    th, tt = np.radians(45), np.radians(28.3)
    xs = xh - (zs - yb) * np.tan(th)
    # the beam's Gaussian taper, sketched on the source line
    gx = np.linspace(xs - 3.2, xs + 3.2, 80)
    ax.fill_between(gx, zs, zs + 0.9 * np.exp(-((gx - xs) / 1.4) ** 2), color=GREEN, alpha=0.25, lw=0)
    # incident beam as a tapered band
    half = 1.0
    nrm = np.array([np.cos(th), np.sin(th)])
    p0, p1 = np.array([xs, zs]), np.array([xh, yb])
    ax.add_patch(Polygon([p0 + half * nrm, p1 + half * nrm * 0.8, p1 - half * nrm * 0.8, p0 - half * nrm],
                         closed=True, facecolor=NAVY, alpha=0.12, lw=0))
    arrow(ax, xs, zs, xh, yb, color=NAVY, lw=2.6, head=16)
    arrow(ax, xh, yb, xh + 3.3 * np.sin(th), yb + 3.3 * np.cos(th), color=RED, lw=1.8, ls="--", head=14)
    arrow(ax, xh, yb, xh + 4.6 * np.sin(tt), yb - 4.6 * np.cos(tt), color=NAVY, lw=2.0, head=15)
    # the upward beam the source also launches, absorbed at the top
    arrow(ax, xs - 0.4, zs + 0.15, xs - 1.6, H - P + 0.4, color=GRAY, lw=1.2, ls=":", head=11)
    ax.plot([xh, xh], [yb - 3.6, yb + 3.6], color=GRAY, lw=0.8, ls=":")
    ax.add_patch(Arc((xh, yb), 3.0, 3.0, theta1=90, theta2=135, color=NAVY, lw=1.2))
    ax.add_patch(Arc((xh, yb), 3.6, 3.6, theta1=270, theta2=270 + 28.3, color=NAVY, lw=1.2))
    lab(ax, xh - 0.85, yb + 2.15, "θ", "i", size=sub)
    lab(ax, xh + 0.55, yb - 2.55, "θ", "t", size=sub)
    if W >= 20:
        ax.text(xs - 0.4, zs - 1.0, "incident", ha="right", va="center", fontsize=fs, color=NAVY)
    else:
        ax.text(P + 0.3, zs - 1.0, "incident", ha="left", va="center", fontsize=fs, color=NAVY)
    ax.text(xh + 2.8, yb + 3.05, "reflected", ha="left", va="center", fontsize=fs, color=RED)
    ax.text(xh + 2.4, yb - 3.6, "transmitted", ha="left", va="center", fontsize=fs, color=NAVY)
    ax.text(P + 0.3, yb + 0.3, "medium 1", ha="left", va="bottom", fontsize=fs)
    ax.text(P + 0.3, yb - 0.3, "medium 2", ha="left", va="top", fontsize=fs)
    ax.text(P + 0.3, zs + 0.25, "source line", ha="left", va="bottom", fontsize=fs, color=GREEN)
    if W >= 20:
        ax.text(W - P - 0.3, zm - 0.25, "power measured", ha="right", va="top", fontsize=fs, color=AMBER)
        ax.text(W - P - 0.3, zt - 0.25, "power measured", ha="right", va="top", fontsize=fs, color=AMBER)
    else:
        ax.text(W - P - 0.3, zm - 0.25, "power", ha="right", va="top", fontsize=fs, color=AMBER)
        ax.text(P + 0.3, zt - 0.25, "power", ha="left", va="top", fontsize=fs, color=AMBER)
    ax.text(W / 2 + W / 6, H - 0.5, "absorbing layer (PML)", ha="center", va="center", fontsize=fs - 1, color=GRAY)
    ax.set_xlim(-0.2, W + 0.2); ax.set_ylim(-0.2, H + 0.2)
    ax.set_aspect("equal"); ax.axis("off")


def setup():
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    _setup(ax, 15, 17)
    save(fig, "L41-setup.svg")
    fig, ax = plt.subplots(figsize=(5.0, 3.9))
    _setup(ax, 16, 18, W=16.0)
    save(fig, "L41-setup-phone.svg")


def separation():
    import l41_fdtd as fd
    Ft = fd.simulate("TE", 1.0, 1.49, 45.0)
    Fr = fd.simulate("TE", 1.0, 1.0, 45.0)
    lim = np.abs(Ft).max()
    # crop to the region the panels show, so the embedded image stays small
    xs = (fd.X / fd.LAM0 > -5.2) & (fd.X / fd.LAM0 < 7.2)
    zs = (fd.Z / fd.LAM0 > -2.8) & (fd.Z / fd.LAM0 < 3.4)
    Xc, Zc = fd.X[xs] / fd.LAM0, fd.Z[zs] / fd.LAM0
    Ft, Fr = Ft[np.ix_(xs, zs)], Fr[np.ix_(xs, zs)]
    ext = [Xc[0], Xc[-1], Zc[-1], Zc[0]]
    Fd = Ft - Fr
    Fd[:, Zc > 0] = 0.0          # below the boundary the difference has no meaning
    k = int(round(lim / np.abs(Fd).max()))          # the reflected beam is weaker: own scale
    titles = ("full run", "reference run", f"full − reference (×{k})")
    fields = (Ft, Fr, Fd)
    lims = (lim, lim, lim / k)

    def panel(ax, F, title, L):
        ax.imshow(np.real(F).T, extent=ext, cmap="RdBu_r", vmin=-L, vmax=L, aspect="equal",
                  interpolation="none")
        ax.axhline(0, color=INK, lw=1.2)
        ax.axhline(fd.Z[fd.ZM] / fd.LAM0, color=AMBER, lw=1.4, ls="--")
        ax.axhline(fd.Z[fd.ZT] / fd.LAM0, color=AMBER, lw=1.4, ls="--")
        ax.set_xlim(-5, 7); ax.set_ylim(3.2, -2.6)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#c7d2e0")
        ax.set_title(title, fontsize=16, color=INK)

    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.0))
    for ax, F, t, L in zip(axs, fields, titles, lims):
        panel(ax, F, t, L)
    fig.subplots_adjust(wspace=0.08)
    save(fig, "L41-separation.svg")
    fig, axs = plt.subplots(3, 1, figsize=(4.6, 7.0))
    for ax, F, t, L in zip(axs, fields, titles, lims):
        panel(ax, F, t, L)
        ax.set_xlim(-4, 6); ax.set_ylim(2.4, -2.2)
    fig.subplots_adjust(hspace=0.3)
    save(fig, "L41-separation-phone.svg")


def _fresnel_tm(n1, n2, th_deg):
    th = np.radians(th_deg)
    ct = np.sqrt(1 - (n1 * np.sin(th) / n2) ** 2 + 0j)
    ci = np.cos(th)
    e1, e2 = 1 / n1, 1 / n2
    return (e2 * ct - e1 * ci) / (e2 * ct + e1 * ci)


def beam_brewster():
    tt = np.linspace(30, 75, 600)
    plane = np.abs(_fresnel_tm(1.0, 1.49, tt))
    sp = 1 / (np.pi * 2.5)                         # spread in air, rad (1/e field half-width 2.5 λ0)
    d = np.linspace(-4 * sp, 4 * sp, 801)
    wgt = np.exp(-2 * (d / sp) ** 2)               # power in each angle of the beam
    beam = np.array([np.sqrt((np.abs(_fresnel_tm(1.0, 1.49, t + np.degrees(d))) ** 2 * wgt).sum()
                             / wgt.sum()) for t in tt])
    # the notebook key's FDTD points (B2), after the boundary-node fix
    fa = np.array([30.0, 45.0, 56.1, 65.0])
    fm = np.array([0.1609, 0.0945, 0.0429, 0.1454])
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(tt, plane, color=NAVY, lw=2.2, label="one plane wave")
    ax.plot(tt, beam, color=AMBER, lw=2.2, ls="--", label="beam 2.5 λ₀ wide")
    ax.plot(fa, fm, "s", color=RED, ms=8, label="FDTD")
    tb = np.degrees(np.arctan(1.49))
    ax.axvline(tb, color=GRAY, lw=1.0, ls=":")
    ax.text(tb + 0.6, 0.27, "Brewster 56.1°", fontsize=14, color=GRAY, va="top")
    ax.set_xlim(30, 75); ax.set_ylim(0, 0.28)
    ax.set_xlabel("angle of incidence (degrees)", fontsize=15, color=GRAY)
    ax.set_ylabel("|Γ| for TM", fontsize=15, color=GRAY)
    style(ax)
    ax.legend(frameon=False, fontsize=14, loc="upper left")
    save(fig, "L41-beam-brewster.svg")


def dispersion():
    N = np.logspace(np.log10(6), np.log10(100), 300)

    def ratio(S, N, diag=False):
        a = np.sin(np.pi * S / N) / (S * (np.sqrt(2) if diag else 1))
        bd = 2 * (np.sqrt(2) if diag else 1) * np.arcsin(np.clip(a, -1, 1))
        return (2 * np.pi / N) / bd

    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.plot(N, np.ones_like(N), color=GREEN, lw=2.2, label="1D, S = 1")
    ax.plot(N, ratio(0.5, N), color=NAVY, lw=2.2, label="1D, S = ½")
    ax.plot(N, ratio(0.5 / 1.49, N), color=AMBER, lw=2.2, label="2D along an axis, S = 0.336")
    ax.plot(N, ratio(0.5 / 1.49, N, diag=True), color=AMBER, lw=2.0, ls="--", label="2D diagonal, S = 0.336")
    ax.plot([40], [ratio(0.5, np.array([40.0]))[0]], "o", color=NAVY, ms=9,
            label="Part A dielectric, 40 cells")
    nb = 24 / 1.49
    ax.plot([nb], [ratio(0.5 / 1.49, np.array([nb]))[0]], "s", color=AMBER, ms=9,
            label="Part B acrylic, 16 cells")
    ax.set_xscale("log"); ax.set_xlim(6, 100); ax.set_ylim(0.95, 1.005)
    ax.set_xticks([6, 10, 20, 40, 80]); ax.set_xticklabels(["6", "10", "20", "40", "80"])
    ax.set_xlabel("cells per wavelength in the medium", fontsize=15, color=GRAY)
    ax.set_ylabel("grid phase velocity / v", fontsize=15, color=GRAY)
    style(ax)
    ax.legend(frameon=False, fontsize=12.5, loc="lower right")
    save(fig, "L41-dispersion.svg")


def mur():
    fig, ax = plt.subplots(figsize=(4.8, 3.4))
    for t in (0, 1):
        ax.plot([-0.3, 1.6], [t, t], color=GRAY, lw=0.8, ls=":")
        for k in (0, 1):
            ax.plot(k, t, "o", color=NAVY, ms=13)
    ax.plot(0.5, 0.5, "x", color=RED, ms=14, mew=2.5)
    for k in (0, 1):
        for t in (0, 1):
            ax.plot([k, 0.5], [t, 0.5], color=RED, lw=0.9, ls="--")
    lab(ax, -0.45, 0, "n", size=17, ha="right")
    lab(ax, -0.45, 1, "n + 1", size=17, ha="right")
    lab(ax, 0, -0.35, "node 0 (end)", size=15, italic=False, color=GRAY)
    lab(ax, 1, -0.35, "node 1", size=15, italic=False, color=GRAY)
    ax.text(0.62, 0.5, "averaged here", fontsize=14, color=RED, va="center")
    ax.set_xlim(-1.2, 1.9); ax.set_ylim(-0.6, 1.25)
    ax.axis("off")
    save(fig, "L41-mur.svg")


def arcoat():
    f = np.linspace(0.3, 2.2, 600) * 1e9
    c0 = 299_792_458.0
    eta1, eta2 = 1.0, 0.5
    nc = np.sqrt(2.0)
    etac = 1 / nc
    d = c0 / 1e9 / (4 * nc)
    bcd = 2 * np.pi * f * nc / c0 * d
    ein = etac * (eta2 + 1j * etac * np.tan(bcd)) / (etac + 1j * eta2 * np.tan(bcd))
    g = np.abs((ein - eta1) / (ein + eta1))
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(f / 1e9, g, color=NAVY, lw=2.4, label="λ/4 layer")
    ax.axhline(1 / 3, color=GRAY, lw=1.2, ls=":", label="no layer")
    band = f[g < 0.1] / 1e9
    ax.axvspan(band.min(), band.max(), color=GREEN, alpha=0.12, lw=0)
    ax.text((band.min() + band.max()) / 2, 0.37, "|Γ| < 0.1", ha="center", fontsize=14, color=GREEN)
    ax.set_xlim(0.3, 2.2); ax.set_ylim(0, 0.42)
    ax.set_xlabel("frequency (GHz)", fontsize=15, color=GRAY)
    ax.set_ylabel("|Γ|", fontsize=15, color=GRAY)
    style(ax)
    ax.legend(frameon=False, fontsize=13, loc="lower right")
    save(fig, "L41-arcoat.svg")


if __name__ == "__main__":
    yee()
    yee2d()
    line1d()
    setup()
    beam_brewster()
    dispersion()
    mur()
    arcoat()
    if "--fast" not in sys.argv:
        separation()
