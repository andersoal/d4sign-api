---
title: Authentication
description: How tokenAPI and cryptKey work across the D4Sign API.
---

Two account-level secrets authenticate every request:

- `tokenAPI`
- `cryptKey`

Unlike a typical bearer-token API, D4Sign expects both as **query string parameters on every request**, and also accepts `tokenAPI` as a header:

```http
GET https://secure.d4sign.com.br/api/v1/users/list?tokenAPI={tokenAPI}&cryptKey={cryptKey}&pg=1
tokenAPI: {tokenAPI}
```

:::tip
Send `tokenAPI` as both a header and a query parameter. This is the documented recommendation. The header alone is not officially guaranteed to work on every endpoint. Always send both.
:::

`cryptKey` only needs to be sent if it's enabled on your account — find both values under **Dev API** in your D4Sign account settings. Contact suporte@d4sign.com.br if you can't locate them.

## Storing credentials

Treat `tokenAPI` and `cryptKey` like passwords:

- Never commit them to a repository or client-side code.
- Store them as environment variables or secrets in your deployment platform.
- Use separate pairs for [Sandbox and Production](/d4sign-api/guides/environments/) — they are not interchangeable.

## In the PHP SDK

```php
$client = new D4sign\Client();
$client->setAccessToken('{tokenAPI}');
$client->setCryptKey('{cryptKey}');
```

## In the Bruno collection

Set `tokenAPI` and `cryptKey` as **secrets** on the `Production` or `Sandbox` environment — see [Bruno Collection](/d4sign-api/tools/bruno/).
