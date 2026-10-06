#!/usr/bin/env python3
"""Compose official logos onto light, GitHub-safe SVG badge backgrounds.

Original source assets remain unchanged. Generated badges embed their source
content and contain no scripts or external resource references.
"""

from __future__ import annotations

import base64
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET


ASSETS = Path(__file__).resolve().parent / "profile-assets"
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)

LOGOS = (
    ("blinkit", "png", 100, 24, "Blinkit"),
    ("google", "svg", 75, 24, "Google"),
    ("ncu", "svg", 98, 75, "The NorthCap University"),
    ("meesho", "svg", 90, 21, "Meesho"),
)


def tag(name: str) -> str:
    return f"{{{SVG}}}{name}"


def validate(root: ET.Element) -> None:
    for element in root.iter():
        local = element.tag.rsplit("}", 1)[-1]
        if local in {"script", "foreignObject"}:
            raise ValueError(f"Disallowed SVG element: {local}")
        for key, value in element.attrib.items():
            attribute = key.rsplit("}", 1)[-1].lower()
            if attribute.startswith("on"):
                raise ValueError(f"Disallowed SVG event: {key}")
            if attribute in {"href", "src"} and not value.startswith(
                ("#", "data:image/png;base64,")
            ):
                raise ValueError(f"External resource: {value}")
            if "url(" in value and "url(#" not in value:
                raise ValueError(f"External SVG paint resource: {value}")
        if local == "style" and element.text:
            css = element.text
            if "@import" in css or ("url(" in css and "url(#" not in css):
                raise ValueError("External stylesheet resource")


def generate() -> None:
    for name, extension, width, height, label in LOGOS:
        source = ASSETS / f"{name}.{extension}"
        original = source.read_bytes()
        digest = hashlib.sha256(original).digest()
        badge_width, badge_height = width + 24, height + 24
        badge = ET.Element(
            tag("svg"),
            {
                "width": str(badge_width),
                "height": str(badge_height),
                "viewBox": f"0 0 {badge_width} {badge_height}",
                "role": "img",
                "aria-labelledby": f"{name}-title",
            },
        )
        ET.SubElement(badge, tag("title"), {"id": f"{name}-title"}).text = label
        ET.SubElement(
            badge,
            tag("rect"),
            {
                "width": str(badge_width),
                "height": str(badge_height),
                "rx": "12",
                "fill": "#f7f5f1",
            },
        )
        placement = {
            "x": "12",
            "y": "12",
            "width": str(width),
            "height": str(height),
            "preserveAspectRatio": "xMidYMid meet",
        }
        if extension == "png":
            data = base64.b64encode(original).decode("ascii")
            ET.SubElement(
                badge,
                tag("image"),
                {**placement, f"{{{XLINK}}}href": f"data:image/png;base64,{data}"},
            )
        else:
            nested = ET.fromstring(original)
            if nested.tag != tag("svg") or "viewBox" not in nested.attrib:
                raise ValueError(f"Source is not a scalable SVG: {source}")
            nested.attrib.update(placement)
            badge.append(nested)
        validate(badge)
        output = ASSETS / f"{name}-badge.svg"
        ET.indent(badge, space="  ")
        ET.ElementTree(badge).write(output, encoding="utf-8", xml_declaration=True)
        validate(ET.parse(output).getroot())
        if hashlib.sha256(source.read_bytes()).digest() != digest:
            raise ValueError(f"Original asset changed: {source}")
        print(f"{output.name}: {badge_width} x {badge_height}, validated")


if __name__ == "__main__":
    generate()
