from pathlib import Path
import json
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

# v2 is now a first-class catalog collection with individual SVG files.
v2_files = {
    "account_circle.svg", "android_device.svg", "apps.svg", "arrow_back.svg",
    "arrow_forward.svg", "battery_full.svg", "bluetooth.svg", "cast.svg",
    "download.svg", "folder.svg", "help.svg", "info.svg", "keyboard.svg",
    "menu.svg", "more_vert.svg", "notifications_active.svg", "qr_code.svg",
    "refresh.svg", "screen_share.svg", "tune.svg", "warning.svg", "wifi.svg",
}
v2_dir = ROOT / "icons/v2/svg"
actual_v2 = {file.name for file in v2_dir.glob("*.svg")}
assert actual_v2 == v2_files, (
    f"v2 SVG files mismatch; missing={sorted(v2_files - actual_v2)}, "
    f"unexpected={sorted(actual_v2 - v2_files)}"
)
for filename in sorted(v2_files):
    source = (v2_dir / filename).read_text(encoding="utf-8")
    assert "<svg" in source and "</svg>" in source, f"v2: invalid SVG content in {filename}"
    assert filename in html, f"v2: source filename {filename} is not indexed by the page"
    assert f'"{filename}"' in html, f"v2: source filename {filename} is missing from the map"

with ZipFile(ARCHIVE) as archive:
    names = archive.namelist()
    archive_svg = [n for n in names if n.startswith("ROYAL_Android_Icons_v2/svg/") and n.endswith(".svg")]
    drawable = [n for n in names if n.startswith("ROYAL_Android_Icons_v2/android/res/drawable/") and n.endswith(".xml")]
    assert len(archive_svg) == 22, f"v2 archive: expected 22 SVGs, found {len(archive_svg)}"
    assert len(drawable) == 22, f"v2 archive: expected 22 Android drawables, found {len(drawable)}"
    archive_v2_names = {Path(name).name for name in archive_svg}
    assert archive_v2_names == v2_files, "v2 source filenames do not match the original archive"
    for member in archive_svg:
        filename = Path(member).name
        assert archive.read(member) == (v2_dir / filename).read_bytes(), (
            f"v2: {filename} differs from the original archived SVG"
        )

assert 'Android: @drawable/' in html, "Android resource ID display missing"
assert 'ROYAL Design' in html and 'id="catalog"' in html, "Catalog page structure missing"
assert "const androidIds=" in html, "Versioned Android resource map missing"
assert 'Android Resource: غير متوفر في هذا الإصدار' in html, "Missing explicit fallback for collections without Android resources"
assert 'const rid=androidIds[g.v]?.[id]' in html, "Resource lookup must be scoped to the icon version"
assert "const v2SourceFiles=" in html, "v2 source filename mapping is missing"
assert "img.src='../../icons/v2/svg/'+v2SourceFiles[id]" in html, "v2 cards are not wired to the individual SVG directory"
assert "g.archive?v2SourceFiles[id]" in html, "v2 source filenames are not displayed on their cards"
assert "SVG داخل أرشيف v2" not in html, "v2 cards must show individual SVG previews, not archive placeholders"
assert "فتح SVG" in html, "Individual SVG open action is missing"


# Verify the machine-readable index and every indexed asset path.
CATALOG = ROOT / "icons/catalog.json"
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
entries = catalog["icons"]
assert len(entries) == 162, f"expected 162 indexed icon concepts, found {len(entries)}"
assert len({(item["version"], item["key"]) for item in entries}) == len(entries), "duplicate version/key pair"
with ZipFile(ARCHIVE) as archive:
    archive_names = set(archive.namelist())
    for item in entries:
        assert (ROOT / item["svg"]).is_file(), f"missing indexed SVG: {item['svg']}"
        if item["android_drawable"]:
            assert (ROOT / item["android_drawable"]).is_file(), f"missing Android drawable: {item['android_drawable']}"
        if item["android_archive_member"]:
            assert item["android_archive_member"] in archive_names, f"missing V2 Android resource: {item['android_archive_member']}"
        for key in ("animated_svg", "android_animated_drawable", "motion_base_drawable"):
            if item[key]:
                assert (ROOT / item[key]).is_file(), f"missing indexed motion asset: {item[key]}"
        for path in item["animator_resources"]:
            assert (ROOT / path).is_file(), f"missing indexed animator: {path}"

expected_versions = {"v2": 22, "v3": 10, "v4": 12, "v5": 20, "v6": 12, "v7": 26, "v8": 23, "v9": 37}
for version, expected in expected_versions.items():
    actual = sum(item["version"] == version for item in entries)
    assert actual == expected, f"{version}: expected {expected} indexed items, found {actual}"

print("PASS: 162 catalog entries; all SVG, Android, animated, animator, and V2 archive paths verified.")
