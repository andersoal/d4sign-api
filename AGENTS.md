# Agent rules for this repo

## Zero-PII policy
- Never commit secrets (`mise.local.toml` with real `tokenAPI`/`cryptKey` stays gitignored, always).
- Never commit a real person's personal email or name baked into example data. D4Sign's own public example accounts (e.g. `teste@gmail.com`) are fine to keep. Scrub anything captured from a live test with real credentials to a generic placeholder before you commit it.
- Before every commit, grep the diff for emails/secrets.

## Git
- Never commit or push without being explicitly asked.
- Never amend or rewrite history unless explicitly asked, and never if already pushed.

## Verifying API claims
- A 401 from an invalid-credentials call proves nothing about whether an endpoint exists. D4Sign verifies credentials before it routes the request. Only the official reference nav, or a live call with *valid* credentials, can verify that an endpoint exists.
- Verify SDK behavior (param order, which services exist on `Client`) by reading `sdk/php/src/D4sign/**`, not by assuming from names.

## Writing English prose
- Always run new or rewritten English text (descriptions, docs, guides, recipes, commit-adjacent prose) through the `asd-ste100` skill before finishing — STE-flavored mode for prose, Strict for tool/error/API text. Don't skip it for "small" edits.

## Editing prose in `openapi/d4sign.yaml`
- When you translate or rewrite `summary`/`description`/parameter text, diff the result: it must touch no structural keys (`operationId`, `in:`, `type:`, parameter or schema names) — only prose text changed.
- Confirm the path count (70) and operation count (72) stay the same after the edit. See `docs/LINTING.md` for the exact `openapi spec query` commands.

## Linting the spec with the `openapi` CLI
- Before committing any change to `openapi/d4sign.yaml`, run `openapi spec validate openapi/d4sign.yaml`, then `openapi spec lint --config openapi/lint.yaml openapi/d4sign.yaml`. Both must report zero problems. See `docs/LINTING.md` for install steps and the reasons behind each disabled rule.
- Never silence a lint finding by inventing a fact about the live API. That includes a length limit, a format, a 4xx/5xx schema, or a rate-limit header D4Sign doesn't document or you haven't confirmed live. Instead, disable the rule in `openapi/lint.yaml` with a one-line reason — see the existing entries for the pattern.
- Prefer `openapi spec query` over manual grep/counting for structural questions about the spec (path counts, operation counts, which operations share a tag, and so on).

## Bruno collection (`collections/bruno/`)
- OpenCollection YAML, not `.bru`. Needs `opencollection.yml` at the root.
- Query params must appear literally in the request's `url` string, or Bruno Desktop shows them unchecked.
- Combined `security: [{schemeA}, {schemeB}]` gets collapsed by Bruno's OpenAPI sync (upstream bug) — keep `tokenAPI` as a collection-root header and `tokenAPI`+`cryptKey` as explicit per-request params, with `autoCheck: false`.

## Astro site (`site/`)
- Always `rm -rf .astro dist` before `npm run build`.
- `openapi/d4sign.yaml` is the single source of truth for `/reference/`.
