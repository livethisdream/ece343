---
frame_view: true
---

# L4 - The Wave Equation

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">The Wave Equation</h1>

<div class="title-rule"></div>

Today we turn the telegrapher's equations into a wave equation and solve it.

Lesson 4 · Module 1: Foundations · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'">
  <li>I can describe the origin of the transmission line equation, understand the method of developing a solution, and interpret the solution.</li>
</ol>

:::{depth}
Lesson 3 ended with the telegrapher's equations: two coupled partial
differential equations for the voltage and current on a line. Today we solve
them for a sinusoidal source. Phasors from Lesson 2 replace every time
derivative with a multiplication by $j\omega$, which leaves two ordinary
differential equations in $z$. Differentiating one and substituting the other
**uncouples** them into a single **wave equation** for the voltage, and another
for the current. Its solution is a pair of waves, one traveling toward the load
and one traveling back toward the source, and the rest of Module 1 is built on
that solution.
:::
::::

::::{frame} Where We Were
:::{present}
**Lesson 3: the telegrapher's equations**

$$\begin{aligned} -\frac{\partial v(z,t)}{\partial z} &= R'\ i(z,t) + L' \frac{\partial i(z,t)}{\partial t} \\ -\frac{\partial i(z,t)}{\partial z} &= G'\ v(z,t) + C' \frac{\partial v(z,t)}{\partial t} \end{aligned}$$

**Lesson 2: phasors**

$$v(z,t) = \text{Re}\left[\widetilde{V}(z) e^{j\omega t}\right]$$
:::

Lesson 3 derived the telegrapher's equations from Kirchhoff's laws on a short
section of line. They hold for any signal, but they are coupled, and each one
contains derivatives in both $z$ and $t$. Lesson 2 gave us the tool that removes
the time derivatives. When the source is a sinusoid at frequency $\omega$, every
voltage and current on the line is a sinusoid at the same frequency, so each one
is the real part of a phasor times $e^{j\omega t}$. On a line the phasor depends
on position, so we write it $\widetilde{V}(z)$: its magnitude is the amplitude
of the sinusoid at $z$, and its angle is the phase there.
::::

::::{frame} Time Derivatives Become jω
:::{present}
$$\begin{aligned} \frac{\partial v(z,t)}{\partial t} &= \frac{\partial}{\partial t} \text{Re}\left[\widetilde{V}(z) e^{j\omega t}\right] \\ &= \text{Re}\left[\widetilde{V}(z) \frac{\partial}{\partial t} e^{j\omega t}\right] \\ &= \text{Re}\left[j\omega \widetilde{V}(z) e^{j\omega t}\right] \end{aligned}$$

- The phasor of $\partial v/\partial t$ is $j\omega \widetilde{V}(z)$.
- The phasor of $\partial v/\partial z$ is $d\widetilde{V}/dz$.
:::

We take the derivative of $v(z,t)$ with respect to time. Taking the real part
and differentiating with respect to $t$ commute, because $t$ is real, so we can
move the derivative inside. The phasor $\widetilde{V}(z)$ does not depend on
time, so the derivative acts only on $e^{j\omega t}$, which brings down a factor
of $j\omega$. The result is again the real part of a phasor times
$e^{j\omega t}$, and that phasor is $j\omega\widetilde{V}(z)$. Differentiating
in time is the same as multiplying the phasor by $j\omega$.

The derivative with respect to $z$ works the other way. Now $e^{j\omega t}$ does
not depend on $z$, so the derivative acts only on $\widetilde{V}(z)$. Because
the phasor depends on $z$ alone, its derivative is an ordinary derivative,
$d\widetilde{V}/dz$, not a partial one.
::::

::::{frame} The Telegrapher's Equations in Phasor Form
:::{present}
$$\begin{aligned} -\frac{d\widetilde{V}(z)}{dz} &= R'\ \widetilde{I}(z) + j\omega L'\ \widetilde{I}(z) = \left(R' + j\omega L'\right)\widetilde{I}(z) \\ -\frac{d\widetilde{I}(z)}{dz} &= G'\ \widetilde{V}(z) + j\omega C'\ \widetilde{V}(z) = \left(G' + j\omega C'\right)\widetilde{V}(z) \end{aligned}$$
:::

