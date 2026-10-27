---
description: Create or update a Sling Context-Aware Configuration interface and content nodes
---

Create or update a Sling Context-Aware Configuration for this AEM project.

Before generating code, first provide:
1. whether this is a new config or an update to an existing one
2. the Java `@interface` location in `core` and the config node path under `/conf/<project>/sling:configs/`
3. the property list with name, type, default value, and label
4. which Sling Models or OSGi services will consume this config
5. whether config values differ per site, environment, or content tree

Requirements:
- define the `@interface` annotated with `@Configuration` (`org.apache.sling.caconfig.annotation.Configuration`) in `core`
- set `name` and `label` on `@Configuration` for editor clarity
- give every property a default so resolution is safe when no content config exists
- use `@Property` labels and descriptions for author-facing fields
- place config content nodes under `/conf/<project>/sling:configs/` in `ui.content`, not `ui.apps`
- ensure `sling:configRef` is set on the content root to wire up inheritance; do not assume it already exists
- resolve config per request or per adaptation in Sling Models — never cache in OSGi service fields
- use `configurationBuilder.as(MyConfig.class)` rather than reading raw `ValueMap` structures
- document whether the config is site-specific (per `/conf/<site>`) or global (`/conf/global`)
- if updating an existing config, flag any property name changes as breaking and suggest defaults for new properties

Output format:
1. design summary (interface, content path, consumers)
2. `@interface` code
3. `ui.content` XML for default config node
4. Sling Model consumption example
5. validation steps
