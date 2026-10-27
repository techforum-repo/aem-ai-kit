# AEM GitHub Copilot Guidance

> **Part of [aem-ai-kit](../README.md).** These files live under `copilot/` in this repository. Install them with `python3 scripts/install.py <aem-project-root> copilot` instead of copying by hand. Rules (`.github/instructions/`) and skills (`.github/skills/`) are generated from the shared `rules/` and `skills/` folders — edit those, then run `python3 scripts/build.py`.

This repository contains reusable GitHub Copilot guidance for an enterprise Adobe Experience Manager as a Cloud Service (AEMaaCS) project.

It is designed to help teams use GitHub Copilot more effectively in both:
- GitHub Copilot CLI
- GitHub Copilot Chat in VS Code

The repository provides:
- global repository guidance
- module-scoped instructions
- reusable prompt files
- practical request examples
- optional repo-level LSP configuration for Copilot CLI

## Quick start

To start using this guidance in another repository:

1. Copy the `.github` folder from this repo into the root of your target repository.
2. Review the prompt files, scoped instructions, and `copilot-instructions.md` to make sure they match your module structure and conventions.
3. Optionally copy the `docs` folder as well if you want the request cheatsheet and setup notes in the target repo.
4. If you use Copilot CLI with LSP, install the required language servers and verify them with `/lsp`.

## Repository structure

### `.github\copilot-instructions.md`
Top-level repository guidance. This file defines the shared rules Copilot should follow across the project, including module boundaries, AEMaaCS conventions, Cloud Manager safety, OakPAL concerns, and general change guidance.

### `.github\instructions\`
Scoped instruction files that apply automatically based on file path patterns.

These cover areas such as:
- `core`
- `ui.apps`
- `ui.apps.structure`
- `ui.content`
- `ui.config`
- frontend modules
- `all`
- `devops`
- Dispatcher
- hooks

Each instruction file is structured to make usage predictable:
- `Scope`
- `Key rules`
- `Review focus`

Some topics intentionally use companion instruction files for different contexts. For example, XML/content guidance can stay scoped to `ui.content` or `ui.config`, while Java consumption rules for the same topic live in Java-scoped instruction files under `core/src/main/**/*.java`.

### `.github\prompts\`
Reusable prompt files for common AEM development and review tasks.

Examples include:
- creating AEM components
- creating Sling Models
- creating servlets
- creating OSGi services
- creating schedulers
- creating workflow steps
- creating Repoinit and service-user mappings
- writing unit tests
- reviewing code
- investigating bugs
- drafting PR summaries

### `.github\lsp.json`
Optional repository-level Language Server Protocol configuration for Copilot CLI.

The starter config in this repo includes:
- Java via `jdtls`
- TypeScript and JavaScript via `typescript-language-server`

This does not affect runtime behavior. It improves Copilot CLI's code intelligence for tasks such as:
- go-to-definition
- hover information
- diagnostics
- better symbol understanding across Java and frontend modules

### Copilot CLI LSP setup

The repo-level `.github\lsp.json` is the shared intended configuration for this repository.

However, some current Copilot CLI versions may detect repo-level LSP config but still fail to start servers from it. If you see an error such as `Server "java" not found. Available: (none)`, use a user-level Copilot LSP config as the local fallback.

For Windows, Linux, and macOS setup details, see:
- `docs\copilot-cli-lsp-setup.md`

Expected benefits after setup:
- better Java symbol understanding
- better dependency tracing
- better diagnostics and class navigation in Copilot CLI

Best request style with LSP enabled:
- prefer class, interface, and method names over only file paths
- ask for implementors, callers, dependencies, and impact analysis
- use file paths as supporting context, not the only anchor

### `docs\`
Supporting documentation for developers using the guidance set.

Current docs include:
- `docs\copilot-request-cheatsheet.md`
- `docs\copilot-cli-lsp-setup.md`

This cheatsheet explains how to use prompts and provides ready-to-paste requests for common AEM tasks, code reviews, bug investigations, PR work, and git/repository workflows.

For LSP setup details, current limitations, and the user-level workaround, see `docs\copilot-cli-lsp-setup.md`.

## How this works in Copilot CLI

Copilot CLI respects:
- `.github\copilot-instructions.md`
- `.github\instructions\**\*.instructions.md`

That means the CLI can automatically apply repository guidance when you work inside this repo.

Useful CLI notes:
- use `/instructions` to inspect loaded instruction files
- use `/lsp` to check configured language servers
- use `/diff`, `/pr`, and `/review` for git and pull request workflows

If you want repo-level LSP support in CLI, install the configured language servers locally so `.github\lsp.json` can be used.

If your CLI version still does not start repo-level servers reliably, use the user-level fallback described in `docs\copilot-cli-lsp-setup.md`.

## How this works in VS Code

In VS Code:
- prompt files in `.github\prompts\` are easier to discover via slash-command selection in Copilot Chat
- scoped instructions from `.github\instructions\` still apply automatically based on file matching
- the same repo guidance can be reused across editor and terminal workflows

## Recommended usage model

Use the repository like this:

1. Keep broad standards in `.github\copilot-instructions.md`
2. Keep module-specific rules in `.github\instructions\`
3. Keep reusable task templates in `.github\prompts\`
4. Keep developer-facing examples in `docs\`

This separation keeps the guidance easier to maintain and makes it clearer which assets are:
- always-on rules
- path-scoped rules
- reusable prompts
- human-readable examples

### `.vscode/settings.json`
VS Code workspace-level Copilot settings that wire instruction files to specific editor tasks automatically:
- `codeGeneration.instructions` — repository-wide generation defaults spanning core Java, UI modules, content/config packaging, frontend, accessibility, and WCM Core Components
- `testGeneration.instructions` — unit test, integration test, UI/frontend, and accessibility conventions applied on every test generation task
- `codeReview.instructions` — security, performance, packaging, Dispatcher, content/config, and frontend review instructions applied on every inline code review
- `commitMessageGeneration.instructions` — AEM module-scoped commit message style
- `pullRequestDescriptionGeneration.instructions` — PR description format covering modules, risks, and testing notes

These apply automatically in VS Code without any manual prompt selection.

### `AGENTS.md`
Universal agent instructions file for cross-tool compatibility. Provides the same core AEM conventions to tools that support `AGENTS.md` natively (GitHub Copilot Workspace, OpenAI Codex, and others) without requiring tool-specific configuration files.

To reduce drift, keep broad repository rules in `.github/copilot-instructions.md`, keep `AGENTS.md` aligned with those broad rules, and keep path-specific detail in `.github/instructions/`.

## Suggested next steps

If you want to extend this repo further, the most useful next improvements are:
- refine prompts based on real team usage
- expand docs with team-specific examples
- keep `lsp.json` aligned with the languages actually used in the target AEM repo

## Summary

This repository is set up as a reusable enterprise AEMaaCS Copilot guidance package.

It is already suitable for:
- enterprise AEM development guardrails
- Copilot CLI workflows
- VS Code Copilot workflows
- code review and PR support
- onboarding developers to large AEM codebases
