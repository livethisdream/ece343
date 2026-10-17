---
frame_view: true
nav: Foundations
---

# Module 1 — Foundations

::::{frame}
:class: title-frame

<div class="course-mark">ECE 343 · Module 01</div>

<h1 class="frame-title">Foundations</h1>

<div class="title-rule"></div>

Fields, phasors, and the transmission line: the first place a circuit stops behaving like one.

Lessons 1–16 · Intro to Electromagnetics · Maj Ellis · Dr. Neil Rogers
::::

::::{frame} Where This Module Goes
What electromagnetics is for, the language of fields and phasors, and the transmission line: wave propagation, reflection, impedance matching, the Smith chart, and transients, measured on a network analyzer in the first lab.
::::

::::{frame} Chapter 1: Introduction

<ol class="lo-list" style="--module: '1'">
  <li>I can articulate what I will learn and how I will be assessed in this course.</li>
  <li>I can articulate practical applications of electromagnetics.</li>
</ol>
::::

::::{frame} Chapter 2: Fields

<ol class="lo-list" style="--module: '2'">
  <li>I can recall the definition of scalar fields, vector fields, phasors, and Euler's identity.</li>
  <li>I can explain the basic terms and quantities used to describe electromagnetic fields.</li>
</ol>
::::

::::{frame} Chapter 3: Transmission Lines (3.1-3.4)

<ol class="lo-list" style="--module: '3'">
  <li>I can describe the origin of the transmission line equation, understand the method of developing a solution, and interpret the solution.</li>
  <li>I can explain the physical meaning of and calculate the following quantities: propagation constant, phase constant, attenuation constant, characteristic impedance, VSWR, reflection coefficient, and transmission coefficient.</li>
  <li>I can use the transmission line equation to calculate the voltage/current at an arbitrary point on a specified transmission line.</li>
  <li>I can use the transmission line equation to match a load to a source using a length of transmission line.</li>
</ol>
::::

::::{frame} Chapter 3: Transmission Lines (3.5-3.8)

<ol class="lo-list" style="--module: '3'; counter-reset: lo 4">
  <li>I can identify the various quantities represented on the Smith Chart.</li>
  <li>I can use a Smith Chart to design a matching network for a given source and load, using series components, parallel components, shorted stubs, and open stubs.</li>
  <li>I can plot the transient response of a load connected to a source through a transmission line.</li>
  <li>I can measure the reflection coefficient across a range of frequencies and interpret the measurement using a network analyzer.</li>
</ol>
::::

::::{frame} Lessons 1-3

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L01-course-intro/index.html">
    <span class="mt-kind">Lesson · L1</span>
    <h4>Course Introduction</h4>
    <p>What you will learn, how you will be assessed, and where electromagnetics shows up in the systems you will operate. Objectives 1.1, 1.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L02-fields/index.html">
    <span class="mt-kind">Lesson · L2</span>
    <h4>Fields, Parameters, and Field Quantities</h4>
    <p>Scalar and vector fields, phasors and Euler's identity, and the quantities that describe electric and magnetic fields. Objectives 2.1, 2.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L03-lumped-element-model/index.html">
    <span class="mt-kind">Lesson · L3</span>
    <h4>The Lumped-Element Model</h4>
    <p>When a pair of wires stops being a short circuit, and how to model a line as a cascade of tiny circuits. Objective 3.1.</p>
  </a>
</div>
::::

::::{frame} Lessons 4-6

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L04-telegraphers-equations/index.html">
    <span class="mt-kind">Lesson · L4</span>
    <h4>The Telegrapher's Equations</h4>
    <p>The wave equations for voltage and current on a line, and the traveling-wave solution. Objective 3.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L05-characteristic-impedance/index.html">
    <span class="mt-kind">Lesson · L5</span>
    <h4>Characteristic Impedance and Wave Propagation</h4>
    <p>Propagation, phase, and attenuation constants, and the characteristic impedance of a line. Objective 3.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L06-reflection-vswr/index.html">
    <span class="mt-kind">Lesson · L6</span>
    <h4>Coaxial Lines, Reflection Coefficient, and VSWR</h4>
    <p>The coaxial line, the reflection coefficient at a load, standing waves, and VSWR. Objectives 3.2, 3.3.</p>
  </a>
</div>
::::

::::{frame} Lessons 7-9

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L07-terminated-lines/index.html">
    <span class="mt-kind">Lesson · L7</span>
    <h4>Terminated Transmission Lines</h4>
    <p>Input impedance of a terminated line, and the special cases: shorted, open, and quarter-wave lines. Objectives 3.3, 3.4.</p>
  </a>
  <a class="mt-card mt-lesson" href="L08-impedance-matching-1/index.html">
    <span class="mt-kind">Lesson · L8</span>
    <h4>Impedance Matching I</h4>
    <p>Matching a load to a source with a length of transmission line. Objective 3.4.</p>
  </a>
  <a class="mt-card mt-lesson" href="L09-impedance-matching-2/index.html">
    <span class="mt-kind">Lesson · L9</span>
    <h4>Impedance Matching II</h4>
    <p>Impedance matching, continued. Objective 3.4.</p>
  </a>
</div>
::::

::::{frame} Lessons 10-12

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L10-smith-charts-1/index.html">
    <span class="mt-kind">Lesson · L10</span>
    <h4>Smith Charts I</h4>
    <p>The Smith chart: what it plots and how to read it. Objective 3.5.</p>
  </a>
  <a class="mt-card mt-lesson" href="L11-smith-charts-2/index.html">
    <span class="mt-kind">Lesson · L11</span>
    <h4>Smith Charts II</h4>
    <p>Working transmission-line problems on the Smith chart. Objectives 3.5, 3.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L12-smith-charts-3/index.html">
    <span class="mt-kind">Lesson · L12</span>
    <h4>Smith Charts III</h4>
    <p>Designing matching networks on the Smith chart. Objective 3.6.</p>
  </a>
</div>
::::

::::{frame} Lessons 13-15

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L13-smith-charts-4/index.html">
    <span class="mt-kind">Lesson · L13</span>
    <h4>Smith Charts IV</h4>
    <p>Matching with series components, parallel components, and stubs. Objective 3.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L14-transients/index.html">
    <span class="mt-kind">Lesson · L14</span>
    <h4>Transients</h4>
    <p>A step launched down a line: bounce diagrams and the transient response at the load. Objective 3.7.</p>
  </a>
  <a class="mt-card mt-lesson" href="L15-lab-reflection-1/index.html">
    <span class="mt-kind">Lab · L15</span>
    <h4>Reflection and Transmission Coefficient Lab I</h4>
    <p>Calibrate a vector network analyzer, then measure known loads. Objective 3.8.</p>
  </a>
</div>
::::

::::{frame} Lesson 16

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L16-lab-reflection-2/index.html">
    <span class="mt-kind">Lab · L16</span>
    <h4>Reflection and Transmission Coefficient Lab II</h4>
    <p>Characterize an unknown device from its measured reflection and transmission. Objective 3.8.</p>
  </a>
</div>
::::
