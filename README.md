# AEM AI Kit

Reusable AI coding-assistant setup for an enterprise Adobe Experience Manager as a Cloud Service (AEMaaCS) project, for both **Claude Code** and **GitHub Copilot**. Works on Windows, macOS and Linux.

This repository replaces the former `aem-claude-code` and `aem-github-copilot` repositories. The module rules are now maintained once and generated for both tools, so the two setups can no longer drift apart.

## Install into an AEM project

```bash
python3 scripts/install.py <aem-project-root>            # Claude Code and Copilot
python3 scripts/install.py <aem-project-root> claude     # Claude Code only
python3 scripts/install.py <aem-project-root> copilot    # Copilot only
```

Add `--dry-run` to preview. Files that already exist in the project are kept unless you pass `--force`, so your project-specific edits survive a re-install.

Then customise for your project:

1. The `aem-project-conventions` skill: replace `com.example` with your package names and update the OSGi config path. This has the biggest effect on code generation quality.
2. `CLAUDE.md` and `.github/copilot-instructions.md` (in this repository, `AGENTS.md` is generated from it; in your project, edit both or re-run the installer): module names, Maven commands, Java version, AEM host and ports.
3. `.claude/settings.json`: `AEM_HOST`, ports, and any extra Maven profiles to allow.
4. `.mcp.json`: the GitHub entry uses GitHub's remote MCP server and reads `GITHUB_TOKEN` from the environment. Swap it for Bitbucket if needed.

Prerequisites: Python 3 (Claude Code hooks), and optionally `jdtls` and `typescript-language-server` for LSP support.

## Repository layout

| Path | What it is |
|---|---|
| `rules/` | **Source of truth** for module rules. One file per rule, with `description` and `paths` frontmatter. |
| `skills/` | **Source of truth** for the AEM review skills (`aem-security`, `aem-sonar`, `aem-oak-index`, …). |
| `claude/` | Claude Code layout: `CLAUDE.md`, `.mcp.json`, `.claude/` (agents, commands, hooks, settings, plus generated rules and skills). |
| `copilot/` | Copilot layout: `AGENTS.md`, `.github/` (copilot-instructions, prompts, LSP config, plus generated instructions and skills), `.vscode/settings.json`. |
| `scripts/build.py` | Generates `claude/.claude/rules`, `copilot/.github/instructions` and both skill folders from `rules/` and `skills/`. |
| `scripts/install.py` | Copies a layout into an AEM project. |
| `tests/` | Tests for the Claude Code safety hooks. Not installed into projects. |
| `docs/` | Detailed guides: [Claude Code](docs/claude-code.md), [GitHub Copilot](docs/github-copilot.md), setup notes and request cheatsheets. |

## Editing rules and skills

Edit files in `rules/` or `skills/`, never the generated copies (each generated rule carries a header saying so), then regenerate:

```bash
python3 scripts/build.py
```

CI runs `python3 scripts/build.py --check` and fails if the generated files are out of date. `copilot/AGENTS.md` is generated the same way, from `copilot/.github/copilot-instructions.md`.

The safety hooks in `claude/.claude/hooks/` have tests: `python3 -m unittest discover tests`. Add a case there whenever you change what a hook blocks.

A rule's `paths` list becomes `paths:` for Claude Code and a comma-separated `applyTo:` for Copilot. To reference another rule from a rule body, write `{{rule:core-java-security}}`; the build turns it into the right file name for each tool.

Tool-specific pieces stay in their own layout: Claude Code hooks, agents, commands and settings live in `claude/`; Copilot prompt files, LSP config and VS Code settings live in `copilot/`.

## License

[MIT](LICENSE)
