---
frame_view: true
---

# L34 - Maxwell's Equations

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">Maxwell's Equations</h1>

<div class="title-rule"></div>

Today we collect the four laws of electromagnetics for fields that change with time.

Lesson 34 · Module 4: Dynamic Fields · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '8'; counter-reset: lo 2">
  <li>I know the forms of Maxwell's equations for time-varying fields and use them to calculate electric and magnetic fields for a variety of physical systems.</li>
</ol>

:::{depth}
Modules 2 and 3 derived four laws for fields that do not change with time, and
Lesson 33 added the two terms that a changing field brings: Faraday's
$\partial\mathbf{B}/\partial t$ and Maxwell's displacement current
$\partial\mathbf{D}/\partial t$. Today we write the four laws together as
**Maxwell's equations**, derive the point forms of the two that changed, and
show that the set conserves charge. We then use the set three ways: to find
the voltage that a changing magnetic flux induces in a loop, to check that a
proposed pair of fields obeys all four laws, and to derive the voltage and
current ratios of an ideal transformer. Lessons 35 through 37 use the same
equations to show that the fields travel as a wave.
:::
::::

::::{frame} Where We Were
:::{present}
| Law | Static form | Lesson |
| :-- | :-- | :-: |
| Gauss's law | $\oint_S \mathbf{D}\cdot d\mathbf{s} = Q_\text{encl}$ | 20–21 |
| Gauss's law for magnetism | $\oint_S \mathbf{B}\cdot d\mathbf{s} = 0$ | 28 |
| Faraday's law | $\oint_C \mathbf{E}\cdot d\mathbf{l} = 0$ | 22 |
| Ampere's law | $\oint_C \mathbf{H}\cdot d\mathbf{l} = I_\text{encl}$ | 29 |
:::

Lesson 30 closed Module 3 with this table of the laws of static fields. Two
laws describe the electric field and two the magnetic field, and in statics
the two halves never mix: charges make the electric field, currents make the
magnetic field, and neither field appears in the other's equations. Lesson 33
showed that this separation fails once the fields change. A changing magnetic
flux through a closed path drives a circulation of $\mathbf{E}$ around it, so
the static Faraday's law gains a term. A charging capacitor carries a current
into one plate with no conduction current across the gap, so Ampere's law
gains a term in the changing electric flux. Today we write the four laws with
those two terms in place.
::::

::::{frame} Maxwell's Equations
:::{present}
| Law | Integral form |
| :-- | :-- |
| Gauss's law | $\oint_S \mathbf{D}\cdot d\mathbf{s} = Q_\text{encl}$ |
| Gauss's law for magnetism | $\oint_S \mathbf{B}\cdot d\mathbf{s} = 0$ |
| Faraday's law | $\oint_C \mathbf{E}\cdot d\mathbf{l} = -\frac{d}{dt}\int_S \mathbf{B}\cdot d\mathbf{s}$ |
| Ampere–Maxwell law | $\oint_C \mathbf{H}\cdot d\mathbf{l} = I_\text{encl} + \frac{d}{dt}\int_S \mathbf{D}\cdot d\mathbf{s}$ |
:::

Together with the material relations later in this lesson, these four
equations describe every classical electromagnetic field. The two
Gauss's laws keep their static form: Lesson 20 derived Gauss's law from
Coulomb's law and Lesson 21 its point form, and Lesson 28 showed that magnetic
field lines close, so the net magnetic flux out of any closed surface is zero.
Neither law contains a time derivative, so each holds at every instant even
when the fields change. Faraday's law is Lesson 33's: the circulation of
$\mathbf{E}$ around a closed path $C$ equals the negative rate of change of the
magnetic flux through a surface $S$ bounded by $C$. The **Ampere–Maxwell law**
is Lesson 29's Ampere's law with Lesson 33's displacement current added: the
circulation of $\mathbf{H}$ equals the conduction current through $S$ plus the
rate of change of the electric flux through it. In both circulation laws, the
right-hand rule of Lesson 29 ties the direction of travel around $C$ to the
normal of $S$.
::::

