param(
  [string]$Message = "docs: update static site"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

try {
  Write-Host "[deploy] Building docs..."
  python scripts/build_docs.py
  if ($LASTEXITCODE -ne 0) { throw "build_docs.py failed with exit code $LASTEXITCODE" }

  Write-Host "[deploy] Staging changes..."
  git add .

  $status = git status --porcelain
  if (-not $status) {
    Write-Host "[deploy] No changes to commit."
    exit 0
  }

  Write-Host "[deploy] Committing..."
  git commit -m $Message

  Write-Host "[deploy] Pushing..."
  git push

  Write-Host "[deploy] Completed."
}
catch {
  Write-Error "[deploy] ERROR: $($_.Exception.Message)"
  exit 1
}
