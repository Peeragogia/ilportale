# Visual Analysis — Architectural reading for Blender

## 1. Overall mass

Public imagery suggests a **compact pavilion with near-monumental vertical articulation despite its small footprint**. The eye reads the building less as a conventional room and more as a richly framed transparent object.

For blockout purposes, model the pavilion as a compact main volume with a strong upper entablature/cornice and a roof terrace/balustrade above.

**Confidence:** medium-high for the overall type, low for exact proportions.

## 2. Façade hierarchy

At least two distinct façade conditions are visible:

1. a **tall arched glazed bay**, strongly vertical;
2. a façade with a **rectangular glazed opening** below a **semicircular relief panel**, framed by classical columns/pilasters and adjacent statuary.

The building should therefore not be simplified as four identical glazed walls.

## 3. Vertical structure

Fluted classical columns/pilasters appear at corners/bays. Capitals are ornate and visually closer to Corinthian/composite language than to a plain Tuscan/Doric order.

For Phase 1:

- cylinder/low-poly fluted proxy is enough;
- preserve shaft-to-capital proportion;
- do not sculpt acanthus leaves yet.

## 4. Glazing

The glazing is one of the most distinctive elements. The frame is dark and highly graphic, with **large circular nodes/medallions at intersections**. This motif should be treated as a reusable modular asset.

Recommended later implementation:

- curves or thin rectangular metal sections;
- instanced circular nodes;
- physically plausible glass thickness only in refinement phase.

## 5. Ornament

The ornament operates at several scales:

- broad entablature/cornice bands;
- frieze reliefs;
- semicircular figurative panel;
- rectangular decorative panels;
- statues in niches/inter-column positions;
- smaller mouldings and carved details.

The first blockout only needs the **depth hierarchy** of these layers. Flat placeholder panels are preferable to invented sculpture.

## 6. Roof terrace and balustrade

Public references clearly show a perimeter balustrade at roof level. This contributes strongly to recognisability and must be present in the first blockout.

Model initially as:

- parapet base;
- repeated baluster proxy module;
- corner/end piers.

Exact baluster profile can wait.

## 7. External stair

A stair rises along the pavilion/rockwork edge toward the terrace. It appears visually integrated with the garden’s constructed topography rather than as an isolated modern stair.

Phase 1 should capture:

- approximate direction;
- rise to terrace level;
- landing relationship;
- rough width;
- handrail silhouette.

Do not infer exact tread/riser counts until field photos or measurements are available.

## 8. Landscape relationship

The pond, grotto/rockwork and vegetation are not optional scenery. They explain how the pavilion is perceived.

The key final views should preserve:

- at least one view across/near the pond;
- one approach view through vegetation;
- one exterior view where the Portale is visible through glazing.

## 9. Provisional modelling ratios

Do **not** assign metres yet. Use a dimensionless proportional model.

Recommended initial convention:

- set the width of the best-documented principal façade to **100 units**;
- derive all visible architectural features as ratios of that width;
- record every ratio used;
- rescale the whole `CAPROTTI_ARCHITECTURE` collection only after one or more reliable field measurements are obtained.

This avoids contaminating the model with false precision.

## 10. Immediate unknowns that affect Il Portale placement

- clear internal width/depth;
- usable floor area after door swing / existing furnishings;
- exact entry threshold and step level;
- wall/window reveal depth;
- ceiling height;
- power/data/service points;
- current restrictions around historic surfaces.

Until these are known, any statement that the existing Portale “fits” is only a visual hypothesis.
