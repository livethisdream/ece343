---
frame_view: true
---

# L26 - Electrostatics Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">Electrostatics Lab</h1>

<div class="title-rule"></div>

Today you compute the fields of Module 2 on a grid in Python and check them against the results you derived by hand.

Lesson 26 · Module 2: Electrostatics · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '5'">
  <li>I can apply Coulomb's Law to use direct integration to calculate the electric field due to charge density in various geometries, including rectangular, cylindrical, and spherical coordinate systems.</li>
  <li>I can apply the integral and differential forms of Gauss's Law to calculate the electric field due to charge density in various geometries, including rectangular, cylindrical, and spherical coordinate systems.</li>
  <li>I can calculate the electric field from the scalar electric potential in a variety of geometries.</li>
  <li>I can apply the electric field boundary conditions to calculate electric fields on both sides of a material boundary.</li>
</ol>

:::{depth}
Lessons 18 through 25 derived fields, potentials, and capacitance with pencil
and paper, one symmetric geometry at a time. This lab hands the same physics
to a computer. In Part A you build fields from Coulomb's law by superposition
and test Gauss's law in both of its forms. In Part B you solve Laplace's
equation for the cross section of a coaxial cable and get its capacitance per
meter from the field. Every computation is checked against a result you can
work by hand, because a program that runs without an error can still be wrong.
The lab is a Python notebook, run in Google Colab or on your own machine, and
you work in a team of two or three.
:::
::::

::::{frame} Where We Were
:::{present}
| Lesson | Result the lab checks |
| :-- | :-- |
| 18 | $\mathbf{E}$ of point charges and of a finite line |
| 20, 21 | Gauss's law, integral and point forms |
| 23 | Laplace's equation; $V(\rho)$ in a coax |
| 25 | $C' = \dfrac{2\pi\epsilon}{\ln(b/a)}$ |
:::

Each part of the lab reproduces a result from Module 2 numerically. Lesson 18
gave the field of point charges by superposition and of a finite line by
direct integration. Lessons 20 and 21 gave Gauss's law in its integral and
point forms. Lesson 23 derived Laplace's equation and solved it for the coax,
and Lesson 25 turned that solution into the capacitance per meter, the
$96.8\ \text{pF/m}$ that Lesson 6 quoted for RG-58.
::::

::::{frame} Superposition on a Grid
:::{present}
$$\mathbf{E}(\mathbf{r}) = \sum_n \frac{q_n}{4\pi\epsilon_0}\ \frac{\mathbf{r} - \mathbf{r}_n}{\vert\mathbf{r} - \mathbf{r}_n\vert^3}$$

- One call fills the whole grid: NumPy works on arrays, so there is no loop over points.
- A line of charge is many point charges in a row.
:::

The code evaluates Lesson 18's sum at every point of a $200 \times 200$ grid at
once. NumPy applies each arithmetic operation to a whole array, so the only
loop is over the charges, and the grid of forty thousand points costs about as
much as a single point would in a loop. Every charge sits in the $z = 0$
plane, and the field is evaluated in that plane, where $E_z = 0$ by symmetry.
To model a line of charge, the code splits it into short pieces and puts a
point charge $\rho_\ell\ \Delta x$ at the center of each, which is the sum that
Lesson 18's integral is the limit of.
::::

::::{frame} Pre-Lab: Predictions
:::{present}
Work these before the lab:

- $\vert\mathbf{E}\vert$ at $0.1\ \text{m}$ from $1\ \text{nC}$
- The dipole's $\mathbf{E}$ at $(0, 0.3)\ \text{m}$
- A $0.8\ \text{m}$ line's $E$ at $d = 0.1\ \text{m}$, finite and infinite
:::

Every computation in Part A has a hand answer to compare with, and the
notebook asks for it. The first is one line of Coulomb's law:

$$\vert\mathbf{E}\vert = \frac{(8.988 \times 10^9)(1 \times 10^{-9})}{(0.1)^2} = 899\ \text{V/m}.$$