We replace each quantity in the telegrapher's equations with its phasor: $v$
with $\widetilde{V}$, $i$ with $\widetilde{I}$, each $\partial/\partial t$ with
$j\omega$, and each $\partial/\partial z$ with $d/dz$. In the first equation the
two terms on the right both multiply $\widetilde{I}(z)$, so we factor it out;
in the second, both multiply $\widetilde{V}(z)$. The factor
$R' + j\omega L'$ is the series impedance of the line per meter, and
$G' + j\omega C'$ is its shunt admittance per meter. The equations are still
coupled, but they are now ordinary differential equations in one variable,
$z$, with constant coefficients.
::::

::::{frame} Uncoupling the Voltage
:::{present}
$$\begin{aligned} -\frac{d^2\widetilde{V}(z)}{dz^2} &= \left(R' + j\omega L'\right)\frac{d\widetilde{I}(z)}{dz} \\ &= -\left(R' + j\omega L'\right)\left(G' + j\omega C'\right)\widetilde{V}(z) \end{aligned}$$

$$\frac{d^2\widetilde{V}(z)}{dz^2} - \gamma^2\ \widetilde{V}(z) = 0, \qquad \gamma^2 = \left(R' + j\omega L'\right)\left(G' + j\omega C'\right)$$
:::

To get an equation in $\widetilde{V}$ alone, we differentiate the first
phasor equation with respect to $z$. The left side becomes the second
derivative of $\widetilde{V}$, and on the right the constant
$R' + j\omega L'$ stays outside the derivative, leaving $d\widetilde{I}/dz$.
The second phasor equation says exactly what $d\widetilde{I}/dz$ is:
$-\left(G' + j\omega C'\right)\widetilde{V}(z)$. Substituting it removes the
current entirely. Multiplying both sides by $-1$ and moving everything to the
left gives the **wave equation** for the voltage. We name the product of the
series impedance and the shunt admittance $\gamma^2$, because the solution
depends on its square root.
::::

::::{frame} The Propagation Constant
:::{present}
$$\gamma = \sqrt{\left(R' + j\omega L'\right)\left(G' + j\omega C'\right)} = \alpha + j\beta$$

| Part | Name | Units |
| :-- | :-- | :-- |
| $\gamma$ | propagation constant | 1/m |
| $\alpha$ | attenuation constant | Np/m |
| $\beta$ | phase constant | rad/m |
:::

The square root $\gamma$ is the **propagation constant**. It is complex,
because the series impedance and the shunt admittance are complex, so we write
it as a real part $\alpha$ and an imaginary part $\beta$. A square root has two
values that differ only in sign; we choose the root with $\alpha \ge 0$ and
$\beta > 0$, and the solution below carries both signs anyway. The units of
$\gamma$ are inverse meters, since $\gamma z$ must be dimensionless. We mark
the real part in **nepers** per meter and the imaginary part in **radians** per
meter to keep track of what each one does: the solution will show that $\alpha$
sets how fast the wave decays and $\beta$ sets how fast its phase changes.
Lesson 5 computes both for a real cable.
::::

::::{frame} The Current Obeys the Same Equation
:::{present}
$$\begin{aligned} -\frac{d^2\widetilde{I}(z)}{dz^2} &= \left(G' + j\omega C'\right)\frac{d\widetilde{V}(z)}{dz} \\ &= -\left(G' + j\omega C'\right)\left(R' + j\omega L'\right)\widetilde{I}(z) \end{aligned}$$

$$\frac{d^2\widetilde{I}(z)}{dz^2} - \gamma^2\ \widetilde{I}(z) = 0$$
:::

The same three steps uncouple the current. We differentiate the second phasor
equation with respect to $z$, substitute the first equation for
$d\widetilde{V}/dz$, and rearrange. The product of the two factors is the same
$\gamma^2$, because multiplication does not depend on order, so the current
obeys exactly the same wave equation as the voltage. The two equations are now
**uncoupled**: each one contains a single unknown function.
::::

::::{frame} Solving the Wave Equation
:::{present}
Assume $\widetilde{V}(z) = A e^{sz}$:

$$\begin{aligned} s^2 A e^{sz} - \gamma^2 A e^{sz} &= 0 \\ s^2 - \gamma^2 &= 0 \\ s &= \pm\gamma \end{aligned}$$
:::

