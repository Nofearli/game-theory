# Install the game-theory skill into a skills directory (Windows PowerShell).
#
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 -Destination C:\path\to\skills
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 -Force
param(
    [string]$Destination = "$env:USERPROFILE\.workbuddy-ai\skills",
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

$src  = $PSScriptRoot
$dest = Join-Path $Destination 'game-theory'

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

if (Test-Path $dest) {
    if (-not $Force) {
        $ans = Read-Host "Destination exists: $dest`nOverwrite? [y/N]"
        if ($ans -notmatch '^[yY]') { Write-Host 'Aborted.'; exit 1 }
    }
    Remove-Item -Recurse -Force $dest
}

New-Item -ItemType Directory -Force -Path $dest | Out-Null

$exclude = @('.git', '__pycache__', 'out')
Get-ChildItem -Path $src -Force | Where-Object { $exclude -notcontains $_.Name } | ForEach-Object {
    Copy-Item -Recurse -Force -LiteralPath $_.FullName -Destination $dest
}

# drop any nested caches / example outputs
Get-ChildItem -Path $dest -Recurse -Force -Directory -ErrorAction SilentlyContinue |
    Where-Object { $exclude -contains $_.Name } |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Installed to: $dest"
Write-Host "Verify with:  python `"$dest\tests\run_tests.py`""
