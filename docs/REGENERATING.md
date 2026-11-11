# Regenerating the reference and the Bruno collection

`openapi/d4sign.yaml` is the single source of truth for both the API Reference pages and the Bruno collection. When D4Sign's API changes, update that file, then:

## API Reference (site)

Nothing to run. `site/` uses the `starlight-openapi` plugin, which reads `openapi/d4sign.yaml` at build/dev time and regenerates the `/reference/` pages automatically.

## Bruno collection

```bash
python scripts/openapi_to_bruno_endpoints.py openapi/d4sign.yaml /tmp/endpoints.json
python "<path-to-bruno-collection-generator-skill>/scripts/scaffold_opencollection.py" \
  --endpoints /tmp/endpoints.json --out collections/bruno --base-url "{{baseUrl}}" --force
python scripts/fix_bruno_multipart_bodies.py
```

1. `openapi_to_bruno_endpoints.py` converts the OpenAPI spec into the flat endpoint-list JSON the second script (from Claude's `bruno-collection-generator` skill) expects.
2. `scaffold_opencollection.py` regenerates every file under `collections/bruno/requests/`. It only knows how to write text-block bodies. That is wrong for `multipart-form` bodies. Bruno's real OpenCollection format needs a list of entries there instead. See `@usebruno/filestore`'s yml body parser if you need to double-check this.
3. `fix_bruno_multipart_bodies.py` rewrites just the `multipart-form` request bodies (file uploads) into the correct list shape, re-deriving them from the spec's schema.

`collections/bruno/opencollection.yml`, `bruno.json`, and `environments/*.yml` are hand-written. This process does not touch them. The collection uses OpenCollection **YAML** format, not classic `.bru`. This is also why the environment files are `.yml`. `bru run` picks its file format (`.bru` vs `.yml`) based only on whether `opencollection.yml` exists at the collection root. It then looks only for environment files with that same extension.

The scaffold script also overwrites `collections/bruno/README.md` with its own generic template — restore the real one with `git checkout -- collections/bruno/README.md` after regenerating.

Review the diff — folder names come from the spec's own `tags`, so a retagged or renamed operation in the spec moves or renames its request file.
