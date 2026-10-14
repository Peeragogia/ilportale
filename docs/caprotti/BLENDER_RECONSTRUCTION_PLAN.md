# Blender Reconstruction Plan v0.3

## Target

Build a controllable, evidence-traceable Blender reconstruction of the Tea Pavilion and use it to evaluate Il Portale as a civic music learning installation.

## Scene structure

```text
CAPROTTI_MASTER
├── CAPROTTI_ARCHITECTURE
│   ├── CAP_Base
│   ├── CAP_MainMass
│   ├── CAP_ArchedBay
│   ├── CAP_RectangularBay
│   ├── CAP_Columns
│   ├── CAP_Capitals_PROXY
│   ├── CAP_Entablature
│   ├── CAP_ReliefPanels_PROXY
│   ├── CAP_Statues_PROXY
│   ├── CAP_Glazing
│   ├── CAP_RoofTerrace
│   ├── CAP_Balustrade
│   └── CAP_ExternalStair
├── IL_PORTALE
├── CONTEXT
│   ├── CAP_Pond_PROXY
│   ├── CAP_Grotto_PROXY
│   ├── CAP_Ground
│   └── CAP_Vegetation_PROXY
├── LIGHTING
├── CAMERAS
└── REFERENCE
```

Keep Il Portale independent from pavilion geometry.

## Phase 0 — dossier review

Before touching Blender, Pi must review this dossier and issue:

- `GO`
- `CONDITIONAL GO`
- `NO-GO`

with reasons using `QUALITY_REVIEW_RUBRIC.md`.

## Phase 1 — proportional blockout

Model only:

- main footprint/mass;
- tall arched glazed bay;
- rectangular glazed bay + semicircular relief placeholder;
- column/pilaster positions;
- entablature/cornice depth;
- terrace/parapet/balustrade proxy;
- external stair mass;
- pond/grotto/ground context proxies.

### Rules

- do not model fine ornament;
- do not sculpt statues;
- no photoreal materials;
- use clean transforms and explicit collection hierarchy;
- use repeated/instanced modules only where repetition is visually supported;
- name unknown/provisional objects with `_PROXY` or `_EST` suffix;
- preserve a modelling note for every major inferred ratio.

### Scale convention

Until measured data exists:

- principal façade width = **100 proportional units**;
- no metres claimed;
- all ratios documented;
- entire architecture collection remains rescalable from a single root/empty.

## Phase 1 output

Generate five quick review cameras:

- `EXT_FRONT_3Q`
- `EXT_STAIR_3Q`
- `EXT_POND`
- `INT_ENTRANCE`
- `INT_PORTALE_POSITION`

Render in fast Eevee/Workbench/low-cost mode. No Cycles HQ yet.

## Phase 2 — visual validation

For each review camera, compare against the closest reference image and report:

- silhouette mismatch;
- opening proportion mismatch;
- column spacing mismatch;
- terrace/balustrade mismatch;
- stair mismatch;
- context mismatch.

Do not proceed merely because the render “looks nice”.

## Phase 3 — metric calibration

When field measurements arrive:

1. choose primary metric anchor;
2. rescale the architecture root;
3. check at least two secondary measured dimensions;
4. report residual error;
5. correct ratios only if evidence justifies it;
6. lock `CAPROTTI_ARCHITECTURE` scale after validation.

## Phase 4 — Portale placement study

Test three hypotheses without redesigning the Portale:

### A — Central / iconic
Strong symbolic presence. Evaluate circulation obstruction.

### B — Lateral / functional
Preserve transparency and movement. Current baseline hypothesis.

### C — Integrated learning environment
Allow additional seating/guidance/acoustic/light elements. More ambitious; test only after A/B.

For each option produce:

- plan/top view;
- entrance eye-level view;
- user interaction view;
- exterior-through-glass view;
- clearance notes;
- provisional acoustic note.

## Phase 5 — architectural refinement

Priority:

1. glazing frame + circular node module;
2. columns and simplified capitals;
3. entablature/cornice;
4. stair and balustrade;
5. relief panels;
6. statues;
7. materials/weathering.

Only create hero-detail geometry where final cameras justify it.

## Phase 6 — atmosphere and final visualisation

Only after geometry approval:

- real vegetation proxies where useful;
- pond shader;
- grotto refinement;
- daylight + restrained interior lighting;
- Cycles HQ;
- subtle post-processing;
- optional cloud/sky animation last.

## Non-destructive requirements

- original Portale file/collection untouched;
- new Blender version at every milestone;
- audit trail for scripts/tool calls;
- change report listing objects created/changed;
- preview after every major phase;
- ability to roll back.
