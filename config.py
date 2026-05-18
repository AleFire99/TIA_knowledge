"""Central path constants for tia-knowledge."""

import os
from pathlib import Path

ROOT = Path(__file__).parent

# ─── AleFire-Library ────────────────────────────────────────────────────────
LIBRARY_PATH = Path(os.getenv(
    "TIA_LIBRARY_PATH",
    r"C:\Users\user015\Desktop\Projects\Libreria software\AleFire-Library\AleFire-Library.al20",
))

# ─── Staging project (export workflow) ──────────────────────────────────────
STAGING_PROJECT = Path(os.getenv(
    "TIA_STAGING_PROJECT",
    str(ROOT / "Library_export" / "Library_export.ap20"),
))

TIA_PLC_NAME = os.getenv("TIA_PLC_NAME", "PLC_1")

# ─── TIA Portal API paths (for pythonnet/Openness — V20) ────────────────────
TIA_PUBLIC_API = Path(r"C:\Program Files\Siemens\Automation\Portal V20\PublicAPI\V20")
TIA_BIN_API    = Path(r"C:\Program Files\Siemens\Automation\Portal V20\Bin\PublicAPI")

# ─── Library sources ─────────────────────────────────────────────────────────
SOURCES     = ROOT / "sources"
FB_SOURCES  = SOURCES / "FBs"
UDT_SOURCES = SOURCES / "UDTs"

# ─── Published artifacts ─────────────────────────────────────────────────────
DIST_DIR      = ROOT / "dist"
MANIFEST_PATH = DIST_DIR / "library_manifest.json"
