---
frame_view: true
---

# L28 - Magnetic Fields and Gauss's Law for Magnetism

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">Magnetic Fields and Gauss's Law for Magnetism</h1>

<div class="title-rule"></div>

Today we find the magnetic field of a current, and show that its field lines always close.

Lesson 28 · Module 3: Magnetostatics · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '7'">
  <li>I can apply the Biot-Savart law to simple magnetostatic systems to find the magnetic field at an observation point.</li>
  <li>I can articulate the meaning of both the integral form and point form of Gauss's Law for magnetism.</li>
</ol>

:::{depth}
Module 2 started from one experimental law, Coulomb's law, and built the
electric field of any arrangement of charge. Module 3 does the same for steady
currents. Today we define the magnetic field by the force it exerts on a moving
charge, write the **Biot-Savart law** for the field of a small piece of
current, and integrate it for a straight wire of finite length and for a
circular loop. Then we look at the lines of the result. Unlike electric field
lines, magnetic field lines have no ends, and **Gauss's law for magnetism**
states that fact as an equation, in integral and point forms.
:::
::::

::::{frame} Magnetic Force on a Moving Charge
:::{present}
<img src="../../viz/img/L28-force.svg"
     alt="A positive charge moving to the right through a uniform field B that points into the page; the force F on it points up, perpendicular to both v and B, and the dashed circle it follows"
     style="max-width: 300px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
A charge $q$ moving with velocity $\mathbf{v}$ through a magnetic field feels the force

$$\mathbf{F} = q\ \mathbf{v}\times\mathbf{B}$$

$$\mathbf{B} = \mu\mathbf{H}, \qquad \mu_0 = 4\pi \times 10^{-7}\ \text{H/m}$$
:::

Lesson 18 defined the electric field by the force on a charge at rest. A charge
that moves feels a second force, and we use that force to define the
**magnetic flux density** $\mathbf{B}$. The force is proportional to the charge
and to its speed, and it points perpendicular to both the velocity and
$\mathbf{B}$, which is what the cross product says. In the figure,
$\mathbf{B}$ points into the page and a positive charge moves to the right, so
$\hat{\mathbf{x}}\times(-\hat{\mathbf{z}}) = \hat{\mathbf{y}}$ and the force
points up. Because the force is always perpendicular to the velocity, it does
no work on the charge: it turns the charge's path without changing its speed,
and in a uniform field the path is the dashed circle. The **permeability** $\mu$ of the
material relates the **magnetic field intensity** $\mathbf{H}$, in A/m, to
$\mathbf{B}$, in teslas (T = Wb/m²),
just as $\mathbf{D} = \epsilon\mathbf{E}$ related the two electric
fields. In free space, and in nearly every material in this module except
iron and its relatives, $\mu = \mu_0$. Lesson 31 treats magnetic materials. For
scale, the Earth's field at the surface is about $50\ \mu$T.
::::

::::{frame} Electrostatics and Magnetostatics
:::{present}
| | Electrostatics | Magnetostatics |
| :-- | :-- | :-- |
| Source | charge $dQ$ | current element $I\ d\mathbf{l}$ |
| Field | $\mathbf{E}$ (V/m) | $\mathbf{H}$ (A/m) |
| Flux density | $\mathbf{D} = \epsilon\mathbf{E}$ | $\mathbf{B} = \mu\mathbf{H}$ |
| Field of a source | Coulomb's law | Biot-Savart law |
| Net flux out of a closed surface | $Q_\text{encl}$ | $0$ |
:::

The two halves of statics run in parallel. In electrostatics the source is charge, and Coulomb's law gives the
field of each small piece of it. In magnetostatics the source is current, and
the Biot-Savart law gives the field of each small piece of a current path.
Each theory has a field and a flux density, linked by a material constant. The
last row is where they differ. Lesson 20 showed that the flux of $\mathbf{D}$
out of a closed surface equals the charge inside. The flux of $\mathbf{B}$ out
of any closed surface is zero, because no magnetic charge exists to put inside
it.
::::

