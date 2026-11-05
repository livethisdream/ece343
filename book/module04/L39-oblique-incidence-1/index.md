---
frame_view: true
---

# L39 - Oblique Incidence I

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">Oblique Incidence I</h1>

<div class="title-rule"></div>

Today we find where a plane wave goes, and how much of it reflects, when it meets a boundary at an angle.

Lesson 39 · Module 4: Dynamic Fields · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '9'; counter-reset: lo 4">
  <li>I can determine the reflection and transmission of UPW at a boundary for Transverse Electric (TE) and Transverse Magnetic (TM) waves, using boundary conditions.</li>
</ol>

:::{depth}
Lesson 38 sent a uniform plane wave straight at a flat boundary and found the
reflection and transmission coefficients from the boundary conditions of
Lessons 24 and 31. Today the wave arrives at an angle. The same boundary
conditions now decide two things. They fix the directions of the reflected and
transmitted waves, which gives the law of reflection and Snell's law. They
also fix the amplitudes, but the answer depends on how the electric field is
oriented, so we split every wave into two cases. Today we work the
**transverse electric** (TE) case in full; Lesson 40 works the transverse
magnetic (TM) case and the two angles that make oblique incidence useful.
:::
::::

::::{frame} Where We Were
:::{present}
At a boundary with no surface current or charge, the tangential fields match:

$$\hat{\mathbf{n}}\times\left(\tilde{\mathbf{E}}_1 - \tilde{\mathbf{E}}_2\right) = 0, \qquad \hat{\mathbf{n}}\times\left(\tilde{\mathbf{H}}_1 - \tilde{\mathbf{H}}_2\right) = 0$$

At normal incidence (Lesson 38):

$$\Gamma = \frac{\eta_2 - \eta_1}{\eta_2 + \eta_1}, \qquad \tau = 1 + \Gamma$$
:::

Lesson 24 showed that the tangential electric field is continuous across any
boundary, and Lesson 31 showed the same for the tangential magnetic field
when no surface current flows, which is the case at a boundary between two
dielectrics. As before, $\hat{\mathbf{n}}$ is the unit normal from region 2
into region 1. Lesson 37 found that a uniform plane wave in a lossless
material has its electric and magnetic fields perpendicular to each other and
to the direction of travel, with magnitudes in the ratio of the **intrinsic
impedance** $\eta = \sqrt{\mu/\epsilon}$. Lesson 38 applied the two boundary
conditions to a wave that meets the boundary head-on. The **reflection
coefficient** $\Gamma$ is the ratio of the reflected electric field to the
incident one at the boundary, and the **transmission coefficient** $\tau$ is
the same ratio for the transmitted field. Both have the form of Lesson 6's
load reflection coefficient, with the intrinsic impedances in place of the
load and line impedances.
::::

::::{frame} A Wave at an Angle
:::{present}
<img src="../../viz/img/L39-geometry.svg"
     alt="A flat boundary between region 1 above and region 2 below, with the normal drawn dashed; the incident ray arrives at angle theta i from the normal, the reflected ray leaves at theta r, and the transmitted ray continues into region 2 at theta t, bent toward the normal; axes x along the boundary, z down into region 2, and y out of the page"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">

$$\tilde{\mathbf{E}} = \mathbf{E}_0\ e^{-j\beta\ \hat{\mathbf{k}}\cdot\mathbf{r}}, \qquad \hat{\mathbf{k}}_i = \hat{\mathbf{x}}\sin\theta_i + \hat{\mathbf{z}}\cos\theta_i$$
:::

We put the boundary in the plane $z = 0$, with region 1 at $z < 0$ and
region 2 at $z > 0$, so $\hat{\mathbf{n}} = -\hat{\mathbf{z}}$. A plane wave
that travels in the direction of the unit vector $\hat{\mathbf{k}}$ has the
phase $\beta\ \hat{\mathbf{k}}\cdot\mathbf{r}$ at the point
$\mathbf{r} = \hat{\mathbf{x}}x + \hat{\mathbf{y}}y + \hat{\mathbf{z}}z$. When
$\hat{\mathbf{k}} = \hat{\mathbf{z}}$ this is the familiar $\beta z$ of
Lesson 37; for any other direction, the surfaces of constant phase are still
planes perpendicular to $\hat{\mathbf{k}}$. Here $\beta = \omega\sqrt{\mu\epsilon}$
is the phase constant of the material the wave is in. We measure each angle
from the normal. The incident direction and the normal together define the
**plane of incidence**; we choose the $x$ axis so that this is the $xz$ plane,
which makes the incident direction
$\hat{\mathbf{k}}_i = \hat{\mathbf{x}}\sin\theta_i + \hat{\mathbf{z}}\cos\theta_i$.
The reflected wave travels back into region 1 with
$\hat{\mathbf{k}}_r = \hat{\mathbf{x}}\sin\theta_r - \hat{\mathbf{z}}\cos\theta_r$,
and the transmitted wave travels into region 2 with
$\hat{\mathbf{k}}_t = \hat{\mathbf{x}}\sin\theta_t + \hat{\mathbf{z}}\cos\theta_t$.
The two new angles, $\theta_r$ and $\theta_t$, are unknowns for now; the
boundary conditions will set them.
::::

