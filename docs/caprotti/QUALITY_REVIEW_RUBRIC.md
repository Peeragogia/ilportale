# Quality Review Rubric — Pi must judge before and after modelling

This is not a ceremonial checklist. Pi must use it to criticise the dossier and its own Blender output.

## Hard gates — any failure blocks progression

1. **Identity gate:** the model must represent the actual Padiglione del Tè, not a generic historical pavilion.
2. **Evidence gate:** unsupported details must be labelled provisional; no invented “historic facts”.
3. **Versioning gate:** original Portale and source model remain recoverable.
4. **Geometry gate:** major openings, roof terrace, external stair and façade hierarchy must match the visual evidence well enough to be recognisable.
5. **Spatial gate:** claims about Portale fit must not be made before metric calibration or clearly labelled as provisional.

## Weighted score — 100 points

### A. Evidence fidelity — 25
- 0–5: generic/invented
- 6–15: partially evidence-based but gaps hidden
- 16–21: major decisions traceable
- 22–25: excellent provenance and uncertainty discipline

### B. Recognisability — 20
Does someone familiar with the pavilion immediately recognise it from silhouette, bay rhythm, arch, stair and terrace?

### C. Spatial usefulness — 20
Does the model actually help test circulation, visibility and Portale placement rather than merely look attractive?

### D. Modelling hygiene — 15
Naming, collections, transforms, instancing, editable geometry, low unnecessary complexity.

### E. Reversibility / operational safety — 10
Versioning, audit trail, original preservation, easy rollback.

### F. Visual communication — 10
Do the review renders expose problems clearly? Beauty is secondary to legibility at blockout stage.

## Rating

- **90–100:** excellent; proceed
- **80–89:** strong; proceed with listed corrections
- **70–79:** usable but conditional; fix before refinement
- **60–69:** weak; revise blockout
- **<60:** reject and rebuild the affected phase

## Required qualitative judgement

Pi must not only give a number. It must answer:

1. What is the strongest part of the dossier/model?
2. What is the weakest practical assumption?
3. Which missing evidence could most change the geometry?
4. What would cause wasted modelling effort if not fixed now?
5. Is the current result useful for deciding where Il Portale goes?
6. What should be done next, in one operational step?

## Review format

```text
CAPROTTI REVIEW
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

Critical missing evidence:
...

Do not do yet:
...

Next operational action:
...
```
