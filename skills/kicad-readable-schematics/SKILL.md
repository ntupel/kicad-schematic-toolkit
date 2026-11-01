---
name: kicad-readable-schematics
description: Generate or improve readable KiCad schematics by describing components, pin connections, electrical roles, and functional relationships before choosing conventional drawing patterns. Use for schematic capture, drawing cleanup, and visual review; not PCB placement or routing.
---

# Readable KiCad schematics

Make the circuit's operation understandable by following visible wires and recognizing familiar circuit patterns. Electrical correctness and graphical clarity are separate acceptance criteria.

This workflow generates the schematic drawing: symbols, wires, junctions, fields, and labels. Arrangement and routing here refer to schematic graphics, not PCB footprints or copper.

## Establish intent and connectivity

- Inspect the existing project, symbols, sheet hierarchy, and user-provided references before editing. Preserve electrical behavior during layout-only work.
- Before generating a new drawing or substantially rearranging one, build a concise circuit description following [Circuit description and pattern selection](references/circuit-description.md). Describe components, exact pin connections, electrical roles, and functional relationships before assigning drawing coordinates. For a small local edit, describe only the affected motif and its interfaces.
- For an existing circuit, capture a baseline netlist and derive the description from it. For a new circuit, establish intended connectivity independently of the drawing. Resolve electrical ambiguities before committing dependent connections; do not invent topology merely to complete a pattern.
- Use available KiCad tools or supported file-generation methods. Inspect tool capabilities and installed-version help before assuming commands or schemas. Do not fabricate tool names, symbol identifiers, or pin positions.
- Resolve missing library assets using [Symbols and footprints](references/library-assets.md). Never silently substitute a different device or package to make generation succeed.
- Prefer the user's drawing conventions and good reference sheets when provided. Do not change component values, pin assignments, or topology merely to fit a visual pattern.

## Compose the drawing

Map the circuit description to applicable motifs in [Circuit patterns](references/circuit-patterns.md) before placing or rearranging components. Record which references and nets fill each motif's roles, its visible signal/feedback paths, and its interfaces to other motifs. The description's connectivity remains authoritative.

- Compose related motifs into one drawing without duplicating shared components or losing shared nets. For example, a Sallen-Key stage combines an RC network, capacitive feedback, a non-inverting gain stage, and supply bypassing.
- Choose relative positions first, then exact symbol coordinates and wire paths, reserving space for the MCP's default fields. When motifs compete for space, compare a few plausible arrangements using the priorities in the circuit-description reference. Prefer a clear conventional arrangement; do not claim a globally optimal drawing.

- Arrange the main signal flow primarily left to right. Place positive supply connections above and ground or negative supply below where practical. Keep related parts together, with space separating functional blocks.
- Establish each motif's relative placement and orientation before assigning detailed coordinates. Reserve routing corridors for feedback, branches, and inter-block signals.
- Use a consistent connection grid compatible with the symbols; standard KiCad symbols normally use a 50 mil connection grid. Inspect actual pin anchors and transformed orientations. Visual proximity does not prove connection.
- Prefer symbols whose functional pin arrangement supports understanding. Do not remap electrical pin numbers for appearance. Avoid mirroring or rotating symbols in ways that obscure polarity or familiar behavior.
- Use the updated KiCad MCP insertion defaults for component fields and power labels. Reserve space around those fields when arranging symbols and wires, but do not preemptively move, rotate, hide, or auto-place text. Follow [Field placement](references/field-placement.md): adjust fields only when the actual rendered visual review identifies a specific problem, or the user explicitly requests a text change.
- Place text outside wire corridors; keep references, values, pin labels, and polarity marks legible at normal reading scale. Keep repeated channels consistent. After routing, check the reserved text areas again before exporting.

## Wire to reveal operation

- Draw direct wires within a functional block. In particular, make the main signal path, divider taps, bias networks, and local feedback loops visibly continuous.
- Do not replace a short, clear connection with two matching labels merely because labels are easier to generate. If routing is awkward, improve placement before introducing disconnected labels.
- Use labels and hierarchical connections for sheet boundaries, distant connections, shared rails, or connections where explicit wiring would cause materially worse clutter. Shared ground and supply symbols are appropriate; do not create a page-spanning ground wire merely to reduce labels.
- Distinguish a name attached to a continuous wire from a label used to connect disconnected wire islands. The former can help identify a signal without interrupting visual tracing. Minimize unnecessary visual jumps, not all labels.
- Keep label scope intentional: local, hierarchical, and global labels are not interchangeable. Preserve distinct grounds and supply domains; do not join them through a shared power-symbol name.
- Prefer orthogonal wires with few bends and crossings. Use clear T junctions for branches; avoid four-way crossings when a pair of offset T junctions is clearer. Show intended junctions and verify that crossings without a junction remain disconnected.
- Never route through symbol bodies, text, unrelated pins, or unrelated wire endpoints. Move components when necessary rather than accepting a maze of detours.
- For dense digital interfaces, prefer orderly buses, explicit bus entries, and meaningful ports when supported by the project. Do not force analog-style continuous wiring across an entire dense digital sheet.

## Required review and repair

Read [Review procedure](references/review.md). Export or capture the actual KiCad-rendered result and inspect it at page scale and at detail scale. Reviewing only source coordinates or a netlist is insufficient.

Compare exported pin groups to the circuit description, and trace each designated signal and feedback relationship in the rendering. Repair readability defects, render again, and recheck electrical connectivity after drawing edits. Do not declare visual review complete if no rendered view was inspected. If rendering is unavailable, report that limitation and the remaining review explicitly.

## Deliver

Provide the editable KiCad schematic and any project-local symbols or supporting files needed to open it. Include a rendered preview when feasible. Briefly report connectivity comparison, electrical-rule-check results, visual review, and any justified disconnected local connections or remaining defects. Do not claim ERC proves circuit operation; simulation or electrical design validation is separate and depends on the task.
