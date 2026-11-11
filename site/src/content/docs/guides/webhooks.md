---
title: Webhooks
description: Register a POSTBack URL to be notified of document status changes.
---

D4Sign calls webhooks "POSTBack". You can register one per **document** or one per **safe**.

:::note
A safe-level webhook, configured from the D4Sign Dashboard, applies to every document registered in that safe — you don't need to register it per document.
:::

## List a document's webhook

```http
GET https://secure.d4sign.com.br/api/v1/documents/{uuid_document}/webhooks
```

```php
$client->documents->webhooklist('{uuid_document}');
```

## Register a document webhook

```http
POST https://secure.d4sign.com.br/api/v1/documents/{uuid_document}/webhooks
Content-Type: application/json

{ "url": "https://yourdomain.com/d4sign/webhook" }
```

```php
$client->documents->webhookadd('{uuid_document}', 'https://yourdomain.com/d4sign/webhook');
```

## What triggers a webhook, and what you get

D4Sign fires a `POST` (form-data) to your URL when a document is **signed by a signer**, **finished**, or **canceled**, and when an **e-mail fails to deliver** to a signer:

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
- Verify the payload defensively (e.g. by re-fetching the document status) rather than trusting it blindly.

D4Sign also signs every webhook with **HMAC-SHA256**: it hashes the document UUID with your account's secret key and sends it as `Content-Hmac: sha256=<hash>`. Enable your secret key in the API area ("Gerar Secret Key MAC"), then compute the same hash (UUID + secret key) on your side and compare it to the header to confirm the request came from D4Sign and wasn't tampered with.
