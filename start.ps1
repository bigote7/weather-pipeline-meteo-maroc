# Démarrage rapide — Pipeline météo Maroc
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
Set-Location $root

Write-Host "=== Pipeline météo Maroc — 4IASDG2 ===" -ForegroundColor Cyan

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Fichier .env cree. Ajoutez OPENWEATHER_API_KEY puis relancez." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path "venv")) {
    python -m venv venv
}
& ".\venv\Scripts\Activate.ps1"
pip install -q -r requirements.txt

Write-Host "Demarrage MinIO..." -ForegroundColor Green
docker start minio 2>$null

Write-Host "Execution du pipeline..." -ForegroundColor Green
python scripts/run_pipeline.py

Write-Host ""
Write-Host "Liens utiles:" -ForegroundColor Cyan
Write-Host "  MinIO    : http://localhost:9001"
Write-Host "  Airflow  : http://localhost:8080  (docker compose -f infra/docker-compose.yml up -d)"
Write-Host "  Power BI : powerbi\weather_analytics.json"
