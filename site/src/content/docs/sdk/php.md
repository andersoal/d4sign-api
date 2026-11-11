---
title: Using the PHP SDK
description: Install and use the original D4Sign PHP client.
---

This repository ships the original D4Sign PHP client, now living at [`sdk/php/`](https://github.com/andersoal/d4sign-api/tree/master/sdk/php). It's one way to call the API — see the [API Reference](/d4sign-api/reference/) if you'd rather call the REST endpoints directly, or [Bruno Collection](/d4sign-api/tools/bruno/) to explore them without writing code.

:::caution
Requires PHP ≥ 5.5. The SDK predates this documentation rewrite and covers a subset of the full API (documents, safes, templates, folders, account, users, groups, tags, certificates). For anything it doesn't expose, call the REST endpoint directly per the [API Reference](/d4sign-api/reference/).
:::

## Install

Via Composer, inside `sdk/php/`:

```json
{
  "require": {
    "d4sign/d4sign-php": "dev-master"
  },
  "minimum-stability": "dev",
  "repositories": [
    { "type": "git", "url": "https://github.com/d4sign/d4sign-php" }
  ]
}
```

Without a dependency manager:

```php
require_once(__DIR__ . '/vendor/autoload.php');
```

## Authenticate

```php
use D4sign\Client;

$client = new Client();
$client->setAccessToken('{tokenAPI}');
$client->setCryptKey('{cryptKey}'); // see the Authentication guide
```

By default the client points at Production (`https://secure.d4sign.com.br/api/`). Switch to Sandbox with:

```php
$client->setUrl('https://sandbox.d4sign.com.br/api/');
```

## Documents

```php
$client->documents->find();                       // list every document
$client->documents->find('{uuid_document}');       // a single document
$client->documents->safe('{uuid_safe}');            // every document in a safe
$client->documents->status('{id_status}');          // every document in a phase (see Core Workflows)

$client->documents->upload('{uuid_safe}', '/path/to/file.pdf');
$client->documents->createList('{uuid_document}', $signers);
$client->documents->sendToSigner('{uuid_document}', $message, $skip_email, $workflow);
$client->documents->listsignatures('{uuid_document}');
$client->documents->cancel('{uuid_document}');
$client->documents->resend('{uuid_document}', $email);

$url = $client->documents->getfileurl('{uuid_document}', 'zip'); // or 'pdf'
```

## Webhooks

```php
$client->documents->webhooklist('{uuid_document}');
$client->documents->webhookadd('{uuid_document}', 'https://yourdomain.com/d4sign/webhook');
```

Every call throws `D4sign\D4signException` on an unexpected HTTP status — wrap calls in `try`/`catch`:

```php
try {
    $docs = $client->documents->find();
} catch (Exception $e) {
    echo $e->getMessage();
}
```

See [Core Workflows](/d4sign-api/guides/core-workflows/) for the full document lifecycle and [Rate Limits & Errors](/d4sign-api/guides/rate-limits-and-errors/) for what the exceptions mean.
