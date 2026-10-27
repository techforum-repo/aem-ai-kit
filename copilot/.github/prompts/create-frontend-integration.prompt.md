---
description: Create or update frontend code with correct AEM integration
---

Create or update frontend code that integrates correctly with this AEM repository.

Before generating code, first provide:
1. which implementation pattern should be followed (`ui.frontend`, `ui.frontend.react`, `ui.frontend.spa`, or `ui.apps` clientlib/component-owned frontend code) and why
2. the AEM integration points involved, such as component markup, `ui.apps` clientlibs, model JSON, or authored content
3. any assumptions about backend data, Sling Models, or servlet endpoints
4. likely risks across authoring, rendering, build, or deployment
5. a module decision checklist covering ownership, build/pipeline impact, runtime integration point, and authoring impact

Requirements:
- if module choice or integration contract is unclear, ask one focused clarifying question before implementing
- follow the conventions of the specific frontend module or `ui.apps` clientlib area being edited
- preserve existing integration with AEM markup, authored content, and clientlibs
- keep contracts between frontend code and AEM components explicit
- avoid unnecessary dependencies, broad refactors, or framework-level changes
- call out any required `ui.apps`, `ui.content`, or `core` changes if the frontend depends on new markup, clientlib wiring, data, or configuration
- suggest validation steps across both frontend behavior and AEM rendering

Output format:
1. integration plan
2. code changes
3. validation steps