::::{frame} Two Polarizations: TE and TM
:::{present}
<img src="../../viz/img/L39-te-tm.svg"
     alt="Two copies of the boundary and its three rays; on the left, the TE case, the electric field of the incident wave points out of the page and the magnetic field lies in the plane of the page, perpendicular to the ray; on the right, the TM case, the magnetic field points out of the page and the electric field lies in the plane"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">

- **TE**: $\tilde{\mathbf{E}}$ along $\hat{\mathbf{y}}$, perpendicular to the plane of incidence.
- **TM**: $\tilde{\mathbf{H}}$ along $\hat{\mathbf{y}}$; $\tilde{\mathbf{E}}$ lies in the plane.
:::

The electric field of a plane wave is perpendicular to $\hat{\mathbf{k}}$,
which leaves it two directions to point in. One is $\hat{\mathbf{y}}$,
perpendicular to the plane of incidence and therefore parallel to the
boundary. We call that wave **transverse electric**, because its electric
field is transverse to the plane of incidence. The other direction lies in
the plane of incidence; then the magnetic field points along $\hat{\mathbf{y}}$,
and we call the wave **transverse magnetic**. Any uniform plane wave, whatever
its polarization in Lesson 37's sense, is the sum of a TE wave and a TM wave
with the same $\hat{\mathbf{k}}$. Because the boundary conditions and
Maxwell's equations are linear, we can find the reflection of each part
separately and add the results. The two parts reflect differently, which is
why we need both.
::::

::::{frame} Phase Matching
:::{present}
At $z = 0$, for every $x$ (TE, tangential $\tilde{E}_y$):

$$E_0\ e^{-j\beta_1 x\sin\theta_i} + E_0^r\ e^{-j\beta_1 x\sin\theta_r} = E_0^t\ e^{-j\beta_2 x\sin\theta_t}$$

$$\beta_1\sin\theta_i = \beta_1\sin\theta_r = \beta_2\sin\theta_t$$
:::

Before we find any amplitudes, the boundary conditions already restrict the
angles. Write the three electric fields of a TE wave with amplitudes $E_0$,
$E_0^r$, and $E_0^t$, and evaluate their phases on the boundary. At $z = 0$
the phase $\beta\ \hat{\mathbf{k}}\cdot\mathbf{r}$ reduces to
$\beta x\sin\theta$, because the $z$ term vanishes. The tangential electric
field must match at every point of the boundary, so the equation in the frame
must hold for every value of $x$, not only at the origin. Each term is an
exponential in $x$ with its own rate. A sum of exponentials with different
rates cannot equal a third exponential at every $x$: if the rates differ, the
terms drift in and out of step as $x$ grows, and equality at one point fails
at the next. The incident term is not zero, so the equation can hold only if
all three terms vary along the boundary at the same rate. That requirement is
**phase matching**: the three waves must have the same phase variation along
the boundary. The same argument applied to the TM wave, or to the magnetic
field, gives the same result, because the exponents are the same.
::::

::::{frame} Reflection and Snell's Law
:::{present}
<img src="../../viz/img/L39-phase-match.svg"
     alt="Wavefronts of the incident wave in region 1 and of the transmitted wave in region 2 meet the boundary at the same points, marked by dots; the transmitted fronts are closer together and tilted, so the transmitted wave travels closer to the normal"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">

$$\theta_r = \theta_i, \qquad n_1\sin\theta_i = n_2\sin\theta_t, \qquad n = \sqrt{\mu_r\epsilon_r} = \frac{c}{v_p}$$
:::

