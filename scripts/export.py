"""
Export all AleFire-Library types to sources/ as ExternalSource files.

Pipeline:
  1. Open/attach staging project (Library_export/Library_export.ap20)
  2. Open global AleFire-Library (if not already open in TIA Portal)
  3. Enumerate all library types via lib.get_types()
  4. Instantiate each type into the PLC (folder_path="" = root)
  5. Export all program blocks -> sources/FBs/
  6. Export all UDTs          -> sources/UDTs/

WARNING — known bug in siemens_tia_scripting v1.2.1:
  version.instantiate() throws NullReferenceException for all AleFire-Library types.
  Root cause: suspected stale COM proxy after library traversal.
  If instantiation fails for all types, use --skip-instantiate and instantiate
  manually in TIA Portal UI, then re-run to export.

Usage:
    uv run python scripts/export.py
    uv run python scripts/export.py --skip-instantiate
    uv run python scripts/export.py --config path/to/config.toml
"""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_config(config_path: Path) -> dict:
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def _ensure_library_open(portal, library_name: str, library_path: str):
    """Return the open GlobalLibrary, opening from file if not already open."""
    try:
        lib = portal.get_global_library(library_name=library_name)
        print(f"Library already open: {library_name}")
        return lib
    except Exception:
        pass
    print(f"Opening library: {library_path}")
    return portal.open_global_library(library_path=library_path)


def _latest_version(lib_type):
    """Return the highest-numbered LibraryTypeVersion for a LibraryType."""
    versions = lib_type.get_versions()
    if not versions:
        return None
    # Sort by version number string; falls back to list order for equal strings
    try:
        versions_sorted = sorted(
            versions,
            key=lambda v: tuple(int(x) for x in v.get_version_number().split(".")),
        )
        return versions_sorted[-1]
    except Exception:
        return versions[-1]


def _collect_all_types(lib_or_folder) -> list:
    """Recursively collect all LibraryType objects from library root and sub-folders."""
    collected = []
    try:
        collected.extend(lib_or_folder.get_types())
    except Exception:
        pass
    try:
        for folder in lib_or_folder.get_folders():
            collected.extend(_collect_all_types(folder))
    except Exception:
        pass
    return collected


def _instantiate_all(lib, plc_name: str) -> tuple[list[str], list[tuple[str, str]]]:
    """
    Try to instantiate every type in the library into the PLC.
    Returns (ok_names, [(failed_name, error_str)]).
    """
    lib_types = _collect_all_types(lib)
    print(f"\nFound {len(lib_types)} library types. Instantiating into '{plc_name}'...")

    ok: list[str] = []
    failed: list[tuple[str, str]] = []

    for lt in lib_types:
        name = lt.get_name()
        version = _latest_version(lt)
        if version is None:
            failed.append((name, "no versions found"))
            print(f"  !   {name}: no versions found")
            continue
        ver_str = version.get_version_number()
        try:
            version.instantiate(device_name=plc_name, folder_path="")
            ok.append(name)
            print(f"  ok  {name} v{ver_str}")
        except Exception as exc:
            msg = str(exc)
            failed.append((name, msg))
            print(f"  !   {name} v{ver_str}: {msg}")

    return ok, failed


def _export_blocks(plc, fb_dir: Path, ts) -> tuple[int, list[str]]:
    blocks = plc.get_program_blocks()
    print(f"\nExporting {len(blocks)} program blocks -> {fb_dir}")
    exported, failed = 0, []
    for block in blocks:
        name = block.get_name()
        try:
            block.export(
                str(fb_dir),
                ts.Enums.ExportOptions.Nan,
                ts.Enums.ExportFormats.ExternalSource,
                True,
            )
            exported += 1
            print(f"  ok  {name}")
        except Exception as e:
            print(f"  !   {name}: {e}")
            failed.append(name)
    return exported, failed


