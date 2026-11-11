#!/usr/bin/env python3
"""Apply semantic SMIL motion to the existing ROYAL Design V18 animated SVGs.

Only */animated/*.svg files are edited. Static and focused variants are never touched.
The original icon geometry, colors, viewBox and dimensions are preserved.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path("preview/royal-design/v18")
OUTER = '<g transform="translate(64 62)"><g>'
INNER = '<g transform="translate(-32 -32)">'
SHADOW = '<g transform="translate(2 4)" opacity="0.35">'
EASE = ' calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"'

def find_g_end(text: str, start: int) -> int:
    token = re.compile(r"</?g\b[^>]*>")
    depth = 0
    for match in token.finditer(text, start):
        value = match.group(0)
        if value.startswith("</"):
            depth -= 1
        elif not value.endswith("/>"):
            depth += 1
        if depth == 0:
            return match.end()
    raise ValueError("unbalanced SVG group")

def motion(kind: str, values: str, duration: str, easing: bool = True) -> str:
    extra = EASE if easing and values.count(";") == 2 else ""
    if kind == "opacity":
        return (f'<animate attributeName="opacity" values="{values}" dur="{duration}" '
                f'repeatCount="indefinite"{extra}/>')
    return (f'<animateTransform attributeName="transform" type="{kind}" values="{values}" '
            f'dur="{duration}" repeatCount="indefinite"{extra}/>' )

def semantic_motion(name: str, category: str) -> str:
    # Motion is applied to the foreground glyph around its own centre, not the tile.
    if name in {"settings", "gear"}:
        return motion("rotate", "0;360", "18s", False)
    if name in {"loading", "refresh", "update", "repeat", "shuffle"}:
        return motion("rotate", "0;360", "2.8s" if name == "loading" else "10s", False)
    if name in {"bell", "notifications", "alarm"}:
        return motion("rotate", "-8 0 -14;8 0 -14;0 0 -14", "2.1s")
    if name in {"heart", "favorites", "star", "like"}:
        return motion("scale", "1;1.085;1", "1.65s")
    if name in {"wifi", "network", "bluetooth", "cast"}:
        return motion("opacity", ".48;1;.7;1;.48", "2.35s", False)
    if name in {"weather_cloud", "cloud"}:
        return motion("translate", "0 0;2 -1;0 0;-2 1;0 0", "5s", False)
    if name in {"weather_sun", "brightness", "sun"}:
        return motion("opacity", ".72;1;.84;1;.72", "3.2s", False)
    if name in {"play", "live", "record", "live_tv"}:
        return motion("opacity", ".72;1;.84;1", "1.9s", False)
    if name in {"pause", "stop", "check", "success"}:
        return motion("opacity", ".8;1;.8", "2.8s")
    if name in {"next", "forward", "seek_forward", "channels", "queue", "series", "ticker", "news"}:
        return motion("translate", "0 0;2.4 0;0 0", "2.2s")
    if name in {"prev", "back", "rewind", "seek_back"}:
        return motion("translate", "0 0;-2.4 0;0 0", "1.7s")
    if name in {"volume_up", "volume_down", "mute", "audio_track"}:
        return motion("opacity", ".58;1;.68;1;.58", "1.9s", False)
    if name in {"cart", "delivery", "orders"}:
        return motion("translate", "-1 0;2 0;-1 0", "3s")
    if name in {"location", "map", "guide"}:
        return motion("translate", "0 0;0 -2.5;0 0", "1.8s")
    if name in {"qr", "barcode"}:
        return motion("opacity", ".72;1;.72", "2.2s")
    if name in {"fullscreen", "aspect", "mirror", "pip"}:
        return motion("scale", "1;1.045;1", "2.6s")
    if name in {"gift", "add", "remove", "close", "open", "playlist_add"}:
        return motion("translate", "0 0;0 -1.7;0 0", "2.2s")
    if name in {"lock", "parental"}:
        return motion("translate", "0 0;0 -1.1;0 0", "3.1s")
    if name in {"music", "headphones", "mic", "podcast", "radio", "album", "lyrics"}:
        return motion("translate", "0 0;0 -1.8;0 0", "2.25s")
    if name in {"clock", "clock_face", "timer"}:
        return motion("rotate", "-1.5;1.5;0", "1s")
    if name == "search":
        return motion("translate", "0 0;1.5 -1;0 0;-1.5 1;0 0", "3s", False)
    if name in {"camera", "photo", "slideshow"}:
        return motion("opacity", ".68;1;.9;1", "2.4s", False)
    if name in {"power", "usb", "hdmi", "source", "input", "storage"}:
        return motion("opacity", ".7;1;.7", "2.6s")
    if name in {"login", "download", "install"}:
        return motion("translate", "0 -1;0 2;0 -1", "2.1s")
    if name in {"logout", "share", "export"}:
        return motion("translate", "0 0;2 0;0 0", "2.2s")
    if name in {"phone", "call"}:
        return motion("rotate", "-2;2;0", "1.8s")
    if name in {"price_tag", "ticket", "calendar", "offer"}:
        return motion("rotate", "-1.8;1.8;0", "2.8s")
    if name in {"chat", "message", "queue_num", "receipt", "payment", "wallet"}:
        return motion("opacity", ".78;1;.78", "2.7s")
    if name in {"night", "sleep"}:
        return motion("opacity", ".65;1;.75;1", "4s", False)
    if name in {"language", "menu", "menu_board", "grid", "apps", "keyboard"}:
        return motion("opacity", ".78;1;.88;1", "3.1s", False)
    if name in {"home", "restaurant", "store_front", "table", "kitchen", "food", "drink", "dessert"}:
        return motion("translate", "0 0;0 -1.2;0 0", "3.3s")
    if name in {"accessibility", "info", "profile", "remote", "subtitles", "temperature", "video"}:
        return motion("opacity", ".68;1;.82;1", "2.5s", False)
    if name in {"bookmark", "kids", "sports"}:
        return motion("translate", "0 0;0 -2;0 0", "1.9s")
    if name in {"edit", "offer"}:
        return motion("rotate", "-2.2;2.2;0", "2.2s")
    if name == "filter":
        return motion("rotate", "-3;3;0", "2.4s")
    if name == "game":
        return motion("translate", "-1.3 0;1.3 0;-1.3 0", "1.3s", False)
    if name == "movies":
        return motion("rotate", "0;360", "22s", False)
    if name == "recent":
        return motion("rotate", "-2;2;0", "2s")
    if name == "screensaver":
        return motion("translate", "-1 -1;1 1;-1 -1", "7s", False)
    if name == "speed":
        return motion("rotate", "-5;5;0", "1.4s")
    if name == "trash":
        return motion("rotate", "-3;3;0", "1.5s")
    if category == "player_music":
        return motion("translate", "0 0;0 -1.4;0 0", "2.6s")
    if category == "player_video":
        return motion("opacity", ".8;1;.8", "2.6s")
    if category == "launcher":
        return motion("translate", "0 0;0 -1.4;0 0", "3s")
    if category == "display":
        return motion("opacity", ".8;1;.8", "3.2s")
    if category == "tv":
        return motion("opacity", ".82;1;.82", "3.4s")
    return motion("translate", "0 0;0 -1.2;0 0", "3.2s")
def animate_equalizer(foreground: str) -> tuple[str, int]:
    count = 0
    def replace(match: re.Match[str]) -> str:
        nonlocal count
        x, y, height = match.group(1), int(match.group(2)), int(match.group(3))
        base = y + height
        low = max(8, round(height * 0.42))
        high = max(12, round(height * 0.82))
        delay = f"{count * 0.16:.2f}s"
        count += 1
        return (f'<rect x="{x}" y="{y}" width="8" height="{height}" rx="3" fill="url(#a)">'
                f'<animate attributeName="height" values="{height};{low};{high};{height}" '
                f'dur="1.25s" begin="{delay}" repeatCount="indefinite"/>'
                f'<animate attributeName="y" values="{y};{base-low};{base-high};{y}" '
                f'dur="1.25s" begin="{delay}" repeatCount="indefinite"/></rect>')
    result = re.sub(
        r'<rect x="(10|24|38|52)" y="(\d+)" width="8" height="(\d+)" rx="3" fill="url\(#a\)"/>',
        replace, foreground)
    return result, count

def animate_coffee(foreground: str) -> tuple[str, bool]:
    needle = ('<path d="M22 12 Q20 16 24 20 M32 12 Q30 16 34 20" '
              'fill="none" stroke="url(#a)" stroke-width="5" stroke-linecap="round" '
              'stroke-linejoin="round"/>')
    replacement = (
        '<path d="M22 12 Q20 16 24 20" fill="none" stroke="url(#a)" stroke-width="4" '
        'stroke-linecap="round"><animateTransform attributeName="transform" type="translate" '
        'values="0 2;0 -6;0 2" dur="2.3s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="0;1;0" dur="2.3s" repeatCount="indefinite"/></path>'
        '<path d="M32 12 Q30 16 34 20" fill="none" stroke="url(#a)" stroke-width="4" '
        'stroke-linecap="round"><animateTransform attributeName="transform" type="translate" '
        'values="0 2;0 -6;0 2" dur="2.3s" begin="1.15s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="0;1;0" dur="2.3s" begin="1.15s" '
        'repeatCount="indefinite"/></path>')
    if needle not in foreground:
        return foreground, False
    return foreground.replace(needle, replacement, 1), True

def animate_sun_rays(foreground: str) -> tuple[str, bool]:
    pattern = re.compile(
        r'<path d="(M32 10 V16[^"]*)" fill="none" stroke="url\(#a\)" '
        r'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    match = pattern.search(foreground)
    if not match:
        return foreground, False
    path = match.group(0)
    replacement = (
        '<g><animateTransform attributeName="transform" type="rotate" values="0 32 32;360 32 32" '
        'dur="24s" repeatCount="indefinite"/>' + path + '</g>')
    return foreground[:match.start()] + replacement + foreground[match.end():], True

def add_scanner(foreground: str) -> str:
    return foreground + (
        '<path d="M8 32 H56" fill="none" stroke="url(#a)" stroke-width="1.8" '
        'stroke-linecap="round" opacity="0"><animateTransform attributeName="transform" '
        'type="translate" values="0 -18;0 18" dur="2.4s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="0;.95;0" dur="2.4s" '
        'repeatCount="indefinite"/></path>')

def transform_svg(source: str, path: Path) -> str:
    name = path.stem.lower()
    category = path.parent.parent.name
    outer_at = source.find(OUTER)
    inner_at = source.find(INNER, outer_at)
    if outer_at < 0 or inner_at < 0:
        raise ValueError(f"{path}: expected V18 icon wrapper was not found")
    inner_open_end = inner_at + len(INNER)
    inner_close_end = find_g_end(source, inner_at)
    inner_close_start = inner_close_end - len("</g>")
    body = source[inner_open_end:inner_close_start]

    shadow_at = body.find(SHADOW)
    shadow_end = find_g_end(body, shadow_at) if shadow_at >= 0 else -1
    if shadow_at >= 0 and shadow_end < 0:
        raise ValueError(f"{path}: shadow group is malformed")
    shadow = body[:shadow_end] if shadow_at >= 0 else ""
    foreground = body[shadow_end:] if shadow_at >= 0 else body

    if name == "equalizer":
        foreground, bars = animate_equalizer(foreground)
        if bars != 4:
            raise ValueError(f"{path}: expected 4 independently animated bars, found {bars}")
        glyph_motion = ""
    elif name == "coffee":
        foreground, done = animate_coffee(foreground)
        glyph_motion = "" if done else semantic_motion(name, category)
    elif name == "weather_sun":
        foreground, done = animate_sun_rays(foreground)
        glyph_motion = "" if done else semantic_motion(name, category)
    else:
        glyph_motion = semantic_motion(name, category)

    if name in {"qr", "barcode"}:
        foreground = add_scanner(foreground)

    animated_foreground = (
        '<g transform="translate(32 32)"><g>' + glyph_motion
        + '<g transform="translate(-32 -32)">' + foreground
        + '</g></g></g>')
    rebuilt = (source[:outer_at] + OUTER + INNER + shadow + animated_foreground
               + '</g>' + source[inner_close_end:])
    root = ET.fromstring(rebuilt)
    if root.tag.split("}")[-1] != "svg":
        raise ValueError(f"{path}: invalid SVG root")
    animation_names = {"animate", "animateTransform"}
    if not any(el.tag.split("}")[-1] in animation_names for el in root.iter()):
        raise ValueError(f"{path}: no SMIL animation was added")
    if "<script" in rebuilt.lower() or "<style" in rebuilt.lower():
        raise ValueError(f"{path}: scripts or CSS are not allowed")
    return rebuilt

def main() -> None:
    all_before = sorted(ROOT.rglob("*.svg"))
    animated_before = sorted(ROOT.glob("*/animated/*.svg"))
    static_before = sorted(ROOT.glob("*/static/*.svg"))
    focused_before = sorted(ROOT.glob("*/focused/*.svg"))
    if not animated_before:
        raise SystemExit("No V18 animated SVG files were found")

    category_counts: dict[str, int] = {}
    for path in animated_before:
        original = path.read_text(encoding="utf-8")
        updated = transform_svg(original, path)
        path.write_text(updated, encoding="utf-8", newline="\n")
        category = path.parent.parent.name
        category_counts[category] = category_counts.get(category, 0) + 1

    all_after = sorted(ROOT.rglob("*.svg"))
    animated_after = sorted(ROOT.glob("*/animated/*.svg"))
    static_after = sorted(ROOT.glob("*/static/*.svg"))
    focused_after = sorted(ROOT.glob("*/focused/*.svg"))
    rel = lambda files: [p.relative_to(ROOT).as_posix() for p in files]
    if rel(all_before) != rel(all_after):
        raise SystemExit("SVG file list changed; refusing to continue")
    if rel(animated_before) != rel(animated_after):
        raise SystemExit("Animated icon paths changed; refusing to continue")
    if rel(static_before) != rel(static_after) or rel(focused_before) != rel(focused_after):
        raise SystemExit("Static or focused icon paths changed; refusing to continue")

    for path in animated_after:
        root = ET.parse(path).getroot()
        if root.tag.split("}")[-1] != "svg":
            raise SystemExit(f"Invalid SVG root: {path}")
        if not any(el.tag.split("}")[-1] in {"animate", "animateTransform"} for el in root.iter()):
            raise SystemExit(f"Missing animation: {path}")
    for path in static_after + focused_after:
        root = ET.parse(path).getroot()
        if any(el.tag.split("}")[-1] in {"animate", "animateTransform"} for el in root.iter()):
            raise SystemExit(f"Unexpected motion in static/focused file: {path}")

    lines = [
        "# ROYAL Design V18 — semantic motion",
        "",
        f"- Animated SVGs updated: **{len(animated_after)}**",
        f"- Static SVGs preserved: **{len(static_after)}**",
        f"- Focused SVGs preserved: **{len(focused_after)}**",
        f"- Total SVGs preserved: **{len(all_after)}**",
        "- Animation format: basic SVG SMIL using animate and animateTransform.",
        "- No JavaScript, CSS keyframes, filters, external assets, or file removals.",
        "- Motion is applied to icon glyphs or meaningful details, not the tile background.",
        "- The original SVG artwork remains visible as a static fallback when animation is unsupported.",
        "",
        "## Processed by category",
        "",
        "| Category | Animated SVGs |",
        "|---|---:|",
    ]
    for category, count in sorted(category_counts.items()):
        lines.append(f"| {category} | {count} |")
    lines += [
        "",
        "## Android 8 rendering note",
        "",
        "The assets use basic SVG elements and SMIL animation only. Android 8 devices need an SVG-capable renderer or WebView to play motion. A native ImageView/VectorDrawable parser that accepts only static vector paths will still show the unchanged icon artwork, but will not execute SMIL.",
        "",
    ]
    (ROOT / "MOTION-REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {len(animated_after)} animated SVGs. Preserved {len(static_after)} static, {len(focused_after)} focused and {len(all_after)} total SVG files.")

if __name__ == "__main__":
    main()
