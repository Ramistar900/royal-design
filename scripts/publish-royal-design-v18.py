#!/usr/bin/env python3
"""Safely validate and publish the ROYAL Design V18 icon archive preview."""
from pathlib import Path
from zipfile import ZipFile
import shutil
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/"icons/v18/restaurant-tv-glossy/restaurant_tv_icons_v3_glossy.zip"
DEST=ROOT/"preview/royal-design/v18"
EXPECTED={
 "store":(45,True,False),
 "tv":(57,True,False),
 "display":(45,True,False),
 "launcher":(25,True,True),
 "player_music":(21,True,False),
 "player_video":(20,True,False),
}
def fail(message):
 raise SystemExit("V18 ERROR: "+message)

if not ARCHIVE.is_file():
 fail("uploaded V18 ZIP is missing")
with ZipFile(ARCHIVE) as z:
 names=[n for n in z.namelist() if not n.endswith("/")]
 if len(names)!=453:
  fail(f"expected 453 archive files, found {len(names)}")
 svg=[n for n in names if n.lower().endswith(".svg")]
 if len(svg)!=451:
  fail(f"expected 451 SVG files, found {len(svg)}")
 if "preview.html" not in names or "INDEX.txt" not in names:
  fail("preview.html or INDEX.txt is missing")
 for category,(expected,has_motion,has_focused) in EXPECTED.items():
  static={Path(n).stem for n in svg if n.startswith(category+"/static/")}
  animated={Path(n).stem for n in svg if n.startswith(category+"/animated/")}
  focused={Path(n).stem for n in svg if n.startswith(category+"/focused/")}
  if len(static)!=expected or len(animated)!=expected:
   fail(f"{category}: expected {expected} static and animated pairs; found {len(static)} and {len(animated)}")
  if static!=animated:
   fail(f"{category}: static/animated names do not match")
  if has_focused and (len(focused)!=expected or focused!=static):
   fail(f"{category}: focused variants are incomplete")
  if not has_focused and focused:
   fail(f"{category}: unexpected focused assets")
 # Validate every SVG as XML and verify motion separation.
 for name in svg:
  info=ZipFile  # keep validation below independent of extraction paths
  raw=z.read(name)
  try:
   root=ET.fromstring(raw)
  except Exception as exc:
   fail(f"invalid SVG XML {name}: {exc}")
  if not root.tag.endswith("svg") or not root.attrib.get("viewBox"):
   fail(f"SVG root/viewBox invalid: {name}")
  lower=raw.decode("utf-8","replace").lower()
  if "<script" in lower or "<foreignobject" in lower:
   fail(f"active content found: {name}")
  is_motion="/animated/" in name
  has_animation=any(node.tag.split("}")[-1] in {"animate","animateTransform","animateMotion","set"} for node in root.iter()) or "animation:" in lower or "@keyframes" in lower
  if is_motion and not has_animation:
   fail(f"animated asset has no animation declaration: {name}")
  if not is_motion and has_animation:
   fail(f"static/focused asset contains animation: {name}")
 # Never delete a folder not created by this generator.
 marker=DEST/".generated-by-v18-extract"
 if DEST.exists() and not marker.exists():
  fail("destination exists but is not marked as generated; refusing to overwrite")
 if DEST.exists():
  shutil.rmtree(DEST)
 DEST.mkdir(parents=True)
 for name in names:
  if name=="preview.html":
   target=DEST/"index.html"
  else:
   target=DEST/name
  if target.resolve().is_relative_to(DEST.resolve()) is False:
   fail(f"unsafe archive path: {name}")
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_bytes(z.read(name))
 (DEST/".generated-by-v18-extract").write_text("Generated from the checked V18 archive. Do not edit by hand.\n",encoding="utf-8")
print("V18 passed: 213 icon concepts, 451 valid SVGs, 25 focused launcher variants, preview extracted.")
