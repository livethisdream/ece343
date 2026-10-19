---
frame_view: true
---

# L6 - Coaxial Lines, Reflection Coefficient, and VSWR

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">Coaxial Lines, Reflection Coefficient, and VSWR</h1>

<div class="title-rule"></div>

Today we terminate the line and find out how much of the wave comes back.

Lesson 6 · Module 1: Foundations · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 1">
  <li>I can explain the physical meaning of and calculate the following quantities: propagation constant, phase constant, attenuation constant, characteristic impedance, VSWR, reflection coefficient, and transmission coefficient.</li>
  <li>I can use the transmission line equation to calculate the voltage/current at an arbitrary point on a specified transmission line.</li>
</ol>

:::{depth}
Lesson 5 gave us a wave on an infinitely long line, described by its
propagation constant and its characteristic impedance. Real lines end, and
whatever sits at the end decides what happens next. Today we compute the
characteristic impedance of the most common real line, coaxial cable, and then
terminate a line in a load. The load sets the **reflection coefficient**, the
ratio of the wave that comes back to the wave that arrived. The incident and
reflected waves add along the line to form a **standing wave**, and the ratio of
its largest voltage to its smallest, the **VSWR**, is the number every
datasheet and every network analyzer quotes for a match.
:::
::::

::::{frame} Where We Were
:::{present}
**Lessons 4 and 5: the wave solution** on a lossless line, $\gamma = j\beta$:

$$\begin{aligned} \widetilde{V}(z) &= V_0^+ e^{-j\beta z} + V_0^- e^{+j\beta z} \\ \widetilde{I}(z) &= \frac{V_0^+}{Z_0} e^{-j\beta z} - \frac{V_0^-}{Z_0} e^{+j\beta z} \end{aligned}$$

$$Z_0 = \sqrt{\frac{L'}{C'}}$$
:::

Lesson 4 solved the telegrapher's equations, and Lesson 5 read the physics out
of the solution. On a lossless line the voltage is the sum of two waves: one
with amplitude $V_0^+$ traveling in the $+z$ direction, toward the load, and
one with amplitude $V_0^-$ traveling in the $-z$ direction, back toward the
source. Each wave carries a current equal to its voltage divided by the
**characteristic impedance** $Z_0$. The minus sign on the second current term
appears because the backward wave carries its current in the $-z$ direction.
Until today, nothing set the size of $V_0^-$. The load does.
::::

::::{frame} The Coaxial Line
:::{present}
For inner radius $a$, outer radius $b$, and dielectric permittivity $\epsilon$:

$$\begin{aligned} L' &= \frac{\mu}{2\pi} \ln\frac{b}{a} \\ C' &= \frac{2\pi\epsilon}{\ln(b/a)} \\ Z_0 &= \frac{\eta}{2\pi} \ln\frac{b}{a} \approx \frac{60\ \Omega}{\sqrt{\epsilon_r}} \ln\frac{b}{a} \end{aligned}$$
:::

Lesson 3 introduced the coaxial line, an inner conductor of radius $a$ inside
a shield of radius $b$, and quoted its per-unit-length inductance and
capacitance. Deriving them requires the fields between the conductors:
Lesson 25 derives $C'$ from Gauss's law, and Module 3 derives $L'$ from
Ampere's law. Here we use the results. The inductance comes from the
magnetic field that circles the inner conductor, and the capacitance comes from
the radial electric field between the conductors, so both depend only on the
ratio $b/a$ and on the material between them.

Dividing the two and taking the square root gives the characteristic
impedance. The $\eta$ in that result is the wave impedance of the dielectric,
$\eta = \eta_0/\sqrt{\epsilon_r}$ with $\eta_0 \approx 377\ \Omega$, and for a
nonmagnetic dielectric the expression simplifies to the $60\ \Omega$ form.
Because $Z_0$ depends on the logarithm of $b/a$, it changes slowly with the
dimensions: doubling $b/a$ adds only $41.6\ \Omega/\sqrt{\epsilon_r}$.
::::

::::{frame} Worked Example: RG-58
:::{present}
| Quantity | Value |
| :-- | :-- |
| $a$, $b$ | $0.405\ \text{mm}$, $1.475\ \text{mm}$ |
| $\epsilon_r$ (polyethylene) | $2.25$ |
| $Z_0$ | $51.7\ \Omega$ |
| $L'$, $C'$ | $259\ \text{nH/m}$, $96.8\ \text{pF/m}$ |
| $v_p$ | $2.0 \times 10^8$ m/s |
:::

