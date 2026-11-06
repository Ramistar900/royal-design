#!/usr/bin/env python3
"""Build the ROYAL AUDIO catalog from original procedural cues and licensed field recordings."""
from __future__ import annotations

import array
import hashlib
import json
import math
import random
import subprocess
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "audio/catalog.json"
WAV_DIR = ROOT / "audio/assets/wav"
OGG_DIR = ROOT / "audio/assets/ogg"
WORK_DIR = ROOT / ".royal-audio-work"
RATE = 48000
CHANNELS = 2

SOURCES = {
    "weather.rain.natural": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Rain.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Rain.ogg",
        "creator": "ジダネ", "license": "CC0 1.0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution": None, "seconds": 16, "start": 0, "loop": True, "gain": 0.82,
    },
    "weather.thunderstorm.rain": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Rain_%281%29.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Rain_(1).ogg",
        "creator": "ezwa", "license": "CC0 1.0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution": None, "seconds": 16, "start": 0, "loop": True, "gain": 0.78,
    },
    "weather.thunderstorm.thunder": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/9/93/Thunder.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Thunder.ogg",
        "creator": "Bidgee", "license": "CC BY 3.0", "license_url": "https://creativecommons.org/licenses/by/3.0/",
        "attribution": "Bidgee", "seconds": 8, "start": 0, "loop": False, "gain": 0.68,
    },
    "nature.birds.general": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/80/Birds_singing_in_garden.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Birds_singing_in_garden.ogg",
        "creator": "ezwa", "license": "CC0 1.0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution": None, "seconds": 16, "start": 0, "loop": True, "gain": 0.70,
    },
    "nature.birds.morning": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/7/75/Birdsong_mild_sunny_day.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Birdsong_mild_sunny_day.ogg",
        "creator": "stephan", "license": "CC0 1.0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution": None, "seconds": 16, "start": 0, "loop": True, "gain": 0.70,
    },
    "nature.ocean.waves": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Waves.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Waves.ogg",
        "creator": "Dsw4", "license": "CC0 1.0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution": None, "seconds": 16, "start": 0, "loop": True, "gain": 0.72,
    },
    "nature.water.stream": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/26/Flowing-water-100019.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Flowing-water-100019.ogg",
        "creator": "Fg2", "license": "CC0 1.0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution": None, "seconds": 16, "start": 0, "loop": True, "gain": 0.72,
    },
    "nature.leaves.rustle": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/6/66/Leaves_in_summer.webm",
        "page": "https://commons.wikimedia.org/wiki/File:Leaves_in_summer.webm",
        "creator": "Joaquim Baeta", "license": "CC BY 4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Joaquim Baeta", "seconds": 16, "start": 0, "loop": True, "gain": 0.72,
    },
    "nature.wind.gentle": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Howling_wind.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Howling_wind.ogg",
        "creator": "Tvabutzku1234", "license": "CC0 1.0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution": None, "seconds": 16, "start": 0, "loop": True, "gain": 0.42,
    },
    "nature.owl.clear_night": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Owlcall.ogg",
        "page": "https://commons.wikimedia.org/wiki/File:Owlcall.ogg",
        "creator": "L. Shyamal", "license": "CC BY-SA 4.0", "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "attribution": "L. Shyamal", "seconds": 6, "start": 0, "loop": False, "gain": 0.72,
    },
}

