#!/usr/bin/env python3
"""Validate ROYAL DESIGN V13 original 2D SVG assets and provenance metadata."""
import json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "icons/v13/2d/catalog.json"
STYLES = ("flat", "glass")
EXPECTED = 8
errors = []
def fail(message): errors.append(message)

try:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"ERROR: cannot read catalog: {exc}")
    sys.exit(1)

if catalog.get("library") != "ROYAL DESIGN V13": fail("wrong library name")
if catalog.get("dimension") != "2D": fail("dimension must be 2D")
if tuple(catalog.get("styles", [])) != STYLES: fail("styles must be flat, glass")
assets = catalog.get("assets", [])
if len(assets) != EXPECTED: fail(f"expected {EXPECTED} concepts, found {len(assets)}")
seen = set()
for item in assets:
    key = item.get("key", "")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", key): fail(f"invalid key: {key!r}")
    if key in seen: fail(f"duplicate key: {key}")
    seen.add(key)
    if item.get("origin") != "original_royal": fail(f"{key}: invalid origin")
    if item.get("license") != "ROYAL_ORIGINAL": fail(f"{key}: invalid license marker")
    if not item.get("authoring_note"): fail(f"{key}: missing authoring note")
    variants = item.get("variants", {})
    if set(variants) != set(STYLES): fail(f"{key}: Flat and Glass must be separate variants")
    for style in STYLES:
        rel = variants.get(style, "")
        expected = f"icons/v13/2d/{style}/{key}.svg"
        if rel != expected: fail(f"{key}/{style}: unexpected path {rel!r}"); continue
        path = ROOT / rel
        if not path.is_file(): fail(f"missing SVG: {rel}"); continue
        try: root = ET.parse(path).getroot()
        except Exception as exc: fail(f"{rel}: invalid XML ({exc})"); continue
        if not root.tag.endswith("svg"): fail(f"{rel}: root is not svg")
        if root.attrib.get("viewBox") != "0 0 128 128": fail(f"{rel}: wrong viewBox")
        content = path.read_text(encoding="utf-8")
        if "origin=original_royal" not in content or "license=ROYAL_ORIGINAL" not in content: fail(f"{rel}: missing embedded provenance")
        if "<script" in content.lower() or "<foreignobject" in content.lower(): fail(f"{rel}: active/foreign content")
        if re.search(r"""(?:href|xlink:href)\s*=\s*['"]https?://""", content, re.I): fail(f"{rel}: external resource link")
        if "iconscout.com" in content.lower(): fail(f"{rel}: marketplace URL embedded")
if errors:
    print("V13 validation FAILED:")
    for error in errors: print(f"- {error}")
    sys.exit(1)
print(f"V13 validation passed: {len(assets)} concepts, {len(assets)*2} SVG files, XML and provenance checks.")
