#!/usr/bin/env python3
"""Convert ROYAL V10-V15 static SVG pairs into Android VectorDrawable resources.

Animated SVG files are intentionally excluded: SVG SMIL and external <image>
references are not VectorDrawable features. Their static 2D assets remain the
runtime fallback until each motion is authored as a native AnimatedVectorDrawable.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "app-icon-validation" / "build" / "generated" / "royal-app-icons"
COLLECTIONS = {
    "almalaki": ("icons/v10/almalaki", 48),
    "royal_tv": ("icons/v11/royal-tv", 8),
    "royal_plus": ("icons/v12/royal-plus", 8),
    "rs_tv": ("icons/v13/rs-tv", 8),
    "rami_developer": ("icons/v14/rami-developer", 8),
    "royal_audio": ("icons/v15/royal-audio", 12),
}

def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        raise SystemExit(
            f"Command failed ({result.returncode}): {' '.join(command)}"
        )

def main() -> None:
    total = 0
    for flavor, (relative_dir, expected) in COLLECTIONS.items():
        collection = ROOT / relative_dir
        output = OUTPUT_ROOT / flavor / "res" / "drawable-anydpi-v24"
        output.mkdir(parents=True, exist_ok=True)
        count = 0
        for style in ("2d", "3d"):
            source_dir = collection / style
            sources = sorted(source_dir.glob("*.svg"))
            if len(sources) != expected:
                raise SystemExit(
                    f"{relative_dir}/{style}: expected {expected} SVGs, found {len(sources)}"
                )
            for source in sources:
                # vdt rejects unsupported SVG features rather than silently
                # changing the artwork; safe normalization remains permitted.
                run(["vdt", "check", str(source)])
                resource_name = f"royal_{flavor}_{source.stem}_{style}"
                destination = output / f"{resource_name}.xml"
                run([
                    "vdt", "convert", str(source),
                    "--size", "128",
                    "--pretty",
                    "-o", str(destination),
                ])
                if not destination.is_file() or destination.stat().st_size == 0:
                    raise SystemExit(f"VectorDrawable output missing: {destination}")
                count += 1
        if count != expected * 2:
            raise SystemExit(f"{flavor}: expected {expected * 2} resources, got {count}")
        print(f"PASS {flavor}: {count} static VectorDrawables")
        total += count
    print(f"PASS total: {total} static Android VectorDrawables across six app collections")

if __name__ == "__main__":
    main()
