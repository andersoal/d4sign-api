---
name: d4sign-docs
description: Unofficial D4Sign electronic signature API knowledge — auth (tokenAPI/cryptKey), environments, core workflows (upload, signers, send to signature, webhooks), rate limits/errors, the PHP SDK, and the full endpoint reference. Use when integrating with or debugging calls to the D4Sign API.
metadata:
  author: unofficial / community (not produced or endorsed by D4Sign)
  version: "1.0"
  tags: [docs, api, d4sign]
---

## Core Workflows

Upload a document, register signers, send for signature, optionally embed the signing UI. Full walk-through: `../../site/src/content/docs/guides/core-workflows.md` and `../../site/src/content/docs/guides/getting-started.md`.

```http
POST https://secure.d4sign.com.br/api/v1/documents/{uuid_safe}/upload
Content-Type: multipart/form-data
tokenAPI: {tokenAPI}

file=@contract.pdf
uuid_folder={uuid_folder}   # optional
workflow=2
```

```http
POST https://secure.d4sign.com.br/api/v1/documents/{uuid_document}/sendtosigner
Content-Type: application/json

{ "message": "...", "workflow": "0", "skip_email": "1" }
```

## Authentication

Every request needs `tokenAPI` and `cryptKey` as **query params**; also send `tokenAPI` as a header. Details: `../../site/src/content/docs/guides/authentication.md`.

## Environments

| Environment | Endpoint | Legal validity |
| --- | --- | --- |
| Production | `https://secure.d4sign.com.br/api/v1` | Yes |
| Sandbox | `https://sandbox.d4sign.com.br/api/v1` | No |

Details: `../../site/src/content/docs/guides/environments.md`.

## Gotchas

- Endpoint paths are case-sensitive, mostly lowercase; wrong case can return `200` with no useful payload.
- Documents in a folder/subfolder may not show up when listing from a parent folder.
- `skip_email` must be `1` when using EMBED or in-person signing.
- Rate limit: 10 requests/hour — back off on `429`.

## Error Handling

- `401` — bad or mismatched (prod vs. sandbox) `tokenAPI`/`cryptKey`.
- `429` — rate limit exceeded.
Details: `../../site/src/content/docs/guides/rate-limits-and-errors.md`.

## Reference Loading Instructions

- Full endpoint-by-endpoint parameters, request/response schemas: the generated API Reference. Source spec: `../../openapi/d4sign.yaml` (67 endpoints, OpenAPI 3.1). Read it directly for exact schemas, or browse the built site under `/reference/`.
- PHP SDK usage: `../../site/src/content/docs/sdk/php.md` (SDK source: `../../sdk/php/src/D4sign/`).
- Webhooks (POSTBack): `../../site/src/content/docs/guides/webhooks.md`.
- Runnable requests for every endpoint (Bruno collection): `../../collections/bruno/` — see `../../collections/bruno/README.md`.
