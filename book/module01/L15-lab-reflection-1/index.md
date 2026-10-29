---
frame_view: true
---

# L15 - Reflection and Transmission Coefficient Lab I

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Spring 2027</div>

<h1 class="frame-title">Reflection and Transmission Coefficient Lab I</h1>

<div class="title-rule"></div>

Today you calibrate a network analyzer and measure loads whose reflection coefficients you can predict.

Lesson 15 · Module 1: Foundations · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 7">
  <li>I can measure the reflection coefficient across a range of frequencies and interpret the measurement using a network analyzer.</li>
</ol>

:::{depth}
Lessons 6 through 14 computed reflection coefficients on paper. This lab
measures them. A **vector network analyzer** (VNA) sends a wave down a cable,
measures the wave that comes back, and reports their ratio, $\Gamma$, in
magnitude and phase across a band of frequencies. Today you calibrate the
instrument, which removes the effect of the cable and connectors, and then
measure five loads: an open, a short, a capacitor, a matched $50\ \Omega$
resistor, and a $1\ \text{k}\Omega$ resistor. You predict each one first, so
every measurement is a check on the theory or on your setup. Lesson 16 uses
the same instrument to identify a device you cannot see.
:::
::::

::::{frame} Where We Were
:::{present}
**Lesson 6**: the reflection coefficient and the special loads

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

| Load | $\Gamma$ |
| :-- | :-- |
| Matched | $0$ |
| Short | $-1$, or $1\angle 180^\circ$ |
| Open | $+1$, or $1\angle 0^\circ$ |
:::

Lesson 6 derived the reflection coefficient from the boundary condition at the
load, and Lessons 10 through 13 put it on the Smith chart, where the matched
load is the center, the short is the left edge, and the open is the right
edge. Every measurement today lands on one of those points or on a curve you
can predict from them.
::::

::::{frame} What a VNA Measures
:::{present}
- $S_{11}$: the wave reflected back into port 1, over the wave sent out. With a load on port 1, $S_{11} = \Gamma$.
- $S_{21}$: the wave arriving at port 2, over the wave sent from port 1. This is a transmission coefficient.
:::

A VNA describes a device by its **scattering parameters**, or S-parameters,
which are ratios of waves rather than of voltages and currents. The subscripts
name the receiving port and then the sending port, so $S_{21}$ is the wave
received at port 2 when port 1 transmits. With a single load connected to
port 1, the reflected wave over the incident wave is exactly the reflection
coefficient of Lesson 6, so $S_{11} = \Gamma$. Lesson 16 uses $S_{21}$ as well.
The NanoVNA displays four traces at once: $\vert S_{11}\vert$ in dB in yellow,
$\vert S_{21}\vert$ in dB in blue, the phase of $S_{11}$ in magenta, and $S_{11}$ on a
Smith chart in green.
::::

::::{frame} Reflection in Decibels
:::{present}
The VNA reports the magnitude as a voltage ratio in dB:

$$\vert\Gamma\vert_\text{dB} = 20\log_{10}\vert\Gamma\vert$$

| $\vert\Gamma\vert$ | $\vert\Gamma\vert_\text{dB}$ |
| :-- | :-- |
| $1$ (open, short) | $0$ dB |
| $0.905$ ($1\ \text{k}\Omega$) | $-0.87$ dB |
| $0$ (matched) | $-\infty$ dB |
:::

The analyzer measures wave amplitudes, which are voltages, so it converts the
magnitude of $\Gamma$ to decibels with $20\log_{10}$, not $10\log_{10}$. A load
that reflects everything reads $0$ dB. A perfect match reads $-\infty$ dB, which
no real measurement reaches: a good $50\ \Omega$ resistor reads somewhere between
$-30$ and $-50$ dB, and the floor is set by how well you calibrated. The
$1\ \text{k}\Omega$ value comes from
$\Gamma = \frac{1000 - 50}{1000 + 50} = 0.905$.
::::

::::{frame} Why Calibrate
:::{present}
- Cables, adapters, and clips add delay and reflections.
- Three known standards (open, short, $50\ \Omega$) let the VNA solve for that error and remove it.
- Recalibrate after any change of cable or frequency range.
:::

Between the analyzer's port and the load sit a cable, an SMA-to-BNC adapter,
and a pair of clip leads. Lesson 7 showed that a length of line transforms the
impedance at its end, so without correction the VNA would report the load as
seen through all of that hardware, not the load itself. Calibration fixes this.
You connect three loads whose reflection coefficients are known exactly, the
open, the short, and the $50\ \Omega$ load, at the exact point where the device
will go. From the three measurements the VNA solves for the error the hardware
introduces at each frequency, and it removes that error from every later
measurement. The correction holds only for the hardware and the frequencies you
calibrated with.
::::

::::{frame} Predicting a Capacitor
:::{present}
For $Z_L = -jX$, with $X = \frac{1}{\omega C}$:

$$\Gamma = \frac{-jX - Z_0}{-jX + Z_0} = \frac{X - jZ_0}{X + jZ_0} = e^{-j2\phi}, \qquad \phi = \tan^{-1}\frac{Z_0}{X}$$

$\vert\Gamma\vert = 1$ at every frequency; only the phase changes.
:::

