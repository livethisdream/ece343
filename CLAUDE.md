# ECE 343 — working notes for Claude

Course site for **ECE 343, Intro to Electromagnetics** (USAFA, Spring 2027),
taught by Dr. Neil Rogers (course director) and Maj Ellis. Jupyter Book under
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

Lessons move to the 444 format one at a time. A converted lesson replaces its
generated page (title, objectives, legacy slides, reading) with a real frame
lesson, following 444's `book/module01/L05-field-regions/` as the worked
example and 444's budgets and checks. Keep the Spring 2025 slide links until
the new material covers the same ground. Then set the lesson's decks to `[]`
in the manifest.

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