The wave equation is a second-order linear differential equation with
constant coefficients, the same kind of equation that describes an RLC circuit
in time. We solve it the same way. We assume a solution of the form
$A e^{sz}$, because the derivative of an exponential is the same exponential
times a constant. Each derivative brings down a factor of $s$, so the second
derivative is $s^2 A e^{sz}$. Substituting into the wave equation, the factor
$A e^{sz}$ appears in both terms and is never zero, so we can divide it out.
What remains is the **characteristic equation**, $s^2 - \gamma^2 = 0$, and its
two roots are $s = +\gamma$ and $s = -\gamma$.
::::

::::{frame} The General Solution
:::{present}
$$\begin{aligned} \widetilde{V}(z) &= V_0^+ e^{-\gamma z} + V_0^- e^{+\gamma z} \\ \widetilde{I}(z) &= I_0^+ e^{-\gamma z} + I_0^- e^{+\gamma z} \end{aligned}$$

- $V_0^\pm$ and $I_0^\pm$ are complex constants.
- The source and the load set them; Lesson 5 relates $I_0^\pm$ to $V_0^\pm$.
:::

Each root gives one solution, and because the wave equation is linear, any sum
of solutions is also a solution. A second-order equation has exactly two
independent solutions, so the **general solution** is the sum of the two, each
with its own constant. We name the constants $V_0^+$ and $V_0^-$ for reasons the
next two frames make clear. The current has the same form with its own
constants, $I_0^+$ and $I_0^-$. The four constants are not independent: the
current and voltage must still satisfy the first-order phasor equations, and
Lesson 5 uses that to find $I_0^\pm$ from $V_0^\pm$. The source and load set
the rest, which is the subject of Lesson 6.
::::

::::{frame} Back to the Time Domain
:::{present}
With $\gamma = \alpha + j\beta$ and $V_0^\pm = \left\vert V_0^\pm\right\vert e^{j\phi^\pm}$:

$$\begin{aligned} v(z,t) &= \text{Re}\left[\widetilde{V}(z) e^{j\omega t}\right] \\ &= \text{Re}\left[\left\vert V_0^+\right\vert e^{j\phi^+} e^{-\alpha z} e^{-j\beta z} e^{j\omega t} + \left\vert V_0^-\right\vert e^{j\phi^-} e^{\alpha z} e^{j\beta z} e^{j\omega t}\right] \\ &= \left\vert V_0^+\right\vert e^{-\alpha z} \cos\left(\omega t - \beta z + \phi^+\right) + \left\vert V_0^-\right\vert e^{\alpha z} \cos\left(\omega t + \beta z + \phi^-\right) \end{aligned}$$
:::

To see what the solution looks like on the line, we return to the time domain:
multiply the phasor by $e^{j\omega t}$ and take the real part. We write each
complex constant as a magnitude and a phase, and split each exponential
$e^{\mp\gamma z}$ into a real part $e^{\mp\alpha z}$ and an imaginary part
$e^{\mp j\beta z}$. The real exponentials and the magnitudes are real numbers,
so they come outside the real part. The remaining imaginary exponentials
combine into a single $e^{j(\cdot)}$, and the real part of $e^{j\theta}$ is
$\cos\theta$. The result is two sinusoids, each multiplied by an exponential in
$z$.
::::

::::{frame} Which Way Each Wave Travels
:::{present}
- Constant $\omega t - \beta z$: as $t$ grows, $z$ grows. The first term travels toward the load.
- Constant $\omega t + \beta z$: the second term travels toward the source.
- Each decays in its own direction of travel.
:::

A crest of the first term sits wherever its cosine argument
$\omega t - \beta z + \phi^+$ is zero. Solving for its position gives
$z = (\omega t + \phi^+)/\beta$, which grows as $t$ grows, so the crest moves in
the $+z$ direction. Every point of constant phase does the same, so the whole
first term is a wave traveling toward the load, and its amplitude
$\left\vert V_0^+\right\vert e^{-\alpha z}$ shrinks as it goes. That is why we
named its constant $V_0^+$. In the second term the crest sits at
$z = -(\omega t + \phi^-)/\beta$, which moves in the $-z$ direction, toward the
source; its amplitude $\left\vert V_0^-\right\vert e^{\alpha z}$ shrinks as $z$
decreases, so this wave also decays in its own direction of travel. The voltage
on any line is the sum of an **incident** wave and a **reflected** wave.
::::