EFFECTS = {
    "notification.message.new": ("two_up", 0.34),
    "notification.alert.general": ("double_low", 0.48),
    "notification.success": ("two_up", 0.43),
    "notification.failure": ("two_down", 0.52),
    "ui.button.tap.soft": ("click", 0.075),
    "ui.selection.confirm": ("click_high", 0.18),
    "ui.panel.open": ("whoosh_up", 0.16),
    "ui.panel.close": ("whoosh_down", 0.14),
    "ui.navigation.back": ("back", 0.12),
    "commerce.cart.add": ("click_high", 0.22),
    "commerce.order.received": ("three_up", 0.50),
    "commerce.payment.success": ("two_up", 0.44),
    "commerce.order.complete": ("three_up", 0.48),
    "media.play": ("click_high", 0.10),
    "media.pause": ("click_low", 0.10),
    "media.channel.changed": ("two_up", 0.18),
    "media.channel.connected": ("two_up", 0.34),
    "media.channel.disconnected": ("two_down", 0.43),
    "system.update.ready": ("two_up", 0.43),
    "system.build.success": ("three_up", 0.43),
    "system.build.failure": ("two_down", 0.56),
    "reminders.timer.finished": ("three_up", 0.68),
    "reminders.prayer.alert": ("two_warm", 0.49),
}

PATTERNS = {
    "two_up": [("tone", 0.02, 0.13, 760, 930, 0.24), ("tone", 0.18, 0.13, 980, 1220, 0.21)],
    "double_low": [("tone", 0.02, 0.16, 650, 650, 0.20), ("tone", 0.27, 0.15, 650, 650, 0.17)],
    "two_down": [("tone", 0.02, 0.20, 620, 460, 0.22), ("tone", 0.27, 0.19, 430, 320, 0.19)],
    "click": [("click", 0.0, 0.045, 0, 0, 0.24)],
    "click_high": [("click", 0.0, 0.025, 0, 0, 0.13), ("tone", 0.025, 0.12, 1040, 1320, 0.19)],
    "click_low": [("click", 0.0, 0.032, 0, 0, 0.16), ("tone", 0.02, 0.07, 540, 430, 0.09)],
    "whoosh_up": [("whoosh", 0.0, 0.15, 280, 760, 0.21)],
    "whoosh_down": [("whoosh", 0.0, 0.13, 760, 280, 0.18)],
    "back": [("tone", 0.01, 0.09, 650, 480, 0.15)],
    "three_up": [("tone", 0.02, 0.11, 620, 740, 0.19), ("tone", 0.17, 0.11, 800, 940, 0.18), ("tone", 0.32, 0.12, 1020, 1220, 0.17)],
    "two_warm": [("tone", 0.02, 0.19, 520, 620, 0.16), ("tone", 0.25, 0.19, 680, 780, 0.15)],
}

def require_tool(name: str) -> None:
    from shutil import which
    if not which(name):
        raise RuntimeError("Required executable is unavailable: " + name)

def run(args: list[str]) -> None:
    subprocess.run(args, check=True)

def pcm24(samples: array.array, channels: int) -> bytes:
    out = bytearray()
    for sample in samples:
        value = int(round(max(-0.95, min(0.95, float(sample))) * 8388607))
        if value < 0:
            value += 1 << 24
        out.extend((value & 255, (value >> 8) & 255, (value >> 16) & 255))
    if len(out) % (channels * 3):
        raise RuntimeError("Audio buffer is not frame-aligned.")
    return bytes(out)

def write_wav(path: Path, samples: array.array, channels: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not samples or max(abs(float(x)) for x in samples) < 0.00001:
        raise RuntimeError("Refusing to write an empty or silent WAV: " + str(path))
    with wave.open(str(path), "wb") as out:
        out.setnchannels(channels)
        out.setsampwidth(3)
        out.setframerate(RATE)
        out.writeframes(pcm24(samples, channels))

def encode_ogg(wav_path: Path, ogg_path: Path) -> None:
    ogg_path.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav_path),
         "-map_metadata", "-1", "-c:a", "libvorbis", "-q:a", "4", str(ogg_path)])
    if not ogg_path.is_file() or ogg_path.stat().st_size < 600:
        raise RuntimeError("OGG encoding failed: " + str(ogg_path))
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-v", "error", "-i", str(ogg_path), "-f", "null", "-"])