::::{frame} What Each Equation Says
:::{present}
| Point form | What it says |
| :-- | :-- |
| $\nabla\cdot\mathbf{D} = \rho_v$ | Charge is the source of $\mathbf{D}$. |
| $\nabla\cdot\mathbf{B} = 0$ | $\mathbf{B}$ has no source; its lines close. |
| $\nabla\times\mathbf{E} = -\frac{\partial\mathbf{B}}{\partial t}$ | A changing $\mathbf{B}$ drives a circulating $\mathbf{E}$. |
| $\nabla\times\mathbf{H} = \mathbf{J} + \frac{\partial\mathbf{D}}{\partial t}$ | Current and a changing $\mathbf{D}$ drive a circulating $\mathbf{H}$. |
:::

The point forms state each law at a single point, and the next frame derives
the two that changed. Each equation names a source. Gauss's law says that electric flux begins and
ends on charge. Gauss's law for magnetism says that there is no magnetic
charge, so magnetic flux has nowhere to begin or end. The two curl equations
are where time enters, and they couple the fields: a magnetic field that
changes with time produces an electric field that circulates around it, and
an electric field that changes with time produces a magnetic field that
circulates around it, just as a conduction current does. The minus sign in
Faraday's law is Lenz's law from Lesson 33: the induced electric field drives
a current whose own magnetic flux opposes the change. Because each field's
change drives the other, the pair can sustain itself in a region with no
charge and no current at all, which is the electromagnetic wave of Lessons 35
through 37.
::::

::::{frame} From Integral Form to Point Form
:::{present}
$$\begin{aligned} \oint_C \mathbf{E}\cdot d\mathbf{l} &= -\frac{d}{dt}\int_S \mathbf{B}\cdot d\mathbf{s} \\ \int_S \left(\nabla\times\mathbf{E}\right)\cdot d\mathbf{s} &= -\int_S \frac{\partial\mathbf{B}}{\partial t}\cdot d\mathbf{s} \\ \nabla\times\mathbf{E} &= -\frac{\partial\mathbf{B}}{\partial t} \end{aligned}$$
:::

Lessons 21 and 28 turned the two Gauss's laws into point forms with the
divergence theorem. The two circulation laws use Stokes' theorem from Lesson
17 instead, and Lesson 29 used it on Ampere's law. We start from Faraday's
law for a path $C$ and a surface $S$ that do not move. Stokes' theorem turns
the circulation on the left into the flux of $\nabla\times\mathbf{E}$ through
$S$. On the right, we hold the surface still, so the derivative with respect to
time acts only on $\mathbf{B}$ and moves inside the integral as a partial
derivative. The two surface integrals are now equal for every surface we
choose, however small, so the integrands must be equal at every point, which
is the point form. The same three steps applied to the Ampere–Maxwell law,
with $I_\text{encl} = \int_S \mathbf{J}\cdot d\mathbf{s}$, give
$\nabla\times\mathbf{H} = \mathbf{J} + \partial\mathbf{D}/\partial t$.
::::

::::{frame} Conservation of Charge
:::{present}
$$\begin{aligned} \nabla\cdot\left(\nabla\times\mathbf{H}\right) &= \nabla\cdot\mathbf{J} + \frac{\partial}{\partial t}\left(\nabla\cdot\mathbf{D}\right) \\ 0 &= \nabla\cdot\mathbf{J} + \frac{\partial\rho_v}{\partial t} \end{aligned}$$
:::

