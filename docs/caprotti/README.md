# Padiglione del Tè — Parco Caprotti
## Reconstruction dossier for Il Portale

**Status:** Research + design basis v0.3  
**Date:** 2026-10-13  
**Project:** Il Portale — civic music learning point  
**Target site:** Padiglione del Tè, Parco Caprotti, Bergamo

This folder is the evidence and design basis for reconstructing the real Tea Pavilion in Blender and testing the installation of **Il Portale** inside it.

The reconstruction must remain traceable: every claim is classified as `OBSERVED`, `INFERRED`, or `UNKNOWN`. The model is allowed to be provisional; the documentation is not allowed to hide uncertainty.

## Why this site matters

The site is not a later aesthetic choice. The original Il Portale paper already framed the proposal as a **“Learning City Point”**, located at **Parco Comunale “dei Caprotti”, Bergamo, Via Tasso**, and described the solution as creating opportunities to learn music modules in a peeragogical style. See [`PROJECT_ORIGIN.md`](PROJECT_ORIGIN.md) and the bundled original source PDF.

## Folder map

- [`PROJECT_ORIGIN.md`](PROJECT_ORIGIN.md) — what the original 2013/2016 project actually proposed.
- [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md) — updated design mission.
- [`RESEARCH_REPORT.md`](RESEARCH_REPORT.md) — historical/context research and conclusions.
- [`SOURCE_REGISTER.md`](SOURCE_REGISTER.md) — sources and what each one supports.
- [`EVIDENCE_REGISTER.md`](EVIDENCE_REGISTER.md) — claim-by-claim evidence status.
- [`IMAGE_REFERENCE_CATALOG.md`](IMAGE_REFERENCE_CATALOG.md) — visual board with public references and source notes.
- [`VISUAL_ANALYSIS.md`](VISUAL_ANALYSIS.md) — architectural reading of the pavilion.
- [`MEASUREMENT_AND_SURVEY_PLAN.md`](MEASUREMENT_AND_SURVEY_PLAN.md) — how to turn field photos into usable geometry.
- [`BLENDER_RECONSTRUCTION_PLAN.md`](BLENDER_RECONSTRUCTION_PLAN.md) — modelling sequence and scene structure.
- [`QUALITY_REVIEW_RUBRIC.md`](QUALITY_REVIEW_RUBRIC.md) — practical/operational quality gate for Pi.
- [`PI_START_PROMPT.md`](PI_START_PROMPT.md) — exact prompt for Pi to begin.
- [`DECISIONS_AND_OPEN_QUESTIONS.md`](DECISIONS_AND_OPEN_QUESTIONS.md) — decisions, uncertainties and research gaps.
- [`reference-manifest.schema.json`](reference-manifest.schema.json) — machine-readable reference metadata.

## Session log

- [`SESSION_2026-10-13.md`](../SESSION_2026-10-13.md) — blockout v1 (0044.blend), 5 renders Eevee, auto-review (76/100), GUI fix.

## Renders di verifica

I renders blockout sono in `/workspace/renders/` (sul server):

| Vista | Dimensione | Note |
|-------|:----------:|------|
| EXT_FRONT_3Q | 297 KB | ✅ Facciata principale 3/4 |
| EXT_STAIR_3Q | 178 KB | ✅ Scala laterale 3/4 |
| EXT_POND | 79 KB | ✅ Vista dallo stagno |
| INT_ENTRANCE | 33 KB | ⚠️ Buio — manca illuminazione interna |
| INT_PORTALE_POSITION | 66 KB | ⚠️ Buio — manca illuminazione interna |

## Image policy

Public reference photographs are **linked, not redistributed**, unless licensing is explicitly known. This keeps provenance clear and avoids copying third-party image files into the repository. The folder `images/` contains only material generated from the user-owned Il Portale PDF and original project diagrams.

## Modelling principle

> **Reconstruct the specific Padiglione del Tè, not a generic neo-Renaissance pavilion.**
>The first goal is recognisable geometry and spatial feasibility, not decorative perfection.
