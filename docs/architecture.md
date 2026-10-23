# Architecture

## Principles

1. **Agent-agnostic.** No skill assumes Claude Code. Claude-specific bits (deny rules,
   plugin packaging) are optional layers.
2. **Self-contained skills.** Each skill folder works on its own.
3. **Read-only by default** for any skill touching production data.
4. **Tests centralised** under `tools/tests` and per-skill `tests/`, with unique
   module names so the whole suite collects in one run.
5. **One source of truth.** Skills live in `skills/`; everything else is tooling.

## Folders

- `framework/` — conventions, patterns, skill template.
- `skill-creator/` — create and evaluate skills.
- `tools/` — export, installer, sql_guard, tests.
- `skills/` — skills shipped with the framework (generic examples + reference skills).
- `docs/` — architecture, contribution, migration.