The first equality in phase matching, $\beta_1\sin\theta_i = \beta_1\sin\theta_r$,
gives $\theta_r = \theta_i$: the **law of reflection**. For the second, write
$\beta = \omega\sqrt{\mu\epsilon} = (\omega/c)\sqrt{\mu_r\epsilon_r}$ and define
the **refractive index** $n = \sqrt{\mu_r\epsilon_r}$, the ratio of the speed of
light in free space to the phase velocity in the material. The factor
$\omega/c$ is common to both sides and cancels, which leaves **Snell's law**,
$n_1\sin\theta_i = n_2\sin\theta_t$. The figure shows what phase matching
means. Each line is a wavefront, a surface of constant phase, drawn one
wavelength apart along its ray. A wavefront of the incident wave crosses the
boundary at a point, and a wavefront of the transmitted wave must cross at the
same point. Along the boundary the incident crossings are
$\lambda_1/\sin\theta_i$ apart, and the transmitted crossings must have the
same spacing. Region 2 has the shorter wavelength, so its fronts tilt to keep
the spacing, and the transmitted wave travels closer to the normal. Going
from air, $n_1 = 1$, into acrylic, $n_2 = 1.49$, at $\theta_i = 45^\circ$,
Snell's law gives $\sin\theta_t = \sin 45^\circ/1.49 = 0.475$, so
$\theta_t = 28.3^\circ$.
::::

::::{frame} The Fields of a TE Wave
:::{present}
$$\begin{aligned} \tilde{\mathbf{E}}^i &= \hat{\mathbf{y}}\ E_0\ e^{-j\psi_i} \\ \tilde{\mathbf{H}}^i &= \frac{E_0}{\eta_1}\left(-\hat{\mathbf{x}}\cos\theta_i + \hat{\mathbf{z}}\sin\theta_i\right)e^{-j\psi_i} \\ \tilde{\mathbf{E}}^r &= \hat{\mathbf{y}}\ \Gamma_\text{TE}E_0\ e^{-j\psi_r} \\ \tilde{\mathbf{H}}^r &= \frac{\Gamma_\text{TE}E_0}{\eta_1}\left(\hat{\mathbf{x}}\cos\theta_i + \hat{\mathbf{z}}\sin\theta_i\right)e^{-j\psi_r} \\ \tilde{\mathbf{E}}^t &= \hat{\mathbf{y}}\ \tau_\text{TE}E_0\ e^{-j\psi_t} \\ \tilde{\mathbf{H}}^t &= \frac{\tau_\text{TE}E_0}{\eta_2}\left(-\hat{\mathbf{x}}\cos\theta_t + \hat{\mathbf{z}}\sin\theta_t\right)e^{-j\psi_t} \end{aligned}$$
:::

The phases are the $\beta\ \hat{\mathbf{k}}\cdot\mathbf{r}$ of each wave:

$$\begin{aligned} \psi_i &= \beta_1\left(x\sin\theta_i + z\cos\theta_i\right) \\ \psi_r &= \beta_1\left(x\sin\theta_i - z\cos\theta_i\right) \\ \psi_t &= \beta_2\left(x\sin\theta_t + z\cos\theta_t\right) \end{aligned}$$

Each electric field points along $\hat{\mathbf{y}}$, with the incident
amplitude $E_0$ and the unknown amplitudes written as $\Gamma_\text{TE}E_0$ and
$\tau_\text{TE}E_0$. We have already used $\theta_r = \theta_i$. Each magnetic
field comes from Lesson 37's relation for a plane wave,
$\tilde{\mathbf{H}} = \hat{\mathbf{k}}\times\tilde{\mathbf{E}}/\eta$, with the
wave's own direction and intrinsic impedance. For the incident wave,

$$\hat{\mathbf{k}}_i\times\hat{\mathbf{y}} = \left(\hat{\mathbf{x}}\sin\theta_i + \hat{\mathbf{z}}\cos\theta_i\right)\times\hat{\mathbf{y}} = \hat{\mathbf{z}}\sin\theta_i - \hat{\mathbf{x}}\cos\theta_i$$

using $\hat{\mathbf{x}}\times\hat{\mathbf{y}} = \hat{\mathbf{z}}$ and
$\hat{\mathbf{z}}\times\hat{\mathbf{y}} = -\hat{\mathbf{x}}$. The reflected
wave's direction has $-\hat{\mathbf{z}}\cos\theta_i$ in place of
$+\hat{\mathbf{z}}\cos\theta_i$, which flips the sign of its $x$ component.
The transmitted wave uses $\theta_t$, $\beta_2$, and $\eta_2$.
::::

::::{frame} The TE Boundary Conditions
:::{present}
At $z = 0$, after phase matching cancels the common factor $e^{-j\beta_1 x\sin\theta_i}$:

$$\begin{aligned} \tilde{E}_y:&\quad 1 + \Gamma_\text{TE} = \tau_\text{TE} \\ \tilde{H}_x:&\quad \frac{\cos\theta_i}{\eta_1}\left(1 - \Gamma_\text{TE}\right) = \frac{\cos\theta_t}{\eta_2}\ \tau_\text{TE} \end{aligned}$$
:::