def add_tone(buf: array.array, start: float, length: float, f0: float, f1: float, gain: float) -> None:
    first = int(start * RATE)
    count = max(1, int(length * RATE))
    phase = 0.0
    for j in range(count):
        i = first + j
        if i >= len(buf):
            break
        t = j / RATE
        p = j / max(1, count - 1)
        frequency = f0 + (f1 - f0) * p
        phase += 2.0 * math.pi * frequency / RATE
        env = min(1.0, t / 0.008) * min(1.0, (length - t) / 0.025)
        env *= math.exp(-2.0 * t / max(length, 0.03))
        buf[i] += gain * env * (math.sin(phase) + 0.12 * math.sin(phase * 2.01))

def add_click(buf: array.array, length: float, gain: float, rng: random.Random) -> None:
    count = min(len(buf), max(1, int(length * RATE)))
    previous = 0.0
    for i in range(count):
        raw = rng.uniform(-1.0, 1.0)
        high = raw - previous * 0.84
        previous = raw
        buf[i] += gain * math.exp(-i / (RATE * 0.0045)) * high

def add_whoosh(buf: array.array, length: float, f0: float, f1: float, gain: float, rng: random.Random) -> None:
    count = min(len(buf), max(1, int(length * RATE)))
    state = 0.0
    phase = 0.0
    for i in range(count):
        p = i / max(1, count - 1)
        t = i / RATE
        state += 0.15 * (rng.uniform(-1.0, 1.0) - state)
        phase += 2.0 * math.pi * (f0 + (f1 - f0) * p) / RATE
        env = math.sin(math.pi * p) ** 1.4
        buf[i] += gain * env * (0.8 * state + 0.2 * math.sin(phase))

def build_effect(track_id: str, pattern: str, duration: float) -> array.array:
    buf = array.array("f", [0.0]) * max(1, int(duration * RATE))
    rng = random.Random(sum(ord(ch) for ch in track_id) + 5021)
    for kind, start, length, f0, f1, gain in PATTERNS[pattern]:
        if kind == "tone":
            add_tone(buf, start, length, f0, f1, gain)
        elif kind == "click":
            add_click(buf, length, gain, rng)
        elif kind == "whoosh":
            add_whoosh(buf, length, f0, f1, gain, rng)
    peak = max(abs(float(x)) for x in buf)
    if peak <= 0:
        raise RuntimeError("Silent effect generated: " + track_id)
    scale = min(1.0, 0.36 / peak)
    for i in range(len(buf)):
        buf[i] *= scale
    fade = min(int(0.003 * RATE), len(buf) // 4)
    for i in range(fade):
        buf[i] *= i / max(1, fade)
        buf[-1-i] *= i / max(1, fade)
    return buf

def fetch_source(track_id: str, spec: dict) -> Path:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    suffix = ".webm" if spec["url"].endswith(".webm") else ".ogg"
    target = WORK_DIR / (track_id.replace(".", "_") + suffix)
    request = urllib.request.Request(spec["url"], headers={
        "User-Agent": "ROYAL-AUDIO-asset-builder/1.0 (licensed sound-library production)"
    })
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as out:
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    out.write(block)
            if target.stat().st_size < 2048:
                raise RuntimeError("Downloaded file is too small: " + track_id)
            return target
        except Exception as exc:
            last_error = exc
            target.unlink(missing_ok=True)
    raise RuntimeError("Unable to fetch " + track_id + ": " + str(last_error))

def decode_source(track_id: str, spec: dict, source: Path) -> array.array:
    raw = WORK_DIR / (track_id.replace(".", "_") + ".f32le")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-ss", str(spec["start"]), "-i", str(source), "-t", str(spec["seconds"]),
         "-map", "0:a:0", "-vn", "-ac", str(CHANNELS), "-ar", str(RATE),
         "-f", "f32le", str(raw)])
    data = array.array("f")
    with raw.open("rb") as handle:
        data.frombytes(handle.read())
    raw.unlink(missing_ok=True)
    if len(data) < RATE * CHANNELS * 1.5:
        raise RuntimeError("Source audio too short or missing: " + track_id)
    return data