The dipole is $+1\ \text{nC}$ at $(-0.1, 0)$ and $-1\ \text{nC}$ at
$(0.1, 0)\ \text{m}$; work its field on the bisector by superposition, as in
Lesson 18. The line carries $\rho_\ell = 12.5\ \text{nC/m}$; use Lesson 18's
finite-line result and its infinite-line limit, and note how far apart they
are.
::::

::::{frame} A Trap in Two Dimensions
:::{present}
$$\nabla\cdot\mathbf{E} = \frac{\partial E_x}{\partial x} + \frac{\partial E_y}{\partial y} + \frac{\partial E_z}{\partial z}$$

A grid in the plane takes only the first two terms. In the plane $E_z = 0$, but $\partial E_z/\partial z$ is not zero.
:::

The point form of Gauss's law says $\nabla\cdot\mathbf{E} = 0$ wherever there is
no charge. The tempting test is to take the divergence of a point charge's
field on the grid and look for zero. It does not come out zero, and the reason
is the third term. The grid lives in one plane, so it can take derivatives
along $x$ and $y$ but not across the plane. $E_z$ vanishes in the plane, yet it
grows as you step above it, so its derivative along $z$ does not vanish, and
leaving it out makes the two-term sum report charge where there is none. In
the notebook you find the missing term and show that it cancels the rest
exactly. Earlier versions of this lab fell into the trap without noticing.
::::

::::{frame} Line Charges Are 2D Fields
:::{present}
$$\mathbf{E} = \frac{\rho_\ell}{2\pi\epsilon_0}\ \frac{\boldsymbol{\rho}}{\vert\boldsymbol{\rho}\vert^2}$$

The same field in every plane, so $\partial/\partial z = 0$, and

$$\oint \epsilon_0\ \mathbf{E}\cdot\hat{\mathbf{n}}\ d\ell = \rho_{\ell,\text{enc}}$$
:::

An infinite line charge along $z$ has the field Lesson 20 found with a
cylindrical Gaussian surface, and that field is the same in every plane of
constant $z$. Nothing changes along $z$, so the two-term divergence is the
whole divergence, and the grid can test the point form. The integral
form becomes a statement per meter of length: the flux of
$\epsilon_0\mathbf{E}$ out through any closed contour in the plane equals the
line charge inside it. The notebook integrates around squares that enclose
one line, two lines of opposite charge, and none, and you explain each result
with Gauss's law.
::::

::::{frame} Laplace's Equation on a Grid
:::{present}
$$V_{i,j} = \tfrac{1}{4}\left(V_{i+1,j} + V_{i-1,j} + V_{i,j+1} + V_{i,j-1}\right)$$

Fix $V$ on the conductors, guess in between, and average until nothing changes.
:::

Lesson 23 showed that in a charge-free region Laplace's equation makes each
point's potential the average of its neighbors, and that the solution is
unique once the potential on the boundaries is fixed. Part B uses both facts.
The inner conductor of RG-58, of radius $a = 0.405\ \text{mm}$, is held at
$1\ \text{V}$, and the outer, of radius $b = 1.475\ \text{mm}$, at $0\ \text{V}$.
The code replaces every point between them with its neighbors' average, half
the grid at a time like the two colors of a checkerboard, and slightly
over-corrects each step so the guess settles in a few hundred sweeps. You then
compare the result with Lesson 23's $V(\rho)$.
::::

::::{frame} Capacitance by Gauss's Law
:::{present}
$$\rho_\ell = \oint \epsilon\ \mathbf{E}\cdot\hat{\mathbf{n}}\ d\ell, \qquad C' = \frac{\rho_\ell}{V_0}$$

Compare with Lesson 25: $C' = \dfrac{2\pi\epsilon}{\ln(b/a)} = 96.8\ \text{pF/m}$
:::

