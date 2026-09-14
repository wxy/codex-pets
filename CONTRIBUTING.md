# Contributing

Thanks for improving the Codex Pet collection.

## Good contributions

- Fix clipping, scale popping, baseline jumps, or animation continuity.
- Improve installer or validation scripts.
- Improve documentation and translations.
- Add screen expressions that preserve the meaning of the runtime state.
- Propose alternate visual variants without replacing the canonical original.
- Add a self-contained pet under `pets/<pet-id>/` and register it in `catalog.json`.

## Asset rules

The shared code and scripts are MIT licensed. Each pet declares its own artwork
license in `pets/<pet-id>/LICENSE-ARTWORK`. By contributing artwork, you confirm
that you have the right to distribute it under the declared license.

Do not remove the root CRT Monitor compatibility files. The validator requires
them to remain byte-identical to `pets/crt-monitor/` because external pages
reference their historical paths.

## Before opening a pull request

Run:

```bash
python3 scripts/validate.py --all
```

For an Awesome Codex Pet submission, generate a clean three-file folder:

```bash
python3 scripts/prepare-community-submission.py YOUR_GITHUB_HANDLE --pet PET_ID
```

Do not put QA previews, README files, or source art inside the community pet folder.
