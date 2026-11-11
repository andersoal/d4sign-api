# D4Sign API — unofficial docs, PHP SDK, and Bruno collection

This repository is three things, all generated from the same [`openapi/d4sign.yaml`](openapi/d4sign.yaml) spec:

1. **[Documentation site](https://andersoal.github.io/d4sign-api/)** (`site/`) — guide + full API reference, built with [Astro Starlight](https://starlight.astro.build/). Unofficial, not produced or endorsed by D4Sign; see the official docs at [docapi.d4sign.com.br](https://docapi.d4sign.com.br/docs).
2. **PHP SDK** (`sdk/php/`) — the original D4Sign PHP client. See [the SDK guide](https://andersoal.github.io/d4sign-api/sdk/php/) or [`sdk/php/README.md`](sdk/php/README.md).
3. **Bruno collection** (`collections/bruno/`) — every endpoint, ready to run. See [`collections/bruno/README.md`](collections/bruno/README.md).

Credentials for testing against the live API (Sandbox or Production) are managed with [mise](https://mise.jdx.dev/) and shared between your shell, the Bruno GUI, and the Bruno CLI — see [`docs/TESTING.md`](docs/TESTING.md).

There's also a [`skill/d4sign-docs/SKILL.md`](skill/d4sign-docs/SKILL.md) packaging the same knowledge for AI coding agents.

## Repository layout

```
openapi/d4sign.yaml     OpenAPI 3.1 spec — single source of truth
site/                   Starlight docs site (guide + generated reference)
sdk/php/                 PHP SDK (composer package)
collections/bruno/       Bruno/OpenCollection API collection
skill/d4sign-docs/       Claude Skill packaging of the same docs
scripts/                 openapi -> Bruno endpoint-list converter
docs/REGENERATING.md     How to regenerate the reference + Bruno collection
docs/TESTING.md          How to test against the real API (mise + Bruno)
docs/COVERAGE.md         Audit of this repo's docs against the live docapi.d4sign.com.br
mise.toml                Shared tokenAPI/cryptKey/baseUrl env vars (see docs/TESTING.md)
```

## Related projects

Other unofficial D4Sign integrations worth knowing about:

- [d4sign-tech/n8n-integration-node](https://github.com/d4sign-tech/n8n-integration-node) — D4Sign node for [n8n](https://n8n.io/) workflow automation.
- [gabrielalmir/d4sign-node](https://github.com/gabrielalmir/d4sign-node) — Node.js/TypeScript client for the D4Sign API.
- [edmarr2/d4sign-laravel](https://github.com/edmarr2/d4sign-laravel) — Laravel package for consuming the D4Sign API.

## Developing the site locally

```bash
cd site
npm install
npm run dev
```

## License

MIT — see [LICENSE](LICENSE). D4Sign's own documentation and OpenAPI spec are their intellectual property; this repo adapts and reorganizes them for integration purposes.