:::{admonition} Worked example — the characteristic impedance of RG-58
:class: tip
RG-58 has an inner conductor of radius $a = 0.405\ \text{mm}$ and a solid
polyethylene dielectric, $\epsilon_r = 2.25$, out to $b = 1.475\ \text{mm}$.
The ratio and its logarithm are

$$\ln\frac{b}{a} = \ln\frac{1.475}{0.405} = \ln 3.64 = 1.293$$

so the characteristic impedance is

$$Z_0 = \frac{60}{\sqrt{2.25}} \times 1.293 = 40 \times 1.293 = 51.7\ \Omega$$

which is why the cable is sold as $50\ \Omega$ line. The per-unit-length values
are

$$\begin{aligned} L' &= \frac{4\pi \times 10^{-7}}{2\pi} \times 1.293 = 259\ \text{nH/m} \\ C' &= \frac{2\pi \times 2.25 \times 8.854 \times 10^{-12}}{1.293} = 96.8\ \text{pF/m} \end{aligned}$$

and the phase velocity is

$$v_p = \frac{1}{\sqrt{L'C'}} = \frac{c}{\sqrt{\epsilon_r}} = \frac{3 \times 10^8}{1.5} = 2.0 \times 10^8\ \text{m/s}$$

These are the RG-58 numbers Lesson 3 used.
:::
::::

::::{frame} Terminating the Line
:::{present}
At the load, $z = 0$, every exponential equals one:

$$\begin{aligned} \widetilde{V}(0) &= V_0^+ + V_0^- \\ \widetilde{I}(0) &= \frac{V_0^+ - V_0^-}{Z_0} \\ Z_L = \frac{\widetilde{V}(0)}{\widetilde{I}(0)} &= Z_0 \frac{V_0^+ + V_0^-}{V_0^+ - V_0^-} \end{aligned}$$
:::

Now we connect a load impedance $Z_L$ at $z = 0$, the convention from Lesson 3.
The load obeys Ohm's law: the voltage across it divided by the current through
it is $Z_L$. That voltage and current are the line's voltage and current at
$z = 0$, where every exponential in the wave solution equals one. So the load
fixes a relationship between the two wave amplitudes. A single incident wave,
with $V_0^- = 0$, has a voltage-to-current ratio of exactly $Z_0$, so it can
satisfy the load only when $Z_L = Z_0$. For any other load, a reflected wave
must appear to make the ratio come out right.
::::

::::{frame} The Reflection Coefficient
:::{present}
$$\begin{aligned} Z_L \left(V_0^+ - V_0^-\right) &= Z_0 \left(V_0^+ + V_0^-\right) \\ V_0^+ \left(Z_L - Z_0\right) &= V_0^- \left(Z_L + Z_0\right) \\ \Gamma = \frac{V_0^-}{V_0^+} &= \frac{Z_L - Z_0}{Z_L + Z_0} \end{aligned}$$

- $\Gamma$ is complex: a magnitude $\vert\Gamma\vert$ and a phase $\theta_\Gamma$.
- For any passive load, $\vert\Gamma\vert \le 1$.
:::

To solve the boundary condition for the ratio of the amplitudes, we multiply
both sides by $V_0^+ - V_0^-$, collect the $V_0^+$ terms on the left and the
$V_0^-$ terms on the right, and divide. The result is the **reflection
coefficient** $\Gamma$, the ratio of the reflected voltage wave to the incident
one at the load. It depends only on the load and the line, not on the source or
the length of the line. Because $Z_L$ can be complex, so can $\Gamma$. We write
it as a magnitude and a phase, $\Gamma = \vert\Gamma\vert e^{j\theta_\Gamma}$,
where $\vert\Gamma\vert$ says how much of the wave comes back and
$\theta_\Gamma$ says how far the reflected wave is shifted in phase. A passive
load cannot return more power than it receives, so $\vert\Gamma\vert$ never
exceeds one.
::::

::::{frame} Special Loads
:::{present}
| Load | $\Gamma$ | What happens |
| :-- | :-- | :-- |
| Matched, $Z_L = Z_0$ | $0$ | no reflection |
| Short, $Z_L = 0$ | $-1$ | full reflection, inverted |
| Open, $Z_L \to \infty$ | $+1$ | full reflection, in phase |
| Pure reactance, $Z_L = jX$ | $\vert\Gamma\vert = 1$ | full reflection, phase shifted |
:::