The tangential components at the boundary are the $x$ and $y$ components. The
electric field has only a $y$ component, and it must be the same on both
sides: the incident and reflected fields add in region 1 and equal the
transmitted field in region 2. Dividing by $E_0$ gives the first equation. The
magnetic field has a tangential $x$ component and a normal $z$ component, and
only the $x$ component enters this condition. In region 1 it is
$-E_0\cos\theta_i/\eta_1$ from the incident wave plus
$\Gamma_\text{TE}E_0\cos\theta_i/\eta_1$ from the reflected wave; in region 2
it is $-\tau_\text{TE}E_0\cos\theta_t/\eta_2$. Setting them equal and dividing
by $-E_0$ gives the second equation. Phase matching makes every exponential on
the boundary equal to the same $e^{-j\beta_1 x\sin\theta_i}$, so it divides out
and the two equations hold at every $x$.
::::

::::{frame} The TE Coefficients
:::{present}
$$\begin{aligned} \eta_2\cos\theta_i\left(1 - \Gamma_\text{TE}\right) &= \eta_1\cos\theta_t\left(1 + \Gamma_\text{TE}\right) \\ \Gamma_\text{TE} &= \frac{\eta_2\cos\theta_i - \eta_1\cos\theta_t}{\eta_2\cos\theta_i + \eta_1\cos\theta_t} \\ \tau_\text{TE} &= 1 + \Gamma_\text{TE} = \frac{2\eta_2\cos\theta_i}{\eta_2\cos\theta_i + \eta_1\cos\theta_t} \end{aligned}$$
:::

The first condition gives $\tau_\text{TE}$ in terms of $\Gamma_\text{TE}$, so
we substitute $1 + \Gamma_\text{TE}$ for $\tau_\text{TE}$ in the second and
multiply both sides by $\eta_1\eta_2$. That gives the first line, with one
unknown. Expanding both sides gives
$\eta_2\cos\theta_i - \eta_2\cos\theta_i\ \Gamma_\text{TE} = \eta_1\cos\theta_t + \eta_1\cos\theta_t\ \Gamma_\text{TE}$;
collecting the $\Gamma_\text{TE}$ terms on one side and dividing gives the
reflection coefficient. Adding one and putting the sum over the common
denominator gives the transmission coefficient. We find $\theta_t$ first from
Snell's law, and then each coefficient is a number.
::::

::::{frame} Two Checks on the TE Result
:::{present}
- $\theta_i = 0$: $\theta_t = 0$, and $\Gamma_\text{TE} = \dfrac{\eta_2 - \eta_1}{\eta_2 + \eta_1}$, Lesson 38's $\Gamma$.
- $\theta_i \to 90^\circ$: $\cos\theta_i \to 0$, so $\Gamma_\text{TE} \to -1$.
:::

At normal incidence, Snell's law gives $\theta_t = 0$, both cosines are one,
and the TE coefficients reduce to Lesson 38's. They must: at normal incidence
the plane of incidence is not defined, and every polarization is TE. At the
other extreme, a wave that arrives at grazing incidence, traveling almost
along the boundary, reflects completely with its electric field reversed,
for any pair of materials. This is why a smooth surface such as a road or a
lake looks like a mirror when we view it at a low angle.
::::

::::{frame} Reflection Against Angle
:::{present}
<img src="../../viz/img/L39-gamma-te.svg"
     alt="Plot of the TE reflection coefficient, from minus 0.197 at normal incidence to minus one at grazing incidence, and the TE transmission coefficient, from 0.803 to zero, against the angle of incidence for air into acrylic; the reflection coefficient is minus 0.299 at 45 degrees"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

- Air into acrylic, $n_2 = 1.49$: $\Gamma_\text{TE}$ runs from $-0.197$ at normal incidence to $-1$.
:::

The plot shows both TE coefficients for a wave in air striking acrylic. For a
nonmagnetic material, $\eta = \eta_0/n$, so acrylic has
$\eta_2 = 376.7/1.49 = 252.8\ \Omega$. At normal incidence
$\Gamma_\text{TE} = -0.197$, and $\vert\Gamma_\text{TE}\vert$ grows steadily
with angle until the wave reflects completely at grazing incidence. The
reflection coefficient stays negative and real at every angle: going into a
material with a larger refractive index, the reflected electric field is
reversed with respect to the incident one, as it was at normal incidence in
Lesson 38. The transmission coefficient falls from $0.803$ to zero.
::::

