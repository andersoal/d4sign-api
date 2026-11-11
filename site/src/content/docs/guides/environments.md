---
title: Environments
description: Production vs. Sandbox endpoints and their legal validity.
---

| Environment | Endpoint | Legal validity |
| --- | --- | --- |
| Production | `https://secure.d4sign.com.br/api/v1` | Yes |
| Development / Sandbox | `https://sandbox.d4sign.com.br/api/v1` | No |

Signatures collected in **Sandbox** have no legal validity — it exists purely for integration testing. `tokenAPI`/`cryptKey` pairs are environment-specific; a Sandbox token does not work against Production and vice versa.

:::danger[Endpoints are case-sensitive]
Paths must match the documentation exactly — most are `lowercase`. Getting the case wrong can make the API answer `200` with no useful payload instead of a clear error, which is a confusing way to lose an afternoon.
:::

:::note
Documents created inside a folder or subfolder may not show up when you list documents at a parent level. Query the folder directly ([`documents/{uuid_safe}/safe/{uuid_folder}`](/d4sign-api/reference/)) if a document seems to be missing.
:::
