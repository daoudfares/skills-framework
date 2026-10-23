# Migrating a skill from a company-specific repo

1. Copy the skill folder into `skills/<name>/`.
2. Remove company-specific references: database names, domain names, flow names,
   internal ADR numbers (replace with "your decision record #N").
3. Replace company-specific macro/tool names with placeholders and document the
   adaptation points in a "Customising" section.
4. Replace `${CLAUDE_SKILL_DIR}` with `${SKILL_DIR}` (both are supported by the
   exporter, but `${SKILL_DIR}` is preferred in this framework).
5. Add tests for any script under `tests/` with a unique module name.
6. Run `uv run pytest` and `python tools/export_skills.py --dry-run`.

## What stays in the company repo

Skills that depend on a specific infrastructure (clone paths, accounts, host keys,
internal catalogues) are usually better kept in the company repo and only the
generic *pattern* is migrated here. Examples: xDI flow catalogues, Oracle account
maps, on-prem SSH host lists.
