---
description: Create or update a Content Fragment model following project conventions
---

Create or update a Content Fragment model for this AEM project.

Before generating any XML, first provide:
1. the model path under `/conf/<project>/settings/dam/cfm/models/` and which module owns it (`ui.content`)
2. the field list with name, type, label, and whether it is required
3. any backward-compatibility concerns if updating an existing model
4. which consuming code (Java, GraphQL persisted queries, SPA components) will be affected

Requirements:
- place the model definition XML in `ui.content`, not `ui.apps` — CF models are mutable content
- every field must have a stable `name` — changing a field `name` silently breaks all existing fragments
- every field must have a non-empty `fieldLabel` for authoring clarity
- use `required` sparingly — required fields block fragment creation in automated workflows
- account for fragment variations in any consuming code
- if a GraphQL persisted query exists for this model, flag the query path and list which fields it reads
- if Java code adapts resources to `ContentFragment`, verify null-safety and element-name alignment
- flag any field renames or removals as breaking changes and suggest a migration path
- suggest a test plan: new fragments, existing fragment editing, GraphQL query execution, Java access

Output format:
1. model design summary (path, fields, consumers)
2. XML definition
3. backward-compatibility notes
4. validation steps
