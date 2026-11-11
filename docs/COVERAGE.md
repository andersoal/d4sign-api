# Coverage audit against the live docapi.d4sign.com.br

`openapi/d4sign.yaml` started as a one-time export of D4Sign's own OpenAPI spec. Exports go stale, and D4Sign's guide pages and reference pages don't always agree with each other either — so this is a point-in-time comparison against the live site, done by hand, to find what the export missed. Re-run it periodically; it is not automated.

## Method

- **Guide pages** (`/docs/*`): read via D4Sign's own `llms.txt` index, which lists every guide page by section.
- **Reference pages** (`/reference/*` and `/v2.0/reference/*`): D4Sign runs two doc *versions* side by side. `/v2.0/reference` is the current, more complete one — it has everything `/reference` (v1) has, plus endpoints `/reference` doesn't list at all. Treat `/v2.0/reference`'s nav as the source of truth for "does this endpoint exist."
- **Existence checks are nav-based, not HTTP-based.** D4Sign validates `tokenAPI`/`cryptKey` *before* route matching, so a request to a path that doesn't exist at all still returns the same `401` as a request to a real endpoint with a bad credential (confirmed by testing a deliberately nonsense path against Sandbox). A live request only tells you the request/response *shape* once you already know the path is real from the docs — it can't tell you whether the path exists in the first place.

## Guide pages (19 total)

| Section | Pages | Covered here |
| --- | --- | --- |
| Introdução | 1 | Yes — `guides/getting-started.md`, `guides/environments.md`, `guides/authentication.md`, `guides/rate-limits-and-errors.md` |
| API Rest (endpoint guides) | 7 (Cofres, Documentos, Signatários, Usuários, Tags, Certificados, Observadores) | Yes — folded into `openapi/d4sign.yaml` operation descriptions + `guides/core-workflows.md` |
| WebHooks | 4 | Yes — `guides/webhooks.md` |
| Embed D4sign | 3 | Yes — `guides/embed.md` |
| SSO SAML 2.0 | 4 | **No, deliberately.** Enterprise IdP federation (Azure AD / Google Workspace) for logging into the D4Sign *dashboard*, not a REST API. Out of scope for a repo about calling the API; linked from `guides/embed.md` instead of duplicated. |

## Reference endpoints

`/v2.0/reference` lists ~70 endpoint pages across 8 sections (Vaults/Safes, Documents, Signers, Users, Tags, ICP-Brasil Certificates, Watchers, Webhook). Comparing that nav against `openapi/d4sign.yaml` found 4 endpoints the original export was missing entirely — added by hand this pass, each tagged in its own `description` with where it came from and a reminder that it wasn't live-verified request/response-wise (no valid credentials at hand when these were added):

| Endpoint | Why it was missing |
| --- | --- |
| `GET /api/v1/webhooks/v2/` | Newer v2.0-only endpoint; v1 export never had it. |
| `POST /api/v1/webhooks/v2/` | Same. |
| `POST /api/v1/documents/{uuid_document}/generate-document-view` | Present on `/v2.0/reference` (`document-and-attachment-viewer`), absent from the v1 export. |
| `POST /api/v1/templates/upload` | Present on `/v2.0/reference` (`template-word-upload`) — uploads a *new* template; don't confuse with `makedocumentbytemplateword`, which *generates a document from* an existing template. |

## Endpoints documented in the guide but not in the reference nav

The reverse direction: the Signatários **guide** page walks through plain "remove a positioned signature" (`removepins`) and "list positioned signatures" (`listpins`) as sub-steps of the pin-positioning workflow, but neither has its own entry in `/v2.0/reference`'s Signers section (only the *replicated*-position variants, `addpinswithreplics`/`removepinswithreplics`, and the base `addpins`, show up there). Both are already in `openapi/d4sign.yaml` (`documentsSignatoriesPinsRemove`, `documentsSignatoriesPinsGetList`) with descriptions sourced from the guide text — no action needed, just worth knowing this asymmetry exists so a future "is X real" check doesn't stop at the reference nav alone.

## Duplicate reference entries (same endpoint, multiple pages)

D4Sign's own reference nav documents a few endpoints more than once under different titles/slugs — not a gap on our side, just noted so nobody re-adds them as if they were new:

- `document-from-word-template` and `create-document-from-word-template-with-multiple-fillers` are the same endpoint (`makedocumentbytemplateword`); the second page is a usage variant (multiple "preenchedores"), not a different path.
- The v1 `/reference` nav's "Listar anexos" entry links to the same slug as "Download Documentos e Certificados Desmembrados" — likely a stale link on D4Sign's side, not something to replicate.

## What wasn't done

- The 4 newly-added endpoints' request/response *shapes* came from reading the reference page text, not from a live call with valid credentials — unlike the rest of this repo's error-shape documentation (see `guides/rate-limits-and-errors.md`), these aren't live-verified yet. Re-test them once real credentials are available and update their descriptions with what actually comes back.
- Didn't do a page-by-page deep read of every one of the ~70 `/v2.0/reference` pages against every one of our 72 operations' full parameter lists — this pass compared titles/slugs to find missing *endpoints*, not missing *parameters* on endpoints we already have. A parameter-level pass would be the natural next step if drift is suspected there too.
