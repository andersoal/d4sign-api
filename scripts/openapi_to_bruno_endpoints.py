#!/usr/bin/env python3
"""Extract a Bruno-scaffold endpoints.json from openapi/d4sign.yaml.

Feeds the bruno-collection-generator skill's scaffold_opencollection.py, which
turns this JSON array into OpenCollection YAML request files. Keeping this as
a separate, re-runnable step is the point: when D4Sign's API changes, update
the OpenAPI spec and rerun both scripts instead of hand-editing the collection.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

HTTP_METHODS = ("get", "post", "put", "patch", "delete", "options", "head")

# Hand-authored Bruno test scripts for specific operations, keyed by (method, bruno_path).
# Kept here (not per-request) so they survive regeneration. Add to this as you verify more
# response shapes live — see docs/TESTING.md.
TESTS: dict[tuple[str, str], str] = {
    ("GET", "/api/v1/safes"): (
        "test('responds with a documented shape even on auth failure', function () {\n"
        "  const body = res.getBody();\n"
        "  if (res.getStatus() === 200) {\n"
        "    expect(body).to.be.an('array');\n"
        "  } else {\n"
        "    // D4Sign's error envelope: confirmed live as {message, mensagem_pt} for 401 —\n"
        "    // see guides/rate-limits-and-errors.md.\n"
        "    expect(body).to.have.property('message');\n"
        "  }\n"
        "});"
    ),
}


def example_for_schema(schema: dict):
    if not isinstance(schema, dict):
        return ""
    if "example" in schema:
        return schema["example"]
    if schema.get("type") == "object":
        props = schema.get("properties", {})
        return {k: example_for_schema(v) for k, v in props.items()}
    if schema.get("type") == "array":
        return [example_for_schema(schema.get("items", {}))]
    if schema.get("format") == "binary":
        return "@file(./example.pdf)"
    return schema.get("default", "")


def build_body(request_body: dict):
    if not request_body:
        return None, None
    content = request_body.get("content", {})
    if "application/json" in content:
        media = content["application/json"]
        body = media.get("example")
        if body is None:
            body = example_for_schema(media.get("schema", {}))
        return body, "json"
    if "multipart/form-data" in content:
        media = content["multipart/form-data"]
        example = media.get("example")
        if example is None:
            example = example_for_schema(media.get("schema", {}))
        if not isinstance(example, dict):
            example = {}
        schema_props = media.get("schema", {}).get("properties", {})
        for name, prop in schema_props.items():
            if prop.get("format") == "binary" and name not in example:
                example[name] = "@file(./example.pdf)"
        # Bruno's multipart-form body is "name: value" lines, not a dict blob.
        lines = "\n".join(f"{k}: {v}" for k, v in example.items())
        return lines, "multipart-form"
    return None, None


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <openapi.yaml> <endpoints.json>", file=sys.stderr)
        return 2
    spec_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))

    endpoints = []
    for path, path_item in (spec.get("paths") or {}).items():
        shared_params = path_item.get("parameters", []) or []
        for method, op in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(op, dict):
                continue
            params = shared_params + (op.get("parameters", []) or [])
            path_params = []
            query_params = [
                {"name": "tokenAPI", "value": "{{tokenAPI}}"},
                {"name": "cryptKey", "value": "{{cryptKey}}"},
            ]
            # tokenAPI header + Accept are inherited from collections/bruno/opencollection.yml's
            # collection-root `request.headers` — only genuinely per-operation headers go here.
            headers = []
            for p in params:
                name = p.get("name")
                if not name or name in ("tokenAPI", "cryptKey"):
                    continue
                example = p.get("example", f"{{{{{name}}}}}")
                location = p.get("in")
                if location == "path":
                    path_params.append({"name": name, "value": example})
                elif location == "query":
                    query_params.append({"name": name, "value": example})
                elif location == "header":
                    headers.append({"name": name, "value": example})

            body, body_type = build_body(op.get("requestBody"))

            tags = op.get("tags") or ["uncategorized"]
            description = (op.get("description") or "").strip()
            # Bruno uses :name for path params, not OpenAPI's {name}.
            bruno_path = path.replace("{", ":").replace("}", "")
            # Bruno Desktop derives each query param's enabled checkbox from whether it's
            # present in the URL text itself, not from the separate `params:` list alone —
            # a request with params but no matching query string in `url` loads with every
            # param showing as unchecked until you manually re-toggle it. Embed the query
            # string in both places, matching what Bruno itself writes back after that.
            query_string = "&".join(f"{p['name']}={p['value']}" for p in query_params)
            endpoint = {
                "name": op.get("summary") or f"{method.upper()} {path}",
                "method": method.upper(),
                "path": f"{bruno_path}?{query_string}",
                "folder": tags[0],
                "tags": tags,
                "path_params": path_params,
                "query": query_params,
                "headers": headers,
                "docs": description or f"{op.get('summary', '')} ({method.upper()} {path})",
            }
            if body is not None:
                endpoint["body"] = body
                endpoint["body_type"] = body_type
            tests = TESTS.get((method.upper(), bruno_path))
            if tests:
                endpoint["tests"] = tests
            endpoints.append(endpoint)

    out_path.write_text(json.dumps(endpoints, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(endpoints)} endpoint(s) to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