def prepare_ambience(data: array.array, spec: dict) -> array.array:
    frames = len(data) // CHANNELS
    if spec["loop"]:
        fade = min(int(0.7 * RATE), frames // 5)
        if fade < 1000:
            raise RuntimeError("Loop source too short for safe crossfade.")
        output = array.array("f", data[fade * CHANNELS:(frames - fade) * CHANNELS])
        for j in range(fade):
            p = j / max(1, fade - 1)
            tail_gain = math.cos(p * math.pi / 2)
            head_gain = math.sin(p * math.pi / 2)
            tail = frames - fade + j
            for channel in range(CHANNELS):
                output.append(float(data[tail * CHANNELS + channel]) * tail_gain +
                              float(data[j * CHANNELS + channel]) * head_gain)
    else:
        output = array.array("f", data)
        fade = min(int(0.25 * RATE), frames // 5)
        for j in range(fade):
            factor = 1.0 - j / max(1, fade)
            for channel in range(CHANNELS):
                output[-(j + 1) * CHANNELS + channel] *= factor
    peak = max(abs(float(x)) for x in output)
    rms = math.sqrt(sum(float(x) * float(x) for x in output) / len(output))
    if peak < 0.00001 or rms < 0.00001:
        raise RuntimeError("Natural source is silent.")
    scale = min((0.105 * spec["gain"]) / rms, (0.60 * spec["gain"]) / peak)
    for i in range(len(output)):
        output[i] *= scale
    return output

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def write_credits() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    lines = [
        "# ROYAL AUDIO — Asset source and licence credits",
        "",
        "The short interface, notification, commerce, media and system cues are original non-verbal procedural sound designs created for ROYAL AUDIO. They contain no third-party samples, speech, or music.",
        "",
        "Natural ambience sources were selected from Wikimedia Commons. Files were trimmed, level-adjusted, converted to 48 kHz stereo PCM 24-bit WAV, and exported as OGG Vorbis. Looping sources receive a short crossfade at the loop boundary.",
        "",
        "| Catalog ID | Creator | Source recording | Licence | Changes |",
        "|---|---|---|---|---|",
    ]
    for track_id, spec in SOURCES.items():
        lines.append("| " + track_id + " | " + spec["creator"] + " | [" + track_id + "](" + spec["page"] + ") | [" + spec["license"] + "](" + spec["license_url"] + ") | Trimmed, level-adjusted, resampled; loop-crossfaded where applicable; WAV/OGG conversion |")
    lines += [
        "",
        "## Licence notes",
        "- CC0 sources are available for reuse without attribution requirements; creator and source are still recorded here for provenance.",
        "- CC BY 3.0 thunder and CC BY 4.0 leaves retain creator attribution and a link to the licence.",
        "- The owl recording remains under CC BY-SA 4.0 after adaptation; the adapted owl files are distributed under the same share-alike licence.",
        "- The source contributor described the owl call as believed to be an owl; species identification was not visually confirmed.",
        "- Original synthesized cues are licensed as original ROYAL AUDIO project assets; no external audio sample libraries are used.",
        "",
    ]
    target = ROOT / "audio/licenses/ATTRIBUTIONS.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")

def update_catalog() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    all_ids = {track["id"] for track in catalog["tracks"]}
    expected_ids = set(EFFECTS) | set(SOURCES)
    if all_ids != expected_ids:
        missing = sorted(all_ids - expected_ids)
        extra = sorted(expected_ids - all_ids)
        raise RuntimeError("Asset recipe/catalog mismatch. Unbuilt IDs: " + str(missing) + "; unknown recipes: " + str(extra))
    for track in catalog["tracks"]:
        track_id = track["id"]
        wav_rel = track["integration"]["asset_paths"]["wav_master"]
        ogg_rel = track["integration"]["asset_paths"]["ogg_runtime"]
        wav_path = ROOT / wav_rel
        ogg_path = ROOT / ogg_rel
        if not wav_path.is_file() or not ogg_path.is_file():
            raise RuntimeError("Missing output for " + track_id)
        with wave.open(str(wav_path), "rb") as audio:
            if audio.getsampwidth() != 3 or audio.getframerate() != RATE:
                raise RuntimeError("Unexpected WAV master format: " + track_id)
            if audio.getnframes() <= 0:
                raise RuntimeError("Empty WAV master: " + track_id)
            duration_ms = round(audio.getnframes() * 1000 / audio.getframerate())
        if track_id in EFFECTS:
            licence = {
                "name": "Original ROYAL AUDIO sound design",
                "source": "Created in this repository by scripts/build_royal_audio_assets.py; no third-party samples",
                "redistribution_allowed": True,
                "attribution": "ROYAL AUDIO project",
                "performer_consent": None,
                "modifications": "Original procedural synthesis; no speech or sampled material.",
            }
            method = "original_procedural_sound_design"
        else:
            spec = SOURCES[track_id]
            licence = {
                "name": spec["license"],
                "source": spec["page"],
                "redistribution_allowed": True,
                "attribution": spec["attribution"],
                "performer_consent": None,
                "creator": spec["creator"],
                "license_url": spec["license_url"],
                "modifications": "Trimmed/loop-crossfaded where applicable, level-adjusted, resampled to 48 kHz stereo PCM 24-bit WAV and exported as OGG Vorbis.",
            }
            if spec["license"] == "CC BY-SA 4.0":
                licence["adapted_asset_license"] = "CC BY-SA 4.0"
            method = "licensed_natural_field_recording"
        track["status"] = "built"
        track["format"] = "ogg"
        track["path"] = ogg_rel
        track["master_path"] = wav_rel
        track["duration_ms"] = duration_ms
        track["language"] = None
        track["license"] = licence
        track["audio_hashes"] = {"wav_sha256": sha256(wav_path), "ogg_sha256": sha256(ogg_path)}
        track["production"] = {
            "method": method,
            "automated_validation": "passed",
            "device_playback_test": "pending",
        }
    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main() -> None:
    require_tool("ffmpeg")
    WAV_DIR.mkdir(parents=True, exist_ok=True)
    OGG_DIR.mkdir(parents=True, exist_ok=True)
    total = len(EFFECTS) + len(SOURCES)
    built = 0
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    print("Building " + str(len(EFFECTS)) + " original non-verbal effects.")
    for track_id, (pattern, duration) in EFFECTS.items():
        samples = build_effect(track_id, pattern, duration)
        wav_path = WAV_DIR / (track_id + ".wav")
        ogg_path = OGG_DIR / (track_id + ".ogg")
        write_wav(wav_path, samples, 1)
        encode_ogg(wav_path, ogg_path)
        built += 1
        print("Built original effect " + track_id + " (" + str(built) + "/" + str(total) + ")")
    print("Preparing " + str(len(SOURCES)) + " licensed nature/weather recordings.")
    for track_id, spec in SOURCES.items():
        source = fetch_source(track_id, spec)
        decoded = decode_source(track_id, spec, source)
        prepared = prepare_ambience(decoded, spec)
        wav_path = WAV_DIR / (track_id + ".wav")
        ogg_path = OGG_DIR / (track_id + ".ogg")
        write_wav(wav_path, prepared, CHANNELS)
        encode_ogg(wav_path, ogg_path)
        built += 1
        print("Prepared natural ambience " + track_id + " (" + str(built) + "/" + str(total) + ")")
    if built != total:
        raise RuntimeError("Incomplete asset build.")
    write_credits()
    update_catalog()
    print("PASS: all " + str(total) + " WAV/OGG pairs built. Catalog state is built, pending device playback tests.")

if __name__ == "__main__":
    main()
