#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re, shutil

ROOT = Path(__file__).resolve().parents[1]

parser = argparse.ArgumentParser(description="Prepare an Awesome Codex Pet submission folder.")
parser.add_argument("handle", help="GitHub handle / author slug")
parser.add_argument("--pet", default="crt-monitor", help="Pet id from catalog.json")
parser.add_argument("--author", help="Display author name; defaults to handle")
parser.add_argument(
    "--output-dir",
    type=Path,
    default=ROOT / "community" / "generated",
    help="Parent directory for the generated submission",
)
args = parser.parse_args()

raw_handle = args.handle.strip()
handle = re.sub(r"[^a-z0-9-]+", "-", raw_handle.lower()).strip("-")
if not handle:
    raise SystemExit("Invalid handle")

author = args.author or raw_handle
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
entry = next((item for item in catalog["pets"] if item["id"] == args.pet), None)
if entry is None:
    raise SystemExit(f"Unknown pet id: {args.pet}")

pet_dir = ROOT / entry["path"]
runtime_manifest = json.loads((pet_dir / "pet.json").read_text(encoding="utf-8"))
pet_id = runtime_manifest["id"]
slug = f"{pet_id}--{handle}"
dest = args.output_dir.expanduser().resolve() / slug

if dest.exists():
    shutil.rmtree(dest)
dest.mkdir(parents=True)

shutil.copy2(pet_dir / "spritesheet.webp", dest / "spritesheet.webp")

pet = {
    "id": slug,
    "displayName": runtime_manifest["displayName"],
    "description": runtime_manifest["description"],
    "spriteVersionNumber": 2,
    "spritesheetPath": "spritesheet.webp"
}
(dest / "pet.json").write_text(json.dumps(pet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

submission = {
    "slug": slug,
    "pet_slug": pet_id,
    "author_slug": handle,
    "name": runtime_manifest["displayName"],
    "localized_names": entry["community"]["localizedNames"],
    "author": author,
    "primary_category": entry["community"]["primaryCategory"],
    "canonical_key": f"original/{handle}/{pet_id}",
    "tags": entry["community"]["tags"],
    "source_type": "original",
    "source_url": f"https://github.com/{raw_handle}/codex-pets/tree/main/{entry['path']}",
    "license": entry["artworkLicense"],
    "preview_image": f"../../assets/previews/{slug}/gifs/idle.gif",
    "codex_install": {
        "pet_json": "pet.json",
        "spritesheet": "spritesheet.webp"
    }
}
(dest / "submission.json").write_text(
    json.dumps(submission, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print(dest)
print("Ready for the Awesome Codex Pet submission folder.")
