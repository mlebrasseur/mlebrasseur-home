# November 6, 2026 — Combined Bathroom Configurations

## Source

- Source ID: SRC-2026-104
- Type: Generated multi-scene GLB / offline HTML / Python / JavaScript
- Generated: 2026-11-06
- Authorization: [Homeowner direction, SRC-2026-103](../../chat/2026/2026-11-06-renovation-bathroom-configurations.md).
- Inputs: [original rotatable model, SRC-2026-094](2026-11-05-bachelor-bathroom-model.md), [v2, SRC-2026-098](2026-11-05-bachelor-bathroom-model-v2.md), [v3, SRC-2026-100](2026-11-05-bachelor-bathroom-model-v3.md), [v4, SRC-2026-102](2026-11-06-bachelor-bathroom-model-v4.md).
- Status: Comparison viewer; no new purchase, order amendment or final construction approval.

## Artifacts and Rebuild

[Combined viewer](../../documents/renovation/bathroom-configurations/dist/index.html) · [four-scene GLB](../../documents/renovation/bathroom-configurations/dist/bathroom-configurations.glb) · [README](../../documents/renovation/bathroom-configurations/README.md) · [generator](../../documents/renovation/bathroom-configurations/generate.py) · [viewer source](../../documents/renovation/bathroom-configurations/viewer.js).

After the cleanup authorized in [SRC-2026-105](../../chat/2026/2026-11-06-renovation-bathroom-cleanup.md), the generator builds all four layouts from local `geometry.py`, then reads `viewer.html`, `viewer.js` and pinned libraries in `vendor/`. No standalone folders or prebuilt input models are needed. Resources are deduplicated across scenes; viewing uses one renderer and one live mirror reflector. The offline HTML embeds the complete model and required libraries. No product evidence was downloaded anew; original product drawings, photos and dimensions remain linked through the input source notes.

## Configuration Rules

All four configurations share **145 right-side meshes from v4**, covering the complete shower including its black profiles, panels, niche, drain, fixture and stool; toilet, behind-toilet storage, bin, robe hook and toilet-paper fittings; and associated right-side wall pieces. Each version retains its original remaining room/left-side meshes and materials. The entrance leaf, handles, hinges and trim remain associated with that version's handing.

The generator selects meshes lying fully beyond the right entrance jamb (minimum authoring X ≥ 48.3 inches), excluding entrance/hinge/casing parts. Geometry comparison verifies that these rules yield the intended v4 right side for all four configurations, including the original model's less-detailed shower being replaced by v4's refined shower.

| Configuration | Scene mesh count | Left-side geometry / mirror | Animated entrance |
|---|---:|---|---|
| V1 | 370 | Original 48-inch Alder at rear, floor linen near front, hamper between; ALEX 900 × 700 mm | Inward-left, assumed hinge X=17.7 / Z=0.9 inches |
| V2 | 376 | 48-inch Alder beside rear-left linen, front-left hamper; ALEX 900 × 700 mm | Inward-right, assumed hinge X=47.8 / Z=0.9 inches |
| V3 | 334 | 36-inch Madison floating furniture; BIBO 600 × 700 mm, top 67.4646 inches | Inward-right, same assumed hinge as v2 |
| V4 | 367 | 36-inch floor Alder/Saxe, matching floor linen; BIBO 600 × 700 mm, top 70.875 inches | Inward-right, same assumed hinge as v2 |

These are configurations of the comparison viewer; the standalone folders were subsequently removed under SRC-2026-105. V1 therefore means the original left-side layout with the newly approved shared right side and animation, rather than a historical full-room snapshot. Source notes for all products and original positions remain applicable.

## Viewer and Export Behavior

- Opens on **v4**, entrance closed, overview camera and automatic wall cutaway.
- Version selector preserves camera position, target, field of view/zoom and display toggles. Selecting a preset then aims at that configuration; the vanity view follows its sink/mirror centre.
- Switching updates furniture, labels, mirror dimensions/position, lighting position, layout finding and assumption notes together.
- Every entrance has Open/Close animation and a 0–90° slider. Each version remembers its current door angle within the session. Switching stops an in-flight animation; reduced motion applies the endpoint immediately. Door panels, handles and moving hinge leaves rotate together and remain visible when walls are hidden.
- V4's five presets, orbit/pan/zoom, keyboard controls, wall/ceiling/glass controls, labels, slow rotation, mirror reflection, lighting, mobile layout and offline operation are retained.
- **Selected GLB:** one scene, referenced resources only, filename `basement-bathroom-vN.glb`; includes v4's shared right side and closed entrance geometry.
- **Combined GLB:** four full-room configuration scenes, default scene v4; filename `bathroom-configurations.glb`. A compatible external viewer must expose scene selection to inspect all versions.
- **PNG:** captures current view, selected layout and current door angle; filename `basement-bathroom-vN.png`.
- Live reflections, lighting presentation and interactive door motion are viewer effects, not exported GLB animation tracks. No hosting deployment performed.

## Verification and Limits

[Geometry report](../../documents/renovation/bathroom-configurations/references/geometry-check.json) and [input/output hashes](../../documents/renovation/bathroom-configurations/references/build-manifest.json).

- All selected source mesh attributes and materials match exactly; each configuration uses the identical v4 right-side geometry. The combined GLB has four scenes and defaults to scene index 3 (v4).
- All 18 moving entrance parts are grouped for animation in each version. Conservative rectangle sweeps with vertical overlap, sampled at each degree 0–90° around the assumed fixed hinge, find no intersection with the tested closed furniture and shower envelopes in any configuration.
- Independent rebuilding from a temporary copy of only `bathroom-configurations/` produces identical outputs. Cleanup comparison confirms all geometry, binary resources, materials and scene settings match the prior combined model exactly; only the standalone-packaging note changed. All 50 reference entries were retained with matching hashes, deduplicating identical files. See [cleanup verification](../../documents/renovation/bathroom-configurations/references/consolidation-check.json).
- [Browser report](../../documents/renovation/bathroom-configurations/references/viewer-check.json): all four selections, camera/zoom preservation, display state, independent door angles, switching during animation, both physical hinge directions, mirror dimensions/positions, presets, reduced motion, selected/combined downloads, PNG export, mobile and offline loading passed. No page errors or external requests. V1, v3 and v4 vanity views, overview and mobile layout were visually reviewed.
- [glTF validation](../../documents/renovation/bathroom-configurations/references/gltf-validation.json): combined model and all four selected-layout exports have zero errors, warnings, informational issues or hints.

## Artifact Integrity

Final artifact byte counts and SHA-256 hashes are in the [build manifest](../../documents/renovation/bathroom-configurations/references/build-manifest.json), together with hashes of the local geometry, generator, viewer and library inputs. The offline viewer is approximately **9.3 MB** and combined model **6.23 MB**; repeated model data is shared.

This consolidation does not resolve existing installation limits: V1's entrance and opened linen doors have overlapping paths; V2's rear-hinged linen doors conflict with rear-wall/window/towel envelopes; V3's low mirror has only 0.18-inch static depth clearance to the schematic faucet lever. V4's mirror retains about 4.10-inch vertical clearance above the static lever. Actual hinge mechanisms, simultaneous openings, plumbing, wiring, faucet motion, hamper access and site measurements remain unverified. Per-configuration findings are shown in the viewer.
