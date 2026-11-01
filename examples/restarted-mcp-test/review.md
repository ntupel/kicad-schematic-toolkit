# Restarted MCP: default-field test

Restarted the Python worker serving this chat through the MCP server's existing automatic-respawn behavior. The previous worker was PID 25408; the replacement worker was PID 45892. The Node MCP transport remained connected. A new U1 insertion returned the updated default field positions, confirming that the replacement loaded the changed implementation.

Generated this fresh 11-component AC-coupled non-inverting amplifier through KiCad MCP tools. No field-position, auto-placement, field-visibility override, or direct schematic-file editing was used. Added only symbols, wires, no-connect marks, and explanatory annotations.

Saved every symbol's initial property expressions before wiring. After generation and export, every property expression still matched that snapshot. This includes all component references/values, power labels, and PWR_FLAG text.

Validation:
- KiCad structural/load check passed.
- ERC: zero errors, warnings, or informational violations.
- Eleven physical components found in the exported netlist.
- All eleven specified pin groups matched, including three unused-pin groups.
- +12V, -12V, and GND matched their intended domains.
- Actual KiCad rendering inspected at whole-sheet and readable detail scales.
- No overlapping component text, power labels, or notes observed. Feedback and the main signal path are continuously wired and traceable.
- No visual repair was needed.

Circuit: C1 = 100 nF and R1 = 100 kohm provide AC coupling and bias return; R2 = 10 kohm and R3 = 100 kohm set nominal gain 11; R4 = 100 ohm is a series output resistor; C2/C3 = 100 nF bypass the +/-12 V supplies. Assumes low source impedance and high load impedance. Nominal input corner approximately 15.9 Hz; no simulation or hardware test was performed.
