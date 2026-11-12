# Coverage audit against the live docapi.d4sign.com.br

`openapi/d4sign.yaml` started as a one-time export of D4Sign's own OpenAPI spec. Exports go stale. D4Sign's own guide pages and reference pages do not always agree with each other either. This document is a point-in-time comparison against the live site, done by hand, to find what the export missed. Re-run it periodically. It is not automated.

## Method

- **Guide pages** (`/docs/*`): read via D4Sign's own `llms.txt` index, which lists every guide page by section.
- **Reference pages** (`/reference/*` and `/v2.0/reference/*`): D4Sign runs two doc *versions* side by side. `/v2.0/reference` is the current, more complete one — it has everything `/reference` (v1) has, plus endpoints `/reference` doesn't list at all. Treat `/v2.0/reference`'s nav as the source of truth for "does this endpoint exist."
- **Existence checks are nav-based, not HTTP-based.** D4Sign requires a valid `tokenAPI`/`cryptKey` pair before it matches the route. Because of this, a nonexistent path and a real endpoint with a bad credential return the same `401`. We verified this by testing a deliberately nonsense path against Sandbox. A live request only tells you the request/response *shape* once you already know from the docs that the path is real. It cannot tell you whether the path exists in the first place.

## Guide pages (19 total)

| Section | Pages | Covered here |
| --- | --- | --- |
| Introdução | 1 | Yes — `guides/getting-started.md`, `guides/environments.md`, `guides/authentication.md`, `guides/rate-limits-and-errors.md` |
| API Rest (endpoint guides) | 7 (Cofres, Documentos, Signatários, Usuários, Tags, Certificados, Observadores) | Yes — folded into `openapi/d4sign.yaml` operation descriptions + `guides/core-workflows.md` |
| WebHooks | 4 | Yes — `guides/webhooks.md` |
| Embed D4sign | 3 | Yes — `guides/embed.md` |
| SSO SAML 2.0 | 4 | **No, deliberately.** Enterprise IdP federation (Azure AD / Google Workspace) for logging into the D4Sign *dashboard*, not a REST API. This is out of scope for a repo about calling the API. We link to it from `guides/embed.md` instead of duplicating it. |

## Reference endpoints

`/v2.0/reference` lists about 70 endpoint pages across 8 sections (Vaults/Safes, Documents, Signers, Users, Tags, ICP-Brasil Certificates, Watchers, Webhook). We compared that nav against `openapi/d4sign.yaml` and found 4 endpoints the original export was missing entirely. We added these by hand in this pass. Each one's `description` field names where it came from. Each one also notes that we have not live-verified its request/response shape, because we had no valid credentials at hand when we added it:

| Endpoint | Why it was missing |
| --- | --- |
| `GET /api/v1/webhooks/v2/` | A newer v2.0-only endpoint. The v1 export never had it. |
| `POST /api/v1/webhooks/v2/` | Same. |
| `POST /api/v1/documents/{uuid_document}/generate-document-view` | Present on `/v2.0/reference` (`document-and-attachment-viewer`), absent from the v1 export. |
| `POST /api/v1/templates/upload` | Present on `/v2.0/reference` (`template-word-upload`). It uploads a *new* template. Do not confuse it with `makedocumentbytemplateword`, which *generates a document from* an existing template. |

## Endpoints documented in the guide but not in the reference nav

The reverse direction: the Signatários **guide** page walks through plain "remove a positioned signature" (`removepins`) and "list positioned signatures" (`listpins`) as sub-steps of the pin-positioning workflow. Neither action has its own entry in `/v2.0/reference`'s Signers section. Only the *replicated*-position variants (`addpinswithreplics`/`removepinswithreplics`) and the base `addpins` show up there. Both actions are already in `openapi/d4sign.yaml` (`documents_signatories_pins_remove`, `documents_signatories_pins_list`), with descriptions sourced from the guide text. No action is needed here. It is worth knowing this asymmetry exists, so a future "is X real" check does not stop at the reference nav alone.

## Duplicate reference entries (same endpoint, multiple pages)

D4Sign's own reference nav documents a few endpoints more than once, under different titles and slugs. This is not a gap on our side. We note it here so nobody re-adds them as if they were new:

- `document-from-word-template` and `create-document-from-word-template-with-multiple-fillers` are the same endpoint (`makedocumentbytemplateword`). The second page is a usage variant (multiple "preenchedores"), not a different path.
- The v1 `/reference` nav's "Listar anexos" entry links to the same slug as "Download Documentos e Certificados Desmembrados". This is likely a stale link on D4Sign's side. Do not replicate it.

## What wasn't done

- The 4 newly-added endpoints' request/response *shapes* came from reading the reference page text, not from a live call with valid credentials. Unlike the rest of this repo's error-shape documentation (see `guides/rate-limits-and-errors.md`), we have not live-verified these yet. Re-test them once real credentials are available, and update their descriptions with what actually comes back.
- We did not do a page-by-page deep read of every one of the ~70 `/v2.0/reference` pages against every one of our 72 operations' full parameter lists. This pass compared titles and slugs, to find missing *endpoints*, not missing *parameters* on endpoints we already have. A parameter-level pass would be the natural next step if we suspect drift there too.
