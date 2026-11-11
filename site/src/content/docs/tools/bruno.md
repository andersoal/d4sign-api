---
title: Bruno Collection
description: Run every D4Sign endpoint from a ready-to-import Bruno collection.
---

[`collections/bruno/`](https://github.com/andersoal/d4sign-api/tree/master/collections/bruno) in this repository is a full [Bruno](https://www.usebruno.com/) collection covering every endpoint in the [API Reference](/d4sign-api/reference/), generated from the same [`openapi/d4sign.yaml`](https://github.com/andersoal/d4sign-api/blob/master/openapi/d4sign.yaml) spec that drives this site.

[<img src="https://fetch.usebruno.com/button.svg" alt="Fetch in Bruno" width="128" height="32" />](https://fetch.usebruno.com?url=https%3A%2F%2Fgithub.com%2Fandersoal%2Fd4sign-api.git)

## Open it

```bash
git clone https://github.com/andersoal/d4sign-api.git
```

Open the `collections/bruno/` folder in Bruno, or use the "Fetch in Bruno" button above (requires Bruno installed locally).

1. Select the **Production** or **Sandbox** environment.
2. Set the `tokenAPI` and `cryptKey` secrets for that environment — see [Authentication](/d4sign-api/guides/authentication/). They're declared as secrets, never committed.
3. Run any request under `requests/` — folders match the API's own resource groupings (documents, safes, webhooks, signatories, ...).

:::caution
Multipart upload requests use a placeholder file reference (`@file(./example.pdf)`) — point it at a real file before sending.
:::
