# November 6, 2026 — Basement Bathroom Concept v4

November 6 cleanup: the standalone V4 folder was removed under [SRC-2026-105](../../chat/2026/2026-11-06-renovation-bathroom-cleanup.md). Use the [combined viewer](../../documents/renovation/bathroom-configurations/dist/index.html) and select **V4**; model links now open the four-scene GLB. Product evidence is consolidated in its `references/`. The dimensions, checks and output hashes below record the historical standalone build; current artifacts and verification are in [SRC-2026-104](2026-11-06-bathroom-combined-configurations.md). All configurations now share v4’s right side and animate the entrance.

## Source

- Source ID: SRC-2026-102
- Type: Manufacturer PDFs / photographs / generated GLB / offline HTML / Python source
- Retrieved and generated: 2026-11-06
- Direction: [Homeowner selections and approval, SRC-2026-101](../../chat/2026/2026-11-06-renovation-bathroom-concept-v4.md).
- Basis: [v2, SRC-2026-098](2026-11-05-bachelor-bathroom-model-v2.md); [v3 spacing and BIBO evidence, SRC-2026-100](2026-11-05-bachelor-bathroom-model-v3.md); [earlier product drawings, SRC-2026-096](2026-11-05-bathroom-product-dimensions.md).
- Status: Comparison concept; no order amendment or final installation approval reported.

## Artifacts

[Offline viewer](../../documents/renovation/bathroom-configurations/dist/index.html) · [GLB](../../documents/renovation/bathroom-configurations/dist/bathroom-configurations.glb) · [generator](../../documents/renovation/bathroom-configurations/generate.py) · [README](../../documents/renovation/bathroom-configurations/README.md).

Originally built as a separate model from v2, incorporating v3's spacing approach and BIBO geometry. All configurations are now maintained together. Viewer is address-free, works offline and retains five presets, wall/glass controls, animated entrance door, angle slider and PNG/GLB downloads. Entrance starts closed; downloaded GLB retains that pose.

## Product Evidence

