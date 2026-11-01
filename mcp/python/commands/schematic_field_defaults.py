"""Initial field positions for familiar schematic symbols, in sheet coordinates.

These defaults clear the symbol itself, not future wires or neighboring symbols.
Explicit field-placement tools remain authoritative after insertion.
"""

import math
import re

import sexpdata


def library_offset(dx, dy, angle, mirror_y=False):
    """Library Y-up -> sheet Y-down -> CCW rotation -> sheet-space mirror."""
    radians = math.radians(angle)
    sx, sy = dx, -dy
    rx = sx * math.cos(radians) + sy * math.sin(radians)
    ry = -sx * math.sin(radians) + sy * math.cos(radians)
    return (-rx if mirror_y else rx), ry


def field_effects(effects, justify):
    """Change alignment only; retain font size, bold/italic and visibility."""
    effects = re.sub(r"\s*\(justify\b[^)]*\)", "", effects)
    if justify:
        effects = effects.rstrip()[:-1] + f" (justify {justify}))"
    return effects


def readable_positions(library, symbol, block, x, y, angle, mirror_y, unit, height):
    """Return Reference/Value (x, y, angle, justification), or no override.

    Bound only the selected unit's graphics and pin anchors. Restrict conventions
    to stock two-terminal R/C symbols and the operational-amplifier library;
    custom libraries retain their transformed library defaults.
    """
    passive = library == "Device" and symbol in {"R", "R_US", "C", "C_Polarized", "C_Polarized_US"}
    amplifier = library == "Amplifier_Operational"
    power = library == "power" and symbol != "PWR_FLAG"
    if not block or not (passive or amplifier or power) or angle % 90:
        return {}
    try:
        data = sexpdata.loads(block)
        points = []

        def collect(node):
            if not isinstance(node, list) or not node:
                return
            if str(node[0]) in {"xy", "start", "end", "center", "at"} and len(node) >= 3:
                if isinstance(node[1], (int, float)) and isinstance(node[2], (int, float)):
                    points.append(library_offset(node[1], node[2], angle, mirror_y))
            for child in node[1:]:
                collect(child)

        for child in data[2:]:
            if isinstance(child, list) and child and str(child[0]) == "symbol":
                match = re.search(r"_(\d+)_(\d+)$", str(child[1]))
                if match and int(match[1]) in (0, unit) and int(match[2]) in (0, 1):
                    collect(child)
        if not points:
            return {}
        min_y = min(py for _, py in points)
        max_x = max(px for px, _ in points)
        gap = max(1.27, height)
        pitch = max(2.54, 2 * height)
        # KiCad interprets a field angle relative to the symbol's orientation.
        horizontal_angle = angle % 180
        if power:
            value = next((n for n in data[2:] if isinstance(n, list)
                          and str(n[0]) == "property" and str(n[1]) == "Value"), None)
            at = next((n for n in value or [] if isinstance(n, list) and str(n[0]) == "at"), None)
            if at is None:
                return {}
            dx, dy = library_offset(float(at[1]), float(at[2]), angle, mirror_y)
            if abs(dy) >= abs(dx):
                edge = min_y if dy < 0 else max(py for _, py in points)
                py = y + edge + (-1 if dy < 0 else 1) * (gap + height / 2)
                return {"Value": (x, py, horizontal_angle, "")}
            edge = min(px for px, _ in points) if dx < 0 else max_x
            return {"Value": (x + edge + (-gap if dx < 0 else gap), y,
                              horizontal_angle, "right" if dx < 0 else "left")}
        if passive and angle % 180 == 90:
            return {
                "Reference": (x, y + min_y - gap - pitch, horizontal_angle, ""),
                "Value": (x, y + min_y - gap, horizontal_angle, ""),
            }
        right = x + max_x + gap
        top = y + min_y - gap if amplifier else y - pitch / 2
        return {
            "Reference": (right, top, horizontal_angle, "left"),
            "Value": (right, top + pitch, horizontal_angle, "left"),
        }
    except (ValueError, TypeError, IndexError):
        return {}
