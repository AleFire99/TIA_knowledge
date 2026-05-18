"""
Generate dist/library_manifest.json from sources/.

Usage:
    python scripts/generate_docs.py

Steps:
  1. Parse all .udt files -> UDT name, DEVICES members, has_out flag
  2. Parse all .scl files -> FB name, VAR_IN_OUT param name + UDT type, is_sim flag
  3. Merge LAD sim FB overrides from config.toml [[manifest.sim_overrides]]
  4. Write dist/library_manifest.json atomically (temp -> rename)
  5. Print summary

Sections 7-8 of wiki/docs/ pages are regenerated separately (not yet implemented).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ImportError:
        print("ERROR: tomllib not available. Python >= 3.11 required, or install tomli.")
        sys.exit(1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
import config as cfg

MANIFEST_VERSION = "1.0.0"


def _load_sim_overrides() -> list[dict]:
    toml_path = REPO_ROOT / "config.toml"
    if not toml_path.exists():
        return []
    with toml_path.open("rb") as f:
        data = tomllib.load(f)
    return data.get("manifest", {}).get("sim_overrides", [])


# ---------------------------------------------------------------------------
# UDT parsing
# ---------------------------------------------------------------------------

def _parse_member_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("//"):
        return None
    m = re.match(r'^(\w+)(?:\s*\{[^}]*\})?\s*:\s*(.+)', stripped)
    if not m:
        return None
    rhs = m.group(2).split(';')[0].split('//')[0].strip()
    type_m = re.match(r'"([^"]+)"|(\w+)', rhs)
    if not type_m:
        return None
    raw_type = type_m.group(1) or type_m.group(2)
    if raw_type.lower() == "struct":
        return None
    return m.group(1), raw_type


def parse_udt(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    name_m = re.search(r'^TYPE\s+"([^"]+)"', text, re.MULTILINE)
    name = name_m.group(1) if name_m else path.stem

    # Derive description from parent folder relative to UDTs dir
    try:
        rel_parts = path.relative_to(cfg.UDT_SOURCES).parts
        desc_parts = list(rel_parts[:-1])
    except ValueError:
        desc_parts = []
    description = " / ".join(desc_parts) if desc_parts else ""

    devices: dict[str, dict] = {}
    has_out = False
    depth = 0
    in_devices = False

    for line in lines:
        stripped = line.strip()

        named_struct_m = re.match(
            r'^(\w+)(?:\s*\{[^}]*\})?\s*:\s*Struct\b', stripped, re.IGNORECASE
        )
        if named_struct_m:
            if depth == 1:
                in_devices = (named_struct_m.group(1).upper() == "DEVICES")
            depth += 1
            continue

        if re.match(r'^STRUCT\s*$', stripped, re.IGNORECASE):
            depth += 1
            continue

        if re.match(r'^END_STRUCT\s*;?\s*$', stripped, re.IGNORECASE):
            if depth == 2:
                in_devices = False
            if depth > 0:
                depth -= 1
            continue

        if depth == 1:
            member = _parse_member_line(line)
            if member and member[0].lower() == "out" and member[1].lower() == "bool":
                has_out = True

        elif depth == 2 and in_devices:
            member = _parse_member_line(line)
            if member:
                fname, ftype = member
                comment_m = re.search(r"//\s*(.+)$", line)
                fdesc = comment_m.group(1).strip() if comment_m else ""
                devices[fname] = {"type": ftype, "description": fdesc}

    return {"name": name, "description": description, "has_out": has_out, "devices": devices}


# ---------------------------------------------------------------------------
# SCL / FB parsing
# ---------------------------------------------------------------------------

_SIM_RE = re.compile(r"(sim(ulator)?)", re.IGNORECASE)


def parse_fb(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8-sig")

    fb_m = re.search(r'^FUNCTION_BLOCK\s+"([^"]+)"', text, re.MULTILINE)
    if not fb_m:
        return None
    fb_name = fb_m.group(1)

    var_io_m = re.search(r'\bVAR_IN_OUT\b(.*?)\bEND_VAR\b', text, re.DOTALL)
    if not var_io_m:
        return None

    param_m = re.search(
        r'(\w+)(?:\s*\{[^}]*\})?\s*:\s*"([^"]+)"\s*;', var_io_m.group(1)
    )
    if not param_m:
        return None

    return {
        "name": fb_name,
        "param_name": param_m.group(1),
        "udt_type": param_m.group(2),
        "is_sim": bool(_SIM_RE.search(fb_name)),
    }


# ---------------------------------------------------------------------------
# Manifest assembly
# ---------------------------------------------------------------------------

def build_manifest(udts: list[dict], fbs: list[dict], sim_overrides: list[dict]) -> dict:
    udt_section: dict[str, dict] = {}
    for u in udts:
        udt_section[u["name"]] = {
            "description": u["description"],
            "has_out": u["has_out"],
            "devices": {
                fname: {"type": fd["type"], "description": fd["description"]}
                for fname, fd in u["devices"].items()
            },
        }

    fb_section: dict[str, dict] = {}
    for fb in fbs:
        udt_key = fb["udt_type"]
        if udt_key not in fb_section:
            fb_section[udt_key] = {"ctrl": None, "sim": None}
        entry = {"name": fb["name"], "param": fb["param_name"]}
        if fb["is_sim"]:
            fb_section[udt_key]["sim"] = entry
        else:
            fb_section[udt_key]["ctrl"] = entry

    # Merge LAD sim FBs that won't appear in SCL exports
    for override in sim_overrides:
        udt_key = override["udt"]
        if udt_key not in fb_section:
            fb_section[udt_key] = {"ctrl": None, "sim": None}
        if fb_section[udt_key]["sim"] is None:
            fb_section[udt_key]["sim"] = {"name": override["name"], "param": override["param"]}

    return {
        "manifest_version": MANIFEST_VERSION,
        "library_version": "unknown",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "udts": udt_section,
        "fbs": fb_section,
    }


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------

def write_manifest_atomic(manifest: dict, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    tmp = dest.with_suffix(".tmp")
    tmp.write_text(content, encoding="utf-8")
    dest.unlink(missing_ok=True)
    tmp.rename(dest)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    udt_files = sorted(cfg.UDT_SOURCES.rglob("*.udt"))
    scl_files = sorted(cfg.FB_SOURCES.rglob("*.scl"))

    if not udt_files and not scl_files:
        print("No source files found in sources/.")
        print(f"  UDTs dir : {cfg.UDT_SOURCES}")
        print(f"  FBs dir  : {cfg.FB_SOURCES}")
        print("Run scripts/export.py first.")
        sys.exit(1)

    udts = [parse_udt(f) for f in udt_files]
    fbs = [fb for fb in (parse_fb(f) for f in scl_files) if fb is not None]
    sim_overrides = _load_sim_overrides()

    manifest = build_manifest(udts, fbs, sim_overrides)
    write_manifest_atomic(manifest, cfg.MANIFEST_PATH)

    print(f"UDTs parsed      : {len(udts)}")
    print(f"FBs parsed       : {len(fbs)} (of {len(scl_files)} .scl files)")
    print(f"Sim overrides    : {len(sim_overrides)}")
    print(f"Manifest written : {cfg.MANIFEST_PATH}")
    print()
    print("UDTs:")
    for u in udts:
        flag = " [has_out]" if u["has_out"] else ""
        print(f"  {u['name']}{flag}  devices={list(u['devices'].keys())}")
    print()
    print("FBs -> UDT mapping:")
    for fb in fbs:
        kind = "sim" if fb["is_sim"] else "ctrl"
        print(f"  [{kind}] {fb['name']}({fb['param_name']} : {fb['udt_type']})")
    if sim_overrides:
        print()
        print("Sim overrides applied:")
        for o in sim_overrides:
            print(f"  [sim] {o['name']}({o['param']} : {o['udt']})")


if __name__ == "__main__":
    main()
