---
frame_view: true
---

# L41 - Incidence Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">Incidence Lab</h1>

<div class="title-rule"></div>

Today you solve Maxwell's curl equations on a grid and measure reflection and refraction at a boundary.

Lesson 41 · Module 4: Dynamic Fields · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '9'; counter-reset: lo 4">
  <li>I can determine the reflection and transmission of UPW at a boundary for Transverse Electric (TE) and Transverse Magnetic (TM) waves, using boundary conditions.</li>
</ol>

:::{depth}
Lessons 38 through 40 found the reflected and transmitted uniform plane waves
(UPW) at a boundary by matching the tangential fields on it. This lab finds
them a second way: it steps Faraday's law and the Ampere–Maxwell law forward
in time on a grid, and the reflected and transmitted waves come out of the
computation without any boundary condition imposed. The method is the
**finite-difference time-domain (FDTD)** method, which engineers use to design
antennas, radomes, and optical coatings. In Part A a pulse travels along one
axis into a dielectric, and you measure $\Gamma$ and $\tau$ and design a
quarter-wave anti-reflection layer. In Part B a beam strikes acrylic at an
angle, and you measure Snell's law, the Brewster angle, and total internal
reflection. The lab is a Python notebook, run in Google Colab or on your own
machine, and you work in a team of two or three.
:::
::::

::::{frame} Where We Were
:::{present}
| Lesson | Result the lab checks |
| :-- | :-- |
| 33, 34 | The curl equations the grid steps forward |
| 38 | $\Gamma$, $\tau = 1 + \Gamma$, and Poynting's theorem |
| 39 | Snell's law and $\Gamma_\text{TE}$ |
| 40 | $\Gamma_\text{TM}$, the Brewster angle, and total internal reflection |
:::

Each part of the lab reproduces a result from Module 4. Lesson 33 derived the
two curl equations, which are all the grid needs, and Lesson 34 collected them
with the rest of Maxwell's equations. Lesson 38 matched the tangential fields at
a boundary to get

$$\Gamma = \frac{\eta_2 - \eta_1}{\eta_2 + \eta_1}, \qquad \tau = 1 + \Gamma,$$

and derived Poynting's theorem, which the lab uses to measure power. Lessons
39 and 40 extended the matching to a wave at an angle: phase matching gave
Snell's law, and the two polarizations gave $\Gamma_\text{TE}$,
$\Gamma_\text{TM}$, the Brewster angle, and the critical angle.
::::

::::{frame} From the Curl Equations to an Update
:::{present}
$$\begin{aligned} \frac{\partial H_y}{\partial t} &= -\frac{1}{\mu}\frac{\partial E_x}{\partial z} \\ \frac{\partial E_x}{\partial t} &= -\frac{1}{\epsilon}\frac{\partial H_y}{\partial z} \end{aligned}$$

$$\begin{aligned} E_x\big|^{n+1}_{k} = E_x\big|^{n}_{k} &- \frac{\Delta t}{\epsilon\Delta z}\left(H_y\big|^{n+1/2}_{k+1/2}\right. \\ &\left. - H_y\big|^{n+1/2}_{k-1/2}\right) \end{aligned}$$
:::

A plane wave along $z$ with $\mathbf{E} = \hat{\mathbf{x}}E_x$ and
$\mathbf{H} = \hat{\mathbf{y}}H_y$ depends only on $z$ and $t$. The $y$
component of Faraday's law and the $x$ component of the Ampere–Maxwell law,
both from Lesson 33, in a source-free and lossless medium, are the first two
equations. The grid replaces each derivative with a centered difference. For
the second equation, the time derivative at step $n + \tfrac{1}{2}$ and the
space derivative at node $k$ become

$$\begin{aligned} &\frac{E_x\big|^{n+1}_{k} - E_x\big|^{n}_{k}}{\Delta t} \\ &= -\frac{1}{\epsilon}\ \frac{H_y\big|^{n+1/2}_{k+1/2} - H_y\big|^{n+1/2}_{k-1/2}}{\Delta z}, \end{aligned}$$

and solving for the newest value gives the update on the slide. Faraday's law
gives the matching update for $H_y$:

$$\begin{aligned} H_y\big|^{n+1/2}_{k+1/2} = H_y\big|^{n-1/2}_{k+1/2} &- \frac{\Delta t}{\mu\Delta z}\left(E_x\big|^{n}_{k+1}\right. \\ &\left. - E_x\big|^{n}_{k}\right). \end{aligned}$$

