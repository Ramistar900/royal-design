from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"audio/catalog.json").read_text(encoding="utf-8"))
assert data.get("schema_version")==1 and data.get("library")=="ROYAL AUDIO"
assert data.get("preferred_runtime_format")=="ogg"
defaults=data.get("defaults",{})
assert defaults.get("human_voice_clips") is True and defaults.get("sound_effects") is True
assert defaults.get("human_voice_gender") == "both", "Both male and female human voice variants are required"
assert defaults.get("music_mode") == "effects", "ROYAL AUDIO V1 uses sound effects only"
assert defaults.get("background_music") is False, "Background music is excluded from V1"
formats=set(data.get("supported_formats",[]))
assert formats <= {"ogg","wav"} and "ogg" in formats
categories=data.get("categories",[])
cat_ids=[x["id"] for x in categories]
assert len(cat_ids)==len(set(cat_ids)) and {"notifications","ui","commerce","media","system","reminders","voice"} <= set(cat_ids)
tracks=data.get("tracks",[])
ids=[x.get("id","") for x in tracks]
assert len(ids)==len(set(ids)), "duplicate audio track ID"
for track in tracks:
 tid=track["id"]
 assert re.fullmatch(r"[a-z0-9]+(?:[._-][a-z0-9]+)*",tid), f"invalid ID: {tid}"
 assert track.get("category") in cat_ids and track.get("kind") in {"effect","voice"}
 assert track.get("status") in {"planned","ready"}
 assert track.get("name",{}).get("ar") and track.get("name",{}).get("en")
 licence=track.get("license",{})
 assert "redistribution_allowed" in licence and licence.get("name") and licence.get("source")
 if track["status"]=="planned":
  assert not track.get("path") and not track.get("master_path") and not track.get("format")
 else:
  assert track.get("format") in formats
  for field in ("path","master_path"):
   value=track.get(field)
   assert value and not Path(value).is_absolute() and ".." not in Path(value).parts
   assert (ROOT/value).is_file(), f"{tid}: missing {field} {value}"
  assert licence["redistribution_allowed"] is True, f"{tid}: redistribution rights not verified"
  assert licence["name"] not in {"pending review","unknown"}
  assert licence["source"] not in {"pending original recording","unknown"}
  if track["kind"]=="voice": assert track.get("language")
assert len(tracks)>=20
print(f"PASS: {len(categories)} categories and {len(tracks)} ROYAL AUDIO entries; V1 scope, IDs, assets, and licence metadata validated.")
