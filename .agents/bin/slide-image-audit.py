#!/usr/bin/env python3
"""Audit slide image usage: which slides have images, which don't, and suggest unused images."""
import re
import sys
from path import Path

REPO = Path(__file__).parent.parent.parent
CONTENT = REPO / "presentation" / "content"
IMAGES = REPO / "presentation" / "images"

def main():
    available = {f.name for f in IMAGES.glob("*") if f.is_file() and not f.name.endswith(".py")}
    used = set()
    slides_without = []
    slides_with = []

    for f in sorted(CONTENT.glob("*.md")):
        if f.name.endswith("~"):
            continue
        text = f.read_text()
        match = re.search(r"^image:\s*(.+)", text, re.MULTILINE)
        if match:
            img = match.group(1).strip().strip('"').replace("../images/", "")
            used.add(img)
            exists = (IMAGES / img).exists()
            slides_with.append((f.name, img, exists))
        else:
            slides_without.append(f.name)

    unused = sorted(available - used)

    print("SLIDES WITH IMAGES:")
    for name, img, exists in slides_with:
        status = "ok" if exists else "MISSING!"
        print(f"  {name:<45} {img:<50} {status}")

    print(f"\nSLIDES WITHOUT IMAGES ({len(slides_without)}):")
    for name in slides_without:
        print(f"  {name}")

    print(f"\nUNUSED IMAGES ({len(unused)}):")
    for img in unused:
        print(f"  {img}")

    print(f"\nSummary: {len(slides_with)} slides have images, {len(slides_without)} don't, {len(unused)} images unused")
    return 0

if __name__ == "__main__":
    sys.exit(main())
