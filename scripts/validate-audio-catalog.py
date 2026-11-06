from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "audio/catalog.json").read_text(encoding="utf-8"))
assert data.get("schema_version") == 1 and data.get("library") == "ROYAL AUDIO"
assert data.get("preferred_runtime_format") == "ogg"

defaults = data.get("defaults", {})
assert defaults.get("human_voice_clips") is False, "Human voice clips are excluded from V1"
assert defaults.get("sound_effects") is True
assert defaults.get("background_music") is False
assert "human_voice_gender" not in defaults
formats = set(data.get("supported_formats", []))
assert formats <= {"ogg", "wav"} and "ogg" in formats

categories = data.get("categories", [])
cat_ids = [item["id"] for item in categories]
assert len(cat_ids) == len(set(cat_ids))
required_categories = {"notifications", "ui", "commerce", "media", "system", "reminders"}
assert required_categories <= set(cat_ids)
assert "voice" not in cat_ids

tracks = data.get("tracks", [])
ids = [item.get("id", "") for item in tracks]
assert len(ids) == len(set(ids)), "duplicate audio track ID"
for track in tracks:
    track_id = track["id"]
    assert re.fullmatch(r"[a-z0-9]+(?:[._-][a-z0-9]+)*", track_id), f"invalid ID: {track_id}"
    assert track.get("category") in cat_ids
    assert track.get("kind") == "effect", "Only non-verbal sound effects are allowed"
    assert track.get("status") in {"planned", "ready"}
    assert track.get("name", {}).get("ar") and track.get("name", {}).get("en")
    licence = track.get("license", {})
    assert "redistribution_allowed" in licence and licence.get("name") and licence.get("source")
    if track["status"] == "planned":
        assert not track.get("path") and not track.get("master_path") and not track.get("format")
    else:
        assert track.get("format") in formats
        for field in ("path", "master_path"):
            value = track.get(field)
            assert value and not Path(value).is_absolute() and ".." not in Path(value).parts
            assert (ROOT / value).is_file(), f"{track_id}: missing {field} {value}"
        assert licence["redistribution_allowed"] is True, f"{track_id}: redistribution rights not verified"
        assert licence["name"] not in {"pending review", "unknown"}
        assert licence["source"] not in {"pending original recording", "unknown"}

assert len(tracks) >= 15
print(f"PASS: {len(categories)} categories and {len(tracks)} effects-only entries; no voice tracks; assets and licence metadata validated.")