The set contains a law we did not put in by hand. Lesson 29 showed that the
divergence of any curl is zero, because the mixed partial derivatives cancel.
We take the divergence of both sides of the Ampere–Maxwell law. The left side
is zero. On the right, the divergence and the time derivative act on different
variables, so they commute, and Gauss's law replaces $\nabla\cdot\mathbf{D}$
with $\rho_v$. The result is the **continuity equation**,
$\nabla\cdot\mathbf{J} = -\partial\rho_v/\partial t$. Integrated over a volume
with the divergence theorem, it says that the net current out of a closed
surface equals the rate at which the charge inside decreases: charge is
conserved. For steady current, $\rho_v$ does not change, and the equation
reduces to Lesson 27's $\nabla\cdot\mathbf{J} = 0$. Without the displacement
current, the left side would still be zero, and the equations would force
$\nabla\cdot\mathbf{J} = 0$ even on a charging capacitor plate, where charge
accumulates. The displacement current is the term that makes Ampere's law
agree with conservation of charge.
::::

::::{frame} The Static Limit
:::{present}
With $\partial/\partial t = 0$:

$$\nabla\times\mathbf{E} = 0, \qquad \nabla\times\mathbf{H} = \mathbf{J}, \qquad \nabla\cdot\mathbf{J} = 0$$

- The fields decouple into Modules 2 and 3.
:::

When nothing changes with time, every time derivative in the set is zero. The
curl of $\mathbf{E}$ vanishes, which is the conservative field of Lesson 22,
and the Ampere–Maxwell law reduces to Lesson 29's Ampere's law. The two
Gauss's laws keep their form. What remains is the table of static fields from
the start of the lesson, in which the electric field depends only on charge
and the magnetic field only on current. The static results also hold
approximately when the fields change slowly enough. A circuit much smaller
than a wavelength, the condition of Lesson 3's electrical length, sees the
same field everywhere at each instant, so we can solve it as if it were
static at each moment. That **quasi-static** approximation is how we treat
the loops and the transformer later in this lesson.
::::

::::{frame} The Material Relations
:::{present}
$$\mathbf{D} = \epsilon\mathbf{E}, \qquad \mathbf{B} = \mu\mathbf{H}, \qquad \mathbf{J} = \sigma\mathbf{E}$$

$$\nabla\times\mathbf{H} = \sigma\mathbf{E} + \epsilon\frac{\partial\mathbf{E}}{\partial t}$$
:::

Maxwell's equations hold in any material. The material enters through three
relations from earlier lessons: $\mathbf{D} = \epsilon\mathbf{E}$ from Lesson
20, $\mathbf{B} = \mu\mathbf{H}$ from Lesson 28, and Ohm's law in point form,
$\mathbf{J} = \sigma\mathbf{E}$, from Lesson 27. In a uniform material with
constant $\epsilon$, $\mu$, and $\sigma$, the three relations let us write the
set in $\mathbf{E}$ and $\mathbf{H}$ alone. The Ampere–Maxwell law then has a
conduction term and a displacement term side by side. For a field that varies
as $\cos\omega t$, the conduction term has amplitude $\sigma E$ and the
displacement term $\omega\epsilon E$, so their ratio is $\sigma/(\omega\epsilon)$,
the ratio Lesson 27 used to separate good conductors from good insulators.
Copper at 100 MHz has $\sigma/(\omega\epsilon_0) = 1.0\times10^{10}$, so
conduction current dominates completely.
::::

::::{frame} Example 1: A Loop in a Ramping Field
:::{present}
$a = 10$ cm, $R = 1\ \text{k}\Omega$, $B_0 = 0.2$ T, $t_0 = 3$ s:

$$B(t) = \begin{cases} 0 & t < 0 \\ B_0\ t/t_0 & 0 \le t \le t_0 \\ B_0 & t > t_0 \end{cases}$$
:::
:::{present}
<img src="../../viz/img/L34-loop.svg"
     alt="A circular wire loop of radius a in the xy plane with a resistor R in a small gap at the front, a uniform field B of t pointing up along z through the loop, and an arrow marking counterclockwise travel around the path C"
     style="max-width: 400px; width: 100%; display: block; margin: 0 auto;">
:::

