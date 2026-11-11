---
title: "Recipe: Collect a Signature Without Leaving Your Site"
description: Upload, register the signer for EMBED, send without an email, then render the iframe.
---

Combines the API calls that prepare a document for [EMBED](/d4sign-api/guides/embed/) with the iframe snippet itself.

:::caution
EMBED must be activated on your account first — contact suporte@d4sign.com.br. Without it, the iframe will load but the signing flow won't work.
:::

## 1. Upload and register the signer for EMBED

```php
$uuid_document = $client->documents->upload('{uuid_safe}', '/path/to/contract.pdf')->uuid;

$client->documents->createList($uuid_document, [
    [
        'email' => 'signer@example.com',
        'act' => '1',
        'foreign' => '0',
        'certificadoicpbr' => '0',
        'assinatura_presencial' => '0',
        'embed_methodauth' => 'email', // or 'sms', 'whats', 'password'
    ],
]);
```

## 2. Send *without* the email link

```php
$client->documents->sendToSigner($uuid_document, '', $workflow = 0, $skip_email = 1);
```

`skip_email: 1` is mandatory here — the signer is about to see the document in your own UI, not click a link in an email.

## 3. Render the iframe

```html
<div id="signature-div"></div>
<script>
  var key = "<?= $uuid_document ?>";
  var host = "https://secure.d4sign.com.br/embed/viewblob";
  var container = "signature-div";
  var signer_email = "signer@example.com"; // must match step 1's email exactly
  // ...rest of the snippet in the Embedding guide
</script>
```

Full snippet with every parameter, the batch variant, and the `signed`/`wrong-data` callback events: [Embedding the Signing UI](/d4sign-api/guides/embed/).

## 4. Know when it's done

The iframe's `message` event fires client-side the moment the signer finishes — good for updating your UI immediately. It is **not** a substitute for a server-side webhook: the browser tab can close before your server hears about it. Register one (see [Upload, Send, and React to Completion](/d4sign-api/recipes/send-and-track/#2-register-a-webhook-once-at-the-safe-not-per-document)) for the authoritative signal.

## What this combines

`upload` · `createlist` (with `embed_methodauth`) · `sendtosigner` (`skip_email: 1`) · the EMBED iframe (client-side) · a webhook (server-side)