The code applies the two updates in turn, once per time step, at every node at
once. Where a material boundary falls on an $E_x$ node, the cell around it,
from $k\Delta z - \Delta z/2$ to $k\Delta z + \Delta z/2$, is half in each
medium. $E_x$ is tangential, so it is continuous (Lesson 24) and takes one
value across the cell, and integrating the Ampere–Maxwell law over the cell
gives

$$\begin{aligned} &\left(\epsilon_1\frac{\Delta z}{2} + \epsilon_2\frac{\Delta z}{2}\right)\frac{\partial E_x}{\partial t} \\ &= -\left(H_y\big|_{k+1/2} - H_y\big|_{k-1/2}\right): \end{aligned}$$

that node takes the average permittivity $(\epsilon_1 + \epsilon_2)/2$. A field
*normal* to the boundary needs a different average, because its $D$, not its
$E$, is continuous; Part B meets that case.
::::

::::{frame} The Yee Grid
:::{present}
<img src="../../viz/img/L41-yee.svg"
     alt="Electric field nodes at whole cells and whole time steps, magnetic field nodes halfway between in space and in time, with two stencils: a new electric field value at node k comes from the old one below it and the two magnetic field values beside it, and a new magnetic field value at k plus one half comes from the old one below it and the two electric field values beside it"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">

- The grid stores $E_x$ at whole cells and whole steps.
- It stores $H_y$ halfway between, in space and in time.
:::

The centered differences need each field halfway between the samples of the
other. The grid therefore stores $E_x$ at $z = k\Delta z$ and $t = n\Delta t$,
and $H_y$ at $z = (k + \tfrac{1}{2})\Delta z$ and $t = (n + \tfrac{1}{2})\Delta t$.
This staggered arrangement is the **Yee grid**. The navy arrows show the
$E_x$ update: the new $E_x$ at node $k$ comes from the old $E_x$ there and the
two $H_y$ values on either side, half a step earlier. The amber arrows show the
$H_y$ update at $k + \tfrac{1}{2}$, from the old $H_y$ and the two $E_x$ values
on either side. Each update uses only its neighbors, so a computer can sweep it
across millions of cells.
::::

::::{frame} The Time Step
:::{present}
Substitute $E, H \propto e^{j(\omega n\Delta t - \beta k\Delta z)}$:

$$\sin\frac{\omega\Delta t}{2} = S\sin\frac{\beta\Delta z}{2}$$

$$S = \frac{v_p\Delta t}{\Delta z}$$

- The grid is stable only for $S \le 1$.
- At $S = 1$, $\omega = v_p\beta$ exactly.
:::

A time step that is too long makes the computed fields grow without bound. To
find the limit, we substitute $E_x = E_0e^{j(\omega n\Delta t - \beta k\Delta z)}$
and $H_y = H_0e^{j(\omega n\Delta t - \beta k\Delta z)}$ into the two updates.
A centered time difference of $e^{j\omega n\Delta t}$ is
$(2j/\Delta t)\sin(\omega\Delta t/2)$ times the wave at the half step, and a
centered space difference of $e^{-j\beta k\Delta z}$ is
$-(2j/\Delta z)\sin(\beta\Delta z/2)$ times the wave at the half node. The two
updates become

$$\epsilon\ \frac{2}{\Delta t}\sin\frac{\omega\Delta t}{2}\ E_0 = \frac{2}{\Delta z}\sin\frac{\beta\Delta z}{2}\ H_0,$$

$$\mu\ \frac{2}{\Delta t}\sin\frac{\omega\Delta t}{2}\ H_0 = \frac{2}{\Delta z}\sin\frac{\beta\Delta z}{2}\ E_0.$$

Multiplying the two equations eliminates $E_0H_0$:

$$\begin{aligned} \mu\epsilon\left(\frac{2}{\Delta t}\right)^2\sin^2\frac{\omega\Delta t}{2} &= \left(\frac{2}{\Delta z}\right)^2 \\ &\times \sin^2\frac{\beta\Delta z}{2}, \end{aligned}$$

