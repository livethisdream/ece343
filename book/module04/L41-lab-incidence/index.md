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
Lessons 38 through 40 found the reflected and transmitted waves at a boundary
by matching the tangential fields on it. This lab finds them a second way:
it steps Faraday's law and the Ampere–Maxwell law forward in time on a grid
and lets the waves sort themselves out. The method is the **finite-difference
time-domain (FDTD)** method, which engineers use to design antennas, radomes,
and optical coatings. In Part A a pulse travels along one axis into a
dielectric, and you measure $\Gamma$ and $\tau$ and design a quarter-wave
anti-reflection layer. In Part B a beam strikes acrylic at an angle, and you
measure Snell's law, the Brewster angle, and total internal reflection. The
lab is a Python notebook, run in Google Colab or on your own machine, and you
work in a team of two or three.
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

Each part of the lab reproduces a result from Module 4. Lessons 33 and 34
gave the two curl equations, which are all the grid needs. Lesson 38 matched
the tangential fields at a boundary to get $\Gamma = (\eta_2 - \eta_1)/(\eta_2 + \eta_1)$
and $\tau = 1 + \Gamma$, and derived Poynting's theorem, which the lab uses to
measure power. Lessons 39 and 40 extended the matching to a wave at an angle:
phase matching gave Snell's law, and the two polarizations gave
$\Gamma_\text{TE}$, $\Gamma_\text{TM}$, the Brewster angle, and the critical
angle.
::::

::::{frame} From the Curl Equations to an Update
:::{present}
$$\begin{aligned} \frac{\partial H_y}{\partial t} &= -\frac{1}{\mu}\frac{\partial E_x}{\partial z} \\ \frac{\partial E_x}{\partial t} &= -\frac{1}{\epsilon}\frac{\partial H_y}{\partial z} \end{aligned}$$

$$E_x\big|^{n+1}_{k} = E_x\big|^{n}_{k} - \frac{\Delta t}{\epsilon\Delta z}\left(H_y\big|^{n+1/2}_{k+1/2} - H_y\big|^{n+1/2}_{k-1/2}\right)$$
:::

A plane wave along $z$ with $\mathbf{E} = \hat{\mathbf{x}}E_x$ and
$\mathbf{H} = \hat{\mathbf{y}}H_y$ depends only on $z$ and $t$. The $y$
component of Faraday's law (Lesson 33) and the $x$ component of the
Ampere–Maxwell law (Lesson 34), in a source-free and lossless medium, are the
first two equations. The grid replaces each derivative with a centered
difference. For the second equation, the time derivative at step $n + \tfrac{1}{2}$
and the space derivative at node $k$ become

$$\frac{E_x\big|^{n+1}_{k} - E_x\big|^{n}_{k}}{\Delta t} = -\frac{1}{\epsilon}\ \frac{H_y\big|^{n+1/2}_{k+1/2} - H_y\big|^{n+1/2}_{k-1/2}}{\Delta z},$$

and solving for the newest value gives the update on the slide. Faraday's law
gives the matching update for $H_y$:

$$H_y\big|^{n+1/2}_{k+1/2} = H_y\big|^{n-1/2}_{k+1/2} - \frac{\Delta t}{\mu\Delta z}\left(E_x\big|^{n}_{k+1} - E_x\big|^{n}_{k}\right).$$

The code applies the two updates in turn, once per time step, at every node at
once. Where a material boundary falls on an $E_x$ node, the cell around it is
half in each medium, and integrating the Ampere–Maxwell law over the cell gives
that node the average permittivity $(\epsilon_1 + \epsilon_2)/2$.
::::

::::{frame} The Yee Grid
:::{present}
<img src="../../viz/img/L41-yee.svg"
     alt="Electric field nodes at whole cells and whole time steps, magnetic field nodes halfway between in space and in time, with arrows showing that a new electric field value comes from the old one below it and the two magnetic field values beside it"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">

- $E_x$ lives at whole cells and whole steps.
- $H_y$ lives halfway between, in space and in time.
:::

