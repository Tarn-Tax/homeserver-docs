# Homeserver Docs - ontwikkelomgeving starten

Set-Location "C:\Users\TARN\homeserver-docs"

Set-ExecutionPolicy `
    -Scope Process `
    -ExecutionPolicy Bypass `
    -Force

& ".\.venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Homeserver Docs ontwikkelomgeving is gereed."
Write-Host "Projectmap: $(Get-Location)"
Write-Host ""