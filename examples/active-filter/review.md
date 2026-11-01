# Active-filter skill test

Tested the updated kicad-readable-schematics skill on a TL081 Sallen-Key second-order low-pass filter.

- R1 = R2 = 15.8 kohm; C1 = C2 = 10 nF.
- R3 = 10 kohm; R4 = 5.90 kohm; ideal passband gain K = 1.59 V/V.
- Ideal natural frequency f0 = 1007.31 Hz; Q = 0.70922; relative -3 dB frequency approximately 1010.31 Hz. These are analytical nominal values, not simulation or measurements.
- Topology and equations checked against [TI SLOA024B, sections 3 and 3.4](https://www.ti.com/lit/an/sloa024b/sloa024b.pdf). Capacitor reference names in this drawing differ from TI's figure; the connectivity follows the same topology.

## Verification

KiCad 10.0.7 loaded the schematic successfully. ERC: zero errors, warnings, or information-level violations. All 11 exported connected-pin groups exactly match the intended pin groups. The +12V, -12V, and GND domains were also checked by name. PWR_FLAG symbols represent the assumed external regulated supply; unused offset-null and NC pins are explicitly marked.

## Visual review

Reference/Value positions and supply labels were assigned before the first render using the updated field-placement guidance. Inspected KiCad's PDF rendering at full-sheet and detail scales. The first render passed: no field-placement repairs were needed.

- Input flows left to right through R1 and R2 into the non-inverting input.
- C1 connects the output back to the RC junction through a continuous upper wire path.
- R4 connects the output to the inverting input through a continuous lower wire path; R3 goes to ground.
- Resistor and capacitor fields are outside their bodies; U1 fields are clear of pin text and unused-pin markers.
- Supply names are clear of wires and arrows; ground names do not collide with notes.
- No disconnected signal net labels or wire crossings are needed. Shared supply/ground symbols intentionally connect the bypass block.

This verifies schematic construction and readability. It does not include SPICE simulation, tolerance analysis, or hardware testing. Embedded library symbols are included in the editable schematic; PCB footprints were not assigned for this drawing test.
