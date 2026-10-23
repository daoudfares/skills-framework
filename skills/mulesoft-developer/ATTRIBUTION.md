# Attribution

The contents of `references/` are derived from MuleSoft's official
documentation, from three sources with three different licences.

| Source | Mule runtime | MUnit | Anypoint Code Builder |
|---|---|---|---|
| Origin | <https://github.com/mulesoft/docs-mule-runtime> | <https://github.com/mulesoft/docs-munit> | <https://docs.mulesoft.com/anypoint-code-builder/> |
| Branch | `v4.12` | `v3.7` | — (no public repository) |
| Pinned at | `fb2ec27bc7de3de79a301e86c6790aea8f1ac31a` | `66c565a92490683aa080a384c1227eab44b46ee9` | digest `19bddf27c4dc3776fb4d5f587376dfb3bc53ad4b` |
| Licence | BSD 3-Clause | Apache 2.0 | see below |
| Copyright | Copyright (c) 2021, Salesforce.com, Inc. | MuleSoft, a Salesforce company | MuleSoft, a Salesforce company |
| Imported | 2026-09-10 | 2026-09-10 | 2026-09-10 |

Licence texts are in `licenses/`. Anypoint Code Builder's documentation is
published only as rendered pages and carries no repository licence file; it is
used here under the terms of the MuleSoft documentation site.

Prose, XML samples and attribute descriptions are MuleSoft's. The selection,
condensation and organisation are not.

## What was derived, and how

Upstream is AsciiDoc (Antora) for the two Git sources — 184 pages for the
runtime, 60 for MUnit — and rendered Markdown for Anypoint Code Builder, 131
pages indexed by its `llms.txt` manifest.

- **The 11 runtime files** and **4 MUnit files** are converted from AsciiDoc and
  concatenated by topic, with headings re-levelled and `See Also` cross-reference
  lists dropped. Antora partials and example files are inlined: `partial$mmp-concept.adoc`
  alone is included 65 times, and dropping it would leave the Maven and
  deployment references full of holes.
- **`components.md`** is built from the 29 `acb-component-*` pages — one entry
  per Core component, reduced to its description, XML skeleton and attribute
  and child-element tables. The worked examples and canvas walkthroughs are cut.
  `doc:name` and `doc:id` are stripped from every table; they are identical on
  all 29 components and `SKILL.md` states the rule once.
- **`acb.md`** and **`troubleshooting.md`** keep only the Anypoint Code Builder
  pages that answer a question an agent editing XML actually has. Anypoint Code
  Builder is a GUI product and most of its documentation is click-through
  walkthroughs; those steps are stripped mechanically.

The rendered `.md` endpoints emit every table as one unwrapped HTML blob. Those
tables carry the payload of the component pages, so `scripts/html2md.py`
recovers them into Markdown rather than stripping them.

## Re-syncing

```sh
git clone --depth 1 --branch v4.12 \
    https://github.com/mulesoft/docs-mule-runtime.git /tmp/mule-runtime
git clone --depth 1 --branch v3.7 \
    https://github.com/mulesoft/docs-munit.git /tmp/munit
python3 scripts/build_references.py \
    --runtime /tmp/mule-runtime --munit /tmp/munit --fetch-acb /tmp/acb
```

The build is deterministic — re-running it on unchanged sources produces
byte-identical output, so `git diff` after a re-sync shows only genuine upstream
change. It prints the Anypoint Code Builder digest to record, and exits non-zero
listing any page upstream has renamed or removed.

Update the pins in the table above when you re-sync, and the versions stated in
`SKILL.md`.

### Scripts

| Script | Does |
|---|---|
| `scripts/build_references.py` | Rebuilds all 18 reference files; also fetches the Anypoint Code Builder pages |
| `scripts/adoc2md.py` | AsciiDoc to Markdown. Adapted from the converter in `dataweave-developer`, with document-attribute support added — the MUnit pages define attributes such as `:port: 1234` and interpolate them inside XML examples |
| `scripts/html2md.py` | Cleans the rendered `.md` pages and recovers their HTML tables |

Both converters run standalone on a single file for debugging.

### Versions

Upstream versions its documentation per release. `docs-mule-runtime` has a
branch per runtime minor (`v4.4` … `v4.12`) and `docs-munit` per MUnit minor.
Pin the branches matching the runtime the applications actually run on — the
component set and available attributes differ between versions. Anypoint Code
Builder publishes only the current version, which is why its identifier is a
digest and `Imported` carries the weight.

DataWeave is deliberately absent: it has its own upstream repository and its own
skill, `dataweave-developer`.