::::{frame} The Biot-Savart Law
:::{present}
<img src="../../viz/img/L28-biot-savart.svg"
     alt="A wire carrying current I upward; a short element I dl on the wire, the vector R from the element to a field point at angle theta from the wire, and the field dH at the field point pointing into the page"
     style="max-width: 340px; width: 100%; display: block; margin: 0 auto;">

$$d\mathbf{H} = \frac{I\ d\mathbf{l}\times\hat{\mathbf{R}}}{4\pi R^2} = \frac{I\ d\mathbf{l}\times\mathbf{R}}{4\pi R^3}$$

- $d\mathbf{H}$ is perpendicular to both $d\mathbf{l}$ and $\mathbf{R}$, with $\vert d\mathbf{H}\vert \propto \sin\theta/R^2$.
:::

A **current element** is a short length $d\mathbf{l}$ of a current path,
pointing along the current $I$. The **Biot-Savart law** gives the field
$d\mathbf{H}$ that the element produces at a field point. Like Coulomb's law,
it is an experimental result, and this course does not derive it. The vector
$\mathbf{R}$ is the one from Lesson 18: it points from the source, the element,
to the field point, and a prime marks source coordinates. The field falls off
as $1/R^2$, as the electric field of a point charge does, but its direction
comes from a cross product. With the right thumb along the current, the
fingers curl in the direction of $d\mathbf{H}$. The magnitude of
the cross product carries a factor $\sin\theta$, where $\theta$ is the angle
between $d\mathbf{l}$ and $\mathbf{R}$, so an element produces no field along
its own line and the most field broadside to it.
::::

::::{frame} Current Elements
:::{present}
| Current flows in | Density | Units | Current element |
| :-- | :-- | :-- | :-- |
| a filament | $I$ | A | $I\ d\mathbf{l}$ |
| a surface | $\mathbf{J}_s$ | A/m | $\mathbf{J}_s\ ds$ |
| a volume | $\mathbf{J}$ | A/m² | $\mathbf{J}\ dv$ |

$$\mathbf{H} = \oint\frac{I\ d\mathbf{l}\times\mathbf{R}}{4\pi R^3}$$
:::

Lesson 18 described spread-out charge by densities, and current works the same
way. Current in a thin wire is a filament with current $I$. We describe current
that flows in a thin sheet by the **surface current density** $\mathbf{J}_s$,
the current per unit width measured across the flow, and current through a
volume by the volume current density $\mathbf{J}$ of Lesson 27, the current per
unit area. Each kind gives a current element, and any of the three can replace
$I\ d\mathbf{l}$ in the Biot-Savart law. The field of the whole current is the
superposition of the fields of its elements, an integral over the current path.
We write the integral around a closed path because a steady current has to
flow in a closed circuit. When we compute the field of one straight segment,
we are computing that segment's share of the field, and the rest of the circuit
adds its own.
::::

::::{frame} A Finite Wire: Set Up
:::{present}
<img src="../../viz/img/L28-finite-wire.svg"
     alt="A straight wire on the z axis from minus L/2 to L/2 carrying current I upward; an element dz prime at height z prime and its mirror image at minus z prime, the vectors R from each to a field point at distance rho on the bisecting plane, and the field H there pointing into the page"
     style="max-width: 440px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$d\mathbf{l}\times\mathbf{R} = \hat{\mathbf{z}}\ dz'\times\left(\rho\ \hat{\boldsymbol{\rho}} - z'\ \hat{\mathbf{z}}\right) = \hat{\boldsymbol{\phi}}\ \rho\ dz'$$
:::

