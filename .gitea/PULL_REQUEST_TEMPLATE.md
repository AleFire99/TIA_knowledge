## What changed / why

<!-- What prompted this change — a raw/ re-export, a new device type, a docs
     correction, a schema/tooling change. Link the issue it closes if any. -->

## Checklist

- [ ] `raw/` changes (if any) re-ingested — `dist/library_manifest.json` committed alongside
- [ ] Both `docs/it/` and `docs/en/` updated together (no locale left as a stub)
- [ ] `.fsm.yaml` updated *before* re-rendering, for any FSM section change
- [ ] `uv run zensical build --config-file zensical.it.toml --strict` and the `.en.toml`
      counterpart pass locally
