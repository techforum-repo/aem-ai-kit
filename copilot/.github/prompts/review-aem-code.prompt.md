---
description: Review selected files for AEM best practices, SonarCloud, and Cloud Manager concerns
---

> Tip: attach `#file:<path>` or select files in the editor before invoking to give Copilot the right context.

Review the selected files for:
- AEM best practices
- SonarCloud-style code quality concerns
- likely Adobe Cloud Manager quality concerns
- null safety
- duplication
- excessive complexity
- missing tests
- frontend/backend integration risks
- authoring impact if applicable

Requirements:
- focus on meaningful findings, not style-only comments
- for each issue, describe the problem clearly, explain why it matters, and suggest the smallest safe fix
- cite the relevant file and code location when possible
- if no major issue is found, say so clearly and then list minor improvements if any

Output format:
1. overall assessment
2. findings by severity
3. recommended validation steps
