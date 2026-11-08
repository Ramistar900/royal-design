#!/usr/bin/env python3
"""Validate the private ROYAL Design browser gallery and currently shipped V10/V13 assets."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "preview/v9-icon-catalog/index.html"

def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")

html = HTML.read_text(encoding="utf-8")
match = re.search(r"const groups=(.*?),labels=", html, re.S)
if not match:
    fail("gallery groups data block is missing")
groups = json.loads(match.group(1))

for version in [f"v{i}" for i in range(2, 10)]:
    if not any(group["v"] == version for group in groups):
        fail(f"gallery is missing {version.upper()}")

v10 = [g for g in groups if g["v"] == "v10"]
if len(v10) != 1 or len(v10[0]["items"]) != 12:
    fail("V10 gallery must expose the 12 imported source SVGs")
for item in v10[0]["items"]:
    path = ROOT / v10[0]["path"] / f"{item}.svg"
    if not path.is_file():
        fail(f"missing V10 SVG: {path.relative_to(ROOT)}")

v13 = [g for g in groups if g["v"] == "v13"]
if len(v13) != 2 or {g["title"].rsplit(" ", 1)[-1] for g in v13} != {"Flat", "Glass"}:
    fail("V13 must expose separate Flat and Glass gallery groups")
if any(len(group["items"]) != 8 for group in v13):
    fail("each V13 style must contain 8 concepts")
for group in v13:
    for item in group["items"]:
        path = ROOT / group["path"] / f"{item}.svg"
        if not path.is_file():
            fail(f"missing V13 SVG: {path.relative_to(ROOT)}")

for catalog_path, expected in [
    ("icons/v10/2d/catalog.json", 12),
    ("icons/v13/2d/catalog.json", 8),
]:
    catalog = json.loads((ROOT / catalog_path).read_text(encoding="utf-8"))
    if len(catalog.get("assets", [])) != expected:
        fail(f"{catalog_path} must contain {expected} assets")

for svg in list((ROOT / "icons/v10/2d").glob("*.svg")) + list((ROOT / "icons/v13/2d/flat").glob("*.svg")) + list((ROOT / "icons/v13/2d/glass").glob("*.svg")):
    try:
        node = ET.parse(svg).getroot()
    except ET.ParseError as exc:
        fail(f"invalid SVG XML in {svg.relative_to(ROOT)}: {exc}")
    if not node.tag.endswith("svg"):
        fail(f"unexpected root element in {svg.relative_to(ROOT)}")

for version in ("V11", "V12", "V14"):
    if version not in html or "قيد الإكمال" not in html:
        fail(f"gallery roadmap is missing {version}")
if 'value="v10"' not in html or 'value="v13"' not in html:
    fail("version filter must include V10 and V13")

print("ROYAL Design gallery validation passed: V2–V10 and V13 assets/paths verified; V11/V12/V14 are explicitly marked in progress.")
