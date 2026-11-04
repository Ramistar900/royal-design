from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "preview/v9-icon-catalog/index.html"
ARCHIVE = ROOT / "ROYAL_Android_Icons_v2.zip"
html = PAGE.read_text(encoding="utf-8")

collections = {
    "v3": ("icons/v3/svg", 10),
    "v4": ("icons/v4", 12),
    "v5": ("icons/v5/finance-shopping/svg", 20),
    "v6": ("icons/v6/colorful-finance-shopping/svg", 12),
    "v7": ("icons/v7/colorful-controls-media/svg", 26),
    "v8": ("icons/v8/colorful-media-product-badges/svg", 23),
    "v9": ("icons/v9/cafe-orders/svg", 37),
}
for version, (folder, expected) in collections.items():
    files = sorted((ROOT / folder).glob("*.svg"))
    assert len(files) == expected, f"{version}: expected {expected} SVG files, found {len(files)}"
    for file in files:
        assert file.stem in html, f"{version}: {file.name} missing from catalog data"

with ZipFile(ARCHIVE) as archive:
    names = archive.namelist()
    svg = [n for n in names if n.startswith("ROYAL_Android_Icons_v2/svg/") and n.endswith(".svg")]
    drawable = [n for n in names if n.startswith("ROYAL_Android_Icons_v2/android/res/drawable/") and n.endswith(".xml")]
    assert len(svg) == 22, f"v2: expected 22 SVGs, found {len(svg)}"
    assert len(drawable) == 22, f"v2: expected 22 Android drawables, found {len(drawable)}"
    for item in svg:
        icon_id = Path(item).stem
        assert icon_id in html, f"v2: {icon_id} missing from catalog data"

assert 'Android: @drawable/' in html, "Android resource ID display missing"
assert 'تحميل أرشيف v2' in html, "v2 archive download action missing"
assert 'ROYAL Design' in html and 'id="catalog"' in html, "Catalog page structure missing"

# Resource IDs are indexed by collection to avoid collisions between versions.
assert "const androidIds=" in html, "Versioned Android resource map missing"
assert 'Android Resource: غير متوفر في هذا الإصدار' in html, "Missing explicit fallback for collections without Android resources"
assert 'const rid=androidIds[g.v]?.[id]' in html, "Resource lookup must be scoped to the icon version"
\nprint("PASS: 140 standalone SVG entries + 22 archived v2 icons; 22 v2 Android drawables; Android resource-ID display present.")
