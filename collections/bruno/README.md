# D4Sign API — Bruno Collection

72 requests covering the full D4Sign REST API, generated from [`openapi/d4sign.yaml`](../../openapi/d4sign.yaml) via `scripts/openapi_to_bruno_endpoints.py` + the Bruno OpenCollection scaffolder + `scripts/fix_bruno_multipart_bodies.py`. Regenerate it after the spec changes instead of hand-editing requests — see [`../../docs/REGENERATING.md`](../../docs/REGENERATING.md).

A handful of these (webhooks v2.0, document view-URL generation, Word template upload) aren't in D4Sign's own OpenAPI export — they were found missing by comparing it against the live reference nav at [docapi.d4sign.com.br/v2.0/reference](https://docapi.d4sign.com.br/v2.0/reference) and added by hand. See `docs/COVERAGE.md` for the full audit.

[<img src="https://fetch.usebruno.com/button.svg" alt="Fetch in Bruno" style="width: 130px; height: 30px;" width="128" height="32">](https://fetch.usebruno.com?url=https%3A%2F%2Fgithub.com%2Fandersoal%2Fd4sign-api.git "target=_blank rel=noopener noreferrer")

## Usage

```bash
git clone https://github.com/andersoal/d4sign-api.git
# Open collections/bruno/ as a collection in Bruno, or run it via the Bruno CLI (`bru`)
```

With the Bruno CLI (`bru`), run from inside `collections/bruno/`:

```bash
bru run requests -r --env Sandbox --env-var tokenAPI=$tokenAPI --env-var cryptKey=$cryptKey
```

1. Pick the **Production** or **Sandbox** environment (top-right in Bruno, or `--env` on the CLI).
2. Set the credentials. In the GUI: environment → secrets `tokenAPI`/`cryptKey`. On the CLI: pass `--env-var tokenAPI=... --env-var cryptKey=...`, or export them first — see [mise.toml](../../mise.toml) at the repo root, which wires up `tokenAPI`/`cryptKey`/`baseUrl` as shell env vars for exactly this. Never commit real values — the committed environment files only declare the variable names.
3. Run any request. Every request sends `tokenAPI` as a query param + header, and `cryptKey` as a query param — matching how D4Sign's API actually expects them (see [`securitySchemes`](../../openapi/d4sign.yaml) in the spec).

## Auth: why it's not a Bruno `auth:` block

D4Sign requires **both** `tokenAPI` and `cryptKey` together (OAS models this as an AND-combined `security` requirement). Bruno's `auth: apikey` mode only holds one key, so its OpenAPI-sync feature collapses the pair into one and silently drops the other if you re-sync from the UI (filed upstream: [usebruno/bruno#9817](https://github.com/usebruno/bruno/issues/9817)). Instead:

- `tokenAPI` (header) is inherited from `opencollection.yml`'s collection-root `request.headers` — every request gets it for free.
- `tokenAPI` and `cryptKey` (query params) are explicit on every request — Bruno has no mechanism to inherit query params, only headers/auth/vars.
- The OpenAPI sync in `opencollection.yml` has `autoCheck: false` on purpose — re-syncing from the Bruno UI re-triggers the collapse described above. Regenerate from the spec with the scripts instead (`../../docs/REGENERATING.md`).

## Query params showing unchecked in Bruno Desktop

Bruno Desktop's checkbox state for a query param is driven by whether it's present in the **URL text itself**, not just the structured `params:` list — so every generated request's `url` also carries the literal query string (`?tokenAPI={{tokenAPI}}&cryptKey={{cryptKey}}...`) in addition to the `params:` entries. If you ever see params load as unchecked, that mismatch is almost certainly why; the generator keeps both in sync so it shouldn't recur after a regeneration.

## Documenting what you test

`requests/safes/001-list-all-safes.yml` carries a real test asserting the response shape — on success it's an array, on failure it has a `message` field (D4Sign's actual error envelope, confirmed live; see [`guides/rate-limits-and-errors.md`](../../site/src/content/docs/guides/rate-limits-and-errors.md)). The point: when you run a request against the real API, even a failing one, fold what actually came back into the docs instead of letting it disappear into a terminal scrollback. Add more via the `TESTS` dict in `scripts/openapi_to_bruno_endpoints.py` (hand-editing a generated request file gets overwritten on the next regen).

**Caution**: don't use a live `401`-vs-`404` response to decide whether an endpoint exists — D4Sign validates `tokenAPI`/`cryptKey` before route matching, so an invalid credential pair returns the same `401` for a path that doesn't exist at all (confirmed by testing a deliberately nonsense path). The only reliable signal for "does this exist" is the official reference nav itself, or a `200`/`400`/`404` with *valid* credentials.

## Structure

- `requests/<resource>/NNN-name.yml` — one OpenCollection YAML file per endpoint, grouped by the spec's own tags (`documents`, `safes`, `webhooks`, `signatories`, ...).
- `environments/*.yml` — `baseUrl` per environment; `tokenAPI`/`cryptKey` declared as secrets, set locally per machine.
- `opencollection.yml` — collection root marker (OpenCollection YAML format) + the inherited `tokenAPI` header. `bruno.json` is also kept for tools that only recognize the classic format.

## Known gaps

- Multipart upload requests (`.../upload`, `.../uploadslave`, `.../templates/upload`) reference a placeholder `./example.pdf` — point it at a real file before sending.
- D4Sign rate-limits to 10 requests/hour per the original docs; back off on `429`.
- The spec was exported at some point in the past and can drift from the live API — see `docs/COVERAGE.md` for the full comparison against the live docs, and `docs/REGENERATING.md` for how to update.
