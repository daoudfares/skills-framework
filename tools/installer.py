"""One-time setup for skills that need credentials.

Creates a data directory (default ~/.skills-data), an .env from .env.example, a
journal folder, and (when a Claude Code config dir exists) adds a deny rule so
the agent cannot read the .env.

Safe to rerun: existing values are preserved, new keys are appended.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

DATA_DIR = Path.home() / ".skills-data"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(DATA_DIR))
    ap.add_argument("--env-example", default=None, help="path to a .env.example to seed from")
    args = ap.parse_args()

    data_dir = Path(args.data_dir).expanduser().resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "journal").mkdir(exist_ok=True)

    env_path = data_dir / ".env"
    example = Path(args.env_example).resolve() if args.env_example else None
    if example and example.is_file() and not env_path.is_file():
        shutil.copyfile(example, env_path)
        print(f"created {env_path} from {example}")
    elif not env_path.is_file():
        env_path.write_text("# fill in your credentials here\n", encoding="utf-8")
        print(f"created empty {env_path}")

    # Claude Code deny rule, only if a Claude config dir exists
    for cfg in (Path.home() / ".claude", Path(os.environ.get("CLAUDE_CONFIG_DIR", ""))):
        if not cfg or not cfg.is_dir():
            continue
        settings = cfg / "settings.json"
        try:
            data = json.loads(settings.read_text(encoding="utf-8")) if settings.is_file() else {}
        except json.JSONDecodeError:
            data = {}
        perms = data.setdefault("permissions", {}).setdefault("deny", [])
        rule = f"Read({env_path})"
        if rule not in perms:
            perms.append(rule)
            settings.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"added deny rule in {settings}")
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
