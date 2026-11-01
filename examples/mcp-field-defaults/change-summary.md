# KiCad MCP default field placement improvement

Installed in `the original MCP installation`.

## Changes

- Correct library-to-sheet field coordinates: flip Y, rotate, then apply the symbol's sheet-space mirror.
- Place standard Device R/R_US/C/C_Polarized/C_Polarized_US Reference and Value fields outside their graphics, horizontally readable, with reference above value.
- Place operational-amplifier fields outside the selected unit's graphic/pin-coordinate envelope.
- Place standard power names outside their glyphs with clearance. Preserve library visibility, including hidden power references. PWR_FLAG retains its library-based field placement with corrected coordinates.
- Preserve custom-library field offsets after the coordinate transform, font settings, and later explicit field edits.
- Use the existing symbol-insertion path; no new MCP arguments or TypeScript rebuild are needed.

Changed source files: `python/commands/dynamic_symbol_loader.py`, new `python/commands/schematic_field_defaults.py`, and new `tests/test_readable_field_defaults.py`. Also ran `corepack pnpm install --lockfile-only` successfully in the installation directory.

## Verification

- 113 focused field-placement, visibility, component-insertion, and explicit-field-editing tests passed.
- 82 related format-compatibility, symbol-completeness, footprint-inheritance, hierarchy, and pin tests passed.
- Recreated every placed symbol in the prior 17-component schematic through the updated loader, retaining circuit wires but discarding the manual instance-field corrections. The accompanying preview shows the generated defaults.
- KiCad loaded/rendered the result. ERC reports zero errors or warnings.
- All exported connected-pin groups match the original circuit.
- Visually inspected the resulting drawing: standard component fields and power names are outside symbol bodies and clear of the tested wiring.
- Installed Python source and tests were checked against the tested staged files by hash.

The test runs used an explicit writable temporary directory and disabled the repository's coverage options because pytest-cov was unavailable. A pre-existing kicad-skip SyntaxWarning was emitted. The optional Black formatter was not available in the test interpreter. The lockfile update reported an existing-version peer mismatch: Vitest 5 requests Node types 22 or 24+, while package.json specifies Node types 20. No dependency versions were changed to address it.

## Activation and limits

Restart/reconnect the KiCad MCP server to load the changed Python modules; an already running worker may retain its previously imported code. Existing schematic files are not rewritten automatically.

These are better initial defaults, not a whole-sheet collision-avoidance solver. They do not anticipate future wires or account for every neighboring component or long custom text. Dense drawings still need the skill's rendered visual review and, where necessary, explicit field-position adjustments. The patch file contains the three Python/test changes; the generated pnpm lockfile remains in the installation directory.

