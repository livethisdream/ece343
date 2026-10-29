#!/usr/bin/env python3
"""Scaffold the ECE 343 lesson pages, module pages, and TOC from one manifest.

For each lesson in LESSONS that does not already exist, this writes
  book/moduleNN/<slug>/index.md     a frame page: title, objectives, the
                                    Spring 2025 slides, and the reading

It also rewrites every module landing page (book/moduleNN/index.md) and
book/_toc.yml. Existing lesson pages are left UNTOUCHED unless --force is
passed, so a lesson that has since been converted to the ECE 444 format is
safe to re-run over. Module pages are regenerated every run until one is hand
written; set generate_index=False on it in MODULES when that happens.

No reveal.js decks are generated yet. The course still teaches from the
Spring 2025 Beamer slides, linked from each lesson page as PDFs under
book/extras/legacy/; a lesson gets a deck when it is converted.

The manifest is the single source of truth for lesson numbers, titles,
objectives, readings, and which legacy deck a lesson uses. Edit it and re-run.

Usage:
    python scripts/scaffold_lessons.py            # create missing pages + modules + toc
    python scripts/scaffold_lessons.py --force    # also overwrite existing lesson pages (careful!)
    python scripts/scaffold_lessons.py --dry-run  # print what would happen, write nothing
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOK = REPO / "book"
LEGACY = BOOK / "extras" / "legacy"

COURSE = "ECE 343"
COURSE_TITLE = "Intro to Electromagnetics"
TERM = "Spring 2027"
INSTRUCTORS = "Maj Ellis · Dr. Neil Rogers"

# ---- Learning objectives, verbatim from the Spring 2025 syllabus ------------
# Numbered by textbook chapter (Ellingson, Vol. 1), as the slides and the
# assessments in ece343-faculty are. Two misspellings in the 2025 list
# ("Coloumb", "varoius") are corrected; nothing else is changed.
LO_TEXT = {
    "1.1": "I can articulate what I will learn and how I will be assessed in this course.",
    "1.2": "I can articulate practical applications of electromagnetics.",
    "2.1": "I can recall the definition of scalar fields, vector fields, phasors, and Euler's identity.",
    "2.2": "I can explain the basic terms and quantities used to describe electromagnetic fields.",
    "3.1": "I can describe the origin of the transmission line equation, understand the method of developing a solution, and interpret the solution.",
    "3.2": "I can explain the physical meaning of and calculate the following quantities: propagation constant, phase constant, attenuation constant, characteristic impedance, VSWR, reflection coefficient, and transmission coefficient.",
    "3.3": "I can use the transmission line equation to calculate the voltage/current at an arbitrary point on a specified transmission line.",
    "3.4": "I can use the transmission line equation to match a load to a source using a length of transmission line.",
    "3.5": "I can identify the various quantities represented on the Smith Chart.",
    "3.6": "I can use a Smith Chart to design a matching network for a given source and load, using series components, parallel components, shorted stubs, and open stubs.",
    "3.7": "I can plot the transient response of a load connected to a source through a transmission line.",
    "3.8": "I can measure the reflection coefficient across a range of frequencies and interpret the measurement using a network analyzer.",
    "4.1": "I can recognize and apply common vector calculus operations, such as: gradient, divergence, curl, and Laplacian in the three major coordinate systems.",
    "4.2": "I can calculate surface and volume integrals in rectangular, cylindrical, and spherical coordinate systems.",
    "4.3": "I can differentiate between Stoke's Theorem and the Divergence Theorem and apply them to various problems to simplify integrals.",
    "5.1": "I can apply Coulomb's Law to use direct integration to calculate the electric field due to charge density in various geometries, including rectangular, cylindrical, and spherical coordinate systems.",
    "5.2": "I can apply the integral and differential forms of Gauss' Law to calculate the electric field due to charge density in various geometries, including rectangular, cylindrical, and spherical coordinate systems.",
    "5.3": "I can calculate the electric field from the scalar electric potential in a variety of geometries.",
    "5.4": "I can apply the electric field boundary conditions to calculate electric fields on both sides of a material boundary.",
    "6.1": "I can calculate the total current through a surface area given a current distribution.",
    "6.2": "I can use Ohm's Law for electromagnetics to calculate the relationship between a current distribution and an electric field.",
    "6.3": "I can articulate and identify what makes a material a good conductor and how conductivity relates to resistance.",
    "7.1": "I can use the Biot-Savart law to simple magnetostatic systems to find the magnetic field at an observation point.",
    "7.2": "I can articulate the meaning of both the integral form and point form of Gauss' Law for magnetism.",
    "7.3": "I can use Ampere's Law to calculate the magnetic field at an observation point for simple magnetostatic systems.",
    "7.4": "I can apply the magnetic field boundary conditions to calculate magnetic fields on both sides of a material boundary.",
    "8.1": "I can articulate the significance of the displacement current and calculate it, given a time-varying electric field.",
    "8.2": "I can articulate the meaning of and calculate the relaxation time for a variety of materials.",
    "8.3": "I know the forms of Maxwell's equations for time-varying fields and use them to calculate electric and magnetic fields for a variety of physical systems.",
    "9.1": "I understand the process of decoupling and finding solutions for Maxwell's equations for dynamic fields.",
    "9.2": "I can articulate what a Uniform Plane Wave (UPW) is and describe key properties that relate the electric and magnetic field.",
    "9.3": "I can calculate the electric and magnetic fields for a UPW.",
    "9.4": "I can articulate the concept of polarization and determine the polarization for various UPWs.",
    "9.5": "I can determine the reflection and transmission of UPW at a boundary for Transverse Electric (TE) and Transverse Magnetic (TM) waves, using boundary conditions.",
}

CHAPTERS = {
    1: "Introduction",
    2: "Fields",
    3: "Transmission Lines",
    4: "Vector Analysis",
    5: "Electrostatics",
    6: "Steady Current and Conductivity",
    7: "Magnetostatics",
    8: "Dynamic Fields",
    9: "Plane Waves",
}

# ---- Module metadata (Neil, 2026-10-17) ------------------------------------
MODULES = {
    1: dict(
        name="Foundations",
        caption="Module 1 — Foundations",
        chapters=[1, 2, 3],
        tagline="Fields, phasors, and the transmission line: the first place a circuit stops behaving like one.",
        synopsis="What electromagnetics is for, the language of fields and phasors, and the transmission line: wave propagation, reflection, impedance matching, the Smith chart, and transients, measured on a network analyzer in the first lab.",
        generate_index=True,
    ),
    2: dict(
        name="Electrostatics",
        caption="Module 2 — Electrostatics",
        chapters=[4, 5],
        tagline="Charges at rest, and the vector calculus that describes their fields.",
        synopsis="The vector calculus the rest of the course runs on, then the electric field of charges at rest: Coulomb's law, Gauss' law, potential, boundary value problems, boundary conditions, and capacitance.",
        generate_index=True,
    ),
    3: dict(
        name="Magnetostatics",
        caption="Module 3 — Magnetostatics",
        chapters=[6, 7],
        tagline="Charges in steady motion, and the magnetic fields they make.",
        synopsis="Steady current and conductivity, then the magnetic field of steady currents: Biot-Savart, Gauss' law for magnetism, Ampere's law, and magnetic boundary conditions.",
        generate_index=True,
    ),
    4: dict(
        name="Dynamic Fields",
        caption="Module 4 — Dynamic Fields",
        chapters=[8, 9],
        tagline="Let the fields change in time, and they leave as a wave.",
        synopsis="Faraday's law, displacement current, and the full set of Maxwell's equations, then the uniform plane wave they predict: its properties, its polarization, and what happens when it meets a boundary.",
        generate_index=True,
    ),
}

# ---- Legacy decks: the Spring 2025 Beamer PDFs under book/extras/legacy/ ----
# key -> (label, [files]). A deck may serve several lessons.
DECKS = {
    "D01-1": ("Course Introduction", ["ECE343_D01-1_Intro_Slides.pdf"]),
    "D01-2": ("Why Electromagnetics", ["ECE343_D01-2_Motivation_Slides.pdf"]),
    "D02": ("Review and Fields", ["ECE343_D02_Fields_Slides.pdf", "ECE343_D02_Fields_Handouts.pdf"]),
    "D03-1": ("Transmission Line Equations", ["ECE343_D03-1_TxLinesIntro_Slides.pdf"]),
    "D03-2": ("Reflection and Transmission Coefficients", ["ECE343_D03-2_ReflectionCoefficients_Slides.pdf"]),
    "D03-3": ("Impedance Matching", ["ECE343_D03-3_ImpedanceMatching_Slides.pdf", "ECE343_D03-3_ImpedanceMatching_Handouts.pdf"]),
    "D03-4": ("Smith Charts", ["ECE343_D03-4_SmithCharts_Slides.pdf"]),
    "D03-5": ("Transients", ["ECE343_D03-5_Transients_Slides.pdf"]),
    "D04": ("Vector Analysis", ["ECE343_D04_VectorAnalysis_Handouts.pdf"]),
    "D05-1": ("Coulomb's Law", ["ECE343_D05-1_Coulomb_Slides.pdf", "ECE343_D05-1_Coulomb_Handouts.pdf"]),
    "D05-2": ("Gauss' Law", ["ECE343_D05-2_Gauss_Slides.pdf", "ECE343_D05-2_Gauss_Handouts.pdf"]),
    "D05-3": ("Electric Field from Potential", ["ECE343_D05-3_EfromV_Slides.pdf", "ECE343_D05-3_EfromV_Handouts.pdf"]),
    "D05-4": ("Electric Boundary Conditions", ["ECE343_D05-4_EBoundaries_Slides.pdf", "ECE343_D05-4_EBoundaries_Handouts.pdf"]),
    "D06": ("Current Density", ["ECE343_D06_CurrentDensity_Slides.pdf", "ECE343_D06_CurrentDensity_Handouts.pdf"]),
    "D07-1": ("Biot-Savart Law", ["ECE343_D07-1_BiotSavart_Slides.pdf", "ECE343_D07-1_BiotSavart_Handouts.pdf"]),
    "D07-2": ("Gauss' Law for Magnetism", ["ECE343_D07-2_GaussMagnetism_Slides.pdf"]),
    "D07-3": ("Ampere's Law", ["ECE343_D07-3_Ampere_Slides.pdf", "ECE343_D07-3_Ampere_Handouts.pdf"]),
    "D07-4": ("Magnetic Boundary Conditions", ["ECE343_D07-4_HBoundaries_Slides.pdf", "ECE343_D07-4_HBoundaries_Handouts.pdf"]),
    "D08-1": ("Displacement Current", ["ECE343_D08-1_DisplacementCurrent_Slides.pdf", "ECE343_D08-1_DisplacementCurrent_Handouts.pdf"]),
    "D08-2": ("Maxwell's Equations", ["ECE343_D08-2_Maxwell_Slides.pdf", "ECE343_D08-2_Maxwell_Handouts.pdf"]),
    "D09-1": ("The Helmholtz Equation", ["ECE343_D09-1_Helmholtz_Slides.pdf", "ECE343_D09-1_Helmholtz_Handouts.pdf"]),
    "D09-2": ("Uniform Plane Waves", ["ECE343_D09-2_UPWCharacteristics_Slides.pdf", "ECE343_D09-2_UPWCharacteristics_Handouts.pdf"]),
    "D09-3": ("Polarization", ["ECE343_D09-3_Polarization_Slides.pdf", "ECE343_D09-3_Polarization_Handouts.pdf"]),
    "D09-4": ("Plane Waves at a Boundary", ["ECE343_D09-4_UPWBoundaries_Slides.pdf", "ECE343_D09-4_UPWBoundaries_Handouts.pdf"]),
}

LAB_PACKET = "../../labs/ECE343_Lab_ReflectionCoefficients_Spring2025.pdf"

# ---- Lesson manifest: the Spring 2025 course as taught (Neil, 2026-10-17) ---
# (module, num, slug, title, [lo_ids], reading, [deck keys], synopsis, event)
# The 2025 calendar had 42 periods; its Flex Day (old L15) is calendar, not a
# lesson, so everything after L14 is one lower than in 2025. Readings are
# Ellingson Vol. 1 sections unless they say otherwise.
LESSONS = [
    (1, 1, "L01-course-intro", "Course Introduction", ["1.1", "1.2"], "Ch. 1", ["D01-1", "D01-2"], "What you will learn, how you will be assessed, and where electromagnetics shows up in the systems you will operate.", ""),
    (1, 2, "L02-fields", "Fields, Parameters, and Field Quantities", ["2.1", "2.2"], "Ch. 2", ["D02"], "Scalar and vector fields, phasors and Euler's identity, and the quantities that describe electric and magnetic fields.", ""),
    (1, 3, "L03-lumped-element-model", "The Lumped-Element Model", ["3.1"], "3.1–3.4", [], "When a pair of wires stops being a short circuit, and how to model a line as a cascade of tiny circuits.", ""),
    (1, 4, "L04-wave-equation", "The Wave Equation", ["3.1"], "3.5–3.6", [], "The telegrapher's equations in phasor form, the wave equation for voltage and current, and its traveling-wave solution.", ""),
    (1, 5, "L05-characteristic-impedance", "Characteristic Impedance and Wave Propagation", ["3.2"], "3.7–3.9", [], "Propagation, phase, and attenuation constants, and the characteristic impedance of a line.", ""),
    (1, 6, "L06-reflection-vswr", "Coaxial Lines, Reflection Coefficient, and VSWR", ["3.2", "3.3"], "3.10, 3.12–3.14", [], "The coaxial line, the reflection coefficient at a load, standing waves, and VSWR.", ""),
    (1, 7, "L07-terminated-lines", "Terminated Transmission Lines", ["3.3", "3.4"], "3.15, 3.17–3.19", ["D03-3"], "Input impedance of a terminated line, and the special cases: shorted, open, and quarter-wave lines.", ""),
    (1, 8, "L08-impedance-matching-1", "Impedance Matching I", ["3.4"], "3.21–3.23", ["D03-3"], "Matching a load to a source with a length of transmission line.", ""),
    (1, 9, "L09-impedance-matching-2", "Impedance Matching II", ["3.4"], "3.21–3.23", ["D03-3"], "Impedance matching, continued.", ""),
    (1, 10, "L10-smith-charts-1", "Smith Charts I", ["3.5"], "Supplemental", ["D03-4"], "The Smith chart: what it plots and how to read it.", ""),
    (1, 11, "L11-smith-charts-2", "Smith Charts II", ["3.5", "3.6"], "Supplemental", ["D03-4"], "Working transmission-line problems on the Smith chart.", ""),
    (1, 12, "L12-smith-charts-3", "Smith Charts III", ["3.6"], "Supplemental", ["D03-4"], "Designing matching networks on the Smith chart.", ""),
    (1, 13, "L13-smith-charts-4", "Smith Charts IV", ["3.6"], "Supplemental", ["D03-4"], "Matching with series components, parallel components, and stubs.", ""),
    (1, 14, "L14-transients", "Transients", ["3.7"], "Supplemental", ["D03-5"], "A step launched down a line: bounce diagrams and the transient response at the load.", ""),
    (1, 15, "L15-lab-reflection-1", "Reflection and Transmission Coefficient Lab I", ["3.8"], "Lab packet", [], "Calibrate a vector network analyzer, then measure known loads.", "lab"),
    (1, 16, "L16-lab-reflection-2", "Reflection and Transmission Coefficient Lab II", ["3.8"], "Lab packet", [], "Characterize an unknown device from its measured reflection and transmission.", "lab"),

    (2, 17, "L17-vector-analysis", "Vector and Coordinate System Review", ["4.1", "4.2", "4.3"], "Ch. 4", ["D04"], "Gradient, divergence, curl, and the Laplacian in three coordinate systems; surface and volume integrals; Stokes' and the divergence theorem.", "GR 1 due"),
    (2, 18, "L18-coulombs-law", "Coulomb's Law", ["5.1"], "5.1–5.3", ["D05-1"], "The electric field of point charges, by superposition.", ""),
    (2, 19, "L19-charge-distributions", "Surface and Volume Charge", ["5.1"], "5.4", ["D05-1"], "The field of a charge distribution, by direct integration.", ""),
    (2, 20, "L20-gauss-integral", "Gauss' Law (Integral Form)", ["5.2"], "5.5–5.6", ["D05-2"], "Using symmetry and a Gaussian surface to find the field without integrating Coulomb's law.", ""),
    (2, 21, "L21-gauss-differential", "Gauss' Law (Differential Form)", ["5.2"], "5.7–5.8", ["D05-2"], "The point form of Gauss' law, and charge density from a known field.", ""),
    (2, 22, "L22-electric-potential", "Electric Potential", ["5.3"], "5.9–5.10, 5.15", ["D05-3"], "Work, potential, and the electric field as the gradient of the potential.", ""),
    (2, 23, "L23-boundary-value-problems", "Boundary Value Problems and Electric Potential", ["5.3"], "5.16", ["D05-3"], "Laplace's equation for the parallel-plate capacitor and the coaxial line.", ""),
    (2, 24, "L24-electric-boundary-conditions", "Electric Boundary Conditions", ["5.4"], "5.18–5.22", ["D05-4"], "Conductors, dielectrics, and the field on both sides of a material boundary.", ""),
    (2, 25, "L25-capacitance", "Boundary Conditions and Capacitance", ["5.4"], "5.23–5.24", ["D05-4"], "Capacitance from the field, and boundary conditions put to work.", ""),
    (2, 26, "L26-lab-electrostatics", "Electrostatics Lab", ["5.1", "5.2", "5.3", "5.4"], "Lab packet", [], "The Module 2 lab. Packet to be posted.", "lab"),

    (3, 27, "L27-current-density", "Current Density, Conductivity, and Resistance", ["6.1", "6.2", "6.3"], "Ch. 6", ["D06"], "Current through a surface, Ohm's law in point form, and what makes a good conductor.", ""),
    (3, 28, "L28-magnetic-fields", "Magnetic Fields and Gauss' Law for Magnetism", ["7.1", "7.2"], "7.1–7.3", ["D07-1", "D07-2"], "The Biot-Savart law, and why magnetic field lines always close.", "GR 2"),
    (3, 29, "L29-amperes-law", "Ampere's Law", ["7.3"], "7.4–7.5, 7.9", ["D07-3"], "Integral and point forms of Ampere's law, and the field of a line current.", ""),
    (3, 30, "L30-amperes-law-applied", "Ampere's Law Applied", ["7.3"], "7.6–7.8", ["D07-3"], "Ampere's law applied to practical current distributions.", ""),
    (3, 31, "L31-magnetic-boundary-conditions", "Magnetic Boundary Conditions", ["7.4"], "7.10–7.14", ["D07-4"], "Magnetic materials, and the field on both sides of a boundary.", ""),
    (3, 32, "L32-lab-magnetostatics", "Magnetostatics Lab", ["7.1", "7.2", "7.3", "7.4"], "Lab packet", [], "The Module 3 lab. Packet to be posted.", "lab"),

    (4, 33, "L33-displacement-current", "Faraday's Law and Displacement Current", ["8.1", "8.2"], "8.3, 8.8, 8.9", ["D08-1"], "Induction, the displacement current that completes Ampere's law, and relaxation time.", ""),
    (4, 34, "L34-maxwells-equations", "Maxwell's Equations", ["8.3"], "8.3, 8.8, 8.9", ["D08-2"], "The full set of Maxwell's equations for time-varying fields.", ""),
    (4, 35, "L35-source-free-maxwell-1", "Maxwell's Equations in a Lossless, Source-Free Region I", ["9.1"], "9.1–9.2", ["D09-1"], "Decoupling Maxwell's equations for time-varying fields.", ""),
    (4, 36, "L36-source-free-maxwell-2", "Maxwell's Equations in a Lossless, Source-Free Region II", ["9.1"], "9.1–9.2", ["D09-1"], "The Helmholtz equation and its solutions, continued.", ""),
    (4, 37, "L37-plane-waves-polarization", "Uniform Plane Waves and Polarization", ["9.2", "9.3", "9.4"], "9.4–9.6", ["D09-2", "D09-3"], "The uniform plane wave, the fields that make it up, and its polarization.", ""),
    (4, 38, "L38-normal-incidence", "Normal Incidence", ["9.5"], "Vol. 2, 5.6–5.7", ["D09-4"], "A plane wave striking a boundary head-on: reflection and transmission.", ""),
    (4, 39, "L39-oblique-incidence-1", "Oblique Incidence I", ["9.5"], "Vol. 2, 5.6–5.7", ["D09-4"], "A plane wave meeting a boundary at an angle.", ""),
    (4, 40, "L40-oblique-incidence-2", "Oblique Incidence II", ["9.5"], "Vol. 2, 5.6–5.7", ["D09-4"], "Oblique incidence, continued: TE and TM waves.", ""),
    (4, 41, "L41-lab-incidence", "Incidence Lab", ["9.5"], "Lab packet", [], "Reflection and transmission at a boundary. Packet to be posted.", "lab"),
]


def lo_list_html(lo_ids, indent="  "):
    """Group the objectives by chapter; each <ol> numbers itself as C.k."""
    out, run = [], []
    for i in lo_ids + [None]:
        if run and (i is None or i.split(".")[0] != run[0].split(".")[0]):
            ch, first = run[0].split(".")
            reset = f"; counter-reset: lo {int(first) - 1}" if int(first) > 1 else ""
            items = "\n".join(f"{indent}<li>{LO_TEXT[x]}</li>" for x in run)
            out.append(f'<ol class="lo-list" style="--module: \'{ch}\'{reset}">\n{items}\n</ol>')
            run = []
        if i is not None:
            run.append(i)
    return "\n\n".join(out)


def obj_label(lo_ids):
    return ("Objective " if len(lo_ids) == 1 else "Objectives ") + ", ".join(lo_ids)


def reading_text(reading):
    if reading == "Lab packet":
        return "The lab packet, start to finish, before the period."
    if reading == "Supplemental":
        return "Supplemental: the Smith chart handouts on the [materials page](../../materials.md)."
    if reading.startswith("Vol. 2"):
        return f"Ellingson, *Electromagnetics*, Vol. 2, sections {reading[len('Vol. 2, '):]}."
    if reading.startswith("Ch."):
        return f"Ellingson, *Electromagnetics*, Vol. 1, Chapter {reading[4:]}."
    return f"Ellingson, *Electromagnetics*, Vol. 1, sections {reading}."


def legacy_links(decks, num):
    lines = []
    for key in decks:
        label, files = DECKS[key]
        for f in files:
            kind = "fill-in handout" if f.endswith("_Handouts.pdf") else "slides"
            lines.append(f'- <a class="doc-link" href="../../legacy/{f}" target="_blank" rel="noopener">{label}, {kind} (PDF)</a>')
    if num in (15, 16):
        lines.append(f'- <a class="doc-link" href="{LAB_PACKET}" target="_blank" rel="noopener">Reflection and Transmission Coefficient Lab packet, Spring 2025 (PDF)</a>')
    return "\n".join(lines)


def lesson_index_md(mnum, num, title, lo_ids, reading, decks, synopsis, event):
    m = MODULES[mnum]
    links = legacy_links(decks, num)
    if links:
        slides = f"""::::{{frame}} Spring 2025 Slides
