# November 5, 2026 — Basement Bathroom Concept v2

Later packaging decision: [November 6 cleanup, SRC-2026-105](2026-11-06-renovation-bathroom-cleanup.md) supersedes the standalone-folder preservation instructions below. V1–V4 and unique product evidence are retained in `bathroom-configurations/`; the four standalone folders are removed.

## Source

- Source ID: SRC-2026-097
- Type: Homeowner conversation
- Recorded: 2026-11-05
- Authorization: Homeowner said `go` after reviewing the separate-concept blueprint; subsequent messages corrected controls/handing and requested door animation. A second `go` authorized the shower-trim, control-order and left-handle corrections below; the later closed-by-default request steered that work.
- Purpose: Evaluate a new bathroom configuration. This is not final construction-layout approval.
- Related project: [Bachelor bathroom](../../../06-projects/renovations/bathroom.md).

## Final Homeowner Directions

Directions are viewed from the entrance unless stated otherwise.

- Create **Concept v2** separately in `01-sources/documents/renovation/bathroom-concept-v2/`, including its generator, references, README and `dist/` files. Preserve the existing `bathroom-concept/` folder.
- Reverse the bathroom door to open inward toward the shower. Add an animated option to open and close it. **Door closed by default**, per the latest correction.
- Put the linen storage in the rear-left corner, facing the toilet; place the vanity beside it along the left wall toward the entrance.
- **Linen handles on the left, hinges on the right when facing the cabinet; doors open toward the back wall.** Handles are on the vanity/front side and hinges on the rear-wall side. This supersedes the intermediate right-handle request.
- Hamper in the **front-left corner**, where the linen cabinet stood in the earlier concept.
- **Light and ventilation controls on the front wall LEFT of the entrance**, side by side. Lights are dimmable: show the light dimmer on the **left** and ventilation switch on the **right when facing the plate from inside**. These corrections supersede the initial right-of-door request and the proposed narrow stacked controls.
- Restore the shower’s missing black border/glass details to match the Alaska KD3329 reference product.
- “Electrical box” means the hairdryer/tool outlet. Move it beside the vanity.

## Modeling Choices and Limits

- Furniture gap, outlet/control heights and precise positions are model assumptions. Mirror follows the vanity; hand-towel fixture follows the hamper. Shower, toilet, rear towel bar, window and other fittings retain their earlier positions for comparison.
- Facing the plate from inside, light dimmer is left and ventilation switch is right. Device models, controlled light fixture/circuit, compatibility, ventilation control type and installation details are not established. The request does not confirm that the ordered ALEX mirror accepts a wall dimmer, nor select the separate vanity light.
- The entrance door starts closed at 0° in the viewer and GLB. Viewer animation and slider allow 0–90° inspection; downloaded GLB retains its initial closed pose.
- Preserve requested linen/rear-wall contact for this study. A simplified sweep found rear-hinged linen-door conflicts with the rear wall and assumed window/towel fittings; the closed-door model does not establish full opening clearance. Cabinet spacing/accessory placement needs further design review.
- No new purchases, costs or construction dates were reported.

Model measurements, verification and artifacts: [SRC-2026-098](../../extractions/2026/2026-11-05-bachelor-bathroom-model-v2.md). Existing product evidence: [SRC-2026-096](../../extractions/2026/2026-11-05-bathroom-product-dimensions.md).

## November 5 Follow-up — Shower Reference and Final Handing

The homeowner requested light-left/vent-right, shower black details matching the product, and cabinet handles left with doors opening toward the back wall, then approved the blueprint with `go`. During implementation, the homeowner requested the entrance door closed by default.

Reference inspected: [archived Alaska KD3329 product photo](../../documents/renovation/bathroom-configurations/references/alaska-1.jpg) and [Tassili product page](https://tassili.ca/produit/douche-en-coin-alaska-a-base-surbaissee-finition-carree-noire-48-po-x-36-po/), consulted November 5. Photo shows black wall channels, an overlap upright, closing/corner profiles, lower sliding-door borders, upper rail and square roller hardware. The model adds/refines those features; extrusion widths and hardware contours are visual approximations. The short side panel retains its open upper glass edge.

No cabinet offset was authorized in this correction. Retain rear-wall contact and document the new rear-hinge swing conflict for further review.
