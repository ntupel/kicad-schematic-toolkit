# Describe the circuit, then choose its drawing

Use this intermediate description to separate electrical intent from drawing coordinates. For a circuit of roughly 10-17 components, a compact component table, net table, and list of functional relationships are usually sufficient. This is not a component-count limit. Plain tables or structured YAML/JSON are both suitable; no special solver or library is required.

## 1. Component inventory and electrical intent

Record:

- Circuit function, input/output interfaces, supply/reference domains, and any provided operating assumptions.
- For each component: unique reference, actual KiCad symbol/unit, value or part number, functional block, and electrical role. Examples: gain-setting resistor, frequency-setting capacitor, bias resistor, supply bypass capacitor, input protection device.
- Relevant pin numbers and their meanings, verified against the selected symbol and device documentation as needed. Do not infer pin numbers from symbol appearance.
- For multi-unit parts, identify units sharing one physical component and include power units. Distinguish intentionally unused pins from missing connections.

Mark roles as supplied, inferred from connectivity, or unresolved when that distinction matters. An inferred role guides presentation but does not authorize a change to electrical connections or values. Unknown electrical details that affect the circuit require clarification; harmless drawing choices do not.

## 2. Authoritative connection table

Represent every net as a set of component-pin pairs, including power, references, connector pins, and intentional unused-pin states. Give nets internal identifiers even when no visible label will be drawn.

Connectivity is an undirected relation: every pin in a net shares an electrical node. A signal-flow arrow or a component-role description is not a substitute for this table. Conversely, a named net in the table does not require a disconnected label pair on the drawing.

Check that every relevant pin is accounted for, no pin belongs to two distinct nets, references and units resolve, and supply domains remain distinct. For existing schematics, preserve the baseline unless the user authorized an electrical change.

## 3. Functional relationships

On top of the net table, describe the paths that a reader should understand. For each relationship, record its kind, participating components, origin/destination pins or nets, and drawing priority. Useful kinds include main signal path, negative feedback, frequency-dependent feedback, bias, sensing, decoupling, and protection.

For paths through components, list both the intervening component and its separate terminal nets. Do not merge nodes merely because they belong to one functional path. Feedback makes cycles expected; do not try to turn the circuit into an acyclic flowchart. Direction is interpretive and may be bidirectional or frequency dependent.

Example relationships for the tested filter:

| Relationship | Members / electrical meaning | Drawing consequence |
|---|---|---|
| Main signal path | Input -> R1 -> R2 -> U1 non-inverting input; U1 output -> output interface | Place left to right with direct wires between adjacent terminals. |
| Frequency-dependent feedback | Output -> C1 -> junction between R1 and R2 | Reserve a continuous upper path; do not confuse C1 with a bypass capacitor. |
| Negative feedback | Output -> R4 -> U1 inverting-input node | Reserve a separate lower loop. |
| Gain reference | Inverting-input node -> R3 -> GND | Draw R3 vertically below the feedback node. |
| Filter shunt branch | Non-inverting-input node -> C2 -> GND | Show the capacitor branch visibly, clear of the negative-feedback wire. |
| Supply bypass | C3 between positive rail and GND; C4 between negative rail and GND | Group and identify these with U1; shared power symbols are acceptable. |

Arrows in this table express functional paths, not additional wires or changes in pin connectivity.

## 4. Bind roles to conventional patterns

Choose motifs by topology and function together, not by matching a list of part types. For each chosen pattern, record:

| Field | What to record |
|---|---|
| Pattern | E.g. non-inverting amplifier, resistor divider, Sallen-Key low-pass |
| Role bindings | Actual component references and pins filling each pattern role |
| Interfaces | Input, output, supply, reference, and shared nets |
| Relative arrangement | Signal direction, branch positions, and feedback corridors |
| Visible paths | Connections that should be followed continuously without label jumps |
| Text space | Clear regions for Reference/Value fields and power names |
| Exceptions | Any disconnected local connection and why it improves readability |

A component may participate in several functional relationships but is drawn once, apart from legitimate multi-unit symbols. Preserve shared interfaces while composing patterns. In a complex device, several visual groups may reference the same supply without requiring a large common supply wire.

For unfamiliar topology, consult an appropriate manufacturer schematic. If no known motif fits, arrange by the identified paths and functional groups; do not alter the circuit to resemble a familiar example.

## 5. Generate and choose an arrangement

Use the agent's circuit interpretation to select patterns and ordinary KiCad tools to realize them. A constraint solver can help when available, but is optional and must not be claimed as used unless actually run.

Reject candidates that change connectivity, obscure required pin information, or introduce overlaps or ambiguous junctions. Among valid candidates prefer, in order:

1. Recognizable motifs with continuous main signal and feedback paths.
2. Fewer unnecessary label jumps and wire crossings.
3. Clear grouping, short comprehensible wire paths, and few bends.
4. Consistent fields, alignment, and reasonable use of space.

For an obvious conventional circuit, one planned arrangement followed by rendered review is enough. If competing motifs or dense pinouts create a real tradeoff, compare a few alternatives, such as feedback above versus below. Do not optimize shortest wire length at the expense of understanding, impose a zero-label target, or call a heuristic result globally optimal.

## 6. Close the loop

Export the schematic's connectivity and compare connected-pin sets against the authoritative table. Inspect the actual rendering and trace every high-priority functional relationship. Confirm that the visible drawing communicates the selected pattern and that fields follow the field-placement reference.

Revise graphic arrangement without changing electrical intent. If an electrical change is authorized, update the description and validate against the revised intent rather than silently changing the expected result to match a faulty drawing. Keep a compact description or review record alongside substantial generated schematics so later edits retain the circuit's rationale.
