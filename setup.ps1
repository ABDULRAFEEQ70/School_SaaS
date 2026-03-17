#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Setup script for School SaaS local development on Windows
.DESCRIPTION
    Automates the setup process for running School SaaS locally
.EXAMPLE
    .\setup.ps1
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "School SaaS - Local Development Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = & python --version 2>&1
Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping creation" -ForegroundColor Yellow
} else {
    & python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to find activation script" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    & pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Set FLASK_APP environment variable
Write-Host ""
Write-Host "Setting FLASK_APP environment variable..." -ForegroundColor Yellow
$env:FLASK_APP = "app.py"
Write-Host "✓ FLASK_APP set to app.py" -ForegroundColor Green

# Initialize database
Write-Host ""
Write-Host "Initializing database..." -ForegroundColor Yellow
$dbFile = "data.db"

if (-not (Test-Path $dbFile)) {
    Write-Host "Creating database migrations..." -ForegroundColor Yellow
    
    # Try flask db init
    & flask db init 2>$null
    
    # Create initial migration
    & flask db migrate -m "Initial migration" 2>$null
    
    # Apply migrations
    & flask db upgrade 2>$null
    
    if (Test-Path $dbFile) {
        Write-Host "✓ Database initialized" -ForegroundColor Green
    } else {
        Write-Host "⚠ Database initialization using flask-migrate encountered issues" -ForegroundColor Yellow
        Write-Host "  Trying alternative method..." -ForegroundColor Yellow
        
        # Fallback: Create database directly
        & python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✓ Database created with fallback method')"
    }
} else {
    Write-Host "Database already exists at $dbFile" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Ensure .env file is configured in the project root" -ForegroundColor White
Write-Host "  2. Run the Flask development server:" -ForegroundColor White
Write-Host "     python app.py" -ForegroundColor Yellow
Write-Host "  3. The API will be available at http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  - Run migrations: flask db migrate -m 'Description'" -ForegroundColor Yellow
Write-Host "  - Run server: python app.py" -ForegroundColor Yellow
Write-Host "  - Flask shell: flask shell" -ForegroundColor Yellow
Write-Host "  - Run tests: pytest" -ForegroundColor Yellow
Write-Host ""
Write-Host "To deactivate virtual environment later, run: deactivate" -ForegroundColor Gray