The centered differences need each field halfway between the samples of the
other. The grid therefore stores $E_x$ at $z = k\Delta z$ and $t = n\Delta t$,
and $H_y$ at $z = (k + \tfrac{1}{2})\Delta z$ and $t = (n + \tfrac{1}{2})\Delta t$.
This staggered arrangement is the **Yee grid**, after Kane Yee, who published it
in 1966. The arrows show one update: the new $E_x$ at node 2 comes from the old
$E_x$ there and the two $H_y$ values on either side, half a step earlier. Each
update uses only its neighbors, so a computer can sweep it across millions of
cells.
::::

::::{frame} The Time Step
:::{present}
Substitute $E, H \propto e^{j(\omega n\Delta t - \beta k\Delta z)}$:

$$\sin\frac{\omega\Delta t}{2} = S\sin\frac{\beta\Delta z}{2}, \qquad S = \frac{v_p\Delta t}{\Delta z}$$

- Stable only for $S \le 1$.
- At $S = 1$, $\omega = v_p\beta$ exactly.
:::

A time step that is too long makes the simulation blow up. To find the limit,
we substitute a wave into the two updates. In the $E_x$ update, the time
difference of $e^{j\omega n\Delta t}$ gives $2j\sin(\omega\Delta t/2)$ times the
wave at the half step, and the space difference of $e^{-j\beta k\Delta z}$ gives
$-2j\sin(\beta\Delta z/2)$ times the wave at the half node. The $H_y$ update
gives the same factors. Eliminating the ratio of the two amplitudes between the
two equations leaves
$\sin^2(\omega\Delta t/2) = (\Delta t/\Delta z)^2\sin^2(\beta\Delta z/2)/(\mu\epsilon)$,
whose square root is the slide's **grid dispersion relation**. The shortest
wave on the grid has $\beta\Delta z = \pi$, so its sine is 1, and for $S > 1$ it
would need $\sin(\omega\Delta t/2) > 1$: $\omega$ becomes complex, and that wave
grows without bound. The **Courant condition** $S \le 1$ prevents it. At
$S = 1$ the two sines are equal, $\omega = v_p\beta$, and the grid carries every
wave at exactly $v_p$. The notebook runs air at $S = 1$, so the dielectric of
$\epsilon_r = 4$ runs at $S = 1/2$, where the grid's waves travel slightly slower
than $v_p$.
::::

::::{frame} An Edge That Absorbs
:::{present}
At the left end the wave leaves toward $-z$: $E_x = f(t + z/v_p)$, so

$$\frac{\partial E_x}{\partial z} - \frac{1}{v_p}\frac{\partial E_x}{\partial t} = 0$$

$$E_x\big|^{n+1}_{0} = E_x\big|^{n}_{1} + \frac{v_p\Delta t - \Delta z}{v_p\Delta t + \Delta z}\left(E_x\big|^{n+1}_{1} - E_x\big|^{n}_{0}\right)$$
:::

The grid has to end, and a wave that reaches the end must leave without
reflecting, as if the medium continued. At the left end every wave travels
toward $-z$, so it has the form $f(t + z/v_p)$, and differentiating shows that
it obeys the one-way equation on the slide. We write that equation with
centered differences at $z = \Delta z/2$ and $t = (n + \tfrac{1}{2})\Delta t$,
averaging the two nodes and the two time steps:

$$\frac{E_x\big|^{n+1}_{1} + E_x\big|^{n}_{1} - E_x\big|^{n+1}_{0} - E_x\big|^{n}_{0}}{2\Delta z} - \frac{E_x\big|^{n+1}_{0} + E_x\big|^{n+1}_{1} - E_x\big|^{n}_{0} - E_x\big|^{n}_{1}}{2v_p\Delta t} = 0.$$

Solving for $E_x\big|^{n+1}_{0}$ gives the slide's **Mur boundary**, and the
right end is its mirror image. At $S = 1$ the coefficient is zero and the end
node simply copies its neighbor's previous value, which is exact for a wave
that moves one cell per step.
::::

::::{frame} Pre-Lab: Part A Predictions
:::{present}
Air onto $\epsilon_r = 4$, so $\eta_2 = \eta_1/2$:

