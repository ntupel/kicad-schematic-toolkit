# Schematic review procedure

## Electrical verification

1. Load the generated or edited schematic with KiCad tooling. Check symbol resolution and parse/load errors.
2. Export connectivity and compare with the baseline or intended pin-to-net table. Compare sets of connected component pins, not just generated net names, wire segment counts, or coordinates. Include hierarchy and multi-unit components. Check named-net identity where names carry interface or domain meaning.
3. Run KiCad ERC when available. Investigate new errors and warnings; distinguish pre-existing or deliberately accepted findings from regressions. Never add power flags, no-connect markers, or suppressions solely to make the report green. Confirm their electrical meaning first.
4. After repairs, repeat affected checks. A visually touching wire must terminate at an actual electrical anchor, and a wire crossing must not accidentally merge separate nets.

## Required rendered review

Use KiCad's own schematic rendering/export or the actual editor view. Convert exported pages to viewable images if needed using available tools. Inspect every changed sheet at whole-page scale, then inspect dense regions at a readable zoom. Do not substitute a conceptual diagram for the delivered schematic.

At page scale:
- Is the input-to-output or power-transfer path obvious?
- Are functional blocks separated by whitespace and grouped internally?
- Are familiar circuit motifs recognizable without decoding every net name?
- Are repeated channels consistent, and is the sheet neither crowded nor scattered?

At detail scale:
- Trace the main path and each local feedback loop with the eye. Every disconnected jump should have a reason; replace unnecessary local label pairs with wires.
- Inspect all dense junctions, crossings, symbol pins, polarity markings, references, and values. Look for overlapping text, ambiguous dots, wires through symbols, and tiny unintended gaps.
- Check label attachment and scope, dangling wire ends, unused pins, and supply-domain boundaries against actual connectivity rather than appearance alone.
- Confirm that important branches remain visible and that power/ground symbols have not hidden a domain error.

Use a short defect list with sheet, location, consequence, and repair. Fix the highest-impact issues first: wrong connectivity; obscured/ambiguous connections; broken main or feedback paths; misleading grouping; unnecessary crossings; spacing and alignment.

Render again after visual repairs and recheck connectivity. Stop when there are no unexplained connectivity changes, no unresolved new ERC errors without documented justification, no visible overlaps or ambiguous connections in reviewed regions, and local signal/feedback paths are traceable except for justified labels. Do not chase an arbitrary numeric score or a zero-label target. If a tool limitation prevents a required check, identify the unchecked result instead of claiming success.

## Practical acceptance examples

- An amplifier whose output and feedback resistor are joined only by matching local labels fails readability review when a clean feedback wire fits.
- A label naming a continuous output wire is acceptable and may help PCB work.
- Repeated ground symbols are acceptable; a web of ground wires across unrelated blocks is not an improvement.
- A sheet-to-sheet interface using meaningful hierarchical ports is acceptable.
- An attractive drawing with a wire one grid step short of a pin fails connectivity verification.
- A netlist-equivalent drawing with a wire crossing a component value fails visual review.
- Resistor values inside their bodies, op-amp fields over supply or offset-null pins, and rail names on their wires fail visual review even when ERC passes. Start with MCP defaults, then use [Field placement](field-placement.md) to repair only the defects actually observed in the rendering.
- After moving a power label, check nearby multiline notes again; a clear label can still collide with the top line of a bottom-anchored note.

For tool syntax, use installed-version CLI help or the corresponding [KiCad documentation](https://docs.kicad.org/). Do not assume that commands or output formats are identical across versions.