::::{frame} The Two Waves
:class: viz-frame

:::{present}
<iframe src="../../viz/traveling-waves.html"
        width="100%" height="474"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="The forward and backward traveling waves of the general solution, with attenuation, and their sum"
        data-autosize>
</iframe>
:::

The widget plots the two terms of the solution over three wavelengths, with
$\left\vert V_0^+\right\vert = 1$. The dots ride one crest of each wave so you
can see which way it moves. Start with no backward wave and set $\alpha\lambda$
to zero: the forward wave moves to the right at constant amplitude. Raise
$\alpha\lambda$, the attenuation over one wavelength, and the wave shrinks as it
travels; at $\alpha\lambda = 0.1$ Np it loses $0.87$ dB per wavelength and
reaches $0.74$ of its starting amplitude after three. Now raise
$\left\vert V_0^-\right\vert$: the backward wave enters from the right and
shrinks as it travels left. The sum, in blue, no longer looks like a single
traveling wave. Lesson 6 shows that the sum forms a standing wave, and that the
load sets the size of the backward wave.
::::

::::{frame} The Lossless Line
:::{present}
Set $R' = 0$ and $G' = 0$:

$$\begin{aligned} \gamma &= \sqrt{\left(j\omega L'\right)\left(j\omega C'\right)} = \sqrt{-\omega^2 L'C'} = j\omega\sqrt{L'C'} \\ \alpha &= 0, \qquad \beta = \omega\sqrt{L'C'} \end{aligned}$$

- RG-58 at 100 MHz: $\beta = 3.15$ rad/m.
:::

On a lossless line the product under the square root is $j^2\omega^2 L'C'$,
which is a negative real number. Its square root is purely imaginary, so the
attenuation constant is zero and the phase constant is $\omega\sqrt{L'C'}$.
Both waves travel without decaying. For RG-58, with $L' = 259$ nH/m and
$C' = 96.8$ pF/m from Lesson 3, at 100 MHz,

$$\beta = 2\pi \times 10^8 \sqrt{259 \times 10^{-9} \times 96.8 \times 10^{-12}} = 2\pi \times 10^8 \times 5.01 \times 10^{-9} = 3.15\ \text{rad/m}$$

so the phase changes by one full cycle, $2\pi$ radians, every
$2\pi/3.15 = 2.0$ m. That is the 2 m wavelength Lesson 3 found for this cable
at 100 MHz, now derived from $L'$ and $C'$.
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Phasor rule | Time derivative becomes multiplication by $j\omega$ | $\partial/\partial t \to j\omega$ |
| Phasor telegrapher's equations | Series impedance and shunt admittance per meter | $R' + j\omega L'$, $G' + j\omega C'$ |
| Wave equation | Uncoupled by differentiating one equation and substituting the other | $\frac{d^2\widetilde{V}}{dz^2} - \gamma^2\widetilde{V} = 0$ |
| $\gamma = \alpha + j\beta$ | Propagation constant: attenuation and phase constants | $\gamma^2 = (R' + j\omega L')(G' + j\omega C')$ |
| Characteristic equation | From the trial solution $Ae^{sz}$ | $s = \pm\gamma$ |
| General solution | Incident plus reflected wave | $V_0^+ e^{-\gamma z} + V_0^- e^{+\gamma z}$ |
| Lossless line | No attenuation | $\alpha = 0$, $\beta = \omega\sqrt{L'C'}$ |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE343_L04_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE343_L04_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 5**: relate the current to the voltage, which defines $Z_0$, and read the speed, wavelength, and loss out of $\gamma$.
- **Lesson 6**: the load sets $V_0^-$.
:::

Today we solved the wave equation and found that the voltage on any line is the
sum of two traveling waves. Two questions remain before we can use the
solution. The first is how the current in each wave relates to its voltage; the
answer is the characteristic impedance $Z_0$, which Lesson 5 derives from the
phasor equations. The second is what the propagation constant means in
numbers: how fast the wave travels, how long a wavelength is, and how much a
real cable attenuates it. Lesson 5 answers both, and Lesson 6 then terminates
the line in a load and finds the reflected wave.

Before Lesson 5, read sections 3.7 through 3.9 of Ellingson,
*Electromagnetics*, Vol. 1.
::::