and with $v_p = 1/\sqrt{\mu\epsilon}$ its square root is the slide's **grid
dispersion relation**. The shortest wave on the grid has $\beta\Delta z = \pi$,
so its sine is 1, and for $S > 1$ it would need $\sin(\omega\Delta t/2) > 1$:
$\omega$ becomes complex, and that wave grows without bound. The **Courant
condition** $S \le 1$ prevents it. At $S = 1$ the two sines are equal,
$\omega = v_p\beta$, and the grid carries every wave at exactly $v_p$. The
notebook runs air at $S = 1$, so the dielectric of $\epsilon_r = 4$ runs at
$S = 1/2$, where the grid's waves travel slightly slower than $v_p$. The
figure solves the dispersion relation for the grid's phase velocity: with 40
cells per wavelength the dielectric's waves are 0.1% slow, and the error grows
quickly below about 15 cells per wavelength.

<img src="../../viz/img/L41-dispersion.svg"
     alt="Grid phase velocity as a fraction of the true phase velocity against cells per wavelength on a log axis, for one dimension at S equals 1 (exactly 1), one dimension at S equals one half, and two dimensions at S equals 0.336 along an axis and along the diagonal; all approach 1 as the cells per wavelength grow, with dots at the notebook's Part A dielectric, 40 cells, and Part B acrylic, 16 cells"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
::::

::::{frame} Explore: The Courant Limit
:class: viz-frame

:::{present}
<iframe src="../../viz/fdtd-1d.html"
        width="100%" height="489"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="A Gaussian pulse stepping across a one-dimensional FDTD grid from air into a dielectric, with sliders for the Courant number and the dielectric's relative permittivity"
        data-autosize>
</iframe>
:::

The widget runs the two updates of this lesson on 400 cells: air on the left,
a dielectric of $\epsilon_{r2}$ on the right, a Gaussian pulse launched at the
source, and Mur ends. It runs a second grid with air everywhere, and the
difference at the probe is the reflected pulse; its signed peak over the
incident peak is the grid's $\Gamma$, shown beside Lesson 38's. Move $S$ below
1 and the pulse still splits correctly, but it spreads as the grid's dispersion
grows. Push $S$ just past 1 and the field near the source grows without bound
within a few dozen steps, which is the Courant condition at work. The readout
also gives $S$ in the dielectric, $S/\sqrt{\epsilon_{r2}}$.
::::

::::{frame} An Edge That Absorbs
:::{present}
At the left end the wave leaves toward $-z$, $E_x = f(t + z/v_p)$, so

$$\frac{\partial E_x}{\partial z} - \frac{1}{v_p}\frac{\partial E_x}{\partial t} = 0$$

$$\begin{aligned} E_x\big|^{n+1}_{0} = E_x\big|^{n}_{1} &+ \frac{v_p\Delta t - \Delta z}{v_p\Delta t + \Delta z} \\ &\times \left(E_x\big|^{n+1}_{1} - E_x\big|^{n}_{0}\right) \end{aligned}$$
:::

The grid has to end, and a wave that reaches the end must leave without
reflecting, as if the medium continued. At the left end every wave travels
toward $-z$, so it has the form $f(t + z/v_p)$, and differentiating shows that
it obeys the one-way equation on the slide. We write that equation with
centered differences at $z = \Delta z/2$ and $t = (n + \tfrac{1}{2})\Delta t$,
averaging the two nodes and the two time steps, at the point the figure marks:

<img src="../../viz/img/L41-mur.svg"
     alt="Four nodes, the end node 0 and its neighbor node 1 at time steps n and n plus 1, with dashed lines to a cross midway between them, the point where we write the one-way equation"
     style="max-width: 300px; width: 100%; display: block; margin: 0 auto;">

$$\begin{aligned} &\frac{E_x\big|^{n+1}_{1} + E_x\big|^{n}_{1} - E_x\big|^{n+1}_{0} - E_x\big|^{n}_{0}}{2\Delta z} \\ &= \frac{E_x\big|^{n+1}_{0} + E_x\big|^{n+1}_{1} - E_x\big|^{n}_{0} - E_x\big|^{n}_{1}}{2v_p\Delta t}. \end{aligned}$$

Multiplying by $2v_p\Delta t\Delta z$ and collecting the newest end value on
the left gives

