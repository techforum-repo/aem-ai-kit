---
description: Create or update a Sling Model following repository annotation and package conventions
---

Create or update a Sling Model for this AEM component.

Before generating code, first provide:
1. nearby Sling Model patterns that should be followed
2. the likely adaptables, injection style, and consumers of the model
3. any assumptions about authored properties, inheritance, or fallback behavior
4. likely SonarCloud or Cloud Manager concerns if any

Requirements:
- follow the existing package structure, annotations, and injection style used in nearby models
- adapt from the appropriate source used by related components
- expose only the data needed by HTL, JSON consumers, or frontend integrations
- keep business logic minimal and focused
- avoid repository writes or expensive work inside the model
- handle nulls, defaults, and fallback behavior explicitly
- suggest tests if logic is non-trivial

Output format:
1. model design summary
2. code changes
3. validation steps