$$\Gamma = -\tfrac{1}{3}, \qquad \tau = \tfrac{2}{3}, \qquad \vert\Gamma\vert^2 + \frac{\eta_1}{\eta_2}\vert\tau\vert^2 = 1$$

Quarter-wave layer: $n_c = \sqrt{2}$, $d = 53.0\ \text{mm}$ at $1\ \text{GHz}$
:::

Work these before the lab period. Lesson 38's coefficient with $\eta_2 = \eta_1/2$
gives $\Gamma = (\tfrac{1}{2} - 1)/(\tfrac{1}{2} + 1) = -\tfrac{1}{3}$ and
$\tau = 1 + \Gamma = \tfrac{2}{3}$, and the power check is
$\tfrac{1}{9} + 2\cdot\tfrac{4}{9} = 1$. A layer between the air and the
dielectric acts as Lesson 7's section of transmission line: a quarter
wavelength thick inside itself, it turns the dielectric's $\eta_2$ into
$\eta_c^2/\eta_2$, which equals $\eta_1$ when $\eta_c = \sqrt{\eta_1\eta_2}$, so
$n_c = \sqrt{n_1 n_2} = \sqrt{2}$. At $1\ \text{GHz}$ its thickness is
$d = \lambda_0/(4n_c) = 0.30/(4\sqrt{2}) = 53.0\ \text{mm}$. The notebook
measures the reflection of the layer from 0.3 to 1.7 GHz and compares it with
Lesson 7's input impedance.
::::

::::{frame} Two Dimensions, Two Polarizations
:::{present}
Plane of incidence $xz$, $\partial/\partial y = 0$:

| | Fields stepped |
| :-- | :-- |
| TE | $E_y,\ H_x,\ H_z$ |
| TM | $H_y,\ E_x,\ E_z$ |

Courant: $S \le 1/\sqrt{2}$
:::

Part B keeps Lesson 39's geometry: the boundary in the plane $z = 0$, medium 1
at $z < 0$, and the plane of incidence in the $xz$ plane. Nothing changes along
$y$, so every $\partial/\partial y$ is zero, and the six components of the curl
equations split into two independent sets. The TE set holds $E_y$, the field
perpendicular to the plane of incidence, with $H_x$ and $H_z$; for example, the
$y$ component of the Ampere–Maxwell law becomes
$\epsilon\ \partial E_y/\partial t = \partial H_x/\partial z - \partial H_z/\partial x$.
The TM set holds $H_y$ with $E_x$ and $E_z$. The grid staggers each set in $x$,
$z$, and $t$ as Part A staggered its two fields in $z$ and $t$. Substituting a plane wave on a square
grid gives
$\sin^2(\omega\Delta t/2) = S^2[\sin^2(\beta_x\Delta/2) + \sin^2(\beta_z\Delta/2)]$;
both sines can reach 1 at once, so the limit tightens to $S \le 1/\sqrt{2}$.
The notebook uses $S = 1/2$ and 24 cells per free-space wavelength.
::::

::::{frame} The Simulation
:::{present}
<img src="../../viz/img/L41-setup.svg"
     alt="A rectangle lined by an absorbing layer; a green source line near the top launches a beam at the angle theta i toward the boundary between medium 1 above and medium 2 below; a reflected beam and a transmitted beam at theta t leave the boundary; two dashed lines, one above and one below the boundary, mark the lines along which the notebook measures power"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">

Source: $g(x)\sin\left(\omega t - \beta_1 x\sin\theta_i\right)$
:::

A line of cells parallel to the boundary drives the field. Its Gaussian taper
$g(x)$ makes a beam rather than an infinite plane wave, and its phase advances
along $x$ at Lesson 39's rate $\beta_1\sin\theta_i$, which aims the beam at
$\theta_i$: phase matching, used to steer. A **perfectly matched layer
(PML)**, 24 cells thick, lines the edges; inside it each field obeys
$\partial U/\partial t + rU = s$ with a loss rate $r$ that grows toward the
outer edge. Holding the curl term $s$ constant over one step and integrating
gives the update
$U^{n+1} = e^{-r\Delta t}U^n + (1 - e^{-r\Delta t})s/r$. The field is split
into a part driven by the $x$ derivatives, which decays at the rate $r_x$, and a
part driven by the $z$ derivatives, at the rate $r_z$. Berenger showed in 1994
that such a layer, with $\mathbf{E}$ and $\mathbf{H}$ decaying at the same rate,
reflects nothing at any angle in the continuous limit; that proof is beyond this
course, and on the notebook's grid the layer reflects well under 1%.
::::

