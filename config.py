"""Central path constants for tia-knowledge."""

import os
from pathlib import Path

ROOT = Path(__file__).parent

# ─── AleFire-Library ────────────────────────────────────────────────────────
LIBRARY_PATH = Path(os.getenv(
    "TIA_LIBRARY_PATH",
    str(ROOT / "library" / "AleFire-Library_V21" / "AleFire-Library_V21.al21"),
))

# ─── Staging project (export workflow) ──────────────────────────────────────
STAGING_PROJECT = Path(os.getenv(
    "TIA_STAGING_PROJECT",
    str(ROOT / "Library_export" / "Library_export.ap20"),
))

TIA_PLC_NAME = os.getenv("TIA_PLC_NAME", "PLC_1")

# ─── TIA Portal API paths (for pythonnet/Openness — V21) ────────────────────
TIA_PUBLIC_API = Path(r"C:\Program Files\Siemens\Automation\Portal V21\PublicAPI\V21")
TIA_BIN_API    = Path(r"C:\Program Files\Siemens\Automation\Portal V21\Bin\PublicAPI")

# ─── Raw Simatic SD exports ───────────────────────────────────────────────────
RAW         = ROOT / "raw"
FB_SOURCES  = RAW / "FBs"    # default subdir when using export.py
UDT_SOURCES = RAW / "UDTs"  # default subdir when using export.py

# ─── Published artifacts ─────────────────────────────────────────────────────
DIST_DIR      = ROOT / "dist"
MANIFEST_PATH = DIST_DIR / "library_manifest.json"

# ─── Ingest change-detection artifacts ───────────────────────────────────────
INGEST_CACHE_PATH = DIST_DIR / ".ingest_cache.json"   # local, gitignored
INGEST_DELTA_PATH = DIST_DIR / "ingest_delta.json"    # committed with manifest