$$\begin{aligned} &(v_p\Delta t + \Delta z)\ E_x\big|^{n+1}_{0} \\ &= (v_p\Delta t + \Delta z)\ E_x\big|^{n}_{1} \\ &+ (v_p\Delta t - \Delta z)\left(E_x\big|^{n+1}_{1} - E_x\big|^{n}_{0}\right), \end{aligned}$$

and dividing by $v_p\Delta t + \Delta z$ gives the slide's **Mur boundary**.
The right end is its mirror image. At $S = 1$ the coefficient is zero and the
end node copies its neighbor's previous value, which is exact for a wave that
moves one cell per step.
::::

::::{frame} Pre-Lab: Part A Predictions
:::{present}
<img src="../../viz/img/L41-line.svg"
     alt="A strip of grid cells: a source and a probe in air on the left, the boundary, the dielectric of relative permittivity 4 on the right with a second probe, an optional layer just before the boundary, Mur ends, and arrows for the incident, reflected, and transmitted pulses"
     style="max-width: 430px; width: 100%; display: block; margin: 0 auto;">

Air meets $\epsilon_r = 4$, so $\eta_2 = \eta_1/2$:

$$\Gamma = -\tfrac{1}{3}, \qquad \tau = \tfrac{2}{3}$$

$$\vert\Gamma\vert^2 + \frac{\eta_1}{\eta_2}\vert\tau\vert^2 = 1$$
:::

Work these before the lab period. The pulse starts at the source, passes the
probe, and splits at the boundary; the reflected pulse returns past the probe,
and the transmitted pulse passes the second probe. Lesson 38's coefficient with
$\eta_2 = \eta_1/2$ gives

$$\Gamma = \frac{\tfrac{1}{2} - 1}{\tfrac{1}{2} + 1} = -\frac{1}{3}, \qquad \tau = 1 + \Gamma = \frac{2}{3},$$

and the power check is $\tfrac{1}{9} + 2\cdot\tfrac{4}{9} = 1$. A layer between
the air and the dielectric acts as Lesson 7's section of transmission line: a
quarter wavelength thick inside itself, it turns the dielectric's $\eta_2$ into
$\eta_c^2/\eta_2$, which equals $\eta_1$ when $\eta_c = \sqrt{\eta_1\eta_2}$, so
$n_c = \sqrt{n_1 n_2} = \sqrt{2}$. At $1\ \text{GHz}$ its thickness is

$$d = \frac{\lambda_0}{4n_c} = \frac{0.30\ \text{m}}{4\sqrt{2}} = 53.0\ \text{mm}.$$

Lesson 7's line theory gives the layer's reflection at every frequency, plotted
below: a null at 1 GHz and $\vert\Gamma\vert < 0.1$ from about 0.82 to
1.18 GHz. The notebook measures the same curve on the grid.

<img src="../../viz/img/L41-arcoat.svg"
     alt="The magnitude of Gamma against frequency from 0.3 to 2.2 gigahertz for the quarter-wave layer: zero at 1 gigahertz, below 0.1 in a shaded band around it, and rising to one third at 2 gigahertz, where a dotted line marks the reflection with no layer"
     style="max-width: 540px; width: 100%; display: block; margin: 0 auto;">
::::

::::{frame} Two Dimensions, Two Polarizations
:::{present}
<img src="../../viz/img/L41-yee2d.svg"
     alt="One cell of the two-dimensional TE grid with x to the right and z down: E y at the grid nodes, H x halfway between nodes along z, H z halfway between nodes along x, with the grid spacing Delta marked"
     style="max-width: 340px; width: 100%; display: block; margin: 0 auto;">

- The plane of incidence is $xz$, and $\partial/\partial y = 0$.
- TE steps $E_y$, $H_x$, $H_z$; TM steps $H_y$, $E_x$, $E_z$.
- The grid is stable only for $S \le 1/\sqrt{2}$.
:::

Part B keeps Lesson 39's geometry: the boundary in the plane $z = 0$, medium 1
at $z < 0$, and the plane of incidence in the $xz$ plane. Nothing changes along
$y$, so every $\partial/\partial y$ is zero, and the six components of the curl
equations split into two independent sets. The TE set holds $E_y$, the field
perpendicular to the plane of incidence, with $H_x$ and $H_z$; the TM set holds
$H_y$ with $E_x$ and $E_z$. The figure places the TE set on a square grid of
spacing $\Delta$: $E_y$ at the nodes $(i, k)$, $H_x$ at $(i, k + \tfrac{1}{2})$,
and $H_z$ at $(i + \tfrac{1}{2}, k)$. For example, the $y$ component of the
Ampere–Maxwell law is

