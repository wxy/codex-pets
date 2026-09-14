param(
    [string]$PetId = "crt-monitor"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if ($env:CODEX_HOME) {
    $CodexHome = $env:CODEX_HOME
} else {
    $CodexHome = Join-Path $HOME ".codex"
}

$Source = Join-Path $Root "pets\$PetId"
$Manifest = Join-Path $Source "pet.json"
$Spritesheet = Join-Path $Source "spritesheet.webp"
if ($PetId -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$' -or
    -not (Test-Path -PathType Leaf $Manifest) -or
    -not (Test-Path -PathType Leaf $Spritesheet)) {
    throw "Unknown pet: $PetId"
}

$Dest = Join-Path $CodexHome "pets\$PetId"
New-Item -ItemType Directory -Force -Path $Dest | Out-Null

Copy-Item $Manifest (Join-Path $Dest "pet.json") -Force
Copy-Item $Spritesheet (Join-Path $Dest "spritesheet.webp") -Force

$DisplayName = (Get-Content $Manifest -Raw | ConvertFrom-Json).displayName
Write-Host "Installed $DisplayName to: $Dest"
Write-Host "Restart Codex and select $DisplayName under Settings -> Appearance -> Pets."
