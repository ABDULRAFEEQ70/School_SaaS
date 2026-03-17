#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Verifies that the School SaaS development environment is properly set up
.DESCRIPTION
    Checks Python, virtual environment, installed packages, and database
.EXAMPLE
    .\verify_setup.ps1
#>

$checks_passed = 0
$checks_failed = 0

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "School SaaS - Setup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check 1: Python Installation
Write-Host "1. Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = & python --version 2>&1
    Write-Host "   ✓ Python found: $pythonVersion" -ForegroundColor Green
    $checks_passed++
} else {
    Write-Host "   ✗ Python not found in PATH" -ForegroundColor Red
    Write-Host "   → Install Python 3.9+ from https://www.python.org/" -ForegroundColor Yellow
    $checks_failed++
}

# Check 2: Virtual Environment
Write-Host ""
Write-Host "2. Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   ✓ Virtual environment exists" -ForegroundColor Green
    $checks_passed++
} else {
    Write-Host "   ✗ Virtual environment not found" -ForegroundColor Red
    Write-Host "   → Run: python -m venv venv" -ForegroundColor Yellow
    $checks_failed++
}

# Check 3: .env File
Write-Host ""
Write-Host "3. Checking configuration file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✓ .env file exists" -ForegroundColor Green
    
    # Check if it has expected variables
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "FLASK_APP") {
        Write-Host "   ✓ FLASK_APP configured" -ForegroundColor Green
        $checks_passed++
    } else {
        Write-Host "   ✗ FLASK_APP not configured in .env" -ForegroundColor Red
        $checks_failed++
    }
    
    if ($envContent -match "SQLALCHEMY_DATABASE_URI") {
        Write-Host "   ✓ Database URI configured" -ForegroundColor Green
        $checks_passed++
    } else {
        Write-Host "   ✗ Database URI not configured in .env" -ForegroundColor Red
        $checks_failed++
    }
} else {
    Write-Host "   ✗ .env file not found" -ForegroundColor Red
    Write-Host "   → Create from example: copy .env.example .env" -ForegroundColor Yellow
    $checks_failed++
}

# Check 4: Database File
Write-Host ""
Write-Host "4. Checking database..." -ForegroundColor Yellow
if (Test-Path "data.db") {
    $dbSize = (Get-Item "data.db").Length
    Write-Host "   ✓ Database file exists ($($dbSize) bytes)" -ForegroundColor Green
    $checks_passed++
} else {
    Write-Host "   ℹ Database file not found (will be created on first run)" -ForegroundColor Cyan
}

# Check 5: Required Python Packages
Write-Host ""
Write-Host "5. Checking Python packages..." -ForegroundColor Yellow

# Activate venv if possible
$activateScript = "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript -ErrorAction SilentlyContinue
    $venvActive = $true
} else {
    $venvActive = $false
}

if ($venvActive -or $pythonCmd) {
    # Check for required packages
    $requiredPackages = @("flask", "flask_sqlalchemy", "flask_jwt_extended", "flask_cors")
    $packagesOK = $true
    
    foreach ($package in $requiredPackages) {
        $installed = & python -c "import importlib.util; exit(0 if importlib.util.find_spec('$package'.replace('_', '-')) else 1)" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✓ $package installed" -ForegroundColor Green
        } else {
            Write-Host "   ✗ $package not installed" -ForegroundColor Red
            $packagesOK = $false
        }
    }
    
    if ($packagesOK) {
        $checks_passed++
    } else {
        Write-Host "   → Run: pip install -r requirements.txt" -ForegroundColor Yellow
        $checks_failed++
    }
} else {
    Write-Host "   ℹ Skipping package check (activate venv first)" -ForegroundColor Cyan
}

# Check 6: Core Application Files
Write-Host ""
Write-Host "6. Checking application files..." -ForegroundColor Yellow
$appFiles = @("app.py", "config.py", "models.py", "routes.py", "services.py", "utils.py", "requirements.txt")
$filesOK = $true

foreach ($file in $appFiles) {
    if (Test-Path $file) {
        Write-Host "   ✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "   ✗ $file missing" -ForegroundColor Red
        $filesOK = $false
    }
}

if ($filesOK) {
    $checks_passed++
} else {
    Write-Host "   → Ensure you have all application files" -ForegroundColor Yellow
    $checks_failed++
}

# Check 7: Documentation
Write-Host ""
Write-Host "7. Checking documentation..." -ForegroundColor Yellow
$docFiles = @("README.md", "QUICKSTART.md", "LOCAL_SETUP.md", "VERIFICATION.md")
foreach ($docFile in $docFiles) {
    if (Test-Path $docFile) {
        Write-Host "   ✓ $docFile found" -ForegroundColor Green
    } else {
        Write-Host "   ℹ $docFile not found" -ForegroundColor Cyan
    }
}
$checks_passed++

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Checks passed: $checks_passed" -ForegroundColor Green
Write-Host "✗ Checks failed: $checks_failed" -ForegroundColor $(if ($checks_failed -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($checks_failed -eq 0) {
    Write-Host "🎉 Everything looks good!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Activate virtual environment:" -ForegroundColor White
    Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  2. Run the application:" -ForegroundColor White
    Write-Host "     python app.py" -ForegroundColor Yellow
    Write-Host "  3. Test the API:" -ForegroundColor White
    Write-Host "     Invoke-WebRequest http://localhost:5000/health" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  Some issues were found. See above for details." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Solutions:" -ForegroundColor Cyan
    Write-Host "  • Run setup script: .\setup.ps1" -ForegroundColor White
    Write-Host "  • Check LOCAL_SETUP.md for troubleshooting" -ForegroundColor White
    Write-Host "  • See VERIFICATION.md for more help" -ForegroundColor White
}

Write-Host ""
