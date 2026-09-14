#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


COLS, ROWS = 8, 11
CELL_W, CELL_H = 192, 208
EXPECTED_SIZE = (COLS * CELL_W, ROWS * CELL_H)


parser = argparse.ArgumentParser(
    description="Inset every Codex Pet v2 frame while preserving its cell and alpha channel."
)
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
parser.add_argument("--inset", type=int, default=6)
parser.add_argument("--remove-edge-components-below", type=int, default=500)
args = parser.parse_args()

if not 2 <= args.inset <= 24:
    parser.error("--inset must be between 2 and 24 pixels")

with Image.open(args.source) as source:
    atlas = source.convert("RGBA")

if atlas.size != EXPECTED_SIZE:
    raise SystemExit(f"expected {EXPECTED_SIZE}, got {atlas.size}")

target_w = CELL_W - 2 * args.inset
target_h = CELL_H - 2 * args.inset
normalized = Image.new("RGBA", EXPECTED_SIZE, (0, 0, 0, 0))


def remove_small_edge_components(cell: Image.Image, area_limit: int) -> Image.Image:
    cleaned = cell.copy()
    alpha = cleaned.getchannel("A")
    pixels = alpha.load()
    visited: set[tuple[int, int]] = set()

    for y in range(CELL_H):
        for x in range(CELL_W):
            if pixels[x, y] <= 8 or (x, y) in visited:
                continue
            stack = [(x, y)]
            visited.add((x, y))
            points: list[tuple[int, int]] = []
            while stack:
                point = stack.pop()
                points.append(point)
                px, py = point
                for neighbor in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    nx, ny = neighbor
                    if (
                        0 <= nx < CELL_W
                        and 0 <= ny < CELL_H
                        and neighbor not in visited
                        and pixels[nx, ny] > 8
                    ):
                        visited.add(neighbor)
                        stack.append(neighbor)

            min_x = min(point[0] for point in points)
            min_y = min(point[1] for point in points)
            max_x = max(point[0] for point in points) + 1
            max_y = max(point[1] for point in points) + 1
            touches_edge = min_x == 0 or min_y == 0 or max_x == CELL_W or max_y == CELL_H
            width = max_x - min_x
            height = max_y - min_y
            near_vertical_edge = min_x < 24 or max_x > CELL_W - 24
            narrow_edge_sliver = (
                near_vertical_edge
                and width <= 4
                and height >= 10
                and len(points) < 100
            )
            if (touches_edge and len(points) < area_limit) or narrow_edge_sliver:
                erase_box = (
                    max(0, min_x - 1),
                    max(0, min_y - 1),
                    min(CELL_W, max_x + 1),
                    min(CELL_H, max_y + 1),
                )
                cleaned.paste((0, 0, 0, 0), erase_box)

    return cleaned


for row in range(ROWS):
    for col in range(COLS):
        box = (
            col * CELL_W,
            row * CELL_H,
            (col + 1) * CELL_W,
            (row + 1) * CELL_H,
        )
        cell = remove_small_edge_components(
            atlas.crop(box), args.remove_edge_components_below
        )
        # Resize premultiplied RGBA so transparent source pixels cannot tint the
        # antialiased edge of the character.
        inset_cell = cell.convert("RGBa").resize(
            (target_w, target_h), Image.Resampling.LANCZOS
        ).convert("RGBA")
        normalized.alpha_composite(
            inset_cell,
            (col * CELL_W + args.inset, row * CELL_H + args.inset),
        )

normalized.save(args.destination, format="PNG", optimize=True)
print(
    f"wrote {args.destination} as {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]} "
    f"with {args.inset}px frame insets"
)
