# Basement Bathroom — Compare Configurations

[Open combined viewer](dist/index.html) · [Four-scene GLB](dist/bathroom-configurations.glb).

One offline viewer with **V1 / V2 / V3 / V4** selection, opening on v4. All versions use **v4's complete right-side fixtures**; each keeps its left-side layout and doorway handing. V1 refers to the original rotatable concept.

| Configuration | Left-side arrangement | Entrance swing |
|---|---|---|
| V1 | 48-inch Alder at rear, floor linen near entrance, hamper between them, 36 × 28 ALEX | Inward-left |
| V2 | 48-inch Alder beside rear-left floor linen, front-left hamper, 36 × 28 ALEX | Inward-right toward shower |
| V3 | 36-inch floating Madison and wall linen, 24 × 28 BIBO | Inward-right toward shower |
| V4 | 36-inch floor Alder, Saxe VT-SQ907 porcelain, floor linen, 24 × 28 BIBO | Inward-right toward shower |

Switching preserves camera position, zoom and display settings. Each layout remembers its own door angle for the current session. The door remains visible with wall cutaways. Five presets, reflections/lighting, labels, slow rotation, keyboard/zoom controls, reduced-motion support and mobile layout follow v4.

The selected-layout download contains one scene and only its referenced resources. The combined download contains four scenes, defaulting to v4. Both export closed entrance geometry; interactive door animation and live reflections are viewer effects. PNG captures the active view and door pose. Exports include the selected version in their filenames.

## Rebuild

```sh
python3 generate.py
```

Python 3 standard library only. From this folder run the command above, or invoke `generate.py` by its full path from any directory. All inputs are local: `geometry.py` builds V1–V4 in separate namespaces using shared construction code and explicit layout branches; `viewer.html` and `viewer.js` define the viewer; `vendor/` contains pinned Three.js r169 libraries and the MIT license. No sibling folders, prebuilt input GLBs or downloads are required.

The generator writes `dist/index.html`, `dist/bathroom-configurations.glb` and `references/build-manifest.json`. Identical geometry/materials/textures are shared in the combined model. The complete `dist/` is portable and offline; no network or source folders are needed at viewing time. For future static hosting, publish only `dist/`. No hosting publication is part of this work.

## Evidence and Checks

- [Homeowner direction, SRC-2026-103](../../../chat/2026/2026-11-06-renovation-bathroom-configurations.md).
- [Model provenance, assumptions and verification, SRC-2026-104](../../../extractions/2026/2026-11-06-bathroom-combined-configurations.md).
- [Build manifest](references/build-manifest.json), [geometry and entrance sweeps](references/geometry-check.json).
- [Browser checks](references/viewer-check.json), [combined and selected GLB validation](references/gltf-validation.json).

Existing layout limits remain visible: V1 entrance/linen opening paths overlap when both are opened; V2 has the documented linen/rear-wall conflict; V3 has a tight static mirror/faucet depth gap. Actual hinges, plumbing and site clearances remain unverified.

The four standalone folders were removed under [SRC-2026-105](../../../chat/2026/2026-11-06-renovation-bathroom-cleanup.md). Unique product drawings, photographs and historical check reports are retained in `references/`. The [consolidation manifest](references/consolidation-manifest.json) records each former reference path, retained path and SHA-256; [cleanup checks](references/consolidation-check.json) verify preservation and independent rebuilding. Historical source notes remain linked from SRC-2026-104.