A straight wire on the $z$ axis carries current $I$ in the $+z$ direction from
$z = -L/2$ to $z = L/2$. We want $\mathbf{H}$ at a distance $\rho$ from the
wire, in the plane $z = 0$ that bisects it. This is the geometry of Lesson 18's
finite line charge, and we reuse its coordinates. The element at height $z'$
is $d\mathbf{l} = \hat{\mathbf{z}}\ dz'$, and the vector from it to the field
point is $\mathbf{R} = \rho\ \hat{\boldsymbol{\rho}} - z'\ \hat{\mathbf{z}}$,
with $R = \sqrt{\rho^2 + z'^2}$. In the cross product,
$\hat{\mathbf{z}}\times\hat{\boldsymbol{\rho}} = \hat{\boldsymbol{\phi}}$ and
$\hat{\mathbf{z}}\times\hat{\mathbf{z}} = 0$. Every element therefore produces
a field along $\hat{\boldsymbol{\phi}}$, circling the wire. For the line
charge, the $z$ components of the fields from $z'$ and $-z'$ canceled in
pairs. Here no element produces a $z$ component at all, and the fields from
$z'$ and $-z'$ both point into the page at the field point and add, as the
figure shows.
::::

::::{frame} The Field of the Finite Wire
:::{present}
$$\begin{aligned} \mathbf{H} &= \int_{-L/2}^{L/2}\frac{I\ \hat{\boldsymbol{\phi}}\ \rho\ dz'}{4\pi\left(\rho^2 + z'^2\right)^{3/2}} \\ &= \hat{\boldsymbol{\phi}}\ \frac{I\rho}{4\pi}\left[\frac{z'}{\rho^2\sqrt{\rho^2 + z'^2}}\right]_{-L/2}^{L/2} \\ &= \hat{\boldsymbol{\phi}}\ \frac{I L}{4\pi\rho\sqrt{\rho^2 + L^2/4}} \end{aligned}$$
:::

We substitute the cross product and $R^3 = (\rho^2 + z'^2)^{3/2}$ into the
Biot-Savart integral. The field point stays fixed while $z'$ varies, so
$\hat{\boldsymbol{\phi}}$ and $\rho$ come outside the integral. The integral
that remains is the one Lesson 18 evaluated for the line charge. The
substitution $z' = \rho\tan\alpha$ gives $dz' = \rho\sec^2\alpha\ d\alpha$ and
$\rho^2 + z'^2 = \rho^2\sec^2\alpha$, so the integrand becomes
$\cos\alpha/\rho^2$, whose antiderivative is $\sin\alpha/\rho^2$. The right
triangle with legs $\rho$ and $z'$ gives
$\sin\alpha = z'/\sqrt{\rho^2 + z'^2}$, which is the bracket. The two limits
give equal and opposite values, so the bracket is twice its value at $L/2$,
and one factor of $\rho$ cancels. The result has the same form as the line
charge's field, with $I$ in place of $\rho_\ell/\epsilon$, and a direction that
circles the wire instead of pointing away from it.
::::

::::{frame} The Infinite Wire
:::{present}
For $L \gg \rho$, $\sqrt{\rho^2 + L^2/4} \approx L/2$:

$$\mathbf{H} = \hat{\boldsymbol{\phi}}\ \frac{I}{2\pi\rho}$$

- $I = 1$ A at $\rho = 1$ cm gives $H = 15.9$ A/m and $B = 20.0\ \mu$T.
:::

Close to a long wire, $\rho^2$ is negligible beside $L^2/4$, the square root
becomes $L/2$, and the length cancels. The field of an **infinite wire**
circles it, with field lines that are circles centered on the wire, and it
falls off as $1/\rho$. The function of $L/\rho$ is the same one as for the
line charge, so the same rule applies: a centered wire 14 times longer than
$\rho$ gives a field within 1% of this result. A $1$ A current makes $20.0\ \mu$T at $1$ cm, comparable to the Earth's
field, so a compass held a centimeter from the wire turns noticeably. Lesson 29
finds this same field without an integral, with Ampere's law.
::::

::::{frame} The Field of a Wire and a Loop
:class: viz-frame

