# Basement Bathroom — Concept v2

Separate layout study dated November 5, 2026: rear-left linen cabinet facing the toilet with handles left; vanity alongside; front-left hamper; inward-right entrance door, closed by default; side-by-side light dimmer and vent switch left of the entrance (dimmer left / vent right when facing the plate); outlet beside vanity.

The earlier [bathroom-concept](../bathroom-concept/README.md) is preserved.

## Files

```text
bathroom-concept-v2/
  README.md
  generate.py
  references/
  dist/
    index.html
    bathroom.glb
```

- [Offline viewer](dist/index.html): five view presets, wall cutaways, animated Open/Close entrance door, angle slider, GLB download and PNG export. Reduced-motion preference skips the animation.
- [GLB model](dist/bathroom.glb): entrance door fixed at the initial closed pose; viewer door changes do not alter the downloaded file.
- `references/`: identical copies of the earlier archived product PDFs and photographs. Provenance remains in [SRC-2026-096](../../../extractions/2026/2026-11-05-bathroom-product-dimensions.md).

## Rebuild

```sh
python3 generate.py
```

Python 3 standard library only. Bundled viewer libraries require no downloads. The generator resolves `dist/` beside itself, independent of the working directory, and replaces only this concept's generated files.

## Publish

Publish only `01-sources/documents/renovation/bathroom-concept-v2/dist/`. Hosting publication remains separate. The viewer is address-free and titled **Basement bathroom · Concept v2**. Exported PNG name: `basement-bathroom-concept-v2.png`.

Black shower profiles and sliding hardware follow the archived Alaska product photograph; detailed extrusion dimensions are schematic. The entrance door starts closed with an **Open door** button.

## Clearance Finding

The entrance-door envelope clears the modeled shower and furniture in a simplified 0–90° sweep. **The rear-hinged linen doors conflict with the rear wall and assumed window/towel fittings during opening.** Rear-wall contact is retained to show the requested arrangement; cabinet spacing and rear fittings need review. Actual hinges, room/window measurements and installation clearances remain unverified.

## Source Records

- [Homeowner directions — SRC-2026-097](../../../chat/2026/2026-11-05-renovation-bathroom-concept-v2.md).
- [Model assumptions, verification and integrity — SRC-2026-098](../../../extractions/2026/2026-11-05-bachelor-bathroom-model-v2.md).
