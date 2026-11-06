# November 5, 2026 — Basement Bathroom — Current Concept

## Source

- Source ID: SRC-2026-094
- Type: Generated 3D concept model, offline viewer and reproducible generator
- Requested / generated / revised: 2026-11-05
- Revision: All accumulated homeowner corrections approved with `go`, including the specific Sterilite hamper, later fixture moves, frosted-glass door, Weiser Breton lever, complete doorway surround, Chormtok shower stool, grooved wood trim, product-dimension corrections, 2-inch linen clearance, centred hamper/hand towel and white vanity base; see [SRC-2026-095](../../chat/2026/2026-11-05-renovation-bathroom-model-corrections.md).
- Homeowner request: generate a model of the bathroom with the newly ordered materials; explicitly chose a **rotatable 3D model** over a rendered image and approved the file blueprint with `go`.
- Method: Procedural mesh geometry generated with Python 3; glTF 2.0 binary export; offline Three.js r169 viewer. This is actual 3D geometry, not an AI-generated image or a manufacturer CAD assembly.
- Confidence: Recorded room and product dimensions are used where available. Positions, detailed product shapes and several installation dimensions are provisional as listed below. This is a spatial concept, not a construction plan or verification of clearances.

## Files and Use

- [Open the offline browser viewer](../../documents/renovation/bathroom-concept/dist/index.html).
- [Download/open the GLB model](../../documents/renovation/bathroom-concept/dist/bathroom.glb).
- [Python generator](../../documents/renovation/bathroom-concept/generate.py).

Open the HTML file in a current browser with WebGL enabled. It contains the model, textures and viewer libraries; no server, account or network connection is required. Drag to orbit, scroll/pinch to zoom, right-drag to pan. Presets provide overview, doorway, overhead, vanity and shower views. Controls expose automatic wall cutaway, hidden/all-visible walls, ceiling, shower enclosure, labels and slow rotation. Arrow keys rotate the focused canvas, `+`/`−` zoom, and `R` resets. GLB and current-view PNG downloads are available inside the viewer.

The GLB contains 365 meshes and two scenes. The default scene is a front cutaway with the ceiling omitted; the alternate scene contains the full shell. Geometry is in metres: X runs left to right from the entrance, Y points up, negative Z runs toward the back wall. The generator authors dimensions in inches and converts them to this frame. The live planar mirror reflection is a viewer effect; the GLB uses a metallic mirror approximation.

From the repository root, rebuild the public files with Python 3 (the script also works when invoked by absolute path from another directory):

```sh
python3 01-sources/documents/renovation/bathroom-concept/generate.py
```

The concept root is `01-sources/documents/renovation/bathroom-concept/`, containing `generate.py`, `references/` and `dist/`. Only its adjacent `dist/index.html` and `dist/bathroom.glb` are overwritten. Publish only that nested `dist/`; see the [concept README](../../documents/renovation/bathroom-concept/README.md). The public header reads “Basement bathroom” and “Current concept · Layout, materials and fixtures”; the property address is omitted. The generator and house records remain outside the publish folder. The generator needs the Python standard library only; pinned viewer libraries are bundled with their MIT license. It performs no downloads. Changing this model requires updating the provenance and verification record as appropriate.

## Evidence and Design Specification

- [Archived product drawings, photos, dimension conflicts and current geometry basis, SRC-2026-096](2026-11-05-bathroom-product-dimensions.md).

- [Latest homeowner corrections and product references, SRC-2026-095](../../chat/2026/2026-11-05-renovation-bathroom-model-corrections.md); supersedes earlier horizontal-niche and right-handle preferences.

- [Room dimensions, layout and finish preferences, SRC-2026-088](../../chat/2026/2026-11-03-renovation-bachelor-bathroom-plan.md).
- [Earlier concept and requested corrections, SRC-2026-089](2026-11-03-bachelor-bathroom-concept-v1-render.md).
- [Toledo and fixture references, SRC-2026-090](../../chat/2026/2026-11-04-renovation-bachelor-bathroom-products.md).
- [Canac order, SRC-2026-091](2026-11-05-renovation-canac-order-4005849329.md).
- [Bain Dépôt order, SRC-2026-092](2026-11-05-renovation-bain-depot-order-4000176758.md).
- [Amazon niche order and Marcel panel allocation, SRC-2026-093](../../chat/2026/2026-11-05-renovation-amazon-shower-niche-order.md).

