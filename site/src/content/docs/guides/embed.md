---
title: Embedding the Signing UI (EMBED)
description: Show D4Sign's signing flow inside your own website via an iframe.
---

EMBED is D4Sign's front-end component: it shows the signing flow inside an iframe on your own site, so the signer never leaves your domain. It's step 5 from [Getting Started](/d4sign-api/guides/getting-started/) — optional, and separate from the REST API calls that cover steps 1–4.

:::caution
EMBED must be activated on your account first — contact suporte@d4sign.com.br.
:::

The document must already be in the **Awaiting Signatures** phase (sent via [`sendtosigner`](/d4sign-api/guides/core-workflows/) with `skip_email: 1`, since there's no need for an email link when the signer is right there in your UI). A document still in **Awaiting Signers** won't render.

## Single document

```html
<div id="signature-div"></div>
<script>
  var key = "{UUID-DOCUMENTO}"; // required
  var host = "https://secure.d4sign.com.br/embed/viewblob"; // required
  var container = "signature-div"; // required — DOM id of the div above
  var signer_email = "signer@example.com"; // required
  var signer_display_name = ""; // optional — pre-fills name, skips asking the signer
  var signer_documentation = ""; // optional — pre-fills CPF
  var signer_birthday = ""; // optional, format dd/mm/yyyy
  var signer_disable_preview = "0"; // "1" hides the document preview (used for hash-based signing)
  var signer_key_signer = ""; // optional — needed if the same signer appears more than once in the document
  var width = "1025";
  var height = "500";

  var src = host + "/" + key +
    "?email=" + signer_email +
    "&display_name=" + signer_display_name +
    "&documentation=" + signer_documentation +
    "&birthday=" + signer_birthday +
    "&disable_preview=" + signer_disable_preview;
  if (signer_key_signer !== "") src += "&key_signer=" + signer_key_signer;

  var iframe = document.createElement("iframe");
  iframe.setAttribute("src", src);
  iframe.setAttribute("width", width);
  iframe.setAttribute("height", height);
  iframe.setAttribute("allow", "geolocation");
  iframe.style.border = 0;
  document.getElementById(container).appendChild(iframe);

  window.addEventListener("message", function (event) {
    if (event.data === "signed") {
      // document was signed — refresh your UI or redirect
    }
    if (event.data === "wrong-data") {
      // signer said their pre-filled data is wrong — send them to fix it
    }
  });
</script>
```

| Parameter | Required | Purpose |
| --- | --- | --- |
| `key` | Yes | UUID of the document to display. |
| `host` | Yes | `https://secure.d4sign.com.br/embed/viewblob`. |
| `container` | Yes | DOM id of the `<div>` that receives the iframe. |
| `signer_email` | Yes | Signer's email. |
| `signer_display_name` | No | Pre-fills the signer's name. |
| `signer_documentation` | No | Pre-fills the signer's CPF. |
| `signer_birthday` | No | `dd/mm/yyyy`. |
| `signer_disable_preview` | No | `1` hides document previews. |
| `signer_key_signer` | No | Disambiguates a signer listed more than once in the document. |

The `message` event fires `"signed"` or `"wrong-data"` — handle both.

## Batches

To embed a whole [batch](/d4sign-api/guides/core-workflows/#batching-documents) instead of one document: create it first with `POST /batches`, then use the same snippet with two changes — `key` is the batch's `uuid_batches`, and `host` is `https://secure.d4sign.com.br/embedlote/viewblob`. Every other parameter stays the same.

## SSO (SAML 2.0)

Separate feature, unrelated to the REST API this repo documents — D4Sign supports SAML 2.0 single sign-on via Azure AD or Google Workspace for logging into the D4Sign dashboard itself, not for signing. See D4Sign's own guide: [Introdução ao SSO](https://docapi.d4sign.com.br/docs/introdução-ao-sso).
