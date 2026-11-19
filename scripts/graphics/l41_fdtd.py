"""The L41 notebook's two-dimensional FDTD solver, for the figures.

The same solver as Part B of the Incidence Lab notebook (faculty
Labs/build_l41_notebooks.py): a TE or TM beam on a 24-cells-per-wavelength
Yee grid at S = 1/2, lined with a PML. l41_figures.py imports it to draw the
reflected-beam figure from a real run.
"""

from __future__ import annotations
import numpy as np

C0 = 299_792_458.0
EPS0 = 8.8541878128e-12
MU0 = 4e-7 * np.pi
ETA0 = np.sqrt(MU0 / EPS0)

F0 = 10e9
LAM0 = C0 / F0
W0 = 2 * np.pi * F0
D = LAM0 / 24
DT2 = 0.5 * D / C0
NX, NZ2, NPML = 704, 240, 24
ZB, ZS, ZM, ZT = 100, 64, 82, 118
X = (np.arange(NX) - NX // 2) * D
Z = (np.arange(NZ2) - ZB) * D


def _pml_rate(n, rmax=3e11):
    s = np.arange(n) + 0.5
    p = np.zeros(n)
    p[:NPML] = ((NPML - s[:NPML]) / NPML) ** 3
    p[-NPML:] = ((s[-NPML:] - (n - NPML)) / NPML) ** 3
    return rmax * np.clip(p, 0, None)


_RX = _pml_rate(NX)[:, None] * np.ones((1, NZ2))
_RZ = _pml_rate(NZ2)[None, :] * np.ones((NX, 1))
_EX, _EZ = np.exp(-_RX * DT2), np.exp(-_RZ * DT2)
_GX = np.where(_RX > 0, (1 - _EX) / np.where(_RX > 0, _RX, 1), DT2)
_GZ = np.where(_RZ > 0, (1 - _EZ) / np.where(_RZ > 0, _RZ, 1), DT2)


def simulate(pol, n1, n2, theta_deg, w=2.5, periods=30, avg=4):
    th = np.radians(theta_deg)
    eps = np.full((NX, NZ2), EPS0 * n1 ** 2)
    eps[:, ZB:] = EPS0 * n2 ** 2
    if pol == "TE":
        eps[:, ZB] = EPS0 * (n1 ** 2 + n2 ** 2) / 2
        cF, cA, s, amp = 1 / eps, np.full_like(eps, 1 / MU0), 1.0, 1.0
        cB = cA
    else:
        cF, cA, s, amp = np.full_like(eps, 1 / MU0), 1 / eps, -1.0, 1.0 / ETA0
        cB = cA.copy()
        cB[:, ZB] = (1 / (EPS0 * n1 ** 2) + 1 / (EPS0 * n2 ** 2)) / 2
    wx = w * LAM0 / np.cos(th)
    x0 = -(ZB - ZS) * D * np.tan(th)
    g = np.exp(-((X - x0) / wx) ** 2)
    kx = n1 * W0 / C0 * np.sin(th)
    Fx, Fz, A, B = (np.zeros((NX, NZ2)) for _ in range(4))
    Fp = np.zeros((NX, NZ2), complex)
    nsteps = int(periods / (F0 * DT2))
    nav = int(round(avg / (F0 * DT2)))
    for n in range(nsteps):
        t = n * DT2
        Fs = Fx + Fz
        A[:, :-1] = _EZ[:, :-1] * A[:, :-1] + s * _GZ[:, :-1] * cA[:, :-1] * (Fs[:, 1:] - Fs[:, :-1]) / D
        B[:-1, :] = _EX[:-1, :] * B[:-1, :] - s * _GX[:-1, :] * cB[:-1, :] * (Fs[1:, :] - Fs[:-1, :]) / D
        Fz[1:, 1:] = _EZ[1:, 1:] * Fz[1:, 1:] + s * _GZ[1:, 1:] * cF[1:, 1:] * (A[1:, 1:] - A[1:, :-1]) / D
        Fx[1:, 1:] = _EX[1:, 1:] * Fx[1:, 1:] - s * _GX[1:, 1:] * cF[1:, 1:] * (B[1:, 1:] - B[:-1, 1:]) / D
        Fz[:, ZS] += min(1.0, t * F0 / 3) * amp * g * np.sin(W0 * t - kx * X)
        if n >= nsteps - nav:
            Fp += (Fx + Fz) * np.exp(-1j * W0 * t)
    return 2 * Fp / nav