This example is from the 2025 slides. A wire loop of radius $a = 10$ cm lies
in the $xy$ plane with a $1\ \text{k}\Omega$ resistor in a small gap. A
uniform magnetic flux density $\mathbf{B} = \hat{\mathbf{z}}\ B(t)$ fills the
region. It is zero before $t = 0$, rises linearly to $B_0 = 0.2$ T over
$t_0 = 3$ s, and then holds steady. We want the voltage across the resistor
and the current through it. We take the path $C$ along the wire,
counterclockwise as seen from $+z$, so by the right-hand rule the normal of
the flat surface $S$ inside the loop is $+\hat{\mathbf{z}}$. The loop is a
fraction of a meter across and the field changes over seconds, so the
quasi-static approximation holds, and the wire, a good conductor, carries
essentially no electric field: the whole circulation of $\mathbf{E}$ appears
across the gap.
::::

::::{frame} Example 1: The Induced Voltage
:::{present}
$$\begin{aligned} \oint_C \mathbf{E}\cdot d\mathbf{l} &= -\frac{d}{dt}\left[\pi a^2 B(t)\right] = -\pi a^2\frac{B_0}{t_0} \\ &= -\frac{\pi(0.1)^2(0.2)}{3} = -2.09\ \text{mV} \quad (0 < t < t_0) \end{aligned}$$
:::
:::{present}
<img src="../../viz/img/L34-ramp.svg"
     alt="Two stacked plots against time in seconds: B rises linearly from 0 at t equals 0 to 0.2 tesla at t equals 3 and then holds; the magnitude of the loop voltage is a constant 2.09 millivolts between 0 and 3 seconds and zero otherwise"
     style="max-width: 440px; width: 100%; display: block; margin: 0 auto;">
:::

$\mathbf{B}$ is uniform and along the normal, so the flux through $S$ is the
field times the area, $\Phi = \pi a^2 B(t)$. Faraday's law gives the
circulation as the negative rate of change of that flux. During the ramp the
flux grows at the constant rate $\pi a^2 B_0/t_0$, so the circulation is a
constant $-2.09$ mV; before the ramp and after it the flux does not change,
and the circulation is zero. The minus sign means the electric field drives
current clockwise as seen from $+z$, opposite to $C$. A clockwise current makes
a magnetic field along $-\hat{\mathbf{z}}$ inside the loop, which opposes the
growing flux, as Lenz's law requires. The resistor carries the full
$2.09$ mV, so Ohm's law gives a current of
$2.09\ \text{mV}/1\ \text{k}\Omega = 2.09\ \mu$A for the 3 s of the ramp. The
voltage depends on how fast the flux changes, not on how large it is: at
$t = 5$ s the field is at its largest and the voltage is zero.
::::

::::{frame} Example 2: A Sinusoidal Field
:::{present}
$$\begin{aligned} B(t) &= B_0\sin\omega t, \qquad f = 1\ \text{kHz} \\ \oint_C \mathbf{E}\cdot d\mathbf{l} &= -\pi a^2 B_0\ \omega\cos\omega t \\ &= -(39.5\ \text{V})\cos\omega t \end{aligned}$$
:::
:::{present}
<img src="../../viz/img/L34-sine.svg"
     alt="Two stacked plots against time in milliseconds over two periods: B is a sine wave of amplitude 0.2 tesla; the loop voltage is a negative cosine of amplitude about 40 volts, peaking a quarter period after B"
     style="max-width: 440px; width: 100%; display: block; margin: 0 auto;">
:::

The second example in the 2025 slides keeps the loop and the resistor and
drives the field sinusoidally at $f = 1$ kHz, with the same amplitude
$B_0 = 0.2$ T. The flux is $\pi a^2 B_0\sin\omega t$, with
$\omega = 2\pi f = 6283$ rad/s. Differentiating gives a voltage that follows
$-\cos\omega t$, with amplitude
$\pi a^2 B_0\omega = \pi(0.1)^2(0.2)(6283) = 39.5$ V. The resistor current
has amplitude $39.5\ \text{V}/1\ \text{k}\Omega = 39.5$ mA. The voltage is
largest when $B$ passes through zero, where the flux changes fastest, and it
lags $B$ by a quarter period. Compared with Example 1, the same field
amplitude produces about $19{,}000$ times the voltage, because the flux now
changes in a quarter of a millisecond instead of three seconds. The induced
voltage grows in proportion to frequency, which is why power transformers and
the coupled coils of wireless chargers work with alternating current.
::::

