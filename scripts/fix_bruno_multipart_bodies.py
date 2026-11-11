#!/usr/bin/env python3
"""Fix multipart-form request bodies in the generated Bruno collection.

The bruno-collection-generator skill's scaffold script only knows how to
write body.data as a text block scalar. That's wrong for multipart-form (and
form-urlencoded): Bruno's OpenCollection YAML format requires body.data to be
a LIST of {name, value, type?} entries (confirmed against
@usebruno/filestore's yml body parser) — a plain string makes `bru run` fail
with "e.data?.map is not a function" on every such request.

Run this after scripts/openapi_to_bruno_endpoints.py + the skill's
scaffold_opencollection.py, as the last step of collection generation.
"""
from __future__ import annotations

import io
from pathlib import Path

import yaml as pyyaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "openapi" / "d4sign.yaml"
REQUESTS_DIR = ROOT / "collections" / "bruno" / "requests"


def load_multipart_schemas() -> dict[tuple[str, str], dict]:
    spec = pyyaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))
    out = {}
    for path, item in spec["paths"].items():
        bruno_path = path.replace("{", ":").replace("}", "")
        for method, op in item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            rb = op.get("requestBody") or {}
            media = (rb.get("content") or {}).get("multipart/form-data")
            if media:
                out[(method.upper(), bruno_path)] = media.get("schema", {}).get("properties", {})
    return out


def entries_for(props: dict) -> CommentedSeq:
    seq = CommentedSeq()
    for name, prop in props.items():
        entry = CommentedMap()
        entry["name"] = name
        if prop.get("format") == "binary":
            entry["type"] = "file"
            value = CommentedSeq(["./example.pdf"])
            value.fa.set_flow_style()
            entry["value"] = value
        else:
            entry["value"] = str(prop.get("example", ""))
        seq.append(entry)
    return seq


def main() -> int:
    schemas = load_multipart_schemas()
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096

    fixed = 0
    for file_path in REQUESTS_DIR.rglob("*.yml"):
        data = yaml.load(io.StringIO(file_path.read_text(encoding="utf-8")))
        body = data.get("http", {}).get("body")
        if not body or body.get("type") != "multipart-form" or not isinstance(body.get("data"), str):
            continue

        method = data["http"]["method"]
        url_path = data["http"]["url"].split("}}", 1)[-1].split("?", 1)[0]  # strip "{{baseUrl}}" and the query string
        props = schemas.get((method, url_path))
        if props is None:
            print(f"warn: no multipart schema found for {method} {url_path} ({file_path.name}) — leaving as-is")
            continue

        body["data"] = entries_for(props)
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            yaml.dump(data, f)
        fixed += 1
        print(f"fixed {file_path.relative_to(ROOT)}")

    print(f"Fixed {fixed} multipart-form request body/bodies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
