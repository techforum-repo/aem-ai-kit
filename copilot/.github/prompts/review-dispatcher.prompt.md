---
description: Review Dispatcher configuration for security, caching, domain setup, and Cloud Manager compatibility
---

> Tip: attach `#file:<path>` for the vhost, farm, or filter file to review.

Review the Dispatcher configuration for security, caching, domain setup, and Cloud Manager compatibility. Report each finding as **Blocking** / **Warning** / **Suggestion**.

## Domain setup completeness

- New domain added without vhost, farm, symlinks, and etc/map all updated together — **Blocking**
- Files created directly in `enabled_*` instead of `available_*` with symlinks — **Warning**
- etc/map entry missing for HTTP or HTTPS (port 80 or 443) — **Warning**
- `default.vhost` or `default.farm` modified instead of creating a separate file — **Blocking**
- `/virtualhosts` using `$include` instead of inline hostnames for domain-specific farm — **Warning**

## Security filter rules

- `/filter` does not default deny — **Blocking**
- Sensitive AEM endpoints exposed (`/crx`, `/system`, `/bin/wcmcommand`, `/bin/receive`, `/etc/replication`, `/mnt/overlay`, `/editor.html`) — **Blocking**
- `.infinity.json` or broad `.json` exposure without a specific public use case — **Blocking**
- Missing security headers (`Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) — **Warning**
- `Strict-Transport-Security` absent on an HTTPS-only deployment — **Warning**

## Caching

- Authenticated or personalized responses cached without exclusion rules — **Blocking**
- Analytics-style query parameters causing cache fragmentation (missing `/ignoreUrlParams`) — **Warning**
- Cache invalidation rules misaligned with publish flush behavior — **Warning**

## Rewrite rules

- Global rewrite rule changed without per-domain `RewriteCond %{HTTP_HOST}` guard — **Warning**
- New domain needs a different content root but the global rewrite is unchanged — **Warning**

## Cloud Manager compatibility

- Dispatcher directive not supported by the AEMaaCS Dispatcher SDK — **Blocking**
- Configuration not validated with `dispatcher-sdk-validator` before merge — **Warning**

Output format:
1. overall risk assessment
2. findings grouped by severity
3. validation steps (local SDK validator, test URLs, security header checks)
