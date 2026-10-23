# Conventions

Generic conventions for skills in this framework. Company-specific decisions
(ADR numbers, layer names, macro names) belong in the consuming repository.

## Skill structure

```
my-skill/
├── SKILL.md              # required: front matter + instructions
├── references/           # optional: large reference docs, read on demand
├── scripts/              # optional: helper scripts
└── tests/                # optional: tests for the scripts
```

## SKILL.md front matter

```yaml
---
name: my-skill
description: When to use this skill. Be specific; this is the trigger.
allowed-tools:          # optional, agent-specific allow-list
  - Bash(python *foo.py *)
---
```

Rules:
- `name` is kebab-case, unique across the repo.
- `description` states the trigger conditions, not a summary. Agents use it to decide
  whether to load the skill.
- Keep `SKILL.md` under ~300 lines; push detail into `references/`.

## Naming

- Skill folders: kebab-case (`dbt-developer`, not `DbtDeveloper`).
- Scripts: snake_case (`sql_guard.py`).
- Tests: `test_<module>.py`, one file per module under test (unique basenames so the
  whole suite collects cleanly).

## Self-containment

A skill must be applicable without another repository present. Where a rule comes
from an external decision record, cite it by number rather than restating reasoning.

## Read-only by default for data skills

Any skill that touches a production data system must be read-only:
- SQL: single SELECT only, enforced by `tools/sql_guard`.
- HTTP: GET only.
- SSH: fixed command templates, no shell injection.
- Credentials never in skill files; one `.env` outside the repo.
