import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import sexpdata

folder = Path(__file__).resolve().parent.parent / 'examples/restarted-mcp-test'
root = sexpdata.loads((folder / 'ac-coupled-amplifier.kicad_sch').read_text(encoding='utf-8'))
fields = {}
for symbol in root:
    if not isinstance(symbol, list) or str(symbol[0]) != 'symbol':
        continue
    props = [n for n in symbol if isinstance(n, list) and str(n[0]) == 'property']
    ref = next(str(n[2]) for n in props if str(n[1]) == 'Reference')
    fields[ref] = [sexpdata.dumps(n) for n in props]
snapshot = folder / 'initial-fields.json'
if '--snapshot' in sys.argv:
    snapshot.write_text(json.dumps(fields, indent=2), encoding='utf-8')
    print(f'Snapshotted original fields for {len(fields)} placed symbols.')
else:
    assert fields == json.loads(snapshot.read_text()), 'Fields changed after initial placement'
    expected = json.loads((folder / 'intended-nets.json').read_text())
    netlist = ET.parse(folder / 'ac-coupled-amplifier.net')
    actual = {n.attrib['name']: frozenset(p.attrib['ref'] + '/' + p.attrib['pin'] for p in n.findall('node')
                                        if not p.attrib['ref'].startswith('#'))
              for n in netlist.findall('./nets/net')}
    assert {p for p in actual.values() if p} == {frozenset(p) for p in expected.values()}
    for rail in ['+12V', '-12V', 'GND']:
        assert actual[rail] == frozenset(expected[rail])
    assert len(netlist.findall('./components/comp')) == 11
    print('PASS: all 11 components and 11 pin groups match; every initial field is unchanged.')
