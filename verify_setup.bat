@echo off
REM Verification script for School SaaS development environment

setlocal enabledelayedexpansion
set CHECKS_PASSED=0
set CHECKS_FAILED=0

echo.
echo ========================================
echo School SaaS - Setup Verification
echo ========================================
echo.

REM Check 1: Python Installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Python not found in PATH
    echo Install Python 3.9+ from https://www.python.org/
    set /a CHECKS_FAILED+=1
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo [OK] Python found: !PYTHON_VERSION!
    set /a CHECKS_PASSED+=1
)
echo.

REM Check 2: Virtual Environment
echo Checking virtual environment...
if exist "venv" (
    echo [OK] Virtual environment exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAILED] Virtual environment not found
    echo Run: python -m venv venv
    set /a CHECKS_FAILED+=1
)
echo.

REM Check 3: .env File
echo Checking configuration file...
if exist ".env" (
    echo [OK] .env file exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAILED] .env file not found
    echo Create from example: copy .env.example .env
    set /a CHECKS_FAILED+=1
)
echo.

REM Check 4: Database File
echo Checking database...
if exist "data.db" (
    echo [OK] Database file exists
    set /a CHECKS_PASSED+=1
) else (
    echo [INFO] Database file not found (will be created on first run)
)
echo.

REM Check 5: Application Files
echo Checking application files...
set FILES_OK=1
for %%f in (app.py config.py models.py routes.py services.py utils.py requirements.txt) do (
    if exist "%%f" (
        echo [OK] %%f exists
    ) else (
        echo [FAILED] %%f missing
        set FILES_OK=0
        set /a CHECKS_FAILED+=1
    )
)
if !FILES_OK!==1 (
    set /a CHECKS_PASSED+=1
)
echo.

REM Check 6: Documentation
echo Checking documentation...
for %%f in (README.md QUICKSTART.md LOCAL_SETUP.md VERIFICATION.md) do (
    if exist "%%f" (
        echo [OK] %%f found
    ) else (
        echo [INFO] %%f not found
    )
)
set /a CHECKS_PASSED+=1
echo.

echo ========================================
echo Verification Summary
echo ========================================
echo.
echo Checks passed: !CHECKS_PASSED!
echo Checks failed: !CHECKS_FAILED!
echo.

if !CHECKS_FAILED!==0 (
    echo Success! Everything looks good.
    echo.
    echo Next steps:
    echo   1. Activate virtual environment:
    echo      venv\Scripts\activate.bat
    echo   2. Run the application:
    echo      python app.py
    echo   3. Test the API:
    echo      Open http://localhost:5000/health in browser
) else (
    echo Warning: Some issues were found (see above).
    echo.
    echo Solutions:
    echo   - Run setup script: setup.bat
    echo   - Check LOCAL_SETUP.md for troubleshooting
    echo   - See VERIFICATION.md for more help
)

echo.
pause

REM Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0   # optional
