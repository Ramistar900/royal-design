#!/usr/bin/env python3
"""Validate ROYAL app collections, static pairs, original metadata and separate motion fallbacks."""
import json,re
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MANIFEST=ROOT/"icons/app-collections.json"; GALLERY=ROOT/"preview/royal-design/index.html"
EXPECTED={"V10":("almalaki",48),"V11":("royal-tv",8),"V12":("royal-plus",8),"V13":("rs-tv",8),"V14":("rami-developer",8),"V15":("royal-audio",12)}
def fail(m): raise SystemExit("ERROR: "+m)
data=json.loads(MANIFEST.read_text(encoding="utf-8")); apps=data.get("versions",[])
if len(apps)!=6: fail("expected six app collections")
seen=set(); count=0; motion_count=0
for app in apps:
 ver=app.get("version"); slug,n=EXPECTED.get(ver,(None,None))
 if not slug or app.get("slug")!=slug: fail(f"unexpected app {ver}/{app.get('slug')}")
 icons=app.get("icons",[])
 if len(icons)!=n: fail(f"{ver}: expected {n} icons, found {len(icons)}")
 keys=set()
 for icon in icons:
  key=icon.get("key","")
  if not re.fullmatch(r"[a-z0-9_-]+",key) or key in keys: fail(f"{ver}: invalid/duplicate key {key}")
  keys.add(key)
  if not icon.get("label_ar") or not icon.get("label_en"): fail(f"{ver}/{key}: missing labels")
  rights=icon.get("rights",{})
  if rights.get("origin")!="original_royal" or rights.get("license")!="ROYAL_ORIGINAL": fail(f"{ver}/{key}: provenance missing")
  variants=icon.get("variants",{})
  if set(variants)!={"2d","3d"}: fail(f"{ver}/{key}: static pair missing")
  for style,rel in variants.items():
   p=(ROOT/rel).resolve()
   if ROOT not in p.parents or not p.is_file(): fail(f"missing/unsafe {rel}")
   try: root=ET.parse(p).getroot()
   except Exception as e: fail(f"invalid XML {rel}: {e}")
   raw=p.read_text(encoding="utf-8")
   if not root.tag.endswith("svg") or not root.attrib.get("viewBox"): fail(f"invalid SVG root {rel}")
   # Provenance is maintained in the manifest for all variants; SVG files need not duplicate metadata.
   if "<script" in raw or "<foreignObject" in raw: fail(f"active content in {rel}")
   if "<animate" in raw or "<animateTransform" in raw: fail(f"animation embedded in static file {rel}")
  if ver=="V10":
   motion=icon.get("motion")
   if not motion: fail(f"V10/{key}: motion mapping missing")
   p=(ROOT/motion).resolve()
   if ROOT not in p.parents or not p.is_file(): fail(f"motion file missing {motion}")
   try: root=ET.parse(p).getroot()
   except Exception as e: fail(f"invalid motion SVG {motion}: {e}")
   raw=p.read_text(encoding="utf-8")
   expected_fallback="../../2d/"+key+".svg"
   if "static_fallback="+expected_fallback not in raw or "reduced_motion=use_static_fallback" not in raw: fail(f"fallback metadata path is invalid {motion}")
   if 'href="'+expected_fallback+'"' not in raw: fail(f"motion art does not reuse its static counterpart {motion}")
   fallback=(p.parent.parent.parent/"2d"/(key+".svg")).resolve()
   if not fallback.is_file(): fail(f"motion fallback target missing {fallback}")
   if "<animate" not in raw and "<animateTransform" not in raw: fail(f"animation missing {motion}")
   motion_count+=1
  count+=1
 seen.add(ver)
if seen!=set(EXPECTED): fail("some app collections are absent")
tot=data.get("totals",{})
if tot.get("concepts")!=count or tot.get("flat_svg")!=count or tot.get("dimensional_svg")!=count: fail("concept/static totals mismatch")
if tot.get("motion_svg")!=motion_count: fail("motion total mismatch")
html=GALLERY.read_text(encoding="utf-8")
for x in ("embeddedManifest","motion","aria-pressed"): 
 if x not in html: fail("gallery missing feature "+x)
print(f"ROYAL Design check passed: {len(apps)} apps, {count} concepts, {2*count} static SVGs, {motion_count} motion SVGs.")
