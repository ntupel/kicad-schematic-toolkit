# Use MCP defaults; repair only observed problems

The updated KiCad MCP fixes library-to-sheet coordinate conversion and provides readable initial fields for stock passives, operational amplifiers, and power symbols. A fresh schematic generated after restarting the worker passed visual review with every initial field unchanged. Use these defaults for new symbols; preserve existing fields during unrelated edits.

Do not call field-position tools, field auto-placement, or visibility overrides before the first rendered review merely as a precaution. Do not rewrite property coordinates directly. Reserve space for the default text while placing components and routing wires. If the active MCP version lacks the improvements, review its actual output and repair demonstrated defects rather than assuming which fields are wrong.

## Reserve space for the whole symbol

Treat the body, pin names/numbers, no-connect marks, visible properties, and nearby wires as a single occupied region. Reserve a separate clear area for Reference and Value. Account for the complete text width, justification, and multiline height rather than only its anchor point. Keep space for power-symbol names before placing explanatory notes.

Use consistent horizontal reading direction for ordinary Reference/Value text. Put the reference above the value, with sufficient separation for the actual font size. For 1.27 mm text, approximately 2.54 mm between line centers and 1.27 mm clearance from neighboring graphics are useful starting points, not guaranteed collision-free dimensions. Increase clearance for long names or dense pin text.

## Repair guidance after visual review finds a defect

| Item | Candidate repair |
|---|---|
| Vertical resistor | Reference and value stacked beside the body, usually on its right; both read horizontally. Keep the value out of the resistor rectangle and away from the vertical wire. |
| Horizontal resistor | Reference and value stacked above or below the body, both reading horizontally. Choose the side with a free text area; keep both clear of the horizontal wire. |
| Capacitor | Reference above value beside the plates, usually on the right. Leave clearance from plates and the supply/return wires. Use the same arrangement for paired bypass capacitors. |
| Op-amp | Reference and value outside the triangle and all pin graphics. For a right-facing amplifier with a feedback loop below, an upper-right text area is often suitable. Inspect supply pins, offset-null pins, no-connect marks, and the output corridor before choosing it. |
| Upward supply symbol | Supply name above the arrow with a visible gap, rather than on the vertical supply wire below it. |
| Downward ground symbol | Ground name below the ground graphic. Reserve this space before placing notes or another circuit block. |
| Downward negative-supply symbol | Name below or beside the arrow in clear space. Use a side position if the feedback corridor lies below; do not collide with supply-pin numbers or null-pin marks. |
| PWR_FLAG | Keep its electrical anchor and diamond intact. Its Value text may be hidden when redundant and crowded; keep actual rail names visible. Flags must represent an intentionally externally driven rail, not merely silence ERC. |
| Connector | Keep reference and value outside its body and pin number, without covering the wire leaving the connector. |

Use these positions only to repair a documented visual problem, not as a blanket override of the MCP defaults. Preserve clear existing project conventions. Move fields rather than moving electrical anchors merely to improve text placement.

## Apply through the available tools

- Record each defect with sheet, reference, field, and visible consequence. Inspect the field-position tool's current schema; if several fields need repair, use `batch_set_schematic_property_positions` only for those affected fields. Do not auto-place every field to fix a local issue. Leave clear fields unchanged.
- Do not assume a field angle of zero always renders horizontally after a symbol rotation. In the tested tool/KiCad combination, the vertical resistor used field angle 0, while the resistor rotated 90 degrees used field angle 90 to obtain horizontal text. This is an observed combination, not a universal transform rule. Check current tool semantics and rendered results before reusing it.
- Preserve visibility of references and component values. Hide only intentionally redundant fields, such as PWR_FLAG Value text; never hide important rail names or component values to conceal collisions.
- Recheck text regions after wiring and after any field movement. In particular, a note's anchor may be at its bottom: moving a note slightly below a ground symbol can still leave its top line overlapping the ground name.
- Confirm at readable zoom that values are outside component bodies, op-amp fields clear every pin, supply names clear wires, and notes clear all power labels. ERC cannot check these conditions.
- Render again after any repair and repeat the affected visual and electrical checks. Report whether defaults passed unchanged or list the targeted repairs. When explicitly testing default placement, optionally snapshot the initial property expressions and compare them with the delivered file.