::::{frame} Checking a Pair of Fields: Faraday's Law
:::{present}
$\mathbf{E} = \hat{\mathbf{x}}\ E_0\cos(\omega t - \beta z)$, in a uniform lossless region with no charge or current:

$$\begin{aligned} \nabla\times\mathbf{E} &= \hat{\mathbf{y}}\ \frac{\partial E_x}{\partial z} = \hat{\mathbf{y}}\ \beta E_0\sin(\omega t - \beta z) = -\mu\frac{\partial\mathbf{H}}{\partial t} \\ \mathbf{H} &= \hat{\mathbf{y}}\ \frac{\beta E_0}{\mu\omega}\cos(\omega t - \beta z) \end{aligned}$$
:::

Maxwell's equations also tell us whether a proposed field can exist, and if it
can, what field must accompany it. We take an electric field along
$\hat{\mathbf{x}}$ that varies with $z$ and $t$ as $\cos(\omega t - \beta z)$,
in a region with permittivity $\epsilon$, permeability $\mu$, and no charge or
current. Because $E_x$ depends only on $z$, the only surviving term of the
Cartesian curl from Lesson 17 is the $\hat{\mathbf{y}}$ component
$\partial E_x/\partial z$. Faraday's law sets that curl equal to
$-\mu\ \partial\mathbf{H}/\partial t$. Integrating with respect to time, and
dropping the constant of integration, which would be a static field
unrelated to this one, gives $\mathbf{H}$ along $\hat{\mathbf{y}}$, in step
with $\mathbf{E}$ and perpendicular to it. The two Gauss's laws hold
automatically: $D_x$ does not depend on $x$ and $B_y$ does not depend on $y$,
so both divergences are zero.
::::

::::{frame} Checking a Pair of Fields: Ampere–Maxwell
:::{present}
$$\begin{aligned} \nabla\times\mathbf{H} &= -\hat{\mathbf{x}}\ \frac{\partial H_y}{\partial z} = -\hat{\mathbf{x}}\ \frac{\beta^2 E_0}{\mu\omega}\sin(\omega t - \beta z) \\ \epsilon\frac{\partial\mathbf{E}}{\partial t} &= -\hat{\mathbf{x}}\ \epsilon\omega E_0\sin(\omega t - \beta z) \\ \beta &= \omega\sqrt{\mu\epsilon}, \qquad \frac{E_0}{H_0} = \sqrt{\frac{\mu}{\epsilon}} = \eta \end{aligned}$$
:::

The last equation is the test. With no conduction current, the Ampere–Maxwell
law requires $\nabla\times\mathbf{H} = \epsilon\ \partial\mathbf{E}/\partial t$.
The curl of $\hat{\mathbf{y}}\ H_y(z, t)$ has only the component
$-\partial H_y/\partial z$ along $\hat{\mathbf{x}}$. Both sides vary as
$\sin(\omega t - \beta z)$, so they agree at every point and time only if
their coefficients match, $\beta^2/(\mu\omega) = \epsilon\omega$. The pair of
fields therefore satisfies all four of Maxwell's equations only when
$\beta = \omega\sqrt{\mu\epsilon}$, and the ratio of the amplitudes becomes
$\mu\omega/\beta = \sqrt{\mu/\epsilon}$, the intrinsic impedance $\eta$ of
Lesson 6. In free space at 100 MHz, $\beta = 2.10$ rad/m, a wavelength of
$3.00$ m, and a field of $E_0 = 1$ V/m comes with $H_0 = 2.65$ mA/m. This
pair is a uniform plane wave, which Lessons 35 through 37 derive directly from
Maxwell's equations.
::::

