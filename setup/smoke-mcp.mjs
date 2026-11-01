// Run after installation: node setup/smoke-mcp.mjs "C:\Program Files\KiCad\10.0\bin\python.exe"
import { Client } from '../mcp/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js';
import { StdioClientTransport } from '../mcp/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js';
import { dirname, resolve, delimiter } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const python = process.argv[2];
if (!python) throw new Error('Pass the KiCad Python executable path.');
const client = new Client({name: 'toolkit-smoke-test', version: '1.0.0'});
const transport = new StdioClientTransport({
  command: process.execPath,
  args: [resolve(root, 'mcp/dist/index.js')],
  cwd: resolve(root, 'mcp'),
  env: {...process.env, KICAD_PYTHON: python,
    PYTHONPATH: [resolve(root, '.runtime/python-deps'), resolve(dirname(python), 'Lib/site-packages')].join(delimiter),
    PYTHONNOUSERSITE: '1', KICAD_AUTO_LAUNCH: 'false', KICAD_INTERACTIVE_SCHEMATIC: 'false', KICAD_MCP_DEV: '0'},
  stderr: 'pipe'
});
let diagnostics = '';
transport.stderr?.on('data', chunk => { diagnostics = (diagnostics + chunk.toString()).slice(-12000); });
try {
  await client.connect(transport, {timeout: 180000});
  const list = await client.listTools();
  if (!list.tools.some(t => t.name === 'add_schematic_component')) throw new Error('Schematic tools unavailable');
  let result;
  const deadline = Date.now() + 180000;
  do {
    result = await client.callTool({name: 'get_symbol_info', arguments: {symbol: 'Device:R'}}, undefined, {timeout: 180000});
    if (!result.isError || !JSON.stringify(result).includes('not running')) break;
    await new Promise(resolve => setTimeout(resolve, 1000));
  } while (Date.now() < deadline);
  if (result.isError || !JSON.stringify(result).includes('Device:R')) throw new Error('Symbol lookup failed: ' + JSON.stringify(result));
  console.log(`PASS: MCP initialization, ${list.tools.length} tool definitions, and Device:R lookup`);
} catch (error) {
  console.error(diagnostics);
  throw error;
} finally {
  await client.close();
}
