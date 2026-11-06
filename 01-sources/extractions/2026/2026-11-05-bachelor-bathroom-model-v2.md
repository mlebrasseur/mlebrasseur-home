# November 5, 2026 — Basement Bathroom Concept v2 Model

## Source

- Source ID: SRC-2026-098
- Type: Generated 3D GLB / offline HTML / Python source
- Generated: 2026-11-05
- Basis: [Homeowner directions, SRC-2026-097](../../chat/2026/2026-11-05-renovation-bathroom-concept-v2.md), [product dimensions, SRC-2026-096](2026-11-05-bathroom-product-dimensions.md), and [earlier model, SRC-2026-094](2026-11-05-bachelor-bathroom-model.md).
- Status: Separate comparison concept; no final installation approval or new purchase recorded.

## Artifacts

[Offline viewer](../../documents/renovation/bathroom-concept-v2/dist/index.html) · [GLB](../../documents/renovation/bathroom-concept-v2/dist/bathroom.glb) · [generator](../../documents/renovation/bathroom-concept-v2/generate.py) · [folder/rebuild instructions](../../documents/renovation/bathroom-concept-v2/README.md).

Existing `bathroom-concept/` files remain byte-for-byte unchanged. V2 has its own copies of the eight archived product reference files; their originals, URLs and hashes remain documented in SRC-2026-096. Publish only v2's `dist/` contents. The public header omits the property address.

## Layout and Modeling Assumptions

Authoring coordinates are inches: X left-to-right, Y up, Z entrance-to-rear. GLB units are metres with Z reversed. Room remains 89 × 86½, ceiling 85. Exact measurements and installations are unverified.

| Item | Concept v2 representation |
|---|---|
| Entrance door | Inward-right toward shower. Assumed hinge axis X=47.8, Z=0.9; 30 × 80 × 1⅜ slab, original frosted pane/Weiser Breton. Shown closed (0°) in GLB and initial viewer. Frame, hinge mechanics and final cut height remain provisional |
| Linen cabinet | X=0–14.1875, Z=70.75–86.5, height 70.875; against left/rear walls, facing toilet. Handles left/front, hinges right/rear when facing cabinet, opening toward rear wall. Assumed hinge X=14.22, Z=86. Opening conflict noted below |
| Vanity | Cabinet Z=22.992–70; top Z=22.165354–70, X=0–18.307087. Left-wall contact; assumed 0.75-in gap from top to linen. Manufacturer cabinet/top/basin envelopes retained |
| Mirror | ALEX 900 × 700 × 45 mm, centred at Z=46.082677 above vanity; bottom Y=44, two inset vertical LED strips. Mounting assumed |
| Hamper | Sterilite 19.5 × 12.25 × 24.5, front-left; X=0.625–12.875, Z=0.625–20.125. About 2.040354 in to vanity top. Lid motion and reach unverified |
| Hand towel | Left wall above hamper, centre Z=10.375, ring Y=43–49; follows hamper as modeling assumption |
| Dimmer / vent switch | Front wall left of doorway, side by side: light dimmer left, vent rocker right when facing plate from inside. Schematic plate X=5.25–10, Y=44.75–49.25; above hamper. Device models, circuit/fixture compatibility and mounting are unverified |
| Tool outlet | Left wall beside front end of vanity/mirror, centre Z=25.3, Y=47; plate Z=23.925–26.675. Circuit/electrical installation not specified |
| Vent grille | Retained front-left, above hamper, assumed 12 × 6, Y=75–81; duct function/dimensions unverified |
| Shower / stool / niche | Base/enclosure dimensions retained; added black overlap upright, closing/corner profiles and lower sliding-door borders; wall channels/top rail/square rollers refined from [archived Alaska photo](../../documents/renovation/bathroom-concept-v2/references/alaska-1.jpg). Profile widths are schematic. Base X=53–89, Z=0–47.75, 1-in threshold; 2000-mm glass; stool near front; end drain beneath removable stool; vertical niche |
| Toilet / rear fittings | Earlier provisional Toledo, behind-tank storage, towel bar, paper holder and window retained. Toilet centre Z=71; window opening X=19–49 / Y=64–76, sill projects 2 in into room; these window dimensions are assumptions |

The light-dimming request establishes intent, not compatibility of a particular dimmer or the ALEX mirror. Separate vanity-light selection remains unresolved.

## Viewer Behavior

Five existing view presets retained; vanity camera, live mirror reflection, mirror light and labels follow the revised positions. Entrance door remains visible in wall cutaways. **Open door / Close door** uses smooth reversible animation; a 0–90° slider permits direct angle inspection and cancels an active animation. Reduced-motion preference changes the angle immediately. PNG captures the current view; GLB download remains the original closed geometry.

## Clearance Findings

A simplified rectangle sweep checks modeled panel/handle envelopes at integer angles 0–90° about assumed fixed pivots. It does not simulate manufacturer hinges or certify actual installation.

- Entrance door and hardware: no intersection with the modeled shower or furniture envelopes over the sweep.
- **Linen cabinet: rear-wall opening conflict.** With the latest requested handles on the left/front and hinges on the right/rear, conservative door bounds first intersect the rear wall around 31°, the assumed window sill around 56°, and towel fittings around 72–73°; trim also intersects later. These are model-envelope observations, not measured opening limits. Rounded corners, window dimensions and actual hinge motion may change the result. This supersedes the previous front-hinged v2 clearance check because the homeowner changed the handing.
- Preserve the homeowner's rear-wall contact and left handles in this comparison; do not silently move the cabinet or rear fittings. Resolve cabinet offset and rear fittings before treating this arrangement as practical. Any offset reduces the space available to the vanity and hamper.
- Actual door/jamb travel, cabinet access, hamper lid motion, window position, wiring, plumbing and clearances remain to verify.

## Verification

- Product/layout envelope checks passed; left-hand linen pulls, left-side dimmer/vent, outlet and mirror alignment confirmed.
- Rebuilding from `/tmp` reproduced both output files byte for byte. Original concept and copied product references verified against pre-change hashes.
- Khronos glTF validator: zero errors, warnings, informational issues or hints.
- Chromium verification passed: five presets, animated entrance-door intermediate motion/endpoints/reversal, slider, world-space hinge rotation, reduced-motion behavior, display controls, GLB/PNG downloads, subdirectory hosting, mobile layout and offline loading; no page errors or external requests. Follow-up checks cover cabinet handles on the left, dimmer left/vent right from inside, added black shower profiles, glass toggle and the closed default with animated opening/closing.

## Artifact Integrity

| File | Bytes | SHA-256 |
|---|---:|---|
| `generate.py` | 307519 | `7c8e745e8e3773aa56996f854697cc00f129f7c3ad3365bb662809d0efd7cfc4` |
| `dist/index.html` | 8213302 | `6edccc443fa9d02679815c85ab59761d5ce359c6ea33aad4e93b596a1e5cf4c3` |
| `dist/bathroom.glb` | 5413880 | `00a16bb3fabad1c757c455a5b1db4d7575c85062b8553d8389a8aaba428470f0` |