Four loads are worth knowing by heart. A **matched** load absorbs the whole
incident wave, and nothing reflects. A **short circuit** forces the voltage at
the load to zero, so the reflected wave must cancel the incident one exactly:
$\Gamma = -1$. An **open circuit** forces the current to zero, so the reflected
voltage adds to the incident voltage: $\Gamma = +1$. A **pure reactance**
stores energy but cannot dissipate any, so it returns all of it; the magnitude
is one, and only the phase depends on $X$. Every other load falls somewhere
between these cases.
::::

::::{frame} Worked Example: Two Loads on a 50 Ω Line
:::{present}
$$\begin{aligned} Z_L = 125\ \Omega: \quad \Gamma &= \frac{125 - 50}{125 + 50} = 0.429 \\ Z_L = 50 + j50\ \Omega: \quad \Gamma &= \frac{j50}{100 + j50} = 0.2 + j0.4 = 0.447\angle 63.4^\circ \end{aligned}$$
:::

:::{admonition} Worked example — a resistive load and a complex load
:class: tip
A $125\ \Omega$ resistor terminates a $50\ \Omega$ line. The reflection
coefficient is real and positive, because the load is a larger resistance than
$Z_0$:

$$\Gamma = \frac{125 - 50}{125 + 50} = \frac{75}{175} = 0.429$$

Now replace the resistor with $Z_L = 50 + j50\ \Omega$. The numerator is
$Z_L - Z_0 = j50$, and multiplying through by the conjugate of the denominator
gives

$$\Gamma = \frac{j50}{100 + j50} = \frac{j50\ (100 - j50)}{100^2 + 50^2} = \frac{2500 + j5000}{12{,}500} = 0.2 + j0.4$$

In polar form, $\vert\Gamma\vert = \sqrt{0.2^2 + 0.4^2} = 0.447$ and
$\theta_\Gamma = \tan^{-1}(0.4/0.2) = 63.4^\circ$. The resistive part of this
load matches the line, but the reactance alone reflects 20% of the power.
:::
::::

::::{frame} The Transmission Coefficient
:::{present}
The voltage that reaches the load is the incident plus the reflected wave:

$$\widetilde{V}(0) = V_0^+(1 + \Gamma) \quad\Longrightarrow\quad \tau = 1 + \Gamma$$

- $125\ \Omega$ load: $\tau = 1.429$.
:::

The **transmission coefficient** $\tau$ is the ratio of the voltage across the
load to the incident voltage. At $z = 0$ the load voltage is the sum of the two
waves, so $\tau = 1 + \Gamma$. For the $125\ \Omega$ load, $\tau = 1.429$: the
load voltage is 43% larger than the incident voltage. That is not a power gain.
The load current is smaller than the incident current by a larger factor,
because the reflected current subtracts, and the power delivered to the load is
less than the incident power. On a short circuit, $\tau = 0$; on an open
circuit, $\tau = 2$, and the voltage at the open end doubles.
::::

::::{frame} The Voltage Along the Line
:::{present}
Substitute $V_0^- = \Gamma V_0^+$ into the wave solution:

$$\begin{aligned} \widetilde{V}(z) &= V_0^+ \left(e^{-j\beta z} + \Gamma e^{+j\beta z}\right) \\ \left\vert\widetilde{V}(z)\right\vert &= \left\vert V_0^+\right\vert\ \left\vert 1 + \Gamma e^{j2\beta z} \right\vert \end{aligned}$$
:::

With $\Gamma$ known, one amplitude describes the whole line. Factoring
$e^{-j\beta z}$ out of the sum, whose magnitude is one, leaves the magnitude of
the voltage at any point. The term $\Gamma e^{j2\beta z}$ is the
**reflection coefficient at position $z$**: the ratio of the reflected wave to
the incident wave there, which has the same magnitude as $\Gamma$ everywhere on
a lossless line but rotates in phase by $2\beta z$, twice the phase delay to the
load, because the reflected wave travels to the load and back. Where that term
points in the same direction as one, the two waves add; where it points
opposite, they subtract.
::::

::::{frame} The Standing Wave
:::{present}
With $\Gamma = \vert\Gamma\vert e^{j\theta_\Gamma}$:

$$\begin{aligned} \left\vert 1 + \Gamma e^{j2\beta z} \right\vert^2 &= \left(1 + \Gamma e^{j2\beta z}\right)\left(1 + \Gamma^* e^{-j2\beta z}\right) \\ &= 1 + \vert\Gamma\vert^2 + 2\vert\Gamma\vert\cos\left(\theta_\Gamma + 2\beta z\right) \end{aligned}$$

$$V_\text{max} = \left\vert V_0^+\right\vert (1 + \vert\Gamma\vert), \qquad V_\text{min} = \left\vert V_0^+\right\vert (1 - \vert\Gamma\vert)$$

- Maxima are $\lambda/2$ apart; each minimum is $\lambda/4$ from a maximum.
:::

To find how the magnitude varies, we square it, which turns it into the
product of the term and its complex conjugate. Multiplying out, the two cross
terms are complex conjugates of each other, and a number plus its conjugate is
twice its real part, which gives the cosine. The cosine swings between $+1$ and
$-1$, so the squared magnitude swings between
$1 + \vert\Gamma\vert^2 + 2\vert\Gamma\vert = (1 + \vert\Gamma\vert)^2$, where the
two waves are in phase, and $(1 - \vert\Gamma\vert)^2$, where they are out of
phase. Taking square roots gives $V_\text{max}$ and $V_\text{min}$. The
pattern does not move along the line, which is why it is called a **standing wave**. The phase
$2\beta z$ changes by $2\pi$ over half a wavelength, so the maxima repeat every
$\lambda/2$, and each minimum sits halfway between two maxima, a quarter
wavelength from each. On a matched line, $\Gamma = 0$, and the voltage
magnitude is the same everywhere. On a short or an open, $\vert\Gamma\vert = 1$,
and the minima fall all the way to zero.
::::

::::{frame} The Standing Wave on a Loaded Line
:class: viz-frame

:::{present}
<iframe src="../../viz/load-standing-wave.html"
        width="100%" height="489"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Standing wave on a 50 ohm line terminated in a load set by its resistance and reactance"
        data-autosize>
</iframe>
:::

The widget drives a $50\ \Omega$ line with a load whose resistance $R_L$ and
reactance $X_L$ you set with the two sliders. The dashed curves are the
envelope $\vert\widetilde{V}\vert$, and the solid curve is the voltage at one
instant; turn on **Animate** to watch it move inside the envelope, and turn on
**Forward + reflected** to see the two waves it is made of. Start with the
$125\ \Omega$ load and confirm $\Gamma = 0.43$ and a VSWR of 2.5, with a
maximum at the load. Then set $X_L = +50\ \Omega$ and $R_L = 50\ \Omega$:
$\vert\Gamma\vert$ and the VSWR change, and the whole pattern slides toward
the source until the first maximum sits $0.088\lambda$ from the load. Set
$R_L = 0$ and $X_L = 0$ for a short circuit, and the minima drop to zero, with
one at the load.
::::

::::{frame} Voltage Standing Wave Ratio
:::{present}
$$\text{VSWR} = \frac{V_\text{max}}{V_\text{min}} = \frac{1 + \vert\Gamma\vert}{1 - \vert\Gamma\vert}, \qquad \vert\Gamma\vert = \frac{\text{VSWR} - 1}{\text{VSWR} + 1}$$

- Matched: VSWR $= 1$. Short, open, or reactance: VSWR $\to \infty$.
- $125\ \Omega$ on $50\ \Omega$: VSWR $= 2.5$.
:::

The **voltage standing wave ratio** is the ratio of the largest voltage on the
line to the smallest. It carries the same information as $\vert\Gamma\vert$ but
was historically easier to measure: slide a probe along a slotted line and
read the maximum and minimum. It runs from one, for a perfect match, to
infinity, for a load that reflects everything. For the $125\ \Omega$ load,

$$\text{VSWR} = \frac{1 + 0.429}{1 - 0.429} = \frac{1.429}{0.571} = 2.5$$

which equals $125/50$. For any real load, VSWR is the larger of $Z_L/Z_0$ and
$Z_0/Z_L$, a quick check worth remembering. VSWR discards the phase of
$\Gamma$, so two different loads can share a VSWR and still behave differently
along the line.
::::

