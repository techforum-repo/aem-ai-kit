---
description: Create or update an OSGi Scheduler or Sling Job following AEMaaCS conventions
---

Create or update an OSGi Scheduler or Sling Job following the conventions already used in this repository.

Before generating code, first provide:
1. whether a `Runnable` scheduler or `JobConsumer` is more appropriate and why
2. the expected trigger type or schedule
3. the OSGi services, configuration, and service user needs
4. any AEMaaCS constraints such as leader-only execution on author
5. likely SonarCloud or Cloud Manager risks

Requirements:
- prefer `Runnable` with `@Component` and the `Scheduler` service for simple periodic tasks
- prefer `JobConsumer` with `JobManager` for reliable, distributed, or retryable work
- make the schedule configurable through OSGi config; do not hardcode timing
- never use `Thread.sleep()` inside scheduler or job execution
- never use admin `ResourceResolver`; use a service user if repository access is required
- keep the scheduled unit of work focused and delegate heavy logic to OSGi services
- handle exceptions explicitly so the job or scheduler remains observable and stable
- use SLF4J parameterized logging only
- suggest unit tests for the execution logic, not the scheduling framework itself

Output format:
1. execution design summary
2. code changes
3. validation steps
