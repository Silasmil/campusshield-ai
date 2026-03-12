# CampusShield Development Server - PowerShell Startup Script
# This script activates the virtual environment and starts the Django development server

param(
    [switch]$SkipBrowser = $false,
    [int]$Port = 8000,
    [string]$BindHost = "127.0.0.1"  # avoid readonly automatic variable 'Host'
)

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     CampusShield AI - Development Server Launcher          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPath = Join-Path $ProjectRoot "venv"

# Check if virtual environment exists
if (!(Test-Path $VenvPath)) {
    Write-Host "❌ Virtual environment not found at: $VenvPath" -ForegroundColor Red
    Write-Host "Please create it first with: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Project root: $ProjectRoot" -ForegroundColor Green
Write-Host "✅ Virtual environment: $VenvPath`n" -ForegroundColor Green

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"

if (!(Test-Path $ActivateScript)) {
    Write-Host "❌ Activation script not found" -ForegroundColor Red
    exit 1
}

& $ActivateScript

# Check Django
Write-Host "🔍 Checking Django installation..." -ForegroundColor Yellow
$DjangoCheck = python -c "import django; print(django.get_version())" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Django $DjangoCheck is installed`n" -ForegroundColor Green
} else {
    Write-Host "❌ Django not available: $DjangoCheck" -ForegroundColor Red
    exit 1
}

# Run Django checks
Write-Host "🔍 Running Django system checks..." -ForegroundColor Yellow
python manage.py check 2>&1 | Select-String "SystemCheckError" | ForEach-Object {
    Write-Host "❌ System check failed: $_" -ForegroundColor Red
}

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     🚀 Starting Django Development Server                  ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "Server URL: http://${BindHost}:${Port}" -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop the server`n" -ForegroundColor Yellow

# Start the server
python manage.py runserver "${BindHost}:${Port}"
