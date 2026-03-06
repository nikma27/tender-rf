# Tender RF Backend - Setup and Run
# Run this in PowerShell after installing Python (add to PATH!)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== Tender RF Backend ===" -ForegroundColor Cyan

# Create venv if not exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & "C:\Users\Mila\AppData\Local\Programs\Python\Launcher\py.exe" -3 -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Python not found. Install from python.org and add to PATH." -ForegroundColor Red
        exit 1
    }
}

# Activate and install
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q

# Run server
Write-Host "Starting API server at http://localhost:8000" -ForegroundColor Green
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
