---
frame_view: true
---

# L25 - Boundary Conditions and Capacitance

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">Boundary Conditions and Capacitance</h1>

<div class="title-rule"></div>

Today we find the capacitance of a structure from its shape and the material inside it.

Lesson 25 · Module 2: Electrostatics · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '5'; counter-reset: lo 3">
  <li>I can apply the electric field boundary conditions to calculate electric fields on both sides of a material boundary.</li>
</ol>

:::{depth}
In circuits, a capacitor is a number printed on a part. Today we derive that
number from the fields. Any two conductors separated by an insulator store
charge when a voltage is applied between them, and the ratio of the charge to
the voltage, the **capacitance**, depends only on their shape and on the
material between them. We find it with a four-step method that uses every
tool of Module 2: the boundary condition at a conductor or Gauss's law for the
field, and the line integral of the field for the voltage. We apply it to
the parallel-plate capacitor and to the coaxial line, which finally derives
the per-unit-length capacitance $C'$ that Lesson 6 quoted for RG-58. Then a
capacitor with two dielectric layers puts the dielectric boundary condition to
work and shows why a thin air gap can break down before the rest of the
insulator.
:::
::::

::::{frame} Where We Were
:::{present}
**Lesson 24**: just outside a conductor,

$$\mathbf{E} = \hat{\mathbf{n}}\,\frac{\rho_s}{\epsilon}$$

**Lesson 22**: the voltage of point $P_2$ relative to point $P_1$ is

$$V_{21} = -\int_{P_1}^{P_2} \mathbf{E}\cdot d\mathbf{l}$$
:::

Lesson 24 found that the field next to a conductor points along the outward
normal $\hat{\mathbf{n}}$ and that its strength is the surface charge density
divided by the permittivity. Lesson 22 defined the potential difference
between two points as the work per unit charge to move a test charge from the
first to the second against the field, which is the negative of the line
integral of $\mathbf{E}$ along any path between them. A field pointing from
$P_2$ toward $P_1$ makes $V_{21}$ positive: the field runs from high potential
to low. Today we combine the two to turn a charge on a pair of conductors
into a voltage between them.
::::

::::{frame} Capacitance
:::{present}
Two conductors carry $+Q$ and $-Q$, with voltage $V$ from the negative to the positive one:

$$C = \frac{Q}{V}$$

- Double $Q$: $\mathbf{E}$ doubles, so $V$ doubles.
- $C$ depends only on the geometry and $\epsilon$.
:::

A **capacitor** is any pair of conductors that carry equal and opposite
charges, $+Q$ and $-Q$. The charges create a field between the conductors, and
the field creates a voltage $V$, the potential of the positive conductor
relative to the negative one. The **capacitance** is the ratio $C = Q/V$, in
farads. The ratio does not depend on how much charge we place. Coulomb's law
is linear, so doubling every charge doubles the field at every point, and the
line integral of a doubled field is a doubled voltage. The charge and voltage
grow together, and their ratio is fixed by the shape of the conductors, their
spacing, and the permittivity of the material between them.
::::

::::{frame} The Method
:::{present}
1. Place $+Q$ on one conductor and $-Q$ on the other.
2. Find $\mathbf{E}$ between them, from Gauss's law or the conductor boundary condition.
3. Integrate: $V = -\int_{-}^{+} \mathbf{E}\cdot d\mathbf{l}$.
4. Divide: $C = Q/V$.
:::

Every capacitance problem in this course follows the same four steps. We assume
a charge rather than a voltage because the field follows directly from the
charge: by Gauss's law when the structure has enough symmetry, or by the
boundary condition when the charge sits on a flat conductor. The voltage is the
line integral of the field from the negative conductor to the positive one;
any path gives the same answer, so we choose the one along the field lines. The
charge $Q$ then appears in both the numerator and the voltage, and it cancels
in the ratio, leaving only geometry and permittivity.
::::

::::{frame} The Parallel-Plate Capacitor
:::{present}
<img src="../../viz/img/L25-parallel-plate.svg"
     alt="Two parallel plates of area A separated by distance d and filled with a dielectric of permittivity epsilon; the top plate at z equals d carries plus Q, the bottom plate at z equals zero carries minus Q, and the field points straight down between them"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

