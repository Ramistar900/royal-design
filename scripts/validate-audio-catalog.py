from pathlib import Path
import hashlib, json, re, wave

ROOT = Path(__file__).resolve().parents[1]

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

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
    assert track.get("kind") in {"effect", "ambience"}, "Only non-verbal effects and natural ambience are allowed"
    if track["kind"] == "ambience":
        assert track.get("category") in {"nature", "weather"}
        ambience_integration = track.get("integration", {})
        playback_mode = ambience_integration.get("playback_mode")
        assert playback_mode in {"loop", "spaced_random_overlay"}
        if playback_mode == "spaced_random_overlay":
            assert track_id in {"weather.thunderstorm.thunder", "nature.owl.clear_night"}
        assert ambience_integration.get("applications") == ["royalplus_launcher"]
        assert ambience_integration.get("activation") in {"weather_condition", "spaced_random_overlay", "user_opt_in"}
        if ambience_integration.get("activation") == "spaced_random_overlay":
            assert track["id"] == "weather.thunderstorm.thunder"
            assert ambience_integration.get("spacing_seconds") == {"minimum": 420, "maximum": 900}
        if track_id == "nature.owl.clear_night":
            assert track.get("category") == "nature"
            assert ambience_integration.get("playback_mode") == "spaced_random_overlay"
            assert ambience_integration.get("activation") == "weather_condition"
            assert ambience_integration.get("scene") == "clear_night"
            assert ambience_integration.get("weather_codes") == [0, 1]
            assert ambience_integration.get("local_time_window") == {
                "start": "19:00",
                "end": "06:00",
                "end_exclusive": True,
                "timezone": "device_local",
            }
            assert ambience_integration.get("spacing_seconds") == {
                "minimum": 1800,
                "maximum": 3600,
            }
            assert ambience_integration.get("user_opt_in") is False
    integration = track.get("integration", {})
    assert integration.get("event_key") == track_id, f"{track_id}: event_key must match stable ID"
    allowed_apps = {"almalaki", "royal_tv", "rami", "royalplus_launcher", "sinjar_tv_show"}
    app_targets = integration.get("applications", [])
    assert app_targets and len(app_targets) == len(set(app_targets)), f"{track_id}: missing or duplicate app targets"
    assert set(app_targets) <= allowed_apps, f"{track_id}: unknown application key"
    maximum_suggestion = 12000 if track.get("kind") == "ambience" else 2000
    assert isinstance(integration.get("suggested_duration_ms"), int) and 50 <= integration["suggested_duration_ms"] <= maximum_suggestion
    expected_wav = f"audio/assets/wav/{track_id}.wav"
    expected_ogg = f"audio/assets/ogg/{track_id}.ogg"
    assert integration.get("asset_paths", {}).get("wav_master") == expected_wav
    assert integration.get("asset_paths", {}).get("ogg_runtime") == expected_ogg
    assert track.get("status") in {"planned", "built", "ready"}
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
        assert isinstance(track.get("duration_ms"), int) and track["duration_ms"] > 0
        wav_path = ROOT / track["master_path"]
        ogg_path = ROOT / track["path"]
        with wave.open(str(wav_path), "rb") as audio:
            assert audio.getframerate() == 48000, f"{track_id}: WAV must be 48 kHz"
            assert audio.getsampwidth() == 3, f"{track_id}: WAV master must be 24-bit PCM"
            assert audio.getnchannels() in {1, 2} and audio.getnframes() > 0
        with ogg_path.open("rb") as audio:
            assert audio.read(4) == b"OggS", f"{track_id}: invalid OGG container"
        hashes = track.get("audio_hashes", {})
        for key, path in (("wav_sha256", wav_path), ("ogg_sha256", ogg_path)):
            expected = hashes.get(key, "")
            assert re.fullmatch(r"[0-9a-f]{64}", expected), f"{track_id}: missing SHA-256 for {key}"
            assert sha256_file(path) == expected, f"{track_id}: SHA-256 mismatch for {key}"
        if track["status"] == "built":
            production = track.get("production", {})
            assert production.get("automated_validation") == "passed"
            assert production.get("device_playback_test") == "pending"
        if track["status"] == "ready":
            qa = track.get("quality_check", {})
            assert qa.get("phone") and qa.get("tv"), f"{track_id}: device playback verification is required before ready"

assert len(tracks) >= 15
print(f"PASS: {len(categories)} categories and {len(tracks)} entries; no voice tracks; planned assets, ambience routing and licence metadata validated.")