::::{frame} Measuring Power
:::{present}
$$P = \int \frac{1}{2}\text{Re}\left[\widetilde{\mathbf{E}}\times\widetilde{\mathbf{H}}^*\right]\cdot\hat{\mathbf{z}}\ dx$$

- A run with medium 1 everywhere gives the incident field alone.
- Full run minus that run leaves the reflected field.
- $R = P_r/P_i = \vert\Gamma\vert^2$
:::

A beam has no single amplitude to compare: its field varies across its width,
and the transmitted beam has a different width and a different $\eta$. Power,
by Lesson 38's Poynting theorem, crosses the boundary without loss, so the
notebook measures power. Once the field has settled into a steady state, it
extracts each field's phasor and integrates the time-average Poynting vector
along the two dashed lines in the figure, which catches the whole beam whatever
its shape. Above the boundary the total field is the incident field plus the
reflected field; subtracting a reference run with medium 1 everywhere removes
the incident part. The ratios give $R = \vert\Gamma\vert^2$ and the transmitted
fraction $T$, and every run checks that $R + T = 1$, which also tests the
absorbing layer.
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
$\theta_t = 28.3^\circ$. The Brewster angle is $\arctan 1.49 = 56.1^\circ$, and
the critical angle from acrylic is $\arcsin(1/1.49) = 42.2^\circ$. Beyond it,
at $50^\circ$, Lesson 40's
$\alpha = \beta_0\sqrt{1.49^2\sin^2 50^\circ - 1} = 0.550\beta_0$ gives the
evanescent field's decay length $1/\alpha = \lambda_0/(2\pi\times 0.550) = 0.289\lambda_0$.
The notebook also asks for $\vert\Gamma_\text{TE}\vert$ and
$\vert\Gamma_\text{TM}\vert$ at $30^\circ$, $45^\circ$, and $65^\circ$, from
Lessons 39 and 40.
::::

::::{frame} Why a Beam Is Not a Plane Wave
:::{present}
- A beam $w$ wide spreads over about $\lambda/(\pi w)$ radians.
- Each angle in the spread reflects by its own $\Gamma$.
- So the measured $\vert\Gamma_\text{TM}\vert$ at Brewster is small, not zero.
:::

Lessons 39 and 40 describe one plane wave at one angle. The notebook's beam is
$2.5\lambda_0$ wide, and a beam of finite width is a sum of plane waves over a
spread of about $\lambda/(\pi w) = 1/(2.5\pi) = 0.13$ rad, or $7^\circ$ to each
side. Only the wave at exactly $56.1^\circ$ has $\Gamma_\text{TM} = 0$; its
neighbors reflect a little, and their powers add. You should expect
$\vert\Gamma_\text{TM}\vert$ near 0.06 at the Brewster angle, against about
0.38 for TE, and an evanescent field that decays a few percent more slowly than
the single-angle prediction. A wider beam narrows the spread, but it needs a
larger grid and a longer run.
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
- Nothing to check out: the lab needs only a laptop.
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
- This lab ends the course's lessons.
- The final exam covers all four modules.
:::

The course began with a voltage wave on a transmission line and its reflection
from a load, and it ends with a plane wave and its reflection from a boundary.
Lesson 38 showed that the two are the same problem: $\Gamma$ in Lesson 6 and
$\Gamma$ in Lesson 38 are the same ratio of impedances, and the quarter-wave
layer of Part A is Lesson 7's quarter-wave line. Review the four modules for
the final exam with that thread in mind: lines, static fields, magnetostatics,
and the waves that Maxwell's equations predict.
::::
