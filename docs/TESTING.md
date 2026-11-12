# Testing against the real D4Sign API

This repo uses [mise](https://mise.jdx.dev/) to manage `tokenAPI`/`cryptKey`/`baseUrl` as shell environment variables. A plain terminal, the [Bruno](https://www.usebruno.com/) GUI, and the Bruno CLI (`bru`) all share these same variables. You set credentials in one place and use them in several ways.

## One-time setup

1. Install mise (already done if you ran `irm https://mise.run/powershell | iex`).
2. **Activate mise in PowerShell** so env vars load automatically when you `cd` into a directory with a `mise.toml` (this repo has one):

   ```powershell
   Add-Content -Path $PROFILE -Value "`nmise activate pwsh | Out-String | Invoke-Expression"
   ```

   Restart your terminal (or `. $PROFILE`) after this.
3. From inside this repo, trust its config once:

   ```powershell
   mise trust
   ```
4. Set your real credentials — they go in `mise.local.toml`, which is gitignored and never committed (`mise.toml`, the non-secret defaults, *is* committed):

   ```powershell
   mise set --file mise.local.toml tokenAPI=<your-token>
   mise set --file mise.local.toml cryptKey=<your-crypt-key>
   ```

   See `mise.local.toml.example` for the file shape if you'd rather edit it by hand.

After this, any new PowerShell session opened inside this repo has `$env:tokenAPI`, `$env:cryptKey`, and `$env:baseUrl` (defaults to Sandbox — see `mise.toml`) set automatically. Run `mise env` any time to check what's loaded, or `mise doctor` to debug activation.

## Running requests

**Bruno GUI** — open `collections/bruno/` as a collection, pick the `Sandbox` or `Production` environment, and set `tokenAPI`/`cryptKey` as environment secrets. This is Bruno's own encrypted store, separate from mise, but you can paste in the same values that `mise env --values` prints.

Alternative that skips re-entering secrets into Bruno entirely: **launch Bruno Desktop from a mise-activated PowerShell session.** `cd` into this repo first, then run `bruno`, not a pinned shortcut. A shortcut launched from Explorer never sees mise's env vars. Bruno resolves `{{process.env.tokenAPI}}`/`{{process.env.cryptKey}}` from its own OS process environment. Because of this, any field can reference those directly instead of `{{tokenAPI}}`. If Bruno was already running before you set this up, quit it and relaunch it from that terminal. An already-running process keeps the environment it had when you launched it.

**Bruno CLI**, from `collections/bruno/`:

```bash
bru run requests -r --env Sandbox --env-var tokenAPI=$tokenAPI --env-var cryptKey=$cryptKey
```

To run a whole recipe as a chained sequence instead of one endpoint at a time, see [`collections/bruno/scenarios/`](../collections/bruno/scenarios/README.md) — same command, pointed at `scenarios/<name>` instead of `requests`, plus `--env-var uuid_safe=...`.

Or the pre-wired mise task (runs just `GET /safes` as a quick smoke test, from the repo root):

```powershell
mise run bruno-smoke
```

**Plain curl/PHP**, anywhere once mise is activated:

```powershell
curl "$env:baseUrl/api/v1/safes?tokenAPI=$env:tokenAPI&cryptKey=$env:cryptKey"
```

A `200` with your real safes back means the request/response shape documented in the [API Reference](../site/src/content/docs/guides/getting-started.md) and the [Bruno collection](../collections/bruno/README.md) matches the live API. A `401` means check the credentials and environment. Sandbox and Production are not interchangeable — see the [Environments guide](../site/src/content/docs/guides/environments.md). A `429` means you have hit the 10-requests/hour rate limit.
