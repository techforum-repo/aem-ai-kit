---
description: Create or update unit tests for a Sling Model, OSGi service, or utility class
---

Create or update unit tests for the selected class following the conventions already used in this repository's test suite.

Before generating tests, first provide:
1. which nearby test patterns and test framework setup should be followed
2. the behaviors, edge cases, and error paths that should be covered
3. any assumptions about mocks, `AemContext`, model registration, or OSGi setup
4. any SonarCloud or coverage concerns if relevant

Requirements:
- follow the existing test framework setup, such as JUnit 5, Mockito, and `AemContext` where applicable
- use `AemContext` for Sling Model tests and component-backed logic
- use `@ExtendWith(MockitoExtension.class)` for service or utility tests when no AEM context is needed
- cover primary behavior, null inputs, and meaningful edge cases
- keep each test focused on one behavior
- prefer clear, behavior-based test names
- avoid brittle interaction-only tests or over-mocking when simple real objects are sufficient

Output format:
1. test plan
2. test code
3. validation notes
