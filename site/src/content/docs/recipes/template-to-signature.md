---
title: "Recipe: Generate a Document from a Template and Send It"
description: Skip the upload step entirely — fill a template and send it straight for signature.
---

Use this for contracts that are mostly boilerplate, with a few fields that change (name, CPF, amount, ...). Generate the document from a template instead of uploading a PDF each time.

## 1. Find the template's ID

```php
$templates = $client->templates->find(); // POST /templates — yes, POST, not GET
// each entry: { id, name, variables: [...] }
```

Copy the `id` of the template you configured in the dashboard, and note its variable names exactly (case-sensitive).

## 2. Generate the document

HTML templates (the SDK's first parameter is named `$documentKey` but is actually the **safe's** UUID — there's no document yet, it's about to be created):

```php
$doc = $client->documents->makedocumentbytemplate('{uuid_safe}', 'Contrato — João', [
    $template_id => [
        'NOME_CLIENTE' => 'João',
        'CPF' => '222.222.222-22',
    ],
]);
```

Word templates — same shape, different endpoint (and supports multiple "preenchedores" filling different sections — see the [reference](/d4sign-api/reference/operations/documents_template_word_create/) for the multi-filler body shape):

```php
$doc = $client->documents->makedocumentbytemplateword('{uuid_safe}', 'Contrato — João', [
    $template_id => [
        'NOME_CLIENTE' => 'João',
        'CPF' => '222.222.222-22',
    ],
]);
```

Either way you get back `{"uuid": "..."}` — the new document, already in the safe, ready for the same [signer + send](/d4sign-api/recipes/send-and-track/#3-add-signers-and-send) steps as an uploaded document.

:::note
Need a template that doesn't exist yet? `POST /templates/upload` creates one from a `.doc`/`.docx` file — see the [reference](/d4sign-api/reference/operations/templates_upload_word/). This is for *creating* a template, not generating a document from one.
:::

## What this combines

`templates->find` · `makeDocumentByTemplate`/`makeDocumentByTemplateWord` · then the same `createlist` + `sendtosigner` as [Upload, Send, and React to Completion](/d4sign-api/recipes/send-and-track/)
