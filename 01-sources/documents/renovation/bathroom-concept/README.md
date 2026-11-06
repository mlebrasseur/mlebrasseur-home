# Basement Bathroom — Current Concept

Rotatable concept for the basement bathroom, with recorded dimensions, selected materials and provisional installation details. The public viewer omits the property address.

## Files

```text
bathroom-concept/
  generate.py
  references/
  dist/
    index.html
    bathroom.glb
```

- `generate.py`: self-contained Python generator with bundled viewer libraries.
- `references/`: product drawings and reference photographs used to check the model.
- [dist/index.html](dist/index.html): self-contained viewer, usable offline or on a static website.
- [dist/bathroom.glb](dist/bathroom.glb): downloadable 3D model.

## Rebuild

From this directory:

```sh
python3 generate.py
```

The generator also works when invoked by path from another directory. It writes only the two files in its adjacent `dist/`, replacing the current concept without numbered versions. Python 3 standard library only; no build-time downloads.

## Publish

Upload **only the contents of this directory's `dist/`**. For hosting configured from the repository root, set the publish directory to:

```text
01-sources/documents/renovation/bathroom-concept/dist
```

The public heading is **Basement bathroom**, with **Current concept · Layout, materials and fixtures** beneath it. The viewer exports `bathroom.glb` and `basement-bathroom-current-concept.png`. No property address is included. Publishing is performed separately by the homeowner.

## Source Records

House records retain their established source locations:

- [Model provenance, assumptions, validation and hashes — SRC-2026-094](../../../extractions/2026/2026-11-05-bachelor-bathroom-model.md).
- [Product dimensions and reference-file provenance — SRC-2026-096](../../../extractions/2026/2026-11-05-bathroom-product-dimensions.md).
- [Homeowner directions — SRC-2026-095](../../../chat/2026/2026-11-05-renovation-bathroom-model-corrections.md).

The model is a spatial concept. Actual hinge motion, final door cut height, plumbing and installation clearances remain to verify.
