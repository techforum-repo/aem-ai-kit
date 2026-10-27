#!/usr/bin/env python3
"""Copy the Claude Code and/or GitHub Copilot setup into an AEM project.

Usage:
  python3 scripts/install.py <aem-project-root> [claude|copilot|all] [--force] [--dry-run]

Existing files in the project are never overwritten unless --force is given, so
project-specific customisations (package names, hosts, Maven profiles) survive a re-install.
Standard library only; works on Windows, macOS and Linux.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYOUTS = {"claude": ROOT / "claude", "copilot": ROOT / "copilot"}
SKIP_PARTS = {"__pycache__"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", type=Path, help="root folder of the AEM project")
    parser.add_argument("tool", nargs="?", default="all", choices=["claude", "copilot", "all"])
    parser.add_argument("--force", action="store_true", help="overwrite files that already exist")
    parser.add_argument("--dry-run", action="store_true", help="show what would be copied")
    args = parser.parse_args()

    project = args.project.resolve()
    if not (project / "pom.xml").is_file():
        print(f"{project} has no pom.xml; pass the root of an AEM Maven project.", file=sys.stderr)
        return 2

    tools = ["claude", "copilot"] if args.tool == "all" else [args.tool]
    copied, skipped = 0, []
    for tool in tools:
        source_root = LAYOUTS[tool]
        for source in sorted(source_root.rglob("*")):
            if not source.is_file() or SKIP_PARTS & set(source.parts):
                continue
            relative = source.relative_to(source_root)
            target = project / relative
            if target.exists() and not args.force:
                skipped.append(str(relative))
                continue
            print(f"{'would copy' if args.dry_run else 'copy'}  {relative}")
            if not args.dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            copied += 1

    if skipped:
        print(f"\nKept {len(skipped)} existing file(s); rerun with --force to overwrite:")
        for relative in skipped:
            print(f"  {relative}")
    print(f"\n{copied} file(s) {'would be ' if args.dry_run else ''}copied into {project}.")
    if "claude" in tools:
        print("Add .claude/settings.local.json to the project's .gitignore for personal overrides.")
    print("Next: replace com.example in the aem-project-conventions skill and review CLAUDE.md / copilot-instructions.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
