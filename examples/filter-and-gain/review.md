# Extended skill test: 17-component circuit

## Workflow exercised

Before drawing, specified 17 physical components, their electrical roles, ten connected nets, six intentionally unused op-amp pins, functional relationships, and conventional pattern bindings. The exact specification is in circuit-description.json, with a readable version in circuit-description.md. Power symbols and ERC flags are not counted as physical components.

Generated a Sallen-Key low-pass stage followed by a non-inverting gain stage. Selected upper capacitive feedback around U1, lower resistive feedback around U1 and U2, a direct interstage wire, and separate identified bypass pairs. Reference/Value and power-label positions were assigned before rendering. No optimization solver was used; the agent selected conventional arrangements and KiCad MCP tools created the drawing.

## Electrical checks

- KiCad loaded and structurally validated the schematic successfully.
- ERC: 0 errors, 0 warnings, 0 informational violations.
- Exported netlist exactly matches all 17 expected references and values.
- All 16 connected-pin groups match the pre-drawing specification: ten connected nets and six intentionally unused singleton pins.
- +12V, -12V, and GND also match by name and remain distinct.
- External regulated supply enters J3: pin 1 +12V, pin 2 GND, pin 3 -12V. Flags represent that external source.

## Visual review

Inspected the actual KiCad PDF rendering at whole-sheet and readable detail scales. The first rendering passed; no text-placement repairs were required.

- Main path reads left to right through the filter into the gain stage and output connector.
- C1, R4, and R6 each have a continuous, visibly traceable feedback path.
- Distinct output branch junctions avoid four-way crossings.
- C2 and the gain-reference resistors have clear ground branches.
- Component names and values are clear of symbol bodies, pins, and wires.
- Supply and ground labels are clear of wires, arrows, and notes.
- Supply entry and each amplifier's bypass pair are separate, identified groups.
- No disconnected signal net labels were used. Shared supply and ground symbols intentionally connect the power groups.

## Scope

Nominal ideal f0 is approximately 1.007 kHz and Q approximately 0.709. U1 passband gain is 1.59 V/V; U2 gain is 2 V/V; combined passband gain is 3.18 V/V. Assumes a low-impedance source, high-impedance load, and linear op-amp operation. This test validates schematic generation and readability, not SPICE response, component tolerances, or hardware operation. No PCB footprints were assigned.

Editable schematic includes embedded symbols. Preview is a crop of KiCad's rendering, not a separately redrawn illustration.
