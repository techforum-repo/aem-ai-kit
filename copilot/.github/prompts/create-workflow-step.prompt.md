---
description: Create or update a custom AEM workflow process step
---

Create or update a custom AEM workflow process step following the conventions already used in this repository.

Before generating code, first provide:
1. the expected payload type, such as page, asset, or another content path
2. the process arguments this step will accept
3. the OSGi services and service user needs
4. likely workflow stability, SonarCloud, or Cloud Manager risks

Requirements:
- implement `WorkflowProcess` and annotate with `@Component(service = WorkflowProcess.class)` including a `process.label` property for the authoring UI
- keep execution logic focused and delegate reusable work to OSGi services
- access the payload through `workItem.getWorkflowData().getPayload()` and validate the payload type before use
- never use admin `ResourceResolver`; use a service user with appropriate ACLs
- always close `ResourceResolver` with try-with-resources
- do not call `Thread.sleep()`
- handle exceptions explicitly because uncaught exceptions terminate the workflow instance
- read process arguments from `metaData.getMetaDataMap()` so behavior remains configurable
- use SLF4J parameterized logging only
- suggest unit tests for happy path and failure handling

Output format:
1. workflow design summary
2. code changes
3. validation steps
