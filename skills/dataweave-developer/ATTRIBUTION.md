# Attribution

The contents of `references/` are derived from MuleSoft's official DataWeave
documentation.

| | |
|---|---|
| Source | <https://github.com/mulesoft/docs-dataweave> |
| Branch | `v2.12` |
| Pinned commit | `23bcd8bdd485df22022e95ce6a22d191e4f5001a` |
| License | BSD 3-Clause (`LICENSE.txt`) |
| Copyright | Copyright (c) 2021, Salesforce.com, Inc. All rights reserved. |
| Imported | 2026-09-02 |

## What was derived, and how

The upstream documentation is AsciiDoc (Antora), roughly 34 MB across 484 pages.
It was converted to Markdown and condensed:

- **The 23 module files** (`core.md`, `strings.md`, and so on) are generated from
  the 321 per-function pages — one file per `dw::` module, each function reduced
  to its signatures, description, parameter list and first worked example.
- **`language.md`, `selectors.md`, `types.md`, `formats.md` and
  `troubleshooting.md`** are converted from the corresponding language and format
  pages, with headings re-levelled for concatenation.

Prose, signatures and examples are MuleSoft's. The selection, condensation and
organisation are not.

## Re-syncing

The files under `references/` are derived artifacts. Regenerate them rather than
hand-editing:

```sh
git clone --depth 1 --branch v2.12 \
    https://github.com/mulesoft/docs-dataweave.git /tmp/dwdocs
python3 scripts/build_references.py --source /tmp/dwdocs
```

`scripts/build_references.py` rebuilds all 28 files; `scripts/adoc2md.py` is the
AsciiDoc converter it uses, and also runs standalone on a single page. The build
is deterministic — re-running it on an unchanged checkout produces byte-identical
output, so `git diff` after a re-sync shows only genuine upstream changes.

Update the pinned commit and branch above when you re-sync, and the DataWeave
version stated in `SKILL.md`.

Upstream is versioned per DataWeave release (`v2.3` … `v2.12`). Pin the branch
matching the Mule runtime the scripts actually run on — the function set differs
between versions.
