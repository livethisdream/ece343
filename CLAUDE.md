# ECE 343 — working notes for Claude

Course site for **ECE 343, Intro to Electromagnetics** (USAFA, Spring 2027),
taught by Maj Ellis (course director) and Dr. Neil Rogers. Jupyter Book under
`book/`, published to GitHub Pages at `livethisdream.github.io/ece343/` on
every push to `main`. 4 modules, 41 lessons, as the course ran in Spring 2025
(Neil, 2026-10-17).

**Follow ECE 444.** `livethisdream/ece444` is the model for this site's
format, conventions, and rules. Its `CLAUDE.md`, `project/ROADMAP.md`,
`COURSE_SPEC.md`, `VOICE.md`, and `REVIEW.md` apply here unless a rule is
about 444's own subject (antennas, the ADALM-PHASER, radar). The shell
(`book/_templates/`, `book/_static/`, `book/_ext/`) and `scripts/verify/` are
444's, with only what a cadet sees changed. Fix the shell in 444 first, then
copy it here.

`project/ROADMAP.md` holds this course's plan and its settled decisions. Read
it before any work.

## What is here

| Path | What |
| :-- | :-- |
| `book/moduleNN/LNN-<slug>/index.md` | the lesson page (a frame page) |
| `book/moduleNN/index.md` | module landing page, generated |
| `book/extras/legacy/*.pdf` | the Spring 2025 Beamer slides and fill-in handouts, served at `/legacy/` |
| `book/extras/handouts/*.pdf` | equation sheet and Smith charts |
| `book/extras/labs/*.pdf` | lab packets, blank copies only |
| `scripts/scaffold_lessons.py` | the manifest: lessons, objectives, readings, legacy decks |

## The manifest

`scripts/scaffold_lessons.py` is the one source for lesson numbers, titles,
objectives, readings, and which Spring 2025 deck a lesson links. It writes the
lesson pages it does not find, regenerates the module pages and
`book/_toc.yml`, and checks that every objective is taught and every linked PDF
exists. **Don't hand-edit `_toc.yml` or a module page**; edit the manifest and
re-run. The schedule and objective tables in `book/syllabus.md` and the deck
tables in `book/materials.md` were generated from it once and are now hand
maintained, so change them together with the manifest.

## Converting a lesson

Lessons move to the 444 format one at a time. **L3 and L6 are the worked
examples** (pilot, 2026-10-18): L3 for a lesson built on figures and a
derivation, L6 for one built on calculation and a widget. A converted lesson is
one bundle:

| What | Path |
| :-- | :-- |
| the frame lesson | `book/moduleNN/LNN-<slug>/index.md` (replaces the generated page) |
| its figures | `book/extras/viz/img/LNN-*.svg`, from `scripts/graphics/lNN_*.py` |
| a widget, where one earns its place | `book/extras/viz/<name>.html` |
| its practice set | `latex/ECE343_Practice_LNN.tex` |
| the built PDFs (committed) | `book/extras/practice/ECE343_LNN_Practice_{blank,SOLUTIONS}.pdf` |

Then set the lesson's decks to `[]` in the manifest and update its row in the
Spring 2025 slide tables on `book/materials.md`.

**Every derivation is shown in full** (Neil, 2026-10-19). This is where 343
departs from 444, whose spec keeps derivations short. A result the course
uses is derived on the page, step by step, as one chain from the general form
to the specific one (444's `VOICE.md` rule 19): L3 goes from Kirchhoff's laws
on a lossy section, through the difference quotient and the limit, to the
telegrapher's equations; L6 derives $\Gamma$ and the standing-wave magnitude.
Present mode shows the chain; the depth text names each step. The only results
quoted without derivation are ones that need a later chapter, and the page
says which lesson derives them (L6's coax $L'$ and $C'$).

There are **no reveal.js decks** in this course: present mode on the frame page
is the slide view. Read 444's `COURSE_SPEC.md` sections 2, 4, 5, and 8, and
`VOICE.md`, before writing; the deck section does not apply.

Before the PR, all of these pass for the lesson:

```sh
scripts/verify/check_density.py LNN       # 20 beats, 40 words a present frame
jupyter-book build book/ --all            # 0 warnings
scripts/verify/check_frames.py LNN        # every frame fits one screen
scripts/verify/check_page.py moduleNN/LNN-<slug>/index.html
scripts/verify/check_widget.py book/extras/viz/<name>.html   # if any
TEXINPUTS=<latex-tools>/tex/latex//: bash latex/build_practice.sh NN
```

Two things that bit the pilot:

- **Figures use plain Unicode labels** (ℓ, λ, Δz, R′), not matplotlib's
  `$...$` math. With `svg.fonttype: none` the math glyphs come out as the wrong
  characters in a browser. `l03_figures.py` has a `lab()` helper for a symbol
  with a subscript.
- **Write primes as `^{\prime}` in practice sets**, never `'`. A bare `R'` in
  math inside a `\question` overflows TeX's input stack with the house macros.

## Build and verify

```sh
pip install -r requirements.txt     # Python 3.10-3.12; 3.13 lacks imghdr
jupyter-book build book/ --all      # ALWAYS --all
scripts/verify/check_shell.py
scripts/verify/check_frames.py
scripts/verify/check_bar.py
```

## Public repo

This repo is **public**. LaTeX sources, assessments, keys, grades, and anything
answer-bearing live in the private `livethisdream/ece343-faculty`, never here.
Only built PDFs a cadet should see are committed. `.gitignore` blocks the usual
names, but check every PDF before adding it.

American spelling everywhere. No thin spaces. Never MATLAB for anything a cadet
runs.
