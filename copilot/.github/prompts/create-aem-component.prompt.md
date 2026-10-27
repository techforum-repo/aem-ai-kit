---
description: Create or update an AEM component following repository conventions
---

Create or update an AEM component following the conventions already used in this repository.

Before generating code, first provide:
1. the modules and files likely to change across `core`, `ui.apps`, `ui.content`, `ui.config`, and frontend modules if relevant
2. the expected `sling:resourceType`, component mapping, or inheritance pattern
3. any authoring, template, policy, or content impacts
4. key assumptions
5. likely risks and validation points
6. an implementation decision matrix that states whether HTL override, Sling Model/service logic, frontend JS/CSS, and `ui.content` policy/template updates are needed (and why)
7. the authoring mode strategy (default behavior, alternate modes, and where authors switch modes)

Requirements:
- if the request is ambiguous, ask one focused clarifying question before implementing (for example: visual variant only vs new interactive behavior)
- reuse nearby component, dialog, Sling Model, clientlib, and template patterns instead of inventing new structure
- use Sling Model or service backing if logic is required
- keep business logic out of HTL
- preserve authoring experience, style system behavior, and existing naming conventions
- prefer Style System classes and policy-driven variants for author-toggle behavior before adding new HTL/Java/Sling Model logic
- explicitly choose and justify the implementation target (`ui.apps`, `ui.frontend.react`, or `ui.frontend.spa`)
- for `ui.frontend.react` or `ui.frontend.spa`, follow existing module patterns and include expected AEM model JSON/props contract, component mapping path, clientlib loading/inclusion point, and authored-content impact
- do not mix SPA Editor patterns into `ui.frontend.react`/`ui.frontend` unless already established there, and do not introduce React/SPA structure into `ui.apps` HTL components unless existing patterns require it
- call out any required `ui.content` or `ui.config` updates when the component depends on templates, policies, CA config, or OSGi config
- avoid unnecessary refactors or cross-module churn
- suggest tests or validation steps if backend or frontend behavior is introduced or changed

Output format:
1. implementation plan
2. code changes
3. validation steps
