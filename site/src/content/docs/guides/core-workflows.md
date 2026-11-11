---
title: Core Workflows
description: Register signers, send for signature, and manage documents end to end.
---

Continuing from [Getting Started](/d4sign-api/guides/getting-started/): once you upload a document into a safe, these are the requests you'll use most. Full parameter lists live in the [API Reference](/d4sign-api/reference/).

## Register signers

```http
POST https://secure.d4sign.com.br/api/v1/documents/{uuid_document}/createlist
Content-Type: application/json

{
  "signers": [
    {
      "email": "signer1@example.com",
      "act": "1",
      "foreign": "0",
      "certificadoicpbr": "0",
      "assinatura_presencial": "0",
      "embed_methodauth": "email",
      "embed_smsnumber": ""
    },
    {
      "email": "signer2@example.com",
      "act": "1",
      "foreign": "0",
      "certificadoicpbr": "0",
      "assinatura_presencial": "0",
      "embed_methodauth": "sms",
      "embed_smsnumber": "+5511953020202"
    }
  ]
}
```

```php
$signers = [
    ['email' => 'signer1@example.com', 'act' => '1', 'foreign' => '0', 'certificadoicpbr' => '0', 'assinatura_presencial' => '0', 'embed_methodauth' => 'email', 'embed_smsnumber' => ''],
    ['email' => 'signer2@example.com', 'act' => '1', 'foreign' => '0', 'certificadoicpbr' => '0', 'assinatura_presencial' => '0', 'embed_methodauth' => 'sms', 'embed_smsnumber' => '+5511953020202'],
];

$client->documents->createList('{uuid_document}', $signers);
```

`act` sets what the signer does. The common ones are `1` sign, `2` approve, `3` acknowledge, `5` witness. D4Sign supports 13 values in total (sign as party, guarantor, etc.) — see the [reference](/d4sign-api/reference/operations/documentssignatoriescreate/) for the full list, plus options for ICP-Brasil certificates, document+selfie auth, PIX auth, and D4Sign Score.

To put several signers in the same signing group instead of listing each one, look up an existing group's UUID:

```php
$groups = $client->groups->find('{uuid_safe}'); // GET /groups/{uuid_safe}
```

then pass its `uuid_grupo` in the signer payload above.

## Send for signature

Moves the document into the "Awaiting Signatures" phase.

```http
POST https://secure.d4sign.com.br/api/v1/documents/{uuid_document}/sendtosigner
Content-Type: application/json

{
  "message": "Please sign the attached contract.",
  "workflow": "0",
  "skip_email": "1"
}
```

- `workflow: 0` — everyone can sign at the same time.
- `skip_email: 1` — don't send the default signing-link email, typically because you're using EMBED or in-person signing instead.

```php
$client->documents->sendToSigner('{uuid_document}', 'Please sign the attached contract.', $workflow = 0, $skip_email = 1);
```

## Document status

Documents move through numbered phases:

| ID | Phase |
| --- | --- |
| 1 | Processing |
| 2 | Awaiting signers |
| 3 | Awaiting signatures |
| 4 | Finished |
| 5 | Archived |
| 6 | Canceled |

List every document in a given phase with `GET /documents/{id_status}/status`, or every document in a safe with `GET /documents/{uuid_safe}/safe`.

## Cancel, resend, download

```php
$client->documents->cancel('{uuid_document}');
$client->documents->resend('{uuid_document}', 'signer@example.com'); // resend the signing link
$url = $client->documents->getfileurl('{uuid_document}', 'zip'); // or 'pdf'
```

Resend is rate-limited per signer: 1st resend after 1 minute, 2nd after 5 minutes, 3rd after 30 minutes, then every 60 minutes.

## Batching documents

Group up to 25 already-uploaded documents into a single batch: `POST /batches` with their UUIDs in `keys`. This is useful for operations that work on a set of documents at once.

## List users

```http
GET https://secure.d4sign.com.br/api/v1/users/list?tokenAPI={tokenAPI}&cryptKey={cryptKey}&pg=1
```

Paginated with `pg`. See [Users](/d4sign-api/reference/) in the reference for `check`, `block`, and `unblock`.

:::note[Gotchas]
- Always send `tokenAPI` and `cryptKey` — see [Authentication](/d4sign-api/guides/authentication/).
- `skip_email` must be `1` when using EMBED or in-person signing (`assinatura_presencial`).
- Uploads and some document operations run in the background. Poll, or use a [webhook](/d4sign-api/guides/webhooks/), instead of assuming immediate completion.
:::
