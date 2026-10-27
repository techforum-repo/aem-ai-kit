---
description: Rules for local developer workflow hook scripts — commit, push and local validation behavior
paths:
  - "hooks/**/*"
---
<!-- Generated from rules/hooks.md by scripts/build.py. Edit the source, not this file. -->

# Instructions for `hooks`

## Scope
These scripts affect local developer workflow, commit behavior, and local validation flow.

## Key rules
- Keep behavior predictable and easy to explain.
- Call out any change that affects commit, push, validation, or local setup flow.
- Avoid surprising side effects or destructive behavior in local workflow scripts.

## Review focus
- unexpected workflow changes
- fragile local assumptions
- developer experience regressions