::::{frame} Where the Maximum Falls
:::{present}
The first voltage maximum toward the source is where $2\beta d = \theta_\Gamma$:

$$d_\text{max} = \frac{\theta_\Gamma}{4\pi}\lambda$$

- $50 + j50\ \Omega$: $d_\text{max} = \frac{63.4^\circ}{720^\circ}\lambda = 0.088\lambda$.
- First minimum: $0.088\lambda + 0.25\lambda = 0.338\lambda$.
:::

The phase of $\Gamma$ sets where the pattern sits. Measure distance from the
load toward the source as $d = -z$. The waves add in phase where the phase of
$\Gamma e^{-j2\beta d}$ is zero, so the first maximum sits at
$2\beta d_\text{max} = \theta_\Gamma$, with $\theta_\Gamma$ taken between $0$
and $2\pi$. A real load larger than $Z_0$ has $\theta_\Gamma = 0$ and a maximum
right at the load; a real load smaller than $Z_0$ has
$\theta_\Gamma = 180^\circ$ and a minimum there instead. For the
$50 + j50\ \Omega$ load the maximum sits $0.088\lambda$ from the load. Measuring
the VSWR and the position of the minimum was the classic way to find an unknown
load impedance before network analyzers.
::::

::::{frame} How Much Power Comes Back
:::{present}
Reflected fraction: $\vert\Gamma\vert^2$. Delivered fraction: $1 - \vert\Gamma\vert^2$.

| VSWR | $\vert\Gamma\vert$ | Reflected power |
| :-- | :-- | :-- |
| 1.5 | 0.20 | 4.0% |
| 2.0 | 0.33 | 11.1% |
| 2.5 | 0.43 | 18.4% |
| 3.0 | 0.50 | 25.0% |
:::

Power goes as voltage squared, so the fraction of the incident power that
reflects is $\vert\Gamma\vert^2$, and the fraction the load absorbs is
$1 - \vert\Gamma\vert^2$. The $125\ \Omega$ load reflects
$0.429^2 = 18.4\%$ of the incident power and absorbs the other 81.6%. The table
gives a sense of scale. A VSWR of 1.5 reflects only 4% of the power, and most
equipment specifications treat 2:1 as the edge of acceptable. Beyond that, the
load wastes the reflected power, and in a transmitter that power returns to the amplifier,
which may not tolerate it. The **rule of thumb** is that VSWR below 2 is a good
match for most purposes.
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Coaxial $Z_0$ | Set by $\ln(b/a)$ and the dielectric | RG-58: $51.7\ \Omega$ |
| $\Gamma$ | Reflected over incident voltage at the load | $\frac{Z_L - Z_0}{Z_L + Z_0}$ |
| Special loads | Matched, short, open, reactive | $0$, $-1$, $+1$, $\vert\Gamma\vert = 1$ |
| $\tau$ | Load voltage over incident voltage | $1 + \Gamma$ |
| Standing wave | Incident plus reflected; maxima $\lambda/2$ apart | $V_\text{max}$, $V_\text{min} = \vert V_0^+\vert (1 \pm \vert\Gamma\vert)$ |
| VSWR | $V_\text{max}/V_\text{min}$ | $\frac{1 + \vert\Gamma\vert}{1 - \vert\Gamma\vert}$; below 2 is good |
| First maximum | Set by the phase of $\Gamma$ | $d_\text{max} = \frac{\theta_\Gamma}{4\pi}\lambda$ |
| Reflected power | Fraction of incident power returned | $\vert\Gamma\vert^2$ |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE343_L06_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE343_L06_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 7**: the impedance seen looking into a terminated line, at any distance from the load.
- **Lessons 8 and 9**: choose the line length to transform a load into a match.
:::

Today the load set $\Gamma$, and $\Gamma$ set the standing wave. The same
standing wave means the ratio of voltage to current changes along the line, so
a source connected at a distance $\ell$ from the load does not see $Z_L$. It
sees a transformed impedance that depends on $\ell$. Lesson 7 derives that
**input impedance** and works the special cases: the shorted line, the open
line, and the quarter-wave line. Lessons 8 and 9 turn the transformation into a
design tool for matching, and Lessons 10 through 13 do the same work
graphically on the Smith chart, which is a plot of $\Gamma$.

Before Lesson 7, read sections 3.15 and 3.17 through 3.19 of Ellingson,
*Electromagnetics*, Vol. 1.
::::
