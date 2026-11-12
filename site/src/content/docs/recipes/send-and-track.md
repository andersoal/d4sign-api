---
title: "Recipe: Upload, Send, and React to Completion"
description: The most common end-to-end flow — upload a document, collect signatures, and get notified when it's done.
---

This is the default path from "I have a PDF" to "it is signed and I have the final file." It combines [Documents](/d4sign-api/guides/core-workflows/), [Webhooks](/d4sign-api/guides/webhooks/), and download. Each step links to the full parameter list instead of repeating it here.

## 1. Upload the document

```php
$client = new D4sign\Client();
$client->setAccessToken('{tokenAPI}');
$client->setCryptKey('{cryptKey}');

$uuid_document = $client->documents->upload('{uuid_safe}', '/path/to/contract.pdf')->uuid;
```

See [Getting Started](/d4sign-api/guides/getting-started/) for the raw HTTP form.

## 2. Register a webhook once, at the safe (not per document)

Do this once per safe, not per document. This webhook then covers every document you upload into that safe, from then on.

```http
POST https://secure.d4sign.com.br/api/v1/webhooks/v2/

{ "type": "cofre", "uuid": "{uuid_safe}", "url": "https://yourdomain.com/d4sign/webhook" }
```

See [Webhooks](/d4sign-api/guides/webhooks/) for the v1-vs-v2.0 distinction, retry schedule, and HMAC verification — verify the signature before trusting any payload your endpoint receives in step 4.

## 3. Add signers and send

```php
$client->documents->createList($uuid_document, [
    ['email' => 'signer@example.com', 'act' => '1', 'foreign' => '0', 'certificadoicpbr' => '0', 'assinatura_presencial' => '0'],
]);

$client->documents->sendToSigner($uuid_document, 'Please sign the attached contract.', $workflow = 0, $skip_email = 0);
```

Full signer field list (ICP-Brasil certs, PIX auth, D4Sign Score, ...) in [Core Workflows](/d4sign-api/guides/core-workflows/#register-signers).

## 4. Handle the webhook — don't poll

Your endpoint receives a `POST` when the document is signed, finished, or canceled (`type_post` `1`/`3`/`4`). Verify the `Content-Hmac` header before acting on it:

```php
// $secret = your account's webhook secret key
$expected = 'sha256=' . hash_hmac('sha256', $_POST['uuid'], $secret);
if (!hash_equals($expected, $_SERVER['HTTP_CONTENT_HMAC'] ?? '')) {
    http_response_code(401);
    exit;
}

if ($_POST['type_post'] === '1') { // Finished
    // fetch the final files — see step 5
}
```

## 5. Download the finished files

```php
$url = $client->documents->getfileurl($uuid_document, 'zip')->url; // or 'pdf', 'pdfa'
```

Only works once the document is actually finished — see the [status table](/d4sign-api/guides/core-workflows/#document-status). For attachments + signature certificates together, use `downloadlist` instead (see the [reference](/d4sign-api/reference/operations/documents_download_batch/)).

## What this combines

`upload` · `webhooks/v2` (register) · `createlist` · `sendtosigner` · webhook callback (your own endpoint) · `getfileurl`/`downloadlist`