- Plates large compared with $d$: ignore the fringing field.
:::

Two flat plates of area $A$ face each other a distance $d$ apart, with a
dielectric of permittivity $\epsilon$ between them. We put the positive plate
at $z = d$ and the negative plate at $z = 0$. Each charge spreads uniformly
over the inner face of its plate, so the surface charge densities are
$+\rho_s$ and $-\rho_s$, with $\rho_s = Q/A$. Near the edges, the field bulges
outward, an effect called **fringing**. When the plates are much wider than
they are apart, the fringing region is a small fraction of the whole, and we
treat the field between the plates as uniform.
::::

::::{frame} The Field Between the Plates
:::{present}
At the positive plate, the outward normal into the gap is $-\hat{\mathbf{z}}$:

$$\begin{aligned} \mathbf{D}\cdot\left(-\hat{\mathbf{z}}\right) &= \rho_s \\ \mathbf{D} &= -\hat{\mathbf{z}}\,\rho_s \\ \mathbf{E} &= -\hat{\mathbf{z}}\,\frac{\rho_s}{\epsilon} \end{aligned}$$
:::

Step 2 uses the conductor boundary condition from Lesson 24 at the inner face
of the top plate. The conductor is the plate, and the region outside it is the
gap below, so the outward normal points down, $-\hat{\mathbf{z}}$. The normal
component of $\mathbf{D}$ along that normal equals the surface charge density
$+\rho_s$, which makes $\mathbf{D} = -\hat{\mathbf{z}}\,\rho_s$: the field
points from the positive plate toward the negative one, as it should. The same
condition at the bottom plate, where the outward normal is $+\hat{\mathbf{z}}$
and the charge density is $-\rho_s$, gives the same $\mathbf{D}$, which
confirms the field is uniform across the gap. Dividing by $\epsilon$ gives
$\mathbf{E}$.
::::

::::{frame} Voltage and Capacitance
:::{present}
Integrate from the negative plate, $z = 0$, to the positive plate, $z = d$:

$$\begin{aligned} V &= -\int_0^d \left(-\hat{\mathbf{z}}\,\frac{\rho_s}{\epsilon}\right)\cdot\hat{\mathbf{z}}\ dz = \frac{\rho_s d}{\epsilon} \\ C &= \frac{Q}{V} = \frac{\rho_s A}{\rho_s d/\epsilon} = \frac{\epsilon A}{d} \end{aligned}$$
:::

Step 3 integrates along a straight path from the bottom plate up to the top
plate, so $d\mathbf{l} = \hat{\mathbf{z}}\ dz$. The field points down, the path
points up, and their dot product is $-\rho_s/\epsilon$; the two minus signs
cancel, and the integral over the gap of length $d$ gives a positive voltage,
$\rho_s d/\epsilon$. The positive plate is at the higher potential, as it
must be. Step 4 divides the charge, $Q = \rho_s A$, by that voltage. The
surface charge density cancels, and the capacitance is $\epsilon A/d$. A larger
plate area or a higher permittivity raises the capacitance; a wider gap lowers
it.
::::

::::{frame} Worked Example: Planes in a Circuit Board
:::{present}
Two $10 \times 10$ cm copper planes, $0.2$ mm apart in FR-4, $\epsilon_r = 4.4$:

$$C = \frac{4.4 \times 8.854 \times 10^{-12} \times 0.01}{2 \times 10^{-4}} = 1.95\ \text{nF}$$
:::

:::{admonition} Worked example — the capacitance between two planes of a circuit board
:class: tip
A four-layer circuit board places a full copper power plane directly above a
full copper ground plane. Each plane is $10\ \text{cm} \times 10\ \text{cm}$,
so $A = 0.01\ \text{m}^2$, and they are separated by $d = 0.2\ \text{mm}$ of
FR-4 fiberglass, with $\epsilon_r = 4.4$. The plates are 500 times wider than
they are apart, so fringing is negligible, and

