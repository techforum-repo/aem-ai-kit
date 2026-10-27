---
description: Trace a symbol definition and usage via LSP-first navigation
---

Trace this symbol using LSP-first navigation.

Requirements:
- use LSP first for definition, references, implementations, and (if requested) rename planning
- when LSP is available, do not start with plain text search
- provide exact file and line locations for each result
- include a short call chain summary for how the symbol is consumed
- if LSP is unavailable, unsupported for the language, or returns no results, fall back to text search and state why
- do not claim references that were not returned by LSP or fallback search

Output format:
1. definition
2. references
3. implementation chain
4. fallback notes (only if fallback was used)
