# Multi-pet repository layout

`pets/<pet-id>/` is the canonical home for every pet. Each directory is a
self-contained package:

```text
pets/<pet-id>/
├── pet.json
├── spritesheet.webp
├── README.md
├── LICENSE-ARTWORK
└── assets/
    ├── source-design.png
    ├── preview-grid.png
    ├── frame-audit.md
    ├── spritesheet.sha256
    └── source/
        ├── README.md
        ├── SHA256SUMS
        ├── runtime-atlas-rgba.png
        └── <pet-specific original artwork>
```

`catalog.json` is the machine-readable index. Add a pet there only after its
runtime package passes `python3 scripts/validate.py <pet-id>`.

## Compatibility contract

The original CRT Monitor release predates the collection layout. Its root
`pet/` runtime and selected root `assets/` files remain published compatibility
mirrors because existing install instructions and external pages reference
those exact paths.

The validator checks these mirrors byte-for-byte against
`pets/crt-monitor/`. Do not edit one copy without updating the other. New pets
do not need root-level mirrors.

## Source asset preservation

The files under the repository-level `assets/readme/` directory and each pet's
`assets/preview-grid.png` are presentation artifacts. Never use them as the
source for another artwork edit.

Each pet keeps its irreplaceable original inputs and a native-resolution,
lossless RGBA atlas under `pets/<pet-id>/assets/source/`. The source directory
also contains a checksum manifest and provenance notes. The runtime WebP
remains the installable artifact; the RGBA PNG is the editing master whose
decoded pixels must match that WebP until an intentional artwork revision is
made.

When artwork changes:

1. Start from an original input or `runtime-atlas-rgba.png`, never a README card.
2. Preserve the previous source assets in Git history and update provenance.
3. Export `spritesheet.webp` at the required native dimensions.
4. Regenerate `preview-grid.png`, `frame-audit.md`, and `spritesheet.sha256`.
5. Refresh `assets/source/SHA256SUMS` and run the full validator.

## Adding a pet

1. Create `pets/<pet-id>/` using the package layout above.
2. Add the pet to `catalog.json`.
3. Generate its contact sheet and frame audit:
   `python3 scripts/generate-preview-and-audit.py <pet-id>`.
4. Run `python3 scripts/validate.py <pet-id>` and then
   `python3 scripts/validate.py --all`.
5. Install a local test copy with `./scripts/install.sh <pet-id>`.

Artwork may have a pet-specific license. The shared code and scripts remain
under the repository's MIT license.
