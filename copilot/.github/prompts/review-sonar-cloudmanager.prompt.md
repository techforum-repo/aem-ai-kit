---
description: Review implementation for SonarCloud maintainability and Cloud Manager quality concerns
---

Review the selected implementation for SonarCloud and Adobe Cloud Manager quality concerns using the specific rules below.

Only report findings that are actually supported by the code. Do not manufacture issues just to satisfy the checklist.

## SonarCloud rules checklist
Check each of the following and flag any violations:

- [ ] **java:S3776** — Cognitive Complexity exceeds 15. Identify the method and suggest how to decompose it.
- [ ] **java:S2095** — Closeable resource not closed. Flag any stream, resolver, or session not wrapped in try-with-resources.
- [ ] **java:S2259** — Potential null dereference. Flag unguarded access on nullable or optional references.
- [ ] **java:S4973** — String or boxed type compared with `==` instead of `.equals()`.
- [ ] **java:S1206** — `equals()` overridden without overriding `hashCode()` or vice versa.
- [ ] **java:S106** — `System.out` or `System.err` used instead of SLF4J logger.
- [ ] **java:S2068** — Hardcoded credential, token, or password in source.
- [ ] **java:S108** — Empty catch block with no explanatory comment.
- [ ] **java:S1481** — Unused local variable.
- [ ] **java:S1172** — Unused method parameter.
- [ ] **java:S107** — Method has more than 7 parameters.
- [ ] **java:S2696** — Static non-final field written from instance method.
- [ ] **java:S2276** — `Thread.sleep()` used in production code path.
- [ ] **java:S1135** — Unresolved TODO or FIXME comment.
- [ ] **Duplication** — Blocks of 10+ identical or near-identical lines duplicated across the codebase.
- [ ] **Testability** — Logic that cannot be unit tested without excessive mocking or static dependencies.

## Adobe Cloud Manager rules checklist
Check each of the following and flag any violations:

- [ ] **CQBP-72 / AMSCORE-304** — `ResourceResolver` obtained but not closed in all code paths including exception paths.
- [ ] **CQBP-75** — `Thread.sleep()` called inside a Sling Servlet, Sling Job, or OSGi Scheduler.
- [ ] **CQBP-84** — `System.out` or `System.err` used anywhere in production classes.
- [ ] **CQBP-84** — Log statements using string concatenation instead of SLF4J parameterized format.
- [ ] **CQBP-71** — Deprecated AEM, Sling, or JCR API used. Check for `@Deprecated` annotations on called methods.
- [ ] **CQBP-84** — Static mutable field written from a non-static context.
- [ ] **Session handling** — `javax.jcr.Session` obtained but not logged out or closed properly.

## OakPAL content package rules checklist
If reviewing XML in `ui.apps`, `ui.content`, `ui.config`, or `all` modules:

- [ ] OSGi configuration XML must not be placed under `/apps` in `ui.apps`; it belongs in `ui.config`.
- [ ] `ui.apps` must not contain mutable content paths such as `/content` or editable template content under `/conf`.
- [ ] `ui.content` must not contain immutable paths such as `/apps` or `/libs`.
- [ ] No `rep:policy` nodes in packages unless explicitly required and reviewed.
- [ ] No `authorizable` nodes in application or content packages.
- [ ] Package filter roots must not overlap across embedded packages in `all`.
- [ ] Package filters must not cover `/oak:index`, `/home`, or `/libs` without a documented reason.
- [ ] OSGi config file names must match the OSGi PID exactly, including factory PID `~identifier` format.
- [ ] Runmode folder names must match a valid AEM runmode such as `config`, `config.author`, `config.publish`, `config.dev`, `config.stage`, or `config.prod`.

## Output format
1. **Summary** — overall risk level: pipeline blocking, high, medium, low, or no major issues
2. **Findings** grouped by severity
3. For each finding: rule ID, file and location, description, why it matters, smallest safe fix
4. **Validation steps** — how to confirm the issue is fixed