::::{frame} Worked Example: Air into Acrylic at 45°
:::{present}
$\theta_i = 45^\circ$, $n_1 = 1$, $n_2 = 1.49$: $\theta_t = 28.3^\circ$.

$$\begin{aligned} \Gamma_\text{TE} &= \frac{252.8\cos 45^\circ - 376.7\cos 28.3^\circ}{252.8\cos 45^\circ + 376.7\cos 28.3^\circ} = -0.299 \\ \tau_\text{TE} &= 1 + \Gamma_\text{TE} = 0.701 \end{aligned}$$
:::

:::{admonition} Worked example — a TE wave on acrylic
:class: tip
A TE wave in air strikes a flat acrylic surface at $\theta_i = 45^\circ$.
Acrylic is nonmagnetic, with $n = 1.49$ at visible wavelengths, so
$\epsilon_r = n^2 = 2.22$. Find the transmitted angle, the two TE coefficients,
and the fraction of the incident power that reflects.

Snell's law gives $\theta_t = 28.3^\circ$. The
intrinsic impedances are $\eta_1 = 376.7\ \Omega$ and
$\eta_2 = 376.7/1.49 = 252.8\ \Omega$. With $\cos 45^\circ = 0.7071$ and
$\cos 28.3^\circ = 0.8803$, the numerator of $\Gamma_\text{TE}$ is
$178.8 - 331.6 = -152.8$ and the denominator is $178.8 + 331.6 = 510.4$, so
$\Gamma_\text{TE} = -0.299$ and $\tau_\text{TE} = 0.701$.

The reflected wave travels in the same material as the incident wave and at
the same angle to the boundary, so the power it carries across a given area
of the boundary is $\vert\Gamma_\text{TE}\vert^2 = 0.090$ of the incident
power: $9.0\%$ reflects. In a lossless material the rest, $91.0\%$, is
transmitted. The transmitted fraction is not $\vert\tau_\text{TE}\vert^2 = 0.491$,
because the transmitted wave travels in a material with a different intrinsic
impedance and at a different angle to the boundary; both change how much
power a field of a given amplitude carries across the boundary. Including
both factors, $\vert\tau_\text{TE}\vert^2(\eta_1/\eta_2)(\cos\theta_t/\cos\theta_i) = 0.910$,
which matches.
:::
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Result |
| :-- | :-- | :-- |
| $\hat{\mathbf{k}}$ | Unit vector along the direction of travel | Phase $\beta\ \hat{\mathbf{k}}\cdot\mathbf{r}$ |
| Plane of incidence | Holds $\hat{\mathbf{k}}_i$ and the normal | The $xz$ plane |
| TE | $\tilde{\mathbf{E}}$ perpendicular to the plane of incidence | $\tilde{\mathbf{E}}$ along $\hat{\mathbf{y}}$ |
| TM | $\tilde{\mathbf{H}}$ perpendicular to the plane of incidence | $\tilde{\mathbf{H}}$ along $\hat{\mathbf{y}}$ (Lesson 40) |
| Phase matching | Same phase variation along the boundary | $\beta_1\sin\theta_i = \beta_1\sin\theta_r = \beta_2\sin\theta_t$ |
| Law of reflection | | $\theta_r = \theta_i$ |
| Snell's law | $n = \sqrt{\mu_r\epsilon_r} = c/v_p$ | $n_1\sin\theta_i = n_2\sin\theta_t$ |
| $\Gamma_\text{TE}$ | Reflected over incident $\tilde{E}_y$ | $\frac{\eta_2\cos\theta_i - \eta_1\cos\theta_t}{\eta_2\cos\theta_i + \eta_1\cos\theta_t}$ |
| $\tau_\text{TE}$ | Transmitted over incident $\tilde{E}_y$ | $1 + \Gamma_\text{TE}$ |
| Reflected power | Fraction of the incident power | $\vert\Gamma_\text{TE}\vert^2$ |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE343_L39_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE343_L39_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 40**: the TM coefficients, the Brewster angle, where TM reflection vanishes, and total internal reflection.
- **Lesson 41**: the Incidence Lab.
:::

Today we derived the directions of the reflected and transmitted waves for
any polarization, and the amplitudes for a TE wave. Lesson 40 repeats the
amplitude calculation for the TM wave. Its reflection coefficient behaves
differently: it passes through zero at one angle, the Brewster angle. Lesson
40 also asks what Snell's law means when it gives $\sin\theta_t > 1$, which
happens when a wave tries to leave a material with a larger refractive index
at a steep angle, and every bit of the wave reflects. Lesson 41 is the
Incidence Lab.

Before Lesson 40, read section 5.7 of Ellingson, *Electromagnetics*, Vol. 2.
::::
