#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path("preview/royal-design")
EXPECTED={"v19":("muslim",18),"v20":("sports",25),"v21":("weather",26)}
ANIM={"animate","animateTransform"}
for version,(folder,count) in EXPECTED.items():
    base=ROOT/version
    static=sorted((base/folder/"static").glob("*.svg"))
    animated=sorted((base/folder/"animated").glob("*.svg"))
    assert len(static)==count,(version,"static",len(static),count)
    assert len(animated)==count,(version,"animated",len(animated),count)
    assert {p.stem for p in static}=={p.stem for p in animated},(version,"variant mismatch")
    for path in static+animated:
        root=ET.parse(path).getroot()
        assert root.tag.endswith("svg"),path
        assert root.attrib.get("viewBox")=="0 0 128 128",path
        assert root.attrib.get("width")=="128" and root.attrib.get("height")=="128",path
        names=[node.tag.split("}")[-1] for node in root.iter()]
        assert not ({"script","filter","foreignObject"} & set(names)),path
        if "static" in path.parts:
            assert not (ANIM & set(names)),("animation in static",path)
        else:
            assert ANIM & set(names),("missing animation",path)
    assert (base/"manifest.json").is_file()
    assert (base/"index.html").is_file()
print("V19/V20/V21 SVG validation passed: 69 concepts, 138 SVG variants.")
