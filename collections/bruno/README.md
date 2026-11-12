# D4Sign API — Bruno Collection

72 requests covering the full D4Sign REST API, generated from [`openapi/d4sign.yaml`](../../openapi/d4sign.yaml) via `scripts/openapi_to_bruno_endpoints.py` + the Bruno OpenCollection scaffolder + `scripts/fix_bruno_multipart_bodies.py`. Regenerate it after the spec changes instead of hand-editing requests — see [`../../docs/REGENERATING.md`](../../docs/REGENERATING.md).

D4Sign's own OpenAPI export is missing a handful of these (webhooks v2.0, document view-URL generation, Word template upload). We found them missing when we compared the export against the live reference nav at [docapi.d4sign.com.br/v2.0/reference](https://docapi.d4sign.com.br/v2.0/reference), and we added them by hand. See `docs/COVERAGE.md` for the full audit.

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

D4Sign requires **both** `tokenAPI` and `cryptKey` together. OAS models this as an AND-combined `security` requirement. Bruno's `auth: apikey` mode holds only one key. Its OpenAPI-sync feature collapses the pair into one key and silently drops the other key when you re-sync from the UI (filed upstream: [usebruno/bruno#9817](https://github.com/usebruno/bruno/issues/9817)). Instead:

- Every request inherits the `tokenAPI` header from `opencollection.yml`'s collection-root `request.headers`. You don't need to set it per request.
- `tokenAPI` and `cryptKey` (query params) are explicit on every request — Bruno has no mechanism to inherit query params, only headers/auth/vars.
- The OpenAPI sync in `opencollection.yml` has `autoCheck: false` on purpose — re-syncing from the Bruno UI re-triggers the collapse described above. Regenerate from the spec with the scripts instead (`../../docs/REGENERATING.md`).

## Query params showing unchecked in Bruno Desktop

Bruno Desktop sets a query param's checkbox state from whether the param text appears in the **URL text itself**, not from the structured `params:` list alone. Because of this, every generated request's `url` field also carries the literal query string (`?tokenAPI={{tokenAPI}}&cryptKey={{cryptKey}}...`) in addition to the `params:` entries. If a param ever shows unchecked, this mismatch is almost certainly why. The generator keeps both in sync, so this should not happen again after a regeneration.

## Documenting what you test

`requests/safes/001-list-all-safes.yml` carries a real test that asserts the response shape. On success, the response is an array. On failure, it has a `message` field. This is D4Sign's actual error envelope. We confirmed this live — see [`guides/rate-limits-and-errors.md`](../../site/src/content/docs/guides/rate-limits-and-errors.md). The point: when you run a request against the real API, even a failing one, add what actually came back into the docs. Don't let it disappear into a terminal scrollback. Add more tests through the `TESTS` dict in `scripts/openapi_to_bruno_endpoints.py`. A hand-edit to a generated request file gets overwritten on the next regeneration.

**Caution**: don't use a live `401`-vs-`404` response to decide whether an endpoint exists. D4Sign requires a valid `tokenAPI`/`cryptKey` pair before it matches the route. Because of this, an invalid credential pair returns the same `401` for a path that doesn't exist at all. We confirmed this by testing a deliberately nonsense path. The only reliable signal for "does this endpoint exist" is the official reference nav itself, or a `200`/`400`/`404` response with *valid* credentials.

## Structure

- `requests/<resource>/NNN-name.yml` — one OpenCollection YAML file per endpoint, grouped by the spec's own tags (`documents`, `safes`, `webhooks`, `signatories`, ...).
- `scenarios/<recipe-name>/NN-step.yml` — multi-step, chained Bruno versions of the recipes in [`../../site/src/content/docs/recipes/`](../../site/src/content/docs/recipes/), one request per step, with `runtime.scripts` passing `uuid_document` etc. from one step's response into the next step's request. Hand-written, untouched by regeneration — see [`scenarios/README.md`](scenarios/README.md).
- `environments/*.yml` — `baseUrl` per environment. Each machine sets `tokenAPI`/`cryptKey` locally as secrets.
- `opencollection.yml` — collection root marker (OpenCollection YAML format) + the inherited `tokenAPI` header. `bruno.json` is also kept for tools that only recognize the classic format.

## Known gaps

- Multipart upload requests (`.../upload`, `.../uploadslave`, `.../templates/upload`) reference a placeholder `./example.pdf` — point it at a real file before sending.
- D4Sign rate-limits to 10 requests/hour per the original docs. Back off on `429`.
- We exported the spec at a past point in time, so it can drift from the live API. See `docs/COVERAGE.md` for the full comparison against the live docs, and `docs/REGENERATING.md` for how to update it.