$$\epsilon\ \frac{\partial E_y}{\partial t} = \frac{\partial H_x}{\partial z} - \frac{\partial H_z}{\partial x},$$

and its centered differences give the $E_y$ update

$$\begin{aligned} E_y\big|^{n+1}_{i,k} &= E_y\big|^{n}_{i,k} \\ &+ \frac{\Delta t}{\epsilon\Delta}\left(H_x\big|^{n+1/2}_{i,k+1/2} - H_x\big|^{n+1/2}_{i,k-1/2}\right) \\ &- \frac{\Delta t}{\epsilon\Delta}\left(H_z\big|^{n+1/2}_{i+1/2,k} - H_z\big|^{n+1/2}_{i-1/2,k}\right); \end{aligned}$$

the notebook writes all three TE updates and the TM set. On the boundary row,
TE's $E_y$ is tangential and takes the average of $\epsilon$, as in Part A.
TM's $E_z$ there is normal to the boundary, and $D_z = \epsilon E_z$ is the
continuous quantity (Lesson 24), so the average of $E_z$ along the cell's side
is

$$\frac{1}{\Delta}\int E_z\ dz = D_z\ \frac{1}{2}\left(\frac{1}{\epsilon_1} + \frac{1}{\epsilon_2}\right):$$

a normal field takes the average of $1/\epsilon$.

To find the time step we substitute a plane wave with amplitudes $E_0$, $X_0$,
and $Z_0$ for $E_y$, $H_x$, and $H_z$. With
$\Omega = (2/\Delta t)\sin(\omega\Delta t/2)$ and
$K_x = (2/\Delta)\sin(\beta_x\Delta/2)$, and $K_z$ likewise, the three updates
become

$$\begin{aligned} \mu\Omega X_0 &= -K_zE_0, \\ \mu\Omega Z_0 &= K_xE_0, \\ \epsilon\Omega E_0 &= -K_zX_0 + K_xZ_0. \end{aligned}$$

Substituting the first two into the third gives $\mu\epsilon\Omega^2 = K_x^2 + K_z^2$, or

$$\begin{aligned} \sin^2\frac{\omega\Delta t}{2} = S^2\Big[&\sin^2\frac{\beta_x\Delta}{2} \\ &+ \sin^2\frac{\beta_z\Delta}{2}\Big]. \end{aligned}$$

Both sines can reach 1 at once, which needs $2S^2 \le 1$: the limit tightens to
$S \le 1/\sqrt{2}$. The notebook uses $S = 1/2$ in air, which is
$0.5/1.49 = 0.336$ in the acrylic, at 24 cells per free-space wavelength.
::::

::::{frame} The Simulation
:::{present}
<picture>
<source media="(max-width: 600px)" srcset="../../viz/img/L41-setup-phone.svg">
<img src="../../viz/img/L41-setup.svg"
     alt="A rectangle lined by an absorbing layer; a green source line near the top, with a Gaussian taper sketched on it, launches a beam at the angle theta i toward the boundary between medium 1 above and medium 2 below, and a faint arrow shows the beam it also launches upward into the absorbing layer; a reflected beam and a transmitted beam at theta t leave the boundary; two dashed lines, one above and one below the boundary, mark where the notebook measures power"
     style="max-width: 880px; width: 100%; display: block; margin: 0 auto;">
</picture>

The source is $g(x)\sin\left(\omega t - \beta_1 x\sin\theta_i\right)$.
:::

A line of cells parallel to the boundary drives the field. Its Gaussian taper
$g(x)$ makes a beam rather than an infinite plane wave, and its phase advances
along $x$ at Lesson 39's rate $\beta_1\sin\theta_i$, which is Lesson 39's
phase-matching condition applied to aim the beam at $\theta_i$. The source line
also launches a beam upward, away from the boundary, which the absorbing layer
removes. A **perfectly matched layer (PML)**, 24 cells thick, lines the edges.
Inside it each field obeys

$$\frac{\partial U}{\partial t} + rU = s,$$

with $s$ the curl term and a loss rate $r$ that grows toward the outer edge.
Multiplying by $e^{rt}$ makes the left side one derivative, and integrating over
one step with $s$ held constant gives the update:

