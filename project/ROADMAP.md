# ECE 343 roadmap

Last updated 2026-11-02. Read with ECE 444's `project/ROADMAP.md`, whose
working rules apply here.

## Settled (Neil, 2026-10-17)

- **Teach it the way ECE 444 is taught**: same site, shell, voice, and checks.
- **The lesson list is Spring 2025's**, 41 lessons. The 2025 Flex Day is
  calendar, not a lesson, so lessons after L14 are numbered one lower than in
  2025. Labs keep lesson numbers, as in 444's Modules 1-2.
- **Four modules**: Foundations (Ch. 1-3, L1-L16), Electrostatics (Ch. 4-5,
  L17-L26), Magnetostatics (Ch. 6-7, L27-L32), Dynamic Fields (Ch. 8-9,
  L33-L41).
- **Objectives are the Spring 2025 list**, numbered by textbook chapter
  (34 in all), so they still match the slides and the assessments.
- **Grades and weights are the same as 2025** for now: LO assessments 40%,
  GRs 20%, final exam 25%, engagement 15%.
- **The L15-L16 lab is a team lab** (Neil, 2026-10-29): two or three cadets
  to a station, one report per team for both periods, where 444's labs are
  individual. The 2027 packet keeps the 2025 procedure and fixes its errors:
  $T_L = 1 + \Gamma_L$, "Impedance", the short-circuit question, and
  Measurement 5 now measures both mismatched loads it promised, the
  $1\ \text{k}\Omega$ resistor and a complex load (the bench's $50\ \Omega$
  resistor and 470 pF capacitor in series, which rides the $r = 1$ circle).
  The source, with its key, is `Labs/ECE343_Lab_L15_L16_Reflection.tex` in
  `ece343-faculty`; its `build_lab.sh` publishes only the blank copy here.
- **The L26 Electrostatics Lab is the 2025 Python notebook, revised**
  (Neil, 2026-11-02), a team lab like L15-L16: two or three cadets, one
  report. Part A keeps the 2025 structure (Coulomb superposition on a grid:
  point charge, dipole, a line of charges, two opposite lines, a cadet
  design) and fixes its Gauss's-law test: the 2025 notebook took the 2D
  divergence of 3D point charges, which misses $\partial E_z/\partial z$ and
  reads $-Kq/r^3$, not zero. A6 now makes that trap the lesson, and A7 tests
  both forms of Gauss's law with infinite line charges, which are truly 2D.
  Part B relaxes Laplace's equation for the RG-58 cross section and gets
  $C'$ by Gauss's law (94.9 pF/m at $h = b/60$, first-order grid error,
  96.4 pF/m extrapolated, against 96.8). Part C, optional, measures $C'$ on
  the NanoVNA from two open-ended cable lengths. The blank notebook is
  `book/extras/labs/ECE343_Lab_L26_Electrostatics.ipynb` (Colab opens it from
  `main`); the source of both copies and the executed key are in
  `ece343-faculty/Labs/` (`build_l26_notebooks.py`, `lab-keys/`).
- **L16's worked marker values stand** (Neil, 2026-10-29: "if the values
  work, it's fine").
- **Every derivation is shown in full** (Neil, 2026-10-19), unlike 444. See
  `CLAUDE.md`, "Converting a lesson". L3 now derives the telegrapher's
  equations, so L4, retitled "The Wave Equation" (Neil, 2026-10-19), starts
  from them: phasor form, the wave equation, and its solution.
- **The old slides are under Materials** as PDFs (slides and fill-in
  handouts), and linked from each lesson page until it is converted. Their
  LaTeX lives in `ece343-faculty`.

## Open

- Maj Ellis's full name, office, and email (Neil to provide). Maj Ellis is
  the course director; Neil has no office this term (Neil, 2026-10-17).
- Spring 2027 meeting periods and calendar dates.
- Lab packets for the Magnetostatics (L32) and Incidence (L41) labs.
- **A possible FR4 capacitance part for L26** (Neil is considering it; he has
  copper-clad boards): measure $C$ of double-sided FR4 plates of several
  sizes, extract FR4's $\epsilon_r$ from $C$ against area, and see fringing
  raise $C$ on the small plates. It could replace or join the optional
  NanoVNA Part C. Not built.
- **Part C needs two RG-58 BNC cables of different length** (about 1 m and
  2 m) per station; confirm the lab has them before assigning it.
- **Module 1 is converted** (L1-L16, 2026-10-29). Modules 2-4 remain, on the
  same pattern (`CLAUDE.md`, "Converting a lesson").
- **The 2025 example load is $33.9 + j17.9\ \Omega$** (L8, L9, L12, L13). The
  2025 matching deck's $j17.6$ was a typo.

## Pilot lessons (2026-10-18)

L3 (The Lumped-Element Model) and L6 (Coaxial Lines, Reflection Coefficient,
and VSWR) are converted as the worked examples for later lesson threads: frame
page, figures or widget, and a practice set with both PDFs. Decisions from the
pilot:

- **No reveal.js decks** (Neil, 2026-10-18). Present mode is the slide view.
- **Practice solutions are public**, as in 444 (Neil, 2026-10-18). Assessments
  and keys stay in `ece343-faculty`.
- **RG-58 is the course's reference cable**: $a = 0.405$ mm, $b = 1.475$ mm,
  $\epsilon_r = 2.25$, giving $Z_0 = 51.7\ \Omega$, $L' = 259$ nH/m,
  $C' = 96.8$ pF/m, $v_p = 2 \times 10^8$ m/s. L3 and L6 quote these numbers.
- **The $\lambda/10$ rule of thumb** for when a connection is an ideal wire (L3).
- The 2025 reflection-coefficient deck wrote $\Gamma(z) = \vert\Gamma_L\vert e^{2\gamma z}$.
  The magnitude bars drop the phase of $\Gamma_L$; the general form is
  $\Gamma_L e^{2\gamma z}$, which L6 writes as $\Gamma_L e^{j2\beta z}$ for a
  lossless line.
