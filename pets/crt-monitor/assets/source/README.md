# CRT Monitor source assets

These files preserve the highest-value confirmed artwork used to maintain CRT
Monitor. They are source material, not runtime package files.

| File | Role |
| --- | --- |
| `design-board-original-9col.png` | Original full design board preserved from repository commit `31ef43b`; includes the unlabeled ninth working column. Keep for provenance and recovery. |
| `design-board-final-8col.png` | Corrected eight-column design board. This is an exact byte mirror of `../source-design.png`. |
| `runtime-atlas-rgba.png` | Lossless RGBA editing master decoded from `../../spritesheet.webp` at its native `1536×2288` size. |
| `SHA256SUMS` | Checksums for every binary source asset in this directory. |

Do not edit CRT Monitor from the small cards in the repository-level
`assets/readme/` directory. Start with the preserved design board or RGBA atlas
master, export a new runtime WebP, and then regenerate the preview and audit.