::::{frame} The Ideal Transformer: Voltage
:::{present}
$$v_1 = N_1\frac{d\Phi}{dt}, \qquad v_2 = N_2\frac{d\Phi}{dt}, \qquad \frac{v_2}{v_1} = \frac{N_2}{N_1}$$
:::
:::{present}
<img src="../../viz/img/L34-transformer.svg"
     alt="A rectangular magnetic core with a winding of N1 turns on the left leg and N2 turns on the right leg, a dashed path for the core flux Phi circling through both legs, and terminal voltages v1 and v2 with currents i1 entering the left winding and i2 leaving the right"
     style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">
:::

A **transformer** is two windings on one closed core. Lesson 31 showed that a
core with $\mu_r$ in the thousands draws the magnetic field into itself, so
nearly all of the flux $\Phi$ stays in the core and passes through every turn
of both windings. We model the ideal case, in which all of the flux stays in
the core and the windings have no resistance. Each turn of winding 1 is a
closed path around the core, and Faraday's law gives a circulation of
$d\Phi/dt$ in magnitude around it. The $N_1$ turns are in series, so their
voltages add to $v_1 = N_1\ d\Phi/dt$, with the sign set by drawing the
windings so that $v_1$ and $v_2$ are positive together. Winding 2 links the
same flux, so $v_2 = N_2\ d\Phi/dt$. Dividing eliminates the flux. The voltage
ratio is the turns ratio, and it holds at every instant, whatever the shape of
the waveform, as long as the flux changes.
::::

::::{frame} The Ideal Transformer: Current
:::{present}
$$\begin{aligned} \oint_C \mathbf{H}\cdot d\mathbf{l} = H\ell_c &= N_1 i_1 - N_2 i_2 \\ N_1 i_1 - N_2 i_2 &= \frac{\Phi\ \ell_c}{\mu A} \to 0 \quad (\mu\to\infty) \\ \frac{i_2}{i_1} = \frac{N_1}{N_2}, &\qquad v_1 i_1 = v_2 i_2 \end{aligned}$$
:::

The currents come from Ampere's law around the dashed path of length
$\ell_c$ through the core. At 60 Hz the wavelength is about 5000 km, so the
displacement current in the core is negligible, and the quasi-static Ampere's
law of Lesson 29 applies. Winding 1 carries $i_1$ through the surface bounded
by the path $N_1$ times, and winding 2 carries $i_2$, drawn leaving its
positive terminal, $N_2$ times in the opposite sense. If $H$ is uniform along
the path, the circulation is $H\ell_c$. With $B = \mu H$ and $\Phi = BA$ for
a core of cross-sectional area $A$, the circulation is
$\Phi\ell_c/(\mu A)$. A finite flux needs almost no net current when $\mu$ is
very large, so in the ideal transformer the two terms balance. The current
ratio is the inverse of the turns ratio, and multiplying the two ratios shows
that the power into winding 1 equals the power out of winding 2: the ideal
transformer stores and dissipates nothing.
::::

::::{frame} Worked Example: A 120 V to 12 V Transformer
:::{present}
$N_1 = 600$, $N_2 = 60$, $6\ \Omega$ load, core area $6\ \text{cm}^2$:

$$\begin{aligned} V_2 &= 12\ \text{V}, \quad I_2 = 2\ \text{A}, \quad I_1 = 0.2\ \text{A}, \quad P = 24\ \text{W} \\ \Phi_\text{pk} &= \frac{V_\text{1,pk}}{N_1\omega} = \frac{169.7}{(600)(377)} = 0.750\ \text{mWb} \\ B_\text{pk} &= \Phi_\text{pk}/A = 1.25\ \text{T} \end{aligned}$$
:::

