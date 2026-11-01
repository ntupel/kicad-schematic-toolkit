[CmdletBinding()]
param(
    [string]$KiCadPython,
    [string]$CodexDir = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }),
    [switch]$CheckOnly
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$mcpRoot = Join-Path $repoRoot 'mcp'
$node = (Get-Command node -ErrorAction Stop).Source
$corepack = (Get-Command corepack -ErrorAction Stop).Source
if (-not $KiCadPython) {
    $candidates = @(Get-ChildItem "$env:ProgramFiles\KiCad\*\bin\python.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending)
    if (-not $candidates) { throw 'Install KiCad 10 with Python support, or pass -KiCadPython <path>.' }
    $KiCadPython = $candidates[0].FullName
}
$KiCadPython = (Resolve-Path -LiteralPath $KiCadPython).Path
$binDir = Split-Path $KiCadPython -Parent
$cli = Join-Path $binDir 'kicad-cli.exe'
if (-not (Test-Path -LiteralPath $cli)) { throw 'kicad-cli.exe must be next to the KiCad Python executable.' }
& $KiCadPython -c 'import pcbnew, tomllib'
if ($LASTEXITCODE) { throw 'KiCad Python must support pcbnew and tomllib (Python 3.11+).' }
& $node --version
& $cli version
if ($LASTEXITCODE) { throw 'KiCad CLI could not start.' }
if ($CheckOnly) { Write-Host 'Prerequisite check passed. No configuration was changed.'; return }
$deps = Join-Path $repoRoot '.runtime\python-deps'
New-Item -ItemType Directory -Force $deps | Out-Null
& $KiCadPython -m pip install --disable-pip-version-check --upgrade --target $deps -r (Join-Path $PSScriptRoot 'requirements-windows.lock.txt')
if ($LASTEXITCODE) { throw 'Python dependency installation failed.' }
Push-Location $mcpRoot
try {
    & $corepack pnpm install --frozen-lockfile
    if ($LASTEXITCODE) { throw 'Node dependency installation failed.' }
    & $corepack pnpm run build
    if ($LASTEXITCODE) { throw 'MCP TypeScript build failed.' }
} finally { Pop-Location }
$pythonPath = $deps + [IO.Path]::PathSeparator + (Join-Path $binDir 'Lib\site-packages')
$oldPythonPath = $env:PYTHONPATH
$oldNoUserSite = $env:PYTHONNOUSERSITE
try {
    $env:PYTHONPATH = $pythonPath
    $env:PYTHONNOUSERSITE = '1'
    & $KiCadPython -c 'import pcbnew, skip, sexpdata, pymupdf'
    if ($LASTEXITCODE) { throw 'MCP runtime imports failed.' }
    & $KiCadPython (Join-Path $PSScriptRoot 'verify-example.py')
    if ($LASTEXITCODE) { throw 'Example connectivity/field verification failed.' }
    & $KiCadPython (Join-Path $PSScriptRoot 'configure.py') --root $repoRoot --codex-dir $CodexDir --node $node --python $KiCadPython --python-path $pythonPath
    if ($LASTEXITCODE) { throw 'Configuration failed.' }
} finally { $env:PYTHONPATH = $oldPythonPath; $env:PYTHONNOUSERSITE = $oldNoUserSite }
Write-Host 'Installation complete. Keep this folder in place and restart Codex.'