$$C = \frac{\epsilon_r\epsilon_0 A}{d} = \frac{4.4 \times 8.854 \times 10^{-12} \times 0.01}{2 \times 10^{-4}} = 1.95 \times 10^{-9}\ \text{F} = 1.95\ \text{nF}$$

Board designers count on this capacitance. It sits directly across the power
supply of every chip on the board, with almost no inductance in series, and it
supplies the fast bursts of current that discrete bypass capacitors are too far
away to deliver.
:::
::::

::::{frame} The Coaxial Line
:::{present}
<img src="../../viz/img/L25-coax.svg"
     alt="Cross section of a coaxial line: an inner conductor of radius a carries positive charge on its surface, the shield of inner radius b carries negative charge, the dielectric of permittivity epsilon fills the space between, the field points radially outward, and a dashed Gaussian cylinder of radius rho lies between the conductors"
     style="max-width: 360px; width: 100%; display: block; margin: 0 auto;">

- Length $\ell$; charge $+\rho_\ell$ per meter on the inner conductor.
:::

Now the structure Lesson 3 introduced: an inner conductor of radius $a$
inside a shield of inner radius $b$, with a dielectric of permittivity
$\epsilon$ between them. For step 1 we place a line charge density
$+\rho_\ell$, in C/m, on the inner conductor and $-\rho_\ell$ on the shield,
over a length $\ell$, so $Q = \rho_\ell\,\ell$. The structure is the same at
every angle and every position along its axis, so the field between the
conductors can point only radially and can depend only on the distance $\rho$
from the axis. That symmetry is what lets Gauss's law find it.
::::

::::{frame} The Field From Gauss's Law
:::{present}
A Gaussian cylinder of radius $\rho$ and length $\ell$, with $a < \rho < b$:

$$\begin{aligned} \oint \mathbf{D}\cdot d\mathbf{s} &= D_\rho\left(2\pi\rho\ell\right) = \rho_\ell\,\ell \\ \mathbf{D} &= \hat{\boldsymbol{\rho}}\,\frac{\rho_\ell}{2\pi\rho} \\ \mathbf{E} &= \hat{\boldsymbol{\rho}}\,\frac{\rho_\ell}{2\pi\epsilon\rho} \end{aligned}$$
:::

Step 2 applies Gauss's law, as in Lesson 20, to a closed cylinder of radius
$\rho$ between the conductors, coaxial with them. On its curved side the
outward normal is $\hat{\boldsymbol{\rho}}$, the field is radial, and $D_\rho$
has the same value everywhere, so the flux is $D_\rho$ times the side area
$2\pi\rho\ell$. On the flat end caps the outward normal is along the axis,
perpendicular to the radial field, so they carry no flux. The enclosed charge
is the charge on the length $\ell$ of the inner conductor, $\rho_\ell\,\ell$.
The shield's charge lies outside the cylinder and does not count. Solving for
$D_\rho$ and dividing by $\epsilon$ gives a field that falls off as $1/\rho$.
::::

::::{frame} Voltage and Capacitance per Meter
:::{present}
Integrate from the shield, $\rho = b$, to the inner conductor, $\rho = a$:

$$\begin{aligned} V &= -\int_b^a \frac{\rho_\ell}{2\pi\epsilon\rho}\ d\rho = \frac{\rho_\ell}{2\pi\epsilon}\ln\frac{b}{a} \\ C &= \frac{Q}{V} = \frac{\rho_\ell\,\ell}{\frac{\rho_\ell}{2\pi\epsilon}\ln\frac{b}{a}} = \frac{2\pi\epsilon\ell}{\ln(b/a)} \\ C' &= \frac{C}{\ell} = \frac{2\pi\epsilon}{\ln(b/a)} \end{aligned}$$
:::

Step 3 integrates along a radial path from the negative conductor, the shield
at $\rho = b$, to the positive one, the inner conductor at $\rho = a$, so
$d\mathbf{l} = \hat{\boldsymbol{\rho}}\ d\rho$ with $\rho$ running from $b$
down to $a$. The integral of $1/\rho$ is $\ln\rho$, and
$-(\ln a - \ln b) = \ln(b/a)$, which is positive because $b > a$. Step 4
divides the charge on the length $\ell$ by the voltage; the line charge
density cancels. The capacitance grows in proportion to the length, because
each meter of cable is another capacitor in parallel, so the natural quantity
for a transmission line is the capacitance per meter, $C'$.
::::

