# Conventional circuit patterns

These are relative layout motifs, not electrically complete circuits. Apply only when the actual topology matches. Preserve device pin mapping, polarity, component values, and manufacturer requirements. Adapt spacing and orientation to the sheet rather than imposing fixed coordinates.

| Motif | Preferred arrangement | Connections that should remain visible |
|---|---|---|
| Resistor divider | Two resistors stacked vertically between the source or rail and return; tap exits sideways toward its consumer. | Both resistors and the tap; directly connect a nearby sensing input. |
| RC low-pass | Series resistor along the left-to-right signal path; shunt capacitor below the output node toward return. | Input through resistor to output, with a clear capacitor branch. |
| RC high-pass | Series capacitor along the signal path; shunt bias or return resistor below the receiving node. | Capacitor-to-receiver node and its resistor branch. |
| Non-inverting amplifier | Input enters the non-inverting input from the left; output exits right. Arrange feedback resistor from output back to the inverting node in a clear corridor, with the gain-setting resistor toward its reference. | Entire local feedback path and reference branch. Do not assume the reference is ground. |
| Sallen-Key low-pass | Two series resistors run left to right toward the non-inverting input; the shunt capacitor drops toward the reference. Route the capacitor from the resistor junction to the output in an upper corridor, and the amplifier's negative feedback in a separate lower corridor when the pinout permits. | Both distinct feedback paths, the RC junction, and the shunt branch. For a unity-gain variant, preserve its actual direct negative-feedback connection rather than adding gain resistors. |
| Inverting amplifier / summing stage | Input resistors approach the inverting summing node from the left; feedback resistor loops from output to the same node above or below the amplifier. | Summing junction and feedback loop. Keep multiple input branches distinct. |
| Differential amplifier | Arrange paired input and feedback/reference resistors so corresponding branches can be compared. | Both input paths and the feedback/reference network; do not distort topology to force symmetry. |
| Low-side transistor switch | Load above the switching device; source/emitter toward return below; gate/base drive approaches from the left. | Drive resistor and pull-down/bias branch, switched load connection, and flyback path when present. Verify actual device polarity. |
| High-side switch | Supply above or to the left, switching device between supply and load; load proceeds toward its return. | Gate/base bias and drive relative to the actual source/emitter. Do not reuse a low-side arrangement blindly. |
| Linear regulator | Input left, output right, return below; input/output capacitors near their corresponding nodes. Feedback divider beside the feedback pin. | Nearby capacitor branches and adjustable-regulator feedback divider. |
| Switching converter | Follow the manufacturer's reference topology. Group switch, diode/synchronous device, inductor, and output capacitor so energy transfer is apparent; keep feedback separate from switch-node clutter. | Power-stage connections and feedback sensing path. Schematic proximity does not substitute for PCB current-loop layout. |
| Decoupling | Capacitor near its IC supply pin or a clearly identified power unit for a multi-unit symbol. | Local supply-to-capacitor relationship when practical. Repeated rail symbols are acceptable; identify which IC a separate bank serves. |
| Connector protection / termination | Connector at block boundary, protection near the entry, then series/filter components, then receiver or driver. | Protected path and return branches. Orient bidirectional interfaces for clarity rather than inventing signal direction. |
| Repeated channels | Same flow direction, component order, spacing, and label positions across channels. | Each channel's local path. Use hierarchy when repetition overwhelms a sheet. |

For unfamiliar motifs, consult a suitable manufacturer reference schematic and adapt its functional arrangement to the actual circuit. Do not copy unrelated circuitry or substitute a similar-looking electrical topology.

Sources for drawing conventions:
- [TU Delft: Guidelines for Drawing Schematics](https://eee.ewi.tudelft.nl/q1-courselabs/schematics/)
- [Altium: Creating Elegant and Readable Schematics](https://resources.altium.com/p/creating-elegant-and-readable-schematics)
- [KiCad Library Conventions](https://klc.kicad.org/)