$$\frac{d}{dt}\left(Ue^{rt}\right) = se^{rt},$$

$$U^{n+1} = e^{-r\Delta t}U^n + \frac{1 - e^{-r\Delta t}}{r}\ s.$$

The code splits each field into a part driven by the $x$ derivatives, which
decays at the rate $r_x$, and a part driven by the $z$ derivatives, at the rate
$r_z$. In the top and bottom layers only the part driven by $\partial/\partial z$
decays, so the layer leaves the wave's variation along $x$, its phase matching
along the layer, as it was, and the layer stays matched to a wave at any angle. Berenger
showed that when $\mathbf{E}$ and $\mathbf{H}$ decay at the same rate, such a
layer reflects nothing at any angle in the continuous limit; that proof is
beyond this course, and on the notebook's grid the layer reflects well under 1%.
::::

::::{frame} Measuring Power
:::{present}
<picture>
<source media="(max-width: 600px)" srcset="../../viz/img/L41-separation-phone.svg">
<img src="../../viz/img/L41-separation.svg"
     alt="Three maps of the electric field from a TE run at 45 degrees onto acrylic: the full run, with incident and reflected beams overlapping above the boundary and the transmitted beam below; the reference run with air everywhere, showing the incident beam alone; and their difference above the boundary, drawn on a color scale four times finer, which is the reflected beam alone; dashed lines above and below the boundary mark the two lines where the notebook measures power"
     style="max-width: 880px; width: 100%; display: block; margin: 0 auto;">
</picture>
:::

A beam has no single amplitude to compare: its field varies across its width,
and the transmitted beam has a different cross-section and a different $\eta$.
Power, by Lesson 38's Poynting theorem, crosses the boundary without loss, so
the notebook measures power. Once the field has settled into a steady state, it
extracts each field's phasor and integrates the time-average Poynting vector
along the two dashed lines,

$$P = \int \frac{1}{2}\text{Re}\left[\widetilde{\mathbf{E}}\times\widetilde{\mathbf{H}}^*\right]\cdot\hat{\mathbf{z}}\ dx,$$

which catches the whole beam whatever its shape.
Above the boundary the total field is the incident field plus the reflected
field, as the left map shows. A reference run with medium 1 everywhere (center)
gives the incident field alone, and subtracting it leaves the reflected beam
(right). The reflected power gives $R = \vert\Gamma\vert^2$, the power below the
boundary gives the transmitted fraction $T$, each measured on its own, and
every run checks that $R + T = 1$, which also tests the absorbing layer.
::::

::::{frame} Pre-Lab: Part B Predictions
:::{present}
| Quantity | Air onto acrylic, $n = 1.49$ |
| :-- | :-- |
| $\vert\Gamma\vert$ at $0^\circ$ | 0.197 |
| $\theta_t$ at $45^\circ$ | $28.3^\circ$ |
| Brewster angle | $56.1^\circ$ |
| Critical angle, acrylic to air | $42.2^\circ$ |
| $1/\alpha$ at $50^\circ$, acrylic to air | $0.289\lambda_0$ |
:::

Work these before the lab period, from Lessons 38 through 40. At normal
incidence, $\vert\Gamma\vert = (1.49 - 1)/(1.49 + 1) = 0.197$. Snell's law at
$45^\circ$ gives $\sin\theta_t = \sin 45^\circ/1.49 = 0.4746$, so
$\theta_t = 28.3^\circ$. The Brewster angle is $\arctan 1.49 = 56.1^\circ$,
where the TM reflection vanishes, as Lesson 40's figure shows:

<img src="../../viz/img/L40-brewster.svg"
     alt="Lesson 40's figure: at the Brewster angle the reflected and transmitted rays are perpendicular, and the reflected ray carries only the TE polarization"
     style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">

The critical angle from acrylic is $\arcsin(1/1.49) = 42.2^\circ$. Beyond it,
at $50^\circ$, Lesson 40's decay constant, with medium 2 air ($n_2 = 1$ and
$\beta_2 = \beta_0$), is

$$\begin{aligned} \alpha &= \beta_2q, \\ q &= \sqrt{\left(\frac{n_1}{n_2}\right)^2\sin^2\theta_i - 1} \\ &= \sqrt{1.49^2\sin^2 50^\circ - 1} = 0.550, \end{aligned}$$

