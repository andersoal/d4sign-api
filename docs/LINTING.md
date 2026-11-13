# Linting and validating the spec

[`speakeasy-api/openapi`](https://github.com/speakeasy-api/openapi) is a Go CLI for OpenAPI documents. This repo uses it to validate and lint `openapi/d4sign.yaml` before any change ships.

## Install

```bash
go install github.com/speakeasy-api/openapi/cmd/openapi@latest
```

This puts `openapi` on your `PATH` (inside `$(go env GOPATH)/bin`, usually `~/go/bin`). It needs a Go toolchain — there's no prebuilt binary wired into `mise.toml` yet.

## Commands this repo uses

Run these from the repo root.

```bash
# Catches real spec bugs: missing required fields, broken refs, bad types.
openapi spec validate openapi/d4sign.yaml

# Style and best-practice checks, using this repo's rule config (see below).
openapi spec lint --config openapi/lint.yaml openapi/d4sign.yaml

# Confirm the path/operation counts AGENTS.md asks for after a prose edit.
openapi spec query 'operations | where(path != "") | group-by(path) | length' openapi/d4sign.yaml   # paths
openapi spec query 'operations | where(path != "") | length' openapi/d4sign.yaml                     # operations
```

Both counts exclude the one `webhooks.documents_callback` operation. The CLI's `operations` source reports it with an empty `path`. Including it gives 73 operations and 71 paths instead of 72 and 70. That's the CLI counting the webhook operation as a 71st "path", not a bug in the spec.

Other commands worth knowing about, not yet part of this repo's workflow:

- `openapi spec list-rules` — prints all ~270 lint rules with severity and fix info.
- `openapi spec query '<pipeline>' openapi/d4sign.yaml` — ad hoc structural questions (see `openapi spec query-reference` for the query language).
- `openapi overlay compare old.yaml new.yaml` — generates an overlay describing exactly what changed between two spec versions. It could replace eyeballing a diff when you confirm a prose edit touched no structural keys (the rule in `AGENTS.md`'s "Editing prose" section). No script calls it yet.
- `openapi spec explore openapi/d4sign.yaml` — interactive terminal browser for the spec, an alternative to grepping the YAML.

## The lint config (`openapi/lint.yaml`)

Running `openapi spec lint` with no config (the `all` ruleset) reports about 1500 findings on this spec. Almost all of them ask this document to assert something about D4Sign's live API. Either it isn't true, or we haven't confirmed it — things like string length limits, rate-limit response headers, or 429/500 error schemas D4Sign doesn't publish. Adding them would mean inventing API behavior, which `AGENTS.md`'s "Verifying API claims" rule forbids.

`openapi/lint.yaml` disables exactly those rules, each with a one-line reason in the file itself. Everything *not* in that list is a real finding — fix it, don't suppress it. With the config, `openapi spec lint --config openapi/lint.yaml openapi/d4sign.yaml` reports 0 problems as of this writing.

Suppose you confirm a disabled rule's concern is true of the live API (confirmed, not guessed — see "Verifying API claims"). Then remove it from the config, and fix the real findings instead of leaving them suppressed.

Known backlog, deliberately not faked to silence a lint hint:

- `oas3-example-missing` (148 hints) — most response/request schemas have no `example`. Real examples need pulling from verified live responses, one at a time, not placeholder values.
- `style-license-url` (1 hint) — `info.license` has no URL because we don't have a confirmed D4Sign terms-of-service link to cite, and this repo doesn't guess URLs.

## Workflow

Before committing any change to `openapi/d4sign.yaml`:

1. `openapi spec validate openapi/d4sign.yaml` — must report 0 errors.
2. `openapi spec lint --config openapi/lint.yaml openapi/d4sign.yaml` — must report 0 problems.
3. If you edited prose only, confirm the path/operation counts above stay the same.
