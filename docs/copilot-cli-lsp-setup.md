# Copilot CLI LSP setup

This guide explains how to enable Language Server Protocol support for GitHub Copilot CLI when using this repository.

It covers:
- the shared repo-level configuration in `.github\lsp.json`
- the current Copilot CLI limitation with repo-level LSP config
- the user-level fallback that works reliably on Windows, Linux, and macOS
- Java and TypeScript setup notes

## What this repo already provides

This repository already includes `.github\lsp.json` with:
- Java via `jdtls`
- TypeScript and JavaScript via `typescript-language-server`

That file is the intended shared team configuration.

## Important current limitation

Some current GitHub Copilot CLI versions detect project-level `.github\lsp.json` but still fail to start servers from it. A common symptom is:

```text
✗ Server "java" not found. Available: (none)
```

If that happens, keep the repo-level file as the shared reference, but use a user-level Copilot config as the active workaround.

## When to use each config

### Repo-level `.github\lsp.json`

Use this file to:
- document the intended language servers for the repository
- give teammates a shared baseline
- keep repo expectations visible in version control

### User-level `lsp-config.json`

Use this file when:
- your Copilot CLI version does not reliably start repo-level LSP servers
- your `jdtls` path is machine-specific
- you need OS-specific local paths

## User-level config file locations

### Windows

```text
C:\Users\<your-user>\.copilot\lsp-config.json
```

### Linux

```text
~/.copilot/lsp-config.json
```

### macOS

```text
~/.copilot/lsp-config.json
```

## Recommended user-level config

Use the same server names as the repo-level file so prompts and team guidance stay consistent.

### Windows example

```json
{
  "lspServers": {
    "java": {
      "command": "jdtls",
      "args": [
        "-data",
        "C:\\Users\\<your-user>\\.copilot\\jdtls-workspace"
      ],
      "fileExtensions": {
        ".java": "java"
      }
    },
    "typescript": {
      "command": "typescript-language-server",
      "args": [
        "--stdio"
      ],
      "fileExtensions": {
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript"
      }
    }
  }
}
```

### Linux example

```json
{
  "lspServers": {
    "java": {
      "command": "jdtls",
      "args": [
        "-data",
        "/home/<your-user>/.copilot/jdtls-workspace"
      ],
      "fileExtensions": {
        ".java": "java"
      }
    },
    "typescript": {
      "command": "typescript-language-server",
      "args": [
        "--stdio"
      ],
      "fileExtensions": {
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript"
      }
    }
  }
}
```

### macOS example

```json
{
  "lspServers": {
    "java": {
      "command": "jdtls",
      "args": [
        "-data",
        "/Users/<your-user>/.copilot/jdtls-workspace"
      ],
      "fileExtensions": {
        ".java": "java"
      }
    },
    "typescript": {
      "command": "typescript-language-server",
      "args": [
        "--stdio"
      ],
      "fileExtensions": {
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript"
      }
    }
  }
}
```

## Java setup notes

### Windows

1. Install JDK 21.
2. Verify `java -version`.
3. Install or extract `jdtls` in a stable location.
4. Make sure `jdtls` is available on `Path`, or replace `"jdtls"` in the config with the full absolute path to the launcher.

Example JDK install:

```powershell
winget install EclipseAdoptium.Temurin.21.JDK
```

### Linux

1. Install JDK 21 using your package manager.
2. Verify `java -version`.
3. Install `jdtls` and ensure it is on `PATH`, or use an absolute path in `lsp-config.json`.

### macOS

1. Install JDK 21.
2. Verify `java -version`.
3. Install `jdtls` and ensure it is on `PATH`, or use an absolute path in `lsp-config.json`.

If `jdtls` works in your shell but Copilot CLI still cannot find it, prefer the full absolute path in the `command` field.

## TypeScript setup notes

Install the TypeScript language server globally if it is not already available:

```text
npm install -g typescript-language-server typescript
```

## How to verify

1. Start Copilot CLI from the repository root.
2. Run:

```text
/restart
```

3. Then run:

```text
/lsp
```

4. Then test a server:

```text
/lsp test java
```

or:

```text
/lsp test typescript
```

## Recommended team guidance

- Keep `.github\lsp.json` in the repository as the shared intended config.
- Add this doc to onboarding material so developers know when to fall back to user-level config.
- Do not commit machine-specific absolute paths into `.github\lsp.json`.
- Prefer user-level `lsp-config.json` for local overrides and OS-specific paths.
