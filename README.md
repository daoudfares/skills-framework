# skills-framework

A generic, agent-agnostic framework for **authoring, testing, packaging and sharing
agent skills** (the `SKILL.md` format used by Claude Code, Codex, Cursor, Gemini
CLI, and local-model agents).

It is deliberately **not tied to any company or domain**. The `skills/` folder ships
a couple of generic example skills; everything company-specific belongs in your
own repository that consumes this framework.

## What a "skill" is

A skill is a self-contained folder with a `SKILL.md` (front matter + instructions)
plus optional `references/`, `scripts/` and `tests/`. An agent loads it when a
request matches its `description`. See `framework/skill-template/`.

## Layout

```
framework/        conventions, patterns, skill template
skill-creator/    create and evaluate skills (skill itself)
tools/            export, installer, sql_guard (multi-dialect), tests
skills/           skills shipped with the framework (generic examples)
docs/             architecture, contribution, migration
```

## Agent agnostic

Nothing here assumes Claude Code. `${CLAUDE_SKILL_DIR}` is resolved at export time
by `tools/export_skills.py` into an absolute path, so skills work on any agent that
reads the Agent Skills format. Claude-specific packaging (`.claude-plugin/`) is
optional and lives outside the core.

## Quick start

```sh
# 1. clone
git clone <this-repo>
cd skills-framework

# 2. run tests
uv run pytest

# 3. export skills to your agent's folder
python tools/export_skills.py            # default: ~/.agents/skills
python tools/export_skills.py --dry-run  # preview
```

## Creating a skill

See `framework/skill-template/` and `skill-creator/SKILL.md`.

## License

Apache-2.0 (see `LICENSE`).
