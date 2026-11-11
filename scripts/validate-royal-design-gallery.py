#!/usr/bin/env python3
"""Validate the current ROYAL Design gallery after legacy V2-V15 retirement."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery/index.html"
V18 = ROOT / "preview/royal-design/v18"
CODE_BUILDER = ROOT / "scripts/build-icon-code-index.py"
CODE_STANDARD = ROOT / "icons/color-code-standard.json"
LEGACY_DIRS = [ROOT / "icons" / f"v{n}" for n in range(2, 16)]
LEGACY_FILES = [
    ROOT / "ROYAL_Android_Icons_v2.zip",
    ROOT / "preview/v9-icon-catalog/index.html",
    ROOT / "preview/royal-design/index.html",
]

def fail(message):
    raise SystemExit("ERROR: " + message)

catalog = json.loads((ROOT / "icons/catalog.json").read_text(encoding="utf-8"))
apps = json.loads((ROOT / "icons/app-collections.json").read_text(encoding="utf-8"))
if catalog.get("versions") or catalog.get("icons"):
    fail("legacy icon catalog must be empty after V2-V15 retirement")
if apps.get("versions"):
    fail("legacy app collections must be empty after V2-V15 retirement")
for path in LEGACY_DIRS + LEGACY_FILES:
    if path.exists():
        fail(f"legacy V2-V15 asset still exists: {path.relative_to(ROOT)}")

svg_files = sorted(V18.rglob("*.svg"))
if len(svg_files) != 451:
    fail(f"V18 expected 451 SVG source files, found {len(svg_files)}")
for path in svg_files:
    try:
        root = ET.parse(path).getroot()
    except Exception as exc:
        fail(f"invalid V18 SVG {path.relative_to(ROOT)}: {exc}")
    if not root.tag.endswith("svg") or not root.attrib.get("viewBox"):
        fail(f"invalid V18 SVG root/viewBox: {path.relative_to(ROOT)}")

if not CODE_BUILDER.is_file():
    fail("color-code generator is missing")
if not CODE_STANDARD.is_file():
    fail("color-code standard is missing")
standard = json.loads(CODE_STANDARD.read_text(encoding="utf-8"))
if standard.get("total_length") != 6 or standard.get("code_format") != r"^[A-Z][0-9]{5}$":
    fail("icon codes must have one letter followed by five digits")
if standard.get("prefixes", {}).get("R", {}).get("name_ar") != "ذهبي":
    fail("R must remain the prefix for gold icons")

page = GALLERY.read_text(encoding="utf-8")
for required in ("source-assets.json", "icons/v16/uploaded-royal-icon-package/catalog.json",
                 "icons/v17/royal-library/catalog.json", "icon-codes.json", "copy-code",
                 "registryKey", "color-legend", "V16", "V17", "V18"):
    if required not in page:
        fail(f"current gallery is missing {required}")
if "V2–V15" in page or "من V2 إلى V18" in page:
    fail("legacy editions are still advertised by the current gallery")

script_blocks = re.findall(r"<script>(.*?)</script>", page, re.S)
if not script_blocks:
    fail("gallery JavaScript block is missing")
if "source.files" not in script_blocks[-1] or "source.archives" not in script_blocks[-1]:
    fail("gallery no longer renders source inventory and archives")

print(f"ROYAL Design gallery passed: legacy V2-V15 absent; V18 {len(svg_files)} SVGs validated; V16/V17 source loading and six-character color codes enabled.")
