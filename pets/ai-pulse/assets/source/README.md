# AI Pulse source assets

These files preserve the confirmed artwork needed to modify AI Pulse without
using a generated preview or a compressed presentation image as the next
editing source.

| File | Role |
| --- | --- |
| `logo-original.png` | Exact byte mirror of the user-provided `AI Pulse-Logo.001.png` and `../source-design.png`. This is the character identity baseline. |
| `runtime-atlas-rgba.png` | Lossless RGBA editing master decoded from `../../spritesheet.webp` at its native `1536×2288` size, including all 88 populated cells. |
| `SHA256SUMS` | Checksums for every binary source asset in this directory. |

Use `logo-original.png` to protect character identity and
`runtime-atlas-rgba.png` for frame-level edits. After exporting a new runtime
WebP, regenerate the preview, checksum, and frame audit. Do not use the small
repository-level README card as an editing source.