:::{present}
<iframe src="../../viz/biot-savart.html"
        width="100%" height="490"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="The magnetic field of a finite wire or a circular loop, seen in a plane through it, with a probe that reads the field"
        data-autosize>
</iframe>
:::

The widget shows the plane that contains the current. With **Finite wire**
selected, the field points into or out of the page, and each symbol's size
shows $\vert\mathbf{H}\vert$ on a logarithmic scale. Drag the amber probe to
read the field, and compare it with the long-wire formula $I/2\pi\rho$ in the
last readout. At the start, a $20$ cm wire carrying $1$ A gives $2.85$ A/m at
$\rho = 5$ cm, 89% of the long-wire value. Lengthen the wire, or move the
probe toward it, and the two readouts converge. With **Circular loop**
selected, the loop crosses the page twice, and the lines are field lines of
$\mathbf{H}$. Every line passes through the loop and returns around the
outside. With the probe on the axis, the last readout gives the on-axis result
we derive next, and the two agree.
::::

::::{frame} A Loop: Set Up
:::{present}
<img src="../../viz/img/L28-loop.svg"
     alt="A circular loop of radius a in the xy plane carrying current I counterclockwise; an element dl at angle phi prime and the element opposite it, the vectors R from each to a point at height z on the axis, the two fields dH there, and their sum H along z"
     style="max-width: 440px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$\begin{aligned} d\mathbf{l}\times\mathbf{R} &= a\ d\phi'\ \hat{\boldsymbol{\phi}}'\times\left(z\ \hat{\mathbf{z}} - a\ \hat{\boldsymbol{\rho}}'\right) \\ &= a\ d\phi'\left(z\ \hat{\boldsymbol{\rho}}' + a\ \hat{\mathbf{z}}\right) \end{aligned}$$
:::

A circular loop of radius $a$ lies in the plane $z = 0$, centered on the $z$
axis, and carries current $I$ counterclockwise seen from above. We want the
field at height $z$ on the axis. The element at angle $\phi'$ is
$d\mathbf{l} = \hat{\boldsymbol{\phi}}'\ a\ d\phi'$, using Lesson 17's
differential length along $\hat{\boldsymbol{\phi}}$, and the primes on the
unit vectors are a reminder that they belong to the element and turn as
$\phi'$ changes. The element sits at $a\ \hat{\boldsymbol{\rho}}'$ and the
field point at $z\ \hat{\mathbf{z}}$, so
$\mathbf{R} = z\ \hat{\mathbf{z}} - a\ \hat{\boldsymbol{\rho}}'$, with
$R = \sqrt{a^2 + z^2}$ for every element. The cyclic order
$\hat{\boldsymbol{\rho}}, \hat{\boldsymbol{\phi}}, \hat{\mathbf{z}}$ gives
$\hat{\boldsymbol{\phi}}\times\hat{\mathbf{z}} = \hat{\boldsymbol{\rho}}$ and
$\hat{\boldsymbol{\phi}}\times\hat{\boldsymbol{\rho}} = -\hat{\mathbf{z}}$,
which produce the two terms.
::::