A capacitor stores energy and dissipates none, so Lesson 6 predicts
$\vert\Gamma\vert = 1$. To get the phase, we multiply the numerator and
denominator by $j$. The numerator becomes the complex conjugate of the
denominator, so the ratio has magnitude one and a phase of minus twice the
denominator's angle. At low frequency $X$ is large, $\phi$ is small, and the
capacitor looks like an open. As the frequency rises, $X$ falls and the phase
grows more negative, so on the Smith chart the measurement traces the outer
circle clockwise from the open toward the short.
::::

::::{frame} Pre-Lab: The 470 pF Capacitor
:::{present}
| $f$ | $Z_C$ | $\Gamma$ |
| :-- | :-- | :-- |
| 50 kHz | $-j6773\ \Omega$ | $1\angle -0.8^\circ$ |
| 500 kHz | $-j677\ \Omega$ | $1\angle -8.4^\circ$ |
| 2 MHz | $-j169\ \Omega$ | $1\angle -32.9^\circ$ |
| 5 MHz | $-j67.7\ \Omega$ | $1\angle -72.9^\circ$ |
:::

The packet asks you to fill in the expected impedance of the 470 pF capacitor at
ten frequencies from 50 kHz to 5 MHz and plot them on the Smith chart before the
lab. The table shows four of them, worked with the result of the previous frame.
At 5 MHz, for example,

$$X = \frac{1}{2\pi \times 5 \times 10^6 \times 470 \times 10^{-12}} = 67.7\ \Omega, \qquad \phi = \tan^{-1}\frac{50}{67.7} = 36.4^\circ$$

so $\Gamma = 1\angle -72.9^\circ$. Work the other six the same way. Over the
band you will measure, the capacitor covers only the upper quarter of the
Smith chart's outer circle; its reactance would equal $50\ \Omega$ at 6.8 MHz,
just above the top of the sweep.
::::

::::{frame} Equipment and Safety
:class: read-only

Each team uses a NanoVNA with its SMA cables, a black SMA-to-BNC adapter, a
BNC-to-grabber-clip cable, a $50\ \Omega$ resistor, a $1\ \text{k}\Omega$
resistor, and a 470 pF capacitor.

- RF connectors are fragile. Tighten them finger tight, and never cross-thread
  one.
- Pause the sweep before you change any connection.
- No food or drink at the bench. At least two people must be in the room while
  equipment is in use.
- Leave the bench as you found it: equipment in its original configuration,
  cables returned, trash removed.
::::

::::{frame} Procedure: Setup and Calibration
:class: read-only

1. Turn on the NanoVNA. Tap the screen, choose **Display**, and tap **Flip
   Display** so the ports face away from you. Tap **Pause Sweep**.
2. Connect the SMA-to-BNC adapter to channel 0 (labeled "1" on the board), and
   the grabber-clip cable to the adapter. Connect the blue SMA cable to
   channel 1, and leave its other end free.
3. Choose **Stimulus** and set the range from 50 kHz to 5 MHz with **Start** and
   **Stop**.
4. Choose **Cal**, then **Reset**.
5. Leave the clips apart (an open) and tap **Open**. Wait for the label to turn
   black.
6. Clip the leads together (a short) and tap **Short**.
7. Clip the leads across the $50\ \Omega$ resistor and tap **Load**. Do not
   perform a **Thru**.
8. Tap **Done**, save the calibration to slot 0 if you wish, and confirm that
   **Correction** is highlighted.
::::

::::{frame} Procedure: Measurements
:class: read-only

Pause the sweep before each change, then restart it to measure. Read values
from the markers at the top of the screen; move a marker by dragging it with a
stylus or with **Markers**, **Select Marker**, and the side buttons.

1. **Open.** Leave the clips apart. Record the magnitude and phase of $S_{11}$,
   and where the trace sits on the Smith chart.
2. **Short.** Clip the leads together and record the same quantities.
3. **Capacitor.** Clip the 470 pF capacitor across the leads. At each frequency
   in the packet's table, record the measured impedance, and compare the trace
   on the Smith chart with your predicted points.
4. **Matched load.** Clip the $50\ \Omega$ resistor across the leads. Record
   $\vert S_{11}\vert$ in dB and the resistance the marker reports.
5. **Resistive mismatch.** Clip the $1\ \text{k}\Omega$ resistor across the
   leads. Record the magnitude and phase of $S_{11}$ and the resistance.

For each load, write at least one observation comparing your measurement with
your prediction.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE343_Lab_ReflectionCoefficients_Spring2025.pdf" target="_blank" rel="noopener">Reflection and Transmission Coefficient Lab packet (PDF)</a>
- <a class="doc-link" href="../../handouts/SmithChart_blank.pdf" target="_blank" rel="noopener">Blank Smith chart (PDF)</a>

:::{depth}
The packet is the turn-in document for both lab periods, and each team submits
one combined report on Gradescope. It holds the predictions table for the
capacitor, a blank Smith chart for plotting it, and the questions for each
measurement. Bring your predictions to the lab already worked.
:::
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 16**: recalibrate with SMA standards and identify a filter you cannot see from its $S_{11}$ and $S_{21}$.
:::

Today you measured loads you already understood, which tests the instrument and
your calibration as much as the theory. Lesson 16 reverses the roles. The device
under test is a filter with its label taped over, and you identify what it is,
where its cutoff falls, and whether it looks capacitive or inductive in each
part of its band, using only the analyzer.

Before Lesson 16, read Part 6 of the lab packet.
::::
