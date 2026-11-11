---
title: Getting Started
description: Authenticate and make your first D4Sign API call.
---

D4Sign signing flows all follow the same five steps:

1. Upload the document.
2. Register a webhook (POSTBack) so your system hears about status changes.
3. Register the signers.
4. Send the document for signature.
5. Optionally, use D4Sign's EMBED feature to show the signing UI on your own website.

This guide covers step 1 and the authentication every request needs. See [Core Workflows](/d4sign-api/guides/core-workflows/) for steps 2–5, and the [API Reference](/d4sign-api/reference/) for every parameter.

## Get credentials

From your D4Sign account, grab:

- `tokenAPI` — your API token.
- `cryptKey` — your crypt key.

Both are account-level secrets. Treat them like passwords — see [Authentication](/d4sign-api/guides/authentication/).

## Pick an environment

Use **Sandbox** (`https://sandbox.d4sign.com.br/api/v1`) while integrating. Nothing signed there has legal validity. Switch to **Production** (`https://secure.d4sign.com.br/api/v1`) when you go live. See [Environments](/d4sign-api/guides/environments/).

## Upload a document

```http
POST https://sandbox.d4sign.com.br/api/v1/documents/{uuid_safe}/upload?tokenAPI={tokenAPI}&cryptKey={cryptKey}
Content-Type: multipart/form-data
tokenAPI: {tokenAPI}

file=@contract.pdf
uuid_folder={uuid_folder}   # optional
workflow=2
```

Every document lives inside a **safe** (`uuid_safe`), an encrypted vault — it's required. The upload runs in the background: you get a `uuid` back immediately, and the document is processed (encrypted, serial-stamped, preview generated) asynchronously.

Using the PHP SDK instead:

```php
use D4sign\Client;

$client = new Client();
$client->setAccessToken('{tokenAPI}');
$client->setCryptKey('{cryptKey}');

$result = $client->documents->upload('{uuid_safe}', '/path/to/contract.pdf');
```

See the full [PHP SDK guide](/d4sign-api/sdk/php/) or the [Bruno collection](/d4sign-api/tools/bruno/) to run this without writing code.
