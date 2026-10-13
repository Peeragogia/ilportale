# Pi Start Prompt — Caprotti Pavilion modelling

Copy the following prompt to Pi as the operational handoff.

---

PI — START CAPROTTI PAVILION RECONSTRUCTION

You are now responsible for the first Blender reconstruction of the real **Padiglione del Tè at Parco Caprotti, Bergamo**, intended to host **Il Portale** as a civic music learning point.

## 0. Read before acting

Read the entire folder:

`docs/caprotti/`

At minimum:

- `PROJECT_ORIGIN.md`
- `PROJECT_BRIEF.md`
- `RESEARCH_REPORT.md`
- `EVIDENCE_REGISTER.md`
- `IMAGE_REFERENCE_CATALOG.md`
- `VISUAL_ANALYSIS.md`
- `MEASUREMENT_AND_SURVEY_PLAN.md`
- `BLENDER_RECONSTRUCTION_PLAN.md`
- `QUALITY_REVIEW_RUBRIC.md`

The bundled original project source is:

`docs/caprotti/source-material/Peeragogy_on_Music.pdf`

Do not treat this as optional context: it establishes the original “Learning City Point” intent and the Parco Caprotti location.

## 1. First task: critique ChatGPT’s dossier

Before modelling anything, give a practical, operational and qualitative review using `QUALITY_REVIEW_RUBRIC.md`.

You must issue:

`GO`, `CONDITIONAL GO`, or `NO-GO`

and score the dossier out of 100.

Do not be polite for the sake of agreement. Identify:

- claims that are too weak;
- missing references;
- contradictions;
- modelling instructions that are impractical;
- anything likely to waste work;
- anything that should be changed before Blender work starts.

Your review must end with **one concrete next action**.

## 2. If decision is GO or CONDITIONAL GO: create the blockout

Do NOT model a generic neo-Renaissance pavilion.

Use the real public reference images catalogued in `IMAGE_REFERENCE_CATALOG.md`.

Build a new, versioned Blender state containing:

`CAPROTTI_ARCHITECTURE`
`CONTEXT`
`REFERENCE`
`CAMERAS`

with the object naming defined in `BLENDER_RECONSTRUCTION_PLAN.md`.

### Important scale rule

We do not yet have reliable absolute dimensions.

Use a proportional system:

**best-documented principal façade width = 100 units**

Do not claim metres.
Keep the entire pavilion under one rescalable architecture root.

## 3. Model only what evidence supports

Required in first blockout:

- compact principal mass;
- tall full-arch glazed bay;
- second façade with rectangular glazed opening;
- semicircular relief-panel placeholder;
- classical column/pilaster positions;
- upper entablature/cornice;
- roof terrace and balustrade proxy;
- external stair mass;
- glazing-frame proxy;
- pond proxy;
- grotto/rockwork proxy;
- basic ground/context.

Do NOT yet:

- sculpt statues;
- model detailed capitals;
- model exact friezes;
- add photoreal materials;
- use heavy vegetation;
- redesign Il Portale;
- perform high-sample Cycles renders.

Unknown geometry must carry `_PROXY` or `_EST` naming.

## 4. Verification renders

Create and render five fast cameras:

- `EXT_FRONT_3Q`
- `EXT_STAIR_3Q`
- `EXT_POND`
- `INT_ENTRANCE`
- `INT_PORTALE_POSITION`

For each camera, identify the closest public reference and explicitly compare:

- silhouette;
- opening proportions;
- column spacing;
- terrace/balustrade;
- stair;
- context.

A beautiful render does not count as validation.

## 5. Self-review of Blender work

After the five renders, run `QUALITY_REVIEW_RUBRIC.md` again, this time on the Blender result.

Return:

```text
CAPROTTI BLOCKOUT REVIEW
Decision: GO / CONDITIONAL GO / NO-GO
Score: XX/100

Evidence fidelity: XX/25
Recognisability: XX/20
Spatial usefulness: XX/20
Modelling hygiene: XX/15
Operational safety: XX/10
Visual communication: XX/10

Strongest aspect:
...
Weakest assumption:
...
Largest visual mismatch:
...
Critical missing evidence:
...
What should NOT be modelled yet:
...
Next operational action:
...
```

## 6. Only after blockout review

If the blockout scores at least **80/100** and passes all hard gates, create a **working copy** of Il Portale and test three placements:

A. central/iconic  
B. lateral/functional  
C. integrated learning environment

Do not modify the original Portale geometry.

For each placement provide:

- top/plan view;
- entrance eye-level view;
- user interaction view;
- exterior-through-glass view;
- circulation/clearance note;
- one sentence on acoustic implications.

## 7. Stop condition

Stop after:

- dossier review;
- first pavilion blockout;
- five verification renders;
- qualitative blockout review;
- three placement studies only if the quality gate passes.

Do not drift into decorative detailing, final sky, clouds, post-processing or animation.

Those are later phases.

## 8. Required final report to Fabrizio

Keep it practical:

1. what you built;
2. what is definitely supported by evidence;
3. what remains estimated;
4. quality score and decision;
5. which photos/measurements Fabrizio should collect next;
6. exact version number of the `.blend`;
7. links/paths to the five renders;
8. one recommended next action.

---
