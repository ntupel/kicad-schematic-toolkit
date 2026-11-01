"""Check repeat installs, configuration preservation, backups and malformed input."""
from pathlib import Path
import tempfile
import tomllib
from configure import configure

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as folder:
    target = Path(folder)
    config = target / 'config.toml'
    initial = '# retain comments\nmodel = "example"\n[mcp_servers.other]\ncommand = "other"\n[mcp_servers.kicad]\ncommand = "old"\n[mcp_servers.kicad.env]\nOLD = "1"\n[features]\nexample = true\n'
    config.write_text(initial)
    for _ in range(2):
        configure(root, target, 'C:/Node/node.exe', 'C:/KiCad/python.exe', 'C:/deps;C:/KiCad/Lib/site-packages')
        parsed = tomllib.loads(config.read_text())
        assert parsed['model'] == 'example'
        assert parsed['features'] == {'example': True}
        assert parsed['mcp_servers']['other'] == {'command': 'other'}
        assert parsed['mcp_servers']['kicad']['command'] == 'C:/Node/node.exe'
        assert 'OLD' not in parsed['mcp_servers']['kicad']['env']
        assert '# retain comments' in config.read_text()
    assert len(list(target.glob('config.toml.backup-*'))) == 2
    assert len(list((target / 'backups').glob('*/kicad-readable-schematics/SKILL.md'))) == 1
    config.write_text('malformed [')
    try:
        configure(root, target, 'node', 'python', '')
    except tomllib.TOMLDecodeError:
        pass
    else:
        raise AssertionError('Malformed config was accepted')
    assert config.read_text() == 'malformed ['
print('PASS: config preservation, repeat install, backups, malformed-input refusal')