so the evanescent field's decay length is

$$\frac{1}{\alpha} = \frac{\lambda_0}{2\pi\times 0.550} = 0.289\lambda_0.$$

The notebook also asks for $\vert\Gamma_\text{TE}\vert$ and
$\vert\Gamma_\text{TM}\vert$ at $30^\circ$, $45^\circ$, and $65^\circ$, from
Lessons 39 and 40.
::::

::::{frame} Why a Beam Is Not a Plane Wave
:::{present}
<img src="../../viz/img/L41-beam-brewster.svg"
     alt="The TM reflection magnitude against angle from 30 to 75 degrees: the plane-wave curve falls to zero at the Brewster angle of 56.1 degrees, the curve averaged over a beam 2.5 wavelengths wide bottoms out near 0.04, and the notebook's FDTD points follow the beam curve"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

- A beam holds plane waves over a spread of angles.
- Each angle in the spread reflects by its own $\Gamma$.
:::

Lessons 39 and 40 describe one plane wave at one angle. The notebook's beam has
a $1/e$ field half-width of $w = 2.5\lambda_0$, and a beam of finite width is a
sum of plane waves over a spread of about $\lambda/(\pi w)$ radians to each
side, with $\lambda$ the wavelength in medium 1. In air that is
$1/(2.5\pi) = 0.127$ rad, or $7.3^\circ$; in the acrylic it is
$1/(1.49\cdot 2.5\pi) = 0.085$ rad, or $4.9^\circ$. Only the wave at exactly
$56.1^\circ$ has $\Gamma_\text{TM} = 0$; its neighbors reflect a little, and
their powers add. Averaging the plane-wave $\vert\Gamma_\text{TM}\vert^2$ over
the beam's spread gives the dashed curve, whose minimum is about 0.04, and the
grid measures 0.043 at the Brewster angle, against about 0.38 for TE. The same
spread makes the evanescent field of Part B3 decay about 9% more slowly than
the single-angle prediction, $0.31\lambda_0$ against $0.289\lambda_0$, because
the angles nearer the critical angle decay more slowly. A wider beam narrows the
spread, but it needs a larger grid and a longer run.
::::

::::{frame} Teams and the Report
:class: read-only

Work in a team of two or three, and submit one report per team.

- Open the notebook in Colab (link below), choose **File**, then **Save a copy
  in Drive**, and share the copy with your teammates. Or download it and run
  it locally with Python 3, NumPy, and Matplotlib.
- Run the cells in order. A cell marked `TODO` is yours to finish; the rest are
  given. Answer every **Answer** cell. Part A runs in seconds; Part B's
  simulations take about three minutes in all.
- Before you submit, choose **Runtime**, then **Run all**, so every output is
  current. Put every member's name and a Documentation line in the first
  cell.
- Export to PDF and upload it to Gradescope as one team submission, adding
  every member.
- You do not check out any equipment; the lab needs only a laptop.
::::

::::{frame} Lab Notebook
:class: read-only doc-links

- <a class="doc-link" href="https://colab.research.google.com/github/livethisdream/ece343/blob/main/book/extras/labs/ECE343_Lab_L41_Incidence.ipynb" target="_blank" rel="noopener">Open the Incidence Lab notebook in Google Colab</a>
- <a class="doc-link" href="../../labs/ECE343_Lab_L41_Incidence.ipynb" download>Download the notebook (.ipynb)</a>

:::{depth}
The notebook is the lab packet and the turn-in document. It holds the
derivations, the code you finish, and the questions you answer. Colab runs it
in the browser with nothing to install; a local copy needs Python 3 with NumPy
and Matplotlib. Work the pre-lab predictions before the period.
:::
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 41**: this lab ends the course's lessons.
- **Final exam**: all four modules, from transmission lines to plane waves.
:::

The course began with a voltage wave on a transmission line and its reflection
from a load, and it ends with a plane wave and its reflection from a boundary.
Lesson 38 showed that the two are the same problem: $\Gamma$ in Lesson 6 and
$\Gamma$ in Lesson 38 are the same ratio of impedances, and the quarter-wave
layer of Part A is Lesson 7's quarter-wave line. Review the four modules for
the final exam with that shared $\Gamma$ in mind: transmission lines,
electrostatics, magnetostatics, and dynamic fields.
::::