The layout uses an 89-inch-wide × 86½-inch-deep room with an 85-inch ceiling; a front-right shower, left-wall vanity and front-left linen cabinet; a back-right toilet facing the vanity; shallow storage behind the tank; and a high, two-pane back window. The visual palette is glossy white cabinetry, white porcelain, matte black fixtures/handles, off-white walls, white marble-look shower panels and fine-speckled white epoxy.

| Component | Representation / basis |
|---|---|
| Alaska KD3329 shower | Corner base 47¾ × 36 in per dimensioned plan (header conflicts); 1-inch threshold, textured SMC, covered end drain. Door corner span 1160 mm, side 852 mm, height 2000 mm and glass 8 mm. Square black sliding hardware, requested rear-half opening; exact hardware/panel split schematic. SRC-2026-096 |
| Sapphire 33003746 panels | White marble-look material on the solid front/right shower walls, extending to the ceiling. Procedural veining is illustrative, not a scanned product sample |
| VF4818-62GWH vanity | 1194 W × 456 D × 820 H mm from archived drawing; six drawers with horizontal pulls and two centre doors with vertical pulls; glossy white. Recessed base matches glossy white cabinet. Detailed pull sizes/interior schematic. SRC-2026-096 |
| VT-SQ1207 sink top / F-4021-3BK faucet | Top 1215 × 465 mm, deck 20 mm, basin opening 510 × 280 mm, total depth 185 mm including underside boss. Drain/overflow included. Interior contour and black faucet dimensions remain schematic. SRC-2026-096 |
| LF1614-62GWH linen cabinet | Body 15¾ wide × 14 3/16 deep × 70⅞ high; two closed doors, with handles on the left and hinges on the right when facing it, per SRC-2026-095. Manufacturer confirms reversible doors (SRC-2026-096); installed swing clearance remains to verify. Dimensions from the [retailer page](https://www.baindepot.com/lingerie-de-plancher-16po-blanc-lustre-a-poignees-noires-lf1614-62gwh.html), consulted November 5 |
| ALEX 84-ALEX-90 mirror | Ordered nominal 36 × 28; actual 900 × 700 × 45 mm, centred over the vanity. Two inset vertical LED strips follow the 84-ALEX-90 product photograph; strip dimensions approximate. Manufacturer reference in SRC-2026-095 |
| Homevacious niche B0DCZC7134 | Nominal 12 wide × 24 high, vertical per SRC-2026-095; recessed white insert with two stacked compartments and a horizontal shelf. Exact shelf height, ordered variant and rough opening unverified |
| SERA Toledo toilet | Provisional one-piece skirted body, elongated D-shaped seat and split rectangular flush button; 26.8 D × 14.6 W × 29.5 H in, bowl rim 16.5 in. Detailed shape inferred from photo; no purchase added. SRC-2026-096 |
| SQ3004BK accessories | Hand-towel ring above hamper on left wall; rear towel bar shifted left with two illustrative hanging towels, rear paper holder retained; hook above bin on right wall (SRC-2026-095). Exact mounting positions are illustrative |
| Sterilite Slim hamper | White plastic, hinged lid, integrated grips and oval perforations; 19½ × 12¼ × 24½ high. Long side along left wall between linen and vanity; selected for model, purchase unreported (SRC-2026-095) |
| IKEA GANSJÖN bin | Black cylindrical pedal bin with lid/rear handle, 17 cm diameter × 26 cm high; between shower and toilet; selected for model, purchase unreported (SRC-2026-095) |
| Door / privacy lever | Canac Shaker 88001678, 30 × 80 × 1⅜ with one frosted pane and white frame; Weiser Breton matte-black privacy lever 9GLC3310-069 with square rose, flat handle and interior turn. References and product photos in SRC-2026-095; exact frame/handle detail and hinges schematic |
| Chormtok shower stool | Black HDPE B0FR49WRFK / HW25016, slotted seat, grip openings, splayed legs, feet and lower shelf. Product diagram 16.9 × 12.6 × 16.5 in used; text-table width conflicts. Selected for model; purchase unreported (SRC-2026-095) |
| Vent / tool outlet | Rectangular front-wall grille above linen; homeowner reports central ducted ventilation. White rear-wall outlet centered above vanity end. Dimensions and electrical/duct details schematic (SRC-2026-095) |

Marcel's C-Ment panels are not bathroom materials. Homeowner now identifies Canac 88001678 as the bathroom door model; complete allocation of the three ordered slabs remains unconfirmed. The modeled handle is the supplied Weiser Breton 9GLC3310-069 reference; purchase unreported. No separate vanity-light model has been selected; the model uses the ordered mirror and illustrative scene lighting.

## Provisional Dimensions and Practical Limits

Wall adjacency, handing, niche orientation and accessory locations follow SRC-2026-095. The numeric offsets, mounting heights and unselected product dimensions below are modeling assumptions, not new measured facts. Coordinates here use the generator's inch frame, with Z increasing from entrance to back.

| Item | Assumption / remaining check |
|---|---|
| Window | 30 wide × 12 high, opening X=19–49, bottom Y=64; exact size and location unknown |
| Entrance | 30 × 80 leaf shown closed at X=17¾–47¾, 1⅜ thick. Stiles/top rail assumed 4½ wide, bottom rail 8; glass appearance approximated. Complete surround has reported 2½-in casing on both faces, modeled jambs/stops and black hinges. Final cut height unresolved: 80-in leaf is a stock-height placeholder. Rough opening/reveals and inward-left swing require checks. Front cutaway hides door/surround with wall; rotate inside to see them |
| Vanity placement | Cabinet Z=39.492–86½; top Z=38.665–86½ and X=0–18.307; both meet left/rear walls. Extra top width projects toward open sides; installation detail unverified |
| Linen placement | Against left wall, 2-inch gap to front wall; Z=2–17¾. Handles left / hinges right. Manufacturer confirms reversible doors; actual hinge travel and clearances require site checks. Close entrance door before opening cabinet fully |
| Mirror mounting | Bottom 44 in, centred on top at Z=62.583; actual 900 × 700 × 45 mm. Two inset vertical strips; strip size/inset and electrical position provisional |
| Niche | Bottom 40 in, top 64 in; centered at Z=24, nominal 12 wide × 24 high with approximately 3½-in recess and shelf centered Y=52. Required rough opening, support and waterproof connection must follow installation instructions |
| Shower | 1-inch threshold; glass height 2000 mm, top approximately 79.74 in. Standing pan assumed 0.75 in; end drain provisionally toward front beneath removable stool. Base-sheet dimensional conflict and placement details in SRC-2026-096 |
| Toilet | Tank back X=81, centre Z=71; overall front X=54.2, bowl rim 16.5 in. Rotated outlet/rough-in unknown; skirt/seat/tank contours inferred from photo |
| Storage behind tank | 7 deep × 20 wide × 35 high, Z=61–81 after moving with toilet; no product selected. Tank-lid, shutoff and cabinet access are not validated |
| Hamper | Centred in clear gap between linen and projecting vanity top at Z=28.207677; overall Z=18.457677–37.957677, X=⅝–12⅞, height 24½. Equal 0.707677-inch spaces each side; lid/door access unverified |
| Bin | Center X=82, Z=55½; diameter 17 cm, height 26 cm. Pedal projects toward room; mechanism schematic |
| Front-wall grille | Outer 12 × 6, X=1.1–13.1, Y=75–81; dimensions/function unknown, no ductwork inferred |
| Rear accessories / outlet | Outlet centre X=9.154 / Y=47 over corrected vanity-top end; towel bar X=24–48 / Y=50; paper holder X=59–64½ / Y=27. Hanging towels remain within X=25–47; visual placements, not drilling/wiring instructions |
| Left hand towel / right hook | Ring and hanging hand towel share hamper centre Z=28.207677; ring Y=43–49, towel bottom Y=29½. Right-wall hook remains Z=55½ / Y=64 above bin; actual linen drape/reach unverified |
| Door hardware | Breton projection 2.718 in; handle center X=45⅜ / Y=36.15, modeled backset 2⅜. Remaining handle geometry and hinges approximate; no door-mounted hook |
| Shower stool | Centre X=71, Z=8.8; footprint 16.9 × 12.6, X=62.55–79.45 / Z=2.5–15.1. Height 16.5 above pan Y=0.75, seat Y=17.25. End-drain cover lies under stool, between feet; stool must move for drain access. Actual dimensions/standing space unverified |
| Doorway surround | Casing X=15¼–17¾ and 47¾–50¼, head Y=80–82½; two recessed border lines, mitered corners and satin white wood grain. Jamb/reveal and groove profile schematic; confirm final door cut height |
| Walls / ceiling | 4½-in shell walls and 3-in ceiling slab for visualization; actual assemblies unmeasured |
| Materials / lighting | Procedural stone, painted wood grain, SMC texture and speckles, approximate sheen and colours, daylight and mirror lighting for readability; no measured illumination calculation |

## Verification

Concept-folder relocation verified: rebuilding from `/tmp` writes into the adjacent nested `dist/` and reproduces both public files byte for byte; root-level outputs removed and links retargeted.

Public packaging: address-free current-concept header, unversioned filenames and dist-only publishing approved in SRC-2026-095. Checks passed: all relocated links resolve; public HTML and decoded GLB metadata omit the property address; geometry/binary payload unchanged; rebuilding from another working directory reproduces both files. Chromium verified static hosting under a subdirectory, desktop/mobile headers, correct GLB/PNG export names and contents, direct GLB download and offline loading, with no browser errors or external requests. Final GLB validation reports zero errors, warnings, infos or hints.

Latest spacing/base revision: geometry/material checks, equal hamper gaps, towel alignment, simplified 0–90° door sweep and all browser checks below passed. Overview, overhead and interior screenshots inspected; vanity base is white. Sweep uses assumed fixed hinge pivot and closed entrance door, not actual hinge kinematics.

Product-refinement checks passed: published cabinet/top/basin, shower glass/base and toilet envelopes; two recessed trim lines; mirror/outlet centering; stool feet clear of the modeled end-drain cover. All five presets and controls passed, followed by a focused check of final mirror alignment, cabinet labeling and GLB download.

- Revised GLB structure, dimensional metadata, mesh/accessor data and embedded textures checked; geometry bounds verify furniture wall contact, hamper gap, vertical niche, mirror size/strips, bin separation, outlet centering, hook alignment, door slab size, towel/paper-holder separation, corrected fixture envelopes, stool feet/end-drain clearance, and recessed casing/jamb/stop geometry.
- Khronos glTF Validator 2.0.0-dev.3.10 used for the exported model.
- Viewer inspected in Chromium from a local `file:` URL with HTTP(S) requests blocked; screenshots used to check overview, interior views and supplied door/lever through rotation. No extra view preset added.
- Generator regeneration checked for byte-identical HTML and GLB output.
- Browser interaction checks passed: all five camera presets, pointer rotation, zoom, keyboard reset, wall modes, glass/ceiling toggles, labels, auto rotation, GLB download, PNG export and 390-pixel mobile layout. No browser errors or external HTTP(S) requests were observed. The downloaded GLB matched the saved file byte for byte.
- Final glTF validation: zero errors, zero warnings and zero informational issues.

Related project: [Bachelor bathroom](../../../06-projects/renovations/bathroom.md). The earlier PNG remains an archived concept image; this model supplies a new interactive view without establishing final construction selections.

## Artifact Integrity

| File | Bytes | SHA-256 |
|---|---:|---|
| `index.html` | 8025755 | `8ecfda26e1d16166b8e43d4179dc225c1580a4ce8b2f996fd2715b30bfbd779b` |
| `bathroom.glb` | 5275568 | `b01746407d86bc33fe532f54fa3d2171722f6689de5d0b449077fe333573549e` |
| `generate.py` | 301680 | `9cbe0645093582a32bf831a70ab13100a9a3fc89820c0410c9589ae53bedd194` |