::::{frame} Closing the Loop on Lesson 6
:::{present}
RG-58: $a = 0.405$ mm, $b = 1.475$ mm, $\epsilon_r = 2.25$.

$$C' = \frac{2\pi \times 2.25 \times 8.854 \times 10^{-12}}{\ln(1.475/0.405)} = \frac{1.252 \times 10^{-10}}{1.293} = 96.8\ \text{pF/m}$$

- The value [Lesson 6](../../module01/L06-reflection-vswr/index.md) quoted.
- $L'$ comes from Ampere's law in Module 3.
:::

Lesson 6 used this result for $C'$ without deriving it, and Lesson 3 used the
RG-58 numbers in the lumped-element model. Now the derivation is complete.
With the RG-58 dimensions and solid polyethylene, the numerator is
$2\pi \times 2.25 \times 8.854 \times 10^{-12} = 1.252 \times 10^{-10}$ F/m and
the logarithm is $\ln 3.642 = 1.293$, so $C' = 96.8$ pF/m, the value Lesson 6
quoted. A one-meter patch cable is a $97$ pF capacitor, which a bench LCR meter
can confirm. The other half of the characteristic impedance,
$L' = (\mu/2\pi)\ln(b/a) = 259$ nH/m, needs the magnetic field between the
conductors; Module 3 derives it from Ampere's law, and then
$Z_0 = \sqrt{L'/C'} = 51.7\ \Omega$ rests entirely on derivations from this
course.
::::

::::{frame} Two Dielectric Layers
:::{present}
<img src="../../viz/img/L25-two-layer.svg"
     alt="Parallel plates with two dielectric layers: a thin air layer of permittivity epsilon 1 and thickness d1 above a thicker glass layer of permittivity epsilon 2 and thickness d2; the field arrows are longer in the air layer than in the glass"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

- No free charge on the interface: $D_{n1} = D_{n2}$.
:::

Now the boundary conditions go to work inside a capacitor. Suppose the space
between the plates holds two layers: thickness $d_1$ with permittivity
$\epsilon_1$ and thickness $d_2$ with permittivity $\epsilon_2$, stacked
parallel to the plates. The field is normal to the interface between the
layers, and the interface carries no free charge, so the normal condition from
Lesson 24 says $\mathbf{D}$ is the same in both layers. The electric field is
not: it is $D/\epsilon$ in each layer, so it is stronger in the layer with the
smaller permittivity, as the longer arrows in the air layer show.
::::

::::{frame} Capacitors in Series
:::{present}
$$\begin{aligned} D &= \rho_s, \qquad E_1 = \frac{\rho_s}{\epsilon_1}, \qquad E_2 = \frac{\rho_s}{\epsilon_2} \\ V &= E_1 d_1 + E_2 d_2 = \rho_s\left(\frac{d_1}{\epsilon_1} + \frac{d_2}{\epsilon_2}\right) \\ C &= \frac{\rho_s A}{V} = \frac{A}{d_1/\epsilon_1 + d_2/\epsilon_2} \quad\Longleftrightarrow\quad \frac{1}{C} = \frac{1}{C_1} + \frac{1}{C_2} \end{aligned}$$
:::

The conductor condition at either plate gives $D = \rho_s$, exactly as for a
single dielectric, and the normal condition carries that same $D$ across the
interface. Dividing by each permittivity gives the field in each layer. Each
field is uniform within its layer, so the line integral from the negative
plate to the positive plate is the sum of the two fields times the two
thicknesses. Dividing the charge $\rho_s A$ by the voltage gives the
capacitance. Its reciprocal is $d_1/(\epsilon_1 A) + d_2/(\epsilon_2 A)$,
which is $1/C_1 + 1/C_2$, where $C_1$ and $C_2$ are the parallel-plate
capacitances of the two layers on their own. Two stacked layers behave as two
capacitors in series, a circuit rule that here comes from the normal boundary
condition.
::::

