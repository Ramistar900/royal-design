#!/usr/bin/env python3
"""Validate stable ROYAL Design icon codes across V16-V21."""
import json,re,shutil,subprocess,tempfile
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"preview/royal-design/icon-codes.json"
EXPECTED={"V16":99,"V17":413,"V18":213,"V19":22,"V20":25,"V21":26}
PATTERN=re.compile(r"^[A-Z][0-9]{5}$")
def fail(message): raise SystemExit("ERROR: "+message)
data=json.loads(REGISTRY.read_text(encoding="utf-8"));items=data.get("items",[])
versions=Counter(x.get("version") for x in items)
if dict(versions)!=EXPECTED: fail(f"version coverage mismatch: {dict(versions)}")
identity_to_code={};code_to_identity={}
for item in items:
 code=item.get("code","");identity=item.get("identity","")
 if not PATTERN.fullmatch(code): fail(f"invalid code for {identity}: {code}")
 if not identity or not item.get("key") or not item.get("version"): fail(f"incomplete record: {item}")
 if code[0]!=item.get("color_letter"): fail(f"color prefix mismatch: {identity}")
 if identity in identity_to_code and identity_to_code[identity]!=code: fail(f"identity has multiple codes: {identity}")
 if code in code_to_identity and code_to_identity[code]!=identity: fail(f"code reused: {code}")
 identity_to_code[identity]=code;code_to_identity[code]=identity
 if item["version"] in {"V18","V19","V20","V21"}:
  for path in item.get("assets",{}).values():
   if not (ROOT/path).is_file(): fail(f"missing local asset: {path}")
 if item["version"] == "V19" and "static" not in item.get("assets",{}):
  fail(f"static asset missing: {identity}")
 if item["version"] in {"V20","V21"} and not {"static","animated"}.issubset(item.get("assets",{})):
  fail(f"static/animated pair missing: {identity}")
if len(code_to_identity)!=data.get("counts",{}).get("unique_codes"): fail("unique code count mismatch")
if len(identity_to_code)!=data.get("counts",{}).get("unique_icons"): fail("unique icon count mismatch")
v16={x["key"]:x["code"] for x in items if x["version"]=="V16"}
v17={x["key"]:x["code"] for x in items if x["version"]=="V17"}
if any(v17.get(k)!=v for k,v in v16.items()): fail("V16/V17 shared keys have different codes")
# Verify that every web gallery actually loads the registry, exposes copy controls,
# and has syntactically valid inline JavaScript.
PAGES=[
 ROOT/"gallery/index.html",
 ROOT/"preview/royal-design/v18/index.html",
 ROOT/"preview/royal-design/v19/index.html",
 ROOT/"preview/royal-design/v20/index.html",
 ROOT/"preview/royal-design/v21/index.html",
]
node=shutil.which("node")
if not node: fail("Node.js is required to validate gallery scripts")
for page in PAGES:
 html=page.read_text(encoding="utf-8")
 if "data-copy-code" not in html or "icon-codes.json" not in html:
  fail(f"code search/copy UI missing from {page.relative_to(ROOT)}")
 scripts=re.findall(r"<script>(.*?)</script>",html,re.S)
 if not scripts: fail(f"missing inline JavaScript: {page.relative_to(ROOT)}")
 for script in scripts:
  with tempfile.NamedTemporaryFile("w",suffix=".js",encoding="utf-8") as temp:
   temp.write(script);temp.flush()
   result=subprocess.run([node,"--check",temp.name],capture_output=True,text=True)
   if result.returncode: fail(f"JavaScript syntax error in {page.relative_to(ROOT)}: {result.stderr}")
print(f"ROYAL icon codes passed: {len(items)} edition records, {len(identity_to_code)} unique icons, V16-V21 covered; all five gallery pages passed JavaScript checks.")
