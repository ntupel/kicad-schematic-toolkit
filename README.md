# Readable KiCad schematic toolkit

Portable skill, modified KiCad MCP, and reviewed schematic examples. This repository is self-contained: the source snapshot includes the component-text and power-label insertion fixes, not just a patch against upstream.

## Windows installation

Install **KiCad 10 with Python support and standard symbol/footprint libraries**, **Node.js 22 LTS or newer**, and Corepack. Git is needed only if cloning rather than downloading the repository. Internet access is needed to install dependencies. The installer targets local Codex MCP configuration; it does not configure ChatGPT browser access.

Clone/download this private repository into a permanent folder. From its root, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup\install.ps1 -CheckOnly
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup\install.ps1
```

For a custom KiCad installation, add `-KiCadPython 'D:\KiCad\10.0\bin\python.exe'`. Use `-CodexDir <folder>` to target a different Codex configuration directory. Otherwise CODEX_HOME is respected, falling back to the current user's `.codex` folder. No administrator rights are needed by this installer.

The installer builds the MCP, installs Python dependencies into `.runtime/python-deps`, verifies the included amplifier's connectivity and unchanged text fields, copies the skill, and registers `mcp_servers.kicad`. It backs up existing configuration and any previous copy of this skill. Other configuration is preserved; an existing MCP named `kicad` is replaced. Keep the repository in place because the MCP runs from it. Restart Codex after installation.

Node dependencies use the committed pnpm lockfile. Python dependencies use `setup/requirements-windows.lock.txt`, pinned from the tested Windows Python 3.11 installation; KiCad supplies its own Python and PCB API. Run the checks after dependency or KiCad upgrades. Other operating systems have not been tested by this installer.

## Try it

Ask the agent:

> Use $kicad-readable-schematics to create an AC-coupled op amp amplifier. Describe components, pin connections, and electrical roles first. Use direct feedback wiring and MCP text defaults without preemptive text movement. Export and visually inspect the actual KiCad rendering, check connectivity and ERC, then show the schematic.

Open `examples/restarted-mcp-test/ac-coupled-amplifier.kicad_sch` in KiCad and compare it with `preview.png`. This eleven-component example used the patched insertion defaults without manual field movement. Its review records the original visual and electrical checks. Older examples show the skill's development and may include manual text adjustments.

The installer verifies saved example data; a fresh generated schematic and its visual review are still required to verify end-to-end agent behavior on the new machine. ERC does not replace simulation or hardware validation.

## Contents

- `skills/kicad-readable-schematics`: electrical roles and connections first, conventional motifs, direct wiring, and required visual review.
- `mcp`: installed source snapshot, including all existing tracked local changes and the new text-placement helper/tests.
- `setup`: Windows installer, conservative configuration writer, and example verifier.
- `examples`: basic amplifier, active filter, seventeen-component filter/gain circuit, and default-field tests.

Custom library assets should live with their projects and use project-relative library paths. The included schematics embed symbol definitions. Empty footprint assignments are acceptable for schematic demonstrations; verify package and pad mapping before PCB work.

## Updating and recovery

Pull a reviewed revision and rerun the installer. Configuration backups are stored alongside `config.toml`; skill backups are under the configuration directory's `backups/`. To uninstall, remove the `mcp_servers.kicad` tables and installed skill, or restore their backups, before removing this repository folder.

For source dependency changes, run `corepack pnpm install --lockfile-only` inside `mcp` and commit the updated lockfile. Do not commit credentials, local config, dependencies, or runtime logs.

## Provenance and license

MCP upstream: https://github.com/mixelpixx/KiCAD-MCP-Server, source base `cbb59a6203997f5e916be7e0480d63fe5519134a`. The snapshot also preserves installed local modifications to package metadata, schematic tool wrappers, and a TypeScript schema test. `mcp/LICENSE` preserves the upstream MIT notice. No upstream Git history, personal Codex configuration, or KiCad binaries are bundled.

New additions in this toolkit are distributed under the MIT license in `LICENSE`. See `VALIDATION.md` for checks and limits of this release.
