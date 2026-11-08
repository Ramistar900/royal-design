#!/usr/bin/env python3
"""Validate app-specific ROYAL Design collections, paired SVG files, and web gallery."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "icons/app-collections.json"
GALLERY = ROOT / "preview/royal-design/index.html"
EXPECTED = {
    "V10": ("almalaki", 8),
    "V11": ("royal-tv", 8),
    "V12": ("royal-plus", 8),
    "V13": ("rs-tv", 8),
    "V14": ("rami-developer", 8),
}

def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")

data = json.loads(MANIFEST.read_text(encoding="utf-8"))
versions = data.get("versions", [])
if len(versions) != 5:
    fail("the app manifest must contain exactly five application collections")
seen = set()
count = 0
for app in versions:
    version = app.get("version")
    if version not in EXPECTED:
        fail(f"unexpected application version: {version}")
    slug, expected_count = EXPECTED[version]
    if app.get("slug") != slug:
        fail(f"{version} has the wrong application slug")
    icons = app.get("icons", [])
    if len(icons) != expected_count:
        fail(f"{version} must contain {expected_count} concepts")
    keys = set()
    for icon in icons:
        key = icon.get("key", "")
        if not re.fullmatch(r"[a-z0-9-]+", key) or key in keys:
            fail(f"{version}: invalid or duplicate icon key {key!r}")
        keys.add(key)
        if not icon.get("label_ar") or not icon.get("label_en"):
            fail(f"{version}/{key}: both Arabic and English labels are required")
        if icon.get("rights", {}).get("origin") != "original_royal":
            fail(f"{version}/{key}: missing original-work provenance")
        if icon.get("rights", {}).get("license") != "ROYAL_ORIGINAL":
            fail(f"{version}/{key}: missing ROYAL_ORIGINAL license")
        variants = icon.get("variants", {})
        if set(variants) != {"2d", "3d"}:
            fail(f"{version}/{key}: the 2D and 3D pair is incomplete")
        for style, relative in variants.items():
            path = (ROOT / relative).resolve()
            if ROOT not in path.parents or not path.is_file():
                fail(f"missing or unsafe asset path: {relative}")
            try:
                node = ET.parse(path).getroot()
            except ET.ParseError as exc:
                fail(f"invalid SVG XML in {relative}: {exc}")
            if not node.tag.endswith("svg"):
                fail(f"unexpected SVG root in {relative}")
            view_box = node.attrib.get("viewBox")
            if not view_box:
                fail(f"missing viewBox in {relative}")
        count += 1
    if app.get("dimension_styles") != ["2d", "3d"]:
        fail(f"{version}: dimension style declaration is inconsistent")
if set(a["version"] for a in versions) != set(EXPECTED):
    fail("one or more app-specific versions are missing")
if data.get("totals", {}).get("concepts") != count:
    fail("manifest concept total does not match its entries")
if data.get("totals", {}).get("flat_svg") != count or data.get("totals", {}).get("dimensional_svg") != count:
    fail("manifest 2D/3D file totals do not match the entries")
html = GALLERY.read_text(encoding="utf-8")
for required in ("app-collections.json", "2d", "3d", "search", "aria-pressed"):
    if required not in html:
        fail(f"gallery is missing required feature: {required}")
print(f"ROYAL Design app gallery passed: {len(versions)} collections, {count} concepts, {count * 2} paired SVG files.")
