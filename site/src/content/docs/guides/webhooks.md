---
title: Webhooks
description: Register a POSTBack URL to be notified of document status changes.
---

D4Sign calls webhooks "POSTBack". You can register one per **document** or one per **safe**. A safe-level webhook applies to every document in that safe — you do not need to register it per document.

:::caution[v1 vs v2.0]
There are two generations of this API. The original endpoints below work per document only. A newer `v2.0` endpoint also supports safe-level registration through the API itself (previously, that required the Dashboard). Prefer v2.0 for new integrations.

D4Sign's exported OpenAPI spec, which most of this reference comes from, does not include this v2.0 endpoint. We found it by comparing against the live docs at [docapi.d4sign.com.br](https://docapi.d4sign.com.br/reference/cadastrar-ou-atualizar-uma-url-de-webhook-20), and we added it by hand.

Do not rely on live `401`-vs-`404` probing to confirm a path like this exists. D4Sign requires a valid `tokenAPI` before it matches the route, so an invalid one returns the same `401` for a path that does not exist at all. We confirmed this by testing a deliberately nonsense path. The official reference nav is the only trustworthy signal for whether an endpoint exists.
:::

## v1 — per document

```http
GET https://secure.d4sign.com.br/api/v1/documents/{uuid_document}/webhooks
```

```php
$client->documents->webhooklist('{uuid_document}');
```

```http
POST https://secure.d4sign.com.br/api/v1/documents/{uuid_document}/webhooks
Content-Type: application/json

{ "url": "https://yourdomain.com/d4sign/webhook" }
```

```php
$client->documents->webhookadd('{uuid_document}', 'https://yourdomain.com/d4sign/webhook');
```

## v2.0 — document or safe

```http
GET https://secure.d4sign.com.br/api/v1/webhooks/v2/?type=documento&uuid={uuid}
```

```http
POST https://secure.d4sign.com.br/api/v1/webhooks/v2/
Content-Type: application/json

{ "type": "documento", "uuid": "{uuid}", "url": "https://yourdomain.com/d4sign/webhook" }
```

`type` is `documento` or `cofre`. The request shape is the same either way. Point `uuid` at the safe instead of a document to register it at the safe level through the API.

Not in the PHP SDK (it predates this endpoint) — call it directly, or see the [Bruno collection](/d4sign-api/tools/bruno/).

## What triggers a webhook, and what you get

D4Sign fires a `POST` (form-data) to your URL on these events:

- a signer **signs** the document
- the document is **finished**
- the document is **canceled**
- an **e-mail fails to deliver** to a signer

```json title="Finished"
{ "uuid": "UUID-DOCUMENT", "type_post": "1", "message": "Finished document" }
```
```json title="E-mail not delivered"
{ "uuid": "UUID-DOCUMENT", "type_post": "2", "message": "E-mail not sent", "email": "signer@example.com" }
```
```json title="Canceled"
{ "uuid": "UUID-DOCUMENT", "type_post": "3", "message": "Cancelled document" }
```
```json title="Signed"
{ "uuid": "UUID-DOCUMENT", "type_post": "4", "message": "Signed", "email": "signer@example.com" }
```

:::tip
Use [requestcatcher.com](http://requestcatcher.com/) while testing — it gives you a URL that just shows you every request it receives.
:::

## Retries

If your URL is unreachable, D4Sign retries up to 6 more times: immediately, then after 1h, 1h, 1h, 6h, 6h, 12h. A webhook is only lost if your URL stays down for more than **27 hours**.

## Securing your endpoint

- Use a public **HTTPS** URL.
- Add your own credentials to the URL (basic auth: `https://user:pass@yourdomain.com/...`) or a secret token in the path (`https://yourdomain.com/webhook/TOKEN`) — D4Sign sends no auth header of its own.
- Confirm the payload defensively (e.g. by re-reading the document status) rather than trusting it blindly.

D4Sign also signs every webhook with **HMAC-SHA256**: it hashes the document UUID with your account's secret key and sends it as `Content-Hmac: sha256=<hash>`. Enable your secret key in the API area ("Gerar Secret Key MAC"). Then compute the same hash (UUID + secret key) on your side. Compare it to the header. This confirms the request came from D4Sign and was not tampered with.