::::{frame} Worked Example: An Air Gap
:::{present}
$1$ mm of glass, $\epsilon_r = 5$, with a $0.1$ mm air gap; $A = 0.01\ \text{m}^2$; $V = 1$ kV.

| | No gap | With gap |
| :-- | :-- | :-- |
| $C$ | $443$ pF | $295$ pF |
| $E$ in glass | $1.0$ MV/m | $0.67$ MV/m |
| $E$ in air | — | $3.3$ MV/m |
:::

:::{admonition} Worked example — the air gap that breaks down
:class: tip
A capacitor uses a $1\ \text{mm}$ glass sheet, $\epsilon_r = 5$, between plates
of area $A = 0.01\ \text{m}^2$, charged to $1\ \text{kV}$. With the plates
pressed flat against the glass,

$$C = \frac{5\epsilon_0 A}{d} = \frac{5 \times 8.854 \times 10^{-12} \times 0.01}{10^{-3}} = 443\ \text{pF}, \qquad E = \frac{1000}{10^{-3}} = 1.0\ \text{MV/m}$$

Now one plate lifts away and leaves a $0.1\ \text{mm}$ air gap, layer 1, above
the $1\ \text{mm}$ of glass, layer 2. The sum in the denominator is

$$\frac{d_1}{\epsilon_1} + \frac{d_2}{\epsilon_2} = \frac{10^{-4}}{\epsilon_0} + \frac{10^{-3}}{5\epsilon_0} = \frac{3 \times 10^{-4}}{\epsilon_0}$$

so $C = \epsilon_0 A/(3 \times 10^{-4}) = 295$ pF. At $1$ kV the flux density is
$D = 1000\,\epsilon_0/(3 \times 10^{-4})$, and the fields are

$$E_1 = \frac{D}{\epsilon_0} = 3.3\ \text{MV/m}, \qquad E_2 = \frac{D}{5\epsilon_0} = 0.67\ \text{MV/m}$$

As a check, $3.33 \times 10^6 \times 10^{-4} + 0.667 \times 10^6 \times 10^{-3} =
333 + 667 = 1000$ V. Air breaks down near $3\ \text{MV/m}$, so the thin gap
arcs while the glass, at a third of its old field, is barely stressed. This is
why high-voltage insulation is cast or potted with no voids: an air bubble in
a good insulator carries the highest field in the part.
:::
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $C$ | Charge over voltage for two conductors | $C = Q/V$, set by geometry and $\epsilon$ |
| The method | Assume $\pm Q$, find $\mathbf{E}$, integrate for $V$, divide | |
| Parallel plates | Uniform field, fringing ignored | $C = \epsilon A/d$ |
| Coaxial line | Radial field from Gauss's law | $C' = \frac{2\pi\epsilon}{\ln(b/a)}$ |
| RG-58 | $a = 0.405$ mm, $b = 1.475$ mm, $\epsilon_r = 2.25$ | $C' = 96.8$ pF/m |
| Two layers | Same $D$ in both; capacitors in series | $C = \frac{A}{d_1/\epsilon_1 + d_2/\epsilon_2}$ |
| Air gap | The field is largest in the lowest $\epsilon$ | Air breaks down near $3$ MV/m |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE343_L25_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE343_L25_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 26**: the electrostatics lab.
- **Module 3**: magnetostatics. Ampere's law gives the coaxial $L'$, and with it $Z_0$.
:::

Today closes the theory of electrostatics. Module 2 began with Coulomb's law
for point charges, built up the field of charge distributions, found the
shortcut of Gauss's law, turned fields into potentials, carried them across
boundaries, and ended with capacitance, the circuit quantity that summarizes
all of it for a pair of conductors. Lesson 26 measures these fields and
capacitances at the bench. Module 3 then does the same work for the magnetic
field. Steady currents replace static charges, Ampere's law plays the part of
Gauss's law, and inductance plays the part of capacitance; its first payoff is
the coaxial $L'$, which completes the derivation of the characteristic
impedance.
::::
