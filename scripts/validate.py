#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
COLS, ROWS = 8, 11
CELL_W, CELL_H = 192, 208
EXPECTED_SIZE = (COLS * CELL_W, ROWS * CELL_H)
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

CRT_COMPATIBILITY_FILES = {
    ROOT / "pet/pet.json": ROOT / "pets/crt-monitor/pet.json",
    ROOT / "pet/spritesheet.webp": ROOT / "pets/crt-monitor/spritesheet.webp",
    ROOT / "assets/source-design.png": ROOT / "pets/crt-monitor/assets/source-design.png",
    ROOT / "assets/preview-grid.png": ROOT / "pets/crt-monitor/assets/preview-grid.png",
    ROOT / "assets/frame-audit.md": ROOT / "pets/crt-monitor/assets/frame-audit.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_catalog() -> tuple[dict, list[str]]:
    errors: list[str] = []
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        return {}, [f"catalog.json unreadable: {exc}"]
    if catalog.get("schemaVersion") != 1:
        errors.append("catalog.json schemaVersion must be 1")
    pets = catalog.get("pets")
    if not isinstance(pets, list) or not pets:
        errors.append("catalog.json pets must be a non-empty array")
    return catalog, errors


def validate_source_assets(pet_dir: Path, pet_id: str, runtime_rgba: Image.Image | None) -> list[str]:
    errors: list[str] = []
    source_dir = pet_dir / "assets/source"
    manifest_path = source_dir / "SHA256SUMS"
    notes_path = source_dir / "README.md"
    master_path = source_dir / "runtime-atlas-rgba.png"

    for required_path in (source_dir, manifest_path, notes_path, master_path):
        if not required_path.exists():
            errors.append(f"missing {required_path.relative_to(pet_dir)}")
    if not manifest_path.is_file():
        return errors

    listed_files: set[str] = set()
    for line_number, line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or not SHA256_PATTERN.fullmatch(parts[0]):
            errors.append(f"assets/source/SHA256SUMS:{line_number}: invalid entry")
            continue
        expected_digest, filename = parts
        filename = filename.strip()
        if Path(filename).name != filename:
            errors.append(f"assets/source/SHA256SUMS:{line_number}: filename must be local")
            continue
        listed_files.add(filename)
        asset_path = source_dir / filename
        if not asset_path.is_file():
            errors.append(f"assets/source/SHA256SUMS:{line_number}: missing {filename}")
        elif sha256(asset_path) != expected_digest:
            errors.append(f"assets/source/SHA256SUMS:{line_number}: checksum mismatch for {filename}")

    actual_pngs = {path.name for path in source_dir.glob("*.png")}
    if listed_files != actual_pngs:
        errors.append(
            "assets/source/SHA256SUMS coverage differs: "
            f"listed={sorted(listed_files)}, actual={sorted(actual_pngs)}"
        )

    if master_path.is_file():
        try:
            with Image.open(master_path) as source_master:
                master_format = source_master.format
                master_size = source_master.size
                master_rgba = source_master.convert("RGBA")
            if master_format != "PNG":
                errors.append(f"assets/source/runtime-atlas-rgba format: expected PNG, got {master_format}")
            if master_size != EXPECTED_SIZE:
                errors.append(
                    "assets/source/runtime-atlas-rgba size: "
                    f"expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}, "
                    f"got {master_size[0]}x{master_size[1]}"
                )
            if runtime_rgba is not None and master_rgba.tobytes() != runtime_rgba.tobytes():
                errors.append("assets/source/runtime-atlas-rgba decoded pixels differ from spritesheet.webp")
        except Exception as exc:
            errors.append(f"assets/source/runtime-atlas-rgba unreadable: {exc}")

    design_mirror_name = {
        "crt-monitor": "design-board-final-8col.png",
        "ai-pulse": "logo-original.png",
    }.get(pet_id)
    if design_mirror_name:
        design_path = pet_dir / "assets/source-design.png"
        archived_design_path = source_dir / design_mirror_name
        if archived_design_path.is_file() and sha256(archived_design_path) != sha256(design_path):
            errors.append(f"assets/source/{design_mirror_name} differs from assets/source-design.png")

    return errors


def validate_pet(entry: dict) -> list[str]:
    errors: list[str] = []
    pet_id = entry.get("id")
    if not isinstance(pet_id, str) or not ID_PATTERN.fullmatch(pet_id):
        return [f"catalog pet id is invalid: {pet_id!r}"]

    expected_path = f"pets/{pet_id}"
    if entry.get("path") != expected_path:
        errors.append(f"catalog path: expected {expected_path!r}, got {entry.get('path')!r}")
    pet_dir = ROOT / expected_path
    manifest_path = pet_dir / "pet.json"
    sprite_path = pet_dir / "spritesheet.webp"

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"pet.json unreadable: {exc}")
        manifest = {}

    required = {
        "id": pet_id,
        "displayName": entry.get("displayName"),
        "spriteVersionNumber": 2,
        "spritesheetPath": "spritesheet.webp",
    }
    for key, value in required.items():
        if manifest.get(key) != value:
            errors.append(f"pet.json {key!r}: expected {value!r}, got {manifest.get(key)!r}")
    if not isinstance(manifest.get("description"), str) or not manifest.get("description", "").strip():
        errors.append("pet.json description must be a non-empty string")

    for required_file in (
        "README.md",
        "LICENSE-ARTWORK",
        "assets/source-design.png",
        "assets/preview-grid.png",
        "assets/frame-audit.md",
        "assets/spritesheet.sha256",
    ):
        if not (pet_dir / required_file).is_file():
            errors.append(f"missing {required_file}")

    preview_path = pet_dir / "assets/preview-grid.png"
    if preview_path.is_file():
        try:
            with Image.open(preview_path) as preview:
                if preview.format != "PNG":
                    errors.append(f"preview-grid format: expected PNG, got {preview.format}")
                if preview.size != EXPECTED_SIZE:
                    errors.append(
                        f"preview-grid size: expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}, "
                        f"got {preview.size[0]}x{preview.size[1]}"
                    )
        except Exception as exc:
            errors.append(f"preview-grid unreadable: {exc}")

    try:
        with Image.open(sprite_path) as source:
            source_size = source.size
            source_format = source.format
            im = source.convert("RGBA")
    except Exception as exc:
        errors.append(f"spritesheet unreadable: {exc}")
        im = None
        source_size = None
        source_format = None

    checksum_path = pet_dir / "assets/spritesheet.sha256"
    if sprite_path.is_file() and checksum_path.is_file():
        expected_digest = checksum_path.read_text(encoding="utf-8").split(maxsplit=1)[0]
        actual_digest = sha256(sprite_path)
        if expected_digest != actual_digest:
            errors.append(
                f"spritesheet checksum: expected {expected_digest}, got {actual_digest}"
            )

    if im is not None:
        if source_format != "WEBP":
            errors.append(f"spritesheet format: expected WEBP, got {source_format}")
        if source_size != EXPECTED_SIZE:
            errors.append(
                f"spritesheet size: expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}, "
                f"got {source_size[0]}x{source_size[1]}"
            )
        if im.getchannel("A").getextrema() == (255, 255):
            errors.append("spritesheet appears fully opaque; transparent background expected")

        if source_size == EXPECTED_SIZE:
            touching = []
            for row in range(ROWS):
                for col in range(COLS):
                    cell = im.crop(
                        (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
                    )
                    bbox = cell.getchannel("A").getbbox()
                    if bbox:
                        left, top, right, bottom = bbox
                        margins = (left, top, CELL_W - right, CELL_H - bottom)
                        if min(margins) < 2:
                            touching.append((row + 1, col + 1, margins))
            if touching:
                errors.append(
                    "frames within 2 px of a cell edge: "
                    + ", ".join(f"r{r}c{c} margins={m}" for r, c, m in touching)
                )

    errors.extend(validate_source_assets(pet_dir, pet_id, im))

    return errors


def validate_compatibility() -> list[str]:
    errors: list[str] = []
    for legacy, canonical in CRT_COMPATIBILITY_FILES.items():
        if not legacy.is_file():
            errors.append(f"missing compatibility file {legacy.relative_to(ROOT)}")
        elif not canonical.is_file():
            errors.append(f"missing canonical file {canonical.relative_to(ROOT)}")
        elif sha256(legacy) != sha256(canonical):
            errors.append(
                f"compatibility mirror differs: {legacy.relative_to(ROOT)} != "
                f"{canonical.relative_to(ROOT)}"
            )
    return errors


parser = argparse.ArgumentParser(description="Validate one or all pets in the collection.")
parser.add_argument("pet_id", nargs="?", help="Pet id from catalog.json")
parser.add_argument("--all", action="store_true", help="Validate every catalog entry")
args = parser.parse_args()
if args.pet_id and args.all:
    parser.error("choose a pet id or --all, not both")

catalog, errors = load_catalog()
entries = catalog.get("pets", []) if isinstance(catalog.get("pets"), list) else []
ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
if len(ids) != len(set(ids)):
    errors.append("catalog.json contains duplicate pet ids")

requested = None if args.all or not args.pet_id else args.pet_id
selected = [
    entry
    for entry in entries
    if isinstance(entry, dict) and (requested is None or entry.get("id") == requested)
]
if requested and not selected:
    errors.append(f"unknown pet id: {requested}")

for entry in selected:
    pet_errors = validate_pet(entry)
    errors.extend(f"{entry.get('id', '<unknown>')}: {message}" for message in pet_errors)

errors.extend(f"compatibility: {message}" for message in validate_compatibility())

if errors:
    print("VALIDATION FAILED")
    for error in errors:
        print(" -", error)
    sys.exit(1)

validated_ids = ", ".join(str(entry["id"]) for entry in selected)
print("VALIDATION PASSED")
print(f" - catalog: {len(entries)} pet(s), schemaVersion 1")
print(f" - validated: {validated_ids}")
print(f" - each spritesheet: {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]} WebP")
print(f" - grid: {COLS}x{ROWS} @ {CELL_W}x{CELL_H}")
print(" - transparency and cell-edge safety: OK")
print(" - CRT Monitor compatibility mirrors: byte-identical")
