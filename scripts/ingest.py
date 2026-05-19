"""
Ingest raw/ Simatic SD exports → dist/library_manifest.json.

Supports VCI export format (.s7dcl files).
Dispatches each file to UDT or FB parser based on content.
Reads sibling .libinfo files for descriptions when available.

Usage:
    uv run python scripts/ingest.py

Steps:
  1. Walk raw/ recursively for .s7dcl files
  2. Parse UDT members, has_out flag, device descriptions
  3. Parse FB VAR_IN_OUT param + UDT type, is_sim flag
  4. Merge LAD sim FB overrides from config.toml [[manifest.sim_overrides]]
  5. Write dist/library_manifest.json atomically
"""

from __future__ import annotations

import hashlib
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

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
import config as cfg

MANIFEST_VERSION = "1.0.0"

# Matches _.TypeName or just TypeName (VCI uses _.prefix for cross-references)
_TYPE_RE = re.compile(r'"([^"]+)"|(?:_\.)?(\w+)')
_SIM_RE = re.compile(r"(sim(ulator)?)", re.IGNORECASE)


def _load_sim_overrides() -> list[dict]:
    toml_path = REPO_ROOT / "config.toml"
    if not toml_path.exists():
        return []
    with toml_path.open("rb") as f:
        data = tomllib.load(f)
    return data.get("manifest", {}).get("sim_overrides", [])


def _read_libinfo_description(path: Path) -> str:
    """Read en-US comment from sibling .libinfo file, return empty string if absent."""
    libinfo = path.with_suffix(".libinfo")
    if not libinfo.exists():
        return ""
    try:
        text = libinfo.read_text(encoding="utf-8-sig")
        m = re.search(r'en-US:\s*(.+)', text)
        return m.group(1).strip() if m else ""
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Change detection helpers
# ---------------------------------------------------------------------------

def _hash_type_files(s7dcl_path: Path) -> str:
    """SHA256 of .s7dcl content + sibling .libinfo content (raw bytes)."""
    h = hashlib.sha256()
    h.update(s7dcl_path.read_bytes())
    libinfo = s7dcl_path.with_suffix(".libinfo")
    if libinfo.exists():
        h.update(libinfo.read_bytes())
    return h.hexdigest()


