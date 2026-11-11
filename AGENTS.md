# Agent rules for this repo

## Zero-PII policy
- Never commit secrets (`mise.local.toml` with real `tokenAPI`/`cryptKey` stays gitignored, always).
- Never commit a real person's personal email/name baked into example data. D4Sign's own public example accounts (e.g. `teste@gmail.com`) are fine to keep; anything captured from a live test with real credentials is not — scrub it to a generic placeholder before committing.
- Before every commit, grep the diff for emails/secrets.

## Git
- Never commit or push without being explicitly asked.
- Never amend or rewrite history unless explicitly asked, and never if already pushed.

## Verifying API claims
- A 401 from an invalid-credentials call proves nothing about whether an endpoint exists — D4Sign checks credentials before routing. Only the official reference nav or a live call with *valid* credentials confirms existence.
- Verify SDK behavior (param order, which services exist on `Client`) by reading `sdk/php/src/D4sign/**`, not by assuming from names.

## Bruno collection (`collections/bruno/`)
- OpenCollection YAML, not `.bru`. Needs `opencollection.yml` at the root.
- Query params must appear literally in the request's `url` string, or Bruno Desktop shows them unchecked.
- Combined `security: [{schemeA}, {schemeB}]` gets collapsed by Bruno's OpenAPI sync (upstream bug) — keep `tokenAPI` as a collection-root header and `tokenAPI`+`cryptKey` as explicit per-request params, with `autoCheck: false`.

## Astro site (`site/`)
- Always `rm -rf .astro dist` before `npm run build`.
- `openapi/d4sign.yaml` is the single source of truth for `/reference/`.
