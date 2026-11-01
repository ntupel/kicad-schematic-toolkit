"""Regression tests for the symbol/field overlaps observed in rendered schematics."""

import pytest
import sexpdata

from commands.dynamic_symbol_loader import DynamicSymbolLoader


def place(tmp_path, library, symbol, angle=0, mirror=False):
    full = f"{library}:{symbol}"
    offset = -3.81 if symbol == "GND" else 3.556
    value_pos = f"0 {offset} 0" if library in ("power", "CustomPower") else "0 0 90"
    source = f'''(kicad_sch (version 20260101) (generator "test")
      (uuid "00000000-0000-0000-0000-000000000001")
      (lib_symbols (symbol "{full}"
        (property "Reference" "R" (at 2.032 0 90)
          (effects (font (size 1.27 1.27))))
        (property "Value" "{symbol}" (at {value_pos})
          (effects (font (size 1.27 1.27))))
        (symbol "{symbol}_1_1"
          (rectangle (start -1.27 -2.54) (end 1.27 2.54))
          (pin passive line (at 0 3.81 270) (length 1.27) (number "1"))
          (pin passive line (at 0 -3.81 90) (length 1.27) (number "2")))))
      (sheet_instances (path "/" (page "1"))))'''
    path = tmp_path / "fields.kicad_sch"
    path.write_text(source, encoding="utf-8")
    loader = DynamicSymbolLoader(project_path=tmp_path)
    loader.create_component_instance(path, library, symbol, "R1", value="10k",
                                     x=50.8, y=50.8, angle=angle, mirror_y=mirror)
    root = sexpdata.loads(path.read_text(encoding="utf-8"))
    instance = next(n for n in root if isinstance(n, list) and str(n[0]) == "symbol")
    return {str(n[1]): n for n in instance if isinstance(n, list) and str(n[0]) == "property"}


def position(prop):
    return next(n[1:] for n in prop if isinstance(n, list) and str(n[0]) == "at")


@pytest.mark.parametrize("symbol", ["R", "R_US", "C", "C_Polarized"])
@pytest.mark.parametrize("angle", [0, 90, 180, 270])
@pytest.mark.parametrize("mirror", [False, True])
def test_passive_fields_clear_body_and_read_horizontally(tmp_path, symbol, angle, mirror):
    props = place(tmp_path, "Device", symbol, angle, mirror)
    ref, val = position(props["Reference"]), position(props["Value"])
    assert ref[2] == val[2] == angle % 180
    assert val[1] - ref[1] >= 2.54 - 1e-6
    if angle % 180:
        assert val[1] < 50.8 - 1.27  # entirely above the horizontal body
    else:
        assert ref[0] > 50.8 + 1.27  # left-justified beyond the vertical body
        assert "(justify left)" in sexpdata.dumps(props["Value"])
    assert '(font (size 1.27 1.27))' in sexpdata.dumps(props["Value"])


@pytest.mark.parametrize("angle", [0, 90, 180, 270])
@pytest.mark.parametrize("mirror", [False, True])
@pytest.mark.parametrize("symbol,offset", [("GND", -3.81), ("+12V", 3.556)])
def test_power_label_follows_library_to_sheet_transform(tmp_path, angle, mirror, symbol, offset):
    props = place(tmp_path, "CustomPower", symbol, angle, mirror)
    px, py, pa = position(props["Value"])
    # Independently enumerated transform of (0, offset) in the library.
    dx, dy = {0: (0, -offset), 90: (-offset, 0),
              180: (0, offset), 270: (offset, 0)}[angle]
    assert px == pytest.approx(50.8 + (-dx if mirror else dx), abs=0.001)
    assert py == pytest.approx(50.8 + dy, abs=0.001)
    assert pa == 0


@pytest.mark.parametrize("symbol", ["GND", "+12V"])
@pytest.mark.parametrize("angle", [0, 90, 180, 270])
def test_power_name_clears_graphics_and_pin_envelope(tmp_path, symbol, angle):
    props = place(tmp_path, "power", symbol, angle)
    px, py, pa = position(props["Value"])
    assert pa == angle % 180
    if angle % 180:
        assert abs(px - 50.8) > 3.81
    else:
        assert abs(py - 50.8) > 3.81


def test_custom_library_keeps_transformed_default(tmp_path):
    props = place(tmp_path, "Custom", "R", 0, True)
    assert position(props["Reference"]) == pytest.approx([48.768, 50.8, 90])
    assert position(props["Value"]) == pytest.approx([50.8, 50.8, 90])


def test_amplifier_fields_are_outside_pin_envelope(tmp_path):
    props = place(tmp_path, "Amplifier_Operational", "Example")
    assert position(props["Reference"])[0] > 52.07
    assert position(props["Reference"])[1] < 46.99
    assert position(props["Value"])[1] > position(props["Reference"])[1]