::::{frame} The Field on the Axis
:::{present}
$$\begin{aligned} \mathbf{H} &= \frac{I a}{4\pi\left(a^2 + z^2\right)^{3/2}}\int_0^{2\pi}\left(z\ \hat{\boldsymbol{\rho}}' + a\ \hat{\mathbf{z}}\right)d\phi' \\ &= \frac{I a}{4\pi\left(a^2 + z^2\right)^{3/2}}\left(0 + 2\pi a\ \hat{\mathbf{z}}\right) \\ &= \hat{\mathbf{z}}\ \frac{I a^2}{2\left(a^2 + z^2\right)^{3/2}} \end{aligned}$$

- At the center, $z = 0$, the field is $H = I/2a$.
:::

Every element is the same distance from the field point, so $R^3$ comes
outside the integral with $I$ and $a$. Two terms remain. The radial term
contains $\hat{\boldsymbol{\rho}}'$, which turns with $\phi'$, and Lesson 17
showed that its integral around a full circle is zero. The figure shows why:
the element opposite any element produces a field whose radial part is equal
and opposite, so the radial parts cancel in pairs and the axial parts add. The
axial term is constant, and its integral is $2\pi a$. For a loop of radius
$a = 5$ cm carrying $1$ A, the field at the center is $10.0$ A/m, or
$12.6\ \mu$T. One radius above the center, at $z = a$, the factor
$(a^2/(a^2 + z^2))^{3/2}$ is $2^{-3/2} = 0.354$, and the field drops to
$3.54$ A/m.
::::

::::{frame} Far From the Loop
:::{present}
For $z \gg a$, drop $a^2$ beside $z^2$:

$$\mathbf{H} \approx \hat{\mathbf{z}}\ \frac{I a^2}{2 z^3} = \hat{\mathbf{z}}\ \frac{m}{2\pi z^3}, \qquad m = I\pi a^2$$

- A small loop is a **magnetic dipole**, and its field falls as $1/z^3$.
:::

Far from the loop, $a^2 + z^2 \approx z^2$, and the denominator becomes
$2z^3$. Multiplying top and bottom by $\pi$ collects the current and the area
of the loop into the **magnetic dipole moment** $m = I\pi a^2$, in A·m². The
far field depends only on $m$, so a loop with half the area and twice the
current produces the same far field. The result has the same form as the
on-axis field of the electric dipole in the Lesson 18 practice set,
$p/2\pi\epsilon z^3$, and the same $1/z^3$ falloff. For the $5$ cm loop at
$z = 50$ cm, ten radii away, the exact result gives $9.85$ mA/m and the
dipole approximation gives $10.0$ mA/m, a difference of 1.5%. A bar magnet,
and the Earth itself, have this same dipole field far away.
::::

::::{frame} Worked Example: A Square Loop
:::{present}
<img src="../../viz/img/L28-square-loop.svg"
     alt="A square loop of side s carrying current I counterclockwise, with one side highlighted; the distance s/2 from the center to that side, the distance s over root 2 to a corner, the dashed inscribed circle, and the field H at the center pointing out of the page"
     style="max-width: 270px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
A square loop of side $s = 10$ cm carries $I = 1$ A. Each side is a finite wire with $L = s$ and $\rho = s/2$:

$$H = 4\ \frac{I s}{4\pi\left(\frac{s}{2}\right)\sqrt{\frac{s^2}{4} + \frac{s^2}{4}}} = \frac{2\sqrt{2}\ I}{\pi s} = 9.00\ \text{A/m}$$
:::

:::{admonition} Worked example — the field at the center of a square loop
:class: tip
The center of the square lies on the bisecting plane of every side, a distance
$s/2$ from each, so the finite-wire result applies to each side with $L = s$
and $\rho = s/2$. The square root is
$\sqrt{s^2/4 + s^2/4} = s/\sqrt{2}$, so one side contributes

$$H_\text{side} = \frac{I s}{4\pi\ (s/2)(s/\sqrt{2})} = \frac{\sqrt{2}\ I}{2\pi s} = 2.25\ \text{A/m}$$

By the right-hand rule, every side produces a field in the same direction at
the center: out of the page for a current that runs counterclockwise. The four
contributions add to $2\sqrt{2}\ I/\pi s = 9.00$ A/m, or $11.3\ \mu$T. A
circular loop that fits inside the square, with $a = s/2 = 5$ cm, gives
$I/2a = 10.0$ A/m. The square has more wire and encloses more area, but its
field at the center is 10% smaller, because the wire near the corners is
farther from the center, up to $s/\sqrt{2} = 7.07$ cm, and those elements see
the center at a smaller $\sin\theta$.
:::
::::

::::{frame} Closed Magnetic Field Lines
:::{present}
<img src="../../viz/img/L28-field-lines.svg"
     alt="Left, the field lines of an electric dipole, which start on the positive charge and end on the negative charge. Right, the field lines of a current loop in cross section, which pass through the loop and close around the outside"
     style="max-width: 480px; width: 100%; display: block; margin: 0 auto;">

- Electric lines start and end on charge; magnetic lines close on themselves.

Element on the $z$ axis, $d\mathbf{H} \propto \hat{\mathbf{z}}\times\mathbf{R}/R^3 = (-y,\ x,\ 0)/R^3$:

$$\nabla\cdot d\mathbf{H} \propto \frac{\partial}{\partial x}\left(\frac{-y}{R^3}\right) + \frac{\partial}{\partial y}\left(\frac{x}{R^3}\right) = \frac{3xy}{R^5} - \frac{3xy}{R^5} = 0$$
:::

The figure draws the field lines of an electric dipole beside those of a small
current loop. Far away, the two patterns match, since both are dipole fields.
Near the sources they differ. Every electric field line starts on the positive
charge and ends on the negative one. Every magnetic field line passes through
the loop and returns around the outside, closing on itself, and none of them
ends anywhere. The Biot-Savart law explains why, and we can show it for one
element. Choose coordinates with the element at the origin, pointing along
$\hat{\mathbf{z}}$. With $\mathbf{R} = (x, y, z)$ and
$R = \sqrt{x^2 + y^2 + z^2}$, the cross product is
$\hat{\mathbf{z}}\times\mathbf{R} = (-y, x, 0)$, so $d\mathbf{H}$ has no $z$
component and circles the element's own line. Its divergence has two terms. The
quotient rule with $\partial R/\partial x = x/R$ gives
$\partial(-y/R^3)/\partial x = 3xy/R^5$, and with $\partial R/\partial y = y/R$
it gives $\partial(x/R^3)/\partial y = -3xy/R^5$. The terms cancel at every
point away from the element. We can place any element on the $z$ axis this
way, so the field of every element has zero divergence, and so does their sum,
the field of any current. A field with zero divergence everywhere has no point
where lines start or end. No experiment has found an isolated magnetic charge, a magnetic monopole, that
could start or end a line. Cutting a bar magnet in half produces two smaller
magnets, each with both poles.
::::

::::{frame} Gauss's Law for Magnetism
:::{present}
<img src="../../viz/img/L28-gauss-mag.svg"
     alt="Left, closed field lines crossing a dashed closed surface S, entering on one side and leaving on the other. Right, a closed curve C with a flat cap S1 and a domed cap S2, both crossed by the same vertical field lines"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">

$$\oint_S \mathbf{B}\cdot d\mathbf{s} = 0$$

- Every field line that enters a closed surface also leaves it.
- Compare Lesson 20: $\oint_S \mathbf{D}\cdot d\mathbf{s} = Q_\text{encl}$.
:::

The **magnetic flux** through a surface is $\int \mathbf{B}\cdot d\mathbf{s}$,
in webers, and it counts the field lines that cross the surface. Because
magnetic field lines close on themselves, a line that enters a closed surface
has to leave it somewhere, and the net flux out of the surface is zero. That is
**Gauss's law for magnetism**. Lesson 20's Gauss's law for $\mathbf{D}$ has the
enclosed charge on the right side. Here the right side is zero for every
closed surface, because there is no magnetic charge to enclose. In the left
panel, each line that enters $S$ leaves it again. One consequence matters in
Module 4. Take two open surfaces that share the same boundary curve, the flat
cap $S_1$ and the dome $S_2$ on the curve $C$ in the right panel. Together they
form a closed surface, so the flux that enters through one
equals the flux that leaves through the other. The flux through a circuit
therefore depends only on the circuit, not on which surface we draw across it.
::::

::::{frame} The Point Form
:::{present}
$$\oint_S \mathbf{B}\cdot d\mathbf{s} = \int_V \nabla\cdot\mathbf{B}\ dv = 0 \quad\Longrightarrow\quad \nabla\cdot\mathbf{B} = 0$$

Check, infinite wire, $\mathbf{B} = \hat{\boldsymbol{\phi}}\ \mu I/2\pi\rho$:

$$\nabla\cdot\mathbf{B} = \frac{1}{\rho}\frac{\partial\left(\rho B_\rho\right)}{\partial\rho} + \frac{1}{\rho}\frac{\partial B_\phi}{\partial\phi} + \frac{\partial B_z}{\partial z} = 0 + 0 + 0$$
:::

The divergence theorem of Lesson 17 turns the flux out of a closed surface into
the volume integral of the divergence over the region inside it. The flux is
zero for every closed surface, so the volume integral of $\nabla\cdot\mathbf{B}$
is zero over every volume, however small and wherever it sits. The only way an
integral can vanish over every volume is for the integrand to be zero
everywhere, which is the argument Lesson 21 used to reach
$\nabla\cdot\mathbf{D} = \rho_v$. The result, $\nabla\cdot\mathbf{B} = 0$, is
the **point form** of Gauss's law for magnetism: at no point does the magnetic
field have a source or a sink. In a uniform material $\mu$ is constant, so
$\nabla\cdot\mathbf{H} = 0$ as well. The infinite wire's field passes the check:
it has only a $\phi$ component, and that component depends only on $\rho$, so
each of the three terms of the cylindrical divergence is zero.
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Result |
| :-- | :-- | :-- |
| Magnetic force | Force on a charge moving through $\mathbf{B}$ | $\mathbf{F} = q\ \mathbf{v}\times\mathbf{B}$ |
| $\mathbf{B}$, $\mathbf{H}$, $\mu$ | Flux density (T), field intensity (A/m), permeability | $\mathbf{B} = \mu\mathbf{H}$; $\mu_0 = 4\pi \times 10^{-7}$ H/m |
| Biot-Savart law | Field of a current element | $d\mathbf{H} = \dfrac{I\ d\mathbf{l}\times\mathbf{R}}{4\pi R^3}$ |
| Current elements | Filament, sheet, volume | $I\ d\mathbf{l}$, $\mathbf{J}_s\ ds$, $\mathbf{J}\ dv$ |
| Finite wire, bisecting plane | Length $L$, distance $\rho$ | $\dfrac{I L}{4\pi\rho\sqrt{\rho^2 + L^2/4}}\ \hat{\boldsymbol{\phi}}$ |
| Infinite wire | $L \gg \rho$ | $\dfrac{I}{2\pi\rho}\ \hat{\boldsymbol{\phi}}$ |
| Loop, on the axis | Radius $a$, height $z$ | $\dfrac{I a^2}{2(a^2 + z^2)^{3/2}}\ \hat{\mathbf{z}}$; $I/2a$ at the center |
| Magnetic dipole | Moment $m = I\pi a^2$ | far field on the axis $m/2\pi z^3$ |
| Gauss's law for magnetism | No magnetic charge; field lines close | $\oint \mathbf{B}\cdot d\mathbf{s} = 0$, $\nabla\cdot\mathbf{B} = 0$ |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE343_L28_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE343_L28_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 29**: Ampere's law finds the infinite wire's field with no integral.
- **Lesson 30**: Ampere's law for the coax, the solenoid, and the toroid, and the coax's $L'$.
:::

Today the Biot-Savart law gave the field of a wire and a loop, one current
element at a time. That method always works, but even a straight wire needs an
integral along its length, and for the most symmetric currents there is a
shortcut, as there was in Module 2. Lesson 29
introduces Ampere's law, the magnetic counterpart of Gauss's law, which finds
the infinite wire's field without an integral. Lesson 30 applies it to the coaxial
cable, the solenoid, and the toroid, and derives the inductance per unit
length $L'$ of the coax that Lesson 6 quoted.

Before Lesson 29, read sections 7.4, 7.5, and 7.9 of Ellingson,
*Electromagnetics*, Vol. 1.
::::
