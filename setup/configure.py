"""Install the skill and update only the selected MCP tables, keeping a backup."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import tomllib


def configure(root, codex_dir, node, python, python_path):
    config = codex_dir / 'config.toml'
    old = config.read_text(encoding='utf-8-sig') if config.exists() else ''
    tomllib.loads(old)  # Reject malformed input before touching anything.
    # Preserve every other table verbatim. Recognize quoted and unquoted kicad keys.
    sections = re.split(r'(?m)(?=^\s*\[)', old)
    retained = []
    for section in sections:
        header = section.strip().splitlines()[0] if section.strip() else ''
        normalized = header.replace('"', '').replace("'", '').replace(' ', '')
        if normalized.startswith('[mcp_servers.kicad]') or normalized.startswith('[mcp_servers.kicad.'):
            continue
        retained.append(section)
    q = lambda value: json.dumps(str(value))
    new = ''.join(retained).rstrip() + '\n\n[mcp_servers.kicad]\n'
    new += f'command = {q(node)}\nargs = [{q(root / "mcp/dist/index.js")}]\n'
    new += f'cwd = {q(root / "mcp")}\nstartup_timeout_sec = 180\ntool_timeout_sec = 600\n'
    new += '[mcp_servers.kicad.env]\n'
    for key, value in {'KICAD_PYTHON': python, 'PYTHONPATH': python_path,
                       'NODE_ENV': 'production', 'LOG_LEVEL': 'info', 'PYTHONNOUSERSITE': '1',
                       'KICAD_AUTO_LAUNCH': 'false', 'KICAD_INTERACTIVE_SCHEMATIC': 'false',
                       'KICAD_MCP_DEV': '0'}.items():
        new += f'{key} = {q(value)}\n'
    parsed = tomllib.loads(new)
    before = tomllib.loads(old)
    for data in (before, parsed):
        data.get('mcp_servers', {}).pop('kicad', None)
        if data.get('mcp_servers') == {}:
            data.pop('mcp_servers')
    if before != parsed:
        raise RuntimeError('Refusing to change unrelated configuration')
    codex_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    target = codex_dir / 'skills/kicad-readable-schematics'
    if target.exists():
        backup = codex_dir / 'backups' / stamp / target.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(backup))
    shutil.copytree(root / 'skills/kicad-readable-schematics', target)
    if config.exists():
        shutil.copy2(config, config.with_name(f'config.toml.backup-{stamp}'))
    tmp = config.with_suffix('.toml.tmp')
    tmp.write_text(new, encoding='utf-8')
    os.replace(tmp, config)
    print(f'Configured MCP and installed skill in {codex_dir}')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for arg in ['root', 'codex-dir', 'node', 'python', 'python-path']:
        p.add_argument('--' + arg, required=True)
    a = p.parse_args()
    configure(Path(a.root).resolve(), Path(a.codex_dir).resolve(), a.node, a.python, a.python_path)
