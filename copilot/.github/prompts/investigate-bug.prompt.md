---
description: Investigate a bug across AEM modules with root cause and fix suggestions
---

> Tip: attach `#file:<path>` for the suspected file, or paste a log snippet for context.

Help investigate this bug in the context of this AEM repository.

Approach:
1. summarize the reported issue and expected behavior
2. identify the impacted modules and files
3. rank the most likely root causes
4. suggest the smallest safe investigation steps
5. suggest likely fixes
6. call out any authoring, frontend, configuration, content, or pipeline risks

Requirements:
- prefer repository-specific reasoning over generic advice
- separate evidence-backed findings from hypotheses
- favor the smallest safe fix over broad refactors unless the root cause requires more
- include validation steps to confirm the fix

Output format:
1. likely issue summary
2. suspected root causes
3. investigation steps
4. likely fixes
5. validation plan
