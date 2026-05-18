# tia-knowledge — CLAUDE.md

## Purpose

Living knowledge base for the **AleFire-Library** — a Siemens TIA Portal V20 global library
of function blocks and UDTs for pneumatic field devices (valves, diverters, filters, etc.).

Two outputs on every update cycle:

| Output | Consumer |
|--------|----------|
| `docs/` — bilingual MkDocs pages (IT primary, EN) | Engineers reading the wiki |
| `dist/library_manifest.json` — structured JSON of all UDTs + FBs | tia-automation |

**AleFire-Library:** `C:\Users\user015\Desktop\Projects\Libreria software\AleFire-Library\AleFire-Library.al20`
**Staging project:** `Library_export/Library_export.ap20` — one PLC, library types manually instantiated.

---

## Repository Layout

```
tia-knowledge/
├── sources/                     ← git-tracked SCL/UDT exports from TIA Portal
│   ├── FBs/                     ← .scl function blocks (99 - Library/Objects/...)
│   ├── UDTs/                    ← .udt data types
│   └── FCs/
├── scripts/
│   ├── export.py                ← TIA Portal → sources/ (requires TIA Portal open)
│   └── generate_docs.py         ← sources/ → docs/ + dist/manifest.json (offline)
├── docs/                        ← MkDocs bilingual pages
│   └── library/
│       ├── valves/
│       ├── diverters/
│       ├── filters/
│       ├── gate/
│       ├── nolvac/
│       └── load-cells/
├── dist/
│   └── library_manifest.json    ← schema contract consumed by tia-automation
├── Library_export/              ← gitignored TIA staging project
├── mkdocs.yml
├── config.py                    ← path constants
└── config.toml                  ← TIA paths + manifest sim_overrides
```

---

## Python Environment

- Python **3.12.x strictly** — siemens_tia_scripting is cp312 only
- Package manager: `uv`
- Wheel: `C:\Users\user015\Documents\109742322_TIA_Scripting_Python_CODE_V1_2_1\install\siemens_tia_scripting-1.2.1-cp312-cp312-win_amd64.whl`

---

## Update Workflow

```bash
# Step 1: export (requires TIA Portal, Library_export project open)
uv run python scripts/export.py

# Step 2: generate manifest + regenerate doc sections 7-8 (offline)
uv run python scripts/generate_docs.py

# Step 3: preview
mkdocs serve

# Step 4: commit
git add sources/ dist/ docs/
git commit -m "chore: update library sources and docs"
```

After export: **remove all user blocks from staging project** before committing.

---

## MkDocs Setup

- Theme: `mkdocs-material` (red/amber, dark mode toggle)
- Plugins: `awesome-pages`, `search`, `mermaid2`, `i18n` (mkdocs-static-i18n)
- Italian = primary/default language; English = secondary
- Build output: `site/` (gitignored)
- `mkdocs serve` from repo root (not from `docs/`)

## Bilingual Structure

`mkdocs-static-i18n` uses **suffix** pattern.

- Always create both `index.it.md` and `index.en.md` when adding a module page
- Italian: primary, full content — written first
- English: full translation — never a stub

## Module Page Format — 8 sections

**Sections 1–6: human-maintained.** `generate_docs.py` never modifies these.
**Sections 7–8: auto-generated** (Mermaid classDiagram + stateDiagram-v2). Overwritten on each run.

```
1. Overview
2. Main Components
3. I/O Signals
4. Operating Routine
5. Alarms
6. Settings
7. Data Structure      ← AUTO-GENERATED: do not edit manually
8. State Machine       ← AUTO-GENERATED: do not edit manually
```

---

## dist/library_manifest.json — Schema Contract

Produced here; consumed by tia-automation's `pipeline/resolve.py`.
**Never remove or rename fields. Bump `manifest_version` on structural changes.**

```json
{
  "manifest_version": "1.0.0",
  "udts": {
    "UDT_SS_Valve": {
      "has_out": false,
      "devices": { "ZSL": {"type": "Bool"}, "ZSH": {"type": "Bool"}, "XY": {"type": "UDT_Solenoid_valve"} }
    }
  },
  "fbs": {
    "UDT_SS_Valve": {
      "ctrl": {"name": "SS_Butterfly_valve", "param": "XV"},
      "sim":  {"name": "SS_valve_simulator",  "param": "XV"}
    }
  }
}
```

---

## AleFire-Library Device Types

| UDT | Controlling FB | VAR_IN_OUT param | Sim FB |
|-----|----------------|------------------|--------|
| UDT_SS_Valve | SS_Butterfly_valve | XV | SS_valve_simulator |
| UDT_DS_Valve | DS_Butterfly_valve | XV | DS_valve_simulator |
| UDT_Pinch_Valve | Pinch_valve | XV | Pinch_valve_simulator |
| UDT_Solenoid_valve | Solenoid_valve | XY | — |
| UDT_Gate_Door | Gate_door | gate_door | Gate_door_sim |
| UDT_Pinch_diverter | Pinch_diverter | DIV | Pinch_diverter_simulator |
| UDT_PTD_IO | Plug_Type_Diverter | ptd_Diverter | — |
| UDT_Filter_1_sleeve | Filter_1_sleeve | filter | — |
| UDT_Filter_2_sleeves | Filter_2_sleeves | filter | — |
| UDT_Load_cells | Load_cells | batch | — |
| UDT_Nolvac | Nolvac | VC | — |

Simulator FBs for SS/DS/Pinch valves and Pinch_diverter are LAD blocks — declared in
`config.toml` as `[[manifest.sim_overrides]]`.

---

## Known Gotchas — TIA Portal V20 / siemens_tia_scripting v1.2.1

1. `LibraryTypeVersion.export()` is **blocked** for global library types via API.
   Workaround: use staging project + `block.export()`.
2. `version.instantiate()` throws `NullReferenceException` for all AleFire-Library types
   when called on a GlobalLibrary proxy. Use `--skip-instantiate` and instantiate manually
   in TIA Portal UI, then re-run.
3. Staging project must be committed in **empty state** between export runs.

---

## Writing Style (Karpathy wiki)

- Prose first. Tables only for reference data.
- Never "This block is responsible for..." — say what it does directly.
- Every behavioral claim verifiable from SCL source.
- No passive voice. No corporate language.

---

## Git Flow

| Branch | Purpose |
|--------|---------|
| `main` | Released state — merge from `release/*` or `hotfix/*` only |
| `develop` | Integration — feature branches merge here |
| `feature/<name>` | One per feature, branched from `develop` |

Never commit directly to `main`.
