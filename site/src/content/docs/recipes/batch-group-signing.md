---
title: "Recipe: Send Multiple Documents to the Same Group of Signers"
description: Batch several documents together and route them all to a signing group in one shot.
---

Use this when the same set of people must sign several unrelated documents. Examples: payroll for a whole team, or a stack of NDAs for the same two counterparties. It replaces running the single-document flow N times.

## 1. Look up the signing group

You create groups in the dashboard, not via the API — this just resolves the UUID of one you've already set up.

```php
$groups = $client->groups->find('{uuid_safe}'); // GET /groups/{uuid_safe}
// each entry: { uuid_grupo, nome }
```

## 2. Upload each document and register the group as signer

```php
$uuids = [];
foreach ($files as $path) {
    $uuids[] = $client->documents->upload('{uuid_safe}', $path)->uuid;
}

foreach ($uuids as $uuid_document) {
    $client->documents->createList($uuid_document, [
        ['act' => '1', 'foreign' => '0', 'certificadoicpbr' => '0', 'assinatura_presencial' => '0', 'uuid_grupo' => $uuid_grupo],
    ]);
    $client->documents->sendToSigner($uuid_document, 'Please review and sign.', $workflow = 0, $skip_email = 0);
}
```

Every member of the group gets added as a signer on every document — no need to list individual emails.

## 3. Batch them for operations that act on a set

```php
$batch = $client->request('/batches', 'POST', ['keys' => json_encode($uuids)], 200);
// { message, uuid_batches, total }
```

:::caution
The `Batches`/`batches` service class exists in the SDK's source, but `Client` never wires it in — `$client->batches` doesn't exist. `$client->request()` (shown above) is the `ClientBase` method every generated service method calls internally. It is public, so you can call it the same way for anything the SDK hasn't gotten around to wrapping. See [Using the PHP SDK](/d4sign-api/sdk/php/) for other gaps.
:::

Max 25 documents per batch.

## 4. Optional: embed the whole batch as one package

```html
<script>
  var key = "<?= $batch->uuid_batches ?>";
  var host = "https://secure.d4sign.com.br/embedlote/viewblob"; // note: embedlote, not embed
  // same container/signer_* params as single-document EMBED
</script>
```

See [Embedding the Signing UI](/d4sign-api/guides/embed/#batches) for the full batch iframe snippet.

## What this combines

`groups` (find) · `upload` ×N · `createlist` (`uuid_grupo`) ×N · `sendtosigner` ×N · `batches` (create) · EMBED (batch variant)
