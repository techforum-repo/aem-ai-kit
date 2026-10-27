---
description: Draft a pull request summary including risks, modules changed, and testing notes
---

Draft a pull request summary for these changes.

> Tip: attach `#changes` in Copilot Chat to use your current git diff as context automatically.

Requirements:
- base the summary on the actual diff or changed files; do not invent implementation details
- if change context is missing, ask for the diff or changed files before drafting the summary
- identify the business or technical purpose of the change set
- group changes by module or functional area
- call out testing performed, missing validation, or recommended checks
- mention risks, rollback considerations, and any AEM, SonarCloud, or Cloud Manager notes
- if the change is documentation or tooling only, say so clearly
- separate confirmed details (from diff) from assumptions when details are incomplete

Output format:
1. summary paragraph
2. key changes
3. testing
4. risks and rollout notes
