---
description: Rules for the devops module — build pipelines, quality gates, deployment and environment configuration
applyTo: "devops/**/*"
---
<!-- Generated from rules/devops.md by scripts/build.py. Edit the source, not this file. -->

# Instructions for `devops`

## Scope
Changes in `devops` can affect build pipelines, deployment behavior, and environment assumptions across all environments.

## Key rules
- Treat pipeline and quality gate changes as deployment-critical.
- Call out required environment variables, secrets, or external configuration changes explicitly.
- Validate dispatcher-related changes with the Dispatcher SDK before merge when applicable.
- Avoid environment-specific assumptions that are not documented in the deployment flow.

## Review focus
- pipeline impact
- rollback or release risk
- undocumented environment dependencies
- deployment safety across environments
