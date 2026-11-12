# Scenarios

The `requests/` collection is one request per endpoint — it mirrors `openapi/d4sign.yaml` 1:1 and gets regenerated from it (see `../../../docs/REGENERATING.md`). It does not encode *order*.

This folder is the other axis: each subfolder is a runnable Bruno version of one recipe from `site/src/content/docs/recipes/`, with the requests numbered in the order the recipe describes and chained with `runtime.scripts` (`after-response` scripts call `bru.setVar(...)` so the next step's `{{uuid_document}}`, `{{template_id}}`, etc. come from the previous response instead of being typed in by hand).

These files are hand-written. Regenerating the main collection does not touch this folder, and never will — it isn't part of `scripts/openapi_to_bruno_endpoints.py`'s output.

| Folder | Recipe | Chains |
| --- | --- | --- |
| `send-and-track/` | [Upload, Send, and React to Completion](../../../site/src/content/docs/recipes/send-and-track.md) | `uuid_document` |
| `template-to-signature/` | [Generate a Document from a Template and Send It](../../../site/src/content/docs/recipes/template-to-signature.md) | `template_id` → `uuid_document` |
| `batch-group-signing/` | [Send Multiple Documents to the Same Group of Signers](../../../site/src/content/docs/recipes/batch-group-signing.md) | `uuid_grupo`, `uuid_document_1`/`uuid_document_2` → `uuid_batches` |
| `embed-in-your-site/` | [Collect a Signature Without Leaving Your Site](../../../site/src/content/docs/recipes/embed-in-your-site.md) | `uuid_document` |

A step that can't be an HTTP request at all (the client-side EMBED iframe, your own server-side webhook endpoint) is noted in that step's `docs:` instead of skipped silently.

## Running a scenario

```bash
cd collections/bruno
bru run scenarios/send-and-track -r --env Sandbox \
  --env-var tokenAPI=$tokenAPI --env-var cryptKey=$cryptKey \
  --env-var uuid_safe=<your-safe-uuid>
```

Set `uuid_safe` yourself first (`--env-var`, or as a runtime var in the Bruno GUI) — every scenario needs it and nothing can derive it for you. `template-to-signature/` has one extra wrinkle: run either `02-make-document-by-template-html.yml` or `02-alt-make-document-by-template-word.yml`, never both in the same pass (each overwrites `uuid_document`); the `-alt` file has `seq: 99` so a plain recursive run leaves it for last, out of the way.

Multipart upload steps still point at the placeholder `./example.pdf` — same known gap as `requests/`, see `../README.md`.
