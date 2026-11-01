#!/usr/bin/env python3
"""L17 figures: coordinate systems, differential elements, and the operators.

    L17-coordinates.svg    one point P located in Cartesian, cylindrical, and
                           spherical coordinates
    L17-unit-vectors.svg   rho-hat and phi-hat at two points: they turn with phi
    L17-elements.svg       the cylindrical and spherical volume elements, with
                           the length of each edge
    L17-gradient.svg       level curves of f = x^2 + y^2 and the gradient
    L17-flux-box.svg       a small box, with F_x entering one face and leaving
                           the opposite face
    L17-tiling.svg         neighbor cells: the shared face (divergence) and the
                           shared edge (Stokes) cancel
    L17-curl-loop.svg      a small loop in the xy plane and the field on each side
    L17-div-curl.svg       a field with divergence and a field with curl
    L17-stokes-example.svg the quarter-disk contour of the worked example

Labels are plain Unicode (see CLAUDE.md); the lesson text does the explaining.

    python3 scripts/graphics/l17_figures.py   ->   book/extras/viz/img/L17-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, AMBER, GREEN, GRAY, INK = (
    "#004a85", "#0067b9", "#8a5a00", "#1d7a4d", "#5b6573", "#15202b")
FILL = "#e3edf6"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})

# Oblique projection: x toward the viewer (down and left), y right, z up.
EX, EY, EZ = np.array([-0.55, -0.42]), np.array([1.0, 0.0]), np.array([0.0, 1.0])


def P(x, y, z):
    return x * EX + y * EY + z * EZ


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(apply_font_stack(buf.getvalue()), encoding="utf-8")
    print("wrote", OUT / name)


def arrow(ax, a, b, color=INK, lw=1.6, ms=14, style="-|>"):
    ax.add_patch(FancyArrowPatch(tuple(a), tuple(b), arrowstyle=style, color=color,
                                 lw=lw, mutation_scale=ms, shrinkA=0, shrinkB=0))


def txt(ax, p, s, color=INK, size=14, ha="center", va="center", italic=True):
    ax.text(p[0], p[1], s, color=color, fontsize=size, ha=ha, va=va,
            fontstyle="italic" if italic else "normal")


def axes3(ax, L=2.6):
    for v, name in ((P(L, 0, 0), "x"), (P(0, L, 0), "y"), (P(0, 0, L), "z")):
        arrow(ax, (0, 0), v, color=GRAY, lw=1.2, ms=11)
        off = v / np.linalg.norm(v) * 0.22
        txt(ax, v + off, name, color=GRAY)


def stxt(ax, p, base, sub, rest="", color=INK, size=14, ha="center"):
    """base_sub(rest) as three pieces: Unicode has no subscript y."""
    fig = ax.figure
    r = fig.canvas.get_renderer()
    parts = [(base, size, 0.0), (sub, size * 0.7, -size * 0.3), (rest, size, 0.0)]
    ws = []
    for s, fs, _ in parts:
        t = ax.text(0, 0, s, fontsize=fs, fontstyle="italic")
        ws.append(t.get_window_extent(renderer=r).width / fig.dpi * 72 if s else 0.0)
        t.remove()
    total = sum(ws)
    x0 = {"center": -total / 2, "left": 0.0, "right": -total}[ha]
    for (s, fs, dy), w in zip(parts, ws):
        if s:
            ax.annotate(s, p, xytext=(x0, dy), textcoords="offset points", fontsize=fs,
                        color=color, ha="left", va="center", fontstyle="italic")
        x0 += w


def hat(ax, p, letter, color=INK, size=15):
    """A unit-vector symbol: the letter with a caret set above it as its own
    text, because a combining circumflex lands off the glyph in most fonts."""
    ax.text(p[0], p[1], letter, color=color, fontsize=size, ha="center", va="center",
            fontstyle="italic", fontweight="bold")
    ax.annotate("ˆ", p, xytext=(0.5, size * 0.38), textcoords="offset points", color=color,
                fontsize=size, ha="center", va="center")


def curve(ax, pts, **kw):
    q = np.array([P(*p) for p in pts])
    ax.plot(q[:, 0], q[:, 1], **kw)


def blank(ax, xl, yl):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(*xl); ax.set_ylim(*yl)


# ---------------------------------------------------------------------------
def coordinates():
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.7))
    x0, y0, z0 = 1.2, 1.6, 1.5
    rho, phi = np.hypot(x0, y0), np.arctan2(y0, x0)
    r, th = np.sqrt(x0**2 + y0**2 + z0**2), np.arccos(z0 / np.sqrt(x0**2 + y0**2 + z0**2))
    titles = ["Cartesian (x, y, z)", "cylindrical (ρ, φ, z)", "spherical (r, θ, φ)"]
    for k, ax in enumerate(axs):
        blank(ax, (-1.8, 2.9), (-1.3, 2.9))
        axes3(ax)
        ax.set_title(titles[k], fontsize=13, color=NAVY)
        pt = P(x0, y0, z0)
        foot = P(x0, y0, 0)
        if k == 0:
            curve(ax, [(x0, 0, 0), (x0, y0, 0)], color=AMBER, lw=1.6)
            curve(ax, [(0, y0, 0), (x0, y0, 0)], color=AMBER, lw=1.6)
            curve(ax, [(x0, y0, 0), (x0, y0, z0)], color=AMBER, lw=1.6)
            txt(ax, P(x0 / 2, 0, 0) + (-0.15, -0.05), "x", color=AMBER, ha="right")
            txt(ax, P(x0, y0 / 2, 0) + (0, -0.2), "y", color=AMBER)
            txt(ax, P(x0, y0, z0 / 2) + (0.15, 0), "z", color=AMBER, ha="left")
        elif k == 1:
            curve(ax, [(0, 0, 0), (x0, y0, 0)], color=AMBER, lw=1.8)
            curve(ax, [(x0, y0, 0), (x0, y0, z0)], color=AMBER, lw=1.8)
            t = np.linspace(0, phi, 30)
            curve(ax, [(0.7 * np.cos(a), 0.7 * np.sin(a), 0) for a in t], color=AMBER, lw=1.2)
            txt(ax, P(x0 / 2, y0 / 2, 0) + (0.05, -0.22), "ρ", color=AMBER)
            txt(ax, P(0.75, 0.25, 0) + (-0.12, -0.18), "φ", color=AMBER)
            txt(ax, P(x0, y0, z0 / 2) + (0.15, 0), "z", color=AMBER, ha="left")
        else:
            curve(ax, [(0, 0, 0), (x0, y0, z0)], color=AMBER, lw=1.8)
            curve(ax, [(0, 0, 0), (x0, y0, 0)], color=GRAY, lw=1.0, ls="--")
            curve(ax, [(x0, y0, 0), (x0, y0, z0)], color=GRAY, lw=1.0, ls="--")
            t = np.linspace(0, th, 30)
            curve(ax, [(0.8 * np.sin(a) * np.cos(phi), 0.8 * np.sin(a) * np.sin(phi),
                        0.8 * np.cos(a)) for a in t], color=AMBER, lw=1.2)
            t = np.linspace(0, phi, 30)
            curve(ax, [(0.7 * np.cos(a), 0.7 * np.sin(a), 0) for a in t], color=AMBER, lw=1.2)
            txt(ax, P(x0 / 2, y0 / 2, z0 / 2) + (0.18, 0.12), "r", color=AMBER, ha="left")
            txt(ax, P(0.15, 0.2, 0.95) + (0.1, 0.05), "θ", color=AMBER, ha="left")
            txt(ax, P(0.75, 0.25, 0) + (-0.12, -0.18), "φ", color=AMBER)
        ax.plot(*pt, "o", color=NAVY, ms=7, zorder=5)
        txt(ax, pt + (0.12, 0.2), "P", color=NAVY, ha="left")
        _ = foot
    save(fig, "L17-coordinates.svg")


def unit_vectors():
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    blank(ax, (-2.3, 2.5), (-0.6, 2.6))
    arrow(ax, (-2.1, 0), (2.4, 0), color=GRAY, lw=1.2, ms=11)
    arrow(ax, (0, -0.4), (0, 2.5), color=GRAY, lw=1.2, ms=11)
    txt(ax, (2.4, -0.25), "x", color=GRAY)
    txt(ax, (-0.22, 2.45), "y", color=GRAY)
    for phi, name in ((np.radians(30), "φ₁"), (np.radians(125), "φ₂")):
        p = 1.7 * np.array([np.cos(phi), np.sin(phi)])
        ax.plot([0, p[0]], [0, p[1]], color=GRAY, lw=1.0, ls="--")
        ax.plot(*p, "o", color=INK, ms=5)
        rh = 0.75 * np.array([np.cos(phi), np.sin(phi)])
        ph = 0.75 * np.array([-np.sin(phi), np.cos(phi)])
        arrow(ax, p, p + rh, color=NAVY, lw=2.2)
        arrow(ax, p, p + ph, color=AMBER, lw=2.2)
        hat(ax, p + rh * 1.3, "ρ", color=NAVY)
        hat(ax, p + ph * 1.3, "φ", color=AMBER)
        t = np.linspace(0, phi, 30)
        rr = 0.45 if phi < 1 else 0.3
        ax.plot(rr * np.cos(t), rr * np.sin(t), color=GRAY, lw=1.0)
        m = phi / 2
        txt(ax, ((rr + 0.18) * np.cos(m), (rr + 0.18) * np.sin(m)), name, color=GRAY, size=12)
    save(fig, "L17-unit-vectors.svg")


def elements():
    fig, axs = plt.subplots(1, 2, figsize=(10.0, 4.4))

    # cylindrical: rho in [r0, r0+dr], phi in [p0, p0+dp], z in [z0, z0+dz]
    ax = axs[0]
    blank(ax, (-1.6, 3.4), (-1.0, 3.3))
    axes3(ax, 2.6)
    ax.set_title("cylindrical", fontsize=13, color=NAVY)
    r0, dr, p0, dp, z0, dz = 1.2, 0.9, np.radians(12), np.radians(48), 0.8, 1.0
    t = np.linspace(p0, p0 + dp, 30)

    def cyl(r, a, z):
        return (r * np.cos(a), r * np.sin(a), z)

    faces = []
    top_outer = [P(*cyl(r0 + dr, a, z0 + dz)) for a in t]
    top_inner = [P(*cyl(r0, a, z0 + dz)) for a in t[::-1]]
    faces.append(top_outer + top_inner)
    side_outer = [P(*cyl(r0 + dr, a, z0)) for a in t] + [P(*cyl(r0 + dr, a, z0 + dz)) for a in t[::-1]]
    faces.append(side_outer)
    end = [P(*cyl(r0, p0, z0)), P(*cyl(r0 + dr, p0, z0)),
           P(*cyl(r0 + dr, p0, z0 + dz)), P(*cyl(r0, p0, z0 + dz))]
    faces.append(end)
    for f in faces:
        ax.add_patch(Polygon(f, closed=True, fc=FILL, ec=NAVY, lw=1.3, alpha=0.95))
    curve(ax, [(0, 0, 0), cyl(r0, p0, 0)], color=GRAY, lw=0.9, ls="--")
    curve(ax, [cyl(r0, p0, 0), cyl(r0, p0, z0)], color=GRAY, lw=0.9, ls="--")
    # edge labels
    a = P(*cyl(r0 + dr / 2, p0, z0)); txt(ax, a + (-0.12, -0.12), "dρ", color=AMBER, ha="right")
    a = P(*cyl(r0 + dr, p0 + dp / 2, z0)); txt(ax, a + (0.05, -0.28), "ρ dφ", color=AMBER)
    a = P(*cyl(r0 + dr, p0 + dp, z0 + dz / 2)); txt(ax, a + (0.2, 0), "dz", color=AMBER, ha="left")

    # spherical: r in [r0, r0+dr], theta in [t0, t0+dt], phi in [p0, p0+dp]
    ax = axs[1]
    blank(ax, (-1.6, 3.4), (-1.0, 3.3))
    axes3(ax, 2.6)
    ax.set_title("spherical", fontsize=13, color=NAVY)
    R0, dR, t0, dt, q0, dq = 1.5, 0.8, np.radians(35), np.radians(30), np.radians(12), np.radians(48)

    def sph(r, th, ph):
        return (r * np.sin(th) * np.cos(ph), r * np.sin(th) * np.sin(ph), r * np.cos(th))

    tt = np.linspace(t0, t0 + dt, 30)
    qq = np.linspace(q0, q0 + dq, 30)
    outer = ([P(*sph(R0 + dR, t0, q)) for q in qq] + [P(*sph(R0 + dR, th, q0 + dq)) for th in tt]
             + [P(*sph(R0 + dR, t0 + dt, q)) for q in qq[::-1]] + [P(*sph(R0 + dR, th, q0)) for th in tt[::-1]])
    endq = ([P(*sph(r, t0, q0)) for r in (R0, R0 + dR)] + [P(*sph(R0 + dR, th, q0)) for th in tt]
            + [P(*sph(r, t0 + dt, q0)) for r in (R0 + dR, R0)] + [P(*sph(R0, th, q0)) for th in tt[::-1]])
    topt = ([P(*sph(R0, t0, q)) for q in qq] + [P(*sph(R0 + dR, t0, q)) for q in qq[::-1]])
    for f in (topt, endq, outer):
        ax.add_patch(Polygon(f, closed=True, fc=FILL, ec=NAVY, lw=1.3, alpha=0.95))
    curve(ax, [(0, 0, 0), sph(R0, t0, q0)], color=GRAY, lw=0.9, ls="--")
    a = P(*sph(R0 + dR / 2, t0 + dt, q0)); txt(ax, a + (-0.1, -0.22), "dr", color=AMBER, ha="right")
    a = P(*sph(R0 + dR, t0 + dt / 2, q0 + dq)); txt(ax, a + (0.18, 0), "r dθ", color=AMBER, ha="left")
    a = P(*sph(R0 + dR, t0, q0 + dq / 2)); txt(ax, a + (0.05, 0.28), "r sinθ dφ", color=AMBER)
    save(fig, "L17-elements.svg")


def gradient():
    fig, ax = plt.subplots(figsize=(4.8, 4.6))
    blank(ax, (-2.3, 2.3), (-2.3, 2.3))
    t = np.linspace(0, 2 * np.pi, 200)
    for c in (0.5, 1, 2, 3, 4):
        r = np.sqrt(c)
        ax.plot(r * np.cos(t), r * np.sin(t), color=GRAY, lw=1.0)
    g = np.linspace(-1.6, 1.6, 5)
    for x in g:
        for y in g:
            if abs(x) < 1e-9 and abs(y) < 1e-9:
                continue
            arrow(ax, (x, y), (x + 0.16 * x, y + 0.16 * y), color=NAVY, lw=1.5, ms=10)
    save(fig, "L17-gradient.svg")


def box(ax, o, d, **kw):
    x, y, z = o; a, b, c = d
    V = [(x, y, z), (x + a, y, z), (x + a, y + b, z), (x, y + b, z),
         (x, y, z + c), (x + a, y, z + c), (x + a, y + b, z + c), (x, y + b, z + c)]
    E = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    for i, j in E:
        curve(ax, [V[i], V[j]], **kw)
    return V


def flux_box():
    # Its own view, x to the right and y into the page, so F_x runs left to right.
    def Q(x, y, z):
        return np.array([x + 0.55 * y, 0.42 * y + z])

    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    blank(ax, (-1.9, 4.1), (-0.6, 2.3))
    a, b, c = 1.8, 1.4, 1.3
    V = [(0, 0, 0), (a, 0, 0), (a, b, 0), (0, b, 0), (0, 0, c), (a, 0, c), (a, b, c), (0, b, c)]
    for face in ([0, 3, 7, 4], [1, 2, 6, 5]):
        ax.add_patch(Polygon([Q(*V[i]) for i in face], closed=True, fc=FILL, ec="none", alpha=0.8))
    for i, j in [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
                 (0, 4), (1, 5), (2, 6), (3, 7)]:
        hidden = 3 in (i, j) and not ({i, j} & {1, 5, 6})
        ax.plot(*zip(Q(*V[i]), Q(*V[j])), color=NAVY, lw=1.0 if hidden else 1.4,
                ls="--" if hidden else "-")
    y0, z0 = b / 2, c / 2
    arrow(ax, Q(-1.5, y0, z0), Q(0, y0, z0), color=AMBER, lw=2.4)
    arrow(ax, Q(a, y0, z0), Q(a + 1.5, y0, z0), color=AMBER, lw=2.4)
    stxt(ax, Q(-0.8, y0, z0) + (0, 0.36), "F", "x", "(x)", color=AMBER)
    stxt(ax, Q(a + 1.0, y0, z0) + (0.1, 0.36), "F", "x", "(x + Δx)", color=AMBER)
    txt(ax, Q(a / 2, 0, 0) + (0, -0.25), "Δx", color=NAVY)
    txt(ax, Q(a, b / 2, 0) + (0.2, -0.08), "Δy", color=NAVY, ha="left")
    txt(ax, Q(0, 0, c / 2) + (-0.15, 0), "Δz", color=NAVY, ha="right")
    save(fig, "L17-flux-box.svg")


def tiling():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.4))
    # divergence: two cells side by side, a shared face
    ax = axs[0]
    blank(ax, (-0.3, 4.6), (-0.6, 2.4))
    for x0, lbl in ((0, "1"), (2.2, "2")):
        ax.add_patch(Polygon([(x0, 0), (x0 + 2.2, 0), (x0 + 2.2, 2), (x0, 2)], closed=True,
                             fc=FILL, ec=NAVY, lw=1.4))
        txt(ax, (x0 + 1.1, 1.65), "cell " + lbl, color=NAVY, size=12, italic=False)
    ax.plot([2.2, 2.2], [0, 2], color=AMBER, lw=2.6)
    arrow(ax, (1.55, 0.85), (2.85, 0.85), color=AMBER, lw=2.0)
    txt(ax, (2.2, -0.3), "out of 1 = into 2", color=AMBER, size=12, italic=False)
    ax.set_title("divergence theorem: shared faces", fontsize=12, color=NAVY)

    # Stokes: 2 x 2 loops, shared edges run both ways
    ax = axs[1]
    blank(ax, (-0.5, 4.5), (-0.6, 4.2))
    s = 1.8
    for i in range(2):
        for j in range(2):
            x0, y0 = 0.2 + i * s, 0.1 + j * s
            ax.add_patch(Polygon([(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)],
                                 closed=True, fc=FILL, ec="none"))
            g = 0.18
            sq = [(x0 + g, y0 + g), (x0 + s - g, y0 + g), (x0 + s - g, y0 + s - g), (x0 + g, y0 + s - g)]
            for k in range(4):
                a, b = np.array(sq[k]), np.array(sq[(k + 1) % 4])
                inner = (k == 1 and i == 0) or (k == 3 and i == 1) or (k == 2 and j == 0) or (k == 0 and j == 1)
                arrow(ax, a + 0.2 * (b - a), a + 0.8 * (b - a), color=AMBER if inner else NAVY,
                      lw=1.5 if inner else 2.0, ms=11)
    ax.add_patch(Polygon([(0.2, 0.1), (0.2 + 2 * s, 0.1), (0.2 + 2 * s, 0.1 + 2 * s), (0.2, 0.1 + 2 * s)],
                         closed=True, fc="none", ec=NAVY, lw=2.2))
    ax.set_title("Stokes' theorem: shared edges", fontsize=12, color=NAVY)
    save(fig, "L17-tiling.svg")


def curl_loop():
    fig, ax = plt.subplots(figsize=(5.4, 4.2))
    blank(ax, (-1.2, 4.0), (-1.0, 3.3))
    arrow(ax, (-0.8, 0), (3.6, 0), color=GRAY, lw=1.1, ms=10)
    arrow(ax, (0, -0.6), (0, 3.1), color=GRAY, lw=1.1, ms=10)
    txt(ax, (3.6, -0.25), "x", color=GRAY)
    txt(ax, (-0.25, 3.05), "y", color=GRAY)
    x0, y0, a, b = 0.8, 0.7, 2.0, 1.6
    ax.add_patch(Polygon([(x0, y0), (x0 + a, y0), (x0 + a, y0 + b), (x0, y0 + b)], closed=True,
                         fc=FILL, ec="none"))
    sides = [((x0, y0), (x0 + a, y0), ("x", "(y)"), (0, -0.3)),
             ((x0 + a, y0), (x0 + a, y0 + b), ("y", "(x + Δx)"), (0.15, 0)),
             ((x0 + a, y0 + b), (x0, y0 + b), ("x", "(y + Δy)"), (0, 0.3)),
             ((x0, y0 + b), (x0, y0), ("y", "(x)"), (-0.15, 0))]
    for (p, q, lbl, off) in sides:
        p, q = np.array(p), np.array(q)
        ax.plot(*zip(p, q), color=NAVY, lw=1.8)
        arrow(ax, p + 0.35 * (q - p), p + 0.65 * (q - p), color=NAVY, lw=2.0)
        m = (p + q) / 2 + off
        ha = "left" if off[0] > 0 else "right" if off[0] < 0 else "center"
        stxt(ax, m, "F", lbl[0], lbl[1], color=AMBER, size=13, ha=ha)
    txt(ax, (x0 + a / 2, y0 + b / 2), "ΔS = Δx Δy", color=GRAY, size=12, italic=False)
    save(fig, "L17-curl-loop.svg")


def div_curl():
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 4.3))
    g = np.linspace(-1.6, 1.6, 7)
    X, Y = np.meshgrid(g, g)
    for ax, (U, V), title in ((axs[0], (X, Y), "radial: divergence, no curl"),
                              (axs[1], (-Y, X), "circulating: curl, no divergence")):
        blank(ax, (-2.0, 2.0), (-2.0, 2.0))
        ax.quiver(X, Y, U, V, color=NAVY, angles="xy", scale_units="xy", scale=4.2,
                  width=0.008, headwidth=4)
        ax.set_title(title, fontsize=12.5, color=NAVY)
    save(fig, "L17-div-curl.svg")


def stokes_example():
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    blank(ax, (-0.6, 2.9), (-0.6, 2.8))
    arrow(ax, (-0.3, 0), (2.8, 0), color=GRAY, lw=1.1, ms=10)
    arrow(ax, (0, -0.3), (0, 2.7), color=GRAY, lw=1.1, ms=10)
    txt(ax, (2.8, -0.22), "x", color=GRAY)
    txt(ax, (-0.22, 2.65), "y", color=GRAY)
    t = np.linspace(0, np.pi / 2, 60)
    ax.fill(np.r_[0, 2 * np.cos(t)], np.r_[0, 2 * np.sin(t)], color=FILL)
    ax.plot([0, 2], [0, 0], color=NAVY, lw=2.2)
    ax.plot(2 * np.cos(t), 2 * np.sin(t), color=NAVY, lw=2.2)
    ax.plot([0, 0], [0, 2], color=NAVY, lw=2.2)
    arrow(ax, (0.8, 0), (1.25, 0), color=NAVY, lw=2.2)
    m = np.pi / 4
    arrow(ax, (2 * np.cos(m - 0.1), 2 * np.sin(m - 0.1)), (2 * np.cos(m + 0.1), 2 * np.sin(m + 0.1)),
          color=NAVY, lw=2.2)
    arrow(ax, (0, 1.25), (0, 0.8), color=NAVY, lw=2.2)
    txt(ax, (1.0, -0.25), "1", color=AMBER, italic=False)
    txt(ax, (2.25 * np.cos(m), 2.25 * np.sin(m)), "2", color=AMBER, italic=False)
    txt(ax, (-0.22, 1.0), "3", color=AMBER, italic=False)
    txt(ax, (2.0, -0.25), "2", color=GRAY, size=11, italic=False)
    txt(ax, (0.75, 0.7), "S", color=NAVY)
    save(fig, "L17-stokes-example.svg")


if __name__ == "__main__":
    coordinates()
    unit_vectors()
    elements()
    gradient()
    flux_box()
    tiling()
    curl_loop()
    div_curl()
    stokes_example()