def _load_cache(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("hashes", {})
    except Exception:
        return {}


def _save_cache(hashes: dict[str, str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "cache_version": "1.0.0",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hashes": hashes,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_delta(delta: dict, path: Path, total: int) -> None:
    """Write ingest_delta.json — Claude Code reads this before doc generation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_doc_update = delta["new"] + delta["changed"]
    payload = {
        "delta_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_types": total,
        "counts": {
            "new":     len(delta["new"]),
            "changed": len(delta["changed"]),
            "removed": len(delta["removed"]),
        },
        "needs_doc_update": needs_doc_update,
        "new":     delta["new"],
        "changed": delta["changed"],
        "removed": delta["removed"],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# UDT parsing
# ---------------------------------------------------------------------------

def _parse_member_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("//") or stripped.startswith("{"):
        return None
    m = re.match(r'^(\w+)(?:\s*\{[^}]*\})?\s*:\s*(.+)', stripped)
    if not m:
        return None
    rhs = m.group(2).split(';')[0].split('//')[0].strip()
    type_m = _TYPE_RE.match(rhs)
    if not type_m:
        return None
    raw_type = type_m.group(1) or type_m.group(2)
    if not raw_type or raw_type.lower() == "struct":
        return None
    return m.group(1), raw_type


def parse_udt(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    # VCI format: TYPE\n    UDT_Name : STRUCT (name unquoted, newline-separated)
    # Old format: TYPE "UDT_Name" (name quoted, same line)
    name_m = re.search(r'\bTYPE\b\s+"([^"]+)"', text)          # old: quoted
    if not name_m:
        name_m = re.search(r'\bTYPE\b\s+(\w+)\s*:', text)       # new: unquoted
    name = name_m.group(1) if name_m else path.stem

    # Description: en-US from .libinfo, else derive from folder path
    description = _read_libinfo_description(path)
    if not description:
        try:
            rel_parts = path.relative_to(cfg.RAW).parts
            description = " / ".join(rel_parts[:-1])
        except ValueError:
            description = ""

    devices: dict[str, dict] = {}
    has_out = False
    depth = 0
    in_devices = False

    for line in lines:
        stripped = line.strip()

        # Skip multi-line annotation lines (lines inside { ... } blocks)
        if stripped.startswith("{") and not stripped.endswith("}"):
            continue  # multi-line annotation open — ignore until close
        if stripped == "}":
            continue  # multi-line annotation close

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
# FB parsing
# ---------------------------------------------------------------------------

def parse_fb(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8-sig")

    fb_m = re.search(r'^FUNCTION_BLOCK\s+"([^"]+)"', text, re.MULTILINE)
    if not fb_m:
        return None
    fb_name = fb_m.group(1)

    var_io_m = re.search(r'\bVAR_IN_OUT\b(.*?)\bEND_VAR\b', text, re.DOTALL)
    if not var_io_m:
        return None

    var_block = var_io_m.group(1)

    # VCI format: "ParamName" : _.UDT_Type;  (param quoted, type prefixed)
    # Old format: ParamName : "UDT_Type";    (param unquoted, type quoted)
    param_m = re.search(
        r'"(\w+)"\s*(?:\{[^}]*\})?\s*:\s*(?:_\.)?(\w+)\s*;',  # VCI: quoted param
        var_block
    )
    if not param_m:
        param_m = re.search(
            r'(\w+)(?:\s*\{[^}]*\})?\s*:\s*"([^"]+)"\s*;',     # old: unquoted param
            var_block
        )
    if not param_m:
        # Fallback: unquoted param, unquoted type with optional _.prefix
        param_m = re.search(
            r'(\w+)(?:\s*\{[^}]*\})?\s*:\s*(?:_\.)?(\w+)\s*;',
            var_block
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
    dest.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    s7dcl_files = sorted(cfg.RAW.rglob("*.s7dcl"))

    # Also support old ExternalSource format (.scl / .udt)
    scl_files = sorted(cfg.RAW.rglob("*.scl"))
    udt_files = sorted(cfg.RAW.rglob("*.udt"))

    if not s7dcl_files and not scl_files and not udt_files:
        print(f"No source files found in raw/ ({cfg.RAW}).")
        print("Run scripts/export.py first, or export manually from TIA Portal.")
        sys.exit(1)

    # ── Change detection ─────────────────────────────────────────────────────
    all_s7dcl = s7dcl_files or udt_files or scl_files
    current_hashes: dict[str, str] = {f.stem: _hash_type_files(f) for f in all_s7dcl}
    old_hashes = _load_cache(cfg.INGEST_CACHE_PATH)
    current_keys, old_keys = set(current_hashes), set(old_hashes)
    delta = {
        "new":     sorted(current_keys - old_keys),
        "removed": sorted(old_keys - current_keys),
        "changed": sorted(k for k in (current_keys & old_keys) if current_hashes[k] != old_hashes[k]),
    }
    # ─────────────────────────────────────────────────────────────────────────

    udts: list[dict] = []
    fbs: list[dict] = []

    if s7dcl_files:
        for f in s7dcl_files:
            text = f.read_text(encoding="utf-8-sig")
            if "FUNCTION_BLOCK" in text:
                fb = parse_fb(f)
                if fb:
                    fbs.append(fb)
            elif "TYPE" in text:
                udts.append(parse_udt(f))
    else:
        # Fallback: old ExternalSource format
        udts = [parse_udt(f) for f in udt_files]
        fbs = [fb for fb in (parse_fb(f) for f in scl_files) if fb is not None]

    sim_overrides = _load_sim_overrides()
    manifest = build_manifest(udts, fbs, sim_overrides)
    write_manifest_atomic(manifest, cfg.MANIFEST_PATH)
    _write_delta(delta, cfg.INGEST_DELTA_PATH, total=len(current_hashes))
    _save_cache(current_hashes, cfg.INGEST_CACHE_PATH)

    print(f"UDTs parsed      : {len(udts)}")
    print(f"FBs parsed       : {len(fbs)} (of {len(s7dcl_files or scl_files)} files)")
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
    print()
    print("Change detection:")
    print(f"  New     : {delta['new'] or '(none)'}")
    print(f"  Changed : {delta['changed'] or '(none)'}")
    print(f"  Removed : {delta['removed'] or '(none)'}")
    if not delta["new"] and not delta["changed"] and not delta["removed"]:
        print("  All types unchanged — doc generation can be skipped.")
    print(f"  Delta   : {cfg.INGEST_DELTA_PATH}")


if __name__ == "__main__":
    main()
