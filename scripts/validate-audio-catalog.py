from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "audio/catalog.json"
ASSET_ROOT = ROOT / "audio/assets"
SUPPORTED_FORMATS = {"ogg", "wav", "mp3"}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,79}$")

catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
assert catalog.get("schema_version") == 1, "unsupported audio catalog schema"
assert catalog.get("library") == "ROYAL AUDIO", "unexpected library name"
assert catalog.get("library_version"), "library_version is required"
assert catalog.get("preferred_runtime_format") == "ogg", "OGG must remain the preferred runtime format"
assert set(catalog.get("supported_formats", [])) <= SUPPORTED_FORMATS
assert catalog.get("defaults", {}).get("human_voice_clips") is True
assert catalog.get("defaults", {}).get("music") is True

categories = catalog.get("categories")
assert isinstance(categories, list) and categories, "categories must be a non-empty list"
category_ids = [item["id"] for item in categories]
assert len(category_ids) == len(set(category_ids)), "duplicate category ID"
required_categories = {"notifications", "ui", "commerce", "media", "voice", "music"}
assert required_categories <= set(category_ids), "one or more required categories are missing"

tracks = catalog.get("tracks")
assert isinstance(tracks, list), "tracks must be a list"
track_ids = set()
asset_paths = set()
for track in tracks:
    track_id = track.get("id", "")
    assert ID_PATTERN.fullmatch(track_id), f"invalid track ID: {track_id!r}"
    assert track_id not in track_ids, f"duplicate track ID: {track_id}"
    track_ids.add(track_id)

    assert track.get("category") in category_ids, f"{track_id}: unknown category"
    assert track.get("name", {}).get("en"), f"{track_id}: English name is required"
    assert track.get("name", {}).get("ar"), f"{track_id}: Arabic name is required"

    fmt = track.get("format", "").lower()
    assert fmt in SUPPORTED_FORMATS, f"{track_id}: unsupported format"
    assert track.get("path", "").startswith(f"audio/assets/{fmt}/"), (
        f"{track_id}: asset must live in audio/assets/{fmt}/"
    )
    relative = Path(track["path"])
    assert not relative.is_absolute() and ".." not in relative.parts, f"{track_id}: unsafe asset path"
    assert relative.as_posix() not in asset_paths, f"{track_id}: duplicate asset path"
    asset_paths.add(relative.as_posix())
    assert (ROOT / relative).is_file(), f"{track_id}: missing asset {relative}"
    assert isinstance(track.get("duration_ms"), int) and track["duration_ms"] > 0
    assert track.get("license", {}).get("name"), f"{track_id}: license name is required"
    assert track.get("license", {}).get("source"), f"{track_id}: license/source evidence is required"
    assert track.get("license", {}).get("redistribution_allowed") is True, (
        f"{track_id}: redistribution rights must be explicitly verified"
    )

print(
    f"PASS: ROYAL AUDIO catalog valid; {len(categories)} categories, "
    f"{len(tracks)} tracks, all referenced assets and license declarations verified."
)
