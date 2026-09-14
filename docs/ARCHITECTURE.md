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
    └── spritesheet.sha256
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
