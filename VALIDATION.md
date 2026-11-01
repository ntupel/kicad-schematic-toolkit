# Transfer package validation

Validated on Windows with KiCad 10.0.7, its Python 3.11, Node 24.11.1 and pnpm 10.33.0.

- Full installer completed using an isolated Codex configuration directory; active user configuration was not changed.
- TypeScript compilation passed with the frozen Node dependency lockfile.
- Configuration tests passed: unrelated settings/comments preserved, repeated installs supported, backups created, malformed TOML rejected.
- Skill validator passed.
- 58 text-placement regression tests passed against the copied MCP source. The earlier implementation test run also passed 195 focused and related tests; the entire upstream test suite has not been rerun for this packaging task.
- Saved amplifier verification passed: 11 physical components, all 11 expected pin groups, and initial fields unchanged.
- Fresh packaged MCP process initialized, exposed 244 tools, and successfully looked up Device:R.
- Reviewed schematic previews and their original review notes are included. The original amplifier ERC had zero violations.

The Windows installation was tested on the source computer, not a separate clean computer. KiCad's bundled sitecustomize can expose KiCad-managed user packages even when PYTHONNOUSERSITE is set. The toolkit supplies its own pinned Python dependencies via PYTHONPATH, but a destination-machine smoke test remains important. No macOS/Linux installer or ChatGPT browser/tunnel setup is included.

Run after installation:

```powershell
node .\setup\smoke-mcp.mjs 'C:\Program Files\KiCad\10.0\bin\python.exe'
```

Allow up to three minutes for Python worker startup. Then generate a fresh schematic using the README prompt and perform the skill's required visual review.