The relaxed potential gives the field, $\mathbf{E} = -\nabla V$, by finite
differences. Lesson 24's boundary condition puts the charge on the inner
conductor's surface, and Gauss's law collects it: the flux of
$\epsilon\mathbf{E}$ out through any contour around the inner conductor is the
charge per meter, $\rho_\ell$. Dividing by the $1\ \text{V}$ between the
conductors gives $C'$, which you compare with Lesson 25's formula for
polyethylene, $\epsilon_r = 2.25$. The two will not agree exactly, and the
notebook asks you to find out why by changing the grid.
::::

::::{frame} Checking a Computation
:::{present}
- Test against a case you can work by hand.
- Change the grid and watch the answer move.
- A program that runs without an error can still answer the wrong question.
:::

The habits this lab practices carry into every simulation you will run. A
computed field earns trust only after it reproduces a result you know, which
is why each part starts with one. A grid answer carries a grid error, and the
only way to see its size is to refine the grid and watch how the answer
changes, which also tells you what the error comes from. The divergence trap is
the third habit: the code ran, the plot looked plausible, and it was answering
a question about a different field.
::::

::::{frame} Part C: Measuring C′ on the Bench
:::{present}
For $\beta\ell \ll 1$, an open line is a capacitor:

$$Z_\text{in} = -jZ_0\cot\beta\ell \approx \frac{1}{j\omega C'\ell}$$

Two lengths cancel the connectors: $C' = \dfrac{C_2 - C_1}{\ell_2 - \ell_1}$
:::

If your instructor assigns Part C, you measure $C'$ with the NanoVNA of
Lessons 15 and 16. Lesson 7 gave the input impedance of an open-circuited
line; when the line is a small fraction of a wavelength, $\cot\beta\ell
\approx 1/\beta\ell$ and the line looks like its total capacitance
$C'\ell$. At 2 MHz a 2 m cable is $0.02\lambda$ long, close enough that the
error is under 1%. You read the reactance of two open-ended cables of
different length, and the difference removes the adapter's few picofarads,
which add equally to both.
::::

::::{frame} Teams and the Report
:class: read-only

Work in a team of two or three, and submit one report per team.

- Open the notebook in Colab (link below), choose **File**, then **Save a copy
  in Drive**, and share the copy with your teammates. Or download it and run
  it locally with Python 3, NumPy, and Matplotlib.
- Run the cells in order. A cell marked `TODO` is yours to finish; the rest are
  given. Answer every **Answer** cell.
- Before you submit, choose **Runtime**, then **Run all**, so every output is
  current. Put every member's name and a Documentation line in the first
  cell.
- Export to PDF and upload it to Gradescope as one team submission, adding
  every member.
- For Part C, if assigned: the NanoVNA with its SMA calibration standards, the
  SMA-to-BNC adapter, and two RG-58 cables of different length.
::::

::::{frame} Lab Notebook
:class: read-only doc-links

- <a class="doc-link" href="https://colab.research.google.com/github/livethisdream/ece343/blob/main/book/extras/labs/ECE343_Lab_L26_Electrostatics.ipynb" target="_blank" rel="noopener">Open the Electrostatics Lab notebook in Google Colab</a>
- <a class="doc-link" href="../../labs/ECE343_Lab_L26_Electrostatics.ipynb" download>Download the notebook (.ipynb)</a>

:::{depth}
The notebook is the lab packet and the turn-in document. It holds the
instructions, the code you finish, and the questions you answer. Colab runs it
in the browser with nothing to install; a local copy needs Python 3 with NumPy
and Matplotlib. Work the pre-lab predictions before the period.
:::
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 27**: charges in motion: current density, conductivity, and resistance.
- **Module 3**: magnetostatics, where Ampere's law gives the coax its $L'$.
:::

Module 2 kept every charge still. Module 3 lets charge move. Lesson 27 starts
with steady current in conductors, and the rest of the module finds the
magnetic field that current makes. That field completes the coax: Lesson 25
derived $C'$, and Ampere's law will derive the $L'$ that Lesson 6 also quoted,
so that $Z_0 = \sqrt{L'/C'}$ is derived from start to finish.
::::
