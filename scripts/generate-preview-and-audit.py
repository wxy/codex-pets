#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from collections import defaultdict
from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
COLS, ROWS = 8, 11
CELL_W, CELL_H = 192, 208
EXPECTED_SIZE = (COLS * CELL_W, ROWS * CELL_H)


def pet_ids() -> list[str]:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    return [entry["id"] for entry in catalog["pets"]]


def generate(pet_id: str) -> None:
    pet_dir = ROOT / "pets" / pet_id
    spritesheet = pet_dir / "spritesheet.webp"
    assets = pet_dir / "assets"
    preview_path = assets / "preview-grid.png"
    audit_path = assets / "frame-audit.md"
    checksum_path = assets / "spritesheet.sha256"
    assets.mkdir(parents=True, exist_ok=True)

    atlas = Image.open(spritesheet).convert("RGBA")
    if atlas.size != EXPECTED_SIZE:
        raise SystemExit(f"{pet_id}: expected {EXPECTED_SIZE}, got {atlas.size}")

    # The checkerboard is only a preview backdrop. Atlas pixels are composited
    # at native 1:1 resolution with no scaling or interpolation.
    checker = Image.new("RGBA", atlas.size, "#f2f4f4")
    draw = ImageDraw.Draw(checker)
    checker_size = 32
    for y in range(0, atlas.height, checker_size):
        for x in range(0, atlas.width, checker_size):
            if (x // checker_size + y // checker_size) % 2:
                draw.rectangle(
                    (
                        x,
                        y,
                        min(x + checker_size - 1, atlas.width - 1),
                        min(y + checker_size - 1, atlas.height - 1),
                    ),
                    fill="#d7dbdc",
                )
    preview = Image.alpha_composite(checker, atlas)
    guide = ImageDraw.Draw(preview)
    for x in range(0, atlas.width + 1, CELL_W):
        edge = min(x, atlas.width - 1)
        guide.line((edge, 0, edge, atlas.height - 1), fill="#00a88f", width=1)
    for y in range(0, atlas.height + 1, CELL_H):
        edge = min(y, atlas.height - 1)
        guide.line((0, edge, atlas.width - 1, edge), fill="#00a88f", width=1)
    preview.convert("RGB").save(preview_path, format="PNG", optimize=True)

    frame_hashes = []
    hash_locations = defaultdict(list)
    for row in range(ROWS):
        row_hashes = []
        for col in range(COLS):
            frame = atlas.crop(
                (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
            )
            digest = sha256(frame.tobytes()).hexdigest()
            row_hashes.append(digest)
            hash_locations[digest].append((row + 1, col + 1))
        frame_hashes.append(row_hashes)

    column_hashes = []
    for col in range(COLS):
        column_bytes = b"".join(
            atlas.crop(
                (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
            ).tobytes()
            for row in range(ROWS)
        )
        column_hashes.append(sha256(column_bytes).hexdigest())

    duplicates = [
        (digest, locations) for digest, locations in hash_locations.items() if len(locations) > 1
    ]
    grouped_columns = defaultdict(list)
    for col, digest in enumerate(column_hashes, 1):
        grouped_columns[digest].append(col)
    duplicate_column_groups = [columns for columns in grouped_columns.values() if len(columns) > 1]

    atlas_digest = sha256(spritesheet.read_bytes()).hexdigest()
    lines = [
        f"# {pet_id} Runtime Sprite Audit",
        "",
        f"- Atlas: `{atlas.width}×{atlas.height}` WebP",
        f"- Grid: `{COLS}×{ROWS}` (`{COLS * ROWS}` frames)",
        f"- Cell: `{CELL_W}×{CELL_H}` RGBA after decoding",
        f"- Atlas SHA-256: `{atlas_digest}`",
        "- Method: SHA-256 over every decoded RGBA cell; SHA-256 over each complete 11-frame column.",
        "",
        "## Duplicate result",
        "",
    ]
    if duplicates:
        lines.extend(["Exact duplicate decoded frames were found:", ""])
        for digest, locations in duplicates:
            joined = ", ".join(f"R{row}C{col}" for row, col in locations)
            lines.append(f"- `{digest}`: {joined}")
    else:
        lines.append("No exact duplicate decoded frames were found among the 88 cells.")
    lines.extend(
        [
            "",
            "No complete duplicate columns were found."
            if not duplicate_column_groups
            else f"Duplicate column groups: {duplicate_column_groups}",
            "",
            "## Per-frame hashes",
            "",
            "| Row | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row, hashes in enumerate(frame_hashes, 1):
        lines.append("| " + str(row) + " | " + " | ".join(f"`{digest[:12]}`" for digest in hashes) + " |")
    lines.extend(["", "## Per-column hashes", ""])
    for col, digest in enumerate(column_hashes, 1):
        lines.append(f"- C{col}: `{digest}`")
    lines.append("")
    audit_path.write_text("\n".join(lines), encoding="utf-8")
    checksum_path.write_text(
        f"{atlas_digest}  pets/{pet_id}/spritesheet.webp\n", encoding="utf-8"
    )

    # Preserve the externally referenced CRT Monitor paths as exact mirrors.
    if pet_id == "crt-monitor":
        shutil.copy2(preview_path, ROOT / "assets/preview-grid.png")
        shutil.copy2(audit_path, ROOT / "assets/frame-audit.md")
        (ROOT / "assets/spritesheet.sha256").write_text(
            f"{atlas_digest}  pet/spritesheet.webp\n", encoding="utf-8"
        )

    print(f"{pet_id}: wrote {preview_path.relative_to(ROOT)} ({preview.width}x{preview.height})")
    print(f"{pet_id}: wrote {audit_path.relative_to(ROOT)}")
    print(f"{pet_id}: wrote {checksum_path.relative_to(ROOT)}")
    print(f"{pet_id}: exact duplicate frame groups: {len(duplicates)}")
    print(f"{pet_id}: exact duplicate column groups: {len(duplicate_column_groups)}")


parser = argparse.ArgumentParser(description="Generate contact sheets and frame audits.")
parser.add_argument("pet_id", nargs="?", help="Pet id from catalog.json")
parser.add_argument("--all", action="store_true", help="Generate assets for every catalog entry")
args = parser.parse_args()
if args.pet_id and args.all:
    parser.error("choose a pet id or --all, not both")

available = pet_ids()
requested = available if args.all or not args.pet_id else [args.pet_id]
unknown = [pet_id for pet_id in requested if pet_id not in available]
if unknown:
    raise SystemExit(f"unknown pet id(s): {', '.join(unknown)}")
for selected_id in requested:
    generate(selected_id)
