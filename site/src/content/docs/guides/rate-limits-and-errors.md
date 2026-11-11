---
title: Rate Limits & Errors
description: HTTP status codes, retry behavior, and the request rate limit.
---

## Rate limit

D4Sign limits requests to **10 per hour** per credential pair by default. Implement exponential backoff on `429` rather than retrying immediately. To raise the limit, contact comercial@d4sign.com.br.

## Common status codes

| Status | Meaning | What to do |
| --- | --- | --- |
| `200` with an empty/odd payload | Usually a path case mismatch, not success — see [Environments](/d4sign-api/guides/environments/). | Check the endpoint path is exactly lowercase as documented. |
| `401 Unauthorized` | Invalid or missing `tokenAPI`/`cryptKey`, or using a Sandbox credential against Production (or vice versa). | Re-check [Authentication](/d4sign-api/guides/authentication/). |
| `429 Too Many Requests` | Rate limit exceeded (10 req/hour). | Back off exponentially; batch requests where possible. |
| `5xx` | Problem on D4Sign's servers, not your request. | Retry later; the body is `{ "message": "Server error." }`. |

For the full set of responses per endpoint, see the [API Reference](/d4sign-api/reference/).

## Error response shapes

D4Sign doesn't use one consistent error envelope — the field names vary by failure type. These are the shapes actually documented in the OpenAPI spec (`components.responses` in `openapi/d4sign.yaml`); the first one is also **confirmed live** (captured running the [Bruno collection](/d4sign-api/tools/bruno/) against Sandbox with an invalid `tokenAPI`):

```json title="401 — bad credentials (live-verified)"
{ "message": "API error: Check API user.", "mensagem_pt": "Chave de API inválida." }
```

```json title="400 — business-rule rejection (message only, or message + mensagem_pt)"
{ "message": "Safe not founded" }
{ "message": "Invalid template ID: OTgx - 6a036f94-26d5-4aa6-89d8-4fddae6b309b", "mensagem_pt": "ID do template inválido." }
```

```json title="404 — unknown method/resource (different shape: status + error)"
{ "status": false, "error": "Método desconhecido" }
```

:::note
No `429` body has been captured yet — only the 10/hour policy is documented, not its exact error shape. If you trigger one, it's worth adding here.
:::

Don't rely on the HTTP status code alone — as the first row in the table above notes, some failure modes (notably the path-case mismatch) still return `200` with the error only visible in the body.

## Testing with Postman

D4Sign publishes an official [Postman collection](https://documenter.getpostman.com/view/1486030/d4sign-api/2TnpL3) ([run it directly](https://app.getpostman.com/run-collection/5d43ba6b3834eb9f5c66)). After importing, set `tokenAPI` and `cryptKey` in the top-right environment variables.

:::note
Postman's default host in that collection is **Sandbox** — switch it to Production when you're ready to go live.
:::