:::{admonition} Worked example — sizing a power transformer
:class: tip
A transformer steps a $120$ V rms, $60$ Hz line down to $12$ V rms for a
$6\ \Omega$ load. The turns ratio is $120/12 = 10$, so with $N_1 = 600$ the
secondary needs $N_2 = 60$ turns. The load draws $I_2 = 12/6 = 2$ A, the
primary draws $I_1 = 2\times60/600 = 0.2$ A, and both sides carry
$P = 24$ W.

The core must carry the flux that Faraday's law requires. With
$v_1 = V_\text{1,pk}\cos\omega t$ and $v_1 = N_1\ d\Phi/dt$, integrating gives
$\Phi = (V_\text{1,pk}/N_1\omega)\sin\omega t$, so the peak flux is
$V_\text{1,pk}/(N_1\omega)$. The peak line voltage is
$120\sqrt{2} = 169.7$ V and $\omega = 2\pi(60) = 377$ rad/s, so
$\Phi_\text{pk} = 0.750$ mWb. Through a core of area $6\ \text{cm}^2$, the
peak flux density is $1.25$ T. Silicon-steel cores saturate near $1.5$ to
$1.7$ T, above which $\mu$ falls and the ideal model fails. A $4\ \text{cm}^2$
core would need $1.88$ T, which is why the design uses the larger core or more
primary turns. The flux does not depend on the load, because $v_1$ alone sets
it.
:::
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Result |
| :-- | :-- | :-- |
| Gauss's law | Charge is the source of $\mathbf{D}$ | $\nabla\cdot\mathbf{D} = \rho_v$ |
| Gauss's law for magnetism | No magnetic charge | $\nabla\cdot\mathbf{B} = 0$ |
| Faraday's law | A changing $\mathbf{B}$ drives a circulating $\mathbf{E}$ | $\nabla\times\mathbf{E} = -\partial\mathbf{B}/\partial t$ |
| Ampere–Maxwell law | Current and a changing $\mathbf{D}$ drive $\mathbf{H}$ | $\nabla\times\mathbf{H} = \mathbf{J} + \partial\mathbf{D}/\partial t$ |
| Continuity | The set conserves charge | $\nabla\cdot\mathbf{J} = -\partial\rho_v/\partial t$ |
| Static limit | $\partial/\partial t = 0$ | The laws of Modules 2 and 3 |
| Material relations | Uniform material | $\mathbf{D} = \epsilon\mathbf{E}$, $\mathbf{B} = \mu\mathbf{H}$, $\mathbf{J} = \sigma\mathbf{E}$ |
| Induced voltage | Loop of fixed area $A$ in uniform $B(t)$ | $\vert v\vert = A\ \vert dB/dt\vert$ |
| Plane-wave pair | $\hat{\mathbf{x}}\ E$ and $\hat{\mathbf{y}}\ H$ along $z$ | $\beta = \omega\sqrt{\mu\epsilon}$, $E/H = \eta$ |
| Ideal transformer | Shared core flux | $v_2/v_1 = N_2/N_1$, $i_2/i_1 = N_1/N_2$ |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE343_L34_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE343_L34_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 35**: Maxwell's equations in phasor form, decoupled into a wave equation for $\mathbf{E}$ alone.
- **Lesson 36**: its solutions, including waves in lossy material.
:::

Today we collected Maxwell's equations, derived the point forms of the two
that change with time, and showed that the set conserves charge. The field
pair we checked was a wave traveling along $z$ at
$\omega/\beta = 1/\sqrt{\mu\epsilon}$, and we found it by guessing. Lesson 35
removes the guess: in a region with no charge or current, it writes the
equations in the phasor form of Lesson 2 and combines the two curl equations
into one wave equation for $\mathbf{E}$, the field counterpart of the
transmission-line wave equation of Lesson 4. Lesson 36 solves it.

Before Lesson 35, read sections 9.1 and 9.2 of Ellingson,
*Electromagnetics*, Vol. 1.
::::
