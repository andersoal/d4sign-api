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
| `429 Too Many Requests` | Rate limit exceeded (10 req/hour). | Back off exponentially. Batch requests where possible. |
| `5xx` | Problem on D4Sign's servers, not your request. | Retry later. The body is `{ "message": "Server error." }`. |

For the full set of responses per endpoint, see the [API Reference](/d4sign-api/reference/).

## Error response shapes

D4Sign does not use one consistent error envelope. The field names vary by failure type. These are the shapes actually documented in the OpenAPI spec (`components.responses` in `openapi/d4sign.yaml`). We also **ran the first one live**, through the [Bruno collection](/d4sign-api/tools/bruno/) against Sandbox with an invalid `tokenAPI`:

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
We have not captured a `429` body yet. The docs state only the 10/hour policy, not its exact error shape. If you trigger one, add it here.
:::

Do not rely on the HTTP status code alone. As the first row in the table shows, some failure modes return `200` instead of an error status. The path-case mismatch is a notable example. The error is visible only in the body.

## Testing with Postman

D4Sign publishes an official [Postman collection](https://documenter.getpostman.com/view/1486030/d4sign-api/2TnpL3) ([run it directly](https://app.getpostman.com/run-collection/5d43ba6b3834eb9f5c66)). After importing, set `tokenAPI` and `cryptKey` in the top-right environment variables.

:::note
Postman's default host in that collection is **Sandbox** — switch it to Production when you're ready to go live.
:::
