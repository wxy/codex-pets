# CRT Monitor

A tiny retro monitor that keeps an eye on your code.

![CRT Monitor design](assets/source-design.png)

## Runtime

- Codex Pet v2
- `1536×2288` transparent WebP atlas
- `8×11` grid with `192×208` cells
- 88 audited frames

Install from the repository root:

```bash
./scripts/install.sh crt-monitor
```

The [contact sheet](assets/preview-grid.png) is generated at native resolution.
The [frame audit](assets/frame-audit.md) records every decoded cell and column
hash. The [runtime checksum](assets/spritesheet.sha256) pins the exact atlas.
Artwork is licensed under [CC BY 4.0](LICENSE-ARTWORK).
