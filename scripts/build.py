#!/usr/bin/env python3
"""Generate the Claude Code and GitHub Copilot layouts from the shared sources.

  rules/<name>.md  ->  claude/.claude/rules/<name>.md                    (paths:)
                   ->  copilot/.github/instructions/<name>.instructions.md (applyTo:)
  skills/<name>/   ->  claude/.claude/skills/<name>/  and  copilot/.github/skills/<name>/
  copilot/.github/copilot-instructions.md  ->  copilot/AGENTS.md  (for Codex and other AGENTS.md readers)

Run with --check to verify the generated files are up to date without writing (used in CI).
Standard library only.
"""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / "rules"
SKILLS_DIR = ROOT / "skills"
CLAUDE_RULES = Path("claude/.claude/rules")
COPILOT_RULES = Path("copilot/.github/instructions")
SKILL_TARGETS = [Path("claude/.claude/skills"), Path("copilot/.github/skills")]
COPILOT_INSTRUCTIONS = Path("copilot/.github/copilot-instructions.md")
AGENTS_FILE = Path("copilot/AGENTS.md")

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
RULE_REF = re.compile(r"\{\{rule:([a-z0-9-]+)\}\}")


def parse_rule(path: Path) -> tuple[str, list[str], str]:
    """Return (description, paths, body) for a rule source file."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"{path.name}: missing frontmatter")
    description, paths = "", []
    for line in match.group(1).splitlines():
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip()
        elif line.lstrip().startswith("- "):
            paths.append(line.strip()[2:].strip().strip("\"'"))
    if not description or not paths:
        raise ValueError(f"{path.name}: frontmatter needs description and paths")
    return description, paths, text[match.end():]


def expand_braces(pattern: str) -> list[str]:
    """Expand the first {a,b} group recursively, so applyTo can be comma-separated safely."""
    match = re.search(r"\{([^{}]*)\}", pattern)
    if not match:
        return [pattern]
    expanded = []
    for option in match.group(1).split(","):
        expanded.extend(expand_braces(pattern[: match.start()] + option + pattern[match.end():]))
    return expanded


def generated_note(name: str) -> str:
    return f"<!-- Generated from rules/{name}.md by scripts/build.py. Edit the source, not this file. -->\n"


def write_rules(out_root: Path, names: list[str]) -> None:
    rule_names = set(names)
    for name in names:
        description, paths, body = parse_rule(RULES_DIR / f"{name}.md")
        for ref in RULE_REF.findall(body):
            if ref not in rule_names:
                raise ValueError(f"{name}.md references unknown rule '{ref}'")

        claude_body = RULE_REF.sub(lambda m: f"`{m.group(1)}.md`", body)
        claude_paths = "".join(f'  - "{p}"\n' for p in paths)
        claude_file = out_root / CLAUDE_RULES / f"{name}.md"
        claude_file.write_text(
            f"---\ndescription: {description}\npaths:\n{claude_paths}---\n{generated_note(name)}{claude_body}",
            encoding="utf-8",
        )

        copilot_body = RULE_REF.sub(lambda m: f"`{m.group(1)}.instructions.md`", body)
        apply_to = ",".join(p for pattern in paths for p in expand_braces(pattern))
        copilot_file = out_root / COPILOT_RULES / f"{name}.instructions.md"
        copilot_file.write_text(
            f'---\ndescription: {description}\napplyTo: "{apply_to}"\n---\n{generated_note(name)}{copilot_body}',
            encoding="utf-8",
        )


def write_agents_file(out_root: Path) -> None:
    """AGENTS.md carries the same repository-wide rules as copilot-instructions.md under a neutral title."""
    text = (ROOT / COPILOT_INSTRUCTIONS).read_text(encoding="utf-8")
    title, _, body = text.partition("\n")
    if not title.startswith("# "):
        raise ValueError(f"{COPILOT_INSTRUCTIONS} must start with a '# ' title")
    note = f"<!-- Generated from {COPILOT_INSTRUCTIONS.relative_to('copilot')} by scripts/build.py. Edit the source, not this file. -->\n"
    (out_root / AGENTS_FILE).parent.mkdir(parents=True, exist_ok=True)
    (out_root / AGENTS_FILE).write_text(f"# Agent Instructions\n{note}{body}", encoding="utf-8")


def build(out_root: Path) -> None:
    for directory in [CLAUDE_RULES, COPILOT_RULES, *SKILL_TARGETS]:
        target = out_root / directory
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
    write_rules(out_root, sorted(p.stem for p in RULES_DIR.glob("*.md")))
    for skill in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        for target in SKILL_TARGETS:
            shutil.copytree(skill, out_root / target / skill.name)
    write_agents_file(out_root)


def differences(left: Path, right: Path, prefix: Path = Path()) -> list[str]:
    """List paths that differ between two directory trees."""
    comparison = filecmp.dircmp(left, right)
    changed = [str(prefix / n) for n in comparison.left_only + comparison.right_only + comparison.diff_files]
    changed += [str(prefix / n) for n in comparison.common_files if not filecmp.cmp(left / n, right / n, shallow=False)
                and n not in comparison.diff_files]
    for sub in comparison.common_dirs:
        changed += differences(left / sub, right / sub, prefix / sub)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if generated files are out of date")
    args = parser.parse_args()

    if not args.check:
        build(ROOT)
        print("Generated claude/ and copilot/ rules and skills.")
        return 0

    with tempfile.TemporaryDirectory() as scratch:
        build(Path(scratch))
        stale = []
        for directory in [CLAUDE_RULES, COPILOT_RULES, *SKILL_TARGETS]:
            if not (ROOT / directory).exists():
                stale.append(str(directory))
                continue
            stale += [str(directory / d) for d in differences(Path(scratch) / directory, ROOT / directory)]
        current = ROOT / AGENTS_FILE
        if not current.exists() or current.read_bytes() != (Path(scratch) / AGENTS_FILE).read_bytes():
            stale.append(str(AGENTS_FILE))
    if stale:
        print("Generated files are out of date. Run: python3 scripts/build.py")
        for path in stale:
            print(f"  {path}")
        return 1
    print("Generated files are up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
