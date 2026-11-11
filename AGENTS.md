# Agent rules for this repo

Rules learned the hard way while building this docs site. Read before touching the repo.

## Git

- **Never commit without being explicitly asked.** Work can sit uncommitted across sessions.
- **Never amend or rewrite history** (`commit --amend`, `rebase`, `reset --hard`) unless the user explicitly asks for it, and only after confirming nothing is pushed (`git rev-list origin/master..HEAD`).
- Before committing, grep the diff for secrets and for the user's/any real person's personal email or PII baked into example data (OpenAPI examples, Bruno request bodies). D4Sign's own public example accounts (e.g. `andydasilva52@gmail.com`, `teste@gmail.com` from their docs) are fine to keep — they're already public. A real person's personal email captured incidentally from a live test call is not; scrub it to a generic placeholder.
- `mise.local.toml` holds real `tokenAPI`/`cryptKey` values and must stay gitignored. Never print or echo its contents.

## Verifying claims about the API

- **An HTTP status from a call made with invalid credentials proves nothing about whether an endpoint exists.** D4Sign validates `tokenAPI`/`cryptKey` *before* route matching — even a nonsense path returns the same `401 Chave de API inválida` as a real one. Only two things confirm an endpoint exists: it appears in the official reference nav, or a live call with *valid* credentials returns something other than that auth-rejection body (200/400/404).
- Verify SDK method signatures, param order, and which services are actually wired into `Client`'s constructor by reading `sdk/php/src/D4sign/**` directly — don't assume from naming. (Found real bugs this way: `sendToSigner`'s `$workflow`/`$skip_email` order, `makedocumentbytemplate`'s misleadingly-named first param, `Batches` service never instantiated on `Client`.)
- If an earlier claim in the conversation turns out wrong, correct it explicitly in the docs rather than leaving it.

## Bruno collection (`collections/bruno/`)

- Must be OpenCollection YAML, not `.bru` — the CLI only auto-detects this format if `opencollection.yml` exists at the collection root (checked before `bruno.json`).
- Environment files must be `.yml`, not `.bru`, to match the detected format.
- Multipart-form bodies must be a YAML list of `{name, value, type}` entries, not a text blob.
- Embed the full query string literally into every request's `url` field — Bruno Desktop derives a param's enabled checkbox from presence in the URL text, not just the `params:` list.
- Bruno's OpenAPI sync collapses an AND-combined `security: [{schemeA: [], schemeB: []}]` into a single scheme, dropping the others (upstream bug, filed: https://github.com/usebruno/bruno/issues/9817). Workaround used here: `tokenAPI` lives as an inheritable header on the collection root in `opencollection.yml`; `tokenAPI`+`cryptKey` stay as explicit per-request query params; `autoCheck: false` is set on the OpenAPI sync entry to stop it from re-collapsing this.
- The scaffold script (`bruno-collection-generator` skill) overwrites `collections/bruno/README.md` with a generic template every run — restore it by hand afterward (see `docs/REGENERATING.md`).

## Astro site (`site/`)

- Always `rm -rf .astro dist` before `npm run build` — stale cache has caused real bugs (a locale-config change silently not taking effect).
- `openapi/d4sign.yaml` is the single source of truth; the `/reference/` section is generated from it by `starlight-openapi`, not hand-written.

## Editing `openapi/d4sign.yaml` with scripts

- Use `ruamel.yaml` for round-trip edits that must preserve formatting.
- On Windows, open files with explicit `encoding="utf-8"` (and `io.StringIO` for in-memory round-trips) — bare `open()` defaults to cp1252 and will corrupt the file silently.
- Take a backup before any risky scripted edit; verify with a before/after path-set diff that only the intended paths changed.
- Delete one-off migration scripts after use; keep only the reusable generation scripts under `scripts/`.