| Product | Verified dimensions and representation | Evidence |
|---|---|---|
| Alder VF3618-62GWH | **894 W × 456 D × 820 H mm**; two doors left, three drawers right; black pulls and glossy white recessed base. Manufacturer drawing August 8, 2022; front dimensions include 297 × 597-mm doors and 296 × 197.5-mm drawers. Small gaps, pull dimensions and internal details schematic | [36-inch product](https://www.baindepot.com/ensemble-meuble-lavabo-collection-alder.html?pid=11812); [PDF](../../documents/renovation/bathroom-configurations/references/vanity-VF3618-62GWH.pdf); [photograph](../../documents/renovation/bathroom-configurations/references/vanity-VF3618-62GWH.jpg) |
| Saxe VT-SQ907 | **915 W × 465 D × 180 total H mm**, vitreous china / porcelain; **20-mm deck**, **500 × 280-mm opening**, faucet centre 60 mm from rear, basin opening rear edge 115 mm from rear, drain centre 230 mm from rear. Faucet/drain/overflow diameters 35/45/24 mm; overflow present. Interior contour and 125-mm usable drop inferred | [Selected product](https://www.baindepot.com/dessus-vanite-porcelaine-lavabo-rectangulaire-saxevt.html?pid=4091); [May 25, 2016 PDF](../../documents/renovation/bathroom-configurations/references/top-VT-SQ907.pdf); [photograph](../../documents/renovation/bathroom-configurations/references/top-VT-SQ907.jpg) |
| LF1614-62GWH floor linen | Retain v2's rounded envelope **15.75 W × 14.1875 D × 70.875 H inches**, equivalent approximately to the drawing's 400 × 360 × 1800 mm. Reversible doors; right/rear hinges and left/front projecting handles | [Copied PDF](../../documents/renovation/bathroom-configurations/references/linen-LF1614-62GWH.pdf); provenance SRC-2026-096 |
| BIBO 84-BIBO-24 | **600 W × 700 H mm** from drawing, **30-mm depth** from listing, as v3. Two inset light strips and touch ring; small details approximate | [Copied PDF](../../documents/renovation/bathroom-configurations/references/mirror-84-BIBO-24.pdf); [photo](../../documents/renovation/bathroom-configurations/references/mirror-84-BIBO-24.jpg); provenance SRC-2026-100 |

**Top/cabinet fit:** retailer identifies VT-SQ907 for a nominal 36 × 18 vanity; actual drawing dimensions allow **10.5-mm overhang at each end** with the cabinet centred beneath the top, and **9-mm front overhang** with both backs against the left wall. These envelopes support the intended pairing; support, basin underside, internal divider/drawer clearance, faucet/drain and trap routing still require installation verification. The 180-mm total top height includes the bowl/boss below the deck; it is not added to cabinet height.

New source URLs, retrieved via `00-inbox/files/bathroom-v4/`, inspected and moved into the concept references:

- [Cabinet PDF](https://www.baindepot.com/media/akeneo_connector/asset_files/V/F/VF3618_62GWH_spec_bfca.pdf)
- [Cabinet photo](https://www.baindepot.com/media/catalog/product/V/F/VF3618_62GWH_01_993c.jpg)
- [Top PDF](https://www.baindepot.com/media/akeneo_connector/asset_files/V/T/VT_SQ907_spec_c9e8.pdf)
- [Top photo](https://www.baindepot.com/media/catalog/product/V/T/VT_SQ907_01_a31e.jpg)

Inherited linen/shower/toilet references are unchanged copies from v2; BIBO references are unchanged copies from v3. Original provenance remains in SRC-2026-096 and SRC-2026-100. The cabinet page currently labels the collection INEZ although its URL and homeowner reference say Alder; SKU VF3618-62GWH identifies the modeled product.

## Placement and Assumptions

Coordinates in inches: X left-to-right, Y up, Z entrance-to-rear. Room 89 × 86½, ceiling 85. GLB uses metres and negated authoring Z. Placements are model choices, not surveyed installation coordinates.

| Item | V4 placement |
|---|---|
| Floor linen | X=0–14.1875, Z=65.75–81.5, Y=0–70.875; **5-inch rear gap**; right/rear hinges retained |
| Vanity/top | Top X=0–18.3071, Z=24.9257–60.9493, Y=33.0709 finished height. Cabinet Z=25.3391–60.5359, Y=0–32.2835; two doors left/front, three drawers right/rear |
| Furniture gaps | **4.8007 inches** from each top edge to linen/hamper; measured to top, not cabinet body |
| Mirror | Centre Z=42.9375; top **70.875 inches** aligned with linen, bottom **43.3159 inches**; **10.2451 inches above countertop**, **4.0951 inches above static modeled faucet lever** |
| Tool outlet | Left wall, centre Z=21.9257 / Y=47; beside mirror, using v3's placement approach |
| Other fixtures | V2 front-left hamper and towel, shower/stool/niche, Toledo and rear fittings, controls, entrance and animation retained |

The higher floor linen sets a higher mirror than v3. Actual viewing height and full faucet lever motion need confirmation. Reusing v3's mirror does not establish wall-dimmer compatibility or amend the ordered mirror. The selected cabinet/top and mirror replace the ordered sizes in this concept only.

## Verification and Limits

[Clearance/placement report](../../documents/renovation/bathroom-configurations/references/v4-clearance-check.json).

- GLB envelopes match the cabinet/top dimensions, equal side gaps, 5-inch rear gap, cabinet-to-top overhangs and BIBO top alignment; three drawers and two doors confirmed.
- Static mirror/faucet meshes do not intersect; vertical clearance to the modeled lever is 4.0951 inches.
- Conservative mesh bounding rectangles with vertical overlap, sampled each degree from 0–90° about assumed fixed pivots, find no collisions for entrance, linen doors/handles or vanity doors/handles against the tested surrounding fixtures. Linen's 5-inch offset clears the v2 rear-wall/window/towel conflict in this model.
- Drawer fronts/pulls clear tested surrounding fixtures over an **illustrative 14-inch extension** at one-inch increments. Actual slides, internal plumbing and cabinet internals are not simulated.
- Rebuild from `/tmp` produces identical viewer and GLB bytes; original, v2 and v3 files match pre-change hashes.
- Chromium checks passed for five presets, entrance-door default/animation/reversal/slider, world-space hinge geometry, reduced motion, display controls, PNG/GLB downloads, subdirectory serving, mobile layout and offline loading; no page errors or external requests. Overview, vanity, overhead and mobile screenshots were visually reviewed; BIBO reflection and two light strips display correctly.
- [Khronos glTF validation](../../documents/renovation/bathroom-configurations/references/v4-gltf-validation.json): zero errors, warnings, informational issues or hints.

These checks do not simulate actual hinge mechanisms, simultaneous opening of components, user reach, hamper lid travel, wall tolerances, electrical installation or plumbing. Site/window dimensions and the schematic faucet shape remain unverified.

## Artifact Integrity

| File | Bytes | SHA-256 |
|---|---:|---|
| `generate.py` | 308622 | `8e2f102e5b0a532a5ae6283b7b964bedc8079e78a6fdf84c230b20489ea79937` |
| `dist/index.html` | 8125157 | `7e699f05983ec299b0c7c6ef3d1bbd2fe5803a60730a92b75501f3c8801c8c23` |
| `dist/bathroom.glb` | 5347644 | `cfc156b0bc78d7e147d8cf4e14c384157093088c9b3945cf83c0d113442baae0` |
| `references/vanity-VF3618-62GWH.pdf` | 11111319 | `653bd70b87440f2e25988ad074b0729a4f451162b4ffc842d7da26e92aca4c09` |
| `references/vanity-VF3618-62GWH.jpg` | 84010 | `2481e06cbdf6b4f7d35516261eb5b62ed4b5ed0f336586d25a0ba5479038a871` |
| `references/top-VT-SQ907.pdf` | 209868 | `e3c535fb323ad1d5a4b17e98a5995f52e949553b386158fba1801bf5e8892661` |
| `references/top-VT-SQ907.jpg` | 14071 | `d3496f9729c5e80f7d28c39f60eb1f85cbd9defc7b402e729a961bab508e7441` |
