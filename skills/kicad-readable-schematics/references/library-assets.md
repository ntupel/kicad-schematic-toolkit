# Missing symbols and footprints

Distinguish a missing library, a missing named symbol, an unassigned footprint, and an assigned footprint that cannot be resolved. They require different remedies.

## Symbols

The MCP symbol loader searches configured libraries, including project-local library tables, and embeds a resolved symbol definition in the schematic. If the library or requested symbol cannot be found, insertion fails; the loader does not automatically invent or download an equivalent symbol. Inspect the tool's response text as well as structured status before continuing dependent wiring.

Search installed libraries and verify library registration/path resolution first. If a suitable symbol exists under another identifier, verify pin numbers, pin functions, unit structure, and device compatibility before using it. A generic symbol may represent the requested device only when its mapping is verified; do not silently substitute another electrical device.

If still missing, use an authoritative manufacturer source or create a project-local symbol from verified device documentation when this is within the requested scope and supported by available tools. Keep source/provenance and include the custom library and library-table entry with the project when needed. Verify symbol loading, pin mapping, polarity, power pins, and units before wiring. If the exact device or mapping is unresolved, ask for that information and continue only independent work; never guess pins to complete the drawing.

## Footprints

The current schematic insertion code stores an explicitly provided footprint identifier; otherwise it inherits the symbol library's default, or leaves the property empty when none exists. This assignment alone does not validate that the footprint library/file exists or matches the selected part.

For a schematic-only demonstration, an unassigned footprint is acceptable if disclosed. Do not choose an arbitrary package just to fill the property. For a PCB-bound design, resolve and validate footprints before transfer to the board.

Check the exact package variant and drawing, pin-to-pad numbering, pad count, dimensions, pitch, and orientation against manufacturer information. Search registered footprint libraries first. If missing, import or create a verified project-local `.pretty` library and register it through the project's footprint library table. Include necessary local assets in delivery. Do not silently replace a package or treat a symbol's inherited footprint as proof of compatibility. Report unresolved assignments explicitly.
