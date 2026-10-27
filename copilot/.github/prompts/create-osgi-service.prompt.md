---
description: Create or update an OSGi service following repository conventions
---

Create or update an OSGi service following repository conventions.

Before generating code, first provide:
1. the likely interface and implementation location
2. the expected consumers, such as Sling Models, servlets, schedulers, or workflow steps
3. dependencies, collaborators, and any configuration requirements
4. key assumptions, risks, and test considerations

Requirements:
- follow existing package, annotation, and service patterns already used in this repository
- keep responsibilities focused and avoid unnecessary abstractions
- make configuration explicit when behavior should vary by environment or site
- avoid repository access inside the service unless it is clearly needed; if needed, call out service user requirements
- keep thread-safety and null-handling explicit
- explain how the service will be used by other AEM layers
- suggest tests for core behavior and failure paths

Output format:
1. design summary
2. code changes
3. validation steps
