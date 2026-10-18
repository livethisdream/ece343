# ECE 343 roadmap

Last updated 2026-10-18. Read with ECE 444's `project/ROADMAP.md`, whose
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
- **The old slides are under Materials** as PDFs (slides and fill-in
  handouts), and linked from each lesson page until it is converted. Their
  LaTeX lives in `ece343-faculty`.

## Open

- Maj Ellis's full name, office, and email (Neil to provide). Maj Ellis is
  the course director; Neil has no office this term (Neil, 2026-10-17).
- Spring 2027 meeting periods and calendar dates.
- Lab packets for the Electrostatics (L26), Magnetostatics (L32), and
  Incidence (L41) labs, and the 2027 Reflection Coefficient packet.
- Convert the remaining lessons to the 444 format, one at a time, on the
  pattern of the L3 and L6 pilots (`CLAUDE.md`, "Converting a lesson").

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
