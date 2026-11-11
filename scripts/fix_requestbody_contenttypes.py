#!/usr/bin/env python3
"""One-off fix: a few operations in openapi/d4sign.yaml were exported with
`multipart/form-data` requestBody content-types even though they're plain
JSON per D4Sign's own docs (confirmed against docapi.d4sign.com.br guide
pages) — and one (a GET) had a vestigial empty requestBody at all. This
surfaced as broken multipart-form bodies when generating the Bruno
collection (the real multipart-form shape is a list of entries, not a
string — see scripts/openapi_to_bruno_endpoints.py). Run once.
"""
from __future__ import annotations

import io
from pathlib import Path

from ruamel.yaml import YAML

SPEC_PATH = Path(__file__).resolve().parent.parent / "openapi" / "d4sign.yaml"

RETYPE_TO_JSON = [
    ("post", "/api/v1/documents/{uuid_document}/resend"),
    ("post", "/api/v1/documents/{uuid_document}/webhooks"),
]
DROP_REQUEST_BODY = [
    ("get", "/api/v1/documents/{uuid_document}/webhooks"),
]


def main() -> int:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    spec = yaml.load(io.StringIO(SPEC_PATH.read_text(encoding="utf-8")))

    for method, path in RETYPE_TO_JSON:
        content = spec["paths"][path][method]["requestBody"]["content"]
        content["application/json"] = content.pop("multipart/form-data")
        print(f"retyped {method.upper()} {path} -> application/json")

    for method, path in DROP_REQUEST_BODY:
        op = spec["paths"][path][method]
        if "requestBody" in op:
            del op["requestBody"]
            print(f"dropped empty requestBody on {method.upper()} {path}")

    with open(SPEC_PATH, "w", encoding="utf-8", newline="\n") as f:
        yaml.dump(spec, f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