:class: read-only doc-links

{links}

:::{{depth}}
These are last year's Beamer slides, posted as they were taught while this
lesson is converted to the new format. The fill-in handout, where there is
one, is the copy to print and bring to class.
:::
::::
"""
    else:
        slides = """::::{frame} Lab Packet
:class: read-only

The Spring 2027 packet for this lab will be posted here before the period.
::::
"""
    ev = f" · **{event}**" if event and event != "lab" else ""
    return f"""---
frame_view: true
---

# L{num} - {title}

::::{{frame}}
:class: title-frame

<div class="course-mark">{COURSE} · {TERM}</div>

<h1 class="frame-title">{title}</h1>

<div class="title-rule"></div>

{synopsis}

Lesson {num} · Module {mnum}: {m['name']} · {INSTRUCTORS}
::::

::::{{frame}} Learning Objectives

{lo_list_html(lo_ids)}
::::

{slides}
::::{{frame}} Reading
:class: read-only

{reading_text(reading)}{ev}
::::

::::{{frame}} Under Construction
:class: read-only

This lesson is being converted to the new course format. The objectives and
reading above are current; the notes, slides, and practice problems will
replace the Spring 2025 material as they are finished.
::::
"""


def module_index_md(mnum):
    m = MODULES[mnum]
    lessons = [x for x in LESSONS if x[0] == mnum]
    first, last = lessons[0][1], lessons[-1][1]
    los = [lo for lo in LO_TEXT if int(lo.split(".")[0]) in m["chapters"]]
    lo_frames = []
    for ch in m["chapters"]:
        ch_los = [lo for lo in los if lo.startswith(f"{ch}.")]
        # Four objectives a frame at most, or a present-mode frame overflows.
        for k in range(0, len(ch_los), 4):
            part = ch_los[k:k + 4]
            rng = "" if len(ch_los) <= 4 else f" ({part[0]}-{part[-1]})"
            lo_frames.append(f"""::::{{frame}} Chapter {ch}: {CHAPTERS[ch]}{rng}

