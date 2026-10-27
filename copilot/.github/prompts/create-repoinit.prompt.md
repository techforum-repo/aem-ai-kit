---
description: Create a Repoinit script to provision a service user and ACLs for AEMaaCS
---

Create a Repoinit script to provision the service user and minimum required ACLs for this use case.

Before generating code, first provide:
1. the paths the service needs to read or write
2. the minimum JCR privileges required
3. the subservice name that will be used in Java code
4. any author-versus-publish differences in access requirements
5. any risks related to package placement or over-broad permissions

Requirements:
- use `create service user` for the principal; do not create a regular system user
- grant only the minimum permissions required for the use case
- prefer path-specific ACLs over broad `/content` or `/` grants
- use explicit `set ACL for <service-user>` statements with only the required privileges
- place the Repoinit and service user mapping files in `ui.config` using the repository's existing OSGi config naming and file format conventions
- ensure Java code uses `resourceResolverFactory.getServiceResourceResolver(Map.of(ResourceResolverFactory.SUBSERVICE, "<subservice-name>"))`
- avoid embedding access control content directly in content packages

Output format:
1. access design summary
2. Repoinit and mapping changes
3. validation steps
