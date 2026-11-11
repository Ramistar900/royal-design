#!/usr/bin/env python3
"""Build a deterministic six-character color-coded ID for every icon displayed in ROYAL DESIGN."""
from __future__ import annotations
import argparse
import colorsys
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

IMAGE_EXTENSIONS = {".svg", ".xml", ".png", ".webp", ".gif"}
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
COLORS = {
    "R": {"ar": "ذهبي", "en": "Gold", "hex": "#D7B96D"},
    "O": {"ar": "برتقالي", "en": "Orange", "hex": "#F28C28"},
    "D": {"ar": "أحمر", "en": "Red", "hex": "#D94141"},
    "Y": {"ar": "أصفر", "en": "Yellow", "hex": "#F4D03F"},
    "G": {"ar": "أخضر", "en": "Green", "hex": "#38A169"},
    "T": {"ar": "فيروزي", "en": "Turquoise", "hex": "#168B79"},
    "C": {"ar": "سماوي", "en": "Cyan", "hex": "#25BBD1"},
    "B": {"ar": "أزرق", "en": "Blue", "hex": "#236BFF"},
    "P": {"ar": "بنفسجي", "en": "Purple", "hex": "#8B35E8"},
    "H": {"ar": "وردي", "en": "Pink", "hex": "#E879B9"},
    "W": {"ar": "أبيض", "en": "White", "hex": "#F2F5FA"},
    "S": {"ar": "فضي/رمادي", "en": "Silver / Gray", "hex": "#9AA7B8"},
    "K": {"ar": "أسود", "en": "Black", "hex": "#343A46"},
    "X": {"ar": "متعدد/غير محدد", "en": "Mixed / Unspecified", "hex": "#7E8798"},
}
PREFERRED_GRADIENTS = ("fg", "foreground", "accent", "icon", "glyph", "a", "t", "primary", "brand", "main")
IGNORED_GRADIENTS = {"p", "bg", "background", "surface", "base", "tile", "h", "highlight", "s", "shadow", "sh", "halo", "g", "glow"}