{lo_list_html(part)}
::::
""")
    cards = []
    for (_, num, slug, title, lo_ids, reading, _d, synopsis, event) in lessons:
        kind = "Lab" if event == "lab" else "Lesson"
        cards.append(
            f"""  <a class="mt-card mt-lesson" href="{slug}/index.html">
    <span class="mt-kind">{kind} · L{num}</span>
    <h4>{title}</h4>
    <p>{synopsis} {obj_label(lo_ids)}.</p>
  </a>"""
        )
    card_frames = []
    for k in range(0, len(cards), 3):
        chunk = lessons[k:k + 3]
        a, b = chunk[0][1], chunk[-1][1]
        rng = f"Lesson {a}" if a == b else f"Lessons {a}-{b}"
        body = "\n".join(cards[k:k + 3])
        card_frames.append(f"""::::{{frame}} {rng}

<div class="module-toc">
{body}
</div>
::::
""")
    return f"""---
frame_view: true
nav: {m['name']}
---

# Module {mnum} — {m['name']}

::::{{frame}}
:class: title-frame

<div class="course-mark">{COURSE} · Module {mnum:02d}</div>

<h1 class="frame-title">{m['name']}</h1>

<div class="title-rule"></div>

{m['tagline']}

Lessons {first}–{last} · {COURSE_TITLE} · {INSTRUCTORS}
::::

