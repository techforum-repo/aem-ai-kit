---
description: Create or update a Sling Servlet following AEMaaCS and repository conventions
---

Create or update a Sling Servlet following the conventions already used in this repository.

Before generating code, first provide:
1. whether resource type or path registration is appropriate and why
2. the expected selectors, extensions, methods, and response format
3. the OSGi services this servlet will depend on
4. any service user requirements for JCR access
5. key assumptions and likely SonarCloud or Cloud Manager risks

Requirements:
- if selectors, extensions, methods, registration style, or authentication model are unclear, ask one focused clarifying question before implementing
- prefer `@SlingServletResourceTypes` over path-based registration unless path registration is already the established pattern here
- use `SlingSafeMethodsServlet` for read-only use cases and `SlingAllMethodsServlet` only when write methods are required
- keep request handling focused and delegate business logic to OSGi services
- validate and sanitize all request parameters before use
- return appropriate HTTP status codes and response bodies for both success and failure paths
- never use admin `ResourceResolver`; use a service user if JCR access is needed
- do not call `Thread.sleep()`
- use SLF4J logging only, with parameterized messages
- suggest unit tests for happy path, missing input, invalid input, and error handling

Output format:
1. servlet design summary
2. code changes
3. validation steps