def rgb(value):
    raw = (value or "").strip().lstrip("#")
    if len(raw) in (3, 4):
        raw = "".join(ch * 2 for ch in raw[:3])
    elif len(raw) == 8:
        raw = raw[-6:]
    if len(raw) != 6:
        return None
    try:
        return tuple(int(raw[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def color_prefix(value):
    parsed = rgb(value)
    if parsed is None:
        return "X"
    h, s, v = colorsys.rgb_to_hsv(*(channel / 255.0 for channel in parsed))
    h *= 360
    if s < 0.13:
        return "W" if v >= 0.88 else ("K" if v <= 0.20 else "S")
    if 34 <= h <= 56: return "R"
    if 18 <= h < 34: return "O"
    if h < 18 or h >= 345: return "D"
    if 56 < h <= 70: return "Y"
    if 70 < h < 155: return "G"
    if 155 <= h < 180: return "T"
    if 180 <= h < 205: return "C"
    if 205 <= h < 255: return "B"
    if 255 <= h < 295: return "P"
    if 295 <= h < 345: return "H"
    return "X"


def style_color(style):
    match = re.search(r"(?:stop-color|fill|stroke)\s*:\s*(#[0-9a-fA-F]{3,8})", style or "")
    return match.group(1) if match else None


def palette(path):
    if not path.is_file():
        raise SystemExit(f"Missing icon source: {path}")
    content = path.read_text(encoding="utf-8", errors="replace")
    gradients = {}
    direct = []
    if path.suffix.lower() in {".svg", ".xml"}:
        try:
            root = ET.fromstring(content)
        except ET.ParseError as exc:
            raise SystemExit(f"Invalid SVG/XML {path}: {exc}") from exc
        for element in root.iter():
            tag = element.tag.rsplit("}", 1)[-1].lower()
            if tag in {"lineargradient", "radialgradient"}:
                ident = (element.attrib.get("id") or "").lower()
                stops = []
                for stop in element:
                    val = stop.attrib.get("stop-color") or style_color(stop.attrib.get("style", ""))
                    if val and rgb(val):
                        stops.append(val.upper())
                if ident and stops:
                    gradients[ident] = stops
            for attr in ("fill", "stroke", "fillColor", "strokeColor", "android:fillColor"):
                val = element.attrib.get(attr)
                if not val or re.search(r"url\(#([^)]+)\)", val):
                    continue
                if rgb(val):
                    direct.append(val.upper())
                else:
                    direct.extend(m.group(0).upper() for m in HEX_RE.finditer(val))
            direct.extend(m.group(0).upper() for m in HEX_RE.finditer(element.attrib.get("style", "")))
    else:
        direct = [m.group(0).upper() for m in HEX_RE.finditer(content[:500000])]

    # Explicit foreground/accent gradients take precedence over backgrounds, shine and shadows.
    for ident in PREFERRED_GRADIENTS:
        if ident in gradients:
            colors = gradients[ident]
            counts = Counter(color_prefix(c) for c in colors)
            chosen = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[0][0]
            matches = [c for c in colors if color_prefix(c) == chosen]
            return chosen, Counter(matches).most_common(1)[0][0]

    referenced = []
    for match in re.finditer(r"url\(#([^)]+)\)", content):
        ident = match.group(1).lower()
        if ident not in IGNORED_GRADIENTS and ident in gradients:
            referenced.extend(gradients[ident])
    colors = referenced + direct
    if not colors:
        return "X", COLORS["X"]["hex"]
    counts = Counter(color_prefix(c) for c in colors)
    chromatic = {key: value for key, value in counts.items() if key not in {"W", "S", "K", "X"}}
    candidates = chromatic or counts
    chosen = sorted(candidates.items(), key=lambda pair: (-pair[1], pair[0]))[0][0]
    matches = [c for c in colors if color_prefix(c) == chosen]
    return chosen, Counter(matches).most_common(1)[0][0] if matches else COLORS[chosen]["hex"]


def paths_for(icon):
    result = []
    variants = icon.get("variants") or {}
    for name in ("2d", "static", "3d", "motion", "focused", "android_xml"):
        value = variants.get(name)
        if isinstance(value, str) and value not in result:
            result.append(value)
    for name in ("svg", "animated_svg", "motion", "android_xml"):
        value = icon.get(name)
        if isinstance(value, str) and value not in result:
            result.append(value)
    return result


def choose_source(paths):
    for path in paths:
        lower = path.lower()
        if lower.endswith((".svg", ".xml")) and any(part in lower for part in ("/2d/", "/static/", "/svg/")):
            return path
    for path in paths:
        if path.lower().endswith((".svg", ".xml")):
            return path
    return paths[0] if paths else None


def record_from_icon(icon, version, key_prefix, site):
    key = str(icon.get("key") or "")
    if not key:
        raise SystemExit(f"Icon in {version} has no stable key")
    refs = paths_for(icon)
    source = choose_source(refs)
    if not source:
        raise SystemExit(f"Icon {key_prefix}:{key} has no usable source")
    public_refs = ["royal-design-gallery/" + value.lstrip("/") for value in refs]
    color, sample = palette(site / public_refs[0 if public_refs else 0]) if False else palette(site / ("royal-design-gallery/" + source.lstrip("/")))
    return {
        "registry_key": key_prefix + ":" + key,
        "name_ar": icon.get("label_ar") or icon.get("label_en") or key,
        "name_en": icon.get("label_en") or key,
        "version": version,
        "color_prefix": color,
        "color_ar": COLORS[color]["ar"],
        "color_en": COLORS[color]["en"],
        "color_hex": sample,
        "path": public_refs[0],
        "variants": public_refs,
        "source_kind": "catalog",
    }


def self_test():
    expected = {
        "#F5B400": "R", "#D7B96D": "R", "#1E6BFF": "B", "#168B79": "T",
        "#8B35E8": "P", "#FFFFFF": "W", "#777777": "S", "#111111": "K",
    }
    for color, target in expected.items():
        if color_prefix(color) != target:
            raise SystemExit(f"Color classifier test failed for {color}: expected {target}")


def build(site, json_output, csv_output):
    self_test()
    inventory_file = site / "source-assets.json"
    if not inventory_file.is_file():
        raise SystemExit(f"Missing source inventory: {inventory_file}")
    inventory = json.loads(inventory_file.read_text(encoding="utf-8"))
    records = []
    keys = set()
    represented = set()

    for version, rel in (
        ("V16", "royal-design-gallery/icons/v16/uploaded-royal-icon-package/catalog.json"),
        ("V17", "royal-design-gallery/icons/v17/royal-library/catalog.json"),
    ):
        catalog_path = site / rel
        if not catalog_path.is_file():
            raise SystemExit(f"Required catalog missing: {catalog_path}")
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for icon in catalog.get("icons", []):
            record = record_from_icon(icon, version, version, site)
            if record["registry_key"] in keys:
                raise SystemExit("Duplicate registry key: " + record["registry_key"])
            records.append(record)
            keys.add(record["registry_key"])
            represented.update(record["variants"])

    current = json.loads((site / "icons/catalog.json").read_text(encoding="utf-8"))
    for icon in current.get("icons", []):
        key = str(icon.get("key") or "")
        refs = [value for value in (icon.get("svg"), icon.get("animated_svg")) if isinstance(value, str)]
        source = choose_source(refs)
        stable = "catalog:" + key
        if not key or not source or stable in keys:
            raise SystemExit("Invalid current icon catalog entry: " + str(icon))
        color, sample = palette(site / source)
        records.append({
            "registry_key": stable, "name_ar": icon.get("label_ar") or key,
            "name_en": icon.get("label_en") or key, "version": str(icon.get("version") or "CURRENT"),
            "color_prefix": color, "color_ar": COLORS[color]["ar"], "color_en": COLORS[color]["en"],
            "color_hex": sample, "path": source, "variants": refs, "source_kind": "catalog",
        })
        keys.add(stable)
        represented.update(refs)

    collections = json.loads((site / "icons/app-collections.json").read_text(encoding="utf-8"))
    for collection in collections.get("versions", []):
        version = str(collection.get("version") or "CURRENT")
        for icon in collection.get("icons", []):
            key = str(icon.get("key") or "")
            refs = paths_for(icon)
            source = choose_source(refs)
            stable = "collection:" + version + ":" + key
            if not key or not source or stable in keys:
                raise SystemExit("Invalid app collection icon: " + str(icon))
            color, sample = palette(site / source)
            records.append({
                "registry_key": stable, "name_ar": icon.get("label_ar") or key,
                "name_en": icon.get("label_en") or key, "version": version,
                "color_prefix": color, "color_ar": COLORS[color]["ar"], "color_en": COLORS[color]["en"],
                "color_hex": sample, "path": source, "variants": refs, "source_kind": "app_collection",
            })
            keys.add(stable)
            represented.update(refs)

    for asset in inventory.get("files", []):
        public_path = str(asset.get("path") or "")
        if not public_path or Path(public_path).suffix.lower() not in IMAGE_EXTENSIONS or public_path in represented:
            continue
        stable = "asset:" + public_path
        if stable in keys:
            raise SystemExit("Duplicate source asset key: " + stable)
        color, sample = palette(site / public_path)
        records.append({
            "registry_key": stable, "name_ar": Path(public_path).name,
            "name_en": Path(public_path).name, "version": str(asset.get("version") or "SOURCE"),
            "color_prefix": color, "color_ar": COLORS[color]["ar"], "color_en": COLORS[color]["en"],
            "color_hex": sample, "path": public_path, "variants": [public_path], "source_kind": "source_asset",
        })
        keys.add(stable)

    used = set()
    for item in sorted(records, key=lambda row: row["registry_key"]):
        stable = item["registry_key"]
        base = hashlib.sha256(stable.encode("utf-8")).hexdigest()
        attempt = 0
        while True:
            digest = base if attempt == 0 else hashlib.sha256((stable + "|" + str(attempt)).encode("utf-8")).hexdigest()
            number = int(digest[:16], 16) % 100000
            code = item["color_prefix"] + f"{number:05d}"
            if code not in used:
                break
            attempt += 1
            if attempt > 100000:
                raise SystemExit("Could not allocate a unique six-character icon code")
        item["code"] = code
        used.add(code)

    records.sort(key=lambda row: (row["version"], row["color_prefix"], row["name_ar"], row["registry_key"]))
    totals = Counter(row["color_prefix"] for row in records)
    result = {
        "schema_version": 1,
        "title": "ROYAL Design · Color-Coded Icon Registry",
        "code_format": "one color letter + five digits",
        "description_ar": "رمز ثابت من ست خانات لكل بطاقة أيقونة؛ الحرف الأول يحدد اللون، والخمس خانات التالية رقم فريد مشتق بصورة حتمية من مفتاح الأيقونة.",
        "color_prefixes": COLORS,
        "total_icons": len(records),
        "color_totals": dict(sorted(totals.items())),
        "icons": records,
    }
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with csv_output.open("w", encoding="utf-8-sig", newline="") as handle:
        fields = ["code", "color_prefix", "color_ar", "name_ar", "name_en", "version", "registry_key", "path", "source_kind"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in records:
            writer.writerow({field: row.get(field, "") for field in fields})

    known = {
        "preview/royal-design/v18/store/static/settings.svg": "R",
        "preview/royal-design/v18/display/static/settings.svg": "R",
        "royal-design-gallery/packages/restaurant-tv-icons-v2-transparent/extracted/store/static/settings.svg": "R",
        "royal-design-gallery/packages/restaurant-tv-icons-v2-transparent/extracted/tv/static/settings.svg": "B",
    }
    for rel, expected in known.items():
        path = site / rel
        if path.is_file():
            actual, _ = palette(path)
            if actual != expected:
                raise SystemExit(f"Color check failed for {rel}: expected {expected}, got {actual}")

    codes = [row["code"] for row in records]
    if len(codes) != len(set(codes)) or any(not re.fullmatch(r"[A-Z][0-9]{5}", code) for code in codes):
        raise SystemExit("Duplicate or malformed icon code")
    print(f"Generated {len(records)} unique six-character icon codes: {dict(totals)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, default=Path("_site"))
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--csv-output", type=Path, default=None)
    args = parser.parse_args()
    build(args.site_root, args.output or args.site_root / "icon-codes.json", args.csv_output or args.site_root / "icon-codes.csv")


if __name__ == "__main__":
    main()