::::{{frame}} Where This Module Goes
{m['synopsis']}
::::

{chr(10).join(lo_frames)}
{chr(10).join(card_frames)}"""


def toc_yaml():
    lines = [
        "# Table of contents for ECE 343.",
        "# Generated by scripts/scaffold_lessons.py from the LESSONS manifest.",
        "# Re-run that script after editing the manifest; hand edits here will be overwritten.",
        "",
        "format: jb-book",
        "root: intro",
        "",
        "parts:",
        "  - caption: Course Information",
        "    chapters:",
        "      - file: syllabus",
        "      - file: materials",
    ]
    for mnum, m in MODULES.items():
        lines += ["", f"  - caption: {m['caption']}", "    chapters:",
                  f"      - file: module{mnum:02d}/index", f"        title: Module {mnum} overview"]
        for (_, num, slug, title, *_rest) in [x for x in LESSONS if x[0] == mnum]:
            lines.append(f"      - file: module{mnum:02d}/{slug}/index")
            lines.append(f'        title: "L{num} — {title}"')
    return "\n".join(lines) + "\n"


def write(path: Path, content: str, force: bool, dry: bool, kind: str):
    exists = path.exists()
    if exists and not force:
        print(f"  skip (exists): {path.relative_to(REPO)}")
        return False
    print(f"  {'overwrite' if exists else 'write'} {kind}: {path.relative_to(REPO)}")
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return True


def check_manifest():
    nums = [x[1] for x in LESSONS]
    assert nums == list(range(1, len(LESSONS) + 1)), "lesson numbers must run 1..N with no gaps"
    for x in LESSONS:
        for lo in x[4]:
            assert lo in LO_TEXT, f"L{x[1]}: unknown objective {lo}"
        for d in x[6]:
            assert d in DECKS, f"L{x[1]}: unknown deck {d}"
    for key, (_label, files) in DECKS.items():
        for f in files:
            assert (LEGACY / f).exists(), f"{key}: missing {f}"
    taught = {lo for x in LESSONS for lo in x[4]}
    missing = sorted(set(LO_TEXT) - taught)
    assert not missing, f"objectives no lesson serves: {missing}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="overwrite existing lesson pages")
    ap.add_argument("--dry-run", action="store_true", help="print actions, write nothing")
    args = ap.parse_args()
    check_manifest()

    print("== Lesson pages ==")
    for (mnum, num, slug, title, lo_ids, reading, decks, synopsis, event) in LESSONS:
        idx = BOOK / f"module{mnum:02d}" / slug / "index.md"
        write(idx, lesson_index_md(mnum, num, title, lo_ids, reading, decks, synopsis, event),
              args.force, args.dry_run, "lesson")

    print("== Module landing pages ==")
    for mnum, m in MODULES.items():
        if not m.get("generate_index"):
            print(f"  skip module {mnum} index (hand-written)")
            continue
        write(BOOK / f"module{mnum:02d}" / "index.md", module_index_md(mnum), True, args.dry_run, "module")

    print("== _toc.yml ==")
    write(BOOK / "_toc.yml", toc_yaml(), True, args.dry_run, "toc")
    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
