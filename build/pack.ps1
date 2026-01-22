# build/pack.ps1
param(
  [string] $OutDir = ".\build\payload",
  [switch] $IncludeOllama = $true,
  [switch] $IncludeZen = $true,
  [string] $ZenDownloadUrl = $env:ZEN_BROWSER_URL,
  [string] $OllamaDownloadUrl = $env:OLLAMA_RELEASE_URL,
  [string] $NodeVersion = "18.20.0"
)

Set-StrictMode -Version Latest

function Ensure-Dir($p) {
  if (-not (Test-Path $p)) { New-Item -ItemType Directory -Force -Path $p | Out-Null }
}

Write-Host "Preparing payload dir: $OutDir"
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $OutDir
Ensure-Dir $OutDir

if ($IncludeOllama) {
  if (-not $OllamaDownloadUrl) {
    Write-Host "Discovering latest Ollama Windows installer via GitHub API..."
    $ollamaApi = "https://api.github.com/repos/ollama/ollama/releases/latest"
    $release = Invoke-RestMethod -Uri $ollamaApi -Headers @{ "User-Agent" = "agentxen-installer" }
    $asset = $release.assets | Where-Object { $_.name -match "windows" -or $_.name -match "win" } | Select-Object -First 1
    if ($asset) { $OllamaDownloadUrl = $asset.browser_download_url }
  }

  if ($OllamaDownloadUrl) {
    $ollamaTarget = Join-Path $OutDir "ollama-installer.exe"
    Write-Host "Downloading Ollama from $OllamaDownloadUrl -> $ollamaTarget"
    Invoke-WebRequest -Uri $OllamaDownloadUrl -OutFile $ollamaTarget -UseBasicParsing
  } else {
    throw "Unable to locate Ollama Windows installer. Set OLLAMA_RELEASE_URL env var to point to the installer."
  }
}

if ($IncludeZen) {
  if (-not $ZenDownloadUrl) {
    Write-Host "Attempting to discover Zen Browser release (github.com/zen-browser)."
    try {
      $zenApi = "https://api.github.com/repos/zen-browser/zen-browser/releases/latest"
      $release = Invoke-RestMethod -Uri $zenApi -Headers @{ "User-Agent" = "agentxen-installer" } -ErrorAction Stop
      $asset = $release.assets | Where-Object { $_.name -match "windows|win|exe|msi" } | Select-Object -First 1
      if ($asset) { $ZenDownloadUrl = $asset.browser_download_url }
    } catch {
      Write-Warning "Could not discover Zen Browser release automatically. You can supply ZEN_BROWSER_URL environment variable or pass -ZenDownloadUrl."
    }
  }

  if ($ZenDownloadUrl) {
    $zenTarget = Join-Path $OutDir "zen-installer.exe"
    Write-Host "Downloading Zen Browser from $ZenDownloadUrl -> $zenTarget"
    Invoke-WebRequest -Uri $ZenDownloadUrl -OutFile $zenTarget -UseBasicParsing
  } else {
    Write-Warning "Zen Browser download URL not provided/found. Installer will prompt the user to provide it during build or install time."
  }
}

Write-Host "Downloading Node $NodeVersion portable..."
$nodeZip = Join-Path $OutDir "node.zip"
$nodeUrl = "https://nodejs.org/dist/v$NodeVersion/node-v$NodeVersion-win-x64.zip"
Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeZip -UseBasicParsing
Expand-Archive -LiteralPath $nodeZip -DestinationPath (Join-Path $OutDir "node") -Force
Remove-Item $nodeZip

Write-Host "Copying agent-server and xen-chat into payload."
Copy-Item -Recurse -Force -Path "agent-server" -Destination (Join-Path $OutDir "agent-server")
Copy-Item -Recurse -Force -Path "xen-chat" -Destination (Join-Path $OutDir "xen-chat")

Ensure-Dir (Join-Path $OutDir "installer")
Copy-Item -Force -Path "installer\install.ps1" -Destination (Join-Path $OutDir "installer\install.ps1")
Copy-Item -Force -Path "installer\installer-config.json" -Destination (Join-Path $OutDir "installer\installer-config.json")

$nsisScript = "build\installer.nsi"
if (-not (Test-Path $nsisScript)) { throw "NSIS script not found: $nsisScript" }
Write-Host "Calling makensis to create installer (requires NSIS on PATH)."
& makensis /V2 $nsisScript

Write-Host "Build finished. Check output in current directory for the produced installer EXE (see installer.nsi OutFile)."