def _export_udts(plc, udt_dir: Path, ts) -> tuple[int, list[str]]:
    udts = plc.get_user_data_types()
    print(f"\nExporting {len(udts)} UDTs -> {udt_dir}")
    exported, failed = 0, []
    for udt in udts:
        name = udt.get_name()
        try:
            udt.export(
                str(udt_dir),
                ts.Enums.ExportOptions.Nan,
                ts.Enums.ExportFormats.ExternalSource,
                True,
            )
            exported += 1
            print(f"  ok  {name}")
        except Exception as e:
            print(f"  !   {name}: {e}")
            failed.append(name)
    return exported, failed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Instantiate AleFire-Library types into staging project and export as SCL/UDT"
    )
    parser.add_argument("--config", default="config.toml")
    parser.add_argument(
        "--skip-instantiate",
        action="store_true",
        help="Skip library instantiation (types already present in staging project)",
    )
    args = parser.parse_args()

    config_path = ROOT / args.config
    if not config_path.exists():
        print(f"ERROR: config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    cfg = load_config(config_path)
    project_path  = cfg["tia"]["project_path"]
    library_path  = cfg["tia"]["library_path"]
    tia_version   = cfg["tia"].get("version") or None
    fb_dir  = ROOT / cfg["export"]["fb_output_dir"]
    udt_dir = ROOT / cfg["export"]["udt_output_dir"]

    # Derive library name from filename (without extension)
    library_name = Path(library_path).stem

    try:
        import siemens_tia_scripting as ts
    except ImportError:
        print(
            "ERROR: siemens_tia_scripting not installed.\n"
            "Run: uv pip install <path>\\siemens_tia_scripting-1.2.1-cp312-cp312-win_amd64.whl",
            file=sys.stderr,
        )
        sys.exit(1)

    fb_dir.mkdir(parents=True, exist_ok=True)
    udt_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: open / attach staging project
    # open_attach_project() returns a Project object; get_portal() gives the Portal.
    # Library methods (open_global_library, get_global_library) live on Portal, not Project.
    print(f"Attaching to project: {project_path}")
    try:
        kwargs: dict = {
            "project_file_path": project_path,
            "portal_mode": ts.Enums.PortalMode.WithGraphicalUserInterface,
        }
        if tia_version:
            kwargs["version"] = tia_version
        project = ts.open_attach_project(**kwargs)
        portal = project.get_portal()
    except Exception as e:
        print(f"ERROR: Could not open/attach project: {e}", file=sys.stderr)
        sys.exit(1)

    plcs = project.get_plcs()
    if not plcs:
        print("ERROR: No PLC found in staging project.", file=sys.stderr)
        sys.exit(1)
    plc = plcs[0]
    plc_name = plc.get_name()
    print(f"PLC: {plc_name}")

    # Step 2 + 3: open library and instantiate all types
    inst_ok: list[str] = []
    inst_failed: list[tuple[str, str]] = []

    if args.skip_instantiate:
        print("\nSkipping instantiation (--skip-instantiate).")
    else:
        try:
            lib = _ensure_library_open(portal, library_name, library_path)
        except Exception as e:
            print(f"ERROR: Could not open library '{library_name}': {e}", file=sys.stderr)
            print("Hint: open the library manually in TIA Portal and re-run, or use --skip-instantiate")
            sys.exit(1)

        inst_ok, inst_failed = _instantiate_all(lib, plc_name)

        if inst_failed and not inst_ok:
            print(
                "\nWARNING: All instantiations failed.\n"
                "Known bug: version.instantiate() throws NullReferenceException for all\n"
                "AleFire-Library types in siemens_tia_scripting v1.2.1.\n"
                "Workaround: instantiate all types manually in TIA Portal UI, then\n"
                "re-run with --skip-instantiate to export.",
                file=sys.stderr,
            )
            sys.exit(1)
        elif inst_failed:
            print(f"\nWARNING: {len(inst_failed)} type(s) failed to instantiate:")
            for name, err in inst_failed:
                print(f"  {name}: {err}")

    # Step 4: export
    block_count, block_failed = _export_blocks(plc, fb_dir, ts)
    udt_count, udt_failed = _export_udts(plc, udt_dir, ts)

    total_failed = block_failed + udt_failed
    print(f"\nDone. {block_count + udt_count} files exported.")
    if total_failed:
        print(f"Export failures ({len(total_failed)}): {', '.join(total_failed)}")

    print(
        "\nNext steps:\n"
        "  1. Remove all user blocks from the staging project in TIA Portal\n"
        "     (keeps staging project in clean empty state for next run)\n"
        "  2. Run: uv run python scripts/generate_docs.py\n"
        "  3. Commit sources/ and dist/library_manifest.json"
    )

    if total_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